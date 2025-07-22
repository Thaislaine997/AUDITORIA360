from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar os roteadores
from .explainability_routes import router as explainability_router

app = FastAPI(
    title="Auditoria360 API",
    description="API para o sistema Auditoria360, fornecendo endpoints para frontend e outros serviços.",
    version="0.1.0"
)

# Incluir o router de explainability
app.include_router(explainability_router, prefix="/explainability", tags=["Explainability"])

# Configuração do CORS
# ATENÇÃO: Para produção, restrinja os origins permitidos.
origins = [
    "http://localhost",          # Permitir localhost para desenvolvimento Streamlit
    "http://localhost:8501",     # Porta padrão do Streamlit
    "http://127.0.0.1",
    "http://127.0.0.1:8501",
    # Adicione aqui os domínios do seu frontend em produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de origins permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os headers
)

# Incluir os roteadores disponíveis na aplicação
app.include_router(explainability_router, prefix="/explainability", tags=["Explainability"])

# TODO: Re-implementar rotas do legacy backup conforme necessário
# As seguintes rotas foram removidas porque os módulos não existem no diretório atual:
# - auth_routes, pdf_processor_routes, auditoria_routes, etc.
# Elas estão disponíveis em src_legacy_backup/ para restauração futura

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API Auditoria360 - Versão Refatorada"}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

# Seção para execução direta via python -m src.api.main
if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor FastAPI da Auditoria360...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

