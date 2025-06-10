"""
Rotas para revisão/admin de cláusulas extraídas de CCTs.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from src.schemas.cct_schemas import ClausulaExtraidaResponse, UpdateClausulaRevisaoRequest
from src.controllers.cct_clausulas_controller import (
    listar_clausulas_extraidas_controller,
    obter_clausula_especifica_controller,
    atualizar_revisao_clausula_controller
)
from src.utils.auth_utils import get_current_active_user
from src.schemas.rbac_schemas import UserPublic  # Para tipagem do usuário

router = APIRouter()

@router.get("/clausulas_extraidas/", response_model=List[ClausulaExtraidaResponse])
async def listar_clausulas_extraidas(
    skip: int = 0, 
    limit: int = 100, 
    id_cct: Optional[str] = Query(None),
    current_user: UserPublic = Depends(get_current_active_user) # Protegendo a rota
):
    # Adicionar lógica para verificar permissões do usuário se necessário
    clausulas = await listar_clausulas_extraidas_controller(id_cct, skip, limit)
    if not clausulas:
        raise HTTPException(status_code=404, detail="Nenhuma cláusula encontrada")
    return clausulas

@router.get("/clausulas_extraidas/{id_clausula}", response_model=ClausulaExtraidaResponse)
async def obter_clausula_especifica(
    id_clausula: str,
    current_user: UserPublic = Depends(get_current_active_user) # Protegendo a rota
):
    # Adicionar lógica para verificar permissões do usuário se necessário
    clausula = await obter_clausula_especifica_controller(id_clausula)
    if not clausula:
        raise HTTPException(status_code=404, detail="Cláusula não encontrada")
    return clausula

@router.patch("/clausulas_extraidas/{id_clausula}/revisao", response_model=ClausulaExtraidaResponse)
async def atualizar_revisao_clausula(
    id_clausula: str, 
    revisao_data: UpdateClausulaRevisaoRequest,
    current_user: UserPublic = Depends(get_current_active_user) # Protegendo a rota
):
    # Adicionar lógica para verificar permissões do usuário se necessário
    clausula_atualizada = await atualizar_revisao_clausula_controller(id_clausula, revisao_data)
    if not clausula_atualizada:
        raise HTTPException(status_code=404, detail="Cláusula não encontrada para atualização")
    return clausula_atualizada

# Adicionar mais rotas conforme necessário, por exemplo, para criar ou deletar cláusulas,
# sempre lembrando de proteger com Depends(get_current_active_user) e verificar permissões.
