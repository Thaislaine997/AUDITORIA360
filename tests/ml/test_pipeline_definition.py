from unittest.mock import MagicMock, patch

import pytest


# Exemplo de teste para pipeline_definition (ajuste o import conforme seu projeto)
def test_pipeline_definition_import():
    try:
        from services.ml import pipeline_definition
    except ImportError:
        pytest.skip("pipeline_definition não implementado ainda")
    assert True
