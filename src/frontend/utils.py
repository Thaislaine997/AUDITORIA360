import streamlit as st
import sys
import os
from typing import Optional

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

def get_auth_headers(api_token: Optional[str] = None):
    """Retorna os cabeçalhos de autenticação para chamadas de API."""
    token = api_token or st.session_state.get("api_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def get_api_token():
    """Obtém o token da API do estado da sessão."""
    return st.session_state.get("api_token")

def get_current_client_id():
    """Obtém o ID do cliente atual do estado da sessão."""
    return st.session_state.get("id_cliente")

def handle_api_error(status_code: int):
    """Lida com erros de API, especificamente 401 Unauthorized."""
    if status_code == 401:
        st.error("Sessão expirada ou inválida. Por favor, faça login novamente.")
        # Limpa o estado da sessão relevante para forçar o login
        keys_to_clear = ["api_token", "user_info", "id_cliente", "authenticated", "username"]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        # Idealmente, redirecionaria para a página de login ou usaria st.rerun()
        # st.rerun() # Pode ser chamado pela página que invoca esta função
    # Outros códigos de status podem ser tratados aqui

def display_user_info_sidebar():
    """Exibe informações do usuário na barra lateral."""
    if "user_info" in st.session_state and st.session_state.user_info:
        user_info = st.session_state.user_info
        st.sidebar.markdown("---")
        st.sidebar.subheader(f"Usuário: {user_info.get('nome', 'N/A')}")
        st.sidebar.caption(f"Empresa: {user_info.get('empresa', 'N/A')}")
        st.sidebar.caption(f"ID Cliente: {st.session_state.get('id_cliente', 'N/A')}")
    else:
        st.sidebar.markdown("---")
        st.sidebar.caption("Informações do usuário não disponíveis.")
