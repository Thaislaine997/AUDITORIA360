"""
Unified Authentication System for AUDITORIA360
Consolidates JWT and SSO authentication flows
"""

import os
import yaml
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Union
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
import streamlit as st
from pathlib import Path

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "auditoria360-secret-key-change-in-production")
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
                with open(yaml_path, 'r', encoding='utf-8') as file:
                    self.yaml_config = yaml.safe_load(file)
            else:
                # Default configuration
                self.yaml_config = {
                    'credentials': {
                        'usernames': {
                            'admin': {
                                'email': 'admin@auditoria360.com',
                                'name': 'Administrator',
                                'password': self.hash_password('admin123'),
                                'client_id': 'ADMIN001',
                                'roles': ['admin', 'user']
                            },
                            'user': {
                                'email': 'user@auditoria360.com',
                                'name': 'Regular User',
                                'password': self.hash_password('user123'),
                                'client_id': 'USER001',
                                'roles': ['user']
                            }
                        }
                    },
                    'cookie': {
                        'expiry_days': 30,
                        'key': SECRET_KEY,
                        'name': 'auditoria360_auth'
                    }
                }
        except Exception as e:
            print(f"Warning: Could not load YAML config: {e}")
            self.yaml_config = {'credentials': {'usernames': {}}}
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
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
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username/password (supports both DB and YAML)"""
        # First try YAML authentication (for development/fallback)
        if self._authenticate_yaml_user(username, password):
            user_data = self.yaml_config['credentials']['usernames'].get(username, {})
            return {
                'username': username,
                'email': user_data.get('email', f'{username}@auditoria360.com'),
                'name': user_data.get('name', username.title()),
                'roles': user_data.get('roles', ['user']),
                'client_id': user_data.get('client_id', 'DEFAULT'),
                'auth_method': 'yaml'
            }
        
        # TODO: Add database authentication here
        # if self._authenticate_db_user(username, password):
        #     return db_user_data
        
        return None
    
    def _authenticate_yaml_user(self, username: str, password: str) -> bool:
        """Authenticate against YAML configuration"""
        try:
            users = self.yaml_config.get('credentials', {}).get('usernames', {})
            if username in users:
                stored_password = users[username].get('password', '')
                return self.verify_password(password, stored_password)
            return False
        except Exception:
            return False
    
    def get_current_user_from_token(self, token: Optional[str]) -> Optional[Dict[str, Any]]:
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
                'username': username,
                'email': payload.get('email', f'{username}@auditoria360.com'),
                'name': payload.get('name', username.title()),
                'roles': payload.get('roles', ['user']),
                'exp': payload.get('exp'),
                'iat': payload.get('iat')
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
            "sub": user['username'],
            "email": user['email'],
            "name": user['name'],
            "roles": user['roles']
        }
        access_token = self.create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": self.token_expire_minutes * 60,
            "user": user
        }
    
    def logout(self, token: Optional[str] = None) -> Dict[str, str]:
        """Logout user (mainly for audit purposes in stateless JWT)"""
        # In JWT, logout is mainly client-side token removal
        # This is for server-side audit logging
        return {"message": "Successfully logged out", "status": "success"}
    
    def get_streamlit_auth_status(self) -> Dict[str, Any]:
        """Get authentication status for Streamlit integration"""
        if 'authentication_status' not in st.session_state:
            return {'authenticated': False, 'user': None}
        
        if st.session_state.get('authentication_status') and st.session_state.get('api_token'):
            user = self.get_current_user_from_token(st.session_state.get('api_token'))
            return {'authenticated': True, 'user': user}
        
        return {'authenticated': False, 'user': None}
    
    def streamlit_login(self, username: str, password: str) -> bool:
        """Streamlit-specific login method"""
        try:
            login_result = self.login(username, password)
            
            # Store in Streamlit session
            st.session_state['authentication_status'] = True
            st.session_state['api_token'] = login_result['access_token']
            st.session_state['username'] = username
            st.session_state['name'] = login_result['user']['name']
            st.session_state['email'] = login_result['user']['email']
            st.session_state['roles'] = login_result['user']['roles']
            
            return True
        except HTTPException:
            return False
    
    def streamlit_logout(self):
        """Streamlit-specific logout method"""
        keys_to_clear = [
            'authentication_status', 'api_token', 'username', 
            'name', 'email', 'roles', 'password'
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]

# Global instance
auth_manager = UnifiedAuthManager()

# FastAPI dependencies
def get_current_user_dependency(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
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
    
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user_dependency)):
        user_roles = current_user.get('roles', [])
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    
    return role_checker

# Convenience functions
def hash_password(password: str) -> str:
    return auth_manager.hash_password(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return auth_manager.verify_password(plain_password, hashed_password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    return auth_manager.create_access_token(data, expires_delta)

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    return auth_manager.authenticate_user(username, password)