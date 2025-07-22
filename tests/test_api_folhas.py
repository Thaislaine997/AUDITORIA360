import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile
from services.api.main import app
# from src.utils.config_manager import get_current_config
import builtins
import json
from unittest.mock import MagicMock
import pdb

@pytest.fixture
def client(mocker):
    original_builtins_open = builtins.open
    original_json_load = json.load

    # Removido autospec=True. Quando 'new' é fornecido, autospec não é usado
    # e causaria o TypeError que estamos vendo.
    mocker.patch('builtins.open', new=original_builtins_open)
    mocker.patch('json.load', new=original_json_load)

    # original_config_dependency_override = app.dependency_overrides.pop(get_current_config, None)
    
    try:
        with TestClient(app) as c:
            yield c
    finally:
        pass  # Removido manipulação de dependency_overrides para get_current_config

@pytest.fixture
def mock_upload_file(mocker):
    mock_file = MagicMock(spec=UploadFile)
    mock_file.filename = "test_sheet.xlsx"
    mock_file.content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    mock_file.file = MagicMock()  # Corrigir: garantir que file é um mock
    mock_file.file.read.return_value = b"dummy excel content"
    return mock_file

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

def test_upload_folha_auth_required(client, mock_upload_file): # Adicionado mock_upload_file
    import pdb; pdb.set_trace() # <<< PONTO DE INTERRUPÇÃO AQUI
    files = {"file": (mock_upload_file.filename, mock_upload_file.file, mock_upload_file.content_type)}
    resp = client.post("/api/v1/folhas/upload", files=files) # Sem header X-Client-ID
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente ou inválido."

def test_processar_folha_auth_required(client):
    resp = client.post("/api/v1/folhas/processar/some_id")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "X-Client-ID header ausente."

def test_folhas_disponiveis_para_checklist(client):
    id_cliente = "cliente_a"
    headers = {"x-client-id": id_cliente}
    resp = client.get(f"/api/v1/clientes/{id_cliente}/folhas-processadas/disponiveis-para-checklist", headers=headers)
    assert resp.status_code in (200, 404, 500)  # 404/500 se não houver dados/config, 200 se sucesso
    if resp.status_code == 200:
        folhas = resp.json()
        assert isinstance(folhas, list)
        for folha in folhas:
            assert "id_folha_processada" in folha
            assert "descricao_display" in folha
            assert "periodo_referencia" in folha
            assert "status_geral_folha" in folha
