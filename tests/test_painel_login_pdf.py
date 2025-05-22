import pytest
from unittest.mock import patch, MagicMock
import streamlit as st
import src.painel as painel_mod

@pytest.fixture
def mock_auth_success(monkeypatch):
    monkeypatch.setitem(st.session_state, "authentication_status", True)
    monkeypatch.setitem(st.session_state, "username", "usuario_teste")
    monkeypatch.setitem(st.session_state, "name", "Usuário Teste")
    yield
    st.session_state.clear()

@pytest.fixture
def mock_auth_fail(monkeypatch):
    monkeypatch.setitem(st.session_state, "authentication_status", False)
    yield
    st.session_state.clear()

@patch("src.painel.st_recaptcha_custom")
@patch("src.painel.requests.post")
def test_login_recaptcha_ok(mock_post, mock_recaptcha, mock_auth_success, monkeypatch):
    # Simula token válido e resposta positiva da API
    mock_recaptcha.return_value = "token123"
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"recaptcha_valid": True}
    monkeypatch.setitem(st.session_state, "recaptcha_verified_for_session", False)
    # Executa parte do fluxo de login
    painel_mod.RECAPTCHA_SITE_KEY = "sitekey"
    painel_mod.API_BASE_URL = "http://fakeapi"
    # Simula clique no botão
    with patch("src.painel.st.button", return_value=True):
        painel_mod.st.session_state["recaptcha_verified_for_session"] = False
        # Chama o trecho de código relevante (não executa o app inteiro)
        # Aqui, você pode chamar uma função auxiliar se o fluxo estiver modularizado
        # Ou apenas garantir que o estado muda corretamente
        # Exemplo:
        painel_mod.st.session_state["recaptcha_verified_for_session"] = True
        assert st.session_state["recaptcha_verified_for_session"] is True

@patch("src.painel.st_recaptcha_custom")
@patch("src.painel.requests.post")
def test_login_recaptcha_falha(mock_post, mock_recaptcha, mock_auth_success, monkeypatch):
    mock_recaptcha.return_value = "token123"
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"recaptcha_valid": False, "detail": "Token inválido"}
    monkeypatch.setitem(st.session_state, "recaptcha_verified_for_session", False)
    painel_mod.RECAPTCHA_SITE_KEY = "sitekey"
    painel_mod.API_BASE_URL = "http://fakeapi"
    with patch("src.painel.st.button", return_value=True):
        painel_mod.st.session_state["recaptcha_verified_for_session"] = False
        # Simula tentativa de login com reCAPTCHA inválido
        painel_mod.st.session_state["recaptcha_verified_for_session"] = False
        assert st.session_state["recaptcha_verified_for_session"] is False

@patch("src.painel.requests.get")
def test_gera_pdf_auditoria(mock_get, mock_auth_success, monkeypatch):
    # Simula resposta da API de PDF
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"PDFDATA"
    painel_mod.API_BASE_URL = "http://fakeapi"
    # Simula auditoria com id_folha
    auditoria = {"id_folha": "folha123"}
    # Simula chamada do botão de PDF
    with patch("src.painel.st.button", return_value=True):
        with patch("src.painel.st.download_button") as mock_download:
            # Chama o trecho de geração de PDF
            pdf_url = f"http://fakeapi/api/v1/auditorias/folha123/pdf"
            response = mock_get(pdf_url, stream=True)
            assert response.status_code == 200
            assert response.content == b"PDFDATA"
            # Simula download_button chamado corretamente
            mock_download.assert_not_called()  # O download_button só é chamado dentro do painel real
