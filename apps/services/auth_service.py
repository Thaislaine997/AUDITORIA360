# AUDITORIA360 - Auth Service (Legacy Reference)
# Actual implementation is in src/services/auth_service.py

# Import from actual implementation
from src.services.auth_service import *

# Legacy alias for compatibility
__all__ = [
    "AuthService",
    "authenticate",
    "authorize"
]