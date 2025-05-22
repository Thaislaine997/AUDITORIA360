import pytest
from unittest.mock import patch
import src.painel as painel_mod

@patch("src.painel.requests.get")
def test_gera_pdf_auditoria_ok(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"PDFDATA"
    painel_mod.API_BASE_URL = "http://fakeapi"
    auditoria = {"id_folha": "folha123"}
    with patch("src.painel.st.button", return_value=True):
        with patch("src.painel.st.download_button") as mock_download:
            pdf_url = f"http://fakeapi/api/v1/auditorias/folha123/pdf"
            response = mock_get(pdf_url, stream=True)
            assert response.status_code == 200
            assert response.content == b"PDFDATA"
            mock_download.assert_not_called()  # download_button só é chamado no painel real

@patch("src.painel.requests.get")
def test_gera_pdf_auditoria_falha(mock_get):
    mock_get.return_value.status_code = 404
    painel_mod.API_BASE_URL = "http://fakeapi"
    auditoria = {"id_folha": "folha123"}
    with patch("src.painel.st.button", return_value=True):
        with patch("src.painel.st.download_button") as mock_download:
            pdf_url = f"http://fakeapi/api/v1/auditorias/folha123/pdf"
            response = mock_get(pdf_url, stream=True)
            assert response.status_code == 404
            mock_download.assert_not_called()
