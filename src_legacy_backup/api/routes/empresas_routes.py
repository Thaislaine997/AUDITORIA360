from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from src.utils.bq_loader import ControleFolhaLoader
from src.utils.config_manager import get_current_config # Corrigido o caminho do import
from src.utils import bq_loader
import logging
import pandas as pd

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api/v1/empresas", 
    tags=["Empresas"]
)

def get_loader_empresas(config: dict = Depends(get_current_config)) -> ControleFolhaLoader:
    gcp_project_id = config.get('gcp_project_id')
    control_bq_dataset_id = config.get('control_bq_dataset_id')
    client_id = config["client_id"] 

    if not gcp_project_id or not control_bq_dataset_id:
        logger.error(f"GCP_PROJECT_ID ou CONTROL_BQ_DATASET_ID não definidos na configuração para empresas (cliente: {client_id}).")
        raise HTTPException(status_code=500, detail="Configuração do loader de empresas ausente.")

    try:
        loader_config = {
            "gcp_project_id": gcp_project_id,
            "control_bq_dataset_id": control_bq_dataset_id,
            "client_id": client_id
        }
        loader = ControleFolhaLoader(config=loader_config)
        logger.info(f"ControleFolhaLoader inicializado para empresas com config: {loader_config}.")
        return loader
    except ValueError as e:
        logger.error(f"Erro de valor ao inicializar ControleFolhaLoader para empresas (cliente: {client_id}): {e}")
        raise HTTPException(status_code=500, detail=f"Erro de valor ao inicializar loader de empresas: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado ao inicializar ControleFolhaLoader para empresas (cliente: {client_id}): {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao inicializar loader de empresas: {e}")

@router.get('/')
async def get_empresas_route(loader: ControleFolhaLoader = Depends(get_loader_empresas)):
    try:
        df_empresas = loader.listar_todas_as_empresas()
        
        if df_empresas is None or df_empresas.empty:
            return JSONResponse(content={"status": "success", "message": "Nenhuma empresa encontrada.", "data": []}, status_code=200)
        
        empresas_list = df_empresas.to_dict(orient='records')
        return JSONResponse(content={"status": "success", "data": empresas_list}, status_code=200)
        
    except HTTPException: # Captura HTTPExceptions levantadas por get_loader_empresas ou outras chamadas
        raise
    except Exception as e:
        client_id = loader.client_id if hasattr(loader, 'client_id') else 'desconhecido'
        logger.exception(f"Erro inesperado ao buscar empresas para o cliente {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao buscar empresas: {str(e)}")

@router.get("/{id_empresa}")
async def get_empresa_route(id_empresa: str, loader: ControleFolhaLoader = Depends(get_loader_empresas)):
    try:
        try:
            empresa_id_int = int(id_empresa)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"ID da empresa inválido: {id_empresa}. Deve ser um inteiro.")

        # Substituir chamada para método inexistente por busca por CNPJ ou listar empresas
        # Aqui, vamos buscar por CNPJ se o id_empresa for um CNPJ válido, senão buscar na lista de empresas
        empresa_data = None
        if len(str(empresa_id_int)) == 14:  # CNPJ
            empresa_data = loader.get_empresa_by_cnpj(str(empresa_id_int))
        else:
            # Buscar na lista de empresas
            df_empresas = loader.listar_todas_as_empresas()
            if not df_empresas.empty:
                empresa_data = next((row for row in df_empresas.to_dict(orient='records') if str(row.get('empresa_id')) == str(empresa_id_int)), None)

        if empresa_data is None:
            raise HTTPException(status_code=404, detail=f"Empresa com ID {id_empresa} não encontrada.")

        if hasattr(loader, 'client_id') and empresa_data.get("client_id") != loader.client_id:
            logger.warning(f"Tentativa de acesso indevido à empresa {id_empresa}. Solicitante: {loader.client_id}, Dono do registro: {empresa_data.get('client_id')}.")
            raise HTTPException(status_code=404, detail=f"Empresa com ID {id_empresa} não encontrada ou acesso não permitido.")

        return JSONResponse(content={"status": "success", "data": empresa_data}, status_code=200)
        
    except HTTPException: # Captura HTTPExceptions levantadas por get_loader_empresas, get_empresa_by_id, ou as próprias verificações
        raise
    except Exception as e:
        client_id = loader.client_id if hasattr(loader, 'client_id') else 'desconhecido'
        logger.exception(f"Erro inesperado ao buscar empresa {id_empresa} para o cliente {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao buscar empresa: {str(e)}")