from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar os roteadores
from .routes import (
    auth_routes, 
    pdf_processor_routes,
    auditoria_routes,
    cct_clausulas_routes,
    cct_routes,
    cct_sugestoes_routes,
    checklist_folha_routes,
    consultor_riscos_routes,
    contabilidade_routes,
    controle_folha_routes,
    dashboard_folha_routes,
    dashboard_routes,
    empresas_routes,
    folhas_processadas_routes,
    folhas_routes, # Reativado - assumindo que bq_loader.py está correto
    parametros_fgts_admin_routes,
    parametros_irrf_admin_routes,
    parametros_legais_admin_routes,
    parametros_salario_familia_admin_routes,
    parametros_salario_minimo_admin_routes,
    param_legais_assistente_routes,
    param_legais_routes,
    predicao_risco_routes,
    relatorios_folha_routes,
    relatorio_routes,
    rubricas_routes
)

app = FastAPI(
    title="Auditoria360 API",
    description="API para o sistema Auditoria360, fornecendo endpoints para frontend e outros serviços.",
    version="0.1.0"
)

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

# Incluir os roteadores na aplicação
app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticação"])
app.include_router(pdf_processor_routes.router, prefix="/pdf", tags=["Processador PDF"])
app.include_router(auditoria_routes.router, prefix="/auditoria", tags=["Auditoria"])
app.include_router(cct_clausulas_routes.router, prefix="/cct-clausulas", tags=["CCT Cláusulas"])
app.include_router(cct_routes.router, prefix="/ccts", tags=["CCTs"])
app.include_router(cct_sugestoes_routes.router, prefix="/cct-sugestoes", tags=["CCT Sugestões"])
app.include_router(checklist_folha_routes.router, prefix="/checklist-folha", tags=["Checklist Folha"])
app.include_router(consultor_riscos_routes.router, prefix="/consultor-riscos", tags=["Consultor de Riscos"])
app.include_router(contabilidade_routes.router, prefix="/contabilidade", tags=["Contabilidade"])
app.include_router(controle_folha_routes.router, prefix="/controle-folha", tags=["Controle Folha"])
app.include_router(dashboard_folha_routes.router, prefix="/dashboard-folha", tags=["Dashboard Folha"])
app.include_router(dashboard_routes.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(empresas_routes.router, prefix="/empresas", tags=["Empresas"])
app.include_router(folhas_processadas_routes.router, prefix="/folhas-processadas", tags=["Folhas Processadas"])
app.include_router(folhas_routes.router, prefix="/folhas", tags=["Folhas"]) # Reativado
app.include_router(parametros_fgts_admin_routes.router, prefix="/admin/parametros/fgts", tags=["Admin - Parâmetros FGTS"])
app.include_router(parametros_irrf_admin_routes.router, prefix="/admin/parametros/irrf", tags=["Admin - Parâmetros IRRF"])
app.include_router(parametros_legais_admin_routes.router, prefix="/admin/parametros/legais", tags=["Admin - Parâmetros Legais"])
app.include_router(parametros_salario_familia_admin_routes.router, prefix="/admin/parametros/salario-familia", tags=["Admin - Parâmetros Salário Família"])
app.include_router(parametros_salario_minimo_admin_routes.router, prefix="/admin/parametros/salario-minimo", tags=["Admin - Parâmetros Salário Mínimo"])
app.include_router(param_legais_assistente_routes.router, prefix="/param-legais-assistente", tags=["Assistente de Parâmetros Legais"])
app.include_router(param_legais_routes.router, prefix="/param-legais", tags=["Parâmetros Legais"])
app.include_router(predicao_risco_routes.router, prefix="/predicao-risco", tags=["Predição de Risco"])
app.include_router(relatorios_folha_routes.router, prefix="/relatorios-folha", tags=["Relatórios Folha"])
app.include_router(relatorio_routes.router, prefix="/relatorios", tags=["Relatórios"])
app.include_router(rubricas_routes.router, prefix="/rubricas", tags=["Rubricas"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API Auditoria360"}

# Seção para execução direta via python -m src.api.main
if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor FastAPI da Auditoria360...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

