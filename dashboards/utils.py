import streamlit as st
import sys
import os
from typing import Optional
from services.core.log_utils import logger # Corrigido caminho do logger

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

def get_auth_headers(api_token: Optional[str] = None):
    """Retorna os cabeçalhos de autenticação para chamadas de API."""
    # Usa token passado como parâmetro ou busca em st.session_state.token
    token = api_token or st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def get_api_token():
    """Obtém o token da API do estado da sessão."""
    # Corrigido para usar 'token' em vez de 'api_token', conforme painel.py
    return st.session_state.get("token")

def get_current_client_id():
    """Obtém o ID do cliente atual do estado da sessão."""
    # Mudado para client_id para compatibilidade com as páginas refatoradas
    client_id = st.session_state.get("client_id")
    # Fallback para o id_cliente legado, se existir
    if not client_id:
        client_id = st.session_state.get("id_cliente")
        if client_id:
            logger.warning("Usando 'id_cliente' legado na sessão. Considere migrar para 'client_id'.")
    return client_id

def handle_api_error(status_code: int):
    """Lida com erros de API, especificamente 401 Unauthorized."""
    if status_code == 401:
        st.error("Sessão expirada ou inválida. Por favor, faça login novamente.")
        # Limpa o estado da sessão relevante para forçar o login
        # Atualizado para incluir tanto as chaves novas quanto as legadas
        keys_to_clear = ["token", "api_token", "user_info", "client_id", "id_cliente", "authenticated", "username", 
                         "authentication_status", "name"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
                logger.info(f"Limpando {key} da sessão devido a erro 401")
        # Idealmente, redirecionaria para a página de login ou usaria st.rerun()
        # st.rerun() # Pode ser chamado pela página que invoca esta função
    # Outros códigos de status podem ser tratados aqui

def display_user_info_sidebar():
    """Exibe informações do usuário na barra lateral."""
    if "user_info" in st.session_state and st.session_state.user_info:
        user_info = st.session_state.user_info
        st.sidebar.markdown("---")
        
        # Tenta obter o nome com fallbacks para diferentes campos possíveis
        nome_display = user_info.get('name') or user_info.get('nome') or user_info.get('username') or 'N/A'
        st.sidebar.subheader(f"Usuário: {nome_display}")
        
        # Mostra empresa/organização se disponível
        empresa = user_info.get('empresa') or user_info.get('organization') or 'N/A'
        st.sidebar.caption(f"Empresa: {empresa}")
        
        # Exibe client_id com fallback para id_cliente
        client_id_display = get_current_client_id() or 'N/A'
        st.sidebar.caption(f"ID Cliente: {client_id_display}")
        
        # Se houver funções/roles definidas, exibi-las
        if 'roles' in user_info and user_info['roles']:
            roles_str = ", ".join(user_info['roles'])
            st.sidebar.caption(f"Funções: {roles_str}")
    else:
        st.sidebar.markdown("---")
        st.sidebar.caption("Informações do usuário não disponíveis.")
