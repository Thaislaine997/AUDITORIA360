from unittest.mock import MagicMock, patch


# Exemplo de mock para DocumentAI
@patch("google.cloud.documentai.DocumentProcessorServiceClient")
def test_docai_process_document(mock_docai_client):
    mock_instance = mock_docai_client.return_value
    mock_instance.process_document.return_value = MagicMock(
        entities=[{"type": "CPF", "text": "123.456.789-00"}]
    )
    from services.ingestion import docai_utils

    result = docai_utils.process_document("fake_path")
    assert hasattr(result, "entities")


# Exemplo de mock para BigQuery
@patch("google.cloud.bigquery.Client")
def test_bq_insert_rows_json(mock_bq_client):
    mock_client = mock_bq_client.return_value
    mock_client.insert_rows_json.return_value = []
    from services.ingestion import bq_loader

    result = bq_loader.insert_rows_json("table", [{"a": 1}])
    assert result is True
