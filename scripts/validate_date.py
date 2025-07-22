import re

def is_iso_date(date_str: str) -> bool:
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_str))

# Módulo migrado para services/core/validators.py
# Use from services.core.validators import is_iso_date
