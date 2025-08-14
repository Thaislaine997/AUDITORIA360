from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List
import secrets

app = FastAPI()
security = HTTPBasic()

# Usuário admin (pode ser movido para .env/config)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "SUA_SENHA_FORTE_AQUI"  # Troque por uma senha forte

class Sugestao(BaseModel):
    titulo: str
    descricao: str
    tipo: str  # "melhoria", "automacao", "bug", etc.

# Mock: sugestões geradas (pode ser persistido em banco futuramente)
sugestoes_db = [
    Sugestao(
        titulo="Automatizar conferência de folha",
        descricao="Detectamos muitos erros manuais, automatize o processo.",
        tipo="automacao"
    ),
    Sugestao(
        titulo="Adicionar validação de CNPJ",
        descricao="Erros constantes de CNPJ inválido. Sugerimos adicionar validação automática.",
        tipo="melhoria"
    )
]

def autenticar_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.post("/api/cerebro/sugestoes")
async def sugestoes(request: Request):
    dados = await request.json()
    # Aqui pode-se usar um modelo LLM ou regras simples para gerar sugestões.
    # Exemplo MVP: retorna sugestões mockadas.
    return {"sugestoes": [sugestao.dict() for sugestao in sugestoes_db]}

@app.get("/admin/cerebro/sugestoes", response_model=List[Sugestao])
def painel_sugestoes(admin: str = Depends(autenticar_admin)):
    """
    Página/endpoint restrito para administradora visualizar sugestões da IA.
    """
    return sugestoes_db

# Para rodar: uvicorn cerebro_api:app --reload
