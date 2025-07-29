from unittest.mock import MagicMock, patch

import pytest


# Exemplo de teste para bq_loader (ajuste o import conforme seu projeto)
@patch("services.ingestion.bq_loader.bigquery.Client")
def test_insert_rows_json(mock_bq_client):
    mock_client = mock_bq_client.return_value
    mock_client.insert_rows_json.return_value = []
    from services.ingestion import bq_loader

    result = bq_loader.insert_rows_json("table", [{"a": 1}])
    assert result is True
