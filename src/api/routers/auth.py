"""
Authentication and User Management API Router
Módulo 8: Gestão de usuários e permissões
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional

from src.models import get_db, User, Permission, AccessLog
from src.schemas.auth_schemas import (
    UserCreate, UserUpdate, User as UserSchema, 
    LoginRequest, LoginResponse, Token,
    PermissionCreate, Permission as PermissionSchema,
    PasswordChange, PasswordReset, PasswordResetConfirm
)
from src.services.auth_service import (
    authenticate_user, create_access_token, get_current_user,
    create_user, update_user, get_user_by_id, get_users,
    create_permission, get_permissions, hash_password, verify_password
)

router = APIRouter()
security = HTTPBearer()

# Authentication endpoints
@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token"""
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    
    # Update last login
    user.last_login = func.now()
    db.commit()
    
    return LoginResponse(
        user=UserSchema.from_orm(user),
        token=Token(access_token=access_token, token_type="bearer", expires_in=3600)
    )

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (mainly for logging purposes)"""
    # In a stateless JWT system, logout is handled client-side
    # This endpoint is for audit logging
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_users_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    updated_user = update_user(db, current_user.id, user_update)
    return updated_user

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    # Verify current password
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.hashed_password = hash_password(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}

# User management endpoints (admin only)
@router.post("/users", response_model=UserSchema)
async def create_new_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new user (admin only)"""
    # Check admin permissions
    if current_user.role != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = create_user(db, user_data)
    return user

@router.get("/users", response_model=List[UserSchema])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of users (admin/HR only)"""
    if current_user.role not in ["administrador", "rh"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin/HR only or own profile)"""
    if current_user.id != user_id and current_user.role not in ["administrador", "rh"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user_by_id(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user by ID (admin only)"""
    if current_user.role != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = update_user(db, user_id, user_update)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# Permission management endpoints
@router.post("/permissions", response_model=PermissionSchema)
async def create_new_permission(
    permission_data: PermissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new permission (admin only)"""
    if current_user.role != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    permission = create_permission(db, permission_data)
    return permission

@router.get("/permissions", response_model=List[PermissionSchema])
async def read_permissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of permissions"""
    permissions = get_permissions(db)
    return permissions

# Password reset endpoints
@router.post("/password-reset")
async def request_password_reset(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """Request password reset (sends email with reset token)"""
    # Implementation would send email with reset token
    # For now, just return success message
    return {"message": "Password reset email sent if user exists"}

@router.post("/password-reset/confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Confirm password reset with token"""
    # Implementation would verify token and reset password
    return {"message": "Password reset successfully"}