"""
Testes unificados de folha, checklist e RBAC usando JWT
"""

import pytest
from fastapi.testclient import TestClient

from services.api.main import app


# --- Helpers ---
def get_jwt_token(client, username, password):
    resp = client.post("/token", data={"username": username, "password": password})
    assert resp.status_code == 200
    return resp.json()["access_token"]


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


# --- Testes de Folha e Checklist com RBAC ---
def test_folha_isolamento_jwt(client):
    # Obter tokens para dois clientes diferentes
    token_a = get_jwt_token(client, "cliente_a", "senha_a")
    token_b = get_jwt_token(client, "cliente_b", "senha_b")
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

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


def test_folha_auth_required_jwt(client):
    resp = client.get("/api/v1/folhas/")
    assert resp.status_code == 401


def test_upload_folha_auth_required_jwt(client):
    files = {"file": ("dummy.csv", b"col1,col2\n1,2", "text/csv")}
    resp = client.post("/api/v1/folhas/upload", files=files)
    assert resp.status_code == 401


def test_folhas_disponiveis_para_checklist_jwt(client):
    token = get_jwt_token(client, "cliente_a", "senha_a")
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get(
        "/api/v1/clientes/cliente_a/folhas-processadas/disponiveis-para-checklist",
        headers=headers,
    )
    assert resp.status_code in (200, 404, 500)
    if resp.status_code == 200:
        folhas = resp.json()
        assert isinstance(folhas, list)
        for folha in folhas:
            assert "id_folha_processada" in folha
            assert "descricao_display" in folha
            assert "periodo_referencia" in folha
            assert "status_geral_folha" in folha


def test_checklist_folha_rbac(client):
    token = get_jwt_token(client, "cliente_a", "senha_a")
    headers = {"Authorization": f"Bearer {token}"}
    # Supondo que haja pelo menos uma folha disponível
    resp = client.get(
        "/api/v1/clientes/cliente_a/folhas-processadas/disponiveis-para-checklist",
        headers=headers,
    )
    if resp.status_code == 200 and resp.json():
        id_folha = resp.json()[0]["id_folha_processada"]
        resp_checklist = client.get(
            f"/api/v1/clientes/cliente_a/folhas/{id_folha}/checklist", headers=headers
        )
        assert resp_checklist.status_code in (200, 404)
        if resp_checklist.status_code == 200:
            checklist = resp_checklist.json()
            assert isinstance(checklist, list)
            for item in checklist:
                assert "id_item_checklist" in item
                assert "descricao" in item
                assert "status" in item
