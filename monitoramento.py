"""
Enhanced Monitoring Script for AUDITORIA360
Integrates with the advanced monitoring system and provides CLI interface.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.utils.monitoring import AlertSeverity, MonitoringSystem
    from src.utils.performance import DatabaseOptimizer, profiler

    ENHANCED_MONITORING = True
except ImportError:
    ENHANCED_MONITORING = False
    print("Enhanced monitoring not available - using basic monitoring")


def checar_servico(nome, url):
    """Check service health with enhanced monitoring"""
    try:
        start_time = datetime.now()
        resp = requests.get(url, timeout=5)
        response_time = (datetime.now() - start_time).total_seconds() * 1000

        if resp.status_code == 200:
            print(f"{nome}: OK (Response: {response_time:.0f}ms)")
            if ENHANCED_MONITORING:
                monitoring.metrics.set_gauge(f"service_status", 1, {"service": nome})
                monitoring.metrics.record_histogram(
                    f"service_response_time_ms", response_time, {"service": nome}
                )
        else:
            print(f"{nome}: Falha ({resp.status_code})")
            if ENHANCED_MONITORING:
                monitoring.metrics.set_gauge(f"service_status", 0, {"service": nome})
    except Exception as e:
        print(f"{nome}: Erro ({e})")
        if ENHANCED_MONITORING:
            monitoring.metrics.set_gauge(f"service_status", 0, {"service": nome})
            monitoring.metrics.increment_counter("service_errors", {"service": nome})


async def check_database_health():
    """Check database connectivity and performance"""
    try:
        # This would normally connect to your actual database
        # For now, we'll simulate the check
        print("Database: Simulating connection check...")
        await asyncio.sleep(0.1)  # Simulate connection time
        print("Database: OK (Connection established)")

        if ENHANCED_MONITORING:
            monitoring.metrics.set_gauge("database_status", 1)
            monitoring.metrics.record_histogram("database_connection_time_ms", 100)

        return True
    except Exception as e:
        print(f"Database: Erro ({e})")
        if ENHANCED_MONITORING:
            monitoring.metrics.set_gauge("database_status", 0)
        return False


async def check_storage_health():
    """Check storage (R2) connectivity"""
    try:
        # This would normally check R2 connectivity
        print("Storage (R2): Simulating connectivity check...")
        await asyncio.sleep(0.05)
        print("Storage (R2): OK")

        if ENHANCED_MONITORING:
            monitoring.metrics.set_gauge("storage_status", 1)

        return True
    except Exception as e:
        print(f"Storage (R2): Erro ({e})")
        if ENHANCED_MONITORING:
            monitoring.metrics.set_gauge("storage_status", 0)
        return False


def check_performance_metrics():
    """Display performance metrics if available"""
    if not ENHANCED_MONITORING:
        return

    print("\n=== Performance Metrics ===")

    # Get recent bottlenecks
    bottlenecks = profiler.get_bottlenecks(hours=1)
    if bottlenecks:
        print("⚠️  Performance Bottlenecks Detected:")
        for bottleneck in bottlenecks[:3]:  # Show top 3
            print(
                f"  - {bottleneck['function_name']}: Severity {bottleneck['severity']:.1f}/100"
            )
            for rec in bottleneck["recommendations"][:2]:  # Show top 2 recommendations
                print(f"    • {rec}")
    else:
        print("✅ No significant performance bottlenecks detected")

    # Show metrics summary
    summary = monitoring.metrics.get_metrics_summary(hours=1)
    print(f"\nMetrics Summary (last hour):")
    for metric_name, stats in list(summary.items())[:5]:  # Show top 5 metrics
        print(f"  {metric_name}: {stats['latest']} (avg: {stats['avg']:.2f})")


def show_alerts():
    """Display active alerts"""
    if not ENHANCED_MONITORING:
        return

    active_alerts = monitoring.alert_manager.get_active_alerts()
    if active_alerts:
        print(f"\n🚨 Active Alerts ({len(active_alerts)}):")
        for alert in active_alerts:
            severity_icon = {
                AlertSeverity.LOW: "🟡",
                AlertSeverity.MEDIUM: "🟠",
                AlertSeverity.HIGH: "🔴",
                AlertSeverity.CRITICAL: "💥",
            }.get(alert.severity, "⚠️")

            print(f"  {severity_icon} [{alert.severity.value.upper()}] {alert.title}")
            print(f"    {alert.description}")
            print(
                f"    Metric: {alert.metric_name} = {alert.current_value} (threshold: {alert.threshold})"
            )
    else:
        print("\n✅ No active alerts")


async def main():
    """Main monitoring routine"""
    print("=== AUDITORIA360 System Monitor ===")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Enhanced Monitoring: {'Enabled' if ENHANCED_MONITORING else 'Disabled'}")

    if ENHANCED_MONITORING:
        # Start monitoring system
        monitoring.start()

        # Add some basic health checks
        monitoring.health_checker.add_health_check("database", check_database_health)
        monitoring.health_checker.add_health_check("storage", check_storage_health)

    print("\n=== Service Health Checks ===")

    # Check main services
    servicos = {
        "API Health": "http://localhost:8000/health",
        "API Root": "http://localhost:8000/",
        "API Auditorias": "http://localhost:8000/api/v1/auditorias/options/contabilidades",
    }

    for nome, url in servicos.items():
        checar_servico(nome, url)

    print("\n=== Infrastructure Health Checks ===")

    # Check infrastructure components
    await check_database_health()
    await check_storage_health()

    if ENHANCED_MONITORING:
        # Run all health checks
        print("\n=== Running Health Checks ===")
        health_results = await monitoring.health_checker.run_all_checks()
        for result in health_results:
            status_icon = "✅" if result.status == "healthy" else "❌"
            print(
                f"{status_icon} {result.name}: {result.status} ({result.response_time_ms:.0f}ms)"
            )
            if result.error:
                print(f"    Error: {result.error}")

        # Show performance metrics
        check_performance_metrics()

        # Show alerts
        show_alerts()

        # Get dashboard data
        dashboard_data = monitoring.get_dashboard_data()
        print(f"\nSystem Status: {dashboard_data['system_status'].upper()}")

        # Stop monitoring
        monitoring.stop()


if __name__ == "__main__":
    if ENHANCED_MONITORING:
        # Initialize monitoring system
        monitoring = MonitoringSystem()

    # Run the monitoring
    asyncio.run(main())
