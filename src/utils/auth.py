"""
Centralized authentication utilities for AUDITORIA360
Consolidates get_api_token and related authentication functions
"""

import streamlit as st
from typing import Optional
from services.core.log_utils import logger


def get_api_token() -> Optional[str]:
    """
    Obtém o token da API do estado da sessão.
    Centralized function to get API token from session state.
    """
    return st.session_state.get("token")


def get_auth_headers(api_token: Optional[str] = None) -> dict:
    """
    Retorna os cabeçalhos de autenticação para chamadas de API.
    Returns authentication headers for API calls.
    
    Args:
        api_token: Optional token to use. If not provided, gets from session state.
        
    Returns:
        Dictionary with Authorization header if token is available.
    """
    token = api_token or get_api_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def get_current_client_id() -> Optional[str]:
    """
    Obtém o ID do cliente atual do estado da sessão.
    Gets current client ID from session state with fallback support.
    """
    client_id = st.session_state.get("client_id")
    # Fallback para o id_cliente legado, se existir
    if not client_id:
        client_id = st.session_state.get("id_cliente")
        if client_id:
            logger.warning("Usando 'id_cliente' legado na sessão. Considere migrar para 'client_id'.")
    return client_id


def handle_api_error(status_code: int) -> None:
    """
    Lida com erros de API, especificamente 401 Unauthorized.
    Handles API errors, specifically 401 Unauthorized.
    
    Args:
        status_code: HTTP status code from API response
    """
    if status_code == 401:
        st.error("Sessão expirada ou inválida. Por favor, faça login novamente.")
        # Limpa o estado da sessão relevante para forçar o login
        keys_to_clear = [
            "token", "api_token", "user_info", "client_id", "id_cliente", 
            "authenticated", "username", "authentication_status", "name"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
                logger.info(f"Limpando {key} da sessão devido a erro 401")


def display_user_info_sidebar() -> None:
    """
    Exibe informações do usuário na barra lateral.
    Displays user information in the sidebar.
    """
    if "user_info" in st.session_state and st.session_state.user_info:
        user_info = st.session_state.user_info
        st.sidebar.markdown("---")
        
        # Tenta obter o nome com fallbacks para diferentes campos possíveis
        nome_display = (
            user_info.get('name') or 
            user_info.get('nome') or 
            user_info.get('username') or 
            'N/A'
        )
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