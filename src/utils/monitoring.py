"""
Enhanced Monitoring System for AUDITORIA360
Implements comprehensive metrics collection, alerting, and real-time monitoring.

This module provides backward compatibility by importing from the new modular structure.
For new code, import from src.monitoring directly.
"""

# Import all components from the new modular structure for backward compatibility
from src.monitoring.alerts import Alert, AlertManager, AlertSeverity
from src.monitoring.core import MonitoringSystem, get_monitoring_system
from src.monitoring.health import HealthCheck, HealthChecker
from src.monitoring.metrics import Metric, MetricsCollector, MetricType
from src.monitoring.system import SystemMonitor

# Re-export all symbols for backward compatibility
__all__ = [
    # Enums
    "AlertSeverity",
    "MetricType",
    
    # Data classes
    "Metric",
    "Alert", 
    "HealthCheck",
    
    # Main classes
    "MetricsCollector",
    "SystemMonitor", 
    "AlertManager",
    "HealthChecker",
    "MonitoringSystem",
    
    # Functions
    "get_monitoring_system",
]
