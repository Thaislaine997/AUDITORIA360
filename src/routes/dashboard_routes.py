from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from ..bq_loader import ControleFolhaLoader
from ..config_manager import get_current_config
import os
import logging
import pandas as pd

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)

# MOCK_DASHBOARD_DB para simular dados de dashboard por cliente
MOCK_DASHBOARD_DB = {
    "cliente_a": [
        {"id_dashboard": "dash1_a", "client_id": "cliente_a", "data": "dados A1"},
        {"id_dashboard": "dash2_a", "client_id": "cliente_a", "data": "dados A2"}
    ],
    "cliente_b": [
        {"id_dashboard": "dash1_b", "client_id": "cliente_b", "data": "dados B1"}
    ]
}

def get_loader(config: dict = Depends(get_current_config)) -> ControleFolhaLoader:
    # get_current_config já trata a ausência/invalidade do client_id levantando HTTPException
    # Portanto, config e config["client_id"] devem existir aqui.
    
    gcp_project_id = config.get('gcp_project_id')
    control_bq_dataset_id = config.get('control_bq_dataset_id')
    client_id = config["client_id"] # Usar o client_id do config

    if not gcp_project_id or not control_bq_dataset_id:
        logger.error(f"GCP_PROJECT_ID ou CONTROL_BQ_DATASET_ID não definidos na configuração para dashboard do cliente {client_id}.")
        raise HTTPException(status_code=500, detail="Configuração do loader do dashboard ausente.")
    
    try:
        loader_config = {
            "gcp_project_id": gcp_project_id,
            "control_bq_dataset_id": control_bq_dataset_id,
            "client_id": client_id 
        }
        # TODO: Considerar se ControleFolhaLoader precisa ser instanciado para todas as rotas de dashboard
        # ou apenas para aquelas que efetivamente o utilizam (ex: /pendencias).
        # Por enquanto, mantemos a instanciação para consistência com o código anterior.
        loader = ControleFolhaLoader(config=loader_config)
        logger.info(f"ControleFolhaLoader inicializado para dashboard com config: {loader_config}.")
        return loader
    except ValueError as e:
        logger.error(f"Erro de valor ao inicializar ControleFolhaLoader para dashboard (cliente {client_id}): {e}")
        raise HTTPException(status_code=500, detail=f"Erro de valor ao inicializar loader: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado ao inicializar ControleFolhaLoader para dashboard (cliente {client_id}): {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao inicializar loader: {e}")

@router.get("/")
async def get_dashboard_root(config: dict = Depends(get_current_config)):
    client_id = config["client_id"]
    items = MOCK_DASHBOARD_DB.get(client_id, [])
    # Filtrar novamente para garantir, embora o get já deva retornar apenas os do cliente.
    items_filtrados = [item for item in items if item["client_id"] == client_id]
    return JSONResponse(content={"status": "success", "items": items_filtrados}, status_code=200)

@router.get("/{id_dashboard}")
async def get_dashboard_by_id(id_dashboard: str, config: dict = Depends(get_current_config)):
    client_id = config["client_id"]
    items_cliente = MOCK_DASHBOARD_DB.get(client_id, [])
    for item in items_cliente:
        if item["id_dashboard"] == id_dashboard:
            # Não é necessário verificar item["client_id"] == client_id aqui,
            # pois já estamos buscando dentro do bucket do cliente correto.
            return JSONResponse(content={"status": "success", "item": item}, status_code=200)
    raise HTTPException(status_code=404, detail=f"Dashboard com ID {id_dashboard} não encontrado para o cliente.")

@router.get('/pendencias')
async def get_pendencias_dashboard_route(loader: ControleFolhaLoader = Depends(get_loader)):
    # A dependência get_loader já garante que o config e client_id são válidos.
    try:
        df_pendencias = loader.buscar_pendencias_dashboard()
        if df_pendencias.empty:
            return JSONResponse(content={"status": "success", "message": "Nenhuma pendência encontrada.", "data": []}, status_code=200)
        
        pendencias_list = df_pendencias.to_dict(orient='records')
        return JSONResponse(content={"status": "success", "data": pendencias_list}, status_code=200)
        
    except HTTPException: # Se get_loader levantar HTTPException, ela será propagada
        raise
    except Exception as e:
        # client_id pode ser obtido do loader.client_id se necessário para logging
        logger.exception(f"Erro inesperado ao buscar pendências do dashboard para o cliente {loader.client_id if hasattr(loader, 'client_id') else 'desconhecido'}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao buscar pendências: {str(e)}")