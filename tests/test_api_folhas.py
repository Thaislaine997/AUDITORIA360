import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_folhas_isolamento(client):
    headers_a = {"x-client-id": "cliente_a"}
    headers_b = {"x-client-id": "cliente_b"}
    # Cliente A só vê suas folhas
    resp_a = client.get("/api/v1/folhas/", headers=headers_a)
    assert resp_a.status_code == 200
    for item in resp_a.json().get("items", []):
        assert item["client_id"] == "cliente_a"
    # Cliente B só vê suas folhas
    resp_b = client.get("/api/v1/folhas/", headers=headers_b)
    assert resp_b.status_code == 200
    for item in resp_b.json().get("items", []):
        assert item["client_id"] == "cliente_b"
    # Cliente A não pode acessar folha de B
    if resp_b.json().get("items"):
        id_b = resp_b.json()["items"][0]["id_folha"]
        resp_cross = client.get(f"/api/v1/folhas/{id_b}", headers=headers_a)
        assert resp_cross.status_code in (403, 404)

def test_folhas_auth_required(client):
    resp = client.get("/api/v1/folhas/")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente."

def test_get_folha_by_id_auth_required(client):
    resp = client.get("/api/v1/folhas/some_id")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente."

def test_upload_folha_auth_required(client, mock_upload_file):
    # Corrigido o endpoint para /api/v1/folhas/importar-csv/
    # Adicionado os query parameters obrigatórios com valores mock
    resp = client.post(
        "/api/v1/folhas/importar-csv/?ano_referencia=2023&mes_referencia=12", 
        files={"csv_file": mock_upload_file} # Alterado "file" para "csv_file" para corresponder ao endpoint
    )
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente."

def test_processar_folha_auth_required(client):
    resp = client.post("/api/v1/folhas/processar/some_id")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente."
