import streamlit as st

st.set_page_config(layout="wide", page_title="Revisão de Cláusulas CCT - AUDITORIA360")

import os  # Add os
import sys  # Add sys

# --- Path Setup ---
_project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)  # Adjusted for pages subdir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---


# --- Carregamento do CSS para Design System ---
def load_css():
    css_path = os.path.join(_project_root, "assets", "style.css")
    if not os.path.exists(css_path):
        css_path = "/workspaces/AUDITORIA360/assets/style.css"
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()  # Carrega os estilos do Design System
# --- Fim do Carregamento do CSS ---

import json

import pandas as pd
import requests

from configs.settings import settings

# Ajustar import para usar os utilitários globais de forma consistente
from dashboards.utils import (
    display_user_info_sidebar as global_display_user_info_sidebar,
)
from dashboards.utils import get_api_token as get_global_api_token
from dashboards.utils import (
    get_auth_headers as get_global_auth_headers,  # Importar get_auth_headers global
)
from dashboards.utils import get_current_client_id as get_global_current_client_id
from dashboards.utils import (
    handle_api_error,
)
from services.core.log_utils import logger  # Corrigido caminho do logger

# Use global functions directly - no need for local wrappers
get_api_token = get_global_api_token
get_current_client_id = get_global_current_client_id
display_user_info_sidebar = global_display_user_info_sidebar


def get_auth_headers_revisao():  # Wrapper local para headers
    token = get_api_token()
    return get_global_auth_headers(token)  # Chama o global com o token


def mostrar_pagina_revisao_clausulas():
    # --- Logo --- (Removido, display_user_info_sidebar cuida disso)
    # st.sidebar.markdown("---") # Removido

    api_token = get_api_token()
    id_cliente_atual = get_current_client_id()

    if (
        not api_token or not id_cliente_atual
    ):  # Adicionado id_cliente_atual na verificação
        st.warning("Por favor, faça login para acessar esta página.")
        if st.button("Retornar ao Login"):
            try:
                st.switch_page("painel.py")
            except (
                AttributeError
            ):  # Para versões mais antigas do Streamlit ou se painel.py não for a página principal
                st.page_link("painel.py", label="Retornar ao Login", icon="🏠")
            except Exception as e:  # Fallback genérico
                st.page_link("painel.py", label="Retornar ao Login", icon="🏠")
                logger.warning(
                    f"Falha ao usar st.switch_page para painel.py: {e}, usando page_link."
                )
        st.stop()

    display_user_info_sidebar()

    st.title("🔍 Revisão de Cláusulas Extraídas de CCTs")
    st.caption(f"Cliente ID: {id_cliente_atual}")

    st.sidebar.header("Filtros avançados")
    tipo_clausula = st.sidebar.text_input("Tipo de cláusula", key="rev_tipo_clausula")
    status_revisao = st.sidebar.selectbox(
        "Status revisão",
        ["", "PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"],
        key="rev_status",
    )
    id_cct_doc = st.sidebar.text_input("ID Documento CCT", key="rev_id_cct")
    data_inicial_filtro = st.sidebar.date_input(
        "Data extração inicial", value=None, key="rev_data_inicial"
    )
    data_final_filtro = st.sidebar.date_input(
        "Data extração final", value=None, key="rev_data_final"
    )

    params = {}
    if tipo_clausula:
        params["tipo_clausula_identificada_contem"] = tipo_clausula
    if status_revisao:
        params["status_revisao_humana"] = status_revisao
    if id_cct_doc:
        params["id_cct_documento_fk"] = id_cct_doc
    if data_inicial_filtro:
        params["data_extracao_gte"] = data_inicial_filtro.isoformat()
    if data_final_filtro:
        params["data_extracao_lte"] = data_final_filtro.isoformat()

    clausulas = []
    try:
        # Usar get_auth_headers_revisao()
        resp = requests.get(
            f"{settings.API_BASE_URL}/api/v1/clausulas/revisao",
            headers=get_auth_headers_revisao(),
            params=params,
        )
        if resp.status_code == 401:
            handle_api_error(resp.status_code)
            st.rerun()
            return
        resp.raise_for_status()
        clausulas = resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar cláusulas para revisão: {e}")
        logger.error(
            f"Erro ao buscar cláusulas para revisão: {e}", exc_info=True
        )  # Adicionado logger
    except json.JSONDecodeError:
        st.error("Erro ao decodificar a resposta da API (não é um JSON válido).")
        logger.error(
            f"Erro ao decodificar JSON da busca de cláusulas: {resp.text if 'resp' in locals() else 'Resposta não disponível'}",
            exc_info=True,
        )  # Adicionado logger
        if hasattr(resp, "text"):
            st.code(resp.text)
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao buscar cláusulas: {e}")
        logger.error(
            f"Erro inesperado na busca de cláusulas: {e}", exc_info=True
        )  # Adicionado logger

    if not clausulas:
        st.info(
            "Nenhuma cláusula encontrada com os filtros aplicados ou pendente de revisão."
        )

    if clausulas:
        df = pd.DataFrame(clausulas)
        if not df.empty:
            st.subheader("Dashboard de Revisão")
            pendentes = (
                int((df["status_revisao_humana"] == "PENDENTE").sum())
                if "status_revisao_humana" in df.columns
                else 0
            )
            aprovadas = (
                int((df["status_revisao_humana"] == "APROVADA").sum())
                if "status_revisao_humana" in df.columns
                else 0
            )
            ajustadas = (
                int((df["status_revisao_humana"] == "AJUSTADA").sum())
                if "status_revisao_humana" in df.columns
                else 0
            )
            rejeitadas = (
                int((df["status_revisao_humana"] == "REJEITADA").sum())
                if "status_revisao_humana" in df.columns
                else 0
            )

            col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
            col_metric1.metric("Pendentes", pendentes)
            col_metric2.metric("Aprovadas", aprovadas)
            col_metric3.metric("Ajustadas", ajustadas)
            col_metric4.metric("Rejeitadas", rejeitadas)

            if (
                "tipo_clausula_identificada" in df.columns
                and not df["tipo_clausula_identificada"].empty
            ):
                st.bar_chart(df["tipo_clausula_identificada"].value_counts())
            else:
                st.caption("Dados de tipo de cláusula indisponíveis para o gráfico.")
    else:
        st.subheader("Dashboard de Revisão")
        st.caption("Nenhuma cláusula para exibir no dashboard.")

    for i, clausula in enumerate(clausulas):
        exp_title = f"Cláusula ID: {clausula.get('id_clausula_extraida', 'N/A')} | Tipo: {clausula.get('tipo_clausula_identificada', 'N/D')} | CCT: {clausula.get('id_cct_documento_fk', 'N/A')}"
        with st.expander(exp_title):
            st.markdown(f"**Texto extraído:**")
            st.text_area(
                "Texto da Cláusula",
                value=clausula.get("texto_clausula_extraido", "Texto não disponível."),
                height=200,
                disabled=True,
                key=f"text_{clausula.get('id_clausula_extraida', i)}",
            )

            col_info1, col_info2 = st.columns(2)
            col_info1.info(
                f"Página no Documento: {clausula.get('pagina_aproximada_documento', 'N/A')}"
            )
            col_info2.info(
                f"Status Atual: {clausula.get('status_revisao_humana', 'N/A')}"
            )

            st.markdown(
                f"**Palavras-chave:** `{', '.join(clausula.get('palavras_chave_clausula', []) or [])}`"
            )

            with st.form(key=f"form_revisao_{clausula.get('id_clausula_extraida', i)}"):
                novo_status_revisao = st.selectbox(
                    "Novo status da revisão",
                    ["PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"],
                    index=(
                        ["PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"].index(
                            clausula.get("status_revisao_humana", "PENDENTE")
                        )
                        if clausula.get("status_revisao_humana")
                        in ["PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"]
                        else 0
                    ),
                    key=f"sel_status_{clausula.get('id_clausula_extraida', i)}",
                )
                notas_revisor = st.text_area(
                    "Notas do revisor",
                    value=clausula.get("notas_revisao_humana") or "",
                    key=f"notas_{clausula.get('id_clausula_extraida', i)}",
                )
                texto_ajustado = st.text_area(
                    "Texto ajustado da cláusula (se status for AJUSTADA)",
                    value=clausula.get("texto_clausula_extraido", ""),
                    height=150,
                    key=f"texto_ajustado_{clausula.get('id_clausula_extraida', i)}",
                )

                submitted = st.form_submit_button("Salvar revisão")

                if submitted:
                    payload = {
                        "status_revisao_humana": novo_status_revisao,
                        "usuario_revisao_humana": st.session_state.get(
                            "user_info", {}
                        ).get("username", "admin_revisor"),
                        "notas_revisao_humana": notas_revisor,
                        "texto_clausula_ajustado": (
                            texto_ajustado
                            if novo_status_revisao == "AJUSTADA"
                            else None
                        ),
                    }
                    payload = {k: v for k, v in payload.items() if v is not None}

                    try:
                        put_resp = requests.put(
                            f"{settings.API_BASE_URL}/api/v1/clausulas/{clausula.get('id_clausula_extraida')}",
                            json=payload,
                            headers=get_auth_headers_revisao(),  # Usar get_auth_headers_revisao()
                        )
                        if put_resp.status_code == 401:
                            handle_api_error(put_resp.status_code)
                            st.rerun()
                        elif put_resp.status_code == 200:
                            st.success(
                                f"Revisão da cláusula {clausula.get('id_clausula_extraida')} salva com sucesso!"
                            )
                            logger.info(
                                f"Revisão da cláusula {clausula.get('id_clausula_extraida')} salva."
                            )  # Adicionado logger
                            st.rerun()
                        else:
                            st.error(
                                f"Erro ao salvar revisão (Cód: {put_resp.status_code}): {put_resp.text}"
                            )
                            logger.error(
                                f"Erro HTTP ao salvar revisão cláusula {clausula.get('id_clausula_extraida')}: {put_resp.status_code} - {put_resp.text}"
                            )  # Adicionado logger
                    except requests.exceptions.RequestException as e_put:
                        st.error(f"Erro de conexão ao salvar revisão: {e_put}")
                        logger.error(
                            f"Erro de conexão ao salvar revisão cláusula {clausula.get('id_clausula_extraida')}: {e_put}",
                            exc_info=True,
                        )  # Adicionado logger
                    except Exception as e_put_general:
                        st.error(f"Erro inesperado ao salvar revisão: {e_put_general}")
                        logger.error(
                            f"Erro inesperado ao salvar revisão cláusula {clausula.get('id_clausula_extraida')}: {e_put_general}",
                            exc_info=True,
                        )  # Adicionado logger

    # --- Código de exemplo para integração backend via API ---
    st.title("Revisão de Cláusulas CCT")

    def obter_token():
        return st.text_input("Token JWT", type="password")

    def get_clausulas(token):
        url = "http://localhost:8000/api/clausulas"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), url, headers
        except Exception as e:
            st.error(f"Erro ao buscar cláusulas: {e}")
            return [], url, headers

    token = obter_token()
    if token:
        clausulas, url, headers = get_clausulas(token)
        filtro = st.text_input("Buscar por cláusula")
        clausulas_filtradas = [
            c for c in clausulas if filtro.lower() in c.get("descricao", "").lower()
        ]
        st.write(clausulas_filtradas)
        with st.form("Adicionar Cláusula"):
            descricao = st.text_input("Descrição")
            tipo = st.text_input("Tipo")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                payload = {"descricao": descricao, "tipo": tipo}
                resp = requests.post(url, json=payload, headers=headers)
                if resp.status_code == 201:
                    st.success("Cláusula adicionada com sucesso!")
                else:
                    st.error(f"Erro ao adicionar cláusula: {resp.text}")
    else:
        st.warning("Informe o token JWT para acessar os dados.")
    # --- Fim do Código de exemplo ---


if __name__ == "__main__":
    # Simulação do st.session_state para fins de teste local
    if "token" not in st.session_state:  # Alterado de api_token para token
        st.session_state.token = "token_simulado_revisao_clausulas"
    if "client_id" not in st.session_state:  # Alterado de id_cliente para client_id
        st.session_state.client_id = "cliente_simulado_revisao_123"
    if "user_info" not in st.session_state:
        st.session_state.user_info = {
            "name": "Revisor Teste",
            "username": "revisor_teste",
        }

    mostrar_pagina_revisao_clausulas()
