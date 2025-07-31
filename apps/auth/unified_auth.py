# AUDITORIA360 - Unified Auth (Legacy Reference)  
# This file provides backward compatibility for the checklist validation
# The actual implementation is in src/auth/unified_auth.py

# Import from the actual implementation
from src.auth.unified_auth import *

# Legacy alias for compatibility
__all__ = [
    "UnifiedAuthService",
    "authenticate_user",
    "authorize_user", 
    "validate_token"
]