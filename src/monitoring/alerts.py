"""
Alert management and notification system for AUDITORIA360 monitoring
"""

import logging
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import requests

# Email imports with fallback
try:
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    logging.warning("Email functionality not available")

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Alert:
    """Alert data structure"""

    id: str
    title: str
    description: str
    severity: AlertSeverity
    timestamp: datetime
    metric_name: str
    current_value: Union[int, float]
    threshold: Union[int, float]
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    labels: Dict[str, str] = field(default_factory=dict)


class AlertManager:
    """Manages alerts and notifications"""

    def __init__(self):
        self.alerts: List[Alert] = []
        self.alert_rules: Dict[str, Dict[str, Any]] = {}
        self.notification_configs: List[Dict[str, Any]] = []

    def add_alert_rule(
        self,
        metric_name: str,
        threshold: Union[int, float],
        comparison: str = "greater_than",
        severity: AlertSeverity = AlertSeverity.MEDIUM,
        title: str = None,
        description: str = None,
    ):
        """Add an alert rule for a metric"""
        self.alert_rules[metric_name] = {
            "threshold": threshold,
            "comparison": comparison,
            "severity": severity,
            "title": title or f"Alert for {metric_name}",
            "description": description or f"Metric {metric_name} threshold exceeded",
        }

    def add_notification_config(self, config: Dict[str, Any]):
        """Add notification configuration (email, webhook, slack)"""
        self.notification_configs.append(config)

    def check_metric_alerts(self, metric_name: str, value: Union[int, float]):
        """Check if a metric value triggers any alerts"""
        if metric_name not in self.alert_rules:
            return

        rule = self.alert_rules[metric_name]
        threshold = rule["threshold"]
        comparison = rule["comparison"]

        alert_triggered = False
        if comparison == "greater_than" and value > threshold:
            alert_triggered = True
        elif comparison == "less_than" and value < threshold:
            alert_triggered = True
        elif comparison == "equal" and value == threshold:
            alert_triggered = True

        if alert_triggered:
            self._create_alert(metric_name, value, rule)
        else:
            # Check if we need to resolve existing alerts
            self._check_alert_resolution(metric_name)

    def _create_alert(
        self, metric_name: str, value: Union[int, float], rule: Dict[str, Any]
    ):
        """Create a new alert"""
        # Check if alert already exists and is active
        existing_alert = self._find_existing_alert(metric_name)
        if existing_alert and not existing_alert.resolved:
            return  # Don't create duplicate alerts

        alert_id = str(uuid.uuid4())
        alert = Alert(
            id=alert_id,
            title=rule["title"],
            description=rule["description"],
            severity=rule["severity"],
            timestamp=datetime.now(),
            metric_name=metric_name,
            current_value=value,
            threshold=rule["threshold"],
        )

        self.alerts.append(alert)
        self._send_notifications(alert)
        logger.warning(f"Alert created: {alert.title} - {alert.description}")

    def _find_existing_alert(self, metric_name: str) -> Optional[Alert]:
        """Find existing active alert for a metric"""
        for alert in self.alerts:
            if alert.metric_name == metric_name and not alert.resolved:
                return alert
        return None

    def _check_alert_resolution(self, metric_name: str):
        """Check if alerts for a metric can be resolved"""
        existing_alert = self._find_existing_alert(metric_name)
        if existing_alert:
            existing_alert.resolved = True
            existing_alert.resolved_at = datetime.now()
            logger.info(f"Alert resolved: {existing_alert.title}")

    def _send_notifications(self, alert: Alert):
        """Send notifications for an alert"""
        for config in self.notification_configs:
            try:
                if config["type"] == "email" and EMAIL_AVAILABLE:
                    self._send_email_notification(alert, config)
                elif config["type"] == "webhook":
                    self._send_webhook_notification(alert, config)
                elif config["type"] == "slack":
                    self._send_slack_notification(alert, config)
            except Exception as e:
                logger.error(f"Failed to send {config['type']} notification: {e}")

    def _send_email_notification(self, alert: Alert, config: Dict[str, Any]):
        """Send email notification"""
        if not EMAIL_AVAILABLE:
            return

        msg = MIMEMultipart()
        msg["From"] = config["smtp_from"]
        msg["To"] = ", ".join(config["recipients"])
        msg["Subject"] = f"[{alert.severity.value.upper()}] {alert.title}"

        body = f"""
        Alert Details:
        - Title: {alert.title}
        - Description: {alert.description}
        - Severity: {alert.severity.value}
        - Metric: {alert.metric_name}
        - Current Value: {alert.current_value}
        - Threshold: {alert.threshold}
        - Timestamp: {alert.timestamp}
        """

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            if config.get("smtp_tls"):
                server.starttls()
            if config.get("smtp_username"):
                server.login(config["smtp_username"], config["smtp_password"])
            server.send_message(msg)

    def _send_webhook_notification(self, alert: Alert, config: Dict[str, Any]):
        """Send webhook notification"""
        payload = {
            "alert": asdict(alert),
            "timestamp": alert.timestamp.isoformat(),
        }

        response = requests.post(
            config["url"],
            json=payload,
            headers=config.get("headers", {}),
            timeout=10,
        )
        response.raise_for_status()

    def _send_slack_notification(self, alert: Alert, config: Dict[str, Any]):
        """Send Slack notification"""
        color_map = {
            AlertSeverity.LOW: "#36a64f",  # green
            AlertSeverity.MEDIUM: "#ff9500",  # orange
            AlertSeverity.HIGH: "#ff0000",  # red
            AlertSeverity.CRITICAL: "#8B0000",  # dark red
        }

        payload = {
            "channel": config["channel"],
            "username": config.get("username", "AUDITORIA360 Monitoring"),
            "attachments": [
                {
                    "color": color_map.get(alert.severity, "#36a64f"),
                    "title": alert.title,
                    "text": alert.description,
                    "fields": [
                        {"title": "Metric", "value": alert.metric_name, "short": True},
                        {
                            "title": "Current Value",
                            "value": str(alert.current_value),
                            "short": True,
                        },
                        {
                            "title": "Threshold",
                            "value": str(alert.threshold),
                            "short": True,
                        },
                        {
                            "title": "Severity",
                            "value": alert.severity.value.upper(),
                            "short": True,
                        },
                    ],
                    "ts": alert.timestamp.timestamp(),
                }
            ],
        }

        response = requests.post(config["webhook_url"], json=payload, timeout=10)
        response.raise_for_status()

    def get_active_alerts(self) -> List[Alert]:
        """Get all active (unresolved) alerts"""
        return [alert for alert in self.alerts if not alert.resolved]

    def resolve_alert(self, alert_id: str):
        """Manually resolve an alert"""
        for alert in self.alerts:
            if alert.id == alert_id and not alert.resolved:
                alert.resolved = True
                alert.resolved_at = datetime.now()
                logger.info(f"Alert manually resolved: {alert.title}")
                break
