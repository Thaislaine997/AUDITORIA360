from datetime import date, timedelta
from typing import Optional

import pytest
from fastapi.testclient import TestClient

from services.api.main import app


# Fixture para o cliente de teste síncrono
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# Dados de exemplo para ParametrosFGTS
def get_fgts_payload(
    data_inicio_vigencia: date,
    aliquota_deposito_mensal: float = 8.0,
    aliquota_multa_rescisoria_saldo: float = 40.0,
    aliquota_contribuicao_social: Optional[float] = 10.0,  # Exemplo, pode ser None
    data_fim_vigencia: Optional[date] = None,
    observacao: Optional[str] = "Teste Parâmetros FGTS",
):
    payload = {
        "data_inicio_vigencia": data_inicio_vigencia.isoformat(),
        "aliquota_deposito_mensal": aliquota_deposito_mensal,
        "aliquota_multa_rescisoria_saldo": aliquota_multa_rescisoria_saldo,
        "observacao": observacao,
    }
    if aliquota_contribuicao_social is not None:  # Incluir apenas se não for None
        payload["aliquota_contribuicao_social"] = aliquota_contribuicao_social
    if data_fim_vigencia:
        payload["data_fim_vigencia"] = data_fim_vigencia.isoformat()
    return payload


# Testes de Criação (POST /param-legais/fgts/)


def test_criar_novos_parametros_fgts(client):
    payload = get_fgts_payload(data_inicio_vigencia=date(2025, 1, 1))
    response = client.post("/param-legais/fgts/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data_inicio_vigencia"] == "2025-01-01"
    assert data["aliquota_deposito_mensal"] == 8.0
    assert data["aliquota_multa_rescisoria_saldo"] == 40.0
    assert data["aliquota_contribuicao_social"] == 10.0  # Valor padrão da função helper
    assert data["observacao"] == "Teste Parâmetros FGTS"
    assert data["ativo"] is True
    assert "id_versao" in data


def test_criar_parametros_fgts_sem_contribuicao_social(client):
    payload = get_fgts_payload(
        data_inicio_vigencia=date(2025, 6, 1),
        aliquota_contribuicao_social=None,  # Testando omissão
    )
    response = client.post("/param-legais/fgts/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data_inicio_vigencia"] == "2025-06-01"
    assert data.get("aliquota_contribuicao_social") is None  # Deve ser None ou ausente


# Testes de Validação de Payload na Criação


@pytest.mark.parametrize(
    "field_to_remove, expected_detail_part",
    [
        ("data_inicio_vigencia", "Field required"),
        ("aliquota_deposito_mensal", "Field required"),
        ("aliquota_multa_rescisoria_saldo", "Field required"),
    ],
)
def test_criar_fgts_campos_obrigatorios_ausentes(
    client, field_to_remove, expected_detail_part
):
    payload = get_fgts_payload(data_inicio_vigencia=date(2025, 3, 1))
    del payload[field_to_remove]
    response = client.post("/param-legais/fgts/", json=payload)
    assert response.status_code == 422
    assert expected_detail_part in response.text


@pytest.mark.parametrize(
    "field_to_test, invalid_value, expected_error_msg_part",
    [
        (
            "aliquota_deposito_mensal",
            -1.0,
            "must be greater than or equal to 0",
        ),  # Ajustar msg
        (
            "aliquota_multa_rescisoria_saldo",
            101.0,
            "must be less than or equal to 100",
        ),  # Ajustar msg
        (
            "aliquota_contribuicao_social",
            -5.0,
            "must be greater than or equal to 0",
        ),  # Ajustar msg
    ],
)
def test_criar_fgts_aliquotas_invalidas(
    client, field_to_test, invalid_value, expected_error_msg_part
):
    payload = get_fgts_payload(data_inicio_vigencia=date(2025, 4, 1))
    payload[field_to_test] = invalid_value
    response = client.post("/param-legais/fgts/", json=payload)
    assert response.status_code == 422
    assert field_to_test in response.text.lower()
    assert (
        expected_error_msg_part in response.text.lower()
    )  # Ajustar conforme a mensagem real


def test_criar_fgts_data_fim_anterior_inicio(client):
    payload = get_fgts_payload(
        data_inicio_vigencia=date(2025, 5, 1),
        data_fim_vigencia=date(2025, 4, 30),  # Fim antes do início
    )
    response = client.post("/param-legais/fgts/", json=payload)
    assert response.status_code == 422
    assert "data_fim_vigencia" in response.text.lower()
    assert (
        "must be after or same as data_inicio_vigencia" in response.text.lower()
    )  # Ajustar


# Testes de Leitura (GET)


def test_listar_parametros_fgts(client):
    client.post("/param-legais/fgts/", json=get_fgts_payload(date(2024, 1, 1)))
    client.post("/param-legais/fgts/", json=get_fgts_payload(date(2024, 5, 1)))

    response = client.get("/param-legais/fgts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_obter_parametros_fgts_por_id(client):
    payload_create = get_fgts_payload(data_inicio_vigencia=date(2026, 1, 1))
    response_create = client.post("/param-legais/fgts/", json=payload_create)
    assert response_create.status_code == 201
    created_id = response_create.json()["id_versao"]

    response_get = client.get(f"/param-legais/fgts/{created_id}")
    assert response_get.status_code == 200
    data_get = response_get.json()
    assert data_get["id_versao"] == created_id
    assert data_get["aliquota_deposito_mensal"] == 8.0


def test_obter_parametros_fgts_por_id_nao_encontrado(client):
    response_get = client.get(f"/param-legais/fgts/id_inexistente_fgts_123")
    assert response_get.status_code == 404
    assert (
        "Parâmetros FGTS não encontrados" in response_get.json()["detail"]
    )  # Ajustar msg


# Testes de Atualização (PUT)


def test_atualizar_parametros_fgts(client):
    payload_v1 = get_fgts_payload(
        data_inicio_vigencia=date(2027, 1, 1),
        aliquota_deposito_mensal=7.0,
        observacao="FGTS V1",
    )
    response_v1 = client.post("/param-legais/fgts/", json=payload_v1)
    assert response_v1.status_code == 201
    id_v1 = response_v1.json()["id_versao"]

    payload_update = {
        "data_inicio_vigencia": date(2027, 6, 1).isoformat(),
        "aliquota_deposito_mensal": 8.5,
        "observacao": "FGTS V2 - Atualizado",
    }
    response_update = client.put(f"/param-legais/fgts/{id_v1}", json=payload_update)
    assert response_update.status_code == 200

    data_updated_new_version = response_update.json()
    assert data_updated_new_version["aliquota_deposito_mensal"] == 8.5
    assert data_updated_new_version["observacao"] == "FGTS V2 - Atualizado"
    assert data_updated_new_version["data_inicio_vigencia"] == "2027-06-01"
    assert data_updated_new_version["ativo"] is True
    assert data_updated_new_version["id_versao"] != id_v1

    response_get_v1_after_update = client.get(f"/param-legais/fgts/{id_v1}")
    assert response_get_v1_after_update.status_code == 200
    data_v1_after_update = response_get_v1_after_update.json()
    assert data_v1_after_update["ativo"] is False
    assert (
        data_v1_after_update["data_fim_vigencia"]
        == (date(2027, 6, 1) - timedelta(days=1)).isoformat()
    )


def test_atualizar_parametros_fgts_nao_encontrado(client):
    payload_update = {"aliquota_deposito_mensal": 9.0}
    response_update = client.put(
        f"/param-legais/fgts/id_inexistente_fgts_put", json=payload_update
    )
    assert response_update.status_code == 404
    assert (
        "Parâmetros FGTS não encontrados" in response_update.json()["detail"]
    )  # Ajustar msg


# Testes de Inativação (DELETE)


def test_inativar_parametros_fgts(client):
    payload_create = get_fgts_payload(data_inicio_vigencia=date(2028, 1, 1))
    response_create = client.post("/param-legais/fgts/", json=payload_create)
    assert response_create.status_code == 201
    created_id = response_create.json()["id_versao"]

    response_delete = client.delete(f"/param-legais/fgts/{created_id}")
    assert response_delete.status_code == 200
    deleted_data = response_delete.json()
    assert deleted_data["ativo"] is False
    assert deleted_data["id_versao"] == created_id

    response_get_after_delete = client.get(f"/param-legais/fgts/{created_id}")
    assert response_get_after_delete.json()["ativo"] is False


def test_inativar_parametros_fgts_nao_encontrado(client):
    response_delete = client.delete(f"/param-legais/fgts/id_inexistente_fgts_delete")
    assert response_delete.status_code == 404
    assert (
        "Parâmetros FGTS não encontrados" in response_delete.json()["detail"]
    )  # Ajustar msg


# Teste de consulta de vigente


def test_obter_parametros_fgts_vigentes_em_data_especifica(client):
    client.post(
        "/param-legais/fgts/",
        json=get_fgts_payload(
            date(2023, 1, 1),
            aliquota_deposito_mensal=7.0,
            data_fim_vigencia=date(2023, 12, 31),
        ),
    )
    client.post(
        "/param-legais/fgts/",
        json=get_fgts_payload(
            date(2024, 1, 1),
            aliquota_deposito_mensal=8.0,
            data_fim_vigencia=date(2024, 12, 31),
        ),
    )
    client.post(
        "/param-legais/fgts/",
        json=get_fgts_payload(date(2025, 1, 1), aliquota_deposito_mensal=8.5),
    )

    response = client.get("/param-legais/fgts/vigente?data_referencia=2024-07-15")
    assert response.status_code == 200
    data = response.json()
    assert data["aliquota_deposito_mensal"] == 8.0
    assert data["data_inicio_vigencia"] == "2024-01-01"

    response_futuro = client.get(
        "/param-legais/fgts/vigente?data_referencia=2025-07-15"
    )
    assert response_futuro.status_code == 200
    assert response_futuro.json()["aliquota_deposito_mensal"] == 8.5

    response_passado_sem_vigencia = client.get(
        "/param-legais/fgts/vigente?data_referencia=2022-01-01"
    )
    assert response_passado_sem_vigencia.status_code == 404
    assert (
        "Nenhum Parâmetro FGTS vigente encontrado"
        in response_passado_sem_vigencia.json()["detail"]
    )  # Ajustar msg
