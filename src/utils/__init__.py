"""
AUDITORIA360 Utils Package
Utility functions and helpers for the AUDITORIA360 application
"""

# Import utils modules with graceful error handling
try:
    from .monitoring import get_monitoring_system
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False
    def get_monitoring_system():
        return None

try:
    from .performance import profile, cached
    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False
    def profile(func):
        return func
    def cached(func):
        return func

try:
    from .api_integration import setup_monitoring_integration
    API_INTEGRATION_AVAILABLE = True
except ImportError:
    API_INTEGRATION_AVAILABLE = False
    def setup_monitoring_integration():
        pass

__all__ = [
    'get_monitoring_system',
    'profile', 
    'cached',
    'setup_monitoring_integration'
]

__version__ = "1.0.0"