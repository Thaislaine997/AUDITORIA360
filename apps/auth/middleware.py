# AUDITORIA360 - Auth Middleware (Legacy Reference)
# This file provides backward compatibility for the checklist validation
# The actual implementation is in src/auth/middleware.py

# Import from the actual implementation
from src.auth.middleware import *

# Legacy alias for compatibility
__all__ = [
    "auth_middleware",
    "tenant_middleware", 
    "security_middleware"
]