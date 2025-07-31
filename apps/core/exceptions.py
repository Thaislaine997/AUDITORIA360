# AUDITORIA360 - Core Exceptions (Legacy Reference)
# Actual implementation is in src/core/exceptions.py

# Import from actual implementation
from src.core.exceptions import *

# Legacy alias for compatibility
__all__ = [
    "BaseException",
    "ValidationError", 
    "AuthenticationError",
    "AuthorizationError"
]