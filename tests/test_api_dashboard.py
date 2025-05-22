import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

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
    assert resp.json()["detail"] == "X-Client-ID header ausente."

@pytest.mark.skip(reason="Rota /api/v1/dashboard/painel-contabil ainda não implementada ou com mock pendente")
def test_get_painel_contabil_auth_required(client):
    pass

@pytest.mark.skip(reason="Rota /api/v1/dashboard/analise-risco ainda não implementada ou com mock pendente")
def test_get_analise_risco_auth_required(client):
    pass

@pytest.mark.skip(reason="Rota /api/v1/dashboard/metricas-compliance ainda não implementada ou com mock pendente")
def test_get_metricas_compliance_auth_required(client):
    pass
