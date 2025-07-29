"""
Enhanced Monitoring System for AUDITORIA360
Implements comprehensive metrics collection, alerting, and real-time monitoring.
"""

import asyncio
import json
import logging
import os
import threading
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import psutil
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MetricType(Enum):
    """Types of metrics"""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class Metric:
    """Metric data structure"""

    name: str
    value: Union[int, float]
    metric_type: MetricType
    timestamp: datetime
    labels: Dict[str, str] = field(default_factory=dict)
    help_text: Optional[str] = None


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


@dataclass
class HealthCheck:
    """Health check result structure"""

    name: str
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: datetime
    response_time_ms: float
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class MetricsCollector:
    """Collects and stores application metrics"""

    def __init__(self):
        self.metrics: Dict[str, List[Metric]] = {}
        self._lock = threading.Lock()
        self.retention_hours = 24

    def record_metric(
        self,
        name: str,
        value: Union[int, float],
        metric_type: MetricType,
        labels: Dict[str, str] = None,
        help_text: str = None,
    ):
        """Record a metric"""
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            timestamp=datetime.now(),
            labels=labels or {},
            help_text=help_text,
        )

        with self._lock:
            if name not in self.metrics:
                self.metrics[name] = []
            self.metrics[name].append(metric)
            self._cleanup_old_metrics(name)

    def increment_counter(
        self, name: str, labels: Dict[str, str] = None, amount: int = 1
    ):
        """Increment a counter metric"""
        current_value = self.get_latest_value(name) or 0
        self.record_metric(name, current_value + amount, MetricType.COUNTER, labels)

    def set_gauge(
        self, name: str, value: Union[int, float], labels: Dict[str, str] = None
    ):
        """Set a gauge metric"""
        self.record_metric(name, value, MetricType.GAUGE, labels)

    def record_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record a histogram value"""
        self.record_metric(name, value, MetricType.HISTOGRAM, labels)

    def get_latest_value(self, name: str) -> Optional[Union[int, float]]:
        """Get the latest value for a metric"""
        with self._lock:
            if name not in self.metrics or not self.metrics[name]:
                return None
            return self.metrics[name][-1].value

    def get_metrics_summary(self, hours: int = 1) -> Dict[str, Any]:
        """Get summary of metrics for the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        summary = {}

        with self._lock:
            for metric_name, metric_list in self.metrics.items():
                recent_metrics = [m for m in metric_list if m.timestamp >= cutoff]
                if not recent_metrics:
                    continue

                values = [m.value for m in recent_metrics]
                summary[metric_name] = {
                    "count": len(recent_metrics),
                    "latest": values[-1] if values else None,
                    "min": min(values) if values else None,
                    "max": max(values) if values else None,
                    "avg": sum(values) / len(values) if values else None,
                    "type": recent_metrics[0].metric_type.value,
                }

        return summary

    def _cleanup_old_metrics(self, name: str):
        """Remove metrics older than retention period"""
        cutoff = datetime.now() - timedelta(hours=self.retention_hours)
        self.metrics[name] = [m for m in self.metrics[name] if m.timestamp >= cutoff]


class SystemMonitor:
    """Monitors system resources and application health"""

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        self.monitoring = False
        self.monitor_thread = None
        self.interval = 30  # seconds

    def start_monitoring(self):
        """Start continuous system monitoring"""
        if self.monitoring:
            return

        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("System monitoring started")

    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("System monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                self._collect_system_metrics()
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.interval)

    def _collect_system_metrics(self):
        """Collect system metrics"""
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        self.metrics.set_gauge("system_cpu_percent", cpu_percent, {"type": "overall"})

        # Memory metrics
        memory = psutil.virtual_memory()
        self.metrics.set_gauge(
            "system_memory_percent", memory.percent, {"type": "virtual"}
        )
        self.metrics.set_gauge(
            "system_memory_available_bytes", memory.available, {"type": "virtual"}
        )
        self.metrics.set_gauge(
            "system_memory_used_bytes", memory.used, {"type": "virtual"}
        )

        # Disk metrics
        disk = psutil.disk_usage("/")
        self.metrics.set_gauge("system_disk_percent", disk.percent, {"mountpoint": "/"})
        self.metrics.set_gauge("system_disk_free_bytes", disk.free, {"mountpoint": "/"})

        # Network metrics
        net_io = psutil.net_io_counters()
        self.metrics.set_gauge(
            "system_network_bytes_sent", net_io.bytes_sent, {"direction": "sent"}
        )
        self.metrics.set_gauge(
            "system_network_bytes_recv", net_io.bytes_recv, {"direction": "received"}
        )

        # Process metrics
        process = psutil.Process()
        self.metrics.set_gauge(
            "process_memory_percent",
            process.memory_percent(),
            {"type": "current_process"},
        )
        self.metrics.set_gauge(
            "process_cpu_percent", process.cpu_percent(), {"type": "current_process"}
        )


class AlertManager:
    """Manages alerts and notifications"""

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        self.alerts: List[Alert] = []
        self.alert_rules: List[Dict[str, Any]] = []
        self.notification_channels: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self.evaluation_interval = 60  # seconds
        self.evaluating = False
        self.evaluation_thread = None

    def add_alert_rule(
        self,
        metric_name: str,
        threshold: Union[int, float],
        condition: str,
        severity: AlertSeverity,
        title: str,
        description: str,
    ):
        """Add an alert rule"""
        rule = {
            "metric_name": metric_name,
            "threshold": threshold,
            "condition": condition,  # 'gt', 'lt', 'gte', 'lte', 'eq'
            "severity": severity,
            "title": title,
            "description": description,
            "enabled": True,
        }
        self.alert_rules.append(rule)
        logger.info(f"Added alert rule: {title}")

    def add_notification_channel(self, channel_type: str, config: Dict[str, Any]):
        """Add a notification channel (email, webhook, slack, etc.)"""
        channel = {"type": channel_type, "config": config, "enabled": True}
        self.notification_channels.append(channel)
        logger.info(f"Added notification channel: {channel_type}")

    def start_evaluation(self):
        """Start continuous alert evaluation"""
        if self.evaluating:
            return

        self.evaluating = True
        self.evaluation_thread = threading.Thread(
            target=self._evaluation_loop, daemon=True
        )
        self.evaluation_thread.start()
        logger.info("Alert evaluation started")

    def stop_evaluation(self):
        """Stop alert evaluation"""
        self.evaluating = False
        if self.evaluation_thread:
            self.evaluation_thread.join(timeout=5)
        logger.info("Alert evaluation stopped")

    def _evaluation_loop(self):
        """Main alert evaluation loop"""
        while self.evaluating:
            try:
                self._evaluate_rules()
                time.sleep(self.evaluation_interval)
            except Exception as e:
                logger.error(f"Error in alert evaluation: {e}")
                time.sleep(self.evaluation_interval)

    def _evaluate_rules(self):
        """Evaluate all alert rules"""
        for rule in self.alert_rules:
            if not rule["enabled"]:
                continue

            try:
                self._evaluate_rule(rule)
            except Exception as e:
                logger.error(f"Error evaluating rule {rule['title']}: {e}")

    def _evaluate_rule(self, rule: Dict[str, Any]):
        """Evaluate a single alert rule"""
        metric_value = self.metrics.get_latest_value(rule["metric_name"])
        if metric_value is None:
            return

        threshold = rule["threshold"]
        condition = rule["condition"]

        triggered = False

        if condition == "gt" and metric_value > threshold:
            triggered = True
        elif condition == "lt" and metric_value < threshold:
            triggered = True
        elif condition == "gte" and metric_value >= threshold:
            triggered = True
        elif condition == "lte" and metric_value <= threshold:
            triggered = True
        elif condition == "eq" and metric_value == threshold:
            triggered = True

        if triggered:
            self._trigger_alert(rule, metric_value)

    def _trigger_alert(self, rule: Dict[str, Any], current_value: Union[int, float]):
        """Trigger an alert"""
        alert_id = f"{rule['metric_name']}_{int(time.time())}"

        # Check if similar alert already exists and is not resolved
        existing_alert = self._find_existing_alert(rule["metric_name"])
        if existing_alert and not existing_alert.resolved:
            return  # Don't spam with duplicate alerts

        alert = Alert(
            id=alert_id,
            title=rule["title"],
            description=rule["description"],
            severity=rule["severity"],
            timestamp=datetime.now(),
            metric_name=rule["metric_name"],
            current_value=current_value,
            threshold=rule["threshold"],
        )

        with self._lock:
            self.alerts.append(alert)

        logger.warning(f"Alert triggered: {alert.title} - {alert.description}")
        self._send_notifications(alert)

    def _find_existing_alert(self, metric_name: str) -> Optional[Alert]:
        """Find existing unresolved alert for metric"""
        with self._lock:
            for alert in reversed(self.alerts):  # Check most recent first
                if alert.metric_name == metric_name and not alert.resolved:
                    return alert
        return None

    def _send_notifications(self, alert: Alert):
        """Send alert notifications through configured channels"""
        for channel in self.notification_channels:
            if not channel["enabled"]:
                continue

            try:
                if channel["type"] == "email":
                    self._send_email_notification(alert, channel["config"])
                elif channel["type"] == "webhook":
                    self._send_webhook_notification(alert, channel["config"])
                elif channel["type"] == "slack":
                    self._send_slack_notification(alert, channel["config"])
            except Exception as e:
                logger.error(f"Failed to send {channel['type']} notification: {e}")

    def _send_email_notification(self, alert: Alert, config: Dict[str, Any]):
        """Send email notification"""
        if not EMAIL_AVAILABLE:
            logger.warning("Email notifications not available - skipping")
            return

        msg = MIMEMultipart()
        msg["From"] = config["from_email"]
        msg["To"] = ", ".join(config["to_emails"])
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

This is an automated alert from AUDITORIA360 monitoring system.
        """

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.starttls()
            server.login(config["username"], config["password"])
            server.send_message(msg)

    def _send_webhook_notification(self, alert: Alert, config: Dict[str, Any]):
        """Send webhook notification"""
        payload = {
            "alert": asdict(alert),
            "timestamp": alert.timestamp.isoformat(),
            "severity": alert.severity.value,
        }

        response = requests.post(
            config["url"], json=payload, headers=config.get("headers", {}), timeout=10
        )
        response.raise_for_status()

    def _send_slack_notification(self, alert: Alert, config: Dict[str, Any]):
        """Send Slack notification"""
        color_map = {
            AlertSeverity.LOW: "good",
            AlertSeverity.MEDIUM: "warning",
            AlertSeverity.HIGH: "danger",
            AlertSeverity.CRITICAL: "danger",
        }

        payload = {
            "attachments": [
                {
                    "color": color_map.get(alert.severity, "warning"),
                    "title": f"[{alert.severity.value.upper()}] {alert.title}",
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
                            "title": "Time",
                            "value": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                            "short": True,
                        },
                    ],
                }
            ]
        }

        response = requests.post(config["webhook_url"], json=payload, timeout=10)
        response.raise_for_status()

    def get_active_alerts(self) -> List[Alert]:
        """Get all active (unresolved) alerts"""
        with self._lock:
            return [alert for alert in self.alerts if not alert.resolved]

    def resolve_alert(self, alert_id: str):
        """Resolve an alert"""
        with self._lock:
            for alert in self.alerts:
                if alert.id == alert_id:
                    alert.resolved = True
                    alert.resolved_at = datetime.now()
                    logger.info(f"Alert resolved: {alert.title}")
                    break


class HealthChecker:
    """Performs health checks on various system components"""

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
        self.health_checks: List[Dict[str, Any]] = []
        self.results: List[HealthCheck] = []
        self._lock = threading.Lock()

    def add_health_check(self, name: str, check_func: Callable, interval: int = 60):
        """Add a health check"""
        health_check = {
            "name": name,
            "check_func": check_func,
            "interval": interval,
            "last_run": None,
            "enabled": True,
        }
        self.health_checks.append(health_check)
        logger.info(f"Added health check: {name}")

    async def run_all_checks(self) -> List[HealthCheck]:
        """Run all health checks"""
        results = []
        for check in self.health_checks:
            if not check["enabled"]:
                continue

            try:
                result = await self._run_check(check)
                results.append(result)
            except Exception as e:
                result = HealthCheck(
                    name=check["name"],
                    status="unhealthy",
                    timestamp=datetime.now(),
                    response_time_ms=0,
                    error=str(e),
                )
                results.append(result)

        with self._lock:
            self.results = results

        return results

    async def _run_check(self, check: Dict[str, Any]) -> HealthCheck:
        """Run a single health check"""
        start_time = time.time()

        try:
            if asyncio.iscoroutinefunction(check["check_func"]):
                result = await check["check_func"]()
            else:
                result = check["check_func"]()

            response_time = (time.time() - start_time) * 1000  # ms

            if isinstance(result, dict):
                status = result.get("status", "healthy")
                details = result.get("details", {})
                error = result.get("error")
            else:
                status = "healthy" if result else "unhealthy"
                details = {}
                error = None

            health_check = HealthCheck(
                name=check["name"],
                status=status,
                timestamp=datetime.now(),
                response_time_ms=response_time,
                details=details,
                error=error,
            )

            # Record metrics
            self.metrics.set_gauge(
                f"health_check_response_time_ms",
                response_time,
                {"check_name": check["name"]},
            )
            self.metrics.set_gauge(
                f"health_check_status",
                1 if status == "healthy" else 0,
                {"check_name": check["name"]},
            )

            check["last_run"] = datetime.now()
            return health_check

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheck(
                name=check["name"],
                status="unhealthy",
                timestamp=datetime.now(),
                response_time_ms=response_time,
                error=str(e),
            )


class MonitoringSystem:
    """Main monitoring system coordinator"""

    def __init__(self):
        self.metrics = MetricsCollector()
        self.system_monitor = SystemMonitor(self.metrics)
        self.alert_manager = AlertManager(self.metrics)
        self.health_checker = HealthChecker(self.metrics)
        self._setup_default_alerts()

    def start(self):
        """Start all monitoring components"""
        self.system_monitor.start_monitoring()
        self.alert_manager.start_evaluation()
        logger.info("Monitoring system started")

    def stop(self):
        """Stop all monitoring components"""
        self.system_monitor.stop_monitoring()
        self.alert_manager.stop_evaluation()
        logger.info("Monitoring system stopped")

    def _setup_default_alerts(self):
        """Setup default alert rules"""
        # CPU alerts
        self.alert_manager.add_alert_rule(
            "system_cpu_percent",
            80,
            "gt",
            AlertSeverity.HIGH,
            "High CPU Usage",
            "CPU usage is above 80%",
        )

        # Memory alerts
        self.alert_manager.add_alert_rule(
            "system_memory_percent",
            85,
            "gt",
            AlertSeverity.HIGH,
            "High Memory Usage",
            "Memory usage is above 85%",
        )

        # Disk alerts
        self.alert_manager.add_alert_rule(
            "system_disk_percent",
            90,
            "gt",
            AlertSeverity.CRITICAL,
            "High Disk Usage",
            "Disk usage is above 90%",
        )

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for monitoring dashboard"""
        return {
            "metrics_summary": self.metrics.get_metrics_summary(hours=1),
            "active_alerts": [
                asdict(alert) for alert in self.alert_manager.get_active_alerts()
            ],
            "health_checks": [asdict(result) for result in self.health_checker.results],
            "system_status": self._get_system_status(),
        }

    def _get_system_status(self) -> str:
        """Get overall system status"""
        active_alerts = self.alert_manager.get_active_alerts()

        if any(alert.severity == AlertSeverity.CRITICAL for alert in active_alerts):
            return "critical"
        elif any(alert.severity == AlertSeverity.HIGH for alert in active_alerts):
            return "degraded"
        elif active_alerts:
            return "warning"
        else:
            return "healthy"


# Global monitoring instance
monitoring = MonitoringSystem()


def get_monitoring_system() -> MonitoringSystem:
    """Get the global monitoring system instance"""
    return monitoring
