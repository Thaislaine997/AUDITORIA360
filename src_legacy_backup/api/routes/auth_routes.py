from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from src.api import auth
from src.api.auth import get_current_user
from src.services import user_service
from src.schemas import rbac_schemas
from src.schemas.rbac_schemas import TokenData

router = APIRouter()

@router.post("/token", response_model=rbac_schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_service.get_user_by_email(email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    token_data = {
        "sub": user.id_usuario,
        "id_cliente": user.id_cliente,
        "roles": user.papeis
    }
    access_token = auth.create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=TokenData)
async def read_users_me(current_user: TokenData = Depends(get_current_user)):
    return current_user
