"""
Monitoring module for AUDITORIA360
Provides modular monitoring, alerting, and health checking capabilities
Enhanced with Prometheus metrics, structured logging, and distributed tracing
"""

from .metrics import MetricsCollector, Metric, MetricType
from .alerts import AlertManager, Alert, AlertSeverity  
from .health import HealthChecker, HealthCheck
from .system import SystemMonitor
from .core import MonitoringSystem, get_monitoring_system

# Enhanced monitoring components (optional imports)
try:
    from .prometheus import PrometheusExporter, get_prometheus_exporter
    from .structured_logging import (
        setup_structured_logging, 
        get_business_logger, 
        get_security_logger, 
        get_performance_logger
    )
    from .tracing import Tracer, setup_tracing, trace_function
    ENHANCED_MONITORING = True
except ImportError:
    ENHANCED_MONITORING = False

__all__ = [
    "MetricsCollector",
    "Metric", 
    "MetricType",
    "AlertManager",
    "Alert",
    "AlertSeverity",
    "HealthChecker", 
    "HealthCheck",
    "SystemMonitor",
    "MonitoringSystem",
    "get_monitoring_system"
]

# Add enhanced components to exports if available
if ENHANCED_MONITORING:
    __all__.extend([
        "PrometheusExporter",
        "get_prometheus_exporter",
        "setup_structured_logging",
        "get_business_logger",
        "get_security_logger", 
        "get_performance_logger",
        "Tracer",
        "setup_tracing",
        "trace_function"
    ])