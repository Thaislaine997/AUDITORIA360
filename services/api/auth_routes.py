from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import os
import logging

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Security configuration
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "auditoria360-dev-secret-key-please-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

# Pydantic models
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    empresa_id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    empresa_id: Optional[str] = None
    is_active: bool = True

# Mock user database (in production, this would be BigQuery/PostgreSQL)
MOCK_USERS = {
    "admin@auditoria360.com": {
        "id": "user_001",
        "email": "admin@auditoria360.com",
        "full_name": "Administrador Sistema",
        "hashed_password": pwd_context.hash("admin123"),  # In production: secure password
        "empresa_id": "empresa_001",
        "is_active": True,
        "roles": ["admin", "auditor"]
    },
    "demo@empresa.com": {
        "id": "user_002", 
        "email": "demo@empresa.com",
        "full_name": "Usuário Demonstração",
        "hashed_password": pwd_context.hash("demo123"),
        "empresa_id": "empresa_demo",
        "is_active": True,
        "roles": ["auditor"]
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token and return user data."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token_data: dict = Depends(verify_token)) -> dict:
    """Get current user from token."""
    email = token_data.get("sub")
    if email not in MOCK_USERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return MOCK_USERS[email]

# Auth endpoints
@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Authenticate user and return access token."""
    user = MOCK_USERS.get(user_data.email)
    
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["id"], "empresa_id": user["empresa_id"]},
        expires_delta=access_token_expires
    )
    
    expires_at = datetime.now(timezone.utc) + access_token_expires
    
    logger.info(f"User {user['email']} logged in successfully")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": expires_at
    }

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister):
    """Register new user (simplified version)."""
    if user_data.email in MOCK_USERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # In production, this would be saved to database
    new_user = {
        "id": f"user_{len(MOCK_USERS) + 1:03d}",
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": get_password_hash(user_data.password),
        "empresa_id": user_data.empresa_id or f"empresa_{len(MOCK_USERS) + 1:03d}",
        "is_active": True,
        "roles": ["auditor"]
    }
    
    MOCK_USERS[user_data.email] = new_user
    
    logger.info(f"New user registered: {user_data.email}")
    
    return UserResponse(
        id=new_user["id"],
        email=new_user["email"],
        full_name=new_user["full_name"],
        empresa_id=new_user["empresa_id"],
        is_active=new_user["is_active"]
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        empresa_id=current_user["empresa_id"],
        is_active=current_user["is_active"]
    )

@router.post("/logout")
async def logout():
    """Logout user (in JWT, this is mainly client-side token removal)."""
    return {"message": "Logout realizado com sucesso"}

@router.get("/health")
async def auth_health():
    """Health check for auth service."""
    return {
        "status": "healthy",
        "service": "authentication",
        "users_count": len(MOCK_USERS),
        "timestamp": datetime.now(timezone.utc)
    }