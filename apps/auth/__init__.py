"""
Redirect module to consolidate auth in src.auth
This module redirects all imports to the centralized auth in src.auth
to avoid duplication while maintaining backward compatibility.
"""

# Import everything from the centralized auth
from src.auth.middleware import *
from src.auth.unified_auth import *