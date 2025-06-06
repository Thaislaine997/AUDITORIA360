# src/main.py

from fastapi import FastAPI, HTTPException, Depends, Body, APIRouter, Request, BackgroundTasks
from pydantic import BaseModel
import requests
from fastapi.responses import JSONResponse
from src.routes import auditoria_routes
from src.routes import relatorio_routes
from src.routes import controle_folha_routes
from src.routes import dashboard_routes
from src.routes import empresas_routes
from src.routes import param_legais_routes
from src.routes import contabilidade_routes
from src.routes import param_legais_assistente_routes
from src.routes import rubricas_routes
from src.routes import auth_routes
from src.routes import checklist_folha_routes # Nova importação para checklist
from src.routes import folhas_processadas_routes # Nova importação para folhas processadas
from src.routes import cct_clausulas_routes # Nova importação para cláusulas extraídas
from src.routes import cct_sugestoes_routes # Nova importação para sugestões de impacto de CCTs
from src.config_manager import get_current_config, get_background_task_config
from src.bq_loader import get_bigquery_client
from src.docai_utils import process_gcs_pdf
from src.sheet_loader import process_control_sheet
import logging
import json

# --- Inicialização do App FastAPI ---
app = FastAPI()

# --- Rota de Health Check ---
@app.get("/", tags=["healthcheck"])
async def read_root():
    return {"status": "healthy"}

# --- Modelos Pydantic ---
class RecaptchaVerificationRequest(BaseModel):
    username: str
    recaptcha_token: str

class RecaptchaVerificationResponse(BaseModel):
    recaptcha_valid: bool
    message: str | None = None

# --- Função de Verificação reCAPTCHA ---
async def verify_recaptcha_token(token: str, recaptcha_secret_key: str) -> bool:
    try:
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": recaptcha_secret_key, "response": token},
            timeout=5
        )
        response.raise_for_status() # Garante que erros HTTP sejam levantados
        result = response.json()
        return bool(result.get("success", False))
    except requests.exceptions.RequestException as e_req: # Mais específico para erros de request
        logging.error(f"Request error verifying reCAPTCHA token: {e_req}")
        return False
    except Exception as e: # Captura genérica para outros erros (ex: JSONDecodeError)
        logging.error(f"General error verifying reCAPTCHA token: {e}")
        return False

# --- Nova Rota para Verificar reCAPTCHA Após Autenticação Inicial ---
@app.post("/verify-recaptcha-session", response_model=RecaptchaVerificationResponse)
async def verify_session_with_recaptcha(payload: RecaptchaVerificationRequest, config: dict = Depends(get_current_config)):
    recaptcha_secret_key = config.get("RECAPTCHA_SECRET_KEY")
    if not recaptcha_secret_key:
        logging.error("RECAPTCHA_SECRET_KEY não configurado.")
        # Não exponha o erro de configuração diretamente ao cliente por segurança
        raise HTTPException(status_code=500, detail="Erro de configuração interna do servidor.")

    is_valid = await verify_recaptcha_token(payload.recaptcha_token, recaptcha_secret_key)
    if not is_valid:
        return RecaptchaVerificationResponse(recaptcha_valid=False, message="reCAPTCHA inválido.")
    
    logging.info(f"reCAPTCHA verificado com sucesso para o usuário: {payload.username}") # Alterado de print para logging.info
    return RecaptchaVerificationResponse(recaptcha_valid=True, message="reCAPTCHA verificado com sucesso.")

@app.get("/public-config")
def public_config(request: Request, config: dict = Depends(get_current_config)):
    public_keys = [
        "RECAPTCHA_SITE_KEY",
        "gcp_project_id",
        "gcp_location",
        "docai_processor_id",
        "branding_name",
        "branding_logo_url",
        "client_display_name"
    ]
    public_config_data = {k: v for k, v in config.items() if k in public_keys and v is not None}
    return JSONResponse(content=public_config_data)

@app.post("/event-handler")
async def gcs_event_handler(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="Nenhum payload JSON recebido.")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Payload não é um JSON válido.")

    if not payload:
        raise HTTPException(status_code=400, detail="Payload JSON vazio ou inválido.")

    logging.info("Received GCS event: %s", payload)

    if "message" not in payload or "attributes" not in payload["message"]:
        logging.error(f"Formato de envelope de evento inválido. Payload: {payload}")
        raise HTTPException(status_code=400, detail="Formato de envelope de evento inválido.")

    message = payload["message"]
    attributes = message.get("attributes", {})
    
    event_type = attributes.get("eventType")
    object_id = attributes.get("objectId")
    bucket_id = attributes.get("bucketId")

    if not object_id or not bucket_id:
        logging.error(f"ID do objeto ou ID do bucket ausente no payload. Attributes: {attributes}")
        raise HTTPException(status_code=400, detail="ID do objeto ou ID do bucket ausente no payload.")

    logging.info(f"Evento GCS recebido: tipo='{event_type}', bucket='{bucket_id}', arquivo='{object_id}'")

    client_id_from_event = attributes.get("X-Client-ID")
    DEFAULT_GCS_CLIENT_ID = "gcs_event_default_client" 

    if not client_id_from_event:
        logging.warning(f"Nenhum X-Client-ID encontrado nos atributos do evento. Usando client_id padrão para GCS: {DEFAULT_GCS_CLIENT_ID}")
        client_id_for_task = DEFAULT_GCS_CLIENT_ID
    else:
        client_id_for_task = client_id_from_event
        logging.info(f"Usando client_id '{client_id_for_task}' extraído dos atributos do evento GCS.")

    try:
        task_config = get_background_task_config(client_id_for_task)
        logging.info(f"Configuração carregada para client_id '{client_id_for_task}' para tarefa de background.")
    except (ValueError, FileNotFoundError) as e_conf:
        logging.error(f"Falha ao obter configuração para client_id '{client_id_for_task}': {e_conf}", exc_info=True)
        return JSONResponse(
            status_code=200, 
            content={"status": "error", "message": f"Erro de configuração para o cliente '{client_id_for_task}'. Impossível processar o evento."}
        )
    except Exception as e_conf_unexpected:
        logging.error(f"Erro inesperado ao obter configuração para client_id '{client_id_for_task}': {e_conf_unexpected}", exc_info=True)
        return JSONResponse(
            status_code=200,
            content={"status": "error", "message": "Erro interno inesperado ao carregar configuração para processamento do evento."}
        )

    bq_client = None
    try:
        bq_client = get_bigquery_client(config_dict=task_config)
        logging.info(f"Cliente BigQuery instanciado com sucesso para o projeto: {task_config.get('gcp_project_id')} (cliente: {client_id_for_task})")
    except Exception as e_bq:
        logging.error(f"Falha ao criar cliente BigQuery com config para '{client_id_for_task}': {e_bq}", exc_info=True)
        return JSONResponse(
            status_code=200,
            content={"status": "error", "message": f"Erro ao inicializar cliente de banco de dados para cliente '{client_id_for_task}'."}
        )

    if object_id.startswith("documentos/"):
        logging.info(f"Adicionando process_gcs_pdf para {object_id} (cliente: {client_id_for_task}) às tarefas em background.")
        try:
            background_tasks.add_task(process_gcs_pdf,
                                      bucket_name=bucket_id,
                                      file_name=object_id,
                                      config_override=task_config,
                                      bq_client=bq_client)
            return {"status": "accepted", "message": f"Processamento do documento {object_id} (cliente: {client_id_for_task}) iniciado."}
        except Exception as e_task_doc:
            logging.error(f"Erro ao agendar process_gcs_pdf para {object_id} (cliente: {client_id_for_task}): {e_task_doc}", exc_info=True)
            return JSONResponse(
                status_code=200,
                content={"status": "error", "message": f"Erro ao iniciar o processamento do documento {object_id} (cliente: {client_id_for_task})."}
            )

    elif object_id.startswith("planilhas-controle/"):
        logging.info(f"Adicionando process_control_sheet para {object_id} (cliente: {client_id_for_task}) às tarefas em background.")
        try:
            background_tasks.add_task(process_control_sheet,
                                      file_name=object_id,
                                      bucket_name=bucket_id,
                                      config_override=task_config,
                                      bq_client_injected=bq_client)
            return {"status": "accepted", "message": f"Processamento da planilha {object_id} (cliente: {client_id_for_task}) iniciado."}
        except Exception as e_task_sheet:
            logging.error(f"Erro ao agendar process_control_sheet para {object_id} (cliente: {client_id_for_task}): {e_task_sheet}", exc_info=True)
            return JSONResponse(
                status_code=200,
                content={"status": "error", "message": f"Erro ao iniciar o processamento da planilha {object_id} (cliente: {client_id_for_task})."}
            )
    else:
        logging.warning(f"Tipo de arquivo não suportado ou caminho desconhecido: {object_id} (cliente: {client_id_for_task})")
        return JSONResponse(
            status_code=200,
            content={"status": "warning", "message": f"Tipo de arquivo não suportado para {object_id} (cliente: {client_id_for_task})."}
        )

app.include_router(auditoria_routes.router)
app.include_router(relatorio_routes.router)
app.include_router(controle_folha_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(empresas_routes.router)
app.include_router(param_legais_routes.router, prefix="/api/v1/parametros-legais", tags=["Parâmetros Legais - Tabelas"])
app.include_router(contabilidade_routes.router)
app.include_router(param_legais_assistente_routes.router)
app.include_router(rubricas_routes.router)
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])

# Incluir os novos routers para checklist e ações da folha
app.include_router(checklist_folha_routes.router) 
app.include_router(checklist_folha_routes.router_folha_actions)
app.include_router(folhas_processadas_routes.router)
app.include_router(cct_clausulas_routes.router)
app.include_router(cct_sugestoes_routes.router)
