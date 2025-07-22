from fastapi import APIRouter, HTTPException, Body, Path, status, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
import logging
from datetime import date # Mantido caso mes_ano ou outras datas precisem ser validadas como date

from src.utils.bq_loader import ControleFolhaLoader # Caminho de importação corrigido
from src.api.auth import get_current_user
from src.schemas.rbac_schemas import TokenData

logger = logging.getLogger(__name__)
router = APIRouter()

# Carrega apenas de variáveis de ambiente
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
CONTROL_BQ_DATASET_ID = os.getenv('CONTROL_BQ_DATASET_ID')

loader: Optional[ControleFolhaLoader] = None
if not GCP_PROJECT_ID or not CONTROL_BQ_DATASET_ID:
    logger.error("GCP_PROJECT_ID ou CONTROL_BQ_DATASET_ID não definidos (via Env Var) para rotas de folhas.")
else:
    try:
        loader = ControleFolhaLoader(config={
            "GCP_PROJECT_ID": GCP_PROJECT_ID,
            "CONTROL_BQ_DATASET_ID": CONTROL_BQ_DATASET_ID
        })
        logger.info(f"ControleFolhaLoader inicializado para folhas com projeto '{GCP_PROJECT_ID}' e dataset '{CONTROL_BQ_DATASET_ID}'.")
    except ValueError as e:
        logger.error(f"Erro ao inicializar ControleFolhaLoader para folhas: {e}")
        loader = None # Garante que o loader não seja usado se a inicialização falhar
    except Exception as e:
        logger.error(f"Erro inesperado ao inicializar ControleFolhaLoader para folhas: {e}", exc_info=True)
        loader = None # Garante que o loader não seja usado se a inicialização falhar

# --- Pydantic Models ---
class FolhaBaseSchema(BaseModel):
    id_folha: str = Field(..., description="Identificador único da folha.")
    codigo_empresa: str = Field(..., description="Código da empresa associada à folha.")
    cnpj_empresa: str = Field(..., description="CNPJ da empresa associada.")
    mes_ano: str = Field(..., description="Mês e ano de referência da folha (ex: 'YYYY-MM-DD' ou 'YYYY-MM').")
    status: str = Field(..., description="Status atual da folha.")
    data_envio_cliente: Optional[str] = Field(None, description="Data de envio pelo cliente (formato ISO string).")
    data_guia_fgts: Optional[str] = Field(None, description="Data da guia FGTS (formato ISO string).")
    data_darf_inss: Optional[str] = Field(None, description="Data do DARF INSS (formato ISO string).")
    observacoes: Optional[str] = Field(None, description="Observações adicionais.")

class FolhaCreateSchema(FolhaBaseSchema):
    pass

class FolhaStatusUpdateSchema(BaseModel):
    status: str = Field(..., description="Novo status para a folha.")

class SuccessResponse(BaseModel):
    status: str = "success"
    message: str

class ErrorDetailItem(BaseModel):
    message: str

class ErrorResponsePayload(BaseModel):
    status: str = "error"
    message: str
    details: Optional[List[ErrorDetailItem]] = None

# --- Endpoints FastAPI ---
@router.post(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar uma nova folha",
    description="Cria um novo registro de folha de pagamento no sistema.",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponsePayload, "description": "Erro nos dados fornecidos ou falha na inserção."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponsePayload, "description": "Erro interno do servidor ou configuração do loader ausente."}
    }
)
async def add_folha_route(folha_data: FolhaCreateSchema = Body(...)):
    if loader is None:
        logger.error("Tentativa de adicionar folha com loader não inicializado.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": "Configuração do loader de folhas ausente ou falhou ao inicializar."}
        )

    try:
        # A validação dos campos obrigatórios e tipos básicos é feita pelo Pydantic
        # Conversões de data específicas ou validações mais complexas podem ser adicionadas aqui ou nos modelos Pydantic
        
        dict_folha_data = folha_data.model_dump()
        errors = loader.inserir_folha(**dict_folha_data)
        
        if not errors:
            return SuccessResponse(message="Folha adicionada com sucesso.")
        else:
            error_messages = [
                ErrorDetailItem(message=err.get('message', 'Erro desconhecido do BigQuery.'))
                for err_group in errors if isinstance(err_group, dict) and 'errors' in err_group and isinstance(err_group['errors'], list)
                for err in err_group['errors'] if isinstance(err, dict)
            ]
            logger.warning(f"Falha ao inserir folha: {folha_data.id_folha}. Detalhes: {error_messages}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponsePayload(message="Falha ao inserir folha.", details=error_messages).model_dump()
            )
            
    except ValueError as ve: # Pode ser levantado por alguma conversão de dados que não está no Pydantic
        logger.error(f"Erro de valor ao processar dados da folha {folha_data.id_folha}: {ve}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponsePayload(message=f"Erro nos dados fornecidos: {ve}").model_dump()
        )
    except Exception as e:
        logger.exception(f"Erro inesperado ao adicionar folha {folha_data.id_folha}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponsePayload(message=f"Erro inesperado: {str(e)}").model_dump()
        )

@router.put(
    "/{id_folha}/status",
    response_model=SuccessResponse,
    summary="Atualizar o status de uma folha",
    description="Modifica o status de uma folha de pagamento existente.",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponsePayload, "description": "Erro nos dados fornecidos ou falha na atualização."},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponsePayload, "description": "Erro interno do servidor ou configuração do loader ausente."}
    }
)
async def update_folha_status_route(
    id_folha: str = Path(..., title="ID da Folha", description="Identificador único da folha a ser atualizada."),
    status_update: FolhaStatusUpdateSchema = Body(...)
):
    if loader is None:
        logger.error(f"Tentativa de atualizar status da folha {id_folha} com loader não inicializado.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": "Configuração do loader de folhas ausente ou falhou ao inicializar."}
        )

    novo_status = status_update.status
    
    try:
        # Correção do parâmetro para atualizar_status_folha
        errors = loader.atualizar_status_folha(id_folha=id_folha, novo_status=novo_status)
        if not errors:
            return SuccessResponse(message=f"Status da folha '{id_folha}' atualizado para '{novo_status}'.")
        else:
            error_messages = [
                ErrorDetailItem(message=err.get('message', 'Erro desconhecido do BigQuery.'))
                for err_group in errors if isinstance(err_group, dict) and 'errors' in err_group and isinstance(err_group['errors'], list)
                for err in err_group['errors'] if isinstance(err, dict)
            ]
            logger.warning(f"Falha ao atualizar status da folha {id_folha}. Detalhes: {error_messages}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponsePayload(message="Falha ao atualizar status da folha.", details=error_messages).model_dump()
            )
    except Exception as e:
        logger.exception(f"Erro inesperado ao atualizar status da folha {id_folha}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponsePayload(message=f"Erro inesperado: {str(e)}").model_dump()
        )

@router.get("/minhas-folhas")
async def listar_minhas_folhas(current_user: TokenData = Depends(get_current_user)):
    id_cliente_logado = current_user.id_cliente
    papeis = current_user.roles
    if "CLIENTE_VISUALIZADOR" not in papeis and "DPEIXER_ADMIN" not in papeis:
        raise HTTPException(status_code=403, detail="Permissão negada.")
    # Aqui você chamaria o serviço real de folhas, filtrando por id_cliente_logado
    return [{"id_folha": 1, "id_cliente": id_cliente_logado, "status": "ok"}]