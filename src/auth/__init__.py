# Unified Authentication Module
from .unified_auth import (
    auth_manager, UnifiedAuthManager, 
    get_current_user_dependency, require_role,
    hash_password, verify_password, create_access_token, authenticate_user
)

__all__ = [
    'auth_manager', 'UnifiedAuthManager',
    'get_current_user_dependency', 'require_role',
    'hash_password', 'verify_password', 'create_access_token', 'authenticate_user'
]