import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.schemas_models import TabelaINSS, FaixaINSS
from datetime import date, timedelta
from typing import List, Optional

# Fixture para o cliente de teste síncrono
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Dados de exemplo para TabelaINSS
def get_inss_payload(
    data_inicio_vigencia: date,
    faixas: Optional[List[dict]] = None, # Usar dict para o payload JSON
    valor_teto_contribuicao: float = 7786.02,
    data_fim_vigencia: Optional[date] = None,
    observacao: Optional[str] = "Teste Tabela INSS"
):
    if faixas is None:
        faixas = [
            {"valor_inicial": 0, "valor_final": 1412.00, "aliquota": 7.5},
            {"valor_inicial": 1412.01, "valor_final": 2666.68, "aliquota": 9.0},
            {"valor_inicial": 2666.69, "valor_final": 4000.03, "aliquota": 12.0},
            {"valor_inicial": 4000.04, "valor_final": valor_teto_contribuicao, "aliquota": 14.0}, # Última faixa até o teto
        ]
    payload = {
        "data_inicio_vigencia": data_inicio_vigencia.isoformat(),
        "faixas": faixas,
        "valor_teto_contribuicao": valor_teto_contribuicao,
        "observacao": observacao
    }
    if data_fim_vigencia:
        payload["data_fim_vigencia"] = data_fim_vigencia.isoformat()
    return payload

# Testes de Criação (POST /param-legais/inss/)

def test_criar_nova_tabela_inss(client):
    payload = get_inss_payload(data_inicio_vigencia=date(2025, 1, 1))
    response = client.post("/param-legais/inss/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data_inicio_vigencia"] == "2025-01-01"
    assert len(data["faixas"]) == 4
    assert data["faixas"][0]["aliquota"] == 7.5
    assert data["valor_teto_contribuicao"] == 7786.02
    assert data["ativo"] is True
    assert "id_versao" in data

# Testes de Validação de Payload na Criação

@pytest.mark.parametrize(
    "field_to_remove, expected_detail_part",
    [
        ("data_inicio_vigencia", "Field required"),
        ("faixas", "Field required"),
        ("valor_teto_contribuicao", "Field required"),
    ]
)
def test_criar_inss_campos_obrigatorios_ausentes(client, field_to_remove, expected_detail_part):
    payload = get_inss_payload(data_inicio_vigencia=date(2025, 3, 1))
    del payload[field_to_remove]
    response = client.post("/param-legais/inss/", json=payload)
    assert response.status_code == 422
    assert expected_detail_part in response.text

def test_criar_inss_faixas_invalidas_formato(client):
    payload = get_inss_payload(data_inicio_vigencia=date(2025, 4, 1))
    payload["faixas"] = "nao_e_uma_lista" # Formato inválido
    response = client.post("/param-legais/inss/", json=payload)
    assert response.status_code == 422
    assert "faixas" in response.text.lower()
    # A mensagem exata pode variar, ex: "Input should be a valid list"

def test_criar_inss_faixa_sem_aliquota(client):
    payload = get_inss_payload(data_inicio_vigencia=date(2025, 4, 1))
    payload["faixas"] = [{"valor_inicial": 0, "valor_final": 1000}] # Aliquota faltando
    response = client.post("/param-legais/inss/", json=payload)
    assert response.status_code == 422
    assert "faixas" in response.text.lower()
    assert "aliquota" in response.text.lower()
    assert "Field required" in response.text # Para Pydantic v2

def test_criar_inss_valor_teto_negativo(client):
    payload = get_inss_payload(data_inicio_vigencia=date(2025, 4, 1), valor_teto_contribuicao=-100.00)
    response = client.post("/param-legais/inss/", json=payload)
    assert response.status_code == 422
    assert "valor_teto_contribuicao" in response.text.lower()
    assert "must be greater than 0" in response.text.lower() # Ajustar

def test_criar_inss_data_fim_anterior_inicio(client):
    payload = get_inss_payload(
        data_inicio_vigencia=date(2025, 5, 1),
        data_fim_vigencia=date(2025, 4, 30)
    )
    response = client.post("/param-legais/inss/", json=payload)
    assert response.status_code == 422
    assert "data_fim_vigencia" in response.text.lower()
    assert "must be after or same as data_inicio_vigencia" in response.text.lower() # Ajustar

# Testes de Leitura (GET)

def test_listar_tabelas_inss(client):
    client.post("/param-legais/inss/", json=get_inss_payload(date(2024,1,1)))
    response = client.get("/param-legais/inss/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_obter_tabela_inss_por_id(client):
    payload_create = get_inss_payload(data_inicio_vigencia=date(2026, 1, 1))
    response_create = client.post("/param-legais/inss/", json=payload_create)
    assert response_create.status_code == 201
    created_id = response_create.json()["id_versao"]

    response_get = client.get(f"/param-legais/inss/{created_id}")
    assert response_get.status_code == 200
    data_get = response_get.json()
    assert data_get["id_versao"] == created_id
    assert data_get["valor_teto_contribuicao"] == 7786.02

def test_obter_tabela_inss_por_id_nao_encontrado(client):
    response_get = client.get(f"/param-legais/inss/id_inss_inexistente_123")
    assert response_get.status_code == 404
    assert "Tabela INSS não encontrada" in response_get.json()["detail"] # Ajustar msg

# Testes de Atualização (PUT)

def test_atualizar_tabela_inss(client):
    payload_v1 = get_inss_payload(data_inicio_vigencia=date(2027, 1, 1), valor_teto_contribuicao=7500.00)
    response_v1 = client.post("/param-legais/inss/", json=payload_v1)
    assert response_v1.status_code == 201
    id_v1 = response_v1.json()["id_versao"]

    payload_update = {
        "data_inicio_vigencia": date(2027, 6, 1).isoformat(),
        "valor_teto_contribuicao": 7800.00,
        "faixas": [{"valor_inicial": 0, "valor_final": 1500, "aliquota": 7.0}], # Faixas simplificadas para teste
        "observacao": "INSS V2 - Atualizado"
    }
    response_update = client.put(f"/param-legais/inss/{id_v1}", json=payload_update)
    assert response_update.status_code == 200
    
    data_updated_new_version = response_update.json()
    assert data_updated_new_version["valor_teto_contribuicao"] == 7800.00
    assert data_updated_new_version["observacao"] == "INSS V2 - Atualizado"
    assert data_updated_new_version["ativo"] is True
    assert data_updated_new_version["id_versao"] != id_v1

    response_get_v1_after_update = client.get(f"/param-legais/inss/{id_v1}")
    data_v1_after_update = response_get_v1_after_update.json()
    assert data_v1_after_update["ativo"] is False
    assert data_v1_after_update["data_fim_vigencia"] == (date(2027, 6, 1) - timedelta(days=1)).isoformat()

def test_atualizar_tabela_inss_nao_encontrada(client):
    payload_update = {"valor_teto_contribuicao": 7900.00}
    response_update = client.put(f"/param-legais/inss/id_inss_inexistente_put", json=payload_update)
    assert response_update.status_code == 404

# Testes de Inativação (DELETE)

def test_inativar_tabela_inss(client):
    payload_create = get_inss_payload(data_inicio_vigencia=date(2028, 1, 1))
    response_create = client.post("/param-legais/inss/", json=payload_create)
    created_id = response_create.json()["id_versao"]

    response_delete = client.delete(f"/param-legais/inss/{created_id}")
    assert response_delete.status_code == 200
    assert response_delete.json()["ativo"] is False

    response_get_after_delete = client.get(f"/param-legais/inss/{created_id}")
    assert response_get_after_delete.json()["ativo"] is False

def test_inativar_tabela_inss_nao_encontrada(client):
    response_delete = client.delete(f"/param-legais/inss/id_inss_inexistente_delete")
    assert response_delete.status_code == 404

# Teste de consulta de vigente

def test_obter_tabela_inss_vigente_em_data_especifica(client):
    client.post("/param-legais/inss/", json=get_inss_payload(date(2023,1,1), valor_teto_contribuicao=7000, data_fim_vigencia=date(2023,12,31)))
    client.post("/param-legais/inss/", json=get_inss_payload(date(2024,1,1), valor_teto_contribuicao=7500, data_fim_vigencia=date(2024,12,31)))
    client.post("/param-legais/inss/", json=get_inss_payload(date(2025,1,1), valor_teto_contribuicao=8000))

    response = client.get("/param-legais/inss/vigente?data_referencia=2024-07-15")
    assert response.status_code == 200
    data = response.json()
    assert data["valor_teto_contribuicao"] == 7500
    assert data["data_inicio_vigencia"] == "2024-01-01"
    
    response_passado_sem_vigencia = client.get("/param-legais/inss/vigente?data_referencia=2022-01-01")
    assert response_passado_sem_vigencia.status_code == 404
    assert "Nenhuma Tabela INSS vigente encontrada" in response_passado_sem_vigencia.json()["detail"] # Ajustar