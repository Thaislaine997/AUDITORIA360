# tests/test_cct_list.py
import pytest
from fastapi.testclient import TestClient
from services.api.main import app

client = TestClient(app)

@pytest.mark.parametrize(
    "mock_return,params,expected_len,expected_status,expected_first_id",
    [
        ([], {}, 0, 200, None),
        ([{
            "id_cct_documento": "uuid-123",
            "nome_documento_original": "CCT Metalúrgicos 2025",
            "gcs_uri_documento": "gs://bucket/cct1.pdf",
            "data_inicio_vigencia_cct": "2025-01-01",
            "data_fim_vigencia_cct": "2025-12-31",
            "sindicatos_laborais": None,
            "sindicatos_patronais": None,
            "status_processamento_ia": "PENDENTE_EXTRACAO"
        }], {}, 1, 200, "uuid-123"),
        ( [
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
        ], {}, 2, 200, "uuid-1"),
    ]
)
def test_listar_ccts_parametrizado(monkeypatch, mock_return, params, expected_len, expected_status, expected_first_id):
    async def mock_listar_ccts(id_cliente_afetado=None, sindicato_nome_contem=None, data_vigencia_em=None):
        return mock_return
    monkeypatch.setattr("src.controllers.cct_controller.listar_ccts", mock_listar_ccts)
    response = client.get("/api/v1/ccts", params=params)
    assert response.status_code == expected_status
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == expected_len
    if expected_first_id:
        assert data[0]["id_cct_documento"] == expected_first_id


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
        pytest.fail("Não deveria chamar controller com data inválida")
    monkeypatch.setattr("src.controllers.cct_controller.listar_ccts", mock_listar_ccts)
    response = client.get("/api/v1/ccts", params={"data_vigencia_em": "data-invalida"})
    assert response.status_code == 422
