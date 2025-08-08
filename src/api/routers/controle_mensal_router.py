# /auditoria360/src/api/routers/controle_mensal_router.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path

from src.lib.supabase_client import get_supabase_async_client
from src.models.schemas.controle_mensal import ControleMensalDetalhado, Tarefa
from src.services.controle_mensal_service import ControleMensalService
from supabase import AsyncClient

router = APIRouter(
    prefix="/v1/controles-mensais",
    tags=["Controle Mensal"],
)


async def get_service(
    supabase: AsyncClient = Depends(get_supabase_async_client),
) -> ControleMensalService:
    return ControleMensalService(supabase)


@router.get("/{ano}/{mes}", response_model=List[ControleMensalDetalhado])
async def get_controles_do_mes(
    ano: int = Path(..., ge=2020),
    mes: int = Path(..., ge=1, le=12),
    service: ControleMensalService = Depends(get_service),
):
    """Obtém a lista detalhada de todos os controles para um dado mês e ano."""
    try:
        return await service.obter_controles_por_mes_ano(ano, mes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gerar-mes-corrente")
async def post_gerar_controles(service: ControleMensalService = Depends(get_service)):
    """Aciona a rotina para gerar os controles do mês corrente para todas as empresas ativas."""
    try:
        return await service.gerar_controles_para_mes_corrente()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/tarefas/{tarefa_id}/status", response_model=Tarefa)
async def patch_atualizar_tarefa(
    tarefa_id: int,
    concluido: bool,
    service: ControleMensalService = Depends(get_service),
):
    """Atualiza o status de conclusão de uma tarefa específica."""
    try:
        return await service.atualizar_status_tarefa(tarefa_id, concluido)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
