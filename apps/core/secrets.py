# AUDITORIA360 - Core Secrets (Legacy Reference)
# Actual implementation is in src/core/secrets.py

# Import from actual implementation
from src.core.secrets import *

# Legacy alias for compatibility
__all__ = [
    "get_secret",
    "SECRET_KEY",
    "DATABASE_URL",
    "OPENAI_API_KEY"
]