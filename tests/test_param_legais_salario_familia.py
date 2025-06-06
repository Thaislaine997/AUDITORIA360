import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.schemas_models import TabelaSalarioFamilia, TabelaFGTS
from datetime import date, timedelta
from typing import List, Optional

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def get_sf_payload(
    data_inicio_vigencia: date,
    faixas: Optional[List[dict]] = None,
    data_fim_vigencia: Optional[date] = None,
    observacao: Optional[str] = "Teste Salário Família"
):
    if faixas is None:
        faixas = [
            {"valor_renda_maxima": 1819.26, "valor_quota": 62.04},
            # Adicionar mais faixas se a lógica suportar múltiplas faixas de SF
            # Ex: {"valor_renda_de": 1819.27, "valor_renda_maxima": 2500.00, "valor_quota": 30.00}
        ]
    payload = {
        "data_inicio_vigencia": data_inicio_vigencia.isoformat(),
        "faixas": faixas,
        "observacao": observacao
    }
    if data_fim_vigencia:
        payload["data_fim_vigencia"] = data_fim_vigencia.isoformat()
    return payload

# Testes de Criação
def test_criar_nova_tabela_salario_familia(client):
    payload = get_sf_payload(data_inicio_vigencia=date(2025, 1, 1))
    response = client.post("/param-legais/salario-familia/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data_inicio_vigencia"] == "2025-01-01"
    assert len(data["faixas"]) >= 1
    assert data["faixas"][0]["valor_quota"] == 62.04
    assert data["ativo"] is True

# Testes de Validação
@pytest.mark.parametrize(
    "field_to_remove, expected_detail_part",
    [
        ("data_inicio_vigencia", "Field required"),
        ("faixas", "Field required"),
    ]
)
def test_criar_sf_campos_obrigatorios_ausentes(client, field_to_remove, expected_detail_part):
    payload = get_sf_payload(data_inicio_vigencia=date(2025, 3, 1))
    del payload[field_to_remove]
    response = client.post("/param-legais/salario-familia/", json=payload)
    assert response.status_code == 422
    assert expected_detail_part in response.text

def test_criar_sf_faixa_sem_valor_quota(client):
    payload = get_sf_payload(data_inicio_vigencia=date(2025, 4, 1))
    payload["faixas"] = [{"valor_renda_maxima": 2000.00}] # valor_quota faltando
    response = client.post("/param-legais/salario-familia/", json=payload)
    assert response.status_code == 422
    assert "faixas" in response.text.lower()
    assert "valor_quota" in response.text.lower() # Ajustar
    assert "Field required" in response.text

def test_criar_sf_valor_quota_negativo(client):
    payload = get_sf_payload(data_inicio_vigencia=date(2025, 4, 1))
    payload["faixas"] = [{"valor_renda_maxima": 1800.00, "valor_quota": -10.00}]
    response = client.post("/param-legais/salario-familia/", json=payload)
    assert response.status_code == 422
    assert "valor_quota" in response.text.lower()
    assert "must be greater than or equal to 0" in response.text.lower() # Ajustar

# Testes de Leitura
def test_listar_tabelas_sf(client):
    client.post("/param-legais/salario-familia/", json=get_sf_payload(date(2024,1,1)))
    response = client.get("/param-legais/salario-familia/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obter_tabela_sf_por_id(client):
    created_id = client.post("/param-legais/salario-familia/", json=get_sf_payload(date(2026,1,1))).json()["id_versao"]
    response_get = client.get(f"/param-legais/salario-familia/{created_id}")
    assert response_get.status_code == 200
    assert response_get.json()["id_versao"] == created_id

# Testes de Atualização
def test_atualizar_tabela_sf(client):
    id_v1 = client.post("/param-legais/salario-familia/", json=get_sf_payload(date(2027,1,1))).json()["id_versao"]
    payload_update = {
        "data_inicio_vigencia": date(2027,6,1).isoformat(),
        "faixas": [{"valor_renda_maxima": 1900.00, "valor_quota": 65.00}],
        "observacao": "SF V2"
    }
    response_update = client.put(f"/param-legais/salario-familia/{id_v1}", json=payload_update)
    assert response_update.status_code == 200
    data_updated = response_update.json()
    assert data_updated["faixas"][0]["valor_quota"] == 65.00
    assert data_updated["id_versao"] != id_v1

    v1_after_update = client.get(f"/param-legais/salario-familia/{id_v1}").json()
    assert v1_after_update["ativo"] is False

# Testes de Inativação
def test_inativar_tabela_sf(client):
    created_id = client.post("/param-legais/salario-familia/", json=get_sf_payload(date(2028,1,1))).json()["id_versao"]
    assert client.delete(f"/param-legais/salario-familia/{created_id}").status_code == 200
    assert client.get(f"/param-legais/salario-familia/{created_id}").json()["ativo"] is False

# Teste de Vigente
def test_obter_tabela_sf_vigente(client):
    client.post("/param-legais/salario-familia/", json=get_sf_payload(date(2023,1,1), faixas=[{"valor_renda_maxima":1700,"valor_quota":50}], data_fim_vigencia=date(2023,12,31)))
    client.post("/param-legais/salario-familia/", json=get_sf_payload(date(2024,1,1), faixas=[{"valor_renda_maxima":1800,"valor_quota":60}], data_fim_vigencia=date(2024,12,31)))
    client.post("/param-legais/salario-familia/", json=get_sf_payload(date(2025,1,1), faixas=[{"valor_renda_maxima":1900,"valor_quota":70}]))

    response = client.get("/param-legais/salario-familia/vigente?data_referencia=2024-06-30")
    assert response.status_code == 200
    assert response.json()["faixas"][0]["valor_quota"] == 60

    assert client.get("/param-legais/salario-familia/vigente?data_referencia=2022-01-01").status_code == 404