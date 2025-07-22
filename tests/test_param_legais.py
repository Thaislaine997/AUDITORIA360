import pytest
from fastapi.testclient import TestClient
from services.api.main import app
from datetime import date

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Parametrização dos endpoints e helpers para cada parâmetro legal
test_matrix = [
    {
        "nome": "salario_minimo",
        "endpoint": "/param-legais/salario-minimo/",
        "payload": lambda: {
            "data_inicio_vigencia": date(2025, 1, 1).isoformat(),
            "valor_nacional": 1500.00,
            "observacao": "Teste Salário Mínimo"
        },
        "campo_valor": "valor_nacional"
    },
    {
        "nome": "salario_familia",
        "endpoint": "/param-legais/salario-familia/",
        "payload": lambda: {
            "data_inicio_vigencia": date(2025, 1, 1).isoformat(),
            "faixas": [{"valor_renda_maxima": 1819.26, "valor_quota": 62.04}],
            "observacao": "Teste Salário Família"
        },
        "campo_valor": "faixas"
    },
    {
        "nome": "irrf",
        "endpoint": "/param-legais/irrf/",
        "payload": lambda: {
            "data_inicio_vigencia": date(2025, 1, 1).isoformat(),
            "faixas": [
                {"base_calculo_de": 0, "base_calculo_ate": 2259.20, "aliquota": 0, "parcela_a_deduzir": 0},
                {"base_calculo_de": 2259.21, "base_calculo_ate": 2826.65, "aliquota": 7.5, "parcela_a_deduzir": 169.44},
            ],
            "deducao_por_dependente": 189.59,
            "observacao": "Teste Tabela IRRF"
        },
        "campo_valor": "faixas"
    },
    {
        "nome": "inss",
        "endpoint": "/param-legais/inss/",
        "payload": lambda: {
            "data_inicio_vigencia": date(2025, 1, 1).isoformat(),
            "faixas": [
                {"valor_inicial": 0, "valor_final": 1412.00, "aliquota": 7.5},
                {"valor_inicial": 1412.01, "valor_final": 2666.68, "aliquota": 9.0},
            ],
            "valor_teto_contribuicao": 7786.02,
            "observacao": "Teste Tabela INSS"
        },
        "campo_valor": "faixas"
    },
    {
        "nome": "fgts",
        "endpoint": "/param-legais/fgts/",
        "payload": lambda: {
            "data_inicio_vigencia": date(2025, 1, 1).isoformat(),
            "aliquota_deposito_mensal": 8.0,
            "aliquota_multa_rescisoria_saldo": 40.0,
            "aliquota_contribuicao_social": 10.0,
            "observacao": "Teste Parâmetros FGTS"
        },
        "campo_valor": "aliquota_deposito_mensal"
    },
]

@pytest.mark.parametrize("param", test_matrix, ids=[p["nome"] for p in test_matrix])
def test_criar_parametro_legal(client, param):
    payload = param["payload"]()
    response = client.post(param["endpoint"], json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data_inicio_vigencia"] == payload["data_inicio_vigencia"]
    assert param["campo_valor"] in data
    assert data["ativo"] is True
    assert "id_versao" in data or "id" in data
