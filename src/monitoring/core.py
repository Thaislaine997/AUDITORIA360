"""
Core monitoring system that orchestrates all monitoring components
Enhanced with Prometheus metrics, structured logging, and distributed tracing
"""

import asyncio
import logging
import threading
import time
from typing import Any, Dict

from .alerts import AlertManager, AlertSeverity
from .health import HealthChecker
from .metrics import MetricsCollector
from .system import SystemMonitor

try:
    from .prometheus import get_prometheus_exporter
    from .structured_logging import setup_structured_logging
    from .tracing import setup_tracing

    ENHANCED_MONITORING = True
except ImportError:
    ENHANCED_MONITORING = False

logger = logging.getLogger(__name__)


class MonitoringSystem:
    """Main monitoring system that coordinates all components"""

    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.system_monitor = SystemMonitor(self.metrics_collector)
        self.alert_manager = AlertManager()
        self.health_checker = HealthChecker(self.metrics_collector)
        self.running = False
        self._monitoring_thread = None

        # Enhanced monitoring components
        if ENHANCED_MONITORING:
            self.prometheus_exporter = get_prometheus_exporter(self.metrics_collector)
            self.tracer = setup_tracing("auditoria360")
            setup_structured_logging("INFO", "auditoria360")
            logger.info("Enhanced monitoring features enabled")
        else:
            self.prometheus_exporter = None
            self.tracer = None
            logger.warning("Enhanced monitoring features not available")

    def start(self):
        """Start the monitoring system"""
        if self.running:
            return

        self.running = True
        self._setup_default_alerts()
        self._monitoring_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self._monitoring_thread.start()
        logger.info("Monitoring system started")

    def stop(self):
        """Stop the monitoring system"""
        self.running = False
        if self._monitoring_thread:
            self._monitoring_thread.join()
        logger.info("Monitoring system stopped")

    def _setup_default_alerts(self):
        """Setup default alert rules"""
        # System resource alerts
        self.alert_manager.add_alert_rule(
            "system_cpu_percent",
            80,
            "greater_than",
            AlertSeverity.HIGH,
            "High CPU Usage",
            "CPU usage is above 80%",
        )

        self.alert_manager.add_alert_rule(
            "system_memory_percent",
            85,
            "greater_than",
            AlertSeverity.HIGH,
            "High Memory Usage",
            "Memory usage is above 85%",
        )

        self.alert_manager.add_alert_rule(
            "system_disk_percent",
            90,
            "greater_than",
            AlertSeverity.CRITICAL,
            "Disk Space Critical",
            "Disk usage is above 90%",
        )

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                # Collect system metrics
                self.system_monitor.collect_system_metrics()

                # Check all metrics for alerts
                for metric_name in self.metrics_collector.metrics:
                    latest_value = self.metrics_collector.get_latest_value(metric_name)
                    if latest_value is not None:
                        self.alert_manager.check_metric_alerts(
                            metric_name, latest_value
                        )

                # Run health checks
                asyncio.run(self.health_checker.run_all_checks())

                time.sleep(30)  # Wait 30 seconds between cycles

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)  # Short sleep on error

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for monitoring dashboard"""
        dashboard_data = {
            "metrics_summary": self.metrics_collector.get_metrics_summary(),
            "system_info": self.system_monitor.get_system_info(),
            "active_alerts": [
                alert.__dict__ for alert in self.alert_manager.get_active_alerts()
            ],
            "health_checks": {
                name: check.__dict__
                for name, check in self.health_checker.get_latest_results().items()
            },
            "system_status": self._get_system_status(),
            "enhanced_monitoring": ENHANCED_MONITORING,
        }

        # Add enhanced monitoring data if available
        if ENHANCED_MONITORING and self.tracer:
            recent_traces = self.tracer.collector.get_recent_traces(10)
            dashboard_data["recent_traces"] = {
                trace_id: [span.__dict__ for span in spans]
                for trace_id, spans in recent_traces.items()
            }

        return dashboard_data

    def get_prometheus_metrics(self) -> str:
        """Get Prometheus metrics if available"""
        if ENHANCED_MONITORING and self.prometheus_exporter:
            return self.prometheus_exporter.get_metrics_output()
        return ""

    def record_business_event(self, event_type: str, data: Dict[str, Any]):
        """Record business event for monitoring"""
        if ENHANCED_MONITORING and self.prometheus_exporter:
            if event_type == "audit_completed":
                self.prometheus_exporter.update_business_metrics(
                    {"auditorias_processadas": [data]}
                )
            elif event_type == "report_generated":
                self.prometheus_exporter.update_business_metrics(
                    {"relatorios_gerados": [data]}
                )

    def record_http_request(
        self, method: str, endpoint: str, status_code: int, duration: float
    ):
        """Record HTTP request metrics"""
        if ENHANCED_MONITORING and self.prometheus_exporter:
            self.prometheus_exporter.record_http_request(
                method, endpoint, status_code, duration
            )

    def _get_system_status(self) -> str:
        """Get overall system status"""
        # Check if there are any critical alerts
        active_alerts = self.alert_manager.get_active_alerts()
        critical_alerts = [
            a for a in active_alerts if a.severity == AlertSeverity.CRITICAL
        ]

        if critical_alerts:
            return "critical"

        # Check health status
        health_status = self.health_checker.get_overall_health()
        if health_status == "unhealthy":
            return "unhealthy"
        elif health_status == "degraded" or any(
            a.severity == AlertSeverity.HIGH for a in active_alerts
        ):
            return "degraded"
        else:
            return "healthy"


# Global monitoring system instance
_monitoring_system = None


def get_monitoring_system() -> MonitoringSystem:
    """Get the global monitoring system instance"""
    global _monitoring_system
    if _monitoring_system is None:
        _monitoring_system = MonitoringSystem()
    return _monitoring_system
