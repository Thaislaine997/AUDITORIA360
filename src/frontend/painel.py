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

if config and 'credentials' in config and 'cookie' in config: # Removido 'preauthorized' da verificação
    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
        # config['preauthorized'] # Removido parâmetro obsoleto
    )
else:
    st.error("Erro crítico: Arquivo de configuração de autenticação (login.yaml) está incompleto ou corrompido. Verifique as chaves 'credentials' e 'cookie'.") # Mensagem de erro atualizada
    logger.error("Erro crítico: Arquivo de configuração de autenticação (login.yaml) está incompleto ou corrompido.")
    st.stop()

# --- Página de Login ---
# Renderiza o formulário de login ou o estado de autenticado/erro
# A função login() precisa ser chamada em cada script/página onde a autenticação é necessária
# se você não estiver usando um gerenciamento de estado de sessão mais centralizado que persista entre "páginas"
# de forma que o authenticator saiba o estado.
# No modelo multipage do Streamlit, o st.session_state é compartilhado.

# Exibe o título e o logo ANTES de chamar authenticator.login()
# para que apareçam mesmo se o usuário ainda não estiver logado.
st.title("Bem-vindo ao Auditoria360")

logo_path = os.path.join('assets', 'logo.png')
if os.path.exists(logo_path):
    st.image(logo_path, width=180)

# A chamada login() irá exibir o formulário ou, se já logado e o cookie for válido,
# irá pular o formulário e definir st.session_state.authentication_status = True.
authenticator.login('main', fields={'Form name': 'Login Auditoria360'})


if st.session_state.get("authentication_status"):
    # Usuário autenticado com sucesso pelo streamlit-authenticator
    
    # Etapa 1: Obter/Confirmar token da API
    if "token" not in st.session_state or st.session_state["token"] is None:
        st.subheader("Confirmação de Segurança Adicional")
        current_username = st.session_state.get("username")
        
        if not current_username:
            st.error("Nome de usuário não encontrado na sessão. Por favor, faça logout e login novamente.")
            authenticator.logout("Logout", "main", key="logout_error_username") # Fornece uma opção de logout
            st.stop()
            
        api_password = st.text_input(
            f"Olá {st.session_state.get('name', 'usuário')}, por favor, insira sua senha novamente para finalizar o login seguro:", 
            type="password", 
            key="api_password_input_main_panel"
        )
        
        if st.button("Confirmar Senha e Acessar API", key="confirm_api_password_main_panel"):
            if api_password: # current_username já verificado
                token = autenticar_api(current_username, api_password)
                if token:
                    st.session_state["token"] = token
                    # Não precisa de st.success aqui, o rerun vai mostrar a interface logada.
                    st.rerun() 
                else:
                    st.error("Falha ao obter o token da API. Verifique sua senha ou tente novamente.")
                    # Não parar aqui, permite nova tentativa de senha.
            else:
                st.warning("Senha é necessária para autenticação na API.")
        else:
            st.info("É necessário confirmar sua senha para acessar os recursos da aplicação.")
            st.stop() # Aguarda a entrada da senha e o clique no botão.
    
    # Etapa 2: Token da API obtido, configurar sessão e interface de usuário logado
    # Esta parte só executa se st.session_state.token existir (após o rerun da etapa anterior)
    if "token" in st.session_state and st.session_state["token"] is not None:
        # Obter id_cliente (client_id)
        if 'client_id' not in st.session_state or st.session_state.get('client_id') is None: # Alterado para client_id
            current_username = st.session_state.get("username") # Já deve estar definido
            if current_username and config:
                user_credentials = config.get('credentials', {}).get('usernames', {}).get(current_username, {})
                client_id = user_credentials.get('client_id')
                if client_id:
                    st.session_state['client_id'] = client_id # Alterado para client_id
                    # Manter id_cliente para compatibilidade com código legado temporariamente
                    st.session_state['id_cliente'] = client_id
                    logger.info(f"ID do Cliente '{client_id}' armazenado na sessão para o usuário '{current_username}'.")
                else:
                    logger.warning(f"ID do Cliente (client_id) não encontrado na configuração para o usuário '{current_username}'.")
                    st.session_state['client_id'] = "N/A" # Alterado para client_id 
                    st.session_state['id_cliente'] = "N/A" # Manter id_cliente para compatibilidade
                    st.warning(f"Atenção: ID do Cliente (client_id) não configurado para o usuário '{current_username}' no arquivo auth/login.yaml. Algumas funcionalidades podem ser limitadas.")
            elif not config: # Deve ser pego antes, mas como fallback
                st.error("Configuração de autenticação (login.yaml) não carregada. Não é possível obter client_id.")
                st.session_state['client_id'] = "ERRO_CONFIG" # Alterado para client_id
                st.session_state['id_cliente'] = "ERRO_CONFIG" # Manter id_cliente para compatibilidade

        # Configurar informações do usuário para utilização em utils.py display_user_info_sidebar
        if 'user_info' not in st.session_state: 
            st.session_state.user_info = {
                "name": st.session_state.get('name', 'Usuário'),
                "username": st.session_state.get('username', ''),
                # Outros campos podem ser adicionados conforme necessário
            }

        # Configurar a interface de usuário logado (sidebar e corpo da página)
        authenticator.logout('Logout', 'sidebar', key='logout_sidebar_button') 
        st.sidebar.title(f"Bem-vindo(a)")
        st.sidebar.markdown(f"**{st.session_state.get('name')}**") # Nome em negrito
        
        if st.session_state.get('client_id') and st.session_state.get('client_id') not in ["N/A", "ERRO_CONFIG"]: # Alterado para client_id
            st.sidebar.caption(f"Cliente ID: {st.session_state['client_id']}") # Alterado para client_id
        elif st.session_state.get('client_id') == "N/A": # Alterado para client_id
             st.sidebar.warning("Cliente ID não definido.")
        else:
            st.sidebar.error("Erro ao obter Cliente ID.")
        
        st.sidebar.markdown("---") # Linha divisória na sidebar
        st.header("Login realizado com sucesso! ✅")
        st.info("Selecione uma página no menu à esquerda para começar a utilizar o sistema.")
        st.balloons() # Celebração!

elif st.session_state.get("authentication_status") is False:
    st.error('Usuário ou senha incorreto. Por favor, tente novamente.')
    # Nenhuma informação de usuário ou logout na sidebar deve aparecer aqui.

elif st.session_state.get("authentication_status") is None:
    st.subheader("Por favor, faça o login para continuar.")
    # O formulário de login é renderizado por authenticator.login() acima.
    # Nenhuma informação de usuário ou logout na sidebar deve aparecer aqui.
    # As páginas na pasta `pages/` ainda serão listadas pelo Streamlit,
    # mas o acesso ao conteúdo delas deve ser bloqueado pela verificação no topo de cada página.
    pass 

else: 
    # Este caso não deveria ser alcançado se as verificações acima estiverem corretas.
    st.error("A aplicação não pôde ser inicializada devido a um erro inesperado na autenticação.")
    logger.error("Estado de autenticação inválido ou inesperado.")
    st.stop()

# Adicionar uma verificação final: se o usuário não está autenticado (status não é True),
# e estamos em painel.py, não devemos mostrar nada além do formulário de login ou erros.
# Se o status é None ou False, a lógica acima já trata de exibir o formulário ou erro.
# O principal é que o conteúdo "logado" (logout na sidebar, etc.) só aparece se status for True E token existir.