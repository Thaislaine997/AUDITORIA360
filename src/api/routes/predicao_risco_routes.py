from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import Optional
from datetime import date # Para o valor default de periodo_referencia no fallback

from src.controllers.predicao_risco_controller import predicao_risco_controller
from src.schemas import PredicaoRiscoDashboardResponse, DetalhePredicaoRiscoResponse
# from src.auth_utils import get_current_active_user # Para autenticação futura
# from src.models import User # Para tipagem do usuário autenticado

router = APIRouter(
    prefix="/api/v1/clientes/{id_cliente}/folhas/{id_folha_processada}/predicao-risco",
    tags=["Predição de Risco Folha"],
    # dependencies=[Depends(get_current_active_user)] # Descomentar para ativar autenticação
)

@router.get(
    "", 
    response_model=PredicaoRiscoDashboardResponse,
    summary="Obtém dados de predição de risco para o dashboard da folha.",
    description="Retorna o score de saúde da folha, classificação de risco, principais riscos previstos e uma explicação geral da IA."
)
async def get_predicao_risco_para_dashboard(
    id_cliente: str = Path(..., description="ID do cliente."),
    id_folha_processada: str = Path(..., description="ID da folha processada.")
    # current_user: User = Depends(get_current_active_user) # Para validação de acesso
):
    # Exemplo de validação de acesso (descomentar com autenticação real)
    # if not current_user or (current_user.id_cliente != id_cliente and not current_user.is_admin):
    #     raise HTTPException(status_code=403, detail="Acesso não autorizado a este cliente ou folha.")
    
    dados_predicao = await predicao_risco_controller.obter_dados_predicao_para_dashboard(
        id_folha_processada=id_folha_processada,
        id_cliente=id_cliente
    )
    if not dados_predicao:
        # Retorna uma resposta padrão indicando que a predição não está disponível
        return PredicaoRiscoDashboardResponse(
            score_saude_folha=None,
            classe_risco_geral="INDISPONIVEL",
            principais_riscos_previstos=[],
            explicacao_geral_ia="Análise preditiva ainda não disponível ou não concluída para esta folha.",
            id_folha_processada=id_folha_processada,
            periodo_referencia=date.today() # Usar uma data placeholder ou buscar da folha
        )
    return dados_predicao

@router.get(
    "/detalhes", 
    response_model=DetalhePredicaoRiscoResponse,
    summary="Obtém detalhes aprofundados de uma predição de risco específica ou do score geral.",
    description="Retorna fatores contribuintes, explicações detalhadas da IA, dados para visualização e recomendações."
)
async def get_detalhes_predicao_risco(
    id_cliente: str = Path(..., description="ID do cliente."),
    id_folha_processada: str = Path(..., description="ID da folha processada."),
    tipo_detalhe: str = Query(..., description="Tipo de detalhe solicitado: 'score_geral' ou 'risco_especifico'.", enum=["score_geral", "risco_especifico"]),
    id_risco_detalhe: Optional[str] = Query(None, description="ID do risco específico detalhado. Obrigatório se tipo_detalhe='risco_especifico'.")
    # current_user: User = Depends(get_current_active_user) # Para validação de acesso
):
    # Exemplo de validação de acesso
    # if not current_user or (current_user.id_cliente != id_cliente and not current_user.is_admin):
    #     raise HTTPException(status_code=403, detail="Acesso não autorizado.")

    if tipo_detalhe == "risco_especifico" and not id_risco_detalhe:
        raise HTTPException(
            status_code=400, 
            detail="O parâmetro 'id_risco_detalhe' é obrigatório quando 'tipo_detalhe' é 'risco_especifico'."
        )

    detalhes = await predicao_risco_controller.obter_detalhes_aprofundados_predicao(
        id_folha_processada=id_folha_processada,
        id_cliente=id_cliente,
        tipo_detalhe=tipo_detalhe,
        id_risco_detalhe=id_risco_detalhe
    )
    if not detalhes:
        raise HTTPException(status_code=404, detail="Detalhes da predição não encontrados para os parâmetros fornecidos.")
    return detalhes
