# tests/test_cct_listagem.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_listar_ccts_vazio(monkeypatch):
    async def mock_listar_ccts(id_cliente_afetado=None, sindicato_nome_contem=None, data_vigencia_em=None):
        return []
    monkeypatch.setattr("src.controllers.cct_controller.listar_ccts", mock_listar_ccts)
    response = client.get("/api/v1/ccts")
    assert response.status_code == 200
    assert response.json() == []

def test_listar_ccts_com_resultado(monkeypatch):
    async def mock_listar_ccts(id_cliente_afetado=None, sindicato_nome_contem=None, data_vigencia_em=None):
        return [
            {
                "id_cct_documento": "uuid-123",
                "nome_documento_original": "CCT Metalúrgicos 2025",
                "gcs_uri_documento": "gs://bucket/cct1.pdf",
                "data_inicio_vigencia_cct": "2025-01-01",
                "data_fim_vigencia_cct": "2025-12-31",
                "sindicatos_laborais": None,
                "sindicatos_patronais": None,
                "status_processamento_ia": "PENDENTE_EXTRACAO"
            }
        ]
    monkeypatch.setattr("src.controllers.cct_controller.listar_ccts", mock_listar_ccts)
    response = client.get("/api/v1/ccts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["id_cct_documento"] == "uuid-123"
    assert data[0]["nome_documento_original"] == "CCT Metalúrgicos 2025"

def test_listar_ccts_filtro_cliente(monkeypatch):
    async def mock_listar_ccts(id_cliente_afetado=None, sindicato_nome_contem=None, data_vigencia_em=None):
        assert id_cliente_afetado == "123"
        return []
    monkeypatch.setattr("src.controllers.cct_controller.listar_ccts", mock_listar_ccts)
    response = client.get("/api/v1/ccts", params={"id_cliente_afetado": "123"})
    assert response.status_code == 200
    assert response.json() == []

def test_listar_ccts_filtro_sindicato(monkeypatch):
    async def mock_listar_ccts(id_cliente_afetado=None, sindicato_nome_contem=None, data_vigencia_em=None):
        assert sindicato_nome_contem == "metal"
        return []
    monkeypatch.setattr("src.controllers.cct_controller.listar_ccts", mock_listar_ccts)
    response = client.get("/api/v1/ccts", params={"sindicato_nome_contem": "metal"})
    assert response.status_code == 200
    assert response.json() == []

def test_listar_ccts_filtro_data_invalida(monkeypatch):
    async def mock_listar_ccts(id_cliente_afetado=None, sindicato_nome_contem=None, data_vigencia_em=None):
        # Não deve ser chamado se data inválida
        pytest.fail("Não deveria chamar controller com data inválida")
    monkeypatch.setattr("src.controllers.cct_controller.listar_ccts", mock_listar_ccts)
    response = client.get("/api/v1/ccts", params={"data_vigencia_em": "data-invalida"})
    assert response.status_code == 422
