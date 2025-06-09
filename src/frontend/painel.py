import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
import os
from core.log_utils import logger
from core.config import *
from core.database import *

# --- Configuração da Página ---
st.set_page_config(
    page_title="Auditoria360 - Login",
    page_icon="🔐",
    layout="centered"
)

# --- Função para carregar as credenciais ---
def load_user_config():
    try:
        with open(os.path.join('auth', 'login.yaml'), encoding='utf-8') as file:
            return yaml.load(file, Loader=SafeLoader)
    except FileNotFoundError:
        st.error("Arquivo de configuração 'auth/login.yaml' não encontrado.")
        st.info("Certifique-se de que o arquivo está no diretório 'auth' na raiz do projeto.")
        return None

config = load_user_config()

# --- Função para autenticar na API e obter o token JWT ---
def autenticar_api(username, password):
    import requests
    API_BASE_URL = os.environ.get("API_BASE_URL") or "http://localhost:8000"
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        st.error(f"Erro ao autenticar na API: {e}")
        return None

if config:
    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # --- Página de Login ---
    st.title("Bem-vindo ao Auditoria360")
    st.subheader("Por favor, faça o login para continuar.")

    # (Opcional) Exibe o logo se existir
    logo_path = os.path.join('assets', 'logo.png')
    if os.path.exists(logo_path):
        st.image(logo_path, width=180)

    login_result = authenticator.login('main')
    if login_result is not None:
        name, authentication_status, username = login_result
    else:
        name = authentication_status = username = None

    if st.session_state["authentication_status"]:
        # --- NOVO: Autenticação na API para obter o token JWT ---
        if "token" not in st.session_state:
            # O campo 'password' pode não estar disponível diretamente, então peça ao usuário novamente se necessário
            password = st.session_state.get("password")
            if not password:
                password = st.text_input("Digite sua senha novamente para autenticação na API:", type="password")
            if password:
                token = autenticar_api(username, password)
                if token:
                    st.session_state["token"] = token
                else:
                    st.stop()
            else:
                st.warning("Senha necessária para autenticação na API.")
                st.stop()
        authenticator.logout('Logout', 'sidebar')
        st.sidebar.title(f"Bem-vindo(a) *{st.session_state['name']}*")
        st.header("Login realizado com sucesso! ✅")
        st.info("Selecione uma página no menu à esquerda para começar.")
    elif st.session_state["authentication_status"] is False:
        st.error('Usuário/senha está incorreto')
    elif st.session_state["authentication_status"] is None:
        st.warning('Por favor, insira seu usuário e senha')
else:
    st.error("A aplicação não pôde ser inicializada devido a um erro na configuração de autenticação.")