import pytest
from playwright.sync_api import sync_playwright
import os

CLIENTES = [
    {"usuario": os.getenv("E2E_USER1", "cliente1"), "senha": os.getenv("E2E_PASS1", "senha1"), "branding": "Cliente 1"},
    {"usuario": os.getenv("E2E_USER2", "cliente2"), "senha": os.getenv("E2E_PASS2", "senha2"), "branding": "Cliente 2"},
]

@pytest.mark.usefixtures("streamlit_server")
@pytest.mark.parametrize("cliente", CLIENTES)
def test_login_isolamento(cliente, streamlit_server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(os.getenv("E2E_URL", "http://localhost:8501"), timeout=60000) # Aumentar timeout do goto
        page.wait_for_load_state("networkidle", timeout=30000) # Esperar a rede ficar ociosa

        # Tentativa de localizar campos de forma mais genérica, comum com streamlit-authenticator
        # Os seletores podem precisar de ajuste fino dependendo da renderização exata.
        
        # Localiza o campo de usuário pelo texto do rótulo (ou um placeholder se disponível)
        # O streamlit-authenticator pode não usar o atributo 'name' de forma consistente.
        # Este é um seletor mais robusto que procura um input precedido por um texto "Username"
        # ou um input com placeholder "Username"
        page.wait_for_selector('//label[contains(text(), "Username")]/following-sibling::input | //input[@placeholder="Username"] | input[aria-label="Username"]', timeout=30000)
        page.fill('//label[contains(text(), "Username")]/following-sibling::input | //input[@placeholder="Username"] | input[aria-label="Username"]', cliente["usuario"], timeout=10000)
        
        page.wait_for_selector('//label[contains(text(), "Password")]/following-sibling::input | //input[@placeholder="Password"] | input[aria-label="Password"]', timeout=10000)
        page.fill('//label[contains(text(), "Password")]/following-sibling::input | //input[@placeholder="Password"] | input[aria-label="Password"]', cliente["senha"], timeout=10000)
        
        # O botão de login do streamlit-authenticator geralmente tem o texto "Login"
        page.wait_for_selector('button:has-text("Login")', timeout=10000)
        page.click('button:has-text("Login")')
        
        # Esperar pelo seletor com um timeout maior
        page.wait_for_selector(f'text={cliente["branding"]}', timeout=20000) # 20 segundos
        
        assert cliente["branding"] in page.content()
        browser.close()

@pytest.mark.usefixtures("streamlit_server")
def test_exportacao_csv(streamlit_server):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(os.getenv("E2E_URL", "http://localhost:8501"))
        # Faça login e navegue até a tela de exportação
        # page.fill(...)
        # page.click(...)
        # page.click('button#exportar-csv')
        # Adapte o seletor conforme o botão real
        # Exemplo de validação de download:
        # with page.expect_download() as download_info:
        #     page.click('button#exportar-csv')
        # download = download_info.value
        # assert download.suggested_filename.endswith('.csv')
        browser.close()
