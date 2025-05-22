import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

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
    assert resp.json()["detail"] == "X-Client-ID header ausente."

def test_get_auditoria_by_id_auth_required(client):
    resp = client.get("/api/v1/auditorias/some_id")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente."

def test_create_auditoria_auth_required(client):
    resp = client.post("/api/v1/auditorias/", json={"nome": "Nova Auditoria"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente."

def test_update_auditoria_auth_required(client):
    resp = client.put("/api/v1/auditorias/some_id", json={"nome": "Auditoria Atualizada"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente."

def test_delete_auditoria_auth_required(client):
    resp = client.delete("/api/v1/auditorias/some_id")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente."
