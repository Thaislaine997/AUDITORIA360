"""
Utilities module for AUDITORIA360 backend.

This module contains utility functions for monitoring, performance,
API integration and other cross-cutting concerns.
"""

# Temporarily disable monitoring imports due to missing dependencies
# from .monitoring import AlertManager, HealthChecker, MonitoringSystem
# from .performance import CacheManager, DatabaseOptimizer, PerformanceProfiler

# Import structured logging for observability
from .structured_logging import setup_structured_logging, log_security_event, log_data_access

__all__ = [
    # "MonitoringSystem",
    # "AlertManager", 
    # "HealthChecker",
    # "PerformanceProfiler",
    # "DatabaseOptimizer",
    # "CacheManager",
    "setup_structured_logging",
    "log_security_event",
    "log_data_access",
]
