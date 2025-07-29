"""
Integration tests for etl_elt.py script
Tests the ETL/ELT data processing functionality and system integration
"""
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add scripts path to system path
scripts_path = Path(__file__).parent.parent.parent / "scripts" / "python"
sys.path.insert(0, str(scripts_path))

try:
    from etl_elt import (
        anonimizar_dados,
        carregar_dataset_treinamento,
        extrair_dados_folha,
        get_bigquery_client,
        main as etl_main,
        transformar_features,
    )
    ETL_AVAILABLE = True
except ImportError as e:
    ETL_AVAILABLE = False
    pytest.skip(f"etl_elt module not available: {e}", allow_module_level=True)


class TestETLScriptIntegration:
    """Integration tests for ETL/ELT script"""

    @pytest.fixture
    def mock_dataframe(self):
        """Create a mock pandas DataFrame for testing"""
        try:
            import pandas as pd
            return pd.DataFrame({
                'cpf_funcionario': ['12345678901', '23456789012'],
                'nome_funcionario': ['João Silva', 'Maria Santos'],
                'total_proventos': [5000.0, 6000.0],
                'total_descontos': [1500.0, 1800.0],
                'salario_base': [4000.0, 5000.0]
            })
        except ImportError:
            # If pandas is not available, create a mock-like object
            class MockDataFrame:
                def __init__(self, data):
                    self.data = data
                    self.columns = list(data.keys())
                
                def __getitem__(self, key):
                    return self.data[key]
                
                def __setitem__(self, key, value):
                    self.data[key] = value
                
                def apply(self, func):
                    return [func(x) for x in self.data[self.columns[0]]]
                
                def drop(self, columns):
                    new_data = {k: v for k, v in self.data.items() if k not in columns}
                    return MockDataFrame(new_data)
                
                def __len__(self):
                    return len(list(self.data.values())[0])
            
            return MockDataFrame({
                'cpf_funcionario': ['12345678901', '23456789012'],
                'nome_funcionario': ['João Silva', 'Maria Santos'],
                'total_proventos': [5000.0, 6000.0],
                'total_descontos': [1500.0, 1800.0],
                'salario_base': [4000.0, 5000.0]
            })

    @pytest.fixture
    def mock_bigquery_client(self):
        """Create a mock BigQuery client for testing"""
        client = MagicMock()
        
        # Mock query method to return a mock result
        mock_result = MagicMock()
        mock_result.to_dataframe.return_value = self.mock_dataframe()
        client.query.return_value = mock_result
        
        # Mock load_table_from_dataframe
        mock_job = MagicMock()
        mock_job.result.return_value = None
        client.load_table_from_dataframe.return_value = mock_job
        
        return client

    def test_get_bigquery_client_without_credentials(self):
        """Test BigQuery client creation without service account credentials"""
        with patch.dict(os.environ, {}, clear=True):
            with patch('etl_elt.bigquery.Client') as mock_client:
                get_bigquery_client()
                mock_client.assert_called_once_with(project=None)  # PROJECT_ID would be None without env

    def test_get_bigquery_client_with_credentials(self):
        """Test BigQuery client creation with service account credentials"""
        test_key_path = "/path/to/service_account.json"
        with patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': test_key_path}):
            with patch('etl_elt.service_account.Credentials.from_service_account_file') as mock_creds:
                with patch('etl_elt.bigquery.Client') as mock_client:
                    mock_credentials = MagicMock()
                    mock_creds.return_value = mock_credentials
                    
                    get_bigquery_client()
                    
                    mock_creds.assert_called_once_with(test_key_path)
                    mock_client.assert_called_once_with(
                        credentials=mock_credentials, 
                        project=None  # PROJECT_ID would be None without env
                    )

    def test_extrair_dados_folha(self, mock_bigquery_client):
        """Test data extraction from payroll table"""
        with patch('etl_elt.get_bigquery_client', return_value=mock_bigquery_client):
            result = extrair_dados_folha(mock_bigquery_client)
            
            # Verify that query was called
            mock_bigquery_client.query.assert_called_once()
            
            # Verify SQL query structure
            query_call = mock_bigquery_client.query.call_args[0][0]
            assert 'SELECT * FROM' in query_call
            assert 'Tabela_Folha_Pagamento' in query_call

    def test_transformar_features(self, mock_dataframe):
        """Test feature transformation functionality"""
        result = transformar_features(mock_dataframe)
        
        # Check that new features were added
        if hasattr(result, 'data'):  # MockDataFrame
            assert 'proporcao_descontos' in result.data
            assert 'flag_inconsistencia' in result.data
        else:  # Real pandas DataFrame
            assert 'proporcao_descontos' in result.columns
            assert 'flag_inconsistencia' in result.columns
            
            # Verify calculations
            expected_prop = [1500.0/5000.0, 1800.0/6000.0]  # descontos/proventos
            assert all(abs(a - b) < 0.001 for a, b in 
                      zip(result['proporcao_descontos'].tolist(), expected_prop))

    def test_anonimizar_dados(self, mock_dataframe):
        """Test data anonymization functionality"""
        result = anonimizar_dados(mock_dataframe)
        
        # Check sensitive data removal
        if hasattr(result, 'data'):  # MockDataFrame
            assert 'nome_funcionario' not in result.data
            assert 'cpf_funcionario' not in result.data
            assert 'cpf_funcionario_hash' in result.data
        else:  # Real pandas DataFrame
            assert 'nome_funcionario' not in result.columns
            assert 'cpf_funcionario' not in result.columns
            assert 'cpf_funcionario_hash' in result.columns

    def test_carregar_dataset_treinamento(self, mock_bigquery_client, mock_dataframe):
        """Test loading training dataset to BigQuery"""
        carregar_dataset_treinamento(mock_bigquery_client, mock_dataframe)
        
        # Verify that load_table_from_dataframe was called
        mock_bigquery_client.load_table_from_dataframe.assert_called_once()
        
        # Verify parameters
        call_args = mock_bigquery_client.load_table_from_dataframe.call_args
        assert call_args[0][0] == mock_dataframe  # DataFrame passed
        # Table name should include the destination table

    def test_etl_environment_variables(self):
        """Test that ETL script respects environment variables"""
        test_project = "test-project-123"
        test_dataset = "test-dataset"
        
        with patch.dict(os.environ, {
            'GCP_PROJECT_ID': test_project,
            'BQ_DATASET_ID': test_dataset
        }):
            # Import module again to get updated environment variables
            import importlib
            import etl_elt
            importlib.reload(etl_elt)
            
            # PROJECT_ID and DATASET_ID should be updated
            assert etl_elt.PROJECT_ID == test_project
            assert etl_elt.DATASET_ID == test_dataset

    @patch('etl_elt.get_bigquery_client')
    @patch('etl_elt.extrair_dados_folha')
    @patch('etl_elt.transformar_features')
    @patch('etl_elt.anonimizar_dados')
    @patch('etl_elt.carregar_dataset_treinamento')
    def test_etl_main_integration(self, mock_carregar, mock_anonimizar, 
                                  mock_transformar, mock_extrair, mock_get_client,
                                  mock_dataframe):
        """Test the main ETL workflow integration"""
        # Setup mocks
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_extrair.return_value = mock_dataframe
        mock_transformar.return_value = mock_dataframe
        mock_anonimizar.return_value = mock_dataframe
        
        # Run main ETL process
        etl_main()
        
        # Verify the complete workflow was executed
        mock_get_client.assert_called_once()
        mock_extrair.assert_called_once_with(mock_client)
        mock_transformar.assert_called_once_with(mock_dataframe)
        mock_anonimizar.assert_called_once_with(mock_dataframe)
        mock_carregar.assert_called_once_with(mock_client, mock_dataframe)

    def test_etl_error_handling(self):
        """Test ETL error handling scenarios"""
        with patch('etl_elt.get_bigquery_client') as mock_get_client:
            mock_get_client.side_effect = Exception("Connection failed")
            
            # The main function should handle exceptions gracefully
            with pytest.raises(Exception) as exc_info:
                etl_main()
            
            assert "Connection failed" in str(exc_info.value)

    def test_etl_table_naming_convention(self):
        """Test that table names follow proper conventions"""
        import etl_elt
        
        # Verify table naming structure
        assert '.Tabela_Folha_Pagamento' in etl_elt.TABELA_FOLHA
        assert '.DatasetTreinamentoRiscosFolha' in etl_elt.TABELA_DESTINO
        
        # Verify project and dataset structure
        assert etl_elt.PROJECT_ID in etl_elt.TABELA_FOLHA
        assert etl_elt.DATASET_ID in etl_elt.TABELA_FOLHA

    def test_etl_logging_configuration(self):
        """Test that ETL script has proper logging configuration"""
        import logging
        import etl_elt
        
        # Verify logging is configured
        logger = logging.getLogger()
        assert logger.level == logging.INFO

    @pytest.mark.parametrize("project_id,dataset_id", [
        ("proj1", "dataset1"),
        ("proj-2", "dataset_2"),
        ("test-project", "test_dataset")
    ])
    def test_etl_configuration_flexibility(self, project_id, dataset_id):
        """Test ETL script with different project and dataset configurations"""
        with patch.dict(os.environ, {
            'GCP_PROJECT_ID': project_id,
            'BQ_DATASET_ID': dataset_id
        }):
            # Import and check configuration
            import importlib
            import etl_elt
            importlib.reload(etl_elt)
            
            assert project_id in etl_elt.TABELA_FOLHA
            assert dataset_id in etl_elt.TABELA_FOLHA
            assert project_id in etl_elt.TABELA_DESTINO
            assert dataset_id in etl_elt.TABELA_DESTINO

    def test_etl_script_structure_and_imports(self):
        """Test that ETL script has the expected structure and imports"""
        assert ETL_AVAILABLE
        
        # Check that all required functions are available
        assert callable(get_bigquery_client)
        assert callable(extrair_dados_folha)
        assert callable(transformar_features)
        assert callable(anonimizar_dados)
        assert callable(carregar_dataset_treinamento)
        assert callable(etl_main)
        
        # Check that main function is properly configured for CLI usage
        import etl_elt
        assert hasattr(etl_elt, '__name__')


if __name__ == "__main__":
    pytest.main([__file__])