import streamlit as st
st.set_page_config(layout="wide", page_title="Consultor de Riscos - AUDITORIA360")

import sys
import os
import requests # Adicionado import
import json # Adicionado import
from typing import Optional # Adicionado Optional

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

from configs.settings import settings
from dashboards.utils import (
    get_api_token as get_global_api_token, 
    get_current_client_id as get_global_current_client_id, 
    handle_api_error,
    display_user_info_sidebar as global_display_user_info_sidebar # Renomeado para evitar conflito
)
from services.core.log_utils import logger # Corrigido caminho do logger

# Use global functions directly - no need for local wrappers
get_api_token = get_global_api_token
get_current_client_id = get_global_current_client_id
display_user_info_sidebar = global_display_user_info_sidebar

def get_auth_headers_consultor(): # Função específica para headers desta página
    token = get_api_token()
    headers = {"Content-Type": "application/json"} # Chat geralmente usa JSON
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def consultor_riscos_page():
    # st.set_page_config já foi chamado no topo

    # --- Logo --- (Removido, pois display_user_info_sidebar já deve cuidar disso ou ser padronizado no utils)
    # Se o logo for específico desta página e não gerenciado por display_user_info_sidebar, pode ser adicionado aqui.
    # Exemplo: st.sidebar.image(os.path.join(_project_root, "assets", "logo.png"), use_column_width=True)
    # st.sidebar.markdown("---")

    api_token = get_api_token()
    id_cliente_atual = get_current_client_id()

    if not api_token or not id_cliente_atual:
        st.warning("Por favor, faça login para acessar esta página.")
        # Usar st.page_link ou st.switch_page para voltar ao painel
        if st.button("Retornar ao Login"):
            try:
                st.switch_page("painel.py")
            except AttributeError:
                st.page_link("painel.py", label="Retornar ao Login", icon="🏠")
            except Exception as e:
                 st.page_link("painel.py", label="Retornar ao Login", icon="🏠")
                 logger.warning(f"Falha ao usar st.switch_page para painel.py: {e}, usando page_link.")
        st.stop()

    display_user_info_sidebar() # Exibe informações do usuário e logo padronizado

    st.title("🤖 Consultor de Riscos Interativo")
    st.caption(f"Conectado como Cliente ID: {id_cliente_atual}")

    # Inicializa o histórico do chat no session_state se não existir
    if "risks_messages" not in st.session_state: 
        st.session_state.risks_messages = []
        # Adicionar mensagem inicial do assistente, se houver contexto do dashboard
        risco_foco = st.session_state.get('risco_em_foco_para_consultor')
        id_folha_contexto = st.session_state.get('id_folha_ativa_contexto_chat')
        if risco_foco and id_folha_contexto:
            st.session_state.risks_messages.append({
                "role": "assistant", 
                "content": f"Olá! Vejo que você selecionou o risco '**{risco_foco.get('descricao_risco', 'N/A')}**' (Severidade: {risco_foco.get('severidade_estimada', 'N/A')}, Probabilidade: {risco_foco.get('probabilidade_estimada',0)*100:.0f}%) referente à folha ID '{id_folha_contexto[:8]}...'. Como posso ajudar a analisar ou mitigar este risco?"
            })
            # Limpar o contexto para não persistir entre sessões de chat independentes
            del st.session_state['risco_em_foco_para_consultor']
            del st.session_state['id_folha_ativa_contexto_chat']
        else:
            st.session_state.risks_messages.append({"role": "assistant", "content": "Olá! Sou seu consultor de riscos IA. Como posso ajudar você hoje?"})


    # Exibe as mensagens do histórico
    for message in st.session_state.risks_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do usuário
    if prompt := st.chat_input("Faça sua pergunta sobre riscos trabalhistas..."):
        st.session_state.risks_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                payload = {
                    "query": prompt,
                    "client_id": id_cliente_atual,
                    "conversation_history": [ # Enviar histórico para contexto
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.risks_messages[:-1] # Exclui a última (prompt atual)
                    ]
                }
                api_url = f"{settings.API_BASE_URL}/chat/riscos" # Endpoint ajustado para /chat/riscos
                logger.info(f"Enviando para API do consultor de riscos: {api_url} com payload: {payload.get('query')}")
                
                response = requests.post(api_url, json=payload, headers=get_auth_headers_consultor(), stream=False) # stream=False para resposta completa
                
                if response.status_code == 401:
                    handle_api_error(response.status_code) # Limpa sessão e avisa
                    st.rerun()
                    return # Para a execução
                
                response.raise_for_status() # Levanta erro para outros códigos HTTP ruins
                
                api_response_data = response.json()
                assistant_response = api_response_data.get("response", "Desculpe, não consegui processar sua pergunta.")
                full_response = assistant_response
                message_placeholder.markdown(full_response)

            except requests.exceptions.HTTPError as http_err:
                logger.error(f"Erro HTTP na API do consultor: {http_err.response.status_code} - {http_err.response.text}")
                error_detail = http_err.response.text
                try: # Tenta pegar o detalhe do JSON se houver
                    error_detail = http_err.response.json().get("detail", error_detail)
                except json.JSONDecodeError:
                    pass
                full_response = f"Erro ao contatar o serviço de consultoria (HTTP {http_err.response.status_code}): {error_detail}"
                message_placeholder.error(full_response)
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro de conexão com API do consultor: {e}", exc_info=True)
                full_response = f"Erro de conexão ao tentar falar com o consultor IA: {e}"
                message_placeholder.error(full_response)
            except json.JSONDecodeError:
                logger.error(f"Erro ao decodificar JSON da API do consultor: {response.text if 'response' in locals() else 'Resposta não disponível'}")
                full_response = "Erro ao processar a resposta do consultor (formato inválido)."
                message_placeholder.error(full_response)
            except Exception as e:
                logger.error(f"Erro inesperado no consultor de riscos: {e}", exc_info=True)
                full_response = f"Ocorreu um erro inesperado: {e}"
                message_placeholder.error(full_response)
            
        st.session_state.risks_messages.append({"role": "assistant", "content": full_response})

    # --- Exemplo completo: endpoint, autenticação JWT, filtro e formulário para Consultor de Riscos ---
    st.title("Consultor de Riscos")

    def obter_token():
        return st.text_input("Token JWT", type="password")

    def get_riscos(token):
        url = "http://localhost:8000/api/riscos"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), url, headers
        except Exception as e:
            st.error(f"Erro ao buscar riscos: {e}")
            return [], url, headers

    token = obter_token()
    if token:
        riscos, url, headers = get_riscos(token)
        filtro = st.text_input("Buscar por risco")
        riscos_filtrados = [r for r in riscos if filtro.lower() in r.get("descricao", "").lower()]
        st.write(riscos_filtrados)
        with st.form("Adicionar Risco"):
            descricao = st.text_input("Descrição")
            nivel = st.text_input("Nível")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                payload = {"descricao": descricao, "nivel": nivel}
                resp = requests.post(url, json=payload, headers=headers)
                if resp.status_code == 201:
                    st.success("Risco adicionado com sucesso!")
                else:
                    st.error(f"Erro ao adicionar risco: {resp.text}")
    else:
        st.warning("Informe o token JWT para acessar os dados.")

if __name__ == "__main__":
    if 'token' not in st.session_state:
        st.session_state.token = "token_simulado_consultor"
    if 'id_cliente' not in st.session_state:
        st.session_state.id_cliente = "cliente_simulado_consultor_123"
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {"name": "Usuário Consultor", "username": "consultor_user"}
    # if "risks_messages" not in st.session_state: # Já tratado dentro da função principal
    #     st.session_state.risks_messages = []

    consultor_riscos_page()
