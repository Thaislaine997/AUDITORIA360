from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from src.auth_utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    User,
    create_access_token,
    get_current_active_user,
    get_user,
    verify_password,
)

router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, get_user(form_data.username).hashed_password): # type: ignore
        # Acessar o hashed_password diretamente do gestor_contas.json ou adaptar get_user para retornar o hash
        # Esta é uma simplificação. Em um cenário real, get_user retornaria o objeto User completo ou None.
        # Para este exemplo, vamos assumir que precisamos recarregar os dados do usuário para obter o hash.
        # Idealmente, o `get_user` já traria o hash ou teríamos uma função `authenticate_user`.
        
        # Recarregando dados do usuário para obter o hash (solução temporária para o exemplo)
        import json
        GESTORES_PATH = "c:/Users/55479/Documents/AUDITORIA360/auth/gestor_contas.json"
        try:
            with open(GESTORES_PATH, 'r') as f:
                users_db = json.load(f)
            user_data_from_db = users_db.get(form_data.username)
            if not user_data_from_db or not verify_password(form_data.password, user_data_from_db.get("hashed_password")):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except (FileNotFoundError, json.JSONDecodeError):
             raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User database not found or corrupted",
            )
        # Se chegou aqui, significa que a senha verificou contra o user_data_from_db
        # mas o `user` original (da primeira chamada a `get_user`) pode não ter o hash.
        # Atualizamos `user` para garantir que temos o objeto correto.
        user = User(username=user_data_from_db["username"], client_id=user_data_from_db["client_id"], disabled=user_data_from_db.get("disabled"))

    if not user: # Checagem adicional caso a lógica acima não resulte em um usuário válido
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "client_id": user.client_id}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> Any:
    return current_user
