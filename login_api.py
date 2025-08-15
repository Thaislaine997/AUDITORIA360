
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import bcrypt
import os
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded



# Configuração de logging para auditoria
logging.basicConfig(
    filename="login_auditoria.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Adiciona CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://www.dpeixerassessoria.com.br"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "config", "gestor_contas.json"))

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    username: str
    is_admin: bool
    client_id: str

@app.post("/api/login", response_model=LoginResponse)
@limiter.limit("5/minute")  # Limite de 5 tentativas por minuto por IP
def login(request: LoginRequest, req: Request):
    # Carrega usuários
    if not os.path.exists(CONFIG_PATH):
        raise HTTPException(status_code=500, detail="Arquivo de usuários não encontrado.")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        users = json.load(f)
    user = users.get(request.username)
    if not user or user.get("disabled"):
        logging.warning(f"LOGIN FALHOU: username={request.username} ip={req.client.host}")
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")
    hashed = user["hashed_password"].encode()
    if not bcrypt.checkpw(request.password.encode(), hashed):
        logging.warning(f"LOGIN FALHOU: username={request.username} ip={req.client.host}")
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")
    logging.info(f"LOGIN SUCESSO: username={request.username} ip={req.client.host}")
    return {
        "username": user["username"],
        "is_admin": user.get("is_admin", False),
        "client_id": user.get("client_id", "")
    }

# Para rodar: uvicorn login_api:app --host 0.0.0.0 --port 8001 --reload
