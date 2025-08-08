"""
Unified Authentication System for AUDITORIA360
Consolidates JWT and SSO authentication flows with secure credential management
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# Import secure secrets manager
from src.core.secrets import secrets_manager

# Configuration - using secure secrets manager
SECRET_KEY = secrets_manager.get_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Security context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


class UnifiedAuthManager:
    """Unified authentication manager that handles both JWT and SSO flows"""

    def __init__(self):
        self.pwd_context = pwd_context
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self._load_yaml_credentials()

    def _load_yaml_credentials(self):
        """Load credentials from YAML file for fallback authentication"""
        try:
            yaml_path = Path("auth/login.yaml")
            if yaml_path.exists():
                with open(yaml_path, "r", encoding="utf-8") as file:
                    self.yaml_config = yaml.safe_load(file)
            else:
                # Get secure passwords from secrets manager
                secure_passwords = secrets_manager.get_default_passwords()

                # Enhanced multi-level access configuration with secure passwords
                self.yaml_config = {
                    "credentials": {
                        "usernames": {
                            # Super Administrator - Full system access
                            "admin@auditoria360-exemplo.com": {
                                "email": "admin@auditoria360-exemplo.com",
                                "name": "Super Administrator",
                                "password": self.hash_password(
                                    secure_passwords["admin"]
                                ),
                                "user_type": "super_admin",
                                "company_id": None,  # Access to all companies
                                "client_id": "SUPER_ADMIN",
                                "roles": ["super_admin", "admin", "user"],
                                "permissions": [
                                    "full_access",
                                    "manage_users",
                                    "manage_companies",
                                    "view_all_data",
                                ],
                            },
                            # Contabilidade A - Gestor
                            "gestor@contabilidade-a.com": {
                                "email": "gestor@contabilidade-a.com",
                                "name": "Gestor Contabilidade A",
                                "password": self.hash_password(
                                    secure_passwords["gestor_a"]
                                ),
                                "user_type": "contabilidade",
                                "company_id": "CONTAB_A",  # Restricted to Contabilidade A
                                "client_id": "CONTAB_A_GESTOR",
                                "roles": ["gestor", "user"],
                                "permissions": [
                                    "view_company_data",
                                    "manage_clients",
                                    "generate_reports",
                                ],
                                "data_scope": {
                                    "contabilidade": "CONTAB_A",
                                    "clients": ["EMPRESA_X", "EMPRESA_Y"],
                                },
                            },
                            # Cliente da Contabilidade A
                            "contato@empresa-teste-x.com": {
                                "email": "contato@empresa-teste-x.com",
                                "name": "Cliente Empresa X",
                                "password": self.hash_password(
                                    secure_passwords["client_x"]
                                ),
                                "user_type": "cliente_final",
                                "company_id": "EMPRESA_X",  # Restricted to specific company
                                "client_id": "EMPRESA_X_USER",
                                "roles": ["cliente", "user"],
                                "permissions": ["view_own_data", "download_documents"],
                                "data_scope": {
                                    "empresa": "EMPRESA_X",
                                    "contabilidade": "CONTAB_A",
                                },
                            },
                            # Contabilidade B - Gestor
                            "gestor@contabilidade-b.com": {
                                "email": "gestor@contabilidade-b.com",
                                "name": "Gestor Contabilidade B",
                                "password": self.hash_password(
                                    secure_passwords["gestor_b"]
                                ),
                                "user_type": "contabilidade",
                                "company_id": "CONTAB_B",  # Restricted to Contabilidade B
                                "client_id": "CONTAB_B_GESTOR",
                                "roles": ["gestor", "user"],
                                "permissions": [
                                    "view_company_data",
                                    "manage_clients",
                                    "generate_reports",
                                ],
                                "data_scope": {
                                    "contabilidade": "CONTAB_B",
                                    "clients": ["EMPRESA_Z"],
                                },
                            },
                            # Legacy users for compatibility
                            "admin": {
                                "email": "admin@auditoria360-exemplo.com",
                                "name": "Administrator",
                                "password": self.hash_password("admin123"),
                                "user_type": "super_admin",
                                "company_id": None,
                                "client_id": "ADMIN001",
                                "roles": ["admin", "user"],
                                "permissions": ["full_access"],
                            },
                            "contabilidade": {
                                "email": "contabilidade@auditoria360.com",
                                "name": "Contabilidade User",
                                "password": self.hash_password("conta123"),
                                "user_type": "contabilidade",
                                "company_id": "DEFAULT_CONTAB",
                                "client_id": "CONTAB001",
                                "roles": ["gestor", "user"],
                                "permissions": ["view_company_data"],
                            },
                        }
                    },
                    "cookie": {
                        "expiry_days": 30,
                        "key": SECRET_KEY,
                        "name": "auditoria360_auth",
                    },
                }
        except Exception as e:
            print(f"Warning: Could not load YAML config: {e}")
            self.yaml_config = {"credentials": {"usernames": {}}}

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.token_expire_minutes)

        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def authenticate_user(
        self, username: str, password: str
    ) -> Optional[Dict[str, Any]]:
        """Enhanced authentication with multi-level access support"""
        # First try YAML authentication (for development/fallback)
        if self._authenticate_yaml_user(username, password):
            user_data = self.yaml_config["credentials"]["usernames"].get(username, {})
            return {
                "username": username,
                "email": user_data.get("email", f"{username}@auditoria360.com"),
                "name": user_data.get("name", username.title()),
                "user_type": user_data.get("user_type", "user"),
                "company_id": user_data.get("company_id"),
                "roles": user_data.get("roles", ["user"]),
                "permissions": user_data.get("permissions", []),
                "data_scope": user_data.get("data_scope", {}),
                "client_id": user_data.get("client_id", "DEFAULT"),
                "auth_method": "yaml",
            }

        # TODO: Add database authentication here
        # if self._authenticate_db_user(username, password):
        #     return db_user_data

        return None

    def check_permission(self, user: Dict[str, Any], permission: str) -> bool:
        """Check if user has specific permission"""
        user_permissions = user.get("permissions", [])
        return permission in user_permissions or "full_access" in user_permissions

    def get_user_data_scope(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Get user's data access scope for query filtering"""
        user_type = user.get("user_type", "user")

        if user_type == "super_admin":
            return {"scope_type": "all", "filters": {}}
        elif user_type == "contabilidade":
            return {
                "scope_type": "company",
                "filters": {
                    "contabilidade_id": user.get("company_id"),
                    "client_ids": user.get("data_scope", {}).get("clients", []),
                },
            }
        elif user_type == "cliente_final":
            return {
                "scope_type": "enterprise",
                "filters": {
                    "empresa_id": user.get("company_id"),
                    "contabilidade_id": user.get("data_scope", {}).get("contabilidade"),
                },
            }
        else:
            return {"scope_type": "none", "filters": {}}

    def authorize_data_access(
        self, user: Dict[str, Any], resource_type: str, resource_id: str = None
    ) -> bool:
        """Authorize user access to specific data resource"""
        scope = self.get_user_data_scope(user)

        if scope["scope_type"] == "all":
            return True
        elif scope["scope_type"] == "company":
            # Contabilidade users can access their company and clients
            if resource_type == "contabilidade":
                return resource_id == scope["filters"]["contabilidade_id"]
            elif resource_type == "client":
                return resource_id in scope["filters"]["client_ids"]
        elif scope["scope_type"] == "enterprise":
            # Cliente final can only access their own enterprise data
            if resource_type == "empresa":
                return resource_id == scope["filters"]["empresa_id"]

        return False

    def _authenticate_yaml_user(self, username: str, password: str) -> bool:
        """Authenticate against YAML configuration"""
        try:
            users = self.yaml_config.get("credentials", {}).get("usernames", {})
            if username in users:
                stored_password = users[username].get("password", "")
                return self.verify_password(password, stored_password)
            return False
        except Exception:
            return False

    def get_current_user_from_token(
        self, token: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Get current user from JWT token"""
        if not token:
            return None

        try:
            payload = self.verify_token(token)
            username = payload.get("sub")
            if not username:
                return None

            # Return user data from token payload
            return {
                "username": username,
                "email": payload.get("email", f"{username}@auditoria360.com"),
                "name": payload.get("name", username.title()),
                "roles": payload.get("roles", ["user"]),
                "exp": payload.get("exp"),
                "iat": payload.get("iat"),
            }
        except HTTPException:
            return None

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Unified login method"""
        user = self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        token_data = {
            "sub": user["username"],
            "email": user["email"],
            "name": user["name"],
            "roles": user["roles"],
        }
        access_token = self.create_access_token(data=token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": self.token_expire_minutes * 60,
            "user": user,
        }

    def logout(self, token: Optional[str] = None) -> Dict[str, str]:
        """Logout user (mainly for audit purposes in stateless JWT)"""
        # In JWT, logout is mainly client-side token removal
        # This is for server-side audit logging
        return {"message": "Successfully logged out", "status": "success"}


# Global instance
auth_manager = UnifiedAuthManager()


# FastAPI dependencies
def get_current_user_dependency(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Dict[str, Any]:
    """FastAPI dependency to get current user from JWT token"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = auth_manager.get_current_user_from_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_role(required_roles: Union[str, List[str]]):
    """Decorator to require specific roles"""
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    def role_checker(
        current_user: Dict[str, Any] = Depends(get_current_user_dependency),
    ):
        user_roles = current_user.get("roles", [])
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
        return current_user

    return role_checker


# Convenience functions
def hash_password(password: str) -> str:
    return auth_manager.hash_password(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return auth_manager.verify_password(plain_password, hashed_password)


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    return auth_manager.create_access_token(data, expires_delta)


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    return auth_manager.authenticate_user(username, password)
