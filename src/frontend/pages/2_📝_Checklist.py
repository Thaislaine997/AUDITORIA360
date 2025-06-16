import streamlit as st
st.set_page_config(page_title="Checklist de Fechamento - Auditoria360", layout="wide")

import sys
import os
import requests
import logging
import json # Adicionado import json
from datetime import datetime # datetime já estava importado
from typing import Optional, List, Dict, Any

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) # Adjusted for pages subdir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

# --- Carregamento do CSS para Design System ---
def load_css():
    with open(os.path.join(_project_root, "assets", "style.css")) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()  # Carrega os estilos do Design System
# --- Fim do Carregamento do CSS ---

from src.core.config import settings
# Importar utilitários do frontend
from src.frontend.utils import (
    display_user_info_sidebar, 
    handle_api_error, 
    get_api_token as get_global_api_token, # Renomeado para evitar conflito se houver um local
    get_current_client_id as get_global_current_client_id # Renomeado
)

logger = logging.getLogger(__name__)

def initialize_session_state_checklist():
    if "checklist_items" not in st.session_state:
        st.session_state.checklist_items = [] # Inicializado como lista vazia
    if "current_folha_id_for_checklist" not in st.session_state: # Renomeado de id_folha_processada_checklist
        st.session_state.current_folha_id_for_checklist = None
    if "dica_ia_cache" not in st.session_state:
         st.session_state.dica_ia_cache = {} # Inicializado como dict vazio

# Funções para obter token e client_id da sessão principal (st.session_state)
# Usando os globais importados e renomeados para clareza
def get_api_token() -> Optional[str]:
    return get_global_api_token()

def get_current_client_id() -> Optional[str]:
    return get_global_current_client_id()

def get_current_folha_id_for_checklist() -> Optional[str]:
    return st.session_state.get("current_folha_id_for_checklist")

def set_current_folha_id_for_checklist(folha_id: Optional[str]):
    st.session_state.current_folha_id_for_checklist = folha_id

def get_auth_headers_checklist(): # Renomeado para evitar conflito com utils global se existir
    token = get_api_token()
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

# Funções de interação com a API do Checklist
def fetch_checklist_items(id_cliente: str, id_folha_processada: str):
    api_url = f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist-fechamento"
    logger.info(f"Buscando itens do checklist: {api_url}")
    try:
        response = requests.get(api_url, headers=get_auth_headers_checklist())
        if response.status_code == 401:
            handle_api_error(response.status_code)
            st.rerun()
            return []
        response.raise_for_status()
        return response.json().get("itens_checklist", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao buscar itens do checklist: {e}")
        logger.error(f"Erro de conexão ao buscar itens do checklist: {e}", exc_info=True)
        return []
    except json.JSONDecodeError:
        st.error("Erro ao decodificar a resposta da API (itens do checklist).")
        logger.error("Erro ao decodificar a resposta da API (itens do checklist).", exc_info=True)
        return []


def update_checklist_item_api(id_cliente: str, id_folha_processada: str, id_item_checklist: str, updates: dict):
    api_url = f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist-fechamento/{id_item_checklist}"
    logger.info(f"Atualizando item do checklist: {api_url} com dados: {updates}")
    try:
        response = requests.put(api_url, json=updates, headers=get_auth_headers_checklist())
        if response.status_code == 401:
            handle_api_error(response.status_code)
            st.rerun()
            return False # Indicar falha
        response.raise_for_status()
        st.success("Item do checklist atualizado com sucesso!")
        return True # Indicar sucesso
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao atualizar item do checklist: {e}")
        logger.error(f"Erro de conexão ao atualizar item do checklist: {e}", exc_info=True)
        return False
    except json.JSONDecodeError: # Embora PUT não espere JSON de volta tipicamente, pode haver erro com JSON
        st.error("Erro ao processar a resposta da API (atualização do item).")
        logger.error("Erro ao processar a resposta da API (atualização do item).", exc_info=True)
        return False

def mark_sheet_as_closed_api(id_cliente: str, id_folha_processada: str):
    api_url = f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/marcar-fechada"
    logger.info(f"Marcando folha como fechada: {api_url}")
    try:
        response = requests.post(api_url, headers=get_auth_headers_checklist())
        if response.status_code == 401:
            handle_api_error(response.status_code)
            st.rerun()
            return False
        response.raise_for_status()
        st.success("Folha marcada como fechada com sucesso!")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao marcar folha como fechada: {e}")
        logger.error(f"Erro de conexão ao marcar folha como fechada: {e}", exc_info=True)
        return False

def get_dica_ia_api(id_cliente: str, id_folha_processada: str, id_item_checklist: str, descricao_item: str):
    api_url = f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist-fechamento/{id_item_checklist}/dica-ia"
    payload = {"descricao_item": descricao_item}
    logger.info(f"Buscando dica IA: {api_url} para item: {descricao_item}")
    try:
        response = requests.post(api_url, json=payload, headers=get_auth_headers_checklist())
        if response.status_code == 401:
            handle_api_error(response.status_code)
            st.rerun()
            return None
        response.raise_for_status()
        return response.json().get("dica")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao buscar dica da IA: {e}")
        logger.error(f"Erro de conexão ao buscar dica da IA: {e}", exc_info=True)
        return None
    except json.JSONDecodeError:
        st.error("Erro ao decodificar a resposta da API (dica IA).")
        logger.error("Erro ao decodificar a resposta da API (dica IA).", exc_info=True)
        return None

def fetch_folhas_disponiveis_para_checklist(id_cliente: str):
    api_url = f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas-processadas?status_checklist=pendente" # Exemplo de filtro
    logger.info(f"Buscando folhas disponíveis para checklist: {api_url}")
    try:
        response = requests.get(api_url, headers=get_auth_headers_checklist())
        if response.status_code == 401:
            handle_api_error(response.status_code)
            st.rerun()
            return []
        response.raise_for_status()
        # Supondo que a resposta seja similar à de buscar_folhas_processadas_cliente em dashboard_folha
        folhas_raw = response.json().get("folhas", [])
        folhas_formatadas = []
        for folha_data in folhas_raw:
            try:
                dt_str = folha_data.get("periodo_referencia")
                if isinstance(dt_str, str):
                    dt_obj = datetime.strptime(dt_str.split('T')[0], "%Y-%m-%d").date() if 'T' in dt_str else datetime.strptime(dt_str, "%Y-%m-%d").date()
                    folha_data["periodo_referencia_display"] = dt_obj.strftime("%B/%Y")
                else: # Se já for um objeto date (improvável vindo de JSON puro)
                     folha_data["periodo_referencia_display"] = "Data Inválida"

                folha_data["selectbox_label"] = f'{folha_data["periodo_referencia_display"]} (ID: {folha_data["id_folha_processada"][:8]}...)'
                folhas_formatadas.append(folha_data)
            except ValueError as ve:
                logger.error(f"Erro ao formatar data para folha {folha_data.get('id_folha_processada')}: {ve}")
                folha_data["periodo_referencia_display"] = "Data Inconsistente"
                folha_data["selectbox_label"] = f'Data Inconsistente (ID: {folha_data.get("id_folha_processada","ERRO")[:8]}...)'
                folhas_formatadas.append(folha_data)
        
        # Ordenar por data, se necessário (exemplo: mais recentes primeiro)
        # folhas_formatadas.sort(key=lambda x: x.get("periodo_referencia_date_obj", date.min), reverse=True)
        return folhas_formatadas
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao buscar folhas disponíveis: {e}")
        logger.error(f"Erro de conexão ao buscar folhas disponíveis: {e}", exc_info=True)
        return []
    except json.JSONDecodeError:
        st.error("Erro ao decodificar a resposta da API (folhas disponíveis).")
        logger.error("Erro ao decodificar a resposta da API (folhas disponíveis).", exc_info=True)
        return []

def mostrar_checklist_page():
    initialize_session_state_checklist()
    
    api_token = get_api_token()
    id_cliente_atual = get_current_client_id()

    if not api_token or not id_cliente_atual:
        st.warning("Você precisa estar logado para acessar esta página.")
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
    
    st.title("📝 Checklist de Fechamento da Folha")

    # Seleção da Folha de Pagamento
    folhas_disponiveis = fetch_folhas_disponiveis_para_checklist(id_cliente_atual)
    
    if not folhas_disponiveis:
        st.info("Nenhuma folha de pagamento com checklist pendente encontrada para este cliente.")
        st.stop()

    map_label_to_id_folha = {f["selectbox_label"]: f["id_folha_processada"] for f in folhas_disponiveis}
    
    # Usar o ID da folha armazenado na sessão se existir, ou o primeiro da lista
    id_folha_selecionada_sessao = get_current_folha_id_for_checklist()
    
    # Encontrar o label correspondente ao ID da sessão, se existir na lista atual
    label_selecionada_default = None
    if id_folha_selecionada_sessao:
        for label, id_f in map_label_to_id_folha.items():
            if id_f == id_folha_selecionada_sessao:
                label_selecionada_default = label
                break
    
    # Se não houver default ou o default não estiver mais na lista, usa o primeiro item
    if not label_selecionada_default and map_label_to_id_folha:
        label_selecionada_default = list(map_label_to_id_folha.keys())[0]

    label_folha_selecionada = st.selectbox(
        "Selecione a Folha de Pagamento para o Checklist:",
        options=list(map_label_to_id_folha.keys()),
        index=list(map_label_to_id_folha.keys()).index(label_selecionada_default) if label_selecionada_default else 0,
        key="select_folha_checklist"
    )

    if not label_folha_selecionada:
        st.info("Por favor, selecione uma folha de pagamento.")
        st.stop()

    id_folha_escolhida = map_label_to_id_folha[label_folha_selecionada]
    set_current_folha_id_for_checklist(id_folha_escolhida) # Atualiza na sessão

    st.markdown(f"### Checklist para a Folha: **{label_folha_selecionada}**")

    # Carregar itens do checklist
    if st.button("Carregar Itens do Checklist") or (id_folha_escolhida and not st.session_state.checklist_items):
        st.session_state.checklist_items = fetch_checklist_items(id_cliente_atual, id_folha_escolhida)

    if not st.session_state.checklist_items:
        st.info("Nenhum item de checklist encontrado para esta folha ou checklist ainda não carregado.")
    else:
        for index, item in enumerate(st.session_state.checklist_items):
            item_id = item.get("id_item_checklist_fechamento") # Ajustar conforme o schema da API
            descricao = item.get("descricao_item", "Item sem descrição")
            status_atual = item.get("status_item", "PENDENTE") # PENDENTE, CONCLUIDO, NAO_APLICAVEL
            observacoes = item.get("observacoes_usuario", "")

            with st.container(border=True):
                st.markdown(f"**{index + 1}. {descricao}**")
                
                cols_status_obs = st.columns([2,3])
                with cols_status_obs[0]:
                    novo_status = st.radio(
                        "Status:", 
                        options=["PENDENTE", "CONCLUIDO", "NAO_APLICAVEL"], 
                        index=["PENDENTE", "CONCLUIDO", "NAO_APLICAVEL"].index(status_atual) if status_atual in ["PENDENTE", "CONCLUIDO", "NAO_APLICAVEL"] else 0,
                        key=f"status_{item_id}",
                        horizontal=True
                    )
                with cols_status_obs[1]:
                    novas_observacoes = st.text_area("Observações:", value=observacoes, key=f"obs_{item_id}", height=75)

                cols_acao_dica = st.columns([1,3])
                with cols_acao_dica[0]:
                    if st.button("Salvar Item", key=f"save_{item_id}"):
                        updates = {"status_item": novo_status, "observacoes_usuario": novas_observacoes}
                        if update_checklist_item_api(id_cliente_atual, id_folha_escolhida, item_id, updates):
                            # Atualizar localmente para refletir mudança imediatamente (opcional, API deve ser fonte da verdade)
                            item["status_item"] = novo_status
                            item["observacoes_usuario"] = novas_observacoes
                            st.rerun() # Para recarregar e mostrar o estado atualizado
                
                with cols_acao_dica[1]:
                    # Cache simples para dicas de IA
                    dica_cache_key = f"{id_folha_escolhida}_{item_id}"
                    if dica_cache_key not in st.session_state.dica_ia_cache:
                        if st.button("💡 Obter Dica da IA", key=f"dica_{item_id}"):
                            dica = get_dica_ia_api(id_cliente_atual, id_folha_escolhida, item_id, descricao)
                            if dica:
                                st.session_state.dica_ia_cache[dica_cache_key] = dica
                                st.info(f"**Dica da IA:** {dica}")
                            else:
                                st.warning("Não foi possível obter a dica da IA no momento.")
                    else:
                        st.info(f"**Dica da IA (cache):** {st.session_state.dica_ia_cache[dica_cache_key]}")
                        if st.button("Limpar Dica", key=f"clear_dica_{item_id}"):
                             del st.session_state.dica_ia_cache[dica_cache_key]
                             st.rerun()
                st.markdown("---")


        # Botão para fechar o checklist da folha
        if all(it.get("status_item") in ["CONCLUIDO", "NAO_APLICAVEL"] for it in st.session_state.checklist_items) and st.session_state.checklist_items:
            if st.button("🏁 Marcar Folha como Fechada (Checklist Concluído)", type="primary"):
                if mark_sheet_as_closed_api(id_cliente_atual, id_folha_escolhida):
                    st.balloons()
                    # Limpar o checklist da sessão e buscar novas folhas pendentes
                    st.session_state.checklist_items = []
                    set_current_folha_id_for_checklist(None)
                    st.rerun()
        elif st.session_state.checklist_items:
            st.warning("Ainda existem itens pendentes no checklist. Conclua todos os itens para fechar a folha.")


if __name__ == "__main__":
    # Simulação do st.session_state para fins de teste local
    # Comente ou remova estas linhas quando integrado ao painel.py
    if 'token' not in st.session_state:
        st.session_state.token = "token_simulado_checklist" # Adicione um token válido se sua API exigir
    if 'id_cliente' not in st.session_state:
        st.session_state.id_cliente = "cliente_simulado_checklist_123" # ID de cliente para teste
    if 'user_info' not in st.session_state: # user_info é usado por display_user_info_sidebar
        st.session_state.user_info = {"name": "Usuário Teste Checklist", "username": "testuser_checklist"}

    mostrar_checklist_page()
