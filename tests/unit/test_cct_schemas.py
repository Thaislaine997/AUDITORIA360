from datetime import date

from src.schemas.cct_schemas import (
    CCTDetalheResponse,
    CCTIdentificacaoResponse,
    CCTStatusResponse,
    CCTUpdateStatusRequest,
    ClausulaExtraidaResponse,
    UpdateClausulaRevisaoRequest,
)


def test_clausula_extraida_response():
    obj = ClausulaExtraidaResponse(texto_clausula="Teste", tipo_clausula="Financeira")
    assert obj.tipo_clausula == "Financeira"


def test_update_clausula_revisao_request():
    obj = UpdateClausulaRevisaoRequest(
        revisado=True, texto_revisado="Novo texto", comentarios="OK"
    )
    assert obj.revisado is True


def test_cct_identificacao_response():
    obj = CCTIdentificacaoResponse(
        id_cct="cct1", vigencia_inicio=date(2025, 1, 1), vigencia_fim=date(2025, 12, 31)
    )
    assert obj.id_cct == "cct1"


def test_cct_detalhe_response():
    obj = CCTDetalheResponse(
        id_cct="cct1", texto_integral="Texto", status_processamento="Processado"
    )
    assert obj.status_processamento == "Processado"


def test_cct_status_response():
    obj = CCTStatusResponse(id_cct="cct1", status_atual="Ativo")
    assert obj.status_atual == "Ativo"


def test_cct_update_status_request():
    obj = CCTUpdateStatusRequest(novo_status="Ativo", detalhes="OK")
    assert obj.novo_status == "Ativo"
