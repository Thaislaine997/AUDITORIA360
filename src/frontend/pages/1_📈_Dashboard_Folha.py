# src/dashboard_folha_page.py

import streamlit as st
import pandas as pd
import requests
from datetime import date
from decimal import Decimal
import logging
from typing import Optional, Any, Dict, List
import re

from schemas import (
    PredicaoRiscoDashboardResponse,
    DetalhePredicaoRiscoResponse,
    RiscoPrevistoDetalheSchema,
    FatorContribuinteTecnicoSchema,
    DadosSuporteVisualizacaoSchema
)

logger = logging.getLogger(__name__)

APP_ROOT_URL = st.secrets.get("APP_ROOT_URL", "http://localhost:8000")
API_BASE_URL_V1 = f"{APP_ROOT_URL}/api/v1"
AUTH_API_BASE_URL = f"{APP_ROOT_URL}/auth"


def initialize_session_state():
    if 'api_token' not in st.session_state:
        st.session_state.api_token = None
    if 'logged_in_client_id' not in st.session_state:
        st.session_state.logged_in_client_id = None
    if 'logged_in_username' not in st.session_state:
        st.session_state.logged_in_username = None
    if 'client_id_simulated' not in st.session_state:
        st.session_state.client_id_simulated = None
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

def login_user(username, password) -> bool:
    try:
        response = requests.post(
            f"{AUTH_API_BASE_URL}/token",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        token_data = response.json()
        st.session_state.api_token = token_data["access_token"]

        headers = {"Authorization": f"Bearer {st.session_state.api_token}"}
        user_info_response = requests.get(f"{AUTH_API_BASE_URL}/users/me/", headers=headers)
        user_info_response.raise_for_status()
        user_info = user_info_response.json()
        
        st.session_state.logged_in_username = user_info.get("username")
        st.session_state.logged_in_client_id = user_info.get("id_contabilidade") 
        
        st.session_state.client_id_simulated = None 
        logger.info(f"Usuário {username} logado com sucesso. Client ID: {st.session_state.logged_in_client_id}")
        return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.error("Login falhou: Usuário ou senha incorretos.")
        else:
            st.error(f"Erro de login: {e.response.status_code} - {e.response.text}")
        logger.error(f"Falha no login para {username}: {e}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão durante o login: {e}")
        logger.error(f"Erro de conexão no login para {username}: {e}")
    except Exception as e_gen:
        st.error(f"Ocorreu um erro inesperado durante o login: {e_gen}")
        logger.error(f"Erro inesperado no login para {username}: {e_gen}", exc_info=True)
    return False

def logout_user():
    st.session_state.api_token = None
    st.session_state.logged_in_client_id = None
    st.session_state.logged_in_username = None
    st.success("Logout realizado com sucesso!")
    st.rerun()

def get_current_client_id() -> Optional[str]:
    if st.session_state.get("logged_in_client_id"):
        return st.session_state.logged_in_client_id
    if st.session_state.get("client_id_simulated"):
        return st.session_state.client_id_simulated
    
    query_params = st.query_params
    client_id_param = query_params.get("client_id")
    if client_id_param:
        actual_client_id = client_id_param[0] if isinstance(client_id_param, list) else client_id_param
        return actual_client_id
    return None

def get_api_token() -> Optional[str]:
    return st.session_state.get("api_token")

def buscar_folhas_processadas_cliente(id_cliente: str, token: Optional[str]) -> list:
    headers: Dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    api_url = f"{API_BASE_URL_V1}/clientes/{id_cliente}/folhas-processadas"
    logger.info(f"Buscando folhas processadas: {api_url} com token: {'Sim' if token else 'Não'}")

    try:
        response = requests.get(api_url, headers=headers)
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
        if e_http.response.status_code == 401:
            st.warning("Sessão expirada ou inválida. Por favor, faça login novamente.")
            logout_user()
        else:
            st.error(f"Erro ao buscar folhas processadas ({e_http.response.status_code}): {detail}")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão ao buscar folhas processadas: {e}")
        return []
    except Exception as e_json:
        st.error(f"Erro ao processar resposta das folhas: {e_json}")
        return []

def mostrar_dashboard_saude_folha():
    st.title("🏥 Dashboard de Saúde da Folha Mensal")
    
    api_token = get_api_token()
    id_cliente_atual = get_current_client_id()

    # Configurações da Sidebar
    if api_token and st.session_state.get("logged_in_username"):
        st.sidebar.success(f"Logado como: {st.session_state.logged_in_username}")
        st.sidebar.caption(f"Cliente ID: {st.session_state.logged_in_client_id}")
        if st.sidebar.button("Logout"):
            logout_user()
        st.sidebar.markdown("---")
        st.sidebar.subheader("Configurações de Desenvolvedor")
        st.sidebar.text_input(
            "Simular Client ID:", 
            value=st.session_state.get("client_id_simulated", ""),
            disabled=True,
            help="Faça logout para simular um Client ID.",
            key="dev_client_id_input_disabled"
        )
        st.sidebar.button("Aplicar Client ID Simulado", disabled=True, key="dev_apply_sim_id_disabled")

    else: 
        st.sidebar.markdown("---")
        st.sidebar.subheader("Configurações de Desenvolvedor")
        dev_client_id_input = st.sidebar.text_input(
            "Simular Client ID (apenas se não logado):", 
            value=st.session_state.get("client_id_simulated", ""),
            disabled=False,
            key="dev_client_id_input_enabled"
        )
        if st.sidebar.button("Aplicar Client ID Simulado", disabled=False, key="dev_apply_sim_id_enabled"):
            st.session_state.client_id_simulated = dev_client_id_input
            st.session_state.logged_in_client_id = None 
            st.session_state.api_token = None
            st.session_state.logged_in_username = None
            st.rerun()

    # Conteúdo Principal
    if not api_token:
        st.subheader("Login Necessário")
        with st.form("login_form_main"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if login_user(username, password):
                    st.rerun() 
        
        if not id_cliente_atual:
            st.info("Por favor, faça login para acessar o dashboard ou simule um Client ID usando as Configurações de Desenvolvedor na barra lateral.")
        else: 
            st.info(f"Visualizando com Client ID simulado: {id_cliente_atual}. Faça login para acesso completo.")
        return 

    if not st.session_state.get("logged_in_client_id"):
        st.error("Erro: Logado mas Client ID não encontrado. Tente fazer login novamente.")
        logout_user()
        return

    id_cliente_para_api = st.session_state.logged_in_client_id

    folhas_disponiveis = buscar_folhas_processadas_cliente(id_cliente_para_api, api_token)
    if not folhas_disponiveis:
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
            api_url = f"{API_BASE_URL_V1}/clientes/{id_cliente_para_api}/folhas/{id_folha_selecionada}/dashboard-saude"
            logger.info(f"Chamando API do dashboard: {api_url} com token: Sim")
            response = requests.get(api_url, headers=headers)
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
            if e_http.response.status_code == 401:
                st.warning("Sessão expirada ou inválida. Por favor, faça login novamente.")
                logout_user()
            else:
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
                    api_url_pred = f"{API_BASE_URL_V1}/clientes/{id_cliente_para_api}/folhas/{id_folha_selecionada}/predicao-risco"
                    logger.info(f"Buscando dados de predição de risco: {api_url_pred}")
                    response_pred = requests.get(api_url_pred, headers=headers_pred)
                    response_pred.raise_for_status()
                    dados_predicao_api = response_pred.json()
                    dados_predicao_obj = PredicaoRiscoDashboardResponse(**dados_predicao_api)
                    st.session_state.predicao_risco_data = dados_predicao_obj
                except requests.exceptions.HTTPError as e_http_pred:
                    logger.error(f"Erro HTTP ao buscar dados de predição: {e_http_pred.response.status_code} - {e_http_pred.response.text}")
                    if e_http_pred.response.status_code == 404:
                        st.info("Análise preditiva de riscos ainda não disponível para esta folha.")
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
                    # Iterar sobre os objetos RiscoPrevistoDetalheSchema já desserializados
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
                            st.info(f"Simulando navegação para Consultor IA com foco em: {risco.descricao_risco}")
                else:
                    st.success("🎉 Nenhuma predição de risco significativa encontrada pela IA para esta folha!")
            
                # Lógica para exibir detalhes SE um risco ou score geral foi selecionado para detalhamento
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
                        
                        api_url_det = f"{API_BASE_URL_V1}/clientes/{id_cliente_para_api}/folhas/{id_folha_selecionada}/predicao-risco/detalhes"
                        logger.info(f"Buscando detalhes da predição: {api_url_det} com params: {params_det}")
                        
                        response_detalhes = requests.get(api_url_det, headers=headers_det, params=params_det)
                        response_detalhes.raise_for_status()
                        dados_detalhe_api = response_detalhes.json()
                        # Correção: Assegurar que os sub-objetos também sejam desserializados
                        dados_detalhe_obj = DetalhePredicaoRiscoResponse(**dados_detalhe_api)
                    
                    except requests.exceptions.HTTPError as e_http_det:
                        logger.error(f"Erro HTTP ao buscar detalhes da predição: {e_http_det.response.status_code} - {e_http_det.response.text}")
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
                                        st.line_chart(visualizacao.dados)
                                    elif visualizacao.tipo_grafico == "VALOR_SIMPLES" and isinstance(visualizacao.dados, dict):
                                        st.metric(label=visualizacao.dados.get("label","Valor"), value=str(visualizacao.dados.get("valor", "N/A")))

                            if dados_detalhe_obj.recomendacoes_ia:
                                st.markdown("**Recomendações da IA:**")
                                for rec in dados_detalhe_obj.recomendacoes_ia:
                                    st.markdown(f"- {rec}")
                            
                            if st.button("Fechar Detalhes", key=f"fechar_detalhe_{id_risco_foco_detalhe}_{id_folha_selecionada}"):
                                st.session_state.tipo_detalhe_predicao = None
                                st.session_state.detalhe_risco_selecionado_id = None
                                st.session_state.id_folha_contexto_detalhe = None
                                st.rerun()
                
                # Botão para ver detalhes do Score Geral (colocado após a lista de riscos)
                if dados_predicao_obj and dados_predicao_obj.score_saude_folha is not None:
                    if st.button("Entender o Score de Saúde Geral", key=f"detail_score_geral_{id_folha_selecionada}"):
                        st.session_state.detalhe_risco_selecionado_id = "score_geral" 
                        st.session_state.tipo_detalhe_predicao = "score_geral"
                        st.session_state.id_folha_contexto_detalhe = id_folha_selecionada
                        st.rerun()
        
        st.subheader("📊 Gerar Relatórios Exportáveis")
        opcoes_relatorio = {
            "Relatório de Divergências Completo": "divergencias_completo",
            "Relatório de Conferência de Encargos": "conferencia_encargos",
            "Relatório de Composição de Bases (Sistema)": "composicao_bases_sistema",
        }
        nome_relatorio_display = st.selectbox("Selecione o Relatório:", list(opcoes_relatorio.keys()))
        col_formato1, col_formato2 = st.columns(2)
        formato_selecionado = col_formato1.radio("Formato:", ["CSV", "XLSX"], horizontal=True, index=0)
        nome_relatorio_api = opcoes_relatorio[nome_relatorio_display]
        formato_api = formato_selecionado.lower()

        if col_formato2.button(f"Gerar e Baixar {formato_selecionado}", key=f"btn_gerar_{nome_relatorio_api}_{formato_api}"):
            with st.spinner(f"Gerando relatório '{nome_relatorio_display}' em {formato_selecionado}..."):
                try:
                    headers_rel = {}
                    if api_token:
                        headers_rel["Authorization"] = f"Bearer {api_token}"
                    
                    api_url_rel = f"{API_BASE_URL_V1}/clientes/{id_cliente_para_api}/folhas/{id_folha_selecionada}/relatorios/{nome_relatorio_api}?formato={formato_api}"
                    logger.info(f"Chamando API de relatório: {api_url_rel} com token: Sim")
                    response_rel = requests.get(api_url_rel, headers=headers_rel, stream=True)
                    response_rel.raise_for_status()

                    content_disposition = response_rel.headers.get('content-disposition')
                    filename_from_header = f"relatorio_{nome_relatorio_api}_{id_folha_selecionada}.{formato_api}" 
                    if content_disposition:
                        fn_match = re.search(r'filename=([^;]+)', content_disposition, flags=re.IGNORECASE)
                        if fn_match:
                            filename_from_header = fn_match.group(1).strip(' \'"')
                    
                    dados_arquivo_bytes = response_rel.content
                    st.download_button(
                        label=f"Clique para baixar {filename_from_header}",
                        data=dados_arquivo_bytes,
                        file_name=filename_from_header,
                        mime=response_rel.headers.get('content-type', "application/octet-stream"),
                        key=f"download_{nome_relatorio_api}_{formato_api}_{id_folha_selecionada}"
                    )
                    st.success(f"Relatório '{nome_relatorio_display}' ({formato_selecionado}) gerado. Use o botão acima para baixar.")
                except requests.exceptions.HTTPError as e_http_rel:
                    logger.error(f"Erro HTTP ao gerar relatório: {e_http_rel.response.status_code} - {e_http_rel.response.text}", exc_info=True)
                    detail_rel = "Erro desconhecido"
                    try:
                        detail_rel = e_http_rel.response.json().get("detail", e_http_rel.response.text)
                    except requests.exceptions.JSONDecodeError:
                        detail_rel = e_http_rel.response.text
                    if e_http_rel.response.status_code == 401:
                        st.warning("Sessão expirada ou inválida. Por favor, faça login novamente.")
                        logout_user()
                    else:
                        st.error(f"Erro ao gerar relatório ({e_http_rel.response.status_code}): {detail_rel}")
                except requests.exceptions.RequestException as e_req_rel:
                    logger.error(f"Erro de requisição ao gerar relatório: {e_req_rel}", exc_info=True)
                    st.error(f"Erro de conexão ao gerar relatório: {e_req_rel}")
                except Exception as e_gen_rel:
                    logger.error(f"Erro inesperado ao gerar relatório: {e_gen_rel}", exc_info=True)
                    st.error(f"Ocorreu um erro inesperado ao gerar o relatório: {e_gen_rel}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    st.set_page_config(layout="wide", page_title="Dashboard Folha")
    
    initialize_session_state()
    
    mostrar_dashboard_saude_folha()
