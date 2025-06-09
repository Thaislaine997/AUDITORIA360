"""
Rotas para revisão/admin de cláusulas extraídas de CCTs.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from src.auth_utils import get_current_active_user, User
from src.controllers.cct_clausulas_controller import (
    listar_clausulas_para_revisao,
    atualizar_clausula_extraida
)
from src.schemas_cct import ClausulaExtraidaResponse, UpdateClausulaRevisaoRequest

router = APIRouter(prefix="/api/v1/ccts/clausulas", tags=["CCTs - Cláusulas"])

@router.get("/revisao", response_model=List[ClausulaExtraidaResponse])
async def get_clausulas_para_revisao(
    tipo_clausula: str = Query(None),
    status: str = Query(None),
    id_cct: str = Query(None),
    data_inicial: str = Query(None),
    data_final: str = Query(None),
    current_user: User = Depends(get_current_active_user)
):
    return await listar_clausulas_para_revisao(tipo_clausula, status, id_cct, data_inicial, data_final)

@router.put("/{id_clausula}", response_model=ClausulaExtraidaResponse)
async def put_revisao_clausula(id_clausula: str, payload: UpdateClausulaRevisaoRequest, current_user: User = Depends(get_current_active_user)):
    return await atualizar_clausula_extraida(id_clausula, payload)
