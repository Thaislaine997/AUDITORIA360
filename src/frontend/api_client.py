import os
import requests
import pandas as pd
import streamlit as st

API_BASE_URL = os.environ.get("API_BASE_URL") or "http://localhost:8000"

def api_login(username: str, password: str) -> str | None:
    """Autentica na API e retorna o token JWT."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if "access_token" not in data:
            st.error("Resposta da API não contém token de acesso.")
            return None
        return data["access_token"]
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        st.error(f"Erro de autenticação: {detail}")
    except Exception as e:
        st.error(f"Erro ao autenticar na API: {e}")
    return None

@st.cache_data(ttl=300)
def get_dashboard_data(id_empresa: int, token: str) -> pd.DataFrame:
    endpoint = f"{API_BASE_URL}/dashboard/folha/"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"id_empresa": id_empresa}
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.HTTPError as err:
        detail = err.response.json().get("detail", err.response.text)
        st.error(f"Erro da API ao carregar dados do dashboard: {detail}")
    except requests.exceptions.RequestException as e:
        st.error(f"Não foi possível conectar ao servidor: {e}")
    return pd.DataFrame()

@st.cache_data(ttl=300)
def get_checklist_folha(id_folha: str, token: str) -> dict:
    endpoint = f"{API_BASE_URL}/checklist/folha/{id_folha}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar checklist: {e}")
        return {}

@st.cache_data(ttl=300)
def get_empresa_info(id_empresa: str, token: str) -> dict:
    endpoint = f"{API_BASE_URL}/empresas/{id_empresa}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados da empresa: {e}")
        return {}

def post_processar_folha(payload: dict, token: str) -> dict:
    endpoint = f"{API_BASE_URL}/folhas/processar"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao processar folha: {e}")
        return {}

@st.cache_data(ttl=300)
def get_folhas_empresa(id_empresa: int, token: str) -> pd.DataFrame:
    """Obtém todas as folhas de uma empresa."""
    endpoint = f"{API_BASE_URL}/folhas/empresa/{id_empresa}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar folhas da empresa: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_relatorio_folha(id_folha: str, token: str) -> dict:
    """Obtém o relatório detalhado de uma folha específica."""
    endpoint = f"{API_BASE_URL}/relatorios/folha/{id_folha}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar relatório da folha: {e}")
        return {}

@st.cache_data(ttl=300)
def get_parametros_legais(tipo: str, token: str) -> pd.DataFrame:
    endpoint = f"{API_BASE_URL}/parametros-legais/{tipo}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar parâmetros legais: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def get_parametros_legais_tipo(tipo: str, token: str) -> pd.DataFrame:
    """Obtém parâmetros legais por tipo (ex: INSS, IRRF, FGTS)."""
    endpoint = f"{API_BASE_URL}/parametros-legais/{tipo}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar parâmetros legais do tipo {tipo}: {e}")
        return pd.DataFrame()

# Função genérica para requisições GET autenticadas

def api_get(endpoint: str, token: str, params: dict = None) -> dict | list | None:
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    if params is None:
        params = {}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar {endpoint}: {e}")
        return None

# Função genérica para requisições POST autenticadas

def api_post(endpoint: str, token: str, payload: dict) -> dict | None:
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar {endpoint}: {e}")
        return None
