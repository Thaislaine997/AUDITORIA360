"""
Pydantic schemas for authentication and user management
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from src.models.auth_models import UserRole, UserStatus


# Base schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    username: str
    role: UserRole = UserRole.COLABORADOR
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    employee_id: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    consent_given: bool = False


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None


class UserInDB(UserBase):
    id: int
    status: UserStatus
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]
    is_email_verified: bool
    consent_given: bool
    consent_date: Optional[datetime]

    class Config:
        from_attributes = True


class User(UserInDB):
    """Public user schema (without sensitive data)"""

    pass


# Permission schemas
class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    resource: str
    action: str


class PermissionCreate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    user: User
    token: Token


# Access log schemas
class AccessLogBase(BaseModel):
    action: str
    resource: str
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None


class AccessLogCreate(AccessLogBase):
    user_id: int


class AccessLog(AccessLogBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# Password change schemas
class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


# User preferences schemas
class UserPreferences(BaseModel):
    timezone: str = "America/Sao_Paulo"
    language: str = "pt-BR"
    theme: str = "light"
    notifications_enabled: bool = True
    email_notifications: bool = True
    sms_notifications: bool = False
