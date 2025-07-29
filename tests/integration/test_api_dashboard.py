# from src.utils.config_manager import get_current_config # Importar get_current_config
import builtins
import json
from unittest.mock import patch as mock_patch  # Renomear para evitar conflito

import pytest
from fastapi.testclient import TestClient

from services.api.main import app


@pytest.fixture
def client(mocker):  # Removido 'request' não utilizado
    original_builtins_open = builtins.open
    original_json_load = json.load

    # Removido autospec=True. Quando 'new' é fornecido, autospec não é usado
    # e causaria o TypeError que estamos vendo.
    mocker.patch("builtins.open", new=original_builtins_open)
    mocker.patch("json.load", new=original_json_load)

    # original_config_dependency_override = app.dependency_overrides.pop(get_current_config, None)

    try:
        with TestClient(app) as c:
            yield c
    finally:
        pass  # Removido manipulação de dependency_overrides para get_current_config


def test_dashboard_isolamento(client):
    headers_a = {"x-client-id": "cliente_a"}
    headers_b = {"x-client-id": "cliente_b"}
    resp_a = client.get("/api/v1/dashboard/", headers=headers_a)
    assert resp_a.status_code == 200
    for item in resp_a.json().get("items", []):
        assert item["client_id"] == "cliente_a"
    resp_b = client.get("/api/v1/dashboard/", headers=headers_b)
    assert resp_b.status_code == 200
    for item in resp_b.json().get("items", []):
        assert item["client_id"] == "cliente_b"
    # Cliente A não pode acessar dashboard de B
    if resp_b.json().get("items"):
        id_b = resp_b.json()["items"][0]["id_dashboard"]
        resp_cross = client.get(f"/api/v1/dashboard/{id_b}", headers=headers_a)
        assert resp_cross.status_code in (403, 404)


def test_dashboard_auth_required(client):
    resp = client.get("/api/v1/dashboard/")
    assert resp.status_code == 401
    # A mensagem correta é "X-Client-ID header ausente ou inválido."
    assert resp.json()["detail"] == "X-Client-ID header ausente ou inválido."
