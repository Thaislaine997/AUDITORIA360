# AUDITORIA360 - Auth Models (Legacy Reference)
# This file provides backward compatibility for the checklist validation
# The actual implementation is in src/models/auth_models.py

# Import from the actual implementation  
from src.models.auth_models import *

# Legacy alias for compatibility
__all__ = [
    "User",
    "Role", 
    "Permission",
    "UserSession",
    "AuthToken"
]