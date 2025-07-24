import streamlit as st
# Configuração da página (deve ser a primeira chamada do Streamlit)
st.set_page_config(page_title="Sugestões de Impacto CCT - AUDITORIA360", layout="wide", initial_sidebar_state="expanded")

import sys 
import os 
import requests
import json
from typing import Optional # Adicionado para tipagem

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) 
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

from configs.settings import settings
from dashboards.utils import (
    display_user_info_sidebar as global_display_user_info_sidebar, 
    handle_api_error, 
    get_api_token as get_global_api_token, 
    get_current_client_id as get_global_current_client_id,
    get_auth_headers as get_global_auth_headers # Importar get_auth_headers global
)
from services.core.log_utils import logger # Corrigido caminho do logger

# Funções wrapper locais para consistência
def get_api_token() -> Optional[str]:
    return get_global_api_token()

def get_current_client_id() -> Optional[str]:
    return get_global_current_client_id()

def display_user_info_sidebar():
    global_display_user_info_sidebar()

def get_auth_headers_sugestoes(): # Wrapper local para headers
    token = get_api_token()
    return get_global_auth_headers(token) # Chama o global com o token


def mostrar_pagina_sugestoes_cct(): # Renomeado para seguir padrão
    # st.set_page_config já foi chamado no topo do arquivo

    # --- Logo --- (Removido, display_user_info_sidebar cuida disso)
    # st.sidebar.markdown(\\"---\\") # Removido

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

    st.title("💡 Sugestões de Impacto das CCTs - Revisão e Aprovação")
    st.caption(f"Cliente ID: {id_cliente_atual}")


    # Filtros iniciais
    # client_id já foi obtido de id_cliente_atual
    
    id_cct_doc_filter = st.text_input("ID do Documento CCT (opcional, para filtrar)", key="sug_id_cct_doc")

    if 'sugestoes_cct_data' not in st.session_state:
        st.session_state.sugestoes_cct_data = []

    if st.button("Buscar Sugestões Pendentes", key="btn_buscar_sugestoes_cct"):
        st.session_state.sugestoes_cct_data = [] # Limpar dados anteriores
        with st.spinner("Buscando sugestões..."):
            params = {"id_cliente_afetado": id_cliente_atual} 
            if id_cct_doc_filter:
                params["id_cct_documento_fk"] = id_cct_doc_filter
            
            auth_hdrs = get_auth_headers_sugestoes()
            api_url = f"{settings.API_BASE_URL}/api/v1/ccts/sugestoes-impacto"
            logger.info(f"Buscando sugestões de CCT: {api_url} com params: {params}")
            
            try:
                response = requests.get(api_url, headers=auth_hdrs, params=params)
                if response.status_code == 401:
                    handle_api_error(response.status_code)
                    st.rerun()
                    return # Adicionado para parar execução após rerun
                response.raise_for_status()
                st.session_state.sugestoes_cct_data = response.json().get("sugestoes", []) # Assumindo que a API retorna {"sugestoes": [...]}
                logger.info(f"Sugestões encontradas: {len(st.session_state.sugestoes_cct_data)}")
            except requests.exceptions.HTTPError as http_err:
                logger.error(f"Erro HTTP ao buscar sugestões CCT: {http_err.response.status_code} - {http_err.response.text}")
                error_detail = http_err.response.text
                try: 
                    error_detail = http_err.response.json().get("detail", error_detail)
                except json.JSONDecodeError: pass
                st.error(f"Erro ao buscar sugestões (HTTP {http_err.response.status_code}): {error_detail}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro de conexão ao buscar sugestões CCT: {e}", exc_info=True)
                st.error(f"Erro de conexão ao buscar sugestões: {e}")
            except json.JSONDecodeError:
                logger.error(f"Erro ao decodificar JSON da busca de sugestões CCT: {response.text if 'response' in locals() else 'Resposta não disponível'}")
                st.error("Erro ao processar a resposta do servidor (sugestões CCT).")
            except Exception as e: 
                logger.error(f"Erro inesperado na busca de sugestões CCT: {e}", exc_info=True)
                st.error(f"Erro inesperado ao processar a busca de sugestões: {e}")

    sugestoes_para_exibir = st.session_state.sugestoes_cct_data
    if not sugestoes_para_exibir:
        st.info("Nenhuma sugestão pendente encontrada para os filtros aplicados ou busca ainda não realizada.")
    else:
        for sugestao in sugestoes_para_exibir:
            sugestao_id = sugestao.get('id_sugestao_impacto', 'N/A')
            with st.expander(f"Sugestão ID {sugestao_id} - Tipo: {sugestao.get('tipo_sugestao', 'N/A')}"):
                # ...existing code...
                # (Conteúdo do expander permanece o mesmo, apenas ajustando a obtenção do username abaixo)
                st.markdown(f"**Cláusula Base:** {sugestao.get('texto_clausula_cct_base', 'N/A')}")
                st.markdown(f"**Justificativa IA:** {sugestao.get('justificativa_sugestao_ia', 'N/A')}")
                st.markdown(f"**Data de Vigência Sugerida:** {sugestao.get('data_inicio_vigencia_sugerida', 'N/A')}")
                st.markdown(f"**Status:** {sugestao.get('status_sugestao', 'PENDENTE')}")
                
                dados_editados = {}
                if sugestao.get('tipo_sugestao') == 'ALTERACAO_RUBRICA_CLIENTE':
                    st.markdown(f"**Rubrica Afetada:** {sugestao.get('codigo_rubrica_cliente_existente', 'N/A')}")
                    try:
                        alteracoes_str = sugestao.get('json_alteracoes_sugeridas_rubrica')
                        alteracoes = json.loads(alteracoes_str) if alteracoes_str else []
                        # Garantir que 'alteracoes' seja uma lista de dicionários
                        if not isinstance(alteracoes, list): alteracoes = []
                        
                        novas_alteracoes_editadas = []
                        for i, alt_item in enumerate(alteracoes):
                            if isinstance(alt_item, dict): # Processar apenas se for um dicionário
                                campo_alt = alt_item.get('campo_a_alterar', f'campo_desconhecido_{i}')
                                valor_sug = str(alt_item.get('novo_valor_sugerido', ''))
                                novo_valor_editado = st.text_input(
                                    f"{campo_alt}",
                                    value=valor_sug,
                                    key=f"{sugestao_id}_{campo_alt}_{i}" 
                                )
                                novas_alteracoes_editadas.append({
                                    "campo_a_alterar": campo_alt,
                                    "novo_valor_sugerido": novo_valor_editado 
                                })
                            else: # Se não for dict, manter o original ou logar erro
                                logger.warning(f"Item em json_alteracoes_sugeridas_rubrica não é um dict: {alt_item} para sugestão {sugestao_id}")
                                novas_alteracoes_editadas.append(alt_item) # Manter se não for dict, ou tratar conforme necessário

                        dados_editados['json_alteracoes_sugeridas_rubrica'] = json.dumps(novas_alteracoes_editadas)
                    except json.JSONDecodeError:
                        logger.error(f"Erro ao decodificar JSON de alterações para sugestão {sugestao_id}: {sugestao.get('json_alteracoes_sugeridas_rubrica')}")
                        st.error("Erro ao decodificar JSON de alterações sugeridas.")
                        dados_editados['json_alteracoes_sugeridas_rubrica'] = sugestao.get('json_alteracoes_sugeridas_rubrica', '[]')


                elif sugestao.get('tipo_sugestao') == 'NOVA_RUBRICA_CLIENTE':
                    dados_editados['codigo_sugerido_nova_rubrica'] = st.text_input("Código Nova Rubrica", value=sugestao.get('codigo_sugerido_nova_rubrica', ''), key=f"cod_nr_{sugestao_id}")
                    dados_editados['descricao_sugerida_nova_rubrica'] = st.text_input("Descrição Nova Rubrica", value=sugestao.get('descricao_sugerida_nova_rubrica', ''), key=f"desc_nr_{sugestao_id}")
                    dados_editados['tipo_sugerido_nova_rubrica'] = st.text_input("Tipo Nova Rubrica", value=sugestao.get('tipo_sugerido_nova_rubrica', ''), key=f"tipo_nr_{sugestao_id}")
                    dados_editados['natureza_esocial_sugerida'] = st.text_input("Natureza eSocial", value=sugestao.get('natureza_esocial_sugerida', ''), key=f"nat_esocial_nr_{sugestao_id}")
                    try:
                        incidencias_str = sugestao.get('json_sugestao_incidencias_completa_nova_rubrica')
                        incidencias = json.loads(incidencias_str) if incidencias_str else {}
                        if not isinstance(incidencias, dict): incidencias = {} # Garantir que é um dict

                        novas_incidencias_editadas = {}
                        for k, v_sug in incidencias.items():
                            valor_editado = st.text_input(
                                f"{k}",
                                value=str(v_sug), # Garantir que o valor é string para o input
                                key=f"{sugestao_id}_incidencia_{k}"
                            )
                            novas_incidencias_editadas[k] = valor_editado
                        dados_editados['json_sugestao_incidencias_completa_nova_rubrica'] = json.dumps(novas_incidencias_editadas)
                    except json.JSONDecodeError:
                        logger.error(f"Erro ao decodificar JSON de incidências para sugestão {sugestao_id}: {sugestao.get('json_sugestao_incidencias_completa_nova_rubrica')}")
                        st.error("Erro ao decodificar JSON de incidências sugeridas.")
                        dados_editados['json_sugestao_incidencias_completa_nova_rubrica'] = sugestao.get('json_sugestao_incidencias_completa_nova_rubrica', '{}')

                elif sugestao.get('tipo_sugestao', '').startswith('ATUALIZACAO_PARAMETRO_LEGAL'):
                    dados_editados['novo_valor_sugerido_parametro'] = st.text_input("Novo Valor Sugerido", value=sugestao.get('novo_valor_sugerido_parametro', ''), key=f"val_param_{sugestao_id}")
                
                notas = st.text_area("Notas de Revisão", key=f"notas_{sugestao_id}", value=sugestao.get("notas_revisao_usuario", "")) # Carregar notas existentes
                
                col1, col2 = st.columns(2)
                
                # Obter username de forma padronizada
                username = st.session_state.get("user_info", {}).get("username", "usuario_desconhecido")

                auth_hdrs_process = get_auth_headers_sugestoes() # Headers para POST/PUT
                api_url_process = f"{settings.API_BASE_URL}/api/v1/ccts/sugestoes-impacto/{sugestao_id}/processar"

                with col1:
                    if st.button("Aprovar e Aplicar", key=f"aprovar_{sugestao_id}"):
                        payload = {
                            "acao_usuario": "APROVAR_APLICAR",
                            "usuario_revisao": username,
                            "notas_revisao_usuario": notas,
                            "dados_sugestao_atualizados_json": json.dumps(dados_editados) if dados_editados else None
                        }
                        logger.info(f"Aprovando sugestão {sugestao_id}. Payload: {payload}")
                        try:
                            response_process = requests.post(api_url_process, headers=auth_hdrs_process, json=payload)
                            if response_process.status_code == 401:
                                handle_api_error(response_process.status_code)
                                st.rerun() # Adicionado rerun em caso de 401
                                return 
                            response_process.raise_for_status()
                            st.success(f"Sugestão {sugestao_id} aprovada e aplicada com sucesso!")
                            logger.info(f"Sugestão {sugestao_id} aprovada.")
                            st.session_state.sugestoes_cct_data = [] # Limpar para forçar recarga na próxima interação
                            st.rerun() 
                        except requests.exceptions.HTTPError as http_err_proc:
                            logger.error(f"Erro HTTP ao aprovar sugestão {sugestao_id}: {http_err_proc.response.status_code} - {http_err_proc.response.text}")
                            error_detail_proc = http_err_proc.response.text
                            try: 
                                error_detail_proc = http_err_proc.response.json().get("detail", error_detail_proc)
                            except json.JSONDecodeError: pass
                            st.error(f"Erro ao aprovar sugestão {sugestao_id} (HTTP {http_err_proc.response.status_code}): {error_detail_proc}")
                        except requests.exceptions.RequestException as e_proc:
                            logger.error(f"Erro de conexão ao aprovar sugestão {sugestao_id}: {e_proc}", exc_info=True)
                            st.error(f"Erro de conexão ao aprovar sugestão {sugestao_id}: {e_proc}")
                        except Exception as e_gen_proc:
                             logger.error(f"Erro inesperado ao processar aprovação da sugestão {sugestao_id}: {e_gen_proc}", exc_info=True)
                             st.error(f"Erro inesperado ao processar aprovação: {e_gen_proc}")

                with col2:
                    if st.button("Rejeitar", key=f"rejeitar_{sugestao_id}"):
                        payload = {
                            "acao_usuario": "REJEITAR",
                            "usuario_revisao": username,
                            "notas_revisao_usuario": notas,
                            "dados_sugestao_atualizados_json": None 
                        }
                        logger.info(f"Rejeitando sugestão {sugestao_id}. Payload: {payload}")
                        try:
                            response_process = requests.post(api_url_process, headers=auth_hdrs_process, json=payload)
                            if response_process.status_code == 401:
                                handle_api_error(response_process.status_code)
                                st.rerun() # Adicionado rerun em caso de 401
                                return
                            response_process.raise_for_status()
                            st.success(f"Sugestão {sugestao_id} rejeitada com sucesso!")
                            logger.info(f"Sugestão {sugestao_id} rejeitada.")
                            st.session_state.sugestoes_cct_data = [] # Limpar para forçar recarga
                            st.rerun() 
                        except requests.exceptions.HTTPError as http_err_rej:
                            logger.error(f"Erro HTTP ao rejeitar sugestão {sugestao_id}: {http_err_rej.response.status_code} - {http_err_rej.response.text}")
                            error_detail_rej = http_err_rej.response.text
                            try: 
                                error_detail_rej = http_err_rej.response.json().get("detail", error_detail_rej)
                            except json.JSONDecodeError: pass
                            st.error(f"Erro ao rejeitar sugestão {sugestao_id} (HTTP {http_err_rej.response.status_code}): {error_detail_rej}")
                        except requests.exceptions.RequestException as e_rej:
                            logger.error(f"Erro de conexão ao rejeitar sugestão {sugestao_id}: {e_rej}", exc_info=True)
                            st.error(f"Erro ao rejeitar sugestão {sugestao_id}: {e_rej}")
                        except Exception as e_gen_rej:
                             logger.error(f"Erro inesperado ao processar rejeição da sugestão {sugestao_id}: {e_gen_rej}", exc_info=True)
                             st.error(f"Erro inesperado ao processar rejeição: {e_gen_rej}")

if __name__ == "__main__":
    # Simula o estado da sessão para teste local
    if 'token' not in st.session_state: # Usar 'token' para consistência com utils
        st.session_state.token = "token_simulado_sugestoes_cct" 
    if 'client_id' not in st.session_state: # Usar 'client_id' para consistência
        st.session_state.client_id = "cliente_simulado_sugestoes_007"
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {"name": "Usuário Sugestão Teste", "username": "sugestao_user"}
    
    mostrar_pagina_sugestoes_cct()
