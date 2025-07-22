import pytest
from unittest.mock import patch

# Exemplo de teste para docai_utils (ajuste o import conforme seu projeto)
@patch('services.ingestion.docai_utils.DocumentProcessorServiceClient')
def test_docai_process_document(mock_docai_client):
    mock_instance = mock_docai_client.return_value
    mock_instance.process_document.return_value = {'entities': []}
    from services.ingestion import docai_utils
    result = docai_utils.process_document('fake_path')
    assert 'entities' in result
