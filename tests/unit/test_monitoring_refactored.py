"""
Tests for the refactored monitoring system modules
"""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from src.monitoring.alerts import AlertManager, AlertSeverity
from src.monitoring.core import MonitoringSystem
from src.monitoring.health import HealthCheck, HealthChecker
from src.monitoring.metrics import MetricsCollector, MetricType
from src.monitoring.system import SystemMonitor


class TestMetricsCollector:
    """Test the MetricsCollector class"""

    def test_record_metric(self):
        """Test recording a metric"""
        collector = MetricsCollector()

        collector.record_metric("test_metric", 42.5, MetricType.GAUGE)

        assert "test_metric" in collector.metrics
        assert len(collector.metrics["test_metric"]) == 1
        assert collector.metrics["test_metric"][0].value == 42.5
        assert collector.metrics["test_metric"][0].metric_type == MetricType.GAUGE

    def test_increment_counter(self):
        """Test incrementing a counter metric"""
        collector = MetricsCollector()

        collector.increment_counter("requests_total")
        collector.increment_counter("requests_total")

        latest_value = collector.get_latest_value("requests_total")
        assert latest_value == 2

    def test_set_gauge(self):
        """Test setting a gauge metric"""
        collector = MetricsCollector()

        collector.set_gauge("cpu_usage", 75.5)

        latest_value = collector.get_latest_value("cpu_usage")
        assert latest_value == 75.5

    def test_get_metrics_summary(self):
        """Test getting metrics summary"""
        collector = MetricsCollector()

        # Add some test metrics
        collector.set_gauge("cpu_usage", 50.0)
        collector.set_gauge("cpu_usage", 75.0)
        collector.set_gauge("cpu_usage", 60.0)

        summary = collector.get_metrics_summary(hours=1)

        assert "cpu_usage" in summary
        assert summary["cpu_usage"]["count"] == 3
        assert summary["cpu_usage"]["latest"] == 60.0
        assert summary["cpu_usage"]["min"] == 50.0
        assert summary["cpu_usage"]["max"] == 75.0
        assert summary["cpu_usage"]["avg"] == 61.666666666666664


class TestAlertManager:
    """Test the AlertManager class"""

    def test_add_alert_rule(self):
        """Test adding an alert rule"""
        manager = AlertManager()

        manager.add_alert_rule(
            "cpu_usage",
            80.0,
            "greater_than",
            AlertSeverity.HIGH,
            "High CPU",
            "CPU usage is high",
        )

        assert "cpu_usage" in manager.alert_rules
        rule = manager.alert_rules["cpu_usage"]
        assert rule["threshold"] == 80.0
        assert rule["comparison"] == "greater_than"
        assert rule["severity"] == AlertSeverity.HIGH

    def test_check_metric_alerts_triggers_alert(self):
        """Test that alert is triggered when threshold is exceeded"""
        manager = AlertManager()

        manager.add_alert_rule(
            "cpu_usage",
            80.0,
            "greater_than",
            AlertSeverity.HIGH,
            "High CPU",
            "CPU usage is high",
        )

        # This should trigger an alert
        manager.check_metric_alerts("cpu_usage", 85.0)

        active_alerts = manager.get_active_alerts()
        assert len(active_alerts) == 1
        assert active_alerts[0].metric_name == "cpu_usage"
        assert active_alerts[0].current_value == 85.0
        assert active_alerts[0].severity == AlertSeverity.HIGH

    def test_check_metric_alerts_no_trigger(self):
        """Test that alert is not triggered when threshold is not exceeded"""
        manager = AlertManager()

        manager.add_alert_rule(
            "cpu_usage",
            80.0,
            "greater_than",
            AlertSeverity.HIGH,
            "High CPU",
            "CPU usage is high",
        )

        # This should not trigger an alert
        manager.check_metric_alerts("cpu_usage", 75.0)

        active_alerts = manager.get_active_alerts()
        assert len(active_alerts) == 0

    def test_resolve_alert(self):
        """Test manually resolving an alert"""
        manager = AlertManager()

        manager.add_alert_rule(
            "cpu_usage",
            80.0,
            "greater_than",
            AlertSeverity.HIGH,
            "High CPU",
            "CPU usage is high",
        )

        # Trigger alert
        manager.check_metric_alerts("cpu_usage", 85.0)
        active_alerts = manager.get_active_alerts()
        assert len(active_alerts) == 1

        # Resolve alert
        alert_id = active_alerts[0].id
        manager.resolve_alert(alert_id)

        # Check that alert is resolved
        resolved_alert = next(a for a in manager.alerts if a.id == alert_id)
        assert resolved_alert.resolved is True
        assert resolved_alert.resolved_at is not None


class TestHealthChecker:
    """Test the HealthChecker class"""

    def test_add_health_check(self):
        """Test adding a health check"""
        collector = MetricsCollector()
        checker = HealthChecker(collector)

        def dummy_check():
            return True

        checker.add_health_check("test_check", dummy_check, interval=30)

        assert "test_check" in checker.health_checks
        assert checker.health_checks["test_check"]["interval"] == 30

    @pytest.mark.asyncio
    async def test_run_healthy_check(self):
        """Test running a healthy check"""
        collector = MetricsCollector()
        checker = HealthChecker(collector)

        def healthy_check():
            return {"status": "healthy", "details": {"response": "ok"}}

        checker.add_health_check("test_check", healthy_check)

        results = await checker.run_all_checks()

        assert len(results) == 1
        assert results[0].name == "test_check"
        assert results[0].status == "healthy"
        assert results[0].details == {"response": "ok"}

    @pytest.mark.asyncio
    async def test_run_failing_check(self):
        """Test running a failing check"""
        collector = MetricsCollector()
        checker = HealthChecker(collector)

        def failing_check():
            raise Exception("Service unavailable")

        checker.add_health_check("test_check", failing_check)

        results = await checker.run_all_checks()

        assert len(results) == 1
        assert results[0].name == "test_check"
        assert results[0].status == "unhealthy"
        assert "Service unavailable" in results[0].error

    def test_get_overall_health_all_healthy(self):
        """Test overall health when all checks are healthy"""
        collector = MetricsCollector()
        checker = HealthChecker(collector)

        # Simulate healthy results
        checker.last_results = {
            "check1": HealthCheck("check1", "healthy", datetime.now(), 10.0),
            "check2": HealthCheck("check2", "healthy", datetime.now(), 15.0),
        }

        assert checker.get_overall_health() == "healthy"

    def test_get_overall_health_one_unhealthy(self):
        """Test overall health when one check is unhealthy"""
        collector = MetricsCollector()
        checker = HealthChecker(collector)

        # Simulate mixed results
        checker.last_results = {
            "check1": HealthCheck("check1", "healthy", datetime.now(), 10.0),
            "check2": HealthCheck(
                "check2", "unhealthy", datetime.now(), 50.0, error="Failed"
            ),
        }

        assert checker.get_overall_health() == "unhealthy"


class TestSystemMonitor:
    """Test the SystemMonitor class"""

    @patch("src.monitoring.system.psutil")
    def test_collect_system_metrics(self, mock_psutil):
        """Test collecting system metrics"""
        # Mock psutil calls
        mock_psutil.cpu_percent.return_value = 45.5
        mock_psutil.virtual_memory.return_value = Mock(
            percent=60.0, used=8000000000, available=4000000000
        )
        mock_psutil.disk_usage.return_value = Mock(
            percent=70.0, used=100000000000, free=50000000000
        )

        collector = MetricsCollector()
        monitor = SystemMonitor(collector)

        monitor.collect_system_metrics()

        # Check that metrics were recorded
        assert collector.get_latest_value("system_cpu_percent") == 45.5
        assert collector.get_latest_value("system_memory_percent") == 60.0
        assert collector.get_latest_value("system_disk_percent") == 70.0

    @patch("src.monitoring.system.psutil")
    def test_get_system_info(self, mock_psutil):
        """Test getting system information"""
        # Mock psutil calls
        mock_psutil.cpu_count.return_value = 4
        mock_psutil.cpu_percent.return_value = 25.0
        mock_psutil.virtual_memory.return_value = Mock(
            total=16000000000, available=8000000000
        )
        mock_psutil.disk_usage.return_value = Mock(
            total=500000000000, free=200000000000
        )
        mock_psutil.boot_time.return_value = 1640995200
        mock_psutil.pids.return_value = [1, 2, 3, 4, 5]

        collector = MetricsCollector()
        monitor = SystemMonitor(collector)

        info = monitor.get_system_info()

        assert info["cpu_count"] == 4
        assert info["cpu_percent"] == 25.0
        assert info["memory_total"] == 16000000000
        assert info["process_count"] == 5


class TestMonitoringSystem:
    """Test the main MonitoringSystem class"""

    def test_initialization(self):
        """Test monitoring system initialization"""
        system = MonitoringSystem()

        assert system.metrics_collector is not None
        assert system.system_monitor is not None
        assert system.alert_manager is not None
        assert system.health_checker is not None

    def test_get_dashboard_data(self):
        """Test getting dashboard data"""
        system = MonitoringSystem()

        # Add some test data
        system.metrics_collector.set_gauge("test_metric", 42.0)

        dashboard_data = system.get_dashboard_data()

        assert "metrics_summary" in dashboard_data
        assert "system_info" in dashboard_data
        assert "active_alerts" in dashboard_data
        assert "health_checks" in dashboard_data
        assert "system_status" in dashboard_data

    def test_system_status_healthy(self):
        """Test system status when everything is healthy"""
        system = MonitoringSystem()

        status = system._get_system_status()
        assert status == "healthy"

    def test_system_status_with_critical_alert(self):
        """Test system status with critical alert"""
        system = MonitoringSystem()

        # Add a critical alert rule and trigger it
        system.alert_manager.add_alert_rule(
            "critical_metric",
            100.0,
            "greater_than",
            AlertSeverity.CRITICAL,
            "Critical Alert",
            "This is critical",
        )
        system.alert_manager.check_metric_alerts("critical_metric", 150.0)

        status = system._get_system_status()
        assert status == "critical"


# Integration test
def test_monitoring_system_integration():
    """Test the complete monitoring system integration"""
    system = MonitoringSystem()

    # Add some metrics
    system.metrics_collector.set_gauge("cpu_usage", 85.0)
    system.metrics_collector.increment_counter("requests_total")

    # Add a health check
    def test_health_check():
        return True

    system.health_checker.add_health_check("test_service", test_health_check)

    # Get dashboard data
    dashboard_data = system.get_dashboard_data()

    # Verify data structure
    assert "metrics_summary" in dashboard_data
    assert "system_info" in dashboard_data
    assert "active_alerts" in dashboard_data
    assert "health_checks" in dashboard_data
    assert "system_status" in dashboard_data

    # Check specific values
    metrics_summary = dashboard_data["metrics_summary"]
    assert "cpu_usage" in metrics_summary
    assert metrics_summary["cpu_usage"]["latest"] == 85.0
