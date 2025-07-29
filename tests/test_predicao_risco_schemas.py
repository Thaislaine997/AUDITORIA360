import pytest

from src.schemas.predicao_risco_schemas import (
    DadosSuporteVisualizacaoSchema,
    FatorContribuinteTecnicoSchema,
    PredicaoRiscoDashboardResponse,
    RiscoPrevistoDetalheSchema,
)


def test_risco_previsto_detalhe_schema():
    obj = RiscoPrevistoDetalheSchema(
        tipo_risco="Financeiro",
        descricao_risco="Teste",
        probabilidade=0.8,
        impacto="Alto",
    )
    assert obj.impacto == "Alto"


def test_fator_contribuinte_tecnico_schema():
    obj = FatorContribuinteTecnicoSchema(
        fator="INSS", descricao="Teste", origem_dado="Folha"
    )
    assert obj.origem_dado == "Folha"


def test_dados_suporte_visualizacao_schema():
    obj = DadosSuporteVisualizacaoSchema(
        tipo_grafico="Bar", titulo="Riscos", dados={"A": 1}
    )
    assert obj.tipo_grafico == "Bar"


def test_predicao_risco_dashboard_response():
    obj = PredicaoRiscoDashboardResponse(
        total_colaboradores=10,
        media_risco_contratual=0.5,
        media_risco_conformidade=0.6,
        media_risco_operacional=0.7,
        media_risco_financeiro=0.8,
        distribuicao_risco_departamento={"RH": 0.5},
        distribuicao_risco_cargo={"Analista": 0.6},
        tendencia_risco_mensal={"Jan": 0.7},
    )
    assert obj.total_colaboradores == 10
