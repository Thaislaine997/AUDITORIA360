"""
Utilitários para frontend e autenticação.
"""

from typing import Any, Dict, Optional

import requests
import streamlit as st


def get_auth_headers() -> Dict[str, str]:
    """
    Retorna os headers de autenticação para requisições à API.

    Returns:
        dict: Headers com token de autenticação se disponível
    """
    headers = {"Content-Type": "application/json"}

    if "api_token" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state['api_token']}"

    return headers


def is_authenticated() -> bool:
    """
    Verifica se o usuário está autenticado.

    Returns:
        bool: True se autenticado, False caso contrário
    """
    return (
        st.session_state.get("authentication_status") is True
        and st.session_state.get("api_token") is not None
    )


def require_authentication():
    """
    Decorator/função para exigir autenticação em páginas.
    Redireciona para login se não autenticado.
    """
    if not is_authenticated():
        st.error("⚠️ Acesso negado. Faça login para continuar.")
        st.stop()


def get_current_user() -> Optional[Dict[str, Any]]:
    """
    Retorna os dados do usuário atual.

    Returns:
        dict: Dados do usuário se autenticado, None caso contrário
    """
    if is_authenticated():
        return {
            "name": st.session_state.get("name"),
            "username": st.session_state.get("username"),
            "authenticated": True,
        }
    return None


def logout_user():
    """
    Faz logout do usuário, limpando a sessão.
    """
    keys_to_clear = [
        "authentication_status",
        "api_token",
        "name",
        "username",
        "password",
        "password_input",
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    st.rerun()


def make_authenticated_request(
    url: str, method: str = "GET", **kwargs
) -> requests.Response:
    """
    Faz uma requisição autenticada à API.

    Args:
        url: URL da API
        method: Método HTTP (GET, POST, etc.)
        **kwargs: Argumentos adicionais para requests

    Returns:
        Response: Resposta da requisição
    """
    headers = get_auth_headers()
    if "headers" in kwargs:
        headers.update(kwargs["headers"])
    kwargs["headers"] = headers

    return requests.request(method, url, **kwargs)
