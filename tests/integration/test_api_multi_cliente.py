# ...existing code...
# from src.utils.config_manager import get_current_config
import builtins
import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from services.api.main import app

# Mock data para cliente_a
empresas_cliente_a = [
    {
        "id_empresa": "empresa1_a",
        "nome_empresa": "Empresa Alpha",
        "client_id": "cliente_a",
    },
    {
        "id_empresa": "empresa2_a",
        "nome_empresa": "Empresa Beta",
        "client_id": "cliente_a",
    },
]
df_empresas_a = pd.DataFrame(empresas_cliente_a)

# Mock data para cliente_b
empresas_cliente_b = [
    {
        "id_empresa": "empresa1_b",
        "nome_empresa": "Empresa Gamma",
        "client_id": "cliente_b",
    }
]
df_empresas_b = pd.DataFrame(empresas_cliente_b)

# from src.utils.config_manager import get_current_config
import builtins
import json

import pytest
from fastapi.testclient import TestClient

from services.api.main import app


@pytest.fixture
def client(mocker):
    original_builtins_open = builtins.open
    original_json_load = json.load
    mocker.patch("builtins.open", new=original_builtins_open)
    mocker.patch("json.load", new=original_json_load)
    # original_config_dependency_override = app.dependency_overrides.pop(get_current_config, None)
    try:
        with TestClient(app) as c:
            yield c
    finally:
        pass  # Removido manipulação de dependency_overrides para get_current_config


from unittest.mock import MagicMock, patch

# --- Testes parametrizados de isolamento multi-cliente para empresas, dashboard e auditorias ---
import pytest


@pytest.mark.parametrize(
    "endpoint, key, mock_data_a, mock_data_b, id_field",
    [
        (
            "/api/v1/empresas/",
            "data",
            empresas_cliente_a,
            empresas_cliente_b,
            "id_empresa",
        ),
        (
            "/api/v1/dashboard/",
            "items",
            [{"id_dashboard": "dash1", "client_id": "cliente_a"}],
            [{"id_dashboard": "dash2", "client_id": "cliente_b"}],
            "id_dashboard",
        ),
        (
            "/api/v1/auditorias/",
            "items",
            [{"id_folha": "folha1", "client_id": "cliente_a"}],
            [{"id_folha": "folha2", "client_id": "cliente_b"}],
            "id_folha",
        ),
    ],
)
def test_isolamento_multi_cliente(
    client, endpoint, key, mock_data_a, mock_data_b, id_field
):
    with patch(
        f'src.routes.{endpoint.split("/")[3]}_routes.get_loader_{endpoint.split("/")[3]}',
        MagicMock(),
    ) as mock_loader:
        mock_loader.return_value.listar_todas_as_empresas.return_value = pd.DataFrame(
            mock_data_a
        )
        headers_a = {"x-client-id": "cliente_a"}
        resp_a = client.get(endpoint, headers=headers_a)
        assert resp_a.status_code == 200
        for item in resp_a.json().get(key, []):
            assert item["client_id"] == "cliente_a"
        mock_loader.return_value.listar_todas_as_empresas.return_value = pd.DataFrame(
            mock_data_b
        )
        headers_b = {"x-client-id": "cliente_b"}
        resp_b = client.get(endpoint, headers=headers_b)
        assert resp_b.status_code == 200
        for item in resp_b.json().get(key, []):
            assert item["client_id"] == "cliente_b"
    headers_a = {"x-client-id": "cliente_a"}
    resp_a = client.get("/api/v1/dashboard/", headers=headers_a)
    assert resp_a.status_code == 200
    for item in resp_a.json().get("items", []):
        assert item["client_id"] == "cliente_a"
    resp_b = client.get("/api/v1/dashboard/", headers=headers_b)
    assert resp_b.status_code == 200
    for item in resp_b.json().get("items", []):
        assert item["client_id"] == "cliente_b"
