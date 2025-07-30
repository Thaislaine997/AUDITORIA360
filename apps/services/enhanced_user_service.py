"""
Enhanced user management service with multi-tenant isolation.
Demonstrates the use of BaseService for business logic encapsulation.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from apps.services.base_service import BaseService
from apps.models.auth_models import User
from apps.auth.unified_auth import UnifiedAuthManager


class EnhancedUserService(BaseService[User]):
    """
    Enhanced business logic service for user management.
    Provides secure, multi-tenant user operations with advanced features.
    """
    
    def __init__(self, db: Session, current_user: User):
        super().__init__(db, current_user)
        self.auth_manager = UnifiedAuthManager()
    
    def get_model_class(self) -> type:
        return User
    
    def create_user_with_validation(self, user_data: Dict[str, Any]) -> User:
        """
        Create a new user with comprehensive validation and password hashing.
        Automatically assigns tenant_id based on current user context.
        """
        # Validate email uniqueness within tenant
        existing_user = self._get_user_by_email(user_data.get('email', ''))
        if existing_user:
            raise ValueError(f"User with email {user_data['email']} already exists in this organization")
        
        # Hash password before storage
        if 'password' in user_data:
            user_data['hashed_password'] = self.auth_manager.hash_password(user_data.pop('password'))
        
        # Ensure proper role assignment based on current user permissions
        user_data['role'] = self._validate_role_assignment(user_data.get('role', 'user'))
        
        return self.create(user_data)
    
    def update_user_with_validation(self, user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
        """
        Update user with validation and security checks.
        """
        # Handle password updates
        if 'password' in update_data:
            update_data['hashed_password'] = self.auth_manager.hash_password(update_data.pop('password'))
        
        # Validate role changes
        if 'role' in update_data:
            update_data['role'] = self._validate_role_assignment(update_data['role'])
        
        return self.update(user_id, update_data)
    
    def get_users_by_role(self, role: str) -> List[User]:
        """Get all users with a specific role in the current tenant"""
        query = self.db.query(User).filter(User.role == role)
        query = self._apply_tenant_filter(query, User)
        return query.all()
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """Get comprehensive user statistics for the current tenant"""
        total_users = self.count()
        active_users = len(self.get_active_users())
        
        # Count by role
        role_counts = {}
        for role in ['admin', 'manager', 'user', 'auditor']:
            role_counts[role] = len(self.get_users_by_role(role))
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': total_users - active_users,
            'role_distribution': role_counts,
            'tenant_id': self.tenant_id
        }
    
    def get_active_users(self) -> List[User]:
        """Get all active users in the current tenant"""
        query = self.db.query(User).filter(User.is_active == True)
        query = self._apply_tenant_filter(query, User)
        return query.all()
    
    def _get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email within current tenant"""
        query = self.db.query(User).filter(User.email == email)
        query = self._apply_tenant_filter(query, User)
        return query.first()
    
    def _validate_role_assignment(self, role: str) -> str:
        """
        Validate that the current user can assign the requested role.
        Implements role hierarchy validation.
        """
        allowed_roles = ['user', 'auditor', 'manager', 'admin']
        
        if role not in allowed_roles:
            raise ValueError(f"Invalid role: {role}. Must be one of {allowed_roles}")
        
        # Role hierarchy validation
        user_role = self.current_user.role
        role_hierarchy = {
            'user': 0,
            'auditor': 1, 
            'manager': 2,
            'admin': 3
        }
        
        if role_hierarchy.get(role, 0) > role_hierarchy.get(user_role, 0):
            raise PermissionError(f"Cannot assign role '{role}' - insufficient permissions")
        
        return role