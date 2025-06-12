import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.schemas.parametros_legais_schemas import TabelaIRRF, FaixaIRRF
from datetime import date, timedelta
from typing import List, Optional

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def get_irrf_payload(
    data_inicio_vigencia: date,
    faixas: Optional[List[dict]] = None,
    deducao_por_dependente: float = 189.59,
    limite_desconto_simplificado: Optional[float] = 564.80,
    data_fim_vigencia: Optional[date] = None,
    observacao: Optional[str] = "Teste Tabela IRRF"
):
    if faixas is None:
        faixas = [
            {"base_calculo_de": 0, "base_calculo_ate": 2259.20, "aliquota": 0, "parcela_a_deduzir": 0},
            {"base_calculo_de": 2259.21, "base_calculo_ate": 2826.65, "aliquota": 7.5, "parcela_a_deduzir": 169.44},
            {"base_calculo_de": 2826.66, "base_calculo_ate": 3751.05, "aliquota": 15, "parcela_a_deduzir": 381.44},
            {"base_calculo_de": 3751.06, "base_calculo_ate": 4664.68, "aliquota": 22.5, "parcela_a_deduzir": 662.77},
            {"base_calculo_de": 4664.69, "aliquota": 27.5, "parcela_a_deduzir": 896.00}, # Última faixa sem base_calculo_ate
        ]
    payload = {
        "data_inicio_vigencia": data_inicio_vigencia.isoformat(),
        "faixas": faixas,
        "deducao_por_dependente": deducao_por_dependente,
        "observacao": observacao
    }
    if limite_desconto_simplificado is not None:
        payload["limite_desconto_simplificado"] = limite_desconto_simplificado
    if data_fim_vigencia:
        payload["data_fim_vigencia"] = data_fim_vigencia.isoformat()
    return payload

# Testes de Criação
def test_criar_nova_tabela_irrf(client):
    payload = get_irrf_payload(data_inicio_vigencia=date(2025, 1, 1))
    response = client.post("/param-legais/irrf/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data_inicio_vigencia"] == "2025-01-01"
    assert len(data["faixas"]) == 5
    assert data["faixas"][1]["aliquota"] == 7.5
    assert data["deducao_por_dependente"] == 189.59
    assert data["limite_desconto_simplificado"] == 564.80
    assert data["ativo"] is True

# Testes de Validação
@pytest.mark.parametrize(
    "field_to_remove, expected_detail_part",
    [
        ("data_inicio_vigencia", "Field required"),
        ("faixas", "Field required"),
        ("deducao_por_dependente", "Field required"),
    ]
)
def test_criar_irrf_campos_obrigatorios_ausentes(client, field_to_remove, expected_detail_part):
    payload = get_irrf_payload(data_inicio_vigencia=date(2025, 3, 1))
    del payload[field_to_remove]
    response = client.post("/param-legais/irrf/", json=payload)
    assert response.status_code == 422
    assert expected_detail_part in response.text

def test_criar_irrf_faixa_sem_parcela_deduzir(client):
    payload = get_irrf_payload(data_inicio_vigencia=date(2025, 4, 1))
    payload["faixas"] = [{"base_calculo_de": 0, "aliquota": 0}] # parcela_a_deduzir faltando
    response = client.post("/param-legais/irrf/", json=payload)
    assert response.status_code == 422
    assert "faixas" in response.text.lower()
    assert "parcela_a_deduzir" in response.text.lower() # Ajustar
    assert "Field required" in response.text

def test_criar_irrf_deducao_dependente_negativa(client):
    payload = get_irrf_payload(data_inicio_vigencia=date(2025, 4, 1), deducao_por_dependente=-10.0)
    response = client.post("/param-legais/irrf/", json=payload)
    assert response.status_code == 422
    assert "deducao_por_dependente" in response.text.lower()
    assert "must be greater than or equal to 0" in response.text.lower() # Ajustar

# Testes de Leitura
def test_listar_tabelas_irrf(client):
    client.post("/param-legais/irrf/", json=get_irrf_payload(date(2024,1,1)))
    response = client.get("/param-legais/irrf/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obter_tabela_irrf_por_id(client):
    created_id = client.post("/param-legais/irrf/", json=get_irrf_payload(date(2026,1,1))).json()["id_versao"]
    response_get = client.get(f"/param-legais/irrf/{created_id}")
    assert response_get.status_code == 200
    assert response_get.json()["id_versao"] == created_id

def test_obter_tabela_irrf_id_nao_encontrado(client):
    assert client.get(f"/param-legais/irrf/id_irrf_inexistente").status_code == 404

# Testes de Atualização
def test_atualizar_tabela_irrf(client):
    id_v1 = client.post("/param-legais/irrf/", json=get_irrf_payload(date(2027,1,1), deducao_por_dependente=180.0)).json()["id_versao"]
    payload_update = {
        "data_inicio_vigencia": date(2027,6,1).isoformat(),
        "deducao_por_dependente": 190.0,
        "faixas": [{"base_calculo_de": 0, "aliquota": 0, "parcela_a_deduzir": 0}], # Simplificado
        "observacao": "IRRF V2"
    }
    response_update = client.put(f"/param-legais/irrf/{id_v1}", json=payload_update)
    assert response_update.status_code == 200
    data_updated = response_update.json()
    assert data_updated["deducao_por_dependente"] == 190.0
    assert data_updated["id_versao"] != id_v1

    v1_after_update = client.get(f"/param-legais/irrf/{id_v1}").json()
    assert v1_after_update["ativo"] is False
    assert v1_after_update["data_fim_vigencia"] == (date(2027,6,1) - timedelta(days=1)).isoformat()

# Testes de Inativação
def test_inativar_tabela_irrf(client):
    created_id = client.post("/param-legais/irrf/", json=get_irrf_payload(date(2028,1,1))).json()["id_versao"]
    assert client.delete(f"/param-legais/irrf/{created_id}").status_code == 200
    assert client.get(f"/param-legais/irrf/{created_id}").json()["ativo"] is False

# Teste de Vigente
def test_obter_tabela_irrf_vigente(client):
    client.post("/param-legais/irrf/", json=get_irrf_payload(date(2023,1,1), deducao_por_dependente=170, data_fim_vigencia=date(2023,12,31)))
    client.post("/param-legais/irrf/", json=get_irrf_payload(date(2024,1,1), deducao_por_dependente=180, data_fim_vigencia=date(2024,12,31)))
    client.post("/param-legais/irrf/", json=get_irrf_payload(date(2025,1,1), deducao_por_dependente=190))

    response = client.get("/param-legais/irrf/vigente?data_referencia=2024-06-30")
    assert response.status_code == 200
    assert response.json()["deducao_por_dependente"] == 180

    assert client.get("/param-legais/irrf/vigente?data_referencia=2022-01-01").status_code == 404