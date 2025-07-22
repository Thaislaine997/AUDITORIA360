"""
Improved test configuration for AUDITORIA360.
Handles missing dependencies and credentials gracefully.
"""
import pytest
import os
import sys
from unittest.mock import MagicMock, patch, Mock
import warnings

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Mock Google Cloud credentials for tests
@pytest.fixture(scope="session", autouse=True)
def mock_gcp_credentials():
    """Mock Google Cloud credentials to prevent authentication errors in tests."""
    with patch.dict(os.environ, {
        'GOOGLE_APPLICATION_CREDENTIALS': '/tmp/fake-credentials.json',
        'GOOGLE_CLOUD_PROJECT': 'test-project',
        'GCP_PROJECT_ID': 'test-project'
    }):
        yield

# Mock Google Cloud clients
@pytest.fixture(scope="session", autouse=True)
def mock_gcp_clients():
    """Mock Google Cloud client libraries."""
    
    # Mock BigQuery client
    mock_bq_client = MagicMock()
    mock_bq_client.query.return_value = MagicMock()
    
    # Mock Document AI client
    mock_docai_client = MagicMock()
    
    # Mock Storage client
    mock_storage_client = MagicMock()
    
    # Mock AI Platform client
    mock_aiplatform_client = MagicMock()
    
    with patch.dict(sys.modules, {
        'google.cloud.bigquery': MagicMock(Client=MagicMock(return_value=mock_bq_client)),
        'google.cloud.documentai': MagicMock(DocumentProcessorServiceClient=MagicMock(return_value=mock_docai_client)),
        'google.cloud.storage': MagicMock(Client=MagicMock(return_value=mock_storage_client)),
        'google.cloud.aiplatform': MagicMock(init=MagicMock()),
        'google.auth': MagicMock(default=MagicMock(return_value=(MagicMock(), None))),
        'google.auth.exceptions': MagicMock(),
    }):
        yield

# Mock external dependencies that might not be available
@pytest.fixture(scope="session", autouse=True)
def mock_external_dependencies():
    """Mock external dependencies to improve test reliability."""
    
    # Mock Streamlit
    mock_st = MagicMock()
    mock_st.session_state = {}
    mock_st.secrets = {}
    
    # Mock TensorFlow/ML libraries
    mock_tf = MagicMock()
    mock_sklearn = MagicMock()
    
    with patch.dict(sys.modules, {
        'streamlit': mock_st,
        'tensorflow': mock_tf,
        'sklearn': mock_sklearn,
        'streamlit_authenticator': MagicMock(),
        'functions_framework': MagicMock(),
    }):
        yield

# Suppress warnings for cleaner test output
@pytest.fixture(scope="session", autouse=True)
def suppress_warnings():
    """Suppress common warnings during testing."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", message=".*defaulting to user installation.*")

# Test data fixtures
@pytest.fixture
def sample_pdf_data():
    """Sample PDF data for testing."""
    return {
        'filename': 'test_folha.pdf',
        'bucket': 'test-bucket',
        'content': b'fake pdf content'
    }

@pytest.fixture
def sample_extraction_data():
    """Sample document extraction data for testing."""
    return [
        {
            'id_item': 'item_001',
            'tipo_campo': 'nome_funcionario',
            'texto_extraido': 'João Silva',
            'valor_limpo': 'João Silva',
            'confianca': 0.95,
            'pagina': 1
        },
        {
            'id_item': 'item_002',
            'tipo_campo': 'salario_base',
            'texto_extraido': 'R$ 5.000,00',
            'valor_limpo': '5000.00',
            'valor_numerico': 5000.0,
            'confianca': 0.98,
            'pagina': 1
        }
    ]

@pytest.fixture
def mock_config():
    """Mock configuration for tests."""
    return {
        'gcp_project_id': 'test-project',
        'gcp_location': 'us',
        'docai_processor_id': 'test-processor',
        'gcs_input_bucket': 'test-input-bucket',
        'bq_dataset_id': 'test_dataset',
        'bq_table_id': 'test_table',
        'log_level': 'INFO'
    }

# Helper function to check if module can be imported
def can_import(module_name):
    """Check if a module can be imported without raising an exception."""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

# Skip tests based on missing dependencies
pytest_plugins = []

# Add custom markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (may require external services)"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test (isolated, fast)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running test"
    )
    config.addinivalue_line(
        "markers", "requires_gcp: mark test as requiring Google Cloud Platform access"
    )

def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their content."""
    for item in items:
        # Mark tests that import Google Cloud modules
        if any(keyword in str(item.fspath) for keyword in ['gcp', 'bigquery', 'docai', 'storage']):
            item.add_marker(pytest.mark.requires_gcp)
        
        # Mark integration tests
        if 'integration' in str(item.fspath) or 'e2e' in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        else:
            item.add_marker(pytest.mark.unit)