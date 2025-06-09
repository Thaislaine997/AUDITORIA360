import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from src.api.main import app

client = TestClient(app)

def test_get_alertas_empty(monkeypatch):
    # Deve retornar lista vazia quando não houver alertas
    monkeypatch.setattr(
        "src.controllers.cct_controller.listar_alertas", lambda status=None: []
    )
    response = client.get("/api/v1/ccts/alerts")
    assert response.status_code == 200
    assert response.json() == []


def test_get_alertas_success(monkeypatch):
    # Deve retornar alertas mockados corretamente
    fake_alertas = [
        {
            "id_alerta_cct": "alerta1",
            "status_alerta": "NOVO",
            "data_deteccao": datetime(2025, 1, 1, 12, 0, 0)
        }
    ]
    monkeypatch.setattr(
        "src.controllers.cct_controller.listar_alertas", lambda status=None: fake_alertas
    )
    response = client.get("/api/v1/ccts/alerts")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)
    assert len(json_data) == 1
    assert json_data[0]["id_alerta_cct"] == "alerta1"
    assert json_data[0]["status_alerta"] == "NOVO"


def test_update_alerta_status_success(monkeypatch):
    # Deve atualizar o status do alerta e retornar o dado atualizado
    async def mock_update(id_alerta, payload):
        return {
            "id_alerta_cct": id_alerta,
            "status_alerta": payload.status_alerta,
            "notas_admin": payload.notas_admin,
            "data_deteccao": datetime(2025, 1, 1, 12, 0, 0)
        }

    monkeypatch.setattr(
        "src.controllers.cct_controller.atualizar_status_alerta", mock_update
    )
    payload = {"status_alerta": "RESOLVIDO", "notas_admin": "Tudo ok"}
    response = client.put("/api/v1/ccts/alerts/alerta1", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["id_alerta_cct"] == "alerta1"
    assert json_data["status_alerta"] == "RESOLVIDO"
    assert json_data["notas_admin"] == "Tudo ok"


def test_update_alerta_status_bad_request():
    # Deve retornar 422 se payload estiver incompleto
    response = client.put("/api/v1/ccts/alerts/alerta1", json={})
    assert response.status_code == 422


def test_update_alerta_status_invalido(monkeypatch):
    async def mock_update(id_alerta, payload):
        raise ValueError("Status inválido")
    monkeypatch.setattr(
        "src.controllers.cct_controller.atualizar_status_alerta", mock_update
    )
    payload = {"status_alerta": "STATUS_INVALIDO", "notas_admin": "Teste"}
    response = client.put("/api/v1/ccts/alerts/alerta1", json=payload)
    # Pode retornar 400 ou 422 dependendo da validação
    assert response.status_code in (400, 422)


def test_update_alerta_nao_encontrado(monkeypatch):
    async def mock_update(id_alerta, payload):
        return None
    monkeypatch.setattr(
        "src.controllers.cct_controller.atualizar_status_alerta", mock_update
    )
    payload = {"status_alerta": "CCT_IMPORTADA", "notas_admin": "Teste"}
    response = client.put("/api/v1/ccts/alerts/inexistente", json=payload)
    assert response.status_code == 404


def test_get_alerta_status_filter(monkeypatch):
    def fake_listar_alertas(status=None):
        assert status == "NOVO"
        return []
    monkeypatch.setattr(
        "src.controllers.cct_controller.listar_alertas", fake_listar_alertas
    )
    response = client.get("/api/v1/ccts/alerts", params={"status": "NOVO"})
    assert response.status_code == 200
    assert response.json() == []
