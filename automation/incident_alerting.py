#!/usr/bin/env python3
"""
AUDITORIA360 - Enhanced Incident Alerting System
Advanced monitoring with notifications and automated issue creation
"""

import os
import json
import requests
import logging
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class IncidentAlert:
    """Data class for incident alerts"""
    severity: str  # critical, high, medium, low
    module_name: str
    status: str
    details: str
    timestamp: str
    response_time: float = None
    url: str = None

class AlertingSystem:
    """Enhanced alerting system for AUDITORIA360"""
    
    def __init__(self):
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        self.email_smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        self.email_smtp_port = int(os.getenv('EMAIL_SMTP_PORT', '587'))
        self.email_username = os.getenv('EMAIL_USERNAME')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.alert_recipients = os.getenv('ALERT_RECIPIENTS', '').split(',')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repo = os.getenv('GITHUB_REPOSITORY', 'Thaislaine997/AUDITORIA360')
        
    def analyze_health_status(self, status_file: str = 'status_report_auditoria360.json') -> List[IncidentAlert]:
        """Analyze health status and generate alerts for issues"""
        alerts = []
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                status_data = json.load(f)
                
            for module in status_data.get('modules', []):
                alert = self._evaluate_module_status(module)
                if alert:
                    alerts.append(alert)
                    
            # System-level alerts
            system_health = status_data.get('system_health', {})
            if system_health.get('status') == 'critical':
                alerts.append(IncidentAlert(
                    severity='critical',
                    module_name='SYSTEM_OVERALL',
                    status='CRITICAL',
                    details=f'System health critical: {system_health.get("score", 0)}% operational',
                    timestamp=datetime.now().isoformat()
                ))
                
        except FileNotFoundError:
            logger.error(f"Status file {status_file} not found")
            alerts.append(IncidentAlert(
                severity='critical',
                module_name='MONITORING',
                status='ERROR',
                details='Health monitoring system failure - status file not found',
                timestamp=datetime.now().isoformat()
            ))
        except Exception as e:
            logger.error(f"Error analyzing health status: {str(e)}")
            
        return alerts
    
    def _evaluate_module_status(self, module: Dict[str, Any]) -> IncidentAlert:
        """Evaluate individual module status and create alert if needed"""
        status = module.get('status', '').upper()
        name = module.get('name', 'UNKNOWN')
        details = module.get('details', '')
        response_time = module.get('response_time')
        
        # Critical conditions
        if status in ['ERRO', 'ERRO DE CONEXÃO', 'TIMEOUT']:
            return IncidentAlert(
                severity='critical',
                module_name=name,
                status=status,
                details=details,
                timestamp=module.get('last_check', datetime.now().isoformat()),
                response_time=response_time,
                url=module.get('url')
            )
        
        # High severity conditions
        if response_time and response_time > 5.0:  # > 5 seconds
            return IncidentAlert(
                severity='high',
                module_name=name,
                status='SLOW_RESPONSE',
                details=f'Response time {response_time:.2f}s exceeds threshold (5s)',
                timestamp=module.get('last_check', datetime.now().isoformat()),
                response_time=response_time,
                url=module.get('url')
            )
        
        # Medium severity - monitoring development modules
        if status == 'EM DESENVOLVIMENTO' and 'crítico' in details.lower():
            return IncidentAlert(
                severity='medium',
                module_name=name,
                status=status,
                details=f'Critical module in development: {details}',
                timestamp=module.get('last_check', datetime.now().isoformat()),
                response_time=response_time
            )
        
        return None
    
    def send_slack_alert(self, alert: IncidentAlert) -> bool:
        """Send alert to Slack channel"""
        if not self.slack_webhook_url:
            logger.warning("Slack webhook URL not configured")
            return False
            
        try:
            severity_emoji = {
                'critical': '🚨',
                'high': '⚠️',
                'medium': '🟡',
                'low': '🔵'
            }
            
            message = {
                "text": f"{severity_emoji.get(alert.severity, '⚠️')} AUDITORIA360 Alert",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{severity_emoji.get(alert.severity, '⚠️')} AUDITORIA360 System Alert"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Severity:* {alert.severity.upper()}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Module:* {alert.module_name}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Status:* {alert.status}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Time:* {alert.timestamp}"
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Details:* {alert.details}"
                        }
                    }
                ]
            }
            
            if alert.response_time:
                message["blocks"].append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Response Time:* {alert.response_time:.3f}s"
                    }
                })
            
            response = requests.post(self.slack_webhook_url, json=message, timeout=10)
            response.raise_for_status()
            logger.info(f"Slack alert sent for {alert.module_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {str(e)}")
            return False
    
    def send_email_alert(self, alert: IncidentAlert) -> bool:
        """Send email alert"""
        if not self.email_username or not self.email_password or not self.alert_recipients:
            logger.warning("Email configuration incomplete")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_username
            msg['To'] = ', '.join(self.alert_recipients)
            msg['Subject'] = f"AUDITORIA360 Alert: {alert.severity.upper()} - {alert.module_name}"
            
            body = f"""
AUDITORIA360 System Alert

Severity: {alert.severity.upper()}
Module: {alert.module_name}
Status: {alert.status}
Time: {alert.timestamp}

Details: {alert.details}
"""
            
            if alert.response_time:
                body += f"\nResponse Time: {alert.response_time:.3f}s"
            
            if alert.url:
                body += f"\nEndpoint: {alert.url}"
            
            body += f"""

This is an automated alert from the AUDITORIA360 monitoring system.
Please investigate and take appropriate action.

Dashboard: https://github.com/{self.github_repo}
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_smtp_server, self.email_smtp_port)
            server.starttls()
            server.login(self.email_username, self.email_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email alert sent for {alert.module_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")
            return False
    
    def create_github_issue(self, alert: IncidentAlert) -> bool:
        """Create GitHub issue for critical alerts"""
        if not self.github_token or alert.severity not in ['critical', 'high']:
            return False
            
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            title = f"🚨 {alert.severity.upper()}: {alert.module_name} - {alert.status}"
            
            body = f"""
## System Alert - Automated Issue Creation

**Alert Details:**
- **Severity**: {alert.severity.upper()}
- **Module**: {alert.module_name}
- **Status**: {alert.status}
- **Timestamp**: {alert.timestamp}

**Issue Description:**
{alert.details}

**Technical Information:**
"""
            
            if alert.response_time:
                body += f"- **Response Time**: {alert.response_time:.3f}s\n"
            
            if alert.url:
                body += f"- **Endpoint**: {alert.url}\n"
            
            body += f"""
**Recommended Actions:**
1. Investigate the affected module immediately
2. Check logs for detailed error information
3. Verify system dependencies and connections
4. Update status once resolved

**Context:**
This issue was automatically created by the AUDITORIA360 monitoring system.
Alert triggered at {alert.timestamp}.

---
*Auto-generated by AUDITORIA360 Incident Management System*
"""
            
            issue_data = {
                'title': title,
                'body': body,
                'labels': [
                    'bug',
                    'automated-alert',
                    f'severity-{alert.severity}',
                    'monitoring'
                ]
            }
            
            url = f"https://api.github.com/repos/{self.github_repo}/issues"
            response = requests.post(url, json=issue_data, headers=headers, timeout=30)
            response.raise_for_status()
            
            issue_url = response.json().get('html_url', '')
            logger.info(f"GitHub issue created: {issue_url}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create GitHub issue: {str(e)}")
            return False
    
    def process_alerts(self, alerts: List[IncidentAlert]) -> Dict[str, int]:
        """Process all alerts and send notifications"""
        results = {
            'slack_sent': 0,
            'email_sent': 0,
            'github_issues': 0
        }
        
        for alert in alerts:
            logger.info(f"Processing {alert.severity} alert for {alert.module_name}")
            
            # Send Slack notification
            if self.send_slack_alert(alert):
                results['slack_sent'] += 1
            
            # Send email for medium+ severity
            if alert.severity in ['critical', 'high', 'medium']:
                if self.send_email_alert(alert):
                    results['email_sent'] += 1
            
            # Create GitHub issue for critical/high severity
            if alert.severity in ['critical', 'high']:
                if self.create_github_issue(alert):
                    results['github_issues'] += 1
        
        return results
    
    def generate_incident_report(self, alerts: List[IncidentAlert]) -> str:
        """Generate incident report"""
        if not alerts:
            return "No incidents to report - all systems operational."
        
        report = f"""# Incident Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
Total Incidents: {len(alerts)}
- Critical: {len([a for a in alerts if a.severity == 'critical'])}
- High: {len([a for a in alerts if a.severity == 'high'])}
- Medium: {len([a for a in alerts if a.severity == 'medium'])}
- Low: {len([a for a in alerts if a.severity == 'low'])}

## Incident Details
"""
        
        for alert in sorted(alerts, key=lambda x: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}[x.severity]):
            report += f"""
### {alert.severity.upper()}: {alert.module_name}
- **Status**: {alert.status}
- **Time**: {alert.timestamp}
- **Details**: {alert.details}
"""
            if alert.response_time:
                report += f"- **Response Time**: {alert.response_time:.3f}s\n"
            if alert.url:
                report += f"- **Endpoint**: {alert.url}\n"
        
        report += f"""
## Actions Taken
- Notifications sent to configured channels
- Critical/High severity incidents escalated to GitHub issues
- System monitoring continues every 5 minutes

---
*Generated by AUDITORIA360 Incident Management System*
"""
        
        return report

def main():
    """Main function for incident alerting"""
    logger.info("Starting AUDITORIA360 incident alerting system...")
    
    alerting = AlertingSystem()
    
    # Analyze current system status
    alerts = alerting.analyze_health_status()
    
    if not alerts:
        logger.info("No incidents detected - all systems operational")
        return 0
    
    logger.info(f"Processing {len(alerts)} alerts...")
    
    # Process alerts and send notifications
    results = alerting.process_alerts(alerts)
    
    # Generate incident report
    incident_report = alerting.generate_incident_report(alerts)
    
    # Save incident report
    report_filename = f"incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(incident_report)
    
    logger.info(f"Incident processing completed:")
    logger.info(f"- Slack notifications: {results['slack_sent']}")
    logger.info(f"- Email alerts: {results['email_sent']}")
    logger.info(f"- GitHub issues: {results['github_issues']}")
    logger.info(f"- Report saved: {report_filename}")
    
    # Return non-zero exit code if critical incidents detected
    critical_count = len([a for a in alerts if a.severity == 'critical'])
    return 1 if critical_count > 0 else 0

if __name__ == "__main__":
    exit(main())