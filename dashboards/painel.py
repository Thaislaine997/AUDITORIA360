import os  # Add os
import sys  # Add sys

import requests
import streamlit as st
import yaml
from streamlit_authenticator import Authenticate
from yaml.loader import SafeLoader

from configs.settings import settings

# --- Path Setup ---
# Add the project root to sys.path to allow imports like 'from src.core...'

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---


# --- Carregamento do CSS para Design System ---
def load_css():
    """Carrega a folha de estilos do Design System AUDITORIA360"""
    css_path = os.path.join(_project_root, "assets", "style.css")
    if os.path.exists(css_path):
        try:
            with open(css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar CSS: {e}")
    else:
        st.warning(f"⚠️ Arquivo de estilo não encontrado em {css_path}")


def load_logo():
    """Carrega e exibe o logotipo da aplicação"""
    logo_path = os.path.join(_project_root, "assets", "logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as img_file:
                import base64

                b64_img = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f"""
                <div class="header">
                    <img src="data:image/png;base64,{b64_img}" 
                         alt="Logo AUDITORIA360" 
                         class="logo"
                         style="height: 60px; width: auto;"/>
                    <h1 class="header-title">AUDITORIA360</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.markdown(
                """
                <div class="header">
                    <h1 class="header-title">🔍 AUDITORIA360</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.warning(f"⚠️ Erro ao carregar logo: {e}")
    else:
        st.markdown(
            """
            <div class="header">
                <h1 class="header-title">🔍 AUDITORIA360</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )


# Aplicar Design System
load_css()  # Carrega os estilos do Design System
load_logo()  # Carrega e exibe o logo
# --- Fim do Carregamento do CSS ---

# from core.database import * # Comentado ou removido se não usado diretamente aqui

# --- Configuração da Página ---
st.set_page_config(
    page_title="AUDITORIA360 - Plataforma de Auditoria Inteligente",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/Thaislaine997/AUDITORIA360",
        "Report a bug": "https://github.com/Thaislaine997/AUDITORIA360/issues",
        "About": "AUDITORIA360 - Plataforma moderna de auditoria com IA",
    },
)

# --- Carregador de Configuração do Autenticador (do arquivo YAML) ---
try:
    with open("auth/login.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )
except FileNotFoundError:
    st.error("Arquivo de configuração de login 'auth/login.yaml' não encontrado.")
    config = None

# --- Página de Login ---
if config:
    st.title("Bem-vindo ao Auditoria360")
    st.subheader("Por favor, faça o login para continuar.")

    # O método login pode variar conforme a versão do streamlit-authenticator
    login_result = authenticator.login("main")
    if isinstance(login_result, tuple):
        name, authentication_status, username = login_result
    else:
        name = authentication_status = username = None

    if st.session_state.get("authentication_status"):
        # ---- INÍCIO DA MODIFICAÇÃO ----
        if "api_token" not in st.session_state:
            try:
                # Tenta obter a senha do session_state
                password = st.session_state.get(
                    "password_input"
                ) or st.session_state.get("password")
                if not password:
                    st.error("Senha não encontrada na sessão. Faça login novamente.")
                    st.session_state["authentication_status"] = False
                else:
                    response = requests.post(
                        f"{settings.API_BASE_URL}/api/auth/token",
                        data={"username": username, "password": password},
                    )
                    if response.status_code == 200:
                        token_data = response.json()
                        st.session_state["api_token"] = token_data["access_token"]
                        st.success("Login na API realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error(
                            f"Falha ao autenticar com a API: {response.json().get('detail')}"
                        )
                        st.session_state["authentication_status"] = False
            except Exception as e:
                st.error(f"Ocorreu um erro ao conectar com a API: {e}")
                st.session_state["authentication_status"] = False
        # ---- FIM DA MODIFICAÇÃO ----

        # Esta parte só é visível após o login e obtenção do token
        if st.session_state.get("api_token"):
            authenticator.logout("Logout", "sidebar")
            st.sidebar.title(f"Bem-vindo(a), {st.session_state.get('name', username)}!")
            st.header("Login realizado com sucesso! ✅")
            st.info("Selecione uma página no menu à esquerda para começar.")

    elif st.session_state.get("authentication_status") is False:
        st.error("Usuário/senha está incorreto")
    elif st.session_state.get("authentication_status") is None:
        st.warning("Por favor, insira seu usuário e senha")
