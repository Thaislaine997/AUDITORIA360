import streamlit as st
import sys # Add sys
import os # Add os

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) # Adjusted for pages subdir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

import requests
import json
import pandas as pd
from datetime import date 

from src.core.config import settings 
from src.frontend.utils import get_auth_headers, get_api_token, get_current_client_id, handle_api_error, display_user_info_sidebar

def mostrar_pagina_revisao_clausulas(): 
    st.set_page_config(layout="wide", page_title="Revisão de Cláusulas CCT - AUDITORIA360")

    # --- Logo ---
    logo_path = "assets/logo.png"
    try:
        st.logo(logo_path, link="https://auditoria360.com.br")
    except Exception as e:
        try:
            st.sidebar.image(logo_path, use_column_width=True)
            st.sidebar.markdown("[AUDITORIA360](https://auditoria360.com.br)")
        except Exception:
            st.sidebar.warning(f"Não foi possível carregar o logo: {logo_path}")
        st.sidebar.warning(f"Não foi possível carregar o logo principal: {e}. Usando fallback na sidebar.")
    st.sidebar.markdown("---")

    api_token = get_api_token()
    id_cliente_atual = get_current_client_id() 

    if not api_token: 
        st.warning("Por favor, faça login para acessar esta página.")
        st.link_button("Ir para Login", "/")
        st.stop()

    display_user_info_sidebar()

    st.title("🔍 Revisão de Cláusulas Extraídas de CCTs")

    st.sidebar.header("Filtros avançados")
    tipo_clausula = st.sidebar.text_input("Tipo de cláusula", key="rev_tipo_clausula")
    status_revisao = st.sidebar.selectbox("Status revisão", ["", "PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"], key="rev_status") 
    id_cct_doc = st.sidebar.text_input("ID Documento CCT", key="rev_id_cct") 
    data_inicial_filtro = st.sidebar.date_input("Data extração inicial", value=None, key="rev_data_inicial")
    data_final_filtro = st.sidebar.date_input("Data extração final", value=None, key="rev_data_final")

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
        resp = requests.get(f"{settings.API_BASE_URL}/api/v1/clausulas/revisao", headers=get_auth_headers(api_token), params=params)
        if resp.status_code == 401:
            handle_api_error(resp.status_code)
            st.rerun()
            return
        resp.raise_for_status()
        clausulas = resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar cláusulas para revisão: {e}")
    except json.JSONDecodeError:
        st.error("Erro ao decodificar a resposta da API (não é um JSON válido).")
        if hasattr(resp, 'text'):
            st.code(resp.text) 
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao buscar cláusulas: {e}")

    if not clausulas:
        st.info("Nenhuma cláusula encontrada com os filtros aplicados ou pendente de revisão.")
    
    if clausulas: 
        df = pd.DataFrame(clausulas)
        if not df.empty:
            st.subheader("Dashboard de Revisão")
            pendentes = int((df["status_revisao_humana"] == "PENDENTE").sum()) if "status_revisao_humana" in df.columns else 0
            aprovadas = int((df["status_revisao_humana"] == "APROVADA").sum()) if "status_revisao_humana" in df.columns else 0
            ajustadas = int((df["status_revisao_humana"] == "AJUSTADA").sum()) if "status_revisao_humana" in df.columns else 0
            rejeitadas = int((df["status_revisao_humana"] == "REJEITADA").sum()) if "status_revisao_humana" in df.columns else 0
            
            col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
            col_metric1.metric("Pendentes", pendentes)
            col_metric2.metric("Aprovadas", aprovadas)
            col_metric3.metric("Ajustadas", ajustadas)
            col_metric4.metric("Rejeitadas", rejeitadas)
            
            if "tipo_clausula_identificada" in df.columns and not df["tipo_clausula_identificada"].empty:
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
            st.text_area("Texto da Cláusula", value=clausula.get('texto_clausula_extraido', 'Texto não disponível.'), height=200, disabled=True, key=f"text_{clausula.get('id_clausula_extraida', i)}")
            
            col_info1, col_info2 = st.columns(2)
            col_info1.info(f"Página no Documento: {clausula.get('pagina_aproximada_documento', 'N/A')}")
            col_info2.info(f"Status Atual: {clausula.get('status_revisao_humana', 'N/A')}")

            st.markdown(f"**Palavras-chave:** `{', '.join(clausula.get('palavras_chave_clausula', []) or [])}`")
            
            with st.form(key=f"form_revisao_{clausula.get('id_clausula_extraida', i)}"):
                novo_status_revisao = st.selectbox(
                    "Novo status da revisão", 
                    ["PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"], 
                    index=["PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"].index(clausula.get('status_revisao_humana', "PENDENTE")) if clausula.get('status_revisao_humana') in ["PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"] else 0,
                    key=f"sel_status_{clausula.get('id_clausula_extraida', i)}"
                )
                notas_revisor = st.text_area(
                    "Notas do revisor", 
                    value=clausula.get("notas_revisao_humana") or "", 
                    key=f"notas_{clausula.get('id_clausula_extraida', i)}"
                )
                texto_ajustado = st.text_area(
                    "Texto ajustado da cláusula (se status for AJUSTADA)",
                    value=clausula.get('texto_clausula_extraido', ''), 
                    height=150,
                    key=f"texto_ajustado_{clausula.get('id_clausula_extraida', i)}"
                )

                submitted = st.form_submit_button("Salvar revisão")

                if submitted:
                    payload = {
                        "status_revisao_humana": novo_status_revisao,
                        "usuario_revisao_humana": st.session_state.get("user_info", {}).get("username", "admin_revisor"), 
                        "notas_revisao_humana": notas_revisor,
                        "texto_clausula_ajustado": texto_ajustado if novo_status_revisao == "AJUSTADA" else None 
                    }
                    payload = {k: v for k, v in payload.items() if v is not None}

                    try:
                        put_resp = requests.put(
                            f"{settings.API_BASE_URL}/api/v1/clausulas/{clausula.get('id_clausula_extraida')}", 
                            json=payload,
                            headers=get_auth_headers(api_token)
                        )
                        if put_resp.status_code == 401:
                            handle_api_error(put_resp.status_code)
                            st.rerun() 
                        elif put_resp.status_code == 200: 
                            st.success(f"Revisão da cláusula {clausula.get('id_clausula_extraida')} salva com sucesso!")
                            st.rerun() 
                        else:
                            st.error(f"Erro ao salvar revisão (Cód: {put_resp.status_code}): {put_resp.text}")
                    except requests.exceptions.RequestException as e_put:
                        st.error(f"Erro de conexão ao salvar revisão: {e_put}")
                    except Exception as e_put_general:
                        st.error(f"Erro inesperado ao salvar revisão: {e_put_general}")

if __name__ == "__main__":
    if "api_token" not in st.session_state:
        st.session_state.api_token = "token_simulado_revisao_clausulas" 
    if "id_cliente" not in st.session_state: 
        st.session_state.id_cliente = "cliente_simulado_revisao_123"
    if "user_info" not in st.session_state:
        st.session_state.user_info = {"nome": "Revisor Teste", "empresa": "Empresa Teste", "username": "revisor_teste"}
    
    mostrar_pagina_revisao_clausulas()
