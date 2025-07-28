"""
User and Authentication Models for AUDITORIA360
Implements granular permissions system with roles:
- Administrador, RH, Contador, Colaborador, Sindicato
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class UserRole(enum.Enum):
    ADMINISTRADOR = "administrador"
    RH = "rh"
    CONTADOR = "contador"
    COLABORADOR = "colaborador"
    SINDICATO = "sindicato"

class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

# Association table for many-to-many relationship between users and permissions
user_permissions = Table(
    'user_permissions',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.COLABORADOR)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    
    # Profile information
    phone = Column(String(20))
    department = Column(String(100))
    position = Column(String(100))
    employee_id = Column(String(50))
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    is_email_verified = Column(Boolean, default=False)
    
    # LGPD Compliance
    consent_given = Column(Boolean, default=False)
    consent_date = Column(DateTime(timezone=True))
    data_retention_date = Column(DateTime(timezone=True))
    
    # Relationships
    permissions = relationship("Permission", secondary=user_permissions, back_populates="users")
    access_logs = relationship("AccessLog", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username} ({self.role.value})>"

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    resource = Column(String(100), nullable=False)  # folha, cct, documentos, etc.
    action = Column(String(50), nullable=False)     # create, read, update, delete, admin
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    users = relationship("User", secondary=user_permissions, back_populates="permissions")
    
    def __repr__(self):
        return f"<Permission {self.name}: {self.action} on {self.resource}>"

class AccessLog(Base):
    __tablename__ = "access_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    resource_id = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="access_logs")
    
    def __repr__(self):
        return f"<AccessLog {self.user.username}: {self.action} on {self.resource}>"