import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from src.api.main import app
from src.utils.config_manager import get_current_config
from core.database import SessionLocal, get_db_session_context
import builtins 
import json     

@pytest.fixture
def client(mocker): # Removido 'request' não utilizado
    original_builtins_open = builtins.open
    original_json_load = json.load

    # Removido autospec=True. Quando 'new' é fornecido, autospec não é usado
    # e causaria o TypeError que estamos vendo.
    mocker.patch('builtins.open', new=original_builtins_open)
    mocker.patch('json.load', new=original_json_load)

    original_config_dependency_override = app.dependency_overrides.pop(get_current_config, None)
    
    try:
        with TestClient(app) as c:
            yield c
    finally:
        if original_config_dependency_override is not None:
            app.dependency_overrides[get_current_config] = original_config_dependency_override
        else:
            app.dependency_overrides.pop(get_current_config, None)

def test_auditorias_isolamento(client):
    # Simula dois clientes diferentes
    headers_a = {"x-client-id": "cliente_a"}
    headers_b = {"x-client-id": "cliente_b"}
    # Cliente A só vê suas auditorias
    resp_a = client.get("/api/v1/auditorias/", headers=headers_a)
    assert resp_a.status_code == 200
    for item in resp_a.json().get("items", []):
        assert item["client_id"] == "cliente_a"
    # Cliente B só vê suas auditorias
    resp_b = client.get("/api/v1/auditorias/", headers=headers_b)
    assert resp_b.status_code == 200
    for item in resp_b.json().get("items", []):
        assert item["client_id"] == "cliente_b"
    # Cliente A não pode acessar auditoria de B
    if resp_b.json().get("items"):
        id_b = resp_b.json()["items"][0]["id_folha"]
        resp_cross = client.get(f"/api/v1/auditorias/{id_b}", headers=headers_a)
        assert resp_cross.status_code in (403, 404)

def test_auditorias_auth_required(client):
    # Sem autenticação deve bloquear
    resp = client.get("/api/v1/auditorias/")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente ou inválido."

def test_get_auditoria_by_id_auth_required(client):
    resp = client.get("/api/v1/auditorias/some_id")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente ou inválido."

def test_create_auditoria_auth_required(client):
    resp = client.post("/api/v1/auditorias/", json={"nome": "Nova Auditoria"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente ou inválido."

def test_update_auditoria_auth_required(client):
    resp = client.put("/api/v1/auditorias/some_id", json={"nome": "Auditoria Atualizada"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente ou inválido."

def test_delete_auditoria_auth_required(client):
    resp = client.delete("/api/v1/auditorias/some_id")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente ou inválido."
