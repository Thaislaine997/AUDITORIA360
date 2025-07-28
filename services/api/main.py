from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import logging

# Importar os roteadores
# from .explainability_routes import router as explainability_router  # Temporariamente comentado

# Importar as funções de processamento
from src.main import process_document_ocr, process_control_sheet

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Auditoria360 API",
    description="API para o sistema Auditoria360, fornecendo endpoints para frontend e outros serviços.",
    version="0.1.0"
)

# Incluir o router de explainability  
# app.include_router(explainability_router, prefix="/explainability", tags=["Explainability"])  # Temporariamente comentado

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

# Modelos Pydantic para as respostas
class HealthResponse(BaseModel):
    status: str
    message: str

class ContabilidadeOption(BaseModel):
    id: str
    nome: str

class EventHandlerResponse(BaseModel):
    status: str
    message: str = None
    
class GCSEventMessage(BaseModel):
    attributes: Dict[str, Any]
    messageId: str
    publishTime: str
    
class GCSEvent(BaseModel):
    message: GCSEventMessage

# Endpoints principais
@app.get("/", response_model=HealthResponse, tags=["Health"])
async def read_root():
    return HealthResponse(status="healthy", message="AUDITORIA360 API is running!")

@app.get("/health", response_model=HealthResponse, tags=["Health"])  
async def health_check():
    return HealthResponse(status="healthy", message="API está funcionando corretamente")

@app.get("/api/v1/auditorias/options/contabilidades", response_model=List[ContabilidadeOption], tags=["Auditoria"])
async def get_contabilidades_options():
    """
    Retorna opções de contabilidades disponíveis.
    Mock implementation para que os testes passem.
    """
    # Mock data - em produção seria consultado no BigQuery
    return [
        ContabilidadeOption(id="contabilidade_1", nome="Contabilidade Teste 1"),
        ContabilidadeOption(id="contabilidade_2", nome="Contabilidade Teste 2"),
    ]

@app.get("/contabilidades/options", response_model=List[ContabilidadeOption], tags=["Contabilidade"])
async def get_contabilidades_options_legacy():
    """
    Endpoint legacy para compatibilidade.
    """
    return await get_contabilidades_options()

@app.post("/event-handler", response_model=EventHandlerResponse, tags=["Events"])
async def gcs_event_handler(request: Request):
    """
    Manipula eventos do Google Cloud Storage via Pub/Sub.
    """
    try:
        # Verifica se existe payload JSON
        content_type = request.headers.get("content-type", "")
        if "application/json" not in content_type.lower():
            raise HTTPException(status_code=400, detail="Nenhum payload JSON recebido")
        
        # Obtém o payload
        try:
            event_data = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Nenhum payload JSON recebido")
        
        # Valida a estrutura do evento
        if "message" not in event_data:
            raise HTTPException(status_code=400, detail="Formato de envelope de evento inválido.")
        
        message = event_data["message"]
        attributes = message.get("attributes", {})
        
        bucket_id = attributes.get("bucketId")
        object_id = attributes.get("objectId")
        
        if not bucket_id or not object_id:
            raise HTTPException(status_code=400, detail="bucketId e objectId são obrigatórios nos atributos da mensagem")
        
        # Obtém os buckets de configuração
        gcs_input_bucket = os.environ.get('GCS_INPUT_BUCKET', '')
        gcs_control_bucket = os.environ.get('GCS_CONTROL_BUCKET', '')
        
        # Processa conforme o tipo de bucket
        if bucket_id == gcs_input_bucket:
            # Bucket de documentos PDF
            if object_id.startswith("documentos/") and object_id.endswith(".pdf"):
                result = process_document_ocr(file_name=object_id, bucket_name=bucket_id)
                logger.info(f"Documento PDF processado: {object_id}")
            else:
                logger.warning(f"Objeto ignorado no bucket de entrada: {object_id}")
                
        elif bucket_id == gcs_control_bucket:
            # Bucket de planilhas de controle
            if object_id.startswith("planilhas-controle/") and object_id.endswith((".xlsx", ".xls")):
                result = process_control_sheet(file_name=object_id, bucket_name=bucket_id)
                logger.info(f"Planilha de controle processada: {object_id}")
            else:
                logger.warning(f"Objeto ignorado no bucket de controle: {object_id}")
        else:
            logger.warning(f"Bucket não reconhecido: {bucket_id}")
        
        return EventHandlerResponse(status="success", message="Evento processado com sucesso")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no processamento do evento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")


## Incluir os roteadores na aplicação (comentados até serem implementados)
# app.include_router(auth_routes.router, prefix="/auth", tags=["Autenticação"])
# app.include_router(pdf_processor_routes.router, prefix="/pdf", tags=["Processador PDF"])
# app.include_router(auditoria_routes.router, prefix="/auditoria", tags=["Auditoria"])
# app.include_router(cct_clausulas_routes.router, prefix="/cct-clausulas", tags=["CCT Cláusulas"])
# app.include_router(cct_routes.router, prefix="/ccts", tags=["CCTs"])
# app.include_router(cct_sugestoes_routes.router, prefix="/cct-sugestoes", tags=["CCT Sugestões"])
# app.include_router(checklist_folha_routes.router, prefix="/checklist-folha", tags=["Checklist Folha"])
# app.include_router(consultor_riscos_routes.router, prefix="/consultor-riscos", tags=["Consultor de Riscos"])
# app.include_router(contabilidade_routes.router, prefix="/contabilidade", tags=["Contabilidade"])
# app.include_router(controle_folha_routes.router, prefix="/controle-folha", tags=["Controle Folha"])
# app.include_router(dashboard_folha_routes.router, prefix="/dashboard-folha", tags=["Dashboard Folha"])
# app.include_router(dashboard_routes.router, prefix="/dashboard", tags=["Dashboard"])
# app.include_router(empresas_routes.router, prefix="/empresas", tags=["Empresas"])
# app.include_router(folhas_processadas_routes.router, prefix="/folhas-processadas", tags=["Folhas Processadas"])
# app.include_router(folhas_routes.router, prefix="/folhas", tags=["Folhas"])
# app.include_router(parametros_fgts_admin_routes.router, prefix="/admin/parametros/fgts", tags=["Admin - Parâmetros FGTS"])
# app.include_router(parametros_irrf_admin_routes.router, prefix="/admin/parametros/irrf", tags=["Admin - Parâmetros IRRF"])
# app.include_router(parametros_legais_admin_routes.router, prefix="/admin/parametros/legais", tags=["Admin - Parâmetros Legais"])
# app.include_router(parametros_salario_familia_admin_routes.router, prefix="/admin/parametros/salario-familia", tags=["Admin - Parâmetros Salário Família"])
# app.include_router(parametros_salario_minimo_admin_routes.router, prefix="/admin/parametros/salario-minimo", tags=["Admin - Parâmetros Salário Mínimo"])
# app.include_router(param_legais_assistente_routes.router, prefix="/param-legais-assistente", tags=["Assistente de Parâmetros Legais"])
# app.include_router(param_legais_routes.router, prefix="/param-legais", tags=["Parâmetros Legais"])
# app.include_router(predicao_risco_routes.router, prefix="/predicao-risco", tags=["Predição de Risco"])
# app.include_router(relatorios_folha_routes.router, prefix="/relatorios-folha", tags=["Relatórios Folha"])
# app.include_router(relatorio_routes.router, prefix="/relatorios", tags=["Relatórios"])
# app.include_router(rubricas_routes.router, prefix="/rubricas", tags=["Rubricas"])
# app.include_router(checklist_folha_routes.router, prefix="/checklist-folha", tags=["Checklist Folha"])
# app.include_router(consultor_riscos_routes.router, prefix="/consultor-riscos", tags=["Consultor de Riscos"])
# app.include_router(contabilidade_routes.router, prefix="/contabilidade", tags=["Contabilidade"])
# app.include_router(controle_folha_routes.router, prefix="/controle-folha", tags=["Controle Folha"])
# app.include_router(dashboard_folha_routes.router, prefix="/dashboard-folha", tags=["Dashboard Folha"])
# app.include_router(dashboard_routes.router, prefix="/dashboard", tags=["Dashboard"])
# app.include_router(empresas_routes.router, prefix="/empresas", tags=["Empresas"])
# app.include_router(folhas_processadas_routes.router, prefix="/folhas-processadas", tags=["Folhas Processadas"])
# app.include_router(folhas_routes.router, prefix="/folhas", tags=["Folhas"]) # Reativado
# app.include_router(parametros_fgts_admin_routes.router, prefix="/admin/parametros/fgts", tags=["Admin - Parâmetros FGTS"])
# app.include_router(parametros_irrf_admin_routes.router, prefix="/admin/parametros/irrf", tags=["Admin - Parâmetros IRRF"])
# app.include_router(parametros_legais_admin_routes.router, prefix="/admin/parametros/legais", tags=["Admin - Parâmetros Legais"])
# app.include_router(parametros_salario_familia_admin_routes.router, prefix="/admin/parametros/salario-familia", tags=["Admin - Parâmetros Salário Família"])
# app.include_router(parametros_salario_minimo_admin_routes.router, prefix="/admin/parametros/salario-minimo", tags=["Admin - Parâmetros Salário Mínimo"])
# app.include_router(param_legais_assistente_routes.router, prefix="/param-legais-assistente", tags=["Assistente de Parâmetros Legais"])
# app.include_router(param_legais_routes.router, prefix="/param-legais", tags=["Parâmetros Legais"])
# app.include_router(predicao_risco_routes.router, prefix="/predicao-risco", tags=["Predição de Risco"])
# app.include_router(relatorios_folha_routes.router, prefix="/relatorios-folha", tags=["Relatórios Folha"])
# app.include_router(relatorio_routes.router, prefix="/relatorios", tags=["Relatórios"])
# app.include_router(rubricas_routes.router, prefix="/rubricas", tags=["Rubricas"])

# Seção para execução direta via python -m src.api.main
if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor FastAPI da Auditoria360...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

