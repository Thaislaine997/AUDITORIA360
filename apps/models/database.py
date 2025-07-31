# AUDITORIA360 - Database Models (Legacy Reference)
# Actual implementation is in src/models/database.py

# Import from actual implementation
from src.models.database import *

# Legacy alias for compatibility
__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db"
]