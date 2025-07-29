import json
from typing import Any, Dict, Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from google.cloud import bigquery  # Para mock do tipo de retorno

# Importar a instância 'app' do FastAPI do local correto
from services.api.main import app  # Sua instância FastAPI
from services.ingestion.bq_loader import get_bigquery_client  # Exemplo de dependência

# Ajustar os imports das dependências conforme necessário
from services.ingestion.config_loader import (  # Função correta para carregar configuração
    load_config,
)


# --- Funções de Mock para as Dependências ---
def mock_get_current_config() -> Dict[str, Any]:
    print("DEBUG: mock_get_current_config foi chamada")
    return {
        "gcp_project_id": "test-project-id",
        "control_bq_dataset_id": "test_dataset_id",
        "empresas_client_id_mapping": {"client_test_1": "empresa_test_1"},
        "default_client_id": "default_test_client",
        "clients": {
            "client_test_1": {
                "AI_PROVIDER": "vertex",
                "LOGO_URL": "http://logo.test/1.png",
            },
            "default_test_client": {
                "AI_PROVIDER": "gemini",
                "LOGO_URL": "http://logo.test/default.png",
            },
        },
    }


class MockBigQueryClient:
    def __init__(self, project=None, credentials=None):
        self.project = project
        print(f"DEBUG: MockBigQueryClient inicializado para projeto: {project}")

    def query(self, query_string: str, job_config=None):
        print(f"DEBUG: MockBigQueryClient.query chamada com: {query_string[:100]}...")

        class MockQueryJob:
            def __init__(self, data):
                self._data = data
                self._result_iterable = iter(self._data)

            def result(self, timeout=None):
                return self._result_iterable

            def __iter__(self):
                return iter(self._data)

        if (
            "FROM `test-project-id.test_dataset_id.vw_contabilidades_options`"
            in query_string
        ):
            return MockQueryJob(
                [
                    bigquery.Row(
                        ("contabilidade_1", "Contabilidade Teste 1"),
                        {"id": 0, "nome": 1},
                    ),
                    bigquery.Row(
                        ("contabilidade_2", "Contabilidade Teste 2"),
                        {"id": 0, "nome": 1},
                    ),
                ]
            )
        return MockQueryJob([])


def mock_get_bigquery_client() -> MockBigQueryClient:
    print("DEBUG: mock_get_bigquery_client foi chamada")
    return MockBigQueryClient(project="test-project-id-from-mock-bq")


# --- Aplicar os Overrides na sua instância 'app' do FastAPI ---
app.dependency_overrides[load_config] = mock_get_current_config
app.dependency_overrides[get_bigquery_client] = mock_get_bigquery_client


# --- Fixture do Pytest para o TestClient ---
@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    """Um cliente de teste para a aplicação FastAPI com dependências sobrescritas."""
    with TestClient(app) as c:
        yield c


# --- Exemplo de um Teste usando a fixture 'client' ---
def test_get_contabilidades_options_com_override(client: TestClient):
    response = client.get("/api/v1/auditorias/options/contabilidades")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 0
    if len(data) > 0:
        assert "id" in data[0]
        assert "nome" in data[0]
    print("DEBUG: Resposta de /options/contabilidades:", data)


def test_health_check(client: TestClient):
    """Testa a rota de health check."""
    response = client.get("/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "healthy"  # Alterado de "ok" para "healthy"


@patch("services.api.main.process_document_ocr")
@patch.dict(
    "os.environ",
    {
        "GCS_INPUT_BUCKET": "meu-bucket-pdf-teste",
        "GCS_CONTROL_BUCKET": "meu-bucket-planilha-teste",
    },
    clear=True,
)
def test_gcs_event_handler_pdf(mock_process_ocr, client: TestClient):
    """Testa o event handler para um evento de PDF."""
    event_data = {
        "message": {
            "attributes": {
                "bucketId": "meu-bucket-pdf-teste",
                "objectId": "documentos/documento_teste.pdf",  # Corrigido: Adicionado prefixo "documentos/"
            },
            "messageId": "12345",
            "publishTime": "2024-05-10T12:00:00Z",
        }
    }
    response = client.post("/event-handler", json=event_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    # A chamada mockada deve refletir o nome completo do objeto como passado
    mock_process_ocr.assert_called_once_with(
        file_name="documentos/documento_teste.pdf", bucket_name="meu-bucket-pdf-teste"
    )


@patch("services.api.main.process_control_sheet")
@patch.dict(
    "os.environ",
    {
        "GCS_INPUT_BUCKET": "outro-bucket-pdf-teste",
        "GCS_CONTROL_BUCKET": "meu-bucket-planilha-teste",
    },
    clear=True,
)
def test_gcs_event_handler_sheet(mock_process_sheet, client: TestClient):
    """Testa o event handler para um evento de planilha."""
    event_data = {
        "message": {
            "attributes": {
                "bucketId": "meu-bucket-planilha-teste",  # Corrigido: de bucket para bucketId
                "objectId": "planilhas-controle/planilha_teste.xlsx",  # Corrigido: de name para objectId e adicionado prefixo
            },
            "messageId": "67890",
            "publishTime": "2024-05-10T12:05:00Z",
        }
    }
    response = client.post("/event-handler", json=event_data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    mock_process_sheet.assert_called_once_with(
        file_name="planilhas-controle/planilha_teste.xlsx",
        bucket_name="meu-bucket-planilha-teste",
    )


def test_gcs_event_handler_no_payload(client: TestClient):
    response = client.post(
        "/event-handler", headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    json_data = response.json()
    assert "detail" in json_data
    assert "Nenhum payload JSON recebido" in json_data["detail"]


def test_gcs_event_handler_invalid_envelope(client: TestClient):
    response = client.post("/event-handler", json={"not_a_message": "data"})
    assert response.status_code == 400
    json_data = response.json()
    assert "detail" in json_data
    assert (
        "Formato de envelope de evento inválido." in json_data["detail"]
    )  # Corrigido: Mensagem de erro atualizada
