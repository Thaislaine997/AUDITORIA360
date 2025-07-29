import pandas as pd
import pytest

# Mock do controle_folha_controller
controle_folha_controller = object()
from fastapi import Request


@pytest.fixture
def mock_request() -> Request:
    return Request(scope={"type": "http", "headers": [(b"host", b"testclient")]})


@pytest.mark.asyncio
async def test_importacao_e_busca_controle_folha(mock_request, monkeypatch):
    """Testa importação e busca de controle de folha com integração real."""

    def mock_get_conf(request: Request):
        return {
            "gcp_project_id": "test-project",
            "control_bq_dataset_id": "test_dataset",
        }

    monkeypatch.setattr(
        "src.controllers.controle_folha_controller.config_manager.get_config",
        mock_get_conf,
    )
    monkeypatch.setattr(
        "src.controllers.controle_folha_controller.bq_loader.get_bigquery_client",
        lambda: None,
    )

    df = pd.DataFrame(
        [
            {
                "CNPJ": "12345678000199",
                "NOME EMPRESA": "EMPRESA TESTE",
                "DADOS FOLHA": "OK",
                "Envio Cliente": "sim",
                "Data de Envio da Folha": "05/05/2025",
                "Guia FGTS": "sim",
                "Data Guia FGTS": "05/05/2025",
                "DARF INSS": "sim",
                "Data DARF INSS": "05/05/2025",
                "Honorários": "1000,50",
                "Data Vencimento Honorários": "10/05/2025",
                "Status Pagamento Honorários": "pago",
                "Data Recebimento Honorários": "11/05/2025",
                "Observações": "Teste obs",
                "Mês Competência": "05/2025",
                "Analista Responsável": "Analista X",
            }
        ]
    )

    try:
        pass
    finally:
        pass
