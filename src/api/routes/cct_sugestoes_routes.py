"""
Rotas para revisão, aprovação e rejeição de sugestões de impacto de CCTs.
"""
from fastapi import APIRouter, HTTPException
from src.controllers import cct_sugestoes_controller
from src.schemas_cct import ProcessarSugestaoCCTRequest

router = APIRouter(prefix="/api/v1/ccts/sugestoes-impacto", tags=["Sugestões de Impacto CCT"])

@router.post("/{id_sugestao_impacto}/processar", status_code=200)
async def processar_sugestao_impacto_cct(id_sugestao_impacto: str, payload: ProcessarSugestaoCCTRequest):
    resultado = await cct_sugestoes_controller.processar_sugestao_usuario(id_sugestao_impacto, payload)
    if "erro" in resultado:
        raise HTTPException(status_code=400, detail=resultado["erro"])
    return resultado
