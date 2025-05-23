import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from src.main import app # Supondo que seu app FastAPI principal esteja em src.main
from src.schemas import TabelaSalarioMinimo # Alterado de SalarioMinimo
from datetime import date, timedelta
from typing import Optional, Dict

# Fixture para o cliente de teste síncrono
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Dados de exemplo para SalarioMinimo
def get_sm_payload(
    data_inicio_vigencia: date,
    valor_nacional: float,
    data_fim_vigencia: Optional[date] = None,
    valores_regionais: Optional[Dict[str, float]] = None,
    observacao: Optional[str] = "Teste Salário Mínimo"
):
    payload = {
        "data_inicio_vigencia": data_inicio_vigencia.isoformat(),
        "valor_nacional": valor_nacional,
        "observacao": observacao
    }
    if data_fim_vigencia:
        payload["data_fim_vigencia"] = data_fim_vigencia.isoformat()
    if valores_regionais:
        payload["valores_regionais"] = valores_regionais # API espera um dict que será convertido para JSON
    return payload

# Testes de Criação (POST /param-legais/salario-minimo/)

def test_criar_novo_salario_minimo(client):
    payload = get_sm_payload(data_inicio_vigencia=date(2025, 1, 1), valor_nacional=1500.00)
    response = client.post("/param-legais/salario-minimo/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data_inicio_vigencia"] == "2025-01-01"
    assert data["valor_nacional"] == 1500.00
    assert data["observacao"] == "Teste Salário Mínimo"
    assert data["ativo"] is True
    assert "id_versao" in data

def test_criar_salario_minimo_com_regionais_e_fim_vigencia(client):
    payload = get_sm_payload(
        data_inicio_vigencia=date(2025, 6, 1),
        valor_nacional=1550.00,
        data_fim_vigencia=date(2025, 12, 31),
        valores_regionais={"SP": 1600.00, "RJ": 1580.00},
        observacao="SM com regionais"
    )
    response = client.post("/param-legais/salario-minimo/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data_inicio_vigencia"] == "2025-06-01"
    assert data["data_fim_vigencia"] == "2025-12-31"
    assert data["valor_nacional"] == 1550.00
    assert data["valores_regionais"] == {"SP": 1600.00, "RJ": 1580.00}
    assert data["observacao"] == "SM com regionais"

# Testes de Validação de Payload na Criação

@pytest.mark.parametrize(
    "field_to_remove, expected_detail_part",
    [
        ("data_inicio_vigencia", "Field required"), # FastAPI 0.100+
        ("valor_nacional", "Field required"),
    ]
)
def test_criar_salario_minimo_campos_obrigatorios_ausentes(client, field_to_remove, expected_detail_part):
    payload = get_sm_payload(data_inicio_vigencia=date(2025, 3, 1), valor_nacional=1520.00)
    del payload[field_to_remove]
    response = client.post("/param-legais/salario-minimo/", json=payload)
    assert response.status_code == 422
    assert expected_detail_part in response.text


def test_criar_salario_minimo_valor_nacional_negativo(client):
    payload = get_sm_payload(data_inicio_vigencia=date(2025, 4, 1), valor_nacional=-100.00)
    response = client.post("/param-legais/salario-minimo/", json=payload)
    assert response.status_code == 422
    # A mensagem exata pode variar dependendo da validação do Pydantic (ex: "greater than 0")
    assert "valor_nacional" in response.text.lower()
    assert "must be greater than 0" in response.text.lower() # Ajustar conforme a mensagem real

def test_criar_salario_minimo_data_fim_anterior_inicio(client):
    payload = get_sm_payload(
        data_inicio_vigencia=date(2025, 5, 1),
        valor_nacional=1530.00,
        data_fim_vigencia=date(2025, 4, 30) # Fim antes do início
    )
    response = client.post("/param-legais/salario-minimo/", json=payload)
    assert response.status_code == 422 # Ou 400 dependendo da validação (schema vs. lógica de negócios)
    assert "data_fim_vigencia" in response.text.lower()
    assert "must be after or same as data_inicio_vigencia" in response.text.lower() # Ajustar

# Testes de Leitura (GET)

def test_listar_salarios_minimos(client):
    # Criar alguns para garantir que a lista não esteja vazia
    client.post("/param-legais/salario-minimo/", json=get_sm_payload(date(2024,1,1), 1400))
    client.post("/param-legais/salario-minimo/", json=get_sm_payload(date(2024,5,1), 1450))

    response = client.get("/param-legais/salario-minimo/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2 # Pelo menos os que acabamos de criar

def test_obter_salario_minimo_por_id(client):
    payload_create = get_sm_payload(data_inicio_vigencia=date(2026, 1, 1), valor_nacional=1600.00)
    response_create = client.post("/param-legais/salario-minimo/", json=payload_create)
    assert response_create.status_code == 201
    created_id = response_create.json()["id_versao"]

    response_get = client.get(f"/param-legais/salario-minimo/{created_id}")
    assert response_get.status_code == 200
    data_get = response_get.json()
    assert data_get["id_versao"] == created_id
    assert data_get["valor_nacional"] == 1600.00

def test_obter_salario_minimo_por_id_nao_encontrado(client):
    response_get = client.get(f"/param-legais/salario-minimo/id_inexistente_123")
    assert response_get.status_code == 404
    assert "Salário Mínimo não encontrado" in response_get.json()["detail"]


# Testes de Atualização (PUT) - Lembre-se que a API cria uma nova versão

def test_atualizar_salario_minimo(client):
    # Criar um item inicial
    payload_v1 = get_sm_payload(data_inicio_vigencia=date(2027, 1, 1), valor_nacional=1700.00, observacao="Versão 1")
    response_v1 = client.post("/param-legais/salario-minimo/", json=payload_v1)
    assert response_v1.status_code == 201
    id_v1 = response_v1.json()["id_versao"]
    data_v1 = response_v1.json()
    assert data_v1["ativo"] is True

    # Payload para atualização (na verdade, cria uma nova versão)
    # A API de PUT deve receber o ID da versão que está sendo "substituída" ou "expirada"
    # e o payload da nova versão.
    # A lógica exata do PUT /param-legais/salario-minimo/{id_versao} precisa ser confirmada.
    # Se o PUT atualiza no local (o que não é ideal para histórico), o teste seria diferente.
    # Assumindo que PUT cria uma nova versão e inativa a antiga:
    payload_update = {
        "data_inicio_vigencia": date(2027, 6, 1).isoformat(), # Nova data de início
        "valor_nacional": 1750.00,
        "observacao": "Versão 2 - Atualizada"
        # data_fim_vigencia da versão anterior (id_v1) deveria ser ajustada para 2027-05-31
    }
    response_update = client.put(f"/param-legais/salario-minimo/{id_v1}", json=payload_update)
    assert response_update.status_code == 200 # Ou 201 se retornar o novo objeto criado
    
    data_updated_new_version = response_update.json() # Esta deve ser a NOVA versão
    assert data_updated_new_version["valor_nacional"] == 1750.00
    assert data_updated_new_version["observacao"] == "Versão 2 - Atualizada"
    assert data_updated_new_version["data_inicio_vigencia"] == "2027-06-01"
    assert data_updated_new_version["ativo"] is True
    new_id = data_updated_new_version["id_versao"]
    assert new_id != id_v1

    # Verificar se a versão antiga (id_v1) foi inativada e/ou teve data_fim_vigencia ajustada
    response_get_v1_after_update = client.get(f"/param-legais/salario-minimo/{id_v1}")
    assert response_get_v1_after_update.status_code == 200
    data_v1_after_update = response_get_v1_after_update.json()
    assert data_v1_after_update["ativo"] is False # Ou verificar data_fim_vigencia
    assert data_v1_after_update["data_fim_vigencia"] == (date(2027, 6, 1) - timedelta(days=1)).isoformat()


def test_atualizar_salario_minimo_nao_encontrado(client):
    payload_update = {"valor_nacional": 1800.00, "observacao": "Tentativa de Update"}
    response_update = client.put(f"/param-legais/salario-minimo/id_inexistente_put", json=payload_update)
    assert response_update.status_code == 404
    assert "Salário Mínimo não encontrado" in response_update.json()["detail"]

# Testes de Inativação (DELETE)

def test_inativar_salario_minimo(client):
    payload_create = get_sm_payload(data_inicio_vigencia=date(2028, 1, 1), valor_nacional=1800.00)
    response_create = client.post("/param-legais/salario-minimo/", json=payload_create)
    assert response_create.status_code == 201
    created_id = response_create.json()["id_versao"]

    # Verificar que está ativo antes de deletar
    response_get_before_delete = client.get(f"/param-legais/salario-minimo/{created_id}")
    assert response_get_before_delete.json()["ativo"] is True

    response_delete = client.delete(f"/param-legais/salario-minimo/{created_id}")
    assert response_delete.status_code == 200 # Ou 204 se não retornar conteúdo
    deleted_data = response_delete.json()
    assert deleted_data["ativo"] is False
    assert deleted_data["id_versao"] == created_id

    # Verificar que está inativo após deletar
    response_get_after_delete = client.get(f"/param-legais/salario-minimo/{created_id}")
    assert response_get_after_delete.status_code == 200
    assert response_get_after_delete.json()["ativo"] is False


def test_inativar_salario_minimo_nao_encontrado(client):
    response_delete = client.delete(f"/param-legais/salario-minimo/id_inexistente_delete")
    assert response_delete.status_code == 404
    assert "Salário Mínimo não encontrado" in response_delete.json()["detail"]

# Placeholder para teste de consulta de vigente (precisa de mais cenários)
def test_obter_salario_minimo_vigente_em_data_especifica(client):
    # Setup: Criar algumas vigências
    client.post("/param-legais/salario-minimo/", json=get_sm_payload(date(2023, 1, 1), 1300, data_fim_vigencia=date(2023,12,31)))
    client.post("/param-legais/salario-minimo/", json=get_sm_payload(date(2024, 1, 1), 1400, data_fim_vigencia=date(2024,12,31)))
    client.post("/param-legais/salario-minimo/", json=get_sm_payload(date(2025, 1, 1), 1500)) # Vigente atualmente

    response = client.get("/param-legais/salario-minimo/vigente?data_referencia=2024-07-15")
    assert response.status_code == 200
    data = response.json()
    assert data["valor_nacional"] == 1400.00
    assert data["data_inicio_vigencia"] == "2024-01-01"

    response_futuro = client.get("/param-legais/salario-minimo/vigente?data_referencia=2025-07-15")
    assert response_futuro.status_code == 200
    assert response_futuro.json()["valor_nacional"] == 1500.00
    
    response_passado_sem_vigencia = client.get("/param-legais/salario-minimo/vigente?data_referencia=2022-01-01")
    assert response_passado_sem_vigencia.status_code == 404 # Ou retorna None/lista vazia dependendo da API
    assert "Nenhum Salário Mínimo vigente encontrado" in response_passado_sem_vigencia.json()["detail"]
# Testes de Conflito de Vigência (POST e PUT)

@pytest.mark.asyncio
async def test_criar_salario_minimo_conflito_vigencia_total(client: AsyncClient):
    # Criar uma tabela que cobre um período
    payload_v1 = get_sm_payload(data_inicio_vigencia=date(2029, 1, 1), valor_nacional=2000.00, data_fim_vigencia=date(2029, 12, 31))
    response_v1 = await client.post("/param-legais/salario-minimo/", json=payload_v1)
    assert response_v1.status_code == status.HTTP_201_CREATED

    # Tentar criar outra tabela que cobre o mesmo período
    payload_conflito = get_sm_payload(data_inicio_vigencia=date(2029, 1, 1), valor_nacional=2100.00, data_fim_vigencia=date(2029, 12, 31))
    response_conflito = await client.post("/param-legais/salario-minimo/", json=payload_conflito)
    assert response_conflito.status_code == status.HTTP_409_CONFLICT
    assert "Conflito de vigência detectado" in response_conflito.json()["detail"]

@pytest.mark.asyncio
async def test_criar_salario_minimo_conflito_vigencia_parcial_inicio(client: AsyncClient):
    # Criar uma tabela que cobre um período
    payload_v1 = get_sm_payload(data_inicio_vigencia=date(2030, 6, 1), valor_nacional=2200.00, data_fim_vigencia=date(2030, 12, 31))
    response_v1 = await client.post("/param-legais/salario-minimo/", json=payload_v1)
    assert response_v1.status_code == status.HTTP_201_CREATED
