from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from src.bq_loader import ControleFolhaLoader
from src.config_manager import get_current_config
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
        df_empresa = loader.get_empresa_by_id(id_empresa)
        
        if df_empresa is None or df_empresa.empty:
            raise HTTPException(status_code=404, detail=f"Empresa com ID {id_empresa} não encontrada.")
        
        empresa_data = df_empresa.to_dict(orient='records')[0]
        
        # Garante que o client_id do loader (solicitante) corresponde ao client_id do registro da empresa
        if hasattr(loader, 'client_id') and empresa_data.get("client_id") != loader.client_id:
            logger.warning(f"Tentativa de acesso indevido à empresa {id_empresa}. Solicitante: {loader.client_id}, Dono do registro: {empresa_data.get('client_id')}.")
            # Retorna 404 para não vazar informação se a empresa existe mas pertence a outro cliente.
            # Ou poderia ser 403 se a política for de negar explicitamente.
            raise HTTPException(status_code=404, detail=f"Empresa com ID {id_empresa} não encontrada ou acesso não permitido.")
            
        return JSONResponse(content={"status": "success", "data": empresa_data}, status_code=200)
        
    except HTTPException: # Captura HTTPExceptions levantadas por get_loader_empresas, get_empresa_by_id, ou as próprias verificações
        raise
    except Exception as e:
        client_id = loader.client_id if hasattr(loader, 'client_id') else 'desconhecido'
        logger.exception(f"Erro inesperado ao buscar empresa {id_empresa} para o cliente {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao buscar empresa: {str(e)}")