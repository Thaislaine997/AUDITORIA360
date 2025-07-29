# filepath: c:\\Users\\55479\\Documents\\AUDITORIA360\\src\\frontend\\pages\\4_📊_Gestão_de_CCTs.py
import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="Gestão de CCTs - AUDITORIA360") 

import sys 
import os 
import json # Adicionado import
import pandas as pd # Adicionado import
from datetime import date
from typing import Optional # Adicionado import

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) # Adjusted for pages subdir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

# --- Carregamento do CSS para Design System ---
def load_css():
    css_path = os.path.join(_project_root, "assets", "style.css")
    if not os.path.exists(css_path):
        css_path = "/workspaces/AUDITORIA360/assets/style.css"
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()  # Carrega os estilos do Design System
# --- Fim do Carregamento do CSS ---


"""
Página Streamlit para Gestão de Convenções Coletivas de Trabalho (CCTs)
"""

from configs.settings import settings
from dashboards.utils import (
    get_api_token as get_global_api_token, 
    get_current_client_id as get_global_current_client_id, 
    handle_api_error,
    display_user_info_sidebar as global_display_user_info_sidebar,
    get_auth_headers as get_global_auth_headers # Importar get_auth_headers global
)
from services.core.log_utils import logger # Corrigido caminho do logger

# Use global functions directly - no need for local wrappers
get_api_token = get_global_api_token
get_current_client_id = get_global_current_client_id
display_user_info_sidebar = global_display_user_info_sidebar

def get_auth_headers_cct(): # Wrapper local se precisar de modificações futuras
    return get_global_auth_headers(get_api_token()) # Chama o global com o token

# Função principal para renderizar a página de gestão de CCTs
def mostrar_pagina_gestao_cct():
    # st.set_page_config já foi chamado

    # --- Logo --- (Removido, pois display_user_info_sidebar deve cuidar disso)
    # st.sidebar.markdown("---")
    
    api_token = get_api_token()
    id_cliente_atual = get_current_client_id()

    if not api_token or not id_cliente_atual:
        st.warning("Por favor, faça login para acessar esta página.")
        if st.button("Retornar ao Login"):
            try:
                st.switch_page("painel.py")
            except AttributeError:
                st.page_link("painel.py", label="Retornar ao Login", icon="🏠")
            except Exception as e:
                 st.page_link("painel.py", label="Retornar ao Login", icon="🏠")
                 logger.warning(f"Falha ao usar st.switch_page para painel.py: {e}, usando page_link.")
        st.stop()

    display_user_info_sidebar() 

    st.title("🗂️ Gestão de Convenções Coletivas de Trabalho (CCTs)")
    st.caption(f"Cliente ID: {id_cliente_atual}")

    tab_upload, tab_listar, tab_monitor = st.tabs([
        "📤 Upload de CCT",
        "🔎 Listar/Buscar CCTs",
        "⚙️ Monitoramento de Alertas"
    ])

    # Aba de Upload
    with tab_upload:
        # A verificação de login já foi feita acima
        st.subheader("📤 Upload de Novo Documento de CCT/Aditivo")
        with st.form("form_upload_cct", clear_on_submit=True):
            nome = st.text_input("Nome Documento CCT")
            arquivo = st.file_uploader("Arquivo (PDF/DOCX)", type=["pdf", "docx"])
            data_inicio = st.date_input("Data Início Vigência", value=date.today())
            data_fim = st.date_input("Data Fim Vigência (opcional)", value=None)
            sind_laborais = st.text_area("Sindicato(s) Laboral(is) (um por linha)")
            sind_patronais = st.text_area("Sindicato(s) Patronal(is) (um por linha)")
            numero_reg = st.text_input("Nº Registro MTE")
            link_fonte = st.text_input("Link Fonte Oficial")
            id_base = st.text_input("ID CCT Base (opcional, se for aditivo)")
            # O campo ids_clientes_afetados pode ser preenchido automaticamente com id_cliente_atual
            # ou permitir uma lista se o usuário for admin de múltiplos clientes.
            # Por simplicidade, vamos assumir que se refere ao cliente atual ou é um campo para admin.
            ids_afetados_default = json.dumps([id_cliente_atual]) if id_cliente_atual else ""
            ids_afetados = st.text_input("IDs Clientes Afetados (JSON lista)", value=ids_afetados_default)
            
            submit_btn = st.form_submit_button("Salvar Documento CCT")
            if submit_btn:
                if not nome or not arquivo:
                    st.warning("Nome e arquivo são obrigatórios.")
                else:
                    # Preparar payload de dados do formulário (não JSON)
                    form_data_payload = {
                        "nome_documento_original": nome,
                        "data_inicio_vigencia_cct": data_inicio.isoformat(),
                        "data_fim_vigencia_cct": data_fim.isoformat() if data_fim else None,
                        "sindicatos_laborais_json_str": json.dumps([s.strip() for s in sind_laborais.split('\n') if s.strip()]) if sind_laborais else '[]', # Enviar como string JSON
                        "sindicatos_patronais_json_str": json.dumps([s.strip() for s in sind_patronais.split('\n') if s.strip()]) if sind_patronais else '[]', # Enviar como string JSON
                        "numero_registro_mte": numero_reg,
                        "link_fonte_oficial": link_fonte,
                        "id_cct_base_fk": id_base or None,
                        "ids_clientes_afetados_lista_str": ids_afetados or json.dumps([id_cliente_atual])
                    }
                    files = {"file": (arquivo.name, arquivo.getvalue(), arquivo.type)}
                    
                    auth_headers_for_upload = get_auth_headers_cct() # Pega o header de autenticação
                    # Remover Content-Type se já estiver nos headers de autenticação ou se a lib requests o define automaticamente para multipart/form-data
                    if 'Content-Type' in auth_headers_for_upload:
                        del auth_headers_for_upload['Content-Type']

                    try:
                        logger.info(f"Enviando CCT para {settings.API_BASE_URL}/ccts/upload. Payload: {form_data_payload.keys()}, File: {arquivo.name}")
                        resp = requests.post(
                            f"{settings.API_BASE_URL}/ccts/upload", # Endpoint corrigido para /ccts/upload
                            data=form_data_payload, # Usar 'data' para multipart/form-data
                            files=files,
                            headers=auth_headers_for_upload # Usar headers de autenticação
                        )
                        if resp.status_code == 401:
                            handle_api_error(resp.status_code)
                            st.rerun()
                            return
                        resp.raise_for_status()
                        data = resp.json()
                        st.success(f"CCT enviada com sucesso! ID: {data.get('id_cct_documento')}")
                    except requests.exceptions.HTTPError as http_err:
                        logger.error(f"Erro HTTP ao enviar CCT: {http_err.response.status_code} - {http_err.response.text}")
                        error_detail = http_err.response.text
                        try: 
                            error_detail = http_err.response.json().get("detail", error_detail)
                        except json.JSONDecodeError:
                            pass
                        st.error(f"Erro ao enviar CCT (HTTP {http_err.response.status_code}): {error_detail}")
                    except requests.exceptions.RequestException as e:
                        logger.error(f"Erro de conexão ao enviar CCT: {e}", exc_info=True)
                        st.error(f"Erro de conexão ao enviar CCT: {e}")
                    except json.JSONDecodeError:
                        logger.error(f"Erro ao decodificar JSON da resposta do upload CCT: {resp.text if 'resp' in locals() else 'Resposta não disponível'}")
                        st.error("Erro ao processar a resposta do servidor (upload CCT).")
                    except Exception as e: 
                        logger.error(f"Erro inesperado no upload da CCT: {e}", exc_info=True)
                        st.error(f"Erro inesperado ao processar o envio da CCT: {e}")


    # Aba de Listar/Buscar CCTs
    with tab_listar:
        st.subheader("🔎 Listar e Buscar CCTs")
        col1, col2, col3 = st.columns(3)
        # Para usuários não-admin, o filtro de cliente pode ser fixo ou não exibido.
        # Aqui, permitimos, mas poderia ser ajustado com base no perfil do usuário (se disponível).
        cliente_filter = col1.text_input("ID Cliente Afetado", key="filter_cliente_cct", value=id_cliente_atual or "")
        sindicato_filter = col2.text_input("Filtro Sindicato (nome)", key="filter_sindicato_cct")
        data_filter = col3.date_input("Data Vigência em", value=None, key="filter_data_cct")
        
        if st.button("Buscar CCTs", key="btn_buscar_ccts"):
            params = {}
            if cliente_filter:
                params["id_cliente_afetado"] = cliente_filter
            if sindicato_filter:
                params["sindicato_nome_contem"] = sindicato_filter
            if data_filter:
                params["data_vigencia_em"] = data_filter.isoformat()
            
            logger.info(f"Buscando CCTs com params: {params}")
            try:
                resp = requests.get(f"{settings.API_BASE_URL}/ccts", params=params, headers=get_auth_headers_cct())
                if resp.status_code == 401:
                    handle_api_error(resp.status_code)
                    st.rerun()
                    return
                resp.raise_for_status()
                ccts = resp.json().get("ccts", []) # Assumindo que a API retorna uma chave 'ccts' com a lista
            except requests.exceptions.HTTPError as http_err:
                logger.error(f"Erro HTTP ao buscar CCTs: {http_err.response.status_code} - {http_err.response.text}")
                error_detail = http_err.response.text
                try: 
                    error_detail = http_err.response.json().get("detail", error_detail)
                except json.JSONDecodeError:
                    pass
                st.error(f"Erro ao buscar CCTs (HTTP {http_err.response.status_code}): {error_detail}")
                ccts = []
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro de conexão ao buscar CCTs: {e}", exc_info=True)
                st.error(f"Erro ao buscar CCTs: {e}")
                ccts = []
            except json.JSONDecodeError:
                logger.error(f"Erro ao decodificar JSON da busca de CCTs: {resp.text if 'resp' in locals() else 'Resposta não disponível'}")
                st.error("Erro ao processar a resposta do servidor (busca CCTs).")
                ccts = []
            except Exception as e:
                logger.error(f"Erro inesperado na busca de CCTs: {e}", exc_info=True)
                st.error(f"Erro inesperado ao processar a busca de CCTs: {e}")
                ccts = []

            if not ccts:
                st.info("Nenhuma CCT encontrada com os filtros aplicados.")
            else:
                table_data = []
                for doc in ccts:
                    try:
                        sind_laborais_list = json.loads(doc.get("sindicatos_laborais_json_str", "[]")) if doc.get("sindicatos_laborais_json_str") else []
                        sind_patronais_list = json.loads(doc.get("sindicatos_patronais_json_str", "[]")) if doc.get("sindicatos_patronais_json_str") else []
                    except json.JSONDecodeError:
                        sind_laborais_list = ["Erro ao ler JSON"]
                        sind_patronais_list = ["Erro ao ler JSON"]

                    table_data.append({
                        "ID": doc.get("id_cct_documento"),
                        "Nome": doc.get("nome_documento_original"),
                        "Início Vigência": doc.get("data_inicio_vigencia_cct"),
                        "Fim Vigência": doc.get("data_fim_vigencia_cct", "-"),
                        "Sind. Laborais": ", ".join(sind_laborais_list),
                        "Sind. Patronais": ", ".join(sind_patronais_list),
                        "Status IA": doc.get("status_processamento_ia", "N/A"),
                        # Adicionar link de download se gcs_uri_documento estiver presente e for uma URL válida
                        "Download": f"[Baixar]({doc.get('gcs_uri_documento')})" if doc.get('gcs_uri_documento') else "Link Indisponível"
                    })
                df = pd.DataFrame(table_data)
                st.markdown("**Resultados:**")
                # st.write("Clique em 'Baixar' para acessar o documento.") # Removido pois o link está na tabela
                st.dataframe(df, hide_index=True, use_container_width=True) # Usar st.dataframe para melhor formatação e interatividade

    # Aba de Monitoramento de Alertas
    with tab_monitor:
        # A verificação de login já foi feita acima
        st.subheader("⚙️ Monitoramento de Alertas de Novas CCTs")
        status_filter = st.selectbox(
            "Filtrar status de alerta",
            options=["TODOS", "NOVO", "EM_REVISAO_ADMIN", "CCT_IMPORTADA", "DESCARTADO"],
            key="status_filter_cct_alerts"
        )
        params = {}
        if status_filter and status_filter != "TODOS":
            params["status"] = status_filter
        # Adicionar filtro por cliente se necessário, especialmente para admins
        # params["client_id"] = id_cliente_atual 

        logger.info(f"Buscando alertas de CCT com params: {params}")
        try:
            response = requests.get(f"{settings.API_BASE_URL}/ccts/alerts", params=params, headers=get_auth_headers_cct())
            if response.status_code == 401:
                handle_api_error(response.status_code)
                st.rerun()
                return
            response.raise_for_status()
            alerts = response.json().get("alerts", []) # Assumindo que a API retorna uma chave 'alerts'
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"Erro HTTP ao buscar alertas CCT: {http_err.response.status_code} - {http_err.response.text}")
            error_detail = http_err.response.text
            try: 
                error_detail = http_err.response.json().get("detail", error_detail)
            except json.JSONDecodeError:
                pass
            st.error(f"Erro ao buscar alertas (HTTP {http_err.response.status_code}): {error_detail}")
            alerts = []
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de conexão ao buscar alertas CCT: {e}", exc_info=True)
            st.error(f"Erro ao buscar alertas: {e}")
            alerts = []
        except json.JSONDecodeError:
            logger.error(f"Erro ao decodificar JSON da busca de alertas CCT: {response.text if 'response' in locals() else 'Resposta não disponível'}")
            st.error("Erro ao processar a resposta do servidor (alertas CCT).")
            alerts = []
        except Exception as e:
            logger.error(f"Erro inesperado na busca de alertas CCT: {e}", exc_info=True)
            st.error(f"Erro inesperado ao processar a busca de alertas: {e}")
            alerts = []


        if not alerts:
            st.info("Nenhum alerta encontrado com os filtros aplicados.")
        else:
            for alert in alerts:
                exp_title = f"Alerta ID: {alert.get('id_alerta_cct', 'N/A')} (Status: {alert.get('status_alerta', 'N/A')})"
                with st.expander(exp_title):
                    st.markdown(f"**Registro MTE:** {alert.get('numero_registro_mte_detectado', '-')}")
                    st.markdown(f"**Vigência Início:** {alert.get('vigencia_inicio_detectada', '-')}")
                    st.markdown(f"**Sindicato(s) Partes:** {alert.get('sindicatos_partes_detectados', '-')}")
                    st.markdown(f"**Link Fonte:** {alert.get('link_fonte_cct_detectada', '-')}")
                    st.markdown(f"**Detectado em:** {alert.get('data_deteccao', '-')}")
                    
                    col_status, col_notas = st.columns(2)
                    with col_status:
                        new_status = st.selectbox(
                            "Novo status para o alerta",
                            options=["NOVO", "EM_REVISAO_ADMIN", "CCT_IMPORTADA", "DESCARTADO"], # Adicionar todos os status válidos
                            index=["NOVO", "EM_REVISAO_ADMIN", "CCT_IMPORTADA", "DESCARTADO"].index(alert.get('status_alerta')) if alert.get('status_alerta') in ["NOVO", "EM_REVISAO_ADMIN", "CCT_IMPORTADA", "DESCARTADO"] else 0,
                            key=f"status_alert_{alert.get('id_alerta_cct')}"
                        )
                    with col_notas:
                        notes = st.text_area(
                            "Notas do Admin",
                            value=alert.get("notas_admin", ""),
                            key=f"notes_alert_{alert.get('id_alerta_cct')}"
                        )
                    
                    if st.button("Atualizar Alerta", key=f"btn_update_alert_{alert.get('id_alerta_cct')}"):
                        update_payload = {"status_alerta": new_status, "notas_admin": notes, "id_cliente": id_cliente_atual}
                        logger.info(f"Atualizando alerta CCT ID {alert.get('id_alerta_cct')} com payload: {update_payload}")
                        try:
                            put_resp = requests.put(
                                f"{settings.API_BASE_URL}/ccts/alerts/{alert.get('id_alerta_cct')}",
                                json=update_payload, 
                                headers=get_auth_headers_cct()
                            )
                            if put_resp.status_code == 401:
                                handle_api_error(put_resp.status_code)
                                st.rerun()
                                return
                            put_resp.raise_for_status()
                            st.success(f"Alerta {alert.get('id_alerta_cct')} atualizado com sucesso.")
                            st.rerun() 
                        except requests.exceptions.HTTPError as http_err_put:
                            logger.error(f"Erro HTTP ao atualizar alerta CCT: {http_err_put.response.status_code} - {http_err_put.response.text}")
                            error_detail_put = http_err_put.response.text
                            try: 
                                error_detail_put = http_err_put.response.json().get("detail", error_detail_put)
                            except json.JSONDecodeError:
                                pass
                            st.error(f"Erro ao atualizar alerta {alert.get('id_alerta_cct')} (HTTP {http_err_put.response.status_code}): {error_detail_put}")
                        except requests.exceptions.RequestException as e_put:
                            logger.error(f"Erro de conexão ao atualizar alerta CCT: {e_put}", exc_info=True)
                            st.error(f"Erro ao atualizar alerta {alert.get('id_alerta_cct')}: {e_put}")
                        except Exception as e_gen_put:
                            logger.error(f"Erro inesperado ao atualizar alerta CCT: {e_gen_put}", exc_info=True)
                            st.error(f"Erro inesperado ao processar a atualização do alerta: {e_gen_put}")
                            
    def get_ccts():
        url = "http://localhost:8000/api/ccts"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Erro ao buscar CCTs: {e}")
            return []

    ccts = get_ccts()
    st.write(ccts)
    
if __name__ == "__main__":
    # Ensure session_state keys used by the page are present for standalone testing
    if "token" not in st.session_state: 
         st.session_state.token = "token_simulado_para_teste_cct" 
    # Assuming get_current_client_id() from utils.py uses st.session_state.client_id
    if "client_id" not in st.session_state:
        st.session_state.client_id = "cliente_simulado_cct_123"
    if "user_info" not in st.session_state: # user_info is used by display_user_info_sidebar
        st.session_state.user_info = {"name": "Usuário Teste CCT", "username": "testuser_cct"}
    
    mostrar_pagina_gestao_cct()
