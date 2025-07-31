# AUDITORIA360 - Core Config (Legacy Reference)
# This file provides backward compatibility for the checklist validation  
# The actual implementation is in src/core/config.py

# Import from the actual implementation
from src.core.config import *

# Legacy alias for compatibility
__all__ = [
    "Settings", 
    "get_settings",
    "DATABASE_URL",
    "SECRET_KEY"
]