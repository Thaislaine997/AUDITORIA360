import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import json
import requests
from typing import Optional, Dict, Any, Literal # Adicionado Literal
from datetime import date, datetime # Adicionado datetime
import os
import pandas as pd

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

# --- Novas Páginas de Gestão de Parâmetros Legais ---

def mostrar_pagina_salario_minimo():
    st.header("🪙 Gestão de Salário Mínimo")

    if 'editing_sm_item' not in st.session_state:
        st.session_state.editing_sm_item = None
    if 'item_id_para_deletar_sm' not in st.session_state:
        st.session_state.item_id_para_deletar_sm = None

    @st.cache_data(ttl=60)
    def fetch_sm_data():
        try:
            response = requests.get(f"{API_BASE_URL}/param-legais/salario-minimo/?skip=0&limit=1000")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.error(f"Erro ao buscar dados de Salário Mínimo: {e}")
            return []
        except json.JSONDecodeError:
            st.error("Erro ao decodificar resposta da API de Salário Mínimo.")
            return []

    def create_sm_entry(payload):
        try:
            response = requests.post(f"{API_BASE_URL}/param-legais/salario-minimo/", json=payload)
            response.raise_for_status()
            st.success("Nova vigência de Salário Mínimo criada com sucesso!")
            st.cache_data.clear()
            return response.json()
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao criar Salário Mínimo ({e.response.status_code}): {detail}")
            return None
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao criar Salário Mínimo: {e}")
            return None

    def update_sm_entry(id_versao: str, payload):
        try:
            response = requests.put(f"{API_BASE_URL}/param-legais/salario-minimo/{id_versao}", json=payload)
            response.raise_for_status()
            st.success(f"Vigência de Salário Mínimo {id_versao} atualizada com sucesso!")
            st.cache_data.clear()
            st.session_state.editing_sm_item = None # Limpa o item de edição após sucesso
            return response.json()
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao atualizar Salário Mínimo {id_versao} ({e.response.status_code}): {detail}")
            return None
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao atualizar Salário Mínimo {id_versao}: {e}")
            return None

    def delete_sm_entry(id_versao: str):
        try:
            response = requests.delete(f"{API_BASE_URL}/param-legais/salario-minimo/{id_versao}")
            response.raise_for_status()
            st.success(f"Vigência de Salário Mínimo {id_versao} inativada com sucesso!")
            st.cache_data.clear()
            return True
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao inativar Salário Mínimo {id_versao} ({e.response.status_code}): {detail}")
            return False
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao inativar Salário Mínimo {id_versao}: {e}")
            return False

    if st.session_state.get('item_id_para_deletar_sm'):
        item_id_to_delete = str(st.session_state.item_id_para_deletar_sm)
        st.warning(f"Tem certeza que deseja inativar a vigência de Salário Mínimo com ID {item_id_to_delete}?")
        col1, col2, _ = st.columns([1,1,5])
        with col1:
            if st.button("Sim, Inativar", key=f"confirm_delete_sm_{item_id_to_delete}"):
                if delete_sm_entry(item_id_to_delete):
                    st.session_state.item_id_para_deletar_sm = None
                    st.rerun()
        with col2:
            if st.button("Cancelar", key=f"cancel_delete_sm_{item_id_to_delete}"):
                st.session_state.item_id_para_deletar_sm = None
                st.rerun()
        return

    col_form, col_view = st.columns([1, 2])

    with col_form:
        editing_item = st.session_state.get('editing_sm_item')
        form_title = "Adicionar Nova Vigência" if not editing_item else f"Editando Vigência ID: {editing_item.get('id_versao', 'Desconhecido')}"
        st.subheader(form_title)

        form_key_suffix = f"_edit_{editing_item['id_versao']}" if editing_item and editing_item.get('id_versao') else "_new"

        default_data_inicio = date.today()
        default_data_fim_val = None
        default_data_fim_chk = False
        default_valor_nacional = 0.0
        default_valores_regionais_str = ""
        default_observacao = ""

        if editing_item:
            raw_data_inicio = editing_item.get('data_inicio_vigencia')
            if raw_data_inicio:
                try:
                    dt_obj = pd.to_datetime(raw_data_inicio)
                    if pd.notna(dt_obj): default_data_inicio = dt_obj.date()
                except Exception as e_parse_data_inicio:
                    print(f"Erro ao parsear data_inicio_vigencia: {raw_data_inicio}, Erro: {e_parse_data_inicio}")
                    # Mantém o default se a conversão falhar

            raw_data_fim = editing_item.get('data_fim_vigencia')
            if raw_data_fim:
                try:
                    dt_obj_fim = pd.to_datetime(raw_data_fim)
                    if pd.notna(dt_obj_fim):
                        default_data_fim_val = dt_obj_fim.date()
                        default_data_fim_chk = True
                except Exception as e_parse_data_fim:
                    print(f"Erro ao parsear data_fim_vigencia: {raw_data_fim}, Erro: {e_parse_data_fim}")
                    # Mantém o default se a conversão falhar
            
            raw_valor_nacional = editing_item.get('valor_nacional')
            if raw_valor_nacional is not None:
                try: 
                    default_valor_nacional = float(raw_valor_nacional)
                except (ValueError, TypeError) as e_parse_valor:
                    print(f"Erro ao parsear valor_nacional: {raw_valor_nacional}, Erro: {e_parse_valor}")
                    # Mantém o default se a conversão falhar

            raw_valores_regionais = editing_item.get('valores_regionais')
            if raw_valores_regionais:
                try:
                    if isinstance(raw_valores_regionais, dict):
                        default_valores_regionais_str = json.dumps(raw_valores_regionais, ensure_ascii=False, indent=2)
                    elif isinstance(raw_valores_regionais, str): # Se já for uma string JSON
                        # Tenta carregar para validar e reformatar, ou usa como está se falhar
                        try:
                            parsed_json = json.loads(raw_valores_regionais)
                            default_valores_regionais_str = json.dumps(parsed_json, ensure_ascii=False, indent=2)
                        except json.JSONDecodeError:
                            default_valores_regionais_str = raw_valores_regionais # Usa a string como está se não for JSON válido
                    else:
                        default_valores_regionais_str = str(raw_valores_regionais) # Fallback para string
                except TypeError as e_parse_regionais_type:
                     print(f"Erro de tipo ao processar valores_regionais: {raw_valores_regionais}, Erro: {e_parse_regionais_type}")
                     default_valores_regionais_str = str(raw_valores_regionais) # Fallback
                except Exception as e_parse_regionais_geral:
                    print(f"Erro geral ao processar valores_regionais: {raw_valores_regionais}, Erro: {e_parse_regionais_geral}")
                    default_valores_regionais_str = str(raw_valores_regionais) # Fallback
            
            default_observacao = str(editing_item.get('observacao', ""))

        with st.form("sm_add_edit_form" + form_key_suffix, clear_on_submit=(not editing_item)):
            data_inicio_vigencia = st.date_input(
                "Data Início Vigência*",
                value=default_data_inicio,
                help="Data de início da validade desta tabela.",
                key="sm_div" + form_key_suffix
            )

            col_fim_chk, col_fim_date = st.columns([1,2])
            with col_fim_chk:
                data_fim_especificada = st.checkbox("Definir Data Fim?",
                                                    value=default_data_fim_chk,
                                                    key="sm_dfv_chk" + form_key_suffix)
            data_fim_vigencia_input_val = None
            if data_fim_especificada:
                with col_fim_date:
                    current_fim_val = default_data_fim_val
                    min_date_for_fim = data_inicio_vigencia 

                    if default_data_fim_val and data_inicio_vigencia and default_data_fim_val < data_inicio_vigencia:
                        current_fim_val = data_inicio_vigencia
                    
                    data_fim_vigencia_input_val = st.date_input("Data Fim Vigência",
                                                      value=current_fim_val,
                                                      min_value=min_date_for_fim, 
                                                      key="sm_dfv_date" + form_key_suffix,
                                                      help="Opcional. Se não definida, a vigência é considerada aberta.")

            valor_nacional = st.number_input(
                "Valor Nacional (R$)*",
                min_value=0.0,
                format="%.2f",
                step=0.01,
                value=default_valor_nacional,
                key="sm_vn" + form_key_suffix
            )
            valores_regionais_json = st.text_area(
                "Valores Regionais (JSON)",
                value=default_valores_regionais_str,
                placeholder='{\"SP\": 1640.00, \"RJ\": 1550.50}',
                help='Opcional. Formato: {\"UF\": valor}. Ex: {\"SP\": 1640.00}',
                key="sm_vr" + form_key_suffix,
                height=100
            )
            observacao = st.text_area(
                "Observação",
                value=default_observacao,
                key="sm_obs" + form_key_suffix
            )

            submit_button_label = "Salvar Nova Vigência" if not editing_item else "Atualizar Vigência"
            submit_button = st.form_submit_button(submit_button_label)

            if editing_item:
                if st.form_submit_button("Cancelar Edição"):
                    st.session_state.editing_sm_item = None
                    st.rerun()

            if submit_button:
                if not data_inicio_vigencia or valor_nacional <= 0:
                    st.error("Data Início Vigência e Valor Nacional são obrigatórios e o valor nacional deve ser positivo.")
                elif data_fim_especificada and data_fim_vigencia_input_val and data_fim_vigencia_input_val < data_inicio_vigencia:
                    st.error("Data Fim Vigência não pode ser anterior à Data Início Vigência.")
                else:
                    payload = {
                        "data_inicio_vigencia": data_inicio_vigencia.isoformat(),
                        "data_fim_vigencia": data_fim_vigencia_input_val.isoformat() if data_fim_vigencia_input_val and data_fim_especificada else None,
                        "valor_nacional": valor_nacional,
                        "observacao": observacao if observacao else None,
                        "valores_regionais": {}
                    }

                    parsed_regionais_ok = True
                    if valores_regionais_json:
                        try:
                            parsed_regionais = json.loads(valores_regionais_json)
                            if not isinstance(parsed_regionais, dict):
                                st.error('Valores Regionais: Formato JSON inválido. Deve ser um objeto, ex: {\"SP\": 1640.00}.')
                                parsed_regionais_ok = False
                            else:
                                payload["valores_regionais"] = parsed_regionais
                        except json.JSONDecodeError:
                            st.error('Valores Regionais: Formato JSON inválido.')
                            parsed_regionais_ok = False
                    
                    if parsed_regionais_ok:
                        if editing_item:
                            if update_sm_entry(str(editing_item['id_versao']), payload):
                                st.rerun()
                        else:
                            if create_sm_entry(payload):
                                st.rerun()

    with col_view:
        st.subheader("Histórico de Salário Mínimo")
        sm_data = fetch_sm_data()
        if sm_data:
            df_sm = pd.DataFrame(sm_data)
            if df_sm.empty:
                st.info("Nenhum histórico de Salário Mínimo encontrado.")
                return

            df_sm_display = df_sm.copy()
            date_cols_to_format = ['data_inicio_vigencia', 'data_fim_vigencia', 'data_cadastro', 'data_atualizacao']
            for col_name in date_cols_to_format:
                if col_name in df_sm_display.columns:
                    # Converte para datetime, tratando erros e NaT
                    df_sm_display[col_name] = pd.to_datetime(df_sm_display[col_name], errors='coerce')
                    
                    # Formata as datas, tratando NaT explicitamente
                    if col_name == 'data_fim_vigencia':
                        df_sm_display[col_name] = df_sm_display[col_name].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else "Aberta")
                    elif col_name in ['data_cadastro', 'data_atualizacao']:
                        df_sm_display[col_name] = df_sm_display[col_name].apply(lambda x: x.strftime('%d/%m/%Y %H:%M') if pd.notna(x) else "-")
                    else: # data_inicio_vigencia
                        df_sm_display[col_name] = df_sm_display[col_name].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else "-")

            if 'valores_regionais' in df_sm_display.columns:
                df_sm_display['valores_regionais_str'] = df_sm_display['valores_regionais'].apply(
                    lambda x: json.dumps(x, ensure_ascii=False, indent=1) if isinstance(x, dict) and x else "-"
                )

            header_cols_list = st.columns([1, 2, 2, 2, 2, 3, 1, 1])
            column_names = ["ID", "Início Vig.", "Fim Vig.", "Valor (R$)", "Regionais", "Obs.", "Editar", "Inativar"]
            for h_col, name in zip(header_cols_list, column_names):
                h_col.markdown(f"**{name}**")

            st.markdown("---")

            for index_val in df_sm.index: 
                row_data_series = df_sm.loc[index_val] 
                display_row_series = df_sm_display.loc[index_val]
                item_id_str = str(row_data_series['id_versao'])

                row_cols_list = st.columns([1, 2, 2, 2, 2, 3, 1, 1])
                row_cols_list[0].text(display_row_series.get('id_versao', 'N/A'))
                row_cols_list[1].text(display_row_series.get('data_inicio_vigencia', 'N/A'))
                row_cols_list[2].text(display_row_series.get('data_fim_vigencia', 'Aberta'))
                
                valor_nacional_display = display_row_series.get('valor_nacional')
                row_cols_list[3].text(f"{valor_nacional_display:.2f}" if pd.notna(valor_nacional_display) else "-")

                valores_regionais_str_display = display_row_series.get('valores_regionais_str', '-')
                if valores_regionais_str_display != '-' and len(valores_regionais_str_display) > 25: # Limite para expander
                    with row_cols_list[4].expander("Ver JSON"):
                        st.json(row_data_series.get('valores_regionais', {}))
                else:
                    row_cols_list[4].text(valores_regionais_str_display)

                observacao_text_display = str(display_row_series.get('observacao', '') or "-") # Garante string e default
                if len(observacao_text_display) > 30: # Limite para expander
                     with row_cols_list[5].expander("Ver Obs."):
                        st.markdown(observacao_text_display)
                else:
                    row_cols_list[5].text(observacao_text_display)

                if row_cols_list[6].button("✏️", key=f"edit_sm_{item_id_str}", help="Editar esta vigência"):
                    st.session_state.editing_sm_item = row_data_series.to_dict()
                    st.session_state.item_id_para_deletar_sm = None
                    st.rerun()

                if row_cols_list[7].button("🗑️", key=f"delete_sm_{item_id_str}", help="Inativar esta vigência"):
                    st.session_state.item_id_para_deletar_sm = item_id_str
                    st.session_state.editing_sm_item = None
                    st.rerun()
                st.markdown("---")
        else:
            st.info("Nenhum histórico de Salário Mínimo encontrado ou erro ao carregar.")

def mostrar_pagina_fgts():
    st.header("📊 Gestão de Parâmetros do FGTS")

    if 'editing_fgts_item' not in st.session_state:
        st.session_state.editing_fgts_item = None
    if 'item_id_para_deletar_fgts' not in st.session_state:
        st.session_state.item_id_para_deletar_fgts = None

    # Funções auxiliares para interagir com a API de FGTS
    @st.cache_data(ttl=60)
    def fetch_fgts_data():
        try:
            response = requests.get(f"{API_BASE_URL}/param-legais/fgts/?skip=0&limit=1000")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.error(f"Erro ao buscar dados de FGTS: {e}")
            return []
        except json.JSONDecodeError:
            st.error("Erro ao decodificar resposta da API de FGTS.")
            return []

    def create_fgts_entry(payload):
        try:
            response = requests.post(f"{API_BASE_URL}/param-legais/fgts/", json=payload)
            response.raise_for_status()
            st.success("Nova vigência de FGTS criada com sucesso!")
            st.cache_data.clear()
            return response.json()
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao criar FGTS ({e.response.status_code}): {detail}")
            return None
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao criar FGTS: {e}")
            return None

    def update_fgts_entry(id_versao: str, payload):
        try:
            response = requests.put(f"{API_BASE_URL}/param-legais/fgts/{id_versao}", json=payload)
            response.raise_for_status()
            st.success(f"Vigência de FGTS {id_versao} atualizada com sucesso!")
            st.cache_data.clear()
            st.session_state.editing_fgts_item = None
            return response.json()
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao atualizar FGTS {id_versao} ({e.response.status_code}): {detail}")
            return None
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao atualizar FGTS {id_versao}: {e}")
            return None

    def delete_fgts_entry(id_versao: str):
        try:
            response = requests.delete(f"{API_BASE_URL}/param-legais/fgts/{id_versao}")
            response.raise_for_status()
            st.success(f"Vigência de FGTS {id_versao} inativada com sucesso!")
            st.cache_data.clear()
            return True
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao inativar FGTS {id_versao} ({e.response.status_code}): {detail}")
            return False
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao inativar FGTS {id_versao}: {e}")
            return False

    if st.session_state.get('item_id_para_deletar_fgts'):
        item_id_to_delete_fgts = str(st.session_state.item_id_para_deletar_fgts)
        st.warning(f"Tem certeza que deseja inativar a vigência de FGTS com ID {item_id_to_delete_fgts}?")
        col1_del, col2_del, _ = st.columns([1,1,5])
        with col1_del:
            if st.button("Sim, Inativar", key=f"confirm_delete_fgts_{item_id_to_delete_fgts}"):
                if delete_fgts_entry(item_id_to_delete_fgts):
                    st.session_state.item_id_para_deletar_fgts = None
                    st.rerun()
        with col2_del:
            if st.button("Cancelar", key=f"cancel_delete_fgts_{item_id_to_delete_fgts}"):
                st.session_state.item_id_para_deletar_fgts = None
                st.rerun()
        return

    # Layout da página
    col_form_fgts, col_view_fgts = st.columns([1, 2])

    with col_form_fgts:
        editing_fgts_item_data = st.session_state.get('editing_fgts_item')
        form_title_fgts = "Adicionar Nova Vigência de FGTS" if not editing_fgts_item_data else f"Editando Vigência FGTS ID: {editing_fgts_item_data.get('id_versao', 'Desconhecido')}"
        st.subheader(form_title_fgts)

        form_key_suffix_fgts = f"_edit_{editing_fgts_item_data['id_versao']}" if editing_fgts_item_data and editing_fgts_item_data.get('id_versao') else "_new"

        default_data_inicio_fgts = date.today()
        default_data_fim_val_fgts = None
        default_data_fim_chk_fgts = False
        default_aliquota_mensal = 8.0
        default_aliquota_multa = 40.0
        default_observacao_fgts = ""

        if editing_fgts_item_data:
            raw_data_inicio_fgts = editing_fgts_item_data.get('data_inicio_vigencia')
            if raw_data_inicio_fgts:
                try:
                    dt_obj_fgts = pd.to_datetime(raw_data_inicio_fgts)
                    if pd.notna(dt_obj_fgts): default_data_inicio_fgts = dt_obj_fgts.date()
                except Exception as e: print(f"Erro parse data_inicio_vigencia FGTS: {e}")

            raw_data_fim_fgts = editing_fgts_item_data.get('data_fim_vigencia')
            if raw_data_fim_fgts:
                try:
                    dt_obj_fim_fgts = pd.to_datetime(raw_data_fim_fgts)
                    if pd.notna(dt_obj_fim_fgts):
                        default_data_fim_val_fgts = dt_obj_fim_fgts.date()
                        default_data_fim_chk_fgts = True
                except Exception as e: print(f"Erro parse data_fim_vigencia FGTS: {e}")
            
            try:
                default_aliquota_mensal = float(editing_fgts_item_data.get('aliquota_mensal', 8.0))
            except (ValueError, TypeError) as e_parse_al_mensal:
                print(f"Erro ao parsear aliquota_mensal FGTS: {editing_fgts_item_data.get('aliquota_mensal')}, Erro: {e_parse_al_mensal}")
                # Mantém o default se a conversão falhar
            
            try:
                default_aliquota_multa = float(editing_fgts_item_data.get('aliquota_multa_rescisoria', 40.0))
            except (ValueError, TypeError) as e_parse_al_multa:
                print(f"Erro ao parsear aliquota_multa_rescisoria FGTS: {editing_fgts_item_data.get('aliquota_multa_rescisoria')}, Erro: {e_parse_al_multa}")
                # Mantém o default se a conversão falhar

            default_observacao_fgts = str(editing_fgts_item_data.get('observacao', ""))

        with st.form("fgts_add_edit_form" + form_key_suffix_fgts, clear_on_submit=(not editing_fgts_item_data)):
            data_inicio_vigencia_fgts = st.date_input("Data Início Vigência*", value=default_data_inicio_fgts, key="fgts_div" + form_key_suffix_fgts, help="Data de início da validade destes parâmetros.")
            
            col_fim_chk_fgts, col_fim_date_fgts = st.columns([1,2])
            with col_fim_chk_fgts:
                data_fim_especificada_fgts = st.checkbox("Definir Data Fim?", value=default_data_fim_chk_fgts, key="fgts_dfv_chk" + form_key_suffix_fgts)
            
            data_fim_vigencia_fgts_input_val = None
            if data_fim_especificada_fgts:
                with col_fim_date_fgts:
                    current_fim_val_fgts = default_data_fim_val_fgts
                    min_date_for_fim_fgts = data_inicio_vigencia_fgts
                    if default_data_fim_val_fgts and data_inicio_vigencia_fgts and default_data_fim_val_fgts < data_inicio_vigencia_fgts:
                        current_fim_val_fgts = data_inicio_vigencia_fgts
                    data_fim_vigencia_fgts_input_val = st.date_input("Data Fim Vigência", value=current_fim_val_fgts, min_value=min_date_for_fim_fgts, key="fgts_dfv_date" + form_key_suffix_fgts, help="Opcional. Se não definida, a vigência é considerada aberta.")

            aliquota_mensal = st.number_input("Alíquota Mensal (%)*", min_value=0.0, max_value=100.0, value=default_aliquota_mensal, format="%.2f", step=0.1, key="fgts_am" + form_key_suffix_fgts, help="Ex: 8.0 para 8%")
            aliquota_multa_rescisoria = st.number_input("Alíquota Multa Rescisória (%)*", min_value=0.0, max_value=100.0, value=default_aliquota_multa, format="%.2f", step=0.1, key="fgts_amr" + form_key_suffix_fgts, help="Ex: 40.0 para 40%")
            observacao_fgts = st.text_area("Observação", value=default_observacao_fgts, key="fgts_obs" + form_key_suffix_fgts)
            
            submit_button_label_fgts = "Salvar Nova Vigência" if not editing_fgts_item_data else "Atualizar Vigência"
            submit_button_fgts = st.form_submit_button(submit_button_label_fgts)

            if editing_fgts_item_data:
                if st.form_submit_button("Cancelar Edição"):
                    st.session_state.editing_fgts_item = None
                    st.rerun()

            if submit_button_fgts:
                if not data_inicio_vigencia_fgts or aliquota_mensal <= 0 or aliquota_multa_rescisoria <=0:
                    st.error("Data Início Vigência, Alíquota Mensal e Alíquota Multa Rescisória são obrigatórios e devem ser positivos.")
                elif data_fim_especificada_fgts and data_fim_vigencia_fgts_input_val and data_fim_vigencia_fgts_input_val < data_inicio_vigencia_fgts:
                     st.error("Data Fim Vigência não pode ser anterior à Data Início Vigência.")
                else:
                    payload_fgts = {
                        "data_inicio_vigencia": data_inicio_vigencia_fgts.isoformat(),
                        "data_fim_vigencia": data_fim_vigencia_fgts_input_val.isoformat() if data_fim_vigencia_fgts_input_val and data_fim_especificada_fgts else None,
                        "aliquota_mensal": aliquota_mensal,
                        "aliquota_multa_rescisoria": aliquota_multa_rescisoria,
                        "observacao": observacao_fgts if observacao_fgts else None
                    }
                    try: # Adicionado try para o bloco de create/update
                        if editing_fgts_item_data:
                            if update_fgts_entry(str(editing_fgts_item_data['id_versao']), payload_fgts):
                                st.rerun()
                        else:
                            if create_fgts_entry(payload_fgts):
                                st.rerun()
                    except Exception as e_submit: # Adicionado except para capturar exceções
                        st.error(f"Erro ao submeter o formulário FGTS: {e_submit}")
    
    with col_view_fgts:
        st.subheader("Histórico de Parâmetros do FGTS")
        fgts_data = fetch_fgts_data()
        if fgts_data:
            df_fgts = pd.DataFrame(fgts_data)
            if df_fgts.empty:
                st.info("Nenhum histórico de FGTS encontrado.")
                return

            df_fgts_display = df_fgts.copy()
            date_cols_to_format_fgts = ['data_inicio_vigencia', 'data_fim_vigencia', 'data_cadastro', 'data_atualizacao']
            for col_name_fgts in date_cols_to_format_fgts:
                if col_name_fgts in df_fgts_display.columns:
                    df_fgts_display[col_name_fgts] = pd.to_datetime(df_fgts_display[col_name_fgts], errors='coerce')
                    if col_name_fgts == 'data_fim_vigencia':
                        df_fgts_display[col_name_fgts] = df_fgts_display[col_name_fgts].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else "Aberta")
                    elif col_name_fgts in ['data_cadastro', 'data_atualizacao']:
                        df_fgts_display[col_name_fgts] = df_fgts_display[col_name_fgts].apply(lambda x: x.strftime('%d/%m/%Y %H:%M') if pd.notna(x) else "-")
                    else: # data_inicio_vigencia
                        df_fgts_display[col_name_fgts] = df_fgts_display[col_name_fgts].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else "-")
            
            header_cols_fgts = st.columns([1, 2, 2, 2, 2, 2, 1, 1]) # Ajustado para novas colunas
            column_names_fgts = ["ID", "Início Vig.", "Fim Vig.", "Alíq. Mensal (%)", "Alíq. Multa (%)", "Obs.", "Editar", "Inativar"]
            for h_col, name in zip(header_cols_fgts, column_names_fgts):
                h_col.markdown(f"**{name}**")
            st.markdown("---")

            for index_val_fgts in df_fgts.index:
                row_data_series_fgts = df_fgts.loc[index_val_fgts]
                display_row_series_fgts = df_fgts_display.loc[index_val_fgts]
                item_id_str_fgts = str(row_data_series_fgts['id_versao'])

                row_cols_list_fgts = st.columns([1, 2, 2, 2, 2, 2, 1, 1])
                row_cols_list_fgts[0].text(display_row_series_fgts.get('id_versao', 'N/A'))
                row_cols_list_fgts[1].text(display_row_series_fgts.get('data_inicio_vigencia', 'N/A'))
                row_cols_list_fgts[2].text(display_row_series_fgts.get('data_fim_vigencia', 'Aberta'))
                
                al_mensal_disp = display_row_series_fgts.get('aliquota_mensal')
                row_cols_list_fgts[3].text(f"{al_mensal_disp:.2f}" if pd.notna(al_mensal_disp) else "-")
                
                al_multa_disp = display_row_series_fgts.get('aliquota_multa_rescisoria')
                row_cols_list_fgts[4].text(f"{al_multa_disp:.2f}" if pd.notna(al_multa_disp) else "-")

                obs_text_fgts = str(display_row_series_fgts.get('observacao', '') or "-")
                if len(obs_text_fgts) > 25:
                    with row_cols_list_fgts[5].expander("Ver Obs."):
                        st.markdown(obs_text_fgts)
                else:
                    row_cols_list_fgts[5].text(obs_text_fgts)

                if row_cols_list_fgts[6].button("✏️", key=f"edit_fgts_{item_id_str_fgts}", help="Editar esta vigência"):
                    st.session_state.editing_fgts_item = row_data_series_fgts.to_dict()
                    st.session_state.item_id_para_deletar_fgts = None
                    st.rerun()

                if row_cols_list_fgts[7].button("🗑️", key=f"delete_fgts_{item_id_str_fgts}", help="Inativar esta vigência"):
                    st.session_state.item_id_para_deletar_fgts = item_id_str_fgts
                    st.session_state.editing_fgts_item = None
                    st.rerun()
                st.markdown("---")
        else:
            st.info("Nenhum histórico de FGTS encontrado ou erro ao carregar.")

def mostrar_pagina_inss():
    st.header("📄 Gestão de Tabelas INSS")

    if 'editing_inss_item' not in st.session_state:
        st.session_state.editing_inss_item = None
    if 'item_id_para_deletar_inss' not in st.session_state:
        st.session_state.item_id_para_deletar_inss = None

    # Funções auxiliares para interagir com a API de INSS
    @st.cache_data(ttl=60)
    def fetch_inss_data():
        try:
            response = requests.get(f"{API_BASE_URL}/param-legais/inss/?skip=0&limit=1000")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.error(f"Erro ao buscar dados de INSS: {e}")
            return []
        except json.JSONDecodeError:
            st.error("Erro ao decodificar resposta da API de INSS.")
            return []

    def create_inss_entry(payload):
        try:
            response = requests.post(f"{API_BASE_URL}/param-legais/inss/", json=payload)
            response.raise_for_status()
            st.success("Nova tabela INSS criada com sucesso!")
            st.cache_data.clear()
            return response.json()
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao criar tabela INSS ({e.response.status_code}): {detail}")
            return None
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao criar tabela INSS: {e}")
            return None

    def update_inss_entry(id_versao: str, payload):
        try:
            response = requests.put(f"{API_BASE_URL}/param-legais/inss/{id_versao}", json=payload)
            response.raise_for_status()
            st.success(f"Tabela INSS {id_versao} atualizada com sucesso!")
            st.cache_data.clear()
            st.session_state.editing_inss_item = None
            return response.json()
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao atualizar tabela INSS {id_versao} ({e.response.status_code}): {detail}")
            return None
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao atualizar tabela INSS {id_versao}: {e}")
            return None

    def delete_inss_entry(id_versao: str):
        try:
            response = requests.delete(f"{API_BASE_URL}/param-legais/inss/{id_versao}")
            response.raise_for_status()
            st.success(f"Tabela INSS {id_versao} inativada com sucesso!")
            st.cache_data.clear()
            return True
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao inativar tabela INSS {id_versao} ({e.response.status_code}): {detail}")
            return False
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao inativar tabela INSS {id_versao}: {e}")
            return False

    if st.session_state.get('item_id_para_deletar_inss'):
        item_id_to_delete_inss = str(st.session_state.item_id_para_deletar_inss)
        st.warning(f"Tem certeza que deseja inativar a tabela INSS com ID {item_id_to_delete_inss}?")
        col1_del, col2_del, _ = st.columns([1,1,5])
        with col1_del:
            if st.button("Sim, Inativar", key=f"confirm_delete_inss_{item_id_to_delete_inss}"):
                if delete_inss_entry(item_id_to_delete_inss):
                    st.session_state.item_id_para_deletar_inss = None
                    st.rerun()
        with col2_del:
            if st.button("Cancelar", key=f"cancel_delete_inss_{item_id_to_delete_inss}"):
                st.session_state.item_id_para_deletar_inss = None
                st.rerun()
        return

    # Layout da página
    col_form_inss, col_view_inss = st.columns([1, 2])

    with col_form_inss:
        editing_inss_item_data = st.session_state.get('editing_inss_item')
        form_title_inss = "Adicionar Nova Vigência de Tabela INSS" if not editing_inss_item_data else f"Editando Tabela INSS ID: {editing_inss_item_data.get('id_versao', 'Desconhecido')}"
        st.subheader(form_title_inss)

        form_key_suffix_inss = f"_edit_{editing_inss_item_data['id_versao']}" if editing_inss_item_data and editing_inss_item_data.get('id_versao') else "_new"

        default_data_inicio_inss = date.today()
        default_data_fim_val_inss = None
        default_data_fim_chk_inss = False
        default_faixas_inss_str = ""
        default_valor_teto_inss = 0.0
        default_observacao_inss = ""

        if editing_inss_item_data:
            raw_data_inicio_inss = editing_inss_item_data.get('data_inicio_vigencia')
            if raw_data_inicio_inss:
                try:
                    dt_obj_inss = pd.to_datetime(raw_data_inicio_inss)
                    if pd.notna(dt_obj_inss): default_data_inicio_inss = dt_obj_inss.date()
                except Exception as e: print(f"Erro parse data_inicio_vigencia INSS: {e}")

            raw_data_fim_inss = editing_inss_item_data.get('data_fim_vigencia')
            if raw_data_fim_inss:
                try:
                    dt_obj_fim_inss = pd.to_datetime(raw_data_fim_inss)
                    if pd.notna(dt_obj_fim_inss):
                        default_data_fim_val_inss = dt_obj_fim_inss.date()
                        default_data_fim_chk_inss = True
                except Exception as e: print(f"Erro parse data_fim_vigencia INSS: {e}")
            
            raw_faixas_inss = editing_inss_item_data.get('faixas')
            if raw_faixas_inss:
                try:
                    if isinstance(raw_faixas_inss, list):
                        default_faixas_inss_str = json.dumps(raw_faixas_inss, ensure_ascii=False, indent=2)
                    elif isinstance(raw_faixas_inss, str):
                        try:
                            parsed_json = json.loads(raw_faixas_inss)
                            default_faixas_inss_str = json.dumps(parsed_json, ensure_ascii=False, indent=2)
                        except json.JSONDecodeError:
                            default_faixas_inss_str = raw_faixas_inss
                    else:
                        default_faixas_inss_str = str(raw_faixas_inss)
                except Exception as e: 
                    print(f"Erro ao processar faixas INSS: {raw_faixas_inss}, Erro: {e}")
                    default_faixas_inss_str = str(raw_faixas_inss)

            raw_valor_teto_inss = editing_inss_item_data.get('valor_teto_contribuicao')
            if raw_valor_teto_inss is not None:
                try:
                    default_valor_teto_inss = float(raw_valor_teto_inss)
                except (ValueError, TypeError) as e: 
                    print(f"Erro ao parsear valor_teto_contribuicao INSS: {raw_valor_teto_inss}, Erro: {e}")

            default_observacao_inss = str(editing_inss_item_data.get('observacao', ""))

        with st.form("inss_add_edit_form" + form_key_suffix_inss, clear_on_submit=(not editing_inss_item_data)):
            data_inicio_vigencia_inss = st.date_input("Data Início Vigência*", value=default_data_inicio_inss, key="inss_div" + form_key_suffix_inss, help="Data de início da validade desta tabela.")
            
            col_fim_chk_inss, col_fim_date_inss = st.columns([1,2])
            with col_fim_chk_inss:
                data_fim_especificada_inss = st.checkbox("Definir Data Fim?", value=default_data_fim_chk_inss, key="inss_dfv_chk" + form_key_suffix_inss)
            
            data_fim_vigencia_inss_input_val = None
            if data_fim_especificada_inss:
                with col_fim_date_inss:
                    current_fim_val_inss = default_data_fim_val_inss
                    min_date_for_fim_inss = data_inicio_vigencia_inss
                    if default_data_fim_val_inss and data_inicio_vigencia_inss and default_data_fim_val_inss < data_inicio_vigencia_inss:
                        current_fim_val_inss = data_inicio_vigencia_inss
                    data_fim_vigencia_inss_input_val = st.date_input("Data Fim Vigência", value=current_fim_val_inss, min_value=min_date_for_fim_inss, key="inss_dfv_date" + form_key_suffix_inss, help="Opcional. Se não definida, a vigência é considerada aberta.")

            faixas_inss_json = st.text_area("Faixas de Contribuição (JSON)*", value=default_faixas_inss_str, height=200, key="inss_faixas" + form_key_suffix_inss, 
                                            placeholder='''[{"valor_inicial": 0, "valor_final": 1412.00, "aliquota": 7.5}, ...]''',
                                            help="Lista de faixas. Ex: [{\"valor_inicial\": 0, \"valor_final\": 1412.00, \"aliquota\": 7.5}, {\"valor_inicial\": 1412.01, \"aliquota\": 9.0, \"valor_final\": 2666.68}] Valor final é opcional para a última faixa antes do teto.")
            
            valor_teto_contribuicao_inss = st.number_input("Valor Teto Contribuição (R$)", value=default_valor_teto_inss, min_value=0.0, format="%.2f", step=0.01, key="inss_teto" + form_key_suffix_inss, help="Opcional. Valor máximo para base de cálculo do INSS.")
            observacao_inss = st.text_area("Observação", value=default_observacao_inss, key="inss_obs" + form_key_suffix_inss)
            
            submit_button_label_inss = "Salvar Nova Tabela" if not editing_inss_item_data else "Atualizar Tabela"
            submit_button_inss = st.form_submit_button(submit_button_label_inss)

            if editing_inss_item_data:
                if st.form_submit_button("Cancelar Edição"):
                    st.session_state.editing_inss_item = None
                    st.rerun()

            if submit_button_inss:
                if not data_inicio_vigencia_inss or not faixas_inss_json:
                    st.error("Data Início Vigência e Faixas de Contribuição são obrigatórios.")
                elif data_fim_especificada_inss and data_fim_vigencia_inss_input_val and data_fim_vigencia_inss_input_val < data_inicio_vigencia_inss:
                    st.error("Data Fim Vigência não pode ser anterior à Data Início Vigência.")
                else:
                    parsed_faixas_ok = True
                    parsed_faixas = []
                    if faixas_inss_json:
                        try:
                            parsed_faixas = json.loads(faixas_inss_json)
                            if not isinstance(parsed_faixas, list) or not all(isinstance(item, dict) for item in parsed_faixas):
                                st.error("Faixas de Contribuição: Formato JSON inválido. Deve ser uma lista de objetos.")
                                parsed_faixas_ok = False
                        except json.JSONDecodeError:
                            st.error("Faixas de Contribuição: Formato JSON inválido.")
                            parsed_faixas_ok = False
                    
                    if parsed_faixas_ok:
                        payload_inss = {
                            "data_inicio_vigencia": data_inicio_vigencia_inss.isoformat(),
                            "data_fim_vigencia": data_fim_vigencia_inss_input_val.isoformat() if data_fim_vigencia_inss_input_val and data_fim_especificada_inss else None,
                            "faixas": parsed_faixas,
                            "valor_teto_contribuicao": valor_teto_contribuicao_inss if valor_teto_contribuicao_inss > 0 else None,
                            "observacao": observacao_inss if observacao_inss else None
                        }
                        try:
                            if editing_inss_item_data:
                                if update_inss_entry(str(editing_inss_item_data['id_versao']), payload_inss):
                                    st.rerun()
                            else:
                                if create_inss_entry(payload_inss):
                                    st.rerun()
                        except Exception as e_submit:
                            st.error(f"Erro ao submeter o formulário INSS: {e_submit}")
    
    with col_view_inss:
        st.subheader("Histórico de Tabelas INSS")
        inss_data = fetch_inss_data()
        if inss_data:
            df_inss = pd.DataFrame(inss_data)
            if df_inss.empty:
                st.info("Nenhum histórico de INSS encontrado.")
                return

            df_inss_display = df_inss.copy()
            date_cols_to_format_inss = ['data_inicio_vigencia', 'data_fim_vigencia', 'data_cadastro', 'data_atualizacao']
            for col_name_inss in date_cols_to_format_inss:
                if col_name_inss in df_inss_display.columns:
                    df_inss_display[col_name_inss] = pd.to_datetime(df_inss_display[col_name_inss], errors='coerce')
                    if col_name_inss == 'data_fim_vigencia':
                        df_inss_display[col_name_inss] = df_inss_display[col_name_inss].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else "Aberta")
                    elif col_name_inss in ['data_cadastro', 'data_atualizacao']:
                        df_inss_display[col_name_inss] = df_inss_display[col_name_inss].apply(lambda x: x.strftime('%d/%m/%Y %H:%M') if pd.notna(x) else "-")
                    else: # data_inicio_vigencia
                        df_inss_display[col_name_inss] = df_inss_display[col_name_inss].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else "-")
            
            if 'faixas' in df_inss_display.columns:
                df_inss_display['faixas_str'] = df_inss_display['faixas'].apply(
                    lambda x: json.dumps(x, ensure_ascii=False, indent=1) if isinstance(x, list) and x else "-"
                )
            if 'valor_teto_contribuicao' in df_inss_display.columns:
                 df_inss_display['valor_teto_contribuicao_fmt'] = df_inss_display['valor_teto_contribuicao'].apply(lambda x: f"R$ {x:.2f}" if pd.notna(x) else "-")


            header_cols_inss = st.columns([1, 2, 2, 3, 2, 2, 1, 1]) 
            column_names_inss = ["ID", "Início Vig.", "Fim Vig.", "Faixas", "Teto Contrib.", "Obs.", "Editar", "Inativar"]
            for h_col, name in zip(header_cols_inss, column_names_inss):
                h_col.markdown(f"**{name}**")
            st.markdown("---")

            for index_val_inss in df_inss.index:
                row_data_series_inss = df_inss.loc[index_val_inss]
                display_row_series_inss = df_inss_display.loc[index_val_inss]
                item_id_str_inss = str(row_data_series_inss['id_versao'])

                row_cols_list_inss = st.columns([1, 2, 2, 3, 2, 2, 1, 1])
                row_cols_list_inss[0].text(display_row_series_inss.get('id_versao', 'N/A'))
                row_cols_list_inss[1].text(display_row_series_inss.get('data_inicio_vigencia', 'N/A'))
                row_cols_list_inss[2].text(display_row_series_inss.get('data_fim_vigencia', 'Aberta'))
                
                faixas_str_display_inss = display_row_series_inss.get('faixas_str', '-')
                if faixas_str_display_inss != '-' and len(faixas_str_display_inss) > 30:
                    with row_cols_list_inss[3].expander("Ver Faixas"):
                        st.json(row_data_series_inss.get('faixas', []))
                else:
                    row_cols_list_inss[3].text(faixas_str_display_inss)

                row_cols_list_inss[4].text(display_row_series_inss.get('valor_teto_contribuicao_fmt', '-'))

                obs_text_inss = str(display_row_series_inss.get('observacao', '') or "-")
                if len(obs_text_inss) > 25:
                    with row_cols_list_inss[5].expander("Ver Obs."):
                        st.markdown(obs_text_inss)
                else:
                    row_cols_list_inss[5].text(obs_text_inss)

                if row_cols_list_inss[6].button("✏️", key=f"edit_inss_{item_id_str_inss}", help="Editar esta tabela"):
                    st.session_state.editing_inss_item = row_data_series_inss.to_dict()
                    st.session_state.item_id_para_deletar_inss = None
                    st.rerun()

                if row_cols_list_inss[7].button("🗑️", key=f"delete_inss_{item_id_str_inss}", help="Inativar esta tabela"):
                    st.session_state.item_id_para_deletar_inss = item_id_str_inss
                    st.session_state.editing_inss_item = None
                    st.rerun()
                st.markdown("---")
        else:
            st.info("Nenhum histórico de INSS encontrado ou erro ao carregar.")

def mostrar_pagina_irrf():
    st.header("💸 Gestão de Tabelas IRRF")

    if 'editing_irrf_item' not in st.session_state:
        st.session_state.editing_irrf_item = None
    if 'item_id_para_deletar_irrf' not in st.session_state:
        st.session_state.item_id_para_deletar_irrf = None

    # Funções auxiliares para interagir com a API de IRRF
    @st.cache_data(ttl=60)
    def fetch_irrf_data():
        try:
            response = requests.get(f"{API_BASE_URL}/param-legais/irrf/?skip=0&limit=1000")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.error(f"Erro ao buscar dados de IRRF: {e}")
            return []
        except json.JSONDecodeError:
            st.error("Erro ao decodificar resposta da API de IRRF.")
            return []

    def create_irrf_entry(payload):
        try:
            response = requests.post(f"{API_BASE_URL}/param-legais/irrf/", json=payload)
            response.raise_for_status()
            st.success("Nova tabela IRRF criada com sucesso!")
            st.cache_data.clear()
            return response.json()
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao criar tabela IRRF ({e.response.status_code}): {detail}")
            return None
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao criar tabela IRRF: {e}")
            return None

    def update_irrf_entry(id_versao: str, payload):
        try:
            response = requests.put(f"{API_BASE_URL}/param-legais/irrf/{id_versao}", json=payload)
            response.raise_for_status()
            st.success(f"Tabela IRRF {id_versao} atualizada com sucesso!")
            st.cache_data.clear()
            st.session_state.editing_irrf_item = None
            return response.json()
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao atualizar tabela IRRF {id_versao} ({e.response.status_code}): {detail}")
            return None
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao atualizar tabela IRRF {id_versao}: {e}")
            return None

    def delete_irrf_entry(id_versao: str):
        try:
            response = requests.delete(f"{API_BASE_URL}/param-legais/irrf/{id_versao}")
            response.raise_for_status()
            st.success(f"Tabela IRRF {id_versao} inativada com sucesso!")
            st.cache_data.clear()
            return True
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao inativar tabela IRRF {id_versao} ({e.response.status_code}): {detail}")
            return False
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao inativar tabela IRRF {id_versao}: {e}")
            return False

    if st.session_state.get('item_id_para_deletar_irrf'):
        item_id_to_delete_irrf = str(st.session_state.item_id_para_deletar_irrf)
        st.warning(f"Tem certeza que deseja inativar a tabela IRRF com ID {item_id_to_delete_irrf}?")
        col1_del, col2_del, _ = st.columns([1,1,5])
        with col1_del:
            if st.button("Sim, Inativar", key=f"confirm_delete_irrf_{item_id_to_delete_irrf}"):
                if delete_irrf_entry(item_id_to_delete_irrf):
                    st.session_state.item_id_para_deletar_irrf = None
                    st.rerun()
        with col2_del:
            if st.button("Cancelar", key=f"cancel_delete_irrf_{item_id_to_delete_irrf}"):
                st.session_state.item_id_para_deletar_irrf = None
                st.rerun()
        return

    # Layout da página
    col_form_irrf, col_view_irrf = st.columns([1, 2])

    with col_form_irrf:
        editing_irrf_item_data = st.session_state.get('editing_irrf_item')
        form_title_irrf = "Adicionar Nova Vigência de Tabela IRRF" if not editing_irrf_item_data else f"Editando Tabela IRRF ID: {editing_irrf_item_data.get('id_versao', 'Desconhecido')}"
        st.subheader(form_title_irrf)

        form_key_suffix_irrf = f"_edit_{editing_irrf_item_data['id_versao']}" if editing_irrf_item_data and editing_irrf_item_data.get('id_versao') else "_new"

        default_data_inicio_irrf = date.today()
        default_data_fim_val_irrf = None
        default_data_fim_chk_irrf = False
        default_faixas_irrf_str = ""
        default_deducao_dependente_irrf = 0.0
        default_limite_desconto_simplificado_irrf = 0.0
        default_observacao_irrf = ""

        if editing_irrf_item_data:
            raw_data_inicio_irrf = editing_irrf_item_data.get('data_inicio_vigencia')
            if raw_data_inicio_irrf:
                try:
                    dt_obj_irrf = pd.to_datetime(raw_data_inicio_irrf)
                    if pd.notna(dt_obj_irrf): default_data_inicio_irrf = dt_obj_irrf.date()
                except Exception as e: print(f"Erro parse data_inicio_vigencia IRRF: {e}")

            raw_data_fim_irrf = editing_irrf_item_data.get('data_fim_vigencia')
            if raw_data_fim_irrf:
                try:
                    dt_obj_fim_irrf = pd.to_datetime(raw_data_fim_irrf)
                    if pd.notna(dt_obj_fim_irrf):
                        default_data_fim_val_irrf = dt_obj_fim_irrf.date()
                        default_data_fim_chk_irrf = True
                except Exception as e: print(f"Erro parse data_fim_vigencia IRRF: {e}")
            
            raw_faixas_irrf = editing_irrf_item_data.get('faixas')
            if raw_faixas_irrf:
                try:
                    if isinstance(raw_faixas_irrf, list):
                        default_faixas_irrf_str = json.dumps(raw_faixas_irrf, ensure_ascii=False, indent=2)
                    elif isinstance(raw_faixas_irrf, str):
                        try:
                            parsed_json = json.loads(raw_faixas_irrf)
                            default_faixas_irrf_str = json.dumps(parsed_json, ensure_ascii=False, indent=2)
                        except json.JSONDecodeError:
                            default_faixas_irrf_str = raw_faixas_irrf
                    else:
                        default_faixas_irrf_str = str(raw_faixas_irrf)
                except Exception as e: 
                    print(f"Erro ao processar faixas IRRF: {raw_faixas_irrf}, Erro: {e}")
                    default_faixas_irrf_str = str(raw_faixas_irrf)

            raw_deducao_dependente = editing_irrf_item_data.get('deducao_por_dependente')
            if raw_deducao_dependente is not None:
                try:
                    default_deducao_dependente_irrf = float(raw_deducao_dependente)
                except (ValueError, TypeError) as e: 
                    print(f"Erro ao parsear deducao_por_dependente IRRF: {raw_deducao_dependente}, Erro: {e}")

            raw_limite_desconto = editing_irrf_item_data.get('limite_desconto_simplificado')
            if raw_limite_desconto is not None:
                try:
                    default_limite_desconto_simplificado_irrf = float(raw_limite_desconto)
                except (ValueError, TypeError) as e:
                    print(f"Erro ao parsear limite_desconto_simplificado IRRF: {raw_limite_desconto}, Erro: {e}")
            
            default_observacao_irrf = str(editing_irrf_item_data.get('observacao', ""))

        with st.form("irrf_add_edit_form" + form_key_suffix_irrf, clear_on_submit=(not editing_irrf_item_data)):
            data_inicio_vigencia_irrf = st.date_input("Data Início Vigência*", value=default_data_inicio_irrf, key="irrf_div" + form_key_suffix_irrf, help="Data de início da validade desta tabela.")
            
            col_fim_chk_irrf, col_fim_date_irrf = st.columns([1,2])
            with col_fim_chk_irrf:
                data_fim_especificada_irrf = st.checkbox("Definir Data Fim?", value=default_data_fim_chk_irrf, key="irrf_dfv_chk" + form_key_suffix_irrf)
            
            data_fim_vigencia_irrf_input_val = None
            if data_fim_especificada_irrf:
                with col_fim_date_irrf:
                    current_fim_val_irrf = default_data_fim_val_irrf
                    min_date_for_fim_irrf = data_inicio_vigencia_irrf
                    if default_data_fim_val_irrf and data_inicio_vigencia_irrf and default_data_fim_val_irrf < data_inicio_vigencia_irrf:
                        current_fim_val_irrf = data_inicio_vigencia_irrf
                    data_fim_vigencia_irrf_input_val = st.date_input("Data Fim Vigência", value=current_fim_val_irrf, min_value=min_date_for_fim_irrf, key="irrf_dfv_date" + form_key_suffix_irrf, help="Opcional. Se não definida, a vigência é considerada aberta.")

            faixas_irrf_json = st.text_area("Faixas de Contribuição (JSON)*", value=default_faixas_irrf_str, height=200, key="irrf_faixas" + form_key_suffix_irrf, 
                                            placeholder='''[{"valor_inicial": 0, "valor_final": 2259.20, "aliquota": 0, "parcela_deduzir": 0}, ...]''',
                                            help="Lista de faixas. Ex: [{\\"valor_inicial\\": 0, \\"valor_final\\": 2259.20, \\"aliquota\\": 0, \\"parcela_deduzir\\": 0}, ...]. Valor final é opcional para a última faixa.")
            
            deducao_por_dependente_irrf = st.number_input("Dedução por Dependente (R$)*", value=default_deducao_dependente_irrf, min_value=0.0, format="%.2f", step=0.01, key="irrf_deducao_dependente" + form_key_suffix_irrf)
            limite_desconto_simplificado_irrf = st.number_input("Limite Desconto Simplificado (R$)", value=default_limite_desconto_simplificado_irrf, min_value=0.0, format="%.2f", step=0.01, key="irrf_limite_simplificado" + form_key_suffix_irrf, help="Opcional. Valor do desconto simplificado mensal.")
            observacao_irrf = st.text_area("Observação", value=default_observacao_irrf, key="irrf_obs" + form_key_suffix_irrf)
            
            submit_button_label_irrf = "Salvar Nova Tabela" if not editing_irrf_item_data else "Atualizar Tabela"
            submit_button_irrf = st.form_submit_button(submit_button_label_irrf)

            if editing_irrf_item_data:
                if st.form_submit_button("Cancelar Edição"):
                    st.session_state.editing_irrf_item = None
                    st.rerun()

            if submit_button_irrf:
                if not data_inicio_vigencia_irrf or not faixas_irrf_json or deducao_por_dependente_irrf < 0:
                    st.error("Data Início Vigência, Faixas de Contribuição e Dedução por Dependente (não negativa) são obrigatórios.")
                elif data_fim_especificada_irrf and data_fim_vigencia_irrf_input_val and data_fim_vigencia_irrf_input_val < data_inicio_vigencia_irrf:
                    st.error("Data Fim Vigência não pode ser anterior à Data Início Vigência.")
                else:
                    parsed_faixas_ok_irrf = True
                    parsed_faixas_irrf = []
                    if faixas_irrf_json:
                        try:
                            parsed_faixas_irrf = json.loads(faixas_irrf_json)
                            if not isinstance(parsed_faixas_irrf, list) or not all(isinstance(item, dict) for item in parsed_faixas_irrf):
                                st.error("Faixas de Contribuição IRRF: Formato JSON inválido. Deve ser uma lista de objetos.")
                                parsed_faixas_ok_irrf = False
                        except json.JSONDecodeError:
                            st.error("Faixas de Contribuição IRRF: Formato JSON inválido.")
                            parsed_faixas_ok_irrf = False
                    
                    if parsed_faixas_ok_irrf:
                        payload_irrf = {

                            "data_inicio_vigencia": data_inicio_vigencia_irrf.isoformat(),
                            "data_fim_vigencia": data_fim_vigencia_irrf_input_val.isoformat() if data_fim_vigencia_irrf_input_val and data_fim_especificada_irrf else None,
                            "faixas": parsed_faixas_irrf,
                            "deducao_por_dependente": deducao_por_dependente_irrf,
                            "limite_desconto_simplificado": limite_desconto_simplificado_irrf if limite_desconto_simplificado_irrf > 0 else None,
                            "observacao": observacao_irrf if observacao_irrf else None
                        }
                        try:
                            if editing_irrf_item_data:
                                if update_irrf_entry(str(editing_irrf_item_data['id_versao']), payload_irrf):
                                    st.rerun()
                            else:
                                if create_irrf_entry(payload_irrf):
                                    st.rerun()
                        except Exception as e_submit:
                            st.error(f"Erro ao submeter o formulário IRRF: {e_submit}")
    
    with col_view_irrf:
        st.subheader("Histórico de Tabelas IRRF")
        irrf_data = fetch_irrf_data()
        if irrf_data:
            df_irrf = pd.DataFrame(irrf_data)
            if df_irrf.empty:
                st.info("Nenhum histórico de IRRF encontrado.")
                return

            df_irrf_display = df_irrf.copy()
            date_cols_to_format_irrf = ['data_inicio_vigencia', 'data_fim_vigencia', 'data_cadastro', 'data_atualizacao']
            for col_name_irrf in date_cols_to_format_irrf:
                if col_name_irrf in df_irrf_display.columns:
                    df_irrf_display[col_name_irrf] = pd.to_datetime(df_irrf_display[col_name_irrf], errors='coerce')
                    if col_name_irrf == 'data_fim_vigencia':
                        df_irrf_display[col_name_irrf] = df_irrf_display[col_name_irrf].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else "Aberta")
                    elif col_name_irrf in ['data_cadastro', 'data_atualizacao']:
                        df_irrf_display[col_name_irrf] = df_irrf_display[col_name_irrf].apply(lambda x: x.strftime('%d/%m/%Y %H:%M') if pd.notna(x) else "-")
                    else: # data_inicio_vigencia
                        df_irrf_display[col_name_irrf] = df_irrf_display[col_name_irrf].apply(lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else "-")
            
            if 'faixas' in df_irrf_display.columns:
                df_irrf_display['faixas_str'] = df_irrf_display['faixas'].apply(
                    lambda x: json.dumps(x, ensure_ascii=False, indent=1) if isinstance(x, list) and x else "-"
                )
            if 'deducao_por_dependente' in df_irrf_display.columns:
                 df_irrf_display['deducao_por_dependente_fmt'] = df_irrf_display['deducao_por_dependente'].apply(lambda x: f"R$ {x:.2f}" if pd.notna(x) else "-")
            if 'limite_desconto_simplificado' in df_irrf_display.columns:
                 df_irrf_display['limite_desconto_simplificado_fmt'] = df_irrf_display['limite_desconto_simplificado'].apply(lambda x: f"R$ {x:.2f}" if pd.notna(x) else "-")

            header_cols_irrf = st.columns([1, 2, 2, 3, 2, 2, 2, 1, 1]) 
            column_names_irrf = ["ID", "Início Vig.", "Fim Vig.", "Faixas", "Dedução Dep.", "Desc. Simplif.", "Obs.", "Editar", "Inativar"]
            for h_col, name in zip(header_cols_irrf, column_names_irrf):
                h_col.markdown(f"**{name}**")
            st.markdown("---")

            for index_val_irrf in df_irrf.index:
                row_data_series_irrf = df_irrf.loc[index_val_irrf]
                display_row_series_irrf = df_irrf_display.loc[index_val_irrf]
                item_id_str_irrf = str(row_data_series_irrf['id_versao'])

                row_cols_list_irrf = st.columns([1, 2, 2, 3, 2, 2, 2, 1, 1])
                row_cols_list_irrf[0].text(display_row_series_irrf.get('id_versao', 'N/A'))
                row_cols_list_irrf[1].text(display_row_series_irrf.get('data_inicio_vigencia', 'N/A'))
                row_cols_list_irrf[2].text(display_row_series_irrf.get('data_fim_vigencia', 'Aberta'))
                
                faixas_str_display_irrf = display_row_series_irrf.get('faixas_str', '-')
                if faixas_str_display_irrf != '-' and len(faixas_str_display_irrf) > 30: # Limite para expander
                    with row_cols_list_irrf[3].expander("Ver Faixas"):
                        st.json(row_data_series_irrf.get('faixas', []))
                else:
                    row_cols_list_irrf[3].text(faixas_str_display_irrf)

                row_cols_list_irrf[4].text(display_row_series_irrf.get('deducao_por_dependente_fmt', '-'))
                row_cols_list_irrf[5].text(display_row_series_irrf.get('limite_desconto_simplificado_fmt', '-'))

                obs_text_irrf = str(display_row_series_irrf.get('observacao', '') or "-")
                if len(obs_text_irrf) > 25: # Limite para expander
                    with row_cols_list_irrf[6].expander("Ver Obs."):
                        st.markdown(obs_text_irrf)
                else:
                    row_cols_list_irrf[6].text(obs_text_irrf)

                if row_cols_list_irrf[7].button("✏️", key=f"edit_irrf_{item_id_str_irrf}", help="Editar esta tabela"):
                    st.session_state.editing_irrf_item = row_data_series_irrf.to_dict()
                    st.session_state.item_id_para_deletar_irrf = None
                    st.rerun()

                if row_cols_list_irrf[8].button("🗑️", key=f"delete_irrf_{item_id_str_irrf}", help="Inativar esta tabela"):
                    st.session_state.item_id_para_deletar_irrf = item_id_str_irrf
                    st.session_state.editing_irrf_item = None
                    st.rerun()
                st.markdown("---")
        else:
            st.info("Nenhum histórico de IRRF encontrado ou erro ao carregar.")

def mostrar_pagina_salario_familia():
    st.header("👨‍👩‍👧‍👦 Gestão de Salário Família")

    # Funções auxiliares para interagir com a API de Salário Família
    @st.cache_data(ttl=60)
    def fetch_sf_data():
        try:
            response = requests.get(f"{API_BASE_URL}/param-legais/salario-familia/?skip=0&limit=1000")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.error(f"Erro ao buscar dados de Salário Família: {e}")
            return []
        except json.JSONDecodeError:
            st.error("Erro ao decodificar resposta da API de Salário Família.")
            return []

    def create_sf_entry(payload):
        try:
            response = requests.post(f"{API_BASE_URL}/param-legais/salario-familia/", json=payload)
            response.raise_for_status()
            st.success("Nova tabela de Salário Família criada com sucesso!")
            st.cache_data.clear()
            return response.json()
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao criar tabela de Salário Família ({e.response.status_code}): {detail}")
            return None
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao criar tabela de Salário Família: {e}")
            return None

    # Layout da página
    col_form_sf, col_view_sf = st.columns([1, 2])

    with col_form_sf:
        st.subheader("Adicionar Nova Vigência de Tabela Salário Família")
        with st.form("sf_add_form", clear_on_submit=True):
            data_inicio_vigencia_sf = st.date_input("Data Início Vigência*", key="sf_div", help="Data de início da validade desta tabela.")
            
            col_fim_chk_sf, col_fim_date_sf = st.columns([1,2])
            with col_fim_chk_sf:
                data_fim_especificada_sf = st.checkbox("Definir Data Fim?", key="sf_dfv_chk")
            data_fim_vigencia_sf = None
            if data_fim_especificada_sf:
                with col_fim_date_sf:
                    data_fim_vigencia_sf = st.date_input("Data Fim Vigência", key="sf_dfv_date", help="Opcional. Se não definida, a vigência é considerada aberta.")

            faixas_sf_json = st.text_area("Faixas de Salário Família (JSON)*", height=200, key="sf_faixas", 
                                            placeholder='''[{"valor_renda_minima": 0, "valor_renda_maxima": 1819.26, "valor_quota": 62.04}, ...]''',
                                            help="Lista de faixas. Ex: [{\"valor_renda_minima\": 0, \"valor_renda_maxima\": 1819.26, \"valor_quota\": 62.04}, ...].")
            
            observacao_sf = st.text_area("Observação", key="sf_obs")
            
            submit_button_sf = st.form_submit_button("Salvar Nova Tabela Salário Família")

            if submit_button_sf:
                if not data_inicio_vigencia_sf or not faixas_sf_json:
                    st.error("Data Início Vigência e Faixas de Salário Família são obrigatórios.")
                else:
                    try:
                        parsed_faixas_sf = json.loads(faixas_sf_json)
                        if not isinstance(parsed_faixas_sf, list) or not all(isinstance(item, dict) for item in parsed_faixas_sf):
                            st.error("Faixas de Salário Família: Formato JSON inválido. Deve ser uma lista de objetos.")
                        else:
                            # Validação básica dos campos das faixas
                            faixas_validas = True
                            for faixa in parsed_faixas_sf:
                                if not all(k in faixa for k in ["valor_renda_maxima", "valor_quota"]) or \
                                   not isinstance(faixa.get("valor_renda_maxima"), (int, float)) or \
                                   not isinstance(faixa.get("valor_quota"), (int, float)):
                                    st.error("Cada faixa deve conter 'valor_renda_maxima' e 'valor_quota' numéricos. 'valor_renda_minima' é opcional e numérico.")
                                    faixas_validas = False
                                    break
                                if "valor_renda_minima" in faixa and not isinstance(faixa.get("valor_renda_minima"), (int, float)):
                                    st.error("Se 'valor_renda_minima' for fornecido, deve ser numérico.")
                                    faixas_validas = False
                                    break
                            
                            if faixas_validas:
                                payload_sf = {
                                    "data_inicio_vigencia": data_inicio_vigencia_sf.isoformat(),
                                    "data_fim_vigencia": data_fim_vigencia_sf.isoformat() if data_fim_vigencia_sf else None,
                                    "faixas": parsed_faixas_sf,
                                    "observacao": observacao_sf if observacao_sf else None
                                }
                                if create_sf_entry(payload_sf):
                                    st.rerun()
                    except json.JSONDecodeError:
                        st.error("Faixas de Salário Família: Formato JSON inválido.")
    
    with col_view_sf:
        st.subheader("Histórico de Tabelas Salário Família")
        sf_data = fetch_sf_data()
        if sf_data:
            df_sf = pd.DataFrame(sf_data)
            df_sf_display = df_sf.copy()

            for col_date in ['data_inicio_vigencia', 'data_fim_vigencia', 'data_cadastro', 'data_atualizacao']:
                if col_date in df_sf_display.columns:
                    df_sf_display[col_date] = pd.to_datetime(df_sf_display[col_date], errors='coerce')
                    if col_date == 'data_fim_vigencia':
                        df_sf_display[col_date] = df_sf_display[col_date].dt.strftime('%d/%m/%Y').fillna("Aberta")
                    else:
                        df_sf_display[col_date] = df_sf_display[col_date].dt.strftime('%d/%m/%Y' + (' %H:%M' if col_date in ['data_cadastro', 'data_atualizacao'] else ''))
            
            if 'faixas' in df_sf_display.columns:
                df_sf_display['faixas_str'] = df_sf_display['faixas'].apply(lambda x: json.dumps(x, ensure_ascii=False, indent=2) if isinstance(x, list) else str(x))

            colunas_visiveis_sf = ['id_versao', 'data_inicio_vigencia', 'data_fim_vigencia', 'faixas_str', 'observacao', 'data_cadastro', 'data_atualizacao']
            colunas_para_mostrar_sf = [col for col in colunas_visiveis_sf if col in df_sf_display.columns]
            
            if 'faixas' in df_sf_display.columns and 'faixas_str' not in colunas_para_mostrar_sf and 'faixas_str' in df_sf_display.columns:
                 if 'faixas' in colunas_para_mostrar_sf:
                    colunas_para_mostrar_sf[colunas_para_mostrar_sf.index('faixas')] = 'faixas_str'
            elif 'faixas' in df_sf_display.columns and 'faixas' not in colunas_para_mostrar_sf:
                 colunas_para_mostrar_sf.insert(3, 'faixas')


            st.dataframe(df_sf_display[colunas_para_mostrar_sf], use_container_width=True, hide_index=True,
                         column_config={
                             "faixas_str": st.column_config.TextColumn("Faixas (JSON)")
                         }
                        )
            # TODO: Adicionar botões de Editar/Inativar por linha para Salário Família
        else:
            st.info("Nenhum histórico de Salário Família encontrado ou erro ao carregar.")

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
        # Use uma chave única para o botão de logout se ele for renderizado aqui
        authenticator.logout('Logout', 'main', key='main_panel_logout') 
        st.title(f"Painel AUDITORIA360 - Bem-vindo(a) {st.session_state.get('name')}!")
        
        # Navegação por Abas
        tab_titulos = [
            "🗓️ Gestão de Controle de Folhas",
            "🪙 Salário Mínimo",
            "📊 FGTS",
            "📄 INSS",
            "💸 IRRF",
            "👨‍👩‍👧‍👦 Salário Família"
        ]
        tab_controle_folhas, tab_sm, tab_fgts, tab_inss, tab_irrf, tab_sf = st.tabs(tab_titulos)

        with tab_controle_folhas:
            mostrar_pagina_gestao_controle_folhas()
        with tab_sm:
            mostrar_pagina_salario_minimo()
        with tab_fgts:
            mostrar_pagina_fgts()
        with tab_inss:
            mostrar_pagina_inss()
        with tab_irrf:
            mostrar_pagina_irrf()
        with tab_sf:
            mostrar_pagina_salario_familia()

def main():
    initialize_app()

    if BRANDING_LOGO_URL:
        st.sidebar.image(BRANDING_LOGO_URL, width=150)
    if CLIENT_DISPLAY_NAME:
        st.sidebar.markdown(f"<h3 style='text-align: center'>{CLIENT_DISPLAY_NAME}</h3>", unsafe_allow_html=True)

    if run_login_flow():
        display_main_panel()

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title=f"Auditoria360 - {CLIENT_DISPLAY_NAME}")
    main()