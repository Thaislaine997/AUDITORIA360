"""
Tests for the refactored BigQuery modules
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

from src.bigquery.client import BigQueryClient, get_bigquery_client
from src.bigquery.schema import SchemaManager
from src.bigquery.operations import DataOperations
from src.bigquery.loaders import ControleFolhaLoader, BaseLoader


class TestBigQueryClient:
    """Test BigQuery client functionality"""
    
    @patch('src.bigquery.client.bigquery.Client')
    def test_create_client_with_config(self, mock_client_class):
        """Test creating client with configuration"""
        mock_client = Mock()
        mock_client.project = "test-project"
        mock_client_class.return_value = mock_client
        
        config = {"GCP_PROJECT_ID": "test-project"}
        bq_client = BigQueryClient(config)
        
        assert bq_client.client == mock_client
        assert bq_client.project_id == "test-project"
    
    @patch('src.bigquery.client.bigquery.Client')
    def test_test_connection(self, mock_client_class):
        """Test connection testing functionality"""
        mock_client = Mock()
        mock_client.project = "test-project"
        
        # Mock query result
        mock_job = Mock()
        mock_result = [Mock()]
        mock_result[0].test = 1
        mock_job.result.return_value = mock_result
        mock_client.query.return_value = mock_job
        
        mock_client_class.return_value = mock_client
        
        bq_client = BigQueryClient()
        assert bq_client.test_connection() is True
    
    def test_legacy_get_bigquery_client(self):
        """Test backward compatibility function"""
        with patch('src.bigquery.client.BigQueryClient') as mock_bq_client:
            mock_instance = Mock()
            mock_client = Mock()
            mock_instance.client = mock_client
            mock_bq_client.return_value = mock_instance
            
            config = {"GCP_PROJECT_ID": "test-project"}
            result = get_bigquery_client(config)
            
            assert result == mock_client
            mock_bq_client.assert_called_once_with(config)


class TestSchemaManager:
    """Test schema management functionality"""
    
    def test_get_controle_folha_schema(self):
        """Test getting controle folha schema"""
        mock_client = Mock()
        schema_manager = SchemaManager(mock_client)
        
        schema = schema_manager.get_controle_folha_schema()
        
        assert len(schema) > 0
        # Check for required fields
        field_names = [field.name for field in schema]
        assert "id" in field_names
        assert "cnpj" in field_names
        assert "empresa_id" in field_names
    
    @patch('src.bigquery.schema.logger')
    def test_create_dataset_if_not_exists_already_exists(self, mock_logger):
        """Test dataset creation when it already exists"""
        mock_client = Mock()
        mock_client.project = "test-project"
        mock_client.get_dataset.return_value = Mock()  # Dataset exists
        
        schema_manager = SchemaManager(mock_client)
        result = schema_manager.create_dataset_if_not_exists("test_dataset")
        
        assert result is True
        mock_client.get_dataset.assert_called_once()
    
    @patch('src.bigquery.schema.logger')
    def test_create_dataset_if_not_exists_creates_new(self, mock_logger):
        """Test dataset creation when it doesn't exist"""
        mock_client = Mock()
        mock_client.project = "test-project"
        mock_client.get_dataset.side_effect = Exception("Not found")  # Dataset doesn't exist
        mock_client.create_dataset.return_value = Mock()  # Successfully created
        
        schema_manager = SchemaManager(mock_client)
        result = schema_manager.create_dataset_if_not_exists("test_dataset")
        
        assert result is True
        mock_client.create_dataset.assert_called_once()


class TestDataOperations:
    """Test data operations functionality"""
    
    def test_insert_rows_success(self):
        """Test successful row insertion"""
        mock_client = Mock()
        mock_client.project = "test-project"
        mock_table = Mock()
        mock_client.get_table.return_value = mock_table
        mock_client.insert_rows_json.return_value = []  # No errors
        
        operations = DataOperations(mock_client)
        
        rows = [{"id": "1", "name": "Test"}]
        result = operations.insert_rows("dataset", "table", rows)
        
        assert result is True
        mock_client.insert_rows_json.assert_called_once()
    
    def test_insert_rows_with_errors(self):
        """Test row insertion with errors"""
        mock_client = Mock()
        mock_client.project = "test-project"
        mock_table = Mock()
        mock_client.get_table.return_value = mock_table
        mock_client.insert_rows_json.return_value = [{"error": "test error"}]  # Errors
        
        operations = DataOperations(mock_client)
        
        rows = [{"id": "1", "name": "Test"}]
        result = operations.insert_rows("dataset", "table", rows)
        
        assert result is False
    
    def test_query_data(self):
        """Test data querying"""
        mock_client = Mock()
        mock_job = Mock()
        mock_result = [Mock()]
        mock_result[0].__dict__ = {"id": "1", "name": "Test"}
        
        # Mock the result iteration
        def mock_iter():
            for row in mock_result:
                yield row
        mock_job.result.return_value = mock_iter()
        mock_client.query.return_value = mock_job
        
        operations = DataOperations(mock_client)
        
        with patch('builtins.dict', side_effect=lambda x: {"id": "1", "name": "Test"}):
            result = operations.query_data("SELECT * FROM table")
        
        assert result is not None
        assert len(result) == 1


class TestControleFolhaLoader:
    """Test ControleFolhaLoader functionality"""
    
    @patch('src.bigquery.loaders.BigQueryClient')
    @patch('src.bigquery.loaders.SchemaManager')
    @patch('src.bigquery.loaders.DataOperations')
    def test_initialization(self, mock_operations, mock_schema, mock_client_class):
        """Test loader initialization"""
        mock_client = Mock()
        mock_client.client = Mock()
        mock_client_class.return_value = mock_client
        
        config = {"dataset_id": "test_dataset"}
        loader = ControleFolhaLoader(config)
        
        assert loader.config == config
        assert loader.dataset_id == "test_dataset"
        assert loader.table_id == "controle_folha"
    
    @patch('src.bigquery.loaders.BigQueryClient')
    @patch('src.bigquery.loaders.SchemaManager')
    @patch('src.bigquery.loaders.DataOperations')
    def test_inserir_folha(self, mock_operations, mock_schema, mock_client_class):
        """Test payroll insertion"""
        # Setup mocks
        mock_client = Mock()
        mock_client.client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_schema_instance = Mock()
        mock_schema.return_value = mock_schema_instance
        mock_schema_instance.create_dataset_if_not_exists.return_value = True
        mock_schema_instance.create_table_if_not_exists.return_value = True
        
        mock_operations_instance = Mock()
        mock_operations.return_value = mock_operations_instance
        mock_operations_instance.insert_rows.return_value = True
        
        config = {"dataset_id": "test_dataset"}
        loader = ControleFolhaLoader(config)
        
        # Test data insertion
        result = loader.inserir_folha(
            cnpj="12345678000199",
            nome_empresa="Test Company",
            mes_referencia=1,
            ano_referencia=2024,
            qtd_funcionarios=10,
            total_proventos=50000.0,
            total_descontos=10000.0,
            total_liquido=40000.0
        )
        
        assert result is not None  # Should return a UUID
        mock_operations_instance.insert_rows.assert_called_once()
    
    @patch('src.bigquery.loaders.BigQueryClient')
    @patch('src.bigquery.loaders.SchemaManager')
    @patch('src.bigquery.loaders.DataOperations')
    def test_listar_todas_as_empresas(self, mock_operations, mock_schema, mock_client_class):
        """Test listing all companies"""
        # Setup mocks
        mock_client = Mock()
        mock_client.client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_operations_instance = Mock()
        mock_operations.return_value = mock_operations_instance
        mock_operations_instance.query_data.return_value = [
            {"cnpj": "12345678000199", "nome_empresa": "Test Company", "empresa_id": "test"}
        ]
        
        config = {"dataset_id": "test_dataset"}
        loader = ControleFolhaLoader(config)
        
        result = loader.listar_todas_as_empresas()
        
        assert len(result) == 1
        assert result[0]["cnpj"] == "12345678000199"
        mock_operations_instance.query_data.assert_called_once()


class TestBackwardCompatibility:
    """Test backward compatibility with original module"""
    
    @patch('services.ingestion.bq_loader.BigQueryClient')
    def test_import_compatibility(self, mock_client_class):
        """Test that all imports work from the original module"""
        from services.ingestion.bq_loader import (
            get_bigquery_client,
            ControleFolhaLoader,
            ensure_dataset_exists,
            ensure_table_exists_or_updated
        )
        
        # Test that imports work
        assert get_bigquery_client is not None
        assert ControleFolhaLoader is not None
        assert ensure_dataset_exists is not None
        assert ensure_table_exists_or_updated is not None
    
    @patch('services.ingestion.bq_loader.SchemaManager')
    def test_ensure_dataset_exists_legacy(self, mock_schema_manager):
        """Test legacy ensure_dataset_exists function"""
        from services.ingestion.bq_loader import ensure_dataset_exists
        
        mock_client = Mock()
        mock_manager = Mock()
        mock_manager.create_dataset_if_not_exists.return_value = True
        mock_schema_manager.return_value = mock_manager
        
        result = ensure_dataset_exists(mock_client, "test_dataset")
        
        assert result is True
        mock_schema_manager.assert_called_once_with(mock_client)
        mock_manager.create_dataset_if_not_exists.assert_called_once_with("test_dataset", "US")


# Integration test for the complete system
def test_bigquery_system_integration():
    """Test the complete BigQuery system integration"""
    with patch('src.bigquery.client.bigquery.Client') as mock_client_class:
        mock_client = Mock()
        mock_client.project = "test-project"
        mock_client_class.return_value = mock_client
        
        # Test client creation
        config = {"GCP_PROJECT_ID": "test-project"}
        bq_client = BigQueryClient(config)
        assert bq_client.project_id == "test-project"
        
        # Test schema manager
        schema_manager = SchemaManager(bq_client.client)
        schema = schema_manager.get_controle_folha_schema()
        assert len(schema) > 0
        
        # Test data operations
        operations = DataOperations(bq_client.client)
        assert operations.client == bq_client.client