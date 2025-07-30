import os

import pytest
from tests.e2e.e2e_config import e2e_context_instance  # Corrigir import path
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

CLIENTES = [
    # Usar os nomes de usuário como definidos no mock_yaml_config_content em conftest.py
    {
        "usuario": "cliente1",
        "senha": "senha1",
        "branding": "Cliente 1 User",
    },  # "branding" deve ser o 'name' do config
    {"usuario": "cliente2", "senha": "senha2", "branding": "Cliente 2 User"},
]


@pytest.mark.usefixtures("streamlit_server")
@pytest.mark.parametrize("cliente", CLIENTES)
def test_login_isolamento(cliente, streamlit_server):
    # Definir o contexto E2E para este teste parametrizado
    e2e_context_instance.username = cliente["usuario"]
    e2e_context_instance.password = cliente["senha"]

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )  # Mantenha headless=True para CI/testes automatizados
        page = browser.new_page()
        try:
            page.goto(os.getenv("E2E_URL", "http://localhost:8501"), timeout=60000)
            page.wait_for_load_state("networkidle", timeout=30000)

            # Os seletores para os campos de texto não são mais necessários, pois o mock de st.text_input
            # usará e2e_context_instance.username e e2e_context_instance.password.
            # O mock de authenticator.login() também usará esses valores.

            # O clique no botão de login ainda é necessário para disparar a lógica de login mockada.
            # O seletor do botão de login pode variar dependendo da implementação do authenticator.
            # Se o authenticator renderiza um formulário com um botão "Login":
            login_button_selector = (
                'button:has-text("Login")'  # Ajuste se o texto/seletor for diferente
            )
            try:
                page.wait_for_selector(
                    login_button_selector, timeout=15000
                )  # Aumentar um pouco se necessário
                page.click(login_button_selector, timeout=5000)
            except PlaywrightTimeoutError:
                print(
                    f"Botão de login não encontrado com seletor: {login_button_selector}"
                )
                # Se o authenticator logar automaticamente ou de outra forma, esta parte pode não ser necessária
                # ou precisar de uma abordagem diferente.
                # Por exemplo, se o login é acionado apenas pela presença de st.session_state mockado,
                # então o clique pode não ser estritamente para submeter um formulário.
                # No entanto, a maioria dos fluxos de UI de login envolve um clique.
                pass  # Continuar para verificar o resultado do login mockado

            # Esperar pelo seletor com o nome do usuário (branding) que deve aparecer após o login mockado.
            # Este nome vem do mock_yaml_config_content['credentials']['usernames'][username]['name']
            branding_selector = f'text={cliente["branding"]}'
            page.wait_for_selector(
                branding_selector, timeout=30000
            )  # Aumentado para 30s

            assert cliente["branding"] in page.content()
            print(
                f"Login bem-sucedido e branding \"{cliente['branding']}\" encontrado para {cliente['usuario']}."
            )

        except PlaywrightTimeoutError as e:
            print(f"Timeout durante o teste E2E para {cliente['usuario']}: {e}")
            # Salvar screenshot e HTML para depuração
            screenshot_path = f"./playwright-screenshot-{cliente['usuario']}.png"
            html_path = f"./playwright-page-{cliente['usuario']}.html"
            try:
                page.screenshot(path=screenshot_path)
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(page.content())
                print(f"Screenshot salvo em: {screenshot_path}")
                print(f"HTML da página salvo em: {html_path}")
            except Exception as ex_save:
                print(f"Erro ao salvar screenshot/HTML: {ex_save}")
            raise  # Re-levanta a exceção original de timeout
        finally:
            browser.close()
            # Limpar o contexto E2E
            e2e_context_instance.username = (
                "test_user_playwright"  # Ou string vazia: ""
            )
            e2e_context_instance.password = "password123"  # Ou string vazia: ""
            e2e_context_instance.login_attempts = 0
            e2e_context_instance.login_success = False


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
