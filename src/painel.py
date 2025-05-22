import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import json
import requests
from typing import Optional, Dict, Any
from datetime import date
import os

# DEBUG: Print a message when painel.py is imported
print(f"DEBUG: painel.py imported. __name__: {__name__}")

# Carregar configuração do YAML (primeira instanciação)
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

# DEBUG: Check if config.yaml exists from painel.py's perspective
print(f"DEBUG: config_path in painel.py: {config_path}")
print(f"DEBUG: os.path.exists(config_path) in painel.py: {os.path.exists(config_path)}")

config_yaml: Dict[str, Any] = {} # Initialize with a default and type hint
try:
    with open(config_path, 'r', encoding='utf-8') as file:
        loaded_yaml = yaml.load(file, Loader=SafeLoader)
        if isinstance(loaded_yaml, dict):
            config_yaml = loaded_yaml
        else:
            print(f"DEBUG: config.yaml at {config_path} did not load as a dict. Loaded: {type(loaded_yaml)}")
            # config_yaml remains {}
        print(f"DEBUG: config_yaml loaded (first instance) in painel.py: {json.dumps(config_yaml, indent=2)}")
except FileNotFoundError:
    print(f"DEBUG: config.yaml not found at {config_path}. Using default {{}}.")
    # config_yaml remains {}
except Exception as e:
    print(f"DEBUG: Error loading config_yaml (first instance) in painel.py: {e}")
    # config_yaml remains {}

# Verificar se 'credentials' e 'usernames' existem e fornecer uma estrutura mínima se não existirem
credentials_data = config_yaml.get('credentials')

if not isinstance(credentials_data, dict) or 'usernames' not in credentials_data:
    print("DEBUG: 'credentials' or 'usernames' not found in config_yaml (first instance). Using dummy structure for Authenticate.")
    config_yaml_auth: Dict[str, Any] = {
        'credentials': {
            'usernames': {
                'dummyuser': {'name': 'Dummy User', 'password': 'dummypassword'}
            }
        },
        'cookie': {'name': 'some_cookie', 'key': 'some_key', 'expiry_days': 30},
        'preauthorized': {}
    }
else:
    config_yaml_auth = config_yaml

print(f"DEBUG: config_yaml_auth for stauth.Authenticate (first instance): {json.dumps(config_yaml_auth, indent=2)}")

# Instanciar o autenticador (primeira e única instância agora)
try:
    # Ensure components of config_yaml_auth are dicts before accessing them to prevent TypeErrors
    auth_credentials = config_yaml_auth.get('credentials', {})
    auth_cookie = config_yaml_auth.get('cookie', {})
    auth_preauthorized = config_yaml_auth.get('preauthorized', {})

    # DEBUG: Print the exact credentials being passed to Authenticate
    print(f"DEBUG PAINEL: Credentials for Authenticate: {json.dumps(auth_credentials, indent=2)}")
    print(f"DEBUG PAINEL: Cookie Name: {auth_cookie.get('name', 'default_cookie_name')}")
    print(f"DEBUG PAINEL: Cookie Key: {auth_cookie.get('key', 'default_cookie_key')}")
    print(f"DEBUG PAINEL: Cookie Expiry: {auth_cookie.get('expiry_days', 30)}")

    if not isinstance(auth_credentials, dict) or not isinstance(auth_cookie, dict):
        print("DEBUG PAINEL: Invalid structure for credentials or cookie in config_yaml_auth. Raising error.") # Added PAINEL
        raise ValueError("Credentials or cookie data is not a dictionary.")

    authenticator = stauth.Authenticate(
        credentials=auth_credentials,
        cookie_name=auth_cookie.get('name', 'default_cookie_name'),
        cookie_key=auth_cookie.get('key', 'default_cookie_key'),
        cookie_expiry_days=auth_cookie.get('expiry_days', 30),
        preauthorized_emails=auth_preauthorized
    )
    print("DEBUG PAINEL: stauth.Authenticate instantiated successfully in painel.py") # Added PAINEL
except KeyError as e:
    print(f"DEBUG PAINEL: KeyError during stauth.Authenticate instantiation: {e}")
    print(f"DEBUG PAINEL: config_yaml_auth at point of error: {json.dumps(config_yaml_auth, indent=2)}")
    raise
except ValueError as e:
    print(f"DEBUG PAINEL: ValueError during stauth.Authenticate setup: {e}")
    raise
except Exception as e:
    print(f"DEBUG PAINEL: Unexpected error during stauth.Authenticate: {e}")
    raise

def st_recaptcha_custom(site_key):
    return st.text_input("Cole aqui o token do reCAPTCHA (prototipagem):")

# --- Carregar Configurações ---
def load_app_config():
    try:
        with open("src/config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        try:
            with open("config.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            st.error("Arquivo de configuração (config.json) não encontrado em src/ ou na raiz.")
            return {}

def fetch_public_config(api_base_url: str) -> dict:
    try:
        resp = requests.get(f"{api_base_url}/public-config", timeout=5)
        if resp.status_code == 200:
            return resp.json()
        else:
            st.warning(f"Não foi possível obter configurações públicas do cliente (status {resp.status_code}). Usando padrão local.")
            return {}
    except Exception as e:
        st.warning(f"Erro ao buscar configurações públicas do cliente: {e}")
        return {}

# Carrega config local para obter API_BASE_URL, mas sobrescreve com config público se disponível
app_cfg = load_app_config()
API_BASE_URL = app_cfg.get("API_BASE_URL", "http://localhost:8000")
public_cfg = fetch_public_config(API_BASE_URL)

# Prioriza valores do config público, mas mantém fallback para config local
RECAPTCHA_SITE_KEY = public_cfg.get("RECAPTCHA_SITE_KEY") or app_cfg.get("RECAPTCHA_SITE_KEY")
CLIENT_DISPLAY_NAME = public_cfg.get("client_display_name") or app_cfg.get("CLIENT_DISPLAY_NAME")
BRANDING_LOGO_URL = public_cfg.get("branding_logo_url") or app_cfg.get("BRANDING_LOGO_URL")

# --- Funções para buscar dados da API para os filtros ---
@st.cache_data(ttl=300)
def get_options_from_api(endpoint: str, params: Optional[dict] = None):
    if not API_BASE_URL:
        st.error("API_BASE_URL não configurado. Não é possível buscar opções.")
        return []
    url = f"{API_BASE_URL}/api/v1/options{endpoint}" 
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao buscar dados para filtros ({url}): {e}")
        return []
    except json.JSONDecodeError:
        st.error(f"Erro ao decodificar JSON da API ({url}). Resposta: {response.text if 'response' in locals() else 'N/A'}")
        return []

@st.cache_data(ttl=300)
def get_auditorias_from_api(filtros: dict):
    if not API_BASE_URL:
        st.error("API_BASE_URL não configurado. Não é possível buscar auditorias.")
        return None
    try:
        params_api = {}
        for key, value in filtros.items():
            if value not in [None, "", []]:
                if isinstance(value, date):
                    params_api[key] = value.isoformat()
                elif key == "page" and "size" in filtros and filtros["size"] is not None:
                    params_api[key] = value
                    params_api["size"] = filtros["size"]
                elif key == "size":
                    if "size" not in params_api:
                        params_api[key] = value
                else:
                    params_api[key] = value

        if "size" not in params_api and "size" in filtros and filtros["size"] is not None:
            params_api["size"] = filtros["size"]
        elif "size" not in params_api:
            params_api["size"] = 20

        response = requests.get(f"{API_BASE_URL}/api/v1/auditorias/", params=params_api)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = f"Erro ao buscar auditorias ({API_BASE_URL}/api/v1/auditorias/): {e}."
        if 'response' in locals() and response is not None:
            try:
                error_detail = response.json().get("detail", response.text)
            except json.JSONDecodeError:
                error_detail = response.text
            error_message += f" Detalhes: {error_detail}"
        st.error(error_message)
        return None
    except json.JSONDecodeError:
        st.error(f"Erro ao decodificar JSON das auditorias. Resposta: {response.text if 'response' in locals() else 'N/A'}")
        return None

def mostrar_pagina_gestao_controle_folhas():
    import pandas as pd
    from datetime import datetime
    st.header("🗓️ Gestão de Controle de Folhas")
    tab_importar, tab_visualizar = st.tabs(["📤 Importar Dados CSV", "📊 Visualizar Controle Mensal"])
    with tab_importar:
        st.subheader("Importar Planilha de Controle Mensal")
        st.markdown("""
            Envie seu arquivo CSV de controle mensal.
            - Os dados relevantes devem começar a partir da linha 9 do arquivo original.
            - Certifique-se de que o arquivo está no formato CSV.
        """)
        current_year = datetime.now().year
        meses_nomes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        col_ano_import, col_mes_import = st.columns([1,2])
        with col_ano_import:
            ano_ref_import = st.number_input("Ano de Referência", min_value=2020, max_value=current_year + 5, value=current_year, key="import_ano")
        with col_mes_import:
            mes_ref_import_nome = st.selectbox("Mês de Referência", options=meses_nomes, index=datetime.now().month -1, key="import_mes_nome")
        mes_ref_import_num = meses_nomes.index(mes_ref_import_nome) + 1
        uploaded_csv_file = st.file_uploader("Escolha o arquivo CSV", type="csv", key="controle_folha_uploader")
        if st.button("⚙️ Processar e Importar CSV", type="primary", key="btn_processar_import"):
            if uploaded_csv_file is not None:
                with st.spinner("Processando e importando dados... Por favor, aguarde."):
                    files = {"csv_file": (uploaded_csv_file.name, uploaded_csv_file, "text/csv")}
                    params = {"ano_referencia": ano_ref_import, "mes_referencia": mes_ref_import_num}
                    try:
                        response = requests.post(f"{API_BASE_URL}/api/v1/controle-folha/importar-csv/", files=files, params=params)
                        if response.status_code == 200:
                            resultado_importacao = response.json()
                            st.success(resultado_importacao.get("message", "Dados importados com sucesso!"))
                            if resultado_importacao.get("erros_processamento"):
                                st.warning("Algumas linhas tiveram problemas na importação:")
                                st.json(resultado_importacao.get("erros_processamento"))
                        else:
                            st.error(f"Falha na importação (HTTP {response.status_code}): {response.json().get('detail', 'Erro desconhecido.')}")
                    except requests.RequestException as e:
                        st.error(f"Erro de conexão ao importar: {e}")
                    except Exception as e:
                        st.error(f"Ocorreu um erro inesperado durante a importação: {str(e)}")
            else:
                st.warning("Por favor, selecione o ano, mês e um arquivo CSV para importar.")
    with tab_visualizar:
        st.subheader("Consultar Controle Mensal Registrado")
        col_ano_view, col_mes_view, col_emp_view = st.columns(3)
        with col_ano_view:
            ano_ref_visualizar = st.number_input("Ano", min_value=2020, max_value=current_year + 5, value=current_year, key="view_ano")
        with col_mes_view:
            opcoes_mes_view = ["Todos os Meses"] + meses_nomes
            mes_ref_visualizar_nome = st.selectbox("Mês", options=opcoes_mes_view, index=0, key="view_mes_nome")
        mes_ref_visualizar_num = None
        if mes_ref_visualizar_nome != "Todos os Meses":
            mes_ref_visualizar_num = meses_nomes.index(mes_ref_visualizar_nome) + 1
        with col_emp_view:
            empresa_id_visualizar = st.text_input("ID da Empresa (Opcional)", key="view_empresa_id", help="Deixe em branco para todas as empresas.")
        if st.button("🔍 Buscar Dados de Controle", key="btn_buscar_controle"):
            with st.spinner("Buscando dados..."):
                params_busca = {
                    "ano_referencia": ano_ref_visualizar,
                    "mes_referencia": mes_ref_visualizar_num,
                    "empresa_id": empresa_id_visualizar if empresa_id_visualizar else None,
                }
                params_busca_clean = {k: v for k, v in params_busca.items() if v is not None}
                try:
                    response = requests.get(f"{API_BASE_URL}/api/v1/controle-folha/", params=params_busca_clean)
                    if response.status_code == 200:
                        dados_controle = response.json()
                        if dados_controle:
                            st.success(f"{len(dados_controle)} registro(s) encontrado(s).")
                            df_controle = pd.DataFrame(dados_controle)
                            colunas_display = [
                                'empresa_id', 'ano_referencia', 'mes_referencia', 'status_dados_pasta',
                                'documentos_enviados_cliente', 'data_envio_documentos_cliente',
                                'guia_fgts_gerada', 'darf_inss_gerado', 'esocial_dctfweb_enviado',
                                'tipo_movimentacao', 'particularidades_observacoes'
                            ]
                            colunas_existentes_no_df = [col for col in colunas_display if col in df_controle.columns]
                            st.dataframe(df_controle[colunas_existentes_no_df], hide_index=True, use_container_width=True)
                        else:
                            st.info("Nenhum registro de controle encontrado para os filtros aplicados.")
                    else:
                        st.error(f"Falha ao buscar dados (HTTP {response.status_code}): {response.json().get('detail', 'Erro desconhecido.')}")
                except requests.RequestException as e:
                    st.error(f"Erro de conexão ao buscar dados: {e}")
                except Exception as e:
                    st.error(f"Ocorreu um erro inesperado ao buscar dados: {str(e)}")

def initialize_app():
    pass

def run_login_flow():
    # DEBUG: Print a message before attempting login call
    print("DEBUG PAINEL: About to call authenticator.login()")
    login_result = authenticator.login('main', fields={'Form name': 'Login Auditoria360'})
    print(f"DEBUG PAINEL: authenticator.login() call completed. Result: {login_result}")

    name = None
    authentication_status = None
    username = None

    if login_result is not None:
        try:
            name, authentication_status, username = login_result
            print(f"DEBUG PAINEL: Login result unpacked. Status: {authentication_status}, Name: {name}, Username: {username}")
        except ValueError:
            print(f"DEBUG PAINEL: Error unpacking login_result. Expected 3 values, got {len(login_result) if isinstance(login_result, tuple) else 'not a tuple'}. Result: {login_result}")
            # Define um status de falha se o desempacotamento falhar
            authentication_status = False 
    else:
        print("DEBUG PAINEL: login_result is None. Setting authentication_status to None to show login form or error.")
        # Se login_result é None, pode indicar que o formulário ainda precisa ser submetido
        # ou um erro mais fundamental. Tratar como 'None' para potencialmente mostrar o formulário.
        authentication_status = None


    if authentication_status is False:
        st.error('Usuário/senha incorreto')
        print("DEBUG PAINEL: Authentication failed (False)")
    elif authentication_status is None:
        st.warning('Por favor, insira seu usuário e senha')
        print("DEBUG PAINEL: Authentication is None (waiting for input)")
    elif authentication_status:
        print(f"DEBUG PAINEL: Authentication successful for user: {username} (Name: {name})")
    return authentication_status

def display_main_panel():
    username = st.session_state.get("username")

    if "recaptcha_verified_for_session" not in st.session_state:
        st.session_state["recaptcha_verified_for_session"] = False

    if not st.session_state["recaptcha_verified_for_session"]:
        st.write(f"Bem-vindo(a) {st.session_state.get('name')}!")
        st.info("Quase lá! Complete a verificação de segurança.")

        recaptcha_token = st_recaptcha_custom(RECAPTCHA_SITE_KEY)

        if st.button("Confirmar Sessão Segura"):
            if not RECAPTCHA_SITE_KEY:
                st.error("A verificação reCAPTCHA não pode ser processada pois a chave do site não está configurada.")
            elif recaptcha_token:
                if not API_BASE_URL:
                    st.error("API_BASE_URL não configurado. Não é possível verificar o reCAPTCHA.")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/auth/verify-recaptcha-session",
                            json={"username": username, "recaptcha_token": recaptcha_token}
                        )
                        if response.status_code == 200 and response.json().get("recaptcha_valid"):
                            st.session_state["recaptcha_verified_for_session"] = True
                            st.success("Verificação de segurança completa!")
                            st.rerun()
                        else:
                            error_detail = response.json().get('detail', 'Tente novamente.')
                            st.error(f"Falha na verificação reCAPTCHA: {error_detail}")
                            authenticator.logout('Logout', 'main')
                            keys_to_delete = ["authentication_status", "name", "username", "recaptcha_verified_for_session", "logout"]
                            for key in keys_to_delete:
                                if key in st.session_state:
                                    del st.session_state[key]
                            st.rerun()
                    except requests.RequestException as e:
                        st.error(f"Erro de comunicação ao verificar reCAPTCHA: {e}")
            else:
                st.warning("Por favor, complete o desafio reCAPTCHA.")
    else:
        authenticator.logout('Logout', 'main')
        st.title(f"Painel AUDITORIA360 - Bem-vindo(a) {st.session_state.get('name')}!")
        mostrar_pagina_gestao_controle_folhas()

def main():
    initialize_app()

    if BRANDING_LOGO_URL:
        st.sidebar.image(BRANDING_LOGO_URL, width=150)
    if CLIENT_DISPLAY_NAME:
        st.sidebar.markdown(f"<h3 style='text-align: center'>{CLIENT_DISPLAY_NAME}</h3>", unsafe_allow_html=True)

    if run_login_flow():
        display_main_panel()

if __name__ == "__main__":
    main()
