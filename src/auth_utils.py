import json
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.config_manager import ConfigManager

# Carregar configurações
config_manager_instance = ConfigManager()
base_app_config = config_manager_instance.base_config # Acessar a configuração base carregada no __init__

SECRET_KEY = base_app_config.get("SECRET_KEY", "super-secret-key-please-change-in-production")
ALGORITHM = base_app_config.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = base_app_config.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
GESTORES_PATH = "c:/Users/55479/Documents/AUDITORIA360/auth/gestor_contas.json" # Usar caminho absoluto

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class User(BaseModel):
    username: str
    client_id: str
    disabled: Optional[bool] = False
    is_admin: Optional[bool] = False

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str) -> Optional[User]:
    try:
        with open(GESTORES_PATH, 'r') as f:
            users_db: Dict[str, Any] = json.load(f)
        user_data = users_db.get(username)
        if user_data:
            return User(
                username=user_data.get("username"),
                client_id=user_data.get("client_id"),
                disabled=user_data.get("disabled", False),
                is_admin=user_data.get("is_admin", False) # Adicionar is_admin
            )
    except FileNotFoundError:
        # Logar ou tratar o erro de arquivo não encontrado
        print(f"Erro: Arquivo de usuários não encontrado em {GESTORES_PATH}")
        return None
    except json.JSONDecodeError:
        # Logar ou tratar o erro de JSON inválido
        print(f"Erro: Formato JSON inválido em {GESTORES_PATH}")
        return None
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Adicionar is_admin ao payload do token se necessário, ou buscar sempre em get_user
    # Por simplicidade, vamos buscar em get_user. Se is_admin for usado com muita frequência,
    # pode ser útil incluí-lo no token.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username_from_payload: Optional[str] = payload.get("sub") # Alterado para Optional[str]
        if username_from_payload is None:
            raise credentials_exception
        username: str = username_from_payload # Atribuição segura agora
    except JWTError:
        raise credentials_exception
    
    user = get_user(username)
    if user is None:
        raise credentials_exception
    # O user já contém is_admin de get_user
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Exemplo de como gerar um hash de senha (para adicionar novos usuários manualmente)
# if __name__ == "__main__":
#     test_password = "testpassword"
#     hashed = get_password_hash(test_password)
#     print(f"'{test_password}': '{hashed}'")
#     # testuser: $2b$12$EixZAxK5Kqyt2m2vP4zSg.RA0jWc1vU2zX7g8xJz0lJz0lJz0lJz0
