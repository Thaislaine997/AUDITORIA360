# --- Auditorias e Relatórios (mock banco em memória) ---
auditorias_db = []
relatorios_db = []

class CriarAuditoriaRequest(BaseModel):
    descricao: str

class CriarRelatorioRequest(BaseModel):
    descricao: str

@app.post("/api/auditorias")
async def criar_auditoria(req: CriarAuditoriaRequest):
    auditoria = {
        "id": len(auditorias_db) + 1,
        "descricao": req.descricao,
    }
    auditorias_db.append(auditoria)
    return JSONResponse(content={"ok": True, "auditoria": auditoria})

@app.post("/api/relatorios")
async def criar_relatorio(req: CriarRelatorioRequest):
    relatorio = {
        "id": len(relatorios_db) + 1,
        "descricao": req.descricao,
    }
    relatorios_db.append(relatorio)
    return JSONResponse(content={"ok": True, "relatorio": relatorio})
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=GITHUB_TOKEN,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IARequest(BaseModel):
    context: str
    prompt: str = None

class CriarTarefaRequest(BaseModel):
    descricao: str

class CriarNotificacaoRequest(BaseModel):
    descricao: str

# Mock banco de dados em memória
tarefas_db = []
notificacoes_db = []
@app.post("/api/tarefas")
async def criar_tarefa(req: CriarTarefaRequest):
    tarefa = {
        "id": len(tarefas_db) + 1,
        "descricao": req.descricao,
        "concluido": False,
    }
    tarefas_db.append(tarefa)
    return JSONResponse(content={"ok": True, "tarefa": tarefa})

@app.post("/api/notificacoes")
async def criar_notificacao(req: CriarNotificacaoRequest):
    notificacao = {
        "id": len(notificacoes_db) + 1,
        "descricao": req.descricao,
        "lida": False,
    }
    notificacoes_db.append(notificacao)
    return JSONResponse(content={"ok": True, "notificacao": notificacao})

@app.post("/api/ia/analyze")
async def analyze_ia(req: IARequest):
    messages = [
        {"role": "system", "content": "Você é um assistente de IA para análise de contexto de auditoria, tickets, tarefas, relatórios e uploads."},
        {"role": "user", "content": req.context},
    ]
    if req.prompt:
        messages.append({"role": "user", "content": req.prompt})
    response = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-4o-mini",
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0
    )
    return {"result": response.choices[0].message.content}

@app.post("/api/ia/chat")
async def chat_ia(req: IARequest):
    messages = [
        {"role": "system", "content": "Você é um assistente de IA para dúvidas sobre o sistema, explicação de campos, sugestões e análise de contexto."},
        {"role": "user", "content": req.context},
    ]
    if req.prompt:
        messages.append({"role": "user", "content": req.prompt})
    response = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-4o-mini",
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0
    )
    return {"result": response.choices[0].message.content}
