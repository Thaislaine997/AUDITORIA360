import streamlit as st # Import principal do Streamlit
# Mover st.set_page_config para o topo absoluto
st.set_page_config(page_title="Dashboard Folha - Auditoria360", layout="wide")

import sys 
import os 

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



# import streamlit as st # Removido import duplicado
import pandas as pd
import requests
from datetime import date
from decimal import Decimal
import logging
from typing import Optional, Any, Dict, List
import re

# 1. Atualizar Imports de Schemas
from src.schemas.predicao_risco_schemas import (
    PredicaoRiscoDashboardResponse,
    DetalhePredicaoRiscoResponse,
    RiscoPrevistoDetalheSchema,
    FatorContribuinteTecnicoSchema,
    DadosSuporteVisualizacaoSchema
)

from configs.settings import settings
# Importar utilitários do frontend
from dashboards.utils import (
    display_user_info_sidebar, 
    handle_api_error,
    get_api_token,
    get_current_client_id
)
# Importar verificação de sessão
# Removido import quebrado

logger = logging.getLogger(__name__)

def initialize_session_state():
    # Mantido para inicializar estados específicos da página, se necessário,
    # mas token e client_id virão do painel.py
    if 'predicao_risco_data' not in st.session_state:
        st.session_state.predicao_risco_data = None
    if 'detalhe_risco_selecionado_id' not in st.session_state:
        st.session_state.detalhe_risco_selecionado_id = None
    if 'tipo_detalhe_predicao' not in st.session_state:
        st.session_state.tipo_detalhe_predicao = None
    if 'id_folha_contexto_detalhe' not in st.session_state:
        st.session_state.id_folha_contexto_detalhe = None
    if 'risco_em_foco_para_consultor' not in st.session_state:
        st.session_state.risco_em_foco_para_consultor = None
    if 'id_folha_ativa_contexto_chat' not in st.session_state:
        st.session_state.id_folha_ativa_contexto_chat = None
    # Remover estados de login duplicados
    # if 'api_token' not in st.session_state:
    #     st.session_state.api_token = None
    # if 'logged_in_client_id' not in st.session_state:
    #     st.session_state.logged_in_client_id = None
    # if 'logged_in_username' not in st.session_state:
    #     st.session_state.logged_in_username = None
    # if 'client_id_simulated' not in st.session_state: # Removido
    #     st.session_state.client_id_simulated = None

# 4. Remover login_user e logout_user duplicados
# def login_user(username, password) -> bool: ... (Removido)
# def logout_user(): ... (Removido - será tratado pelo painel.py ou navegação)

# Use global functions from dashboards.utils - no need for local implementations

def buscar_folhas_processadas_cliente(id_cliente: str, token: Optional[str]) -> list:
    headers: Dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    api_url = f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas-processadas"
    logger.info(f"Buscando folhas processadas: {api_url} com token: {'Sim' if token else 'Não'}")

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 401: # Adicionado tratamento com handle_api_error
            handle_api_error(response.status_code)
            st.rerun() # st.rerun() pode ser útil após handle_api_error se ele não parar a execução
            return [] # Retorna lista vazia em caso de erro de autenticação
        response.raise_for_status()
        folhas_raw = response.json().get("folhas", [])
        folhas_formatadas = []
        for folha_data in folhas_raw: 
            try:
                if isinstance(folha_data.get("periodo_referencia"), str):
                    dt_str = folha_data["periodo_referencia"]
                    if len(dt_str) == 7:  # YYYY-MM
                        dt_obj = date.fromisoformat(dt_str + "-01")
                    else:  # YYYY-MM-DD or other full date format
                        dt_obj = date.fromisoformat(dt_str)
                    folha_data["periodo_referencia_display"] = dt_obj.strftime("%B/%Y")
                    folha_data["periodo_referencia_date"] = dt_obj
                else:
                    dt_obj = folha_data.get("periodo_referencia") 
                    if isinstance(dt_obj, date):
                        folha_data["periodo_referencia_display"] = dt_obj.strftime("%B/%Y")
                        folha_data["periodo_referencia_date"] = dt_obj
                    else:
                        folha_data["periodo_referencia_display"] = "Data Inválida"
                        folha_data["periodo_referencia_date"] = date(1900, 1, 1)
                
                folha_data["selectbox_label"] = f'{folha_data["periodo_referencia_display"]} (ID: {folha_data["id_folha_processada"][:8]}...)'
                folhas_formatadas.append(folha_data)
            except ValueError as ve_date:
                logger.error(f"Erro ao parsear data para folha {folha_data.get('id_folha_processada')}: {ve_date}")
                folha_data["periodo_referencia_display"] = "Data Inconsistente"
                folha_data["periodo_referencia_date"] = date(1900, 1, 1)
                folha_data["selectbox_label"] = f'Data Inconsistente (ID: {folha_data.get("id_folha_processada","ERRO")[:8]}...)'
                folhas_formatadas.append(folha_data)
        
        folhas_formatadas.sort(key=lambda x: x["periodo_referencia_date"], reverse=True)
        return folhas_formatadas
    except requests.exceptions.HTTPError as e_http:
        logger.error(f"Erro HTTP ao buscar folhas processadas: {e_http.response.status_code} - {e_http.response.text}", exc_info=True)
        detail = "Erro desconhecido"
        try:
            detail = e_http.response.json().get("detail", e_http.response.text)
        except requests.exceptions.JSONDecodeError: 
            detail = e_http.response.text
        # O tratamento de 401 foi movido para cima. Outros erros HTTP são tratados aqui.
        st.error(f"Erro ao buscar folhas processadas ({e_http.response.status_code}): {detail}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao buscar folhas processadas: {e}")
        return []
    except Exception as e_json: # Renomeado para e_gen para clareza
        st.error(f"Erro ao processar resposta das folhas: {e_json}")
        return []

def mostrar_dashboard_saude_folha():
    # st.set_page_config já foi chamado no topo do script
    st.title("🏥 Dashboard de Saúde da Folha Mensal")
    
    initialize_session_state() # Inicializa estados da página

    # Verifica a sessão e obtém dados do usuário usando o novo módulo auth_verify
    # Removido verify_session()
    
    # Extrai o token, id_cliente e papéis do usuário
    api_token = st.session_state.get("api_token")
    id_cliente_atual = st.session_state.user_info.get("cliente_id") if "user_info" in st.session_state else None
    user_roles = st.session_state.user_info.get("roles", []) if "user_info" in st.session_state else []
      # Verifica se o usuário tem um cliente associado
    if not id_cliente_atual and "admin" not in user_roles:
        st.warning("Você precisa estar associado a um cliente para acessar esta página.")
        st.stop()
    
    # O código abaixo estava mal alinhado e foi removido pois já é tratado pelo verify_session:    # Exibir informações do usuário na sidebar usando a função utilitária
    display_user_info_sidebar()
    
    # Renderização condicional baseada nos papéis do usuário
    with st.sidebar:
        st.subheader("Seu Acesso")
        
        # Exibir os papéis do usuário
        st.write("**Papéis de Usuário:**")
        for role in user_roles:
            st.write(f"- {role}")
            
        # Adicionar informações específicas do cliente se não for admin
        if "admin" not in user_roles and id_cliente_atual:
            st.write(f"**Cliente ID:** {id_cliente_atual}")
            
        # Mostrar acesso especial para administradores
        if "admin" in user_roles:
            st.success("🔑 Acesso Administrativo")
            
            # Opção para simular visualização como cliente específico
            with st.expander("Simular Acesso de Cliente"):
                cliente_simulado = st.text_input("ID do Cliente a simular:", key="admin_simular_cliente")
                if st.button("Aplicar Simulação", key="btn_simular_cliente"):
                    if cliente_simulado:
                        st.session_state["cliente_simulado"] = cliente_simulado
                        st.rerun()
                    else:
                        st.warning("Informe um ID de cliente válido")
            
            # Opção para resetar simulação
            if "cliente_simulado" in st.session_state and st.session_state["cliente_simulado"]:
                if st.button("Resetar Simulação de Cliente", key="btn_reset_simular"):
                    if "cliente_simulado" in st.session_state:
                        del st.session_state["cliente_simulado"]
                    st.rerun()
            
        st.markdown("---")
    # Remover a lógica antiga da sidebar:
    # if st.session_state.get("username"): 
    #      st.sidebar.success(f"Logado como: {st.session_state.get('username')}")
    #      st.sidebar.caption(f"Cliente ID: {id_cliente_atual}")
    # st.sidebar.markdown("---")
    # Conteúdo Principal - agora assume que o usuário está logado
    
    # Determina se estamos usando um cliente simulado (apenas para admins)
    id_cliente_para_api = id_cliente_atual
    
    if "admin" in user_roles and "cliente_simulado" in st.session_state and st.session_state["cliente_simulado"]:
        id_cliente_para_api = st.session_state["cliente_simulado"]
        st.warning(f"🔄 Visualizando dados como cliente ID: {id_cliente_para_api} (Modo Simulação)")
    else:
        st.info(f"Exibindo dados para o cliente ID: {id_cliente_para_api}")

    folhas_disponiveis = []
    if id_cliente_para_api:
        folhas_disponiveis = buscar_folhas_processadas_cliente(id_cliente_para_api, api_token)
    if not folhas_disponiveis:
        st.info("Nenhuma folha processada encontrada para este cliente ou ocorreu um erro ao buscá-las.")
        return

    map_label_to_id = {f["selectbox_label"]: f["id_folha_processada"] for f in folhas_disponiveis}
    label_selecionada = st.selectbox("Selecione o Período da Folha:", options=list(map_label_to_id.keys()))

    if not label_selecionada:
        st.info("Por favor, selecione um período.")
        return
    id_folha_selecionada = map_label_to_id[label_selecionada]
    
    folha_selecionada_obj = next((f for f in folhas_disponiveis if f["id_folha_processada"] == id_folha_selecionada), None)
    periodo_selecionado_display = folha_selecionada_obj["periodo_referencia_display"] if folha_selecionada_obj else "Período Desconhecido"

    if st.button("Carregar Dashboard"):
        st.session_state.dashboard_data = None
        st.session_state.predicao_risco_data = None 
        try:
            headers = {"Authorization": f"Bearer {api_token}"}
            api_url = f"{settings.API_BASE_URL}/clientes/{id_cliente_para_api}/folhas/{id_folha_selecionada}/dashboard-saude"
            logger.info(f"Chamando API do dashboard: {api_url} com token: Sim")
            response = requests.get(api_url, headers=headers)
            if response.status_code == 401: # Adicionado tratamento com handle_api_error
                handle_api_error(response.status_code)
                st.rerun()
                return # Parar execução aqui
            response.raise_for_status()
            st.session_state.dashboard_data = response.json()
            st.success("Dados do dashboard carregados com sucesso!")
        except requests.exceptions.HTTPError as e_http:
            logger.error(f"Erro HTTP ao buscar dados do dashboard: {e_http.response.status_code} - {e_http.response.text}", exc_info=True)
            detail = "Erro desconhecido"
            try:
                detail = e_http.response.json().get("detail", e_http.response.text)
            except requests.exceptions.JSONDecodeError: 
                detail = e_http.response.text
            # O tratamento de 401 foi movido para cima.
            st.error(f"Erro ao buscar dados do dashboard ({e_http.response.status_code}): {detail}")
            st.session_state.dashboard_data = None
        except requests.exceptions.RequestException as e_req:
            logger.error(f"Erro de requisição ao buscar dados do dashboard: {e_req}", exc_info=True)
            st.error(f"Erro de conexão ao buscar dados do dashboard: {e_req}")
            st.session_state.dashboard_data = None
        except Exception as e_gen:
            logger.error(f"Erro inesperado ao carregar dashboard: {e_gen}", exc_info=True)
            st.error(f"Ocorreu um erro inesperado: {e_gen}")
            st.session_state.dashboard_data = None

    if 'dashboard_data' in st.session_state and st.session_state.dashboard_data:
        data = st.session_state.dashboard_data
        kpis = data.get("kpis", {})
        div_severidade = data.get("divergencias_por_severidade", [])
        div_tipo = data.get("divergencias_por_tipo", [])

        st.subheader(f"Resultados para: {periodo_selecionado_display} (Folha ID: {id_folha_selecionada})")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Bruto (Extrato)", f"R$ {Decimal(kpis.get('total_bruto_folha_extrato', '0.00')):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col2.metric("Total Líquido (Extrato)", f"R$ {Decimal(kpis.get('total_liquido_folha_extrato', '0.00')):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col3.metric("Nº Funcionários", str(kpis.get('numero_funcionarios_identificados', 0)))
        col4.metric("Status da Análise", str(kpis.get('status_geral_folha', 'N/A')))
        total_div = kpis.get('total_divergencias_identificadas', 0)
        col5.metric("Total de Divergências", str(total_div), delta_color="inverse" if total_div > 0 else "off")
        st.markdown("---")

        col_graf1, col_graf2 = st.columns(2)
        with col_graf1:
            st.subheader("Divergências por Severidade")
            if div_severidade:
                df_severidade = pd.DataFrame(div_severidade)
                if not df_severidade.empty:
                    st.bar_chart(df_severidade.set_index("severidade")["quantidade"])
                else:
                    st.info("Nenhuma divergência por severidade para exibir.")
            else:
                st.info("Dados de severidade de divergências não disponíveis.")
        with col_graf2:
            st.subheader("Divergências por Tipo de Encargo")
            if div_tipo:
                df_tipo = pd.DataFrame(div_tipo)
                if not df_tipo.empty:
                    st.bar_chart(df_tipo.set_index("tipo_divergencia")["quantidade"])
                else:
                    st.info("Nenhuma divergência por tipo para exibir.")
            else:
                st.info("Dados de tipo de divergências não disponíveis.")
        st.markdown("---")

        st.subheader("Impacto Financeiro Estimado por Tipo de Divergência")
        if div_tipo:
            df_impacto = pd.DataFrame(div_tipo)
            df_impacto["soma_diferenca_absoluta"] = df_impacto["soma_diferenca_absoluta"].astype(float)
            if not df_impacto.empty:
                st.bar_chart(df_impacto.set_index("tipo_divergencia")["soma_diferenca_absoluta"])
            else:
                st.info("Nenhum dado de impacto financeiro para exibir.")
        else:
            st.info("Dados de impacto financeiro não disponíveis.")
        st.markdown("---")

        # --- INÍCIO DA SEÇÃO DE ANÁLISE PREDITIVA DE RISCOS (ÉPICO 3.3) ---
        if id_folha_selecionada: 
            st.markdown("---") 
            st.header("🔮 Análise Preditiva de Riscos (IA)")

            dados_predicao_obj: Optional[PredicaoRiscoDashboardResponse] = None
            # Carregar ou buscar dados de predição
            if 'predicao_risco_data' not in st.session_state or \
               st.session_state.predicao_risco_data is None or \
               st.session_state.predicao_risco_data.id_folha_processada != id_folha_selecionada:
                try:
                    headers_pred = {"Authorization": f"Bearer {api_token}"}
                    api_url_pred = f"{settings.API_BASE_URL}/clientes/{id_cliente_para_api}/folhas/{id_folha_selecionada}/predicao-risco"
                    logger.info(f"Buscando dados de predição de risco: {api_url_pred}")
                    response_pred = requests.get(api_url_pred, headers=headers_pred)
                    if response_pred.status_code == 401: # Adicionado tratamento com handle_api_error
                        handle_api_error(response_pred.status_code)
                        st.rerun()
                        return # Parar execução aqui
                    response_pred.raise_for_status()
                    dados_predicao_api = response_pred.json()
                    dados_predicao_obj = PredicaoRiscoDashboardResponse(**dados_predicao_api)
                    st.session_state.predicao_risco_data = dados_predicao_obj
                except requests.exceptions.HTTPError as e_http_pred:
                    logger.error(f"Erro HTTP ao buscar dados de predição: {e_http_pred.response.status_code} - {e_http_pred.response.text}")
                    if e_http_pred.response.status_code == 404:
                        st.info("Análise preditiva de riscos ainda não disponível para esta folha.")
                    # O tratamento de 401 foi movido para cima.
                    else:
                        st.error(f"Erro ao carregar análise preditiva ({e_http_pred.response.status_code}). Tente novamente.")
                    st.session_state.predicao_risco_data = None 
                except requests.exceptions.RequestException as e_req_pred:
                    logger.error(f"Erro de conexão ao buscar dados de predição: {e_req_pred}")
                    st.error("Erro de conexão ao buscar análise preditiva. Verifique sua rede.")
                    st.session_state.predicao_risco_data = None
                except Exception as e_gen_pred:
                    logger.error(f"Erro inesperado ao processar dados de predição: {e_gen_pred}", exc_info=True)
                    st.error("Ocorreu um erro inesperado ao carregar a análise preditiva.")
                    st.session_state.predicao_risco_data = None
            else: 
                dados_predicao_obj = st.session_state.predicao_risco_data

            if dados_predicao_obj:
                col_score, col_risco_geral = st.columns(2)
                with col_score:
                    score = dados_predicao_obj.score_saude_folha
                    if score is not None:
                        st.metric(
                            label="Score de Saúde da Folha (IA)", 
                            value=f"{score:.1f}%"
                        )
                        st.progress(int(score) / 100)
                    else:
                        st.metric(label="Score de Saúde da Folha (IA)", value="Não Calculado")

                with col_risco_geral:
                    if dados_predicao_obj.classe_risco_geral and dados_predicao_obj.classe_risco_geral != "INDISPONIVEL":
                        st.metric(label="Classificação de Risco Geral (IA)", value=str(dados_predicao_obj.classe_risco_geral).upper())
                    else:
                        st.metric(label="Classificação de Risco Geral (IA)", value="N/A")

                if dados_predicao_obj.explicacao_geral_ia and dados_predicao_obj.explicacao_geral_ia != "Análise preditiva ainda não disponível ou não concluída para esta folha.":
                    with st.expander("Ver Entendimento Geral da IA sobre os Riscos", expanded=False):
                        st.info(dados_predicao_obj.explicacao_geral_ia)

                st.subheader("Principais Riscos Previstos pela IA")
                if dados_predicao_obj.principais_riscos_previstos:
                    for risco in dados_predicao_obj.principais_riscos_previstos:
                        container_risco = st.container(border=True)
                        container_risco.markdown(f"**🚨 {risco.descricao_risco}**")
                        cols_risco_detalhe = container_risco.columns(3)
                        cols_risco_detalhe[0].caption(f"Severidade: **{risco.severidade_estimada or 'N/A'}**")
                        cols_risco_detalhe[1].caption(f"Probabilidade: **{risco.probabilidade_estimada*100:.0f}%**" if risco.probabilidade_estimada is not None else "N/A")
                        cols_risco_detalhe[2].caption(f"Fator Principal: *{risco.fator_principal or 'N/A'}*")
                        
                        if container_risco.button("Ver Detalhes do Risco", key=f"detail_risk_{risco.id_risco_detalhe}_{id_folha_selecionada}"):
                            st.session_state.detalhe_risco_selecionado_id = risco.id_risco_detalhe
                            st.session_state.tipo_detalhe_predicao = "risco_especifico"
                            st.session_state.id_folha_contexto_detalhe = id_folha_selecionada 
                            st.rerun() 

                        if container_risco.button("Analisar Risco com Consultor IA", key=f"consult_risk_{risco.id_risco_detalhe}_{id_folha_selecionada}"):
                            st.session_state.risco_em_foco_para_consultor = risco.model_dump() 
                            st.session_state.id_folha_ativa_contexto_chat = id_folha_selecionada
                            try:
                                st.switch_page("pages/2_🤖_Consultor_de_Riscos_IA.py")
                            except Exception as e_switch:
                                logger.warning(f"Falha ao usar st.switch_page para Consultor IA: {e_switch}")
                                st.page_link("pages/2_🤖_Consultor_de_Riscos_IA.py", label="Analisar com Consultor IA", icon="🤖")
                else:
                    st.success("🎉 Nenhuma predição de risco significativa encontrada pela IA para esta folha!")
            
                if 'tipo_detalhe_predicao' in st.session_state and st.session_state.tipo_detalhe_predicao and \
                   st.session_state.get('id_folha_contexto_detalhe') == id_folha_selecionada: 

                    id_risco_foco_detalhe = st.session_state.get('detalhe_risco_selecionado_id')
                    tipo_detalhe_foco = st.session_state.tipo_detalhe_predicao

                    dados_detalhe_obj: Optional[DetalhePredicaoRiscoResponse] = None
                    try:
                        headers_det = {"Authorization": f"Bearer {api_token}"}
                        params_det: Dict[str, Any] = {"tipo_detalhe": tipo_detalhe_foco}
                        if tipo_detalhe_foco == "risco_especifico":
                            params_det["id_risco_detalhe"] = id_risco_foco_detalhe
                        
                        api_url_det = f"{settings.API_BASE_URL}/clientes/{id_cliente_para_api}/folhas/{id_folha_selecionada}/predicao-risco/detalhes"
                        logger.info(f"Buscando detalhes da predição: {api_url_det} com params: {params_det}")
                        
                        response_detalhes = requests.get(api_url_det, headers=headers_det, params=params_det)
                        if response_detalhes.status_code == 401: # Adicionado tratamento com handle_api_error
                            handle_api_error(response_detalhes.status_code)
                            st.rerun()
                            return # Parar execução aqui
                        response_detalhes.raise_for_status()
                        dados_detalhe_api = response_detalhes.json()
                        dados_detalhe_obj = DetalhePredicaoRiscoResponse(**dados_detalhe_api)
                    
                    except requests.exceptions.HTTPError as e_http_det:
                        logger.error(f"Erro HTTP ao buscar detalhes da predição: {e_http_det.response.status_code} - {e_http_det.response.text}")
                        # O tratamento de 401 foi movido para cima.
                        st.error(f"Não foi possível carregar os detalhes da predição ({e_http_det.response.status_code}).")
                    except requests.exceptions.RequestException as e_req_det:
                        logger.error(f"Erro de conexão ao buscar detalhes da predição: {e_req_det}")
                        st.error("Erro de conexão ao buscar detalhes da predição.")
                    except Exception as e_gen_det:
                        logger.error(f"Erro inesperado ao processar detalhes da predição: {e_gen_det}", exc_info=True)
                        st.error("Ocorreu um erro inesperado ao carregar os detalhes da predição.")

                    if dados_detalhe_obj:
                        titulo_expander = "🔍 Detalhes Aprofundados"
                        risco_selecionado_obj = dados_detalhe_obj.risco_selecionado 
                        if risco_selecionado_obj:
                            titulo_expander = f"🔍 Detalhes: {risco_selecionado_obj.descricao_risco}"
                        elif tipo_detalhe_foco == "score_geral":
                            titulo_expander = "🔍 Detalhes do Score de Saúde Geral"

                        with st.expander(titulo_expander, expanded=True):
                            st.markdown("**Explicação Detalhada (IA):**")
                            st.info(dados_detalhe_obj.explicacao_detalhada_ia)
                            
                            st.markdown("**Principais Fatores Técnicos Identificados:**")
                            if dados_detalhe_obj.fatores_contribuintes_tecnicos:
                                fatores_dumped = [f.model_dump() for f in dados_detalhe_obj.fatores_contribuintes_tecnicos]
                                df_fatores = pd.DataFrame(fatores_dumped)
                                if not df_fatores.empty:
                                    st.table(df_fatores[['feature', 'valor', 'atribuicao_impacto']])
                                else:
                                    st.caption("Nenhum fator técnico principal detalhado.")
                            else:
                                st.caption("Nenhum fator técnico principal detalhado.")

                            if dados_detalhe_obj.dados_suporte_visualizacao:
                                st.markdown("**Dados de Suporte para Contexto:**")
                                for visualizacao in dados_detalhe_obj.dados_suporte_visualizacao:
                                    st.caption(visualizacao.titulo_grafico or "Visualização de Dados")
                                    if visualizacao.tipo_grafico == "SERIE_TEMPORAL" and isinstance(visualizacao.dados, list):
                                        # Assegurar que os dados são formatados corretamente para st.line_chart
                                        # Exemplo: se visualizacao.dados for uma lista de dicts [{'x': val, 'y': val}]
                                        # ou um DataFrame pandas.
                                        try:
                                            df_chart = pd.DataFrame(visualizacao.dados)
                                            if not df_chart.empty and 'x' in df_chart.columns and 'y' in df_chart.columns:
                                                st.line_chart(df_chart.set_index('x')['y'])
                                            elif not df_chart.empty: # Tenta plotar a primeira coluna numérica se x,y não presentes
                                                st.line_chart(df_chart)
                                            else:
                                                st.caption("Dados de série temporal vazios ou malformados.")
                                        except Exception as e_chart:
                                            logger.error(f"Erro ao renderizar gráfico de série temporal: {e_chart}")
                                            st.caption("Não foi possível renderizar os dados da série temporal.")
                                    elif visualizacao.tipo_grafico == "VALOR_SIMPLES" and isinstance(visualizacao.dados, dict):
                                        st.metric(label=visualizacao.dados.get("label","Valor"), value=str(visualizacao.dados.get("valor", "N/A")))
                                    # Adicionar outros tipos de gráficos conforme necessário

                            if dados_detalhe_obj.recomendacoes_ia:
                                st.markdown("**Recomendações da IA:**")
                                for rec in dados_detalhe_obj.recomendacoes_ia:
                                    st.markdown(f"- {rec}")
                            
                            if st.button("Fechar Detalhes", key=f"fechar_detalhe_{id_risco_foco_detalhe}_{id_folha_selecionada}"):
                                st.session_state.tipo_detalhe_predicao = None
                                st.session_state.detalhe_risco_selecionado_id = None
                                st.session_state.id_folha_contexto_detalhe = None
                                st.rerun()
                
                if dados_predicao_obj and dados_predicao_obj.score_saude_folha is not None:
                    if st.button("Entender o Score de Saúde Geral", key=f"detail_score_geral_{id_folha_selecionada}"):
                        st.session_state.detalhe_risco_selecionado_id = "score_geral"
                        st.session_state.tipo_detalhe_predicao = "score_geral"
                        st.session_state.id_folha_contexto_detalhe = id_folha_selecionada
                        st.rerun()
        
        st.subheader("📊 Gerar Relatórios Exportáveis")
        opcoes_relatorio = {
            "Resumo da Saúde da Folha": "resumo_saude",
            "Detalhamento de Divergências": "detalhe_divergencias",
            "Análise Preditiva de Riscos (IA)": "predicao_riscos_ia"
        }
        
        # Adiciona opções de relatórios para usuários com papéis específicos
        if any(role in user_roles for role in ["admin", "auditor", "gerente"]):
            opcoes_relatorio.update({
                "Relatório Técnico Detalhado": "relatorio_tecnico_detalhado",
                "Análise de Tendência Histórica": "tendencia_historica"
            })
            
        # Opções exclusivas para administradores
        if "admin" in user_roles:
            opcoes_relatorio.update({
                "Auditoria Completa (Técnico)": "auditoria_tecnica_completa",
                "Relatório Gerencial Executivo": "relatorio_gerencial_executivo"
            })
        tipo_relatorio_selecionado = st.selectbox(
            "Selecione o tipo de relatório para gerar:",
            options=list(opcoes_relatorio.keys())
        )

        if st.button("Gerar e Baixar Relatório"):
            if tipo_relatorio_selecionado and id_folha_selecionada:
                codigo_relatorio = opcoes_relatorio[tipo_relatorio_selecionado]
                try:
                    headers_rel = {"Authorization": f"Bearer {api_token}"}
                    api_url_rel = f"{settings.API_BASE_URL}/clientes/{id_cliente_para_api}/folhas/{id_folha_selecionada}/relatorios/{codigo_relatorio}"
                    logger.info(f"Solicitando relatório: {api_url_rel}")
                    
                    response_rel = requests.get(api_url_rel, headers=headers_rel, stream=True) # stream=True para download
                    if response_rel.status_code == 401: # Adicionado tratamento com handle_api_error
                        handle_api_error(response_rel.status_code)
                        st.rerun()
                        return # Parar execução aqui
                    response_rel.raise_for_status()

                    # Tentar obter o nome do arquivo do header Content-Disposition
                    content_disposition = response_rel.headers.get('content-disposition')
                    filename = "relatorio.pdf" # Default
                    if content_disposition:
                        match = re.search(r'filename="?([^"]+)"?', content_disposition)
                        if match:
                            filename = match.group(1)
                    
                    # Corrigido para usar response_rel.content diretamente para bytes
                    st.download_button(
                        label="Clique para baixar o relatório",
                        data=response_rel.content, # .content para obter bytes
                        file_name=filename,
                        mime=response_rel.headers.get("content-type", "application/octet-stream") # Usar content-type do header se disponível
                    )
                    # st.success(f"Relatório '{tipo_relatorio_selecionado}' gerado. Clique no botão acima para baixar.") # Removido pois o botão de download já é a ação

                except requests.exceptions.HTTPError as e_http_rel:
                    logger.error(f"Erro HTTP ao gerar relatório: {e_http_rel.response.status_code} - {e_http_rel.response.text}")
                    if e_http_rel.response.status_code == 401:
                        st.warning("Sessão expirada. Faça login novamente.")
                        st.session_state.clear()
                        st.rerun()
                    else:
                        st.error(f"Erro ao gerar relatório ({e_http_rel.response.status_code}).")
                except requests.exceptions.RequestException as e_req_rel:
                    logger.error(f"Erro de conexão ao gerar relatório: {e_req_rel}")
                    st.error("Erro de conexão ao gerar relatório.")
                except Exception as e_gen_rel:
                    logger.error(f"Erro inesperado ao gerar relatório: {e_gen_rel}", exc_info=True)
                    st.error("Ocorreu um erro inesperado ao gerar o relatório.")
            else:
                st.warning("Selecione um tipo de relatório e uma folha válida.")

    else: # Se não houver dashboard_data (após tentativa de carregar ou se não clicou em carregar)
        if id_cliente_atual and api_token and label_selecionada: # Se tudo estiver pronto para carregar
             st.info("Clique em 'Carregar Dashboard' para visualizar os dados da folha selecionada.")
        elif not label_selecionada and folhas_disponiveis:
             st.info("Selecione um período da folha para começar.")

    # --- EXEMPLO DE INTEGRAÇÃO BACKEND VIA API ---
    st.markdown("---")
    st.title("Exemplo de Integração Backend via API")

    def get_folha_data():
        url = "http://localhost:8000/api/folha"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Erro ao buscar dados da folha: {e}")
            return {}

    if st.button("Carregar Dados do Exemplo"):
        with st.spinner("Buscando dados do exemplo..."):
            dados_exemplo = get_folha_data()
            if dados_exemplo:
                st.success("Dados do exemplo carregados com sucesso!")
                st.json(dados_exemplo)  # Exibe os dados em formato JSON
            else:
                st.warning("Nenhum dado encontrado no exemplo.")
