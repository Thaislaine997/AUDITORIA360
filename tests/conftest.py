# filepath: c:\Users\55479\Documents\AUDITORIA360\tests\conftest.py
import pytest
from fastapi.testclient import TestClient
from typing import Generator, Dict, Any

# Importe a instância 'app' e as dependências originais
from src.main import app
from src.config_manager import get_current_config
from src.bq_loader import get_bigquery_client
from google.cloud import bigquery # Para o mock

# --- Suas funções de Mock (mock_get_current_config, MockBigQueryClient, mock_get_bigquery_client) ---
# --- Coloque as definições delas aqui, como você fez em test_main.py ---
def mock_get_current_config() -> Dict[str, Any]:
    # ... (sua implementação do mock) ...
    return {
        "gcp_project_id": "test-project-id",
        "control_bq_dataset_id": "test_dataset_id",
        # ... etc ...
    }

class MockBigQueryClient:
    # ... (sua implementação do mock) ...
    def __init__(self, project=None, credentials=None):
        self.project = project
    def query(self, query_string: str, job_config=None):
        class MockQueryJob:
            def __init__(self, data): self._data = data; self._result_iterable = iter(self._data)
            def result(self, timeout=None): return self._result_iterable
            def __iter__(self): return iter(self._data)
        if "vw_contabilidades_options" in query_string:
            return MockQueryJob([
                bigquery.Row(("c1", "Cont Test 1"), {"id": 0, "nome": 1}),
            ])
        return MockQueryJob([])

def mock_get_bigquery_client() -> MockBigQueryClient:
    return MockBigQueryClient(project="test-project-id-from-mock-bq")
# --- Fim das funções de Mock ---

@pytest.fixture(scope="session", autouse=True)
def apply_global_dependency_overrides():
    """Aplica overrides de dependência globalmente para a sessão de teste."""
    app.dependency_overrides[get_current_config] = mock_get_current_config
    app.dependency_overrides[get_bigquery_client] = mock_get_bigquery_client
    yield
    # Limpar overrides após a sessão, se necessário, embora para testes geralmente não seja
    app.dependency_overrides = {}


@pytest.fixture
def client(apply_global_dependency_overrides: None) -> Generator[TestClient, Any, None]:
    """Um cliente de teste para a aplicação FastAPI com dependências sobrescritas."""
    # apply_global_dependency_overrides garante que os overrides foram aplicados
    with TestClient(app) as c:
        yield c