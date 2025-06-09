import streamlit as st
import sys # Add sys
import os # Add os

# --- Path Setup ---
# Add the project root to sys.path to allow imports like 'from src.core...'
# Assumes painel.py is in src/frontend/
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
import requests # Adicionado import de requests
from src.core.log_utils import logger # Corrigido o caminho do import
from src.core.config import settings # Corrigido o caminho do import
# from core.database import * # Comentado ou removido se não usado diretamente aqui

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
    # API_BASE_URL = os.environ.get("API_BASE_URL") or "http://localhost:8000" # Removido
    try:
        response = requests.post(
            f"{settings.API_BASE_URL}/auth/token",  # Corrigido endpoint e usando settings.API_BASE_URL
            data={"username": username, "password": password}, # FastAPI espera dados de formulário para OAuth2PasswordRequestForm
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("access_token") # Usar .get() para segurança
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Erro HTTP ao autenticar na API: {http_err}")
        logger.error(f"Detalhes da resposta: {response.text}")
        st.error(f"Erro ao autenticar com o servidor: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Erro ao autenticar na API: {e}")
        st.error(f"Ocorreu um erro inesperado durante a autenticação na API.")
        return None

if config and 'credentials' in config and 'cookie' in config and 'preauthorized' in config:
    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
else:
    st.error("Erro crítico: Arquivo de configuração de autenticação (login.yaml) está incompleto ou corrompido. Verifique as chaves 'credentials', 'cookie' e 'preauthorized'.")
    logger.error("Erro crítico: Arquivo de configuração de autenticação (login.yaml) está incompleto ou corrompido.")
    st.stop()

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
    if "token" not in st.session_state or st.session_state["token"] is None: # Adicionado check para token None
        # O campo 'password' pode não estar disponível diretamente, então peça ao usuário novamente se necessário
        # Esta é uma limitação de como o streamlit-authenticator lida com senhas após o login.
        # Idealmente, o próprio authenticator poderia lidar com a obtenção do token da API.
        # Por enquanto, pedimos a senha novamente de forma segura.

        # Tentativa de usar a senha do formulário de login se disponível (improvável com streamlit-authenticator)
        # O streamlit-authenticator não armazena a senha em st.session_state por segurança.
        # Portanto, a única forma segura é pedir novamente ou usar um fluxo OAuth mais complexo.

        # Para simplificar e manter a segurança, vamos assumir que o usuário precisa digitar a senha novamente
        # apenas para esta etapa de obtenção do token da API, se não for encontrado.
        # O username é st.session_state["username"]

        if 'provided_password_for_api' not in st.session_state:
            st.session_state['provided_password_for_api'] = ""

        # Usar o username já autenticado pelo streamlit-authenticator
        current_username = st.session_state.get("username")
        
        # Solicitar a senha novamente para a chamada da API
        # Isso é feito aqui porque o streamlit-authenticator não expõe a senha após o login bem-sucedido.
        api_password = st.text_input(
            f"Olá {st.session_state['name']}, por favor, insira sua senha novamente para finalizar o login seguro:", 
            type="password", 
            key="api_password_input"
        )
        
        if st.button("Confirmar Senha e Acessar API"):
            if api_password and current_username:
                st.session_state['provided_password_for_api'] = api_password
                token = autenticar_api(current_username, st.session_state['provided_password_for_api'])
                if token:
                    st.session_state["token"] = token
                    st.success("Token da API obtido com sucesso!")
                    # Força o rerun para remover o campo de senha e prosseguir
                    st.rerun() # Corrigido de st.experimental_rerun para st.rerun
                else:
                    st.error("Falha ao obter o token da API. Verifique suas credenciais ou tente novamente.")
                    # Não parar, permitir nova tentativa
            else:
                st.warning("Senha é necessária para autenticação na API.")
        else:
            # Se o botão não foi clicado, e não há token, parar para aguardar a senha.
            st.info("É necessário confirmar sua senha para acessar os recursos da aplicação.")
            st.stop() 
    
    # Se o token foi obtido (ou já existia), prossegue normalmente
    if "token" in st.session_state and st.session_state["token"] is not None:
        # Adicionar lógica para obter e armazenar id_cliente
        if 'id_cliente' not in st.session_state:
            current_username = st.session_state.get("username")
            if current_username and config:
                user_credentials = config.get('credentials', {}).get('usernames', {}).get(current_username, {})
                client_id = user_credentials.get('client_id')
                if client_id:
                    st.session_state['id_cliente'] = client_id # Correção: atribuir client_id
                    logger.info(f"ID do Cliente '{client_id}' armazenado na sessão para o usuário '{current_username}'.")
                else:
                    st.error(f"ID do Cliente (client_id) não encontrado na configuração para o usuário '{current_username}' em auth/login.yaml.")
                    st.warning("Algumas funcionalidades podem não operar corretamente sem o ID do Cliente.")
                    # Considere st.stop() aqui se o client_id for estritamente necessário para prosseguir
            elif not config:
                st.error("Configuração de autenticação (login.yaml) não carregada. Não é possível obter client_id.")
        
        authenticator.logout('Logout', 'sidebar')
        st.sidebar.title(f"Bem-vindo(a) *{st.session_state['name']}*")
        # Exibir client_id na sidebar se disponível
        if 'id_cliente' in st.session_state:
            st.sidebar.caption(f"Cliente ID: {st.session_state['id_cliente']}")
        else:
            st.sidebar.caption("Cliente ID: Não definido")
        
        st.header("Login realizado com sucesso! ✅")
        st.info("Selecione uma página no menu à esquerda para começar.")
    else:
        # Caso onde o token não foi obtido e o usuário não forneceu a senha ainda, ou falhou.
        # A lógica acima com st.stop() e o botão deve cobrir isso.
        # Se chegar aqui, é um estado inesperado ou o usuário não interagiu com o formulário de senha.
        if not st.session_state.get("token"):
             st.warning("Autenticação com a API pendente. Por favor, forneça sua senha quando solicitado.")
             st.stop()
elif st.session_state["authentication_status"] is False:
    st.error('Usuário/senha está incorreto')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor, insira seu usuário e senha')
else:
    st.error("A aplicação não pôde ser inicializada devido a um erro na configuração de autenticação.")