import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch, MagicMock
import pandas as pd
from src.config_manager import get_current_config # Importar get_current_config
import builtins
import json

@pytest.fixture
def client(mocker): # Removido 'request' não utilizado
    original_builtins_open = builtins.open
    original_json_load = json.load

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

# Mock data para cliente_a
empresas_cliente_a = [
    {"id_empresa": "empresa1_a", "nome_empresa": "Empresa Alpha", "client_id": "cliente_a"},
    {"id_empresa": "empresa2_a", "nome_empresa": "Empresa Beta", "client_id": "cliente_a"}
]
df_empresas_a = pd.DataFrame(empresas_cliente_a)

# Mock data para cliente_b
empresas_cliente_b = [
    {"id_empresa": "empresa1_b", "nome_empresa": "Empresa Gamma", "client_id": "cliente_b"}
]
df_empresas_b = pd.DataFrame(empresas_cliente_b)

@patch('src.routes.empresas_routes.get_loader_empresas')
def test_empresas_isolamento(mock_get_loader, client):
    mock_loader_instance_a = MagicMock()
    mock_loader_instance_b = MagicMock()

    def side_effect_loader(config):
        if config.get("client_id") == "cliente_a":
            mock_loader_instance_a.listar_todas_as_empresas.return_value = df_empresas_a
            # Mock para get_empresa_by_id para cliente_a
            def get_empresa_a(id_empresa):
                emp = df_empresas_a[df_empresas_a['id_empresa'] == id_empresa]
                return emp if not emp.empty else None
            mock_loader_instance_a.get_empresa_by_id.side_effect = get_empresa_a
            return mock_loader_instance_a
        elif config.get("client_id") == "cliente_b":
            mock_loader_instance_b.listar_todas_as_empresas.return_value = df_empresas_b
            # Mock para get_empresa_by_id para cliente_b
            def get_empresa_b(id_empresa):
                emp = df_empresas_b[df_empresas_b['id_empresa'] == id_empresa]
                return emp if not emp.empty else None
            mock_loader_instance_b.get_empresa_by_id.side_effect = get_empresa_b
            return mock_loader_instance_b
        return MagicMock() # Default mock se client_id não corresponder

    mock_get_loader.side_effect = side_effect_loader

    headers_a = {"x-client-id": "cliente_a"}
    headers_b = {"x-client-id": "cliente_b"}

    # Cliente A só vê suas empresas
    resp_a = client.get("/api/v1/empresas/", headers=headers_a)
    assert resp_a.status_code == 200
    response_data_a = resp_a.json().get("data", [])
    assert len(response_data_a) == len(empresas_cliente_a)
    for item in response_data_a:
        assert item["client_id"] == "cliente_a"

    # Cliente B só vê suas empresas
    resp_b = client.get("/api/v1/empresas/", headers=headers_b)
    assert resp_b.status_code == 200
    response_data_b = resp_b.json().get("data", [])
    assert len(response_data_b) == len(empresas_cliente_b)
    for item in response_data_b:
        assert item["client_id"] == "cliente_b"

    # Cliente A não pode acessar empresa de B
    if empresas_cliente_b:
        id_b = empresas_cliente_b[0]["id_empresa"]
        resp_cross = client.get(f"/api/v1/empresas/{id_b}", headers=headers_a)
        # Espera 403 (Acesso negado) porque o loader de A não encontrará/permitirá acesso à empresa de B
        # ou 404 se o mock de get_empresa_by_id de A retornar None para id_b
        assert resp_cross.status_code in (403, 404)

def test_empresas_auth_required(client): # Removido mock_get_config
    resp = client.get("/api/v1/empresas/")
    assert resp.status_code == 401
    # A mensagem correta é "X-Client-ID header ausente ou inválido."
    assert resp.json()["detail"] == "X-Client-ID header ausente ou inválido."

def test_get_empresa_by_id_auth_required(client):
    resp = client.get("/api/v1/empresas/some_id")
    assert resp.status_code == 401
    # A mensagem correta é "X-Client-ID header ausente ou inválido."
    assert resp.json()["detail"] == "X-Client-ID header ausente ou inválido."

# Mock para ControleFolhaLoader.get_empresa_by_id para o teste de acesso indevido
@patch('src.bq_loader.ControleFolhaLoader.get_empresa_by_id')
def test_acesso_indevido_empresa_by_id(mock_get_empresa_by_id, client):
    pass
