# tests/test_cct_list.py
import pytest
from fastapi.testclient import TestClient
from src.main import app
import json

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_listar_ccts(monkeypatch):
    # Mocka a função listar_ccts para retornar dados de teste
    async def fake_listar_ccts(
        id_cliente_afetado=None,
        sindicato_nome_contem=None,
        data_vigencia_em=None
    ):
        return [
            {
                "id_cct_documento": "uuid-1",
                "nome_documento_original": "CCT Exemplo 1",
                "gcs_uri_documento": "gs://bucket/doc1.pdf",
                "data_inicio_vigencia_cct": "2025-01-01",
                "data_fim_vigencia_cct": None,
                "sindicatos_laborais": None,
                "sindicatos_patronais": None,
                "status_processamento_ia": "PENDENTE_EXTRACAO"
            },
            {
                "id_cct_documento": "uuid-2",
                "nome_documento_original": "CCT Exemplo 2",
                "gcs_uri_documento": "gs://bucket/doc2.pdf",
                "data_inicio_vigencia_cct": "2024-05-01",
                "data_fim_vigencia_cct": "2024-12-31",
                "sindicatos_laborais": None,
                "sindicatos_patronais": None,
                "status_processamento_ia": "ANALISE_CONCLUIDA_SUCESSO"
            }
        ]
    from src.controllers.cct_controller import listar_ccts
    monkeypatch.setattr('src.controllers.cct_controller.listar_ccts', fake_listar_ccts)
    yield

def test_get_ccts_no_filters():
    response = client.get("/api/v1/ccts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_get_ccts_with_filters():
    params = {"id_cliente_afetado": "cliente1"}
    response = client.get("/api/v1/ccts", params=params)
    assert response.status_code == 200
    data = response.json()
    assert all(item["status_processamento_ia"] for item in data)
