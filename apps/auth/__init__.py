# Unified Authentication Module
from .unified_auth import (
    UnifiedAuthManager,
    auth_manager,
    authenticate_user,
    create_access_token,
    get_current_user_dependency,
    hash_password,
    require_role,
    verify_password,
)

__all__ = [
    "auth_manager",
    "UnifiedAuthManager",
    "get_current_user_dependency",
    "require_role",
    "hash_password",
    "verify_password",
    "create_access_token",
    "authenticate_user",
]
