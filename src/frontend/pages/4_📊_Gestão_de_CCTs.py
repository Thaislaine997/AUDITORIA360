import streamlit as st
import sys # Add sys
import os # Add os

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) # Adjusted for pages subdir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

# filepath: c:\\Users\\55479\\Documents\\AUDITORIA360\\src\\frontend\\pages\\4_📊_Gestão_de_CCTs.py
# src/pages/gestao_cct_page.py
"""
Página Streamlit para Gestão de Convenções Coletivas de Trabalho (CCTs)
"""
st.set_page_config(layout="wide", page_title="Gestão de CCTs - AUDITORIA360")

import requests
import json
import os
from datetime import date
import pandas as pd # Importar pandas no início

from src.core.config import settings
from src.frontend.utils import get_auth_headers, get_api_token, get_current_client_id, handle_api_error, display_user_info_sidebar

# Remover a lógica de login local daqui

# Função principal para renderizar a página de gestão de CCTs
def mostrar_pagina_gestao_cct():
    # st.set_page_config(layout="wide", page_title="Gestão de CCTs - AUDITORIA360") # Movido para o topo

    # --- Logo ---
    logo_path = "assets/logo.png" 
    try:
        st.logo(logo_path, link="https://auditoria360.com.br")
    except Exception as e:
        try:
            st.sidebar.image(logo_path, use_column_width=True)
            st.sidebar.markdown("[AUDITORIA360](https://auditoria360.com.br)")
        except Exception: # Se st.sidebar.image também falhar
             st.sidebar.warning(f"Não foi possível carregar o logo: {logo_path}")
        st.sidebar.warning(f"Não foi possível carregar o logo principal: {e}. Usando fallback na sidebar.")
    st.sidebar.markdown("---")
    
    api_token = get_api_token()
    id_cliente_atual = get_current_client_id()

    if not api_token or not id_cliente_atual:
        st.warning("Por favor, faça login para acessar esta página.")
        st.link_button("Ir para Login", "/") 
        st.stop()

    display_user_info_sidebar() # Exibe informações do usuário autenticado

    st.title("🗂️ Gestão de Convenções Coletivas de Trabalho (CCTs)")

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
                    payload = {
                        "nome_documento_original": nome,
                        "data_inicio_vigencia_cct": data_inicio.isoformat(),
                        "data_fim_vigencia_cct": data_fim.isoformat() if data_fim else None,
                        "sindicatos_laborais_json_str": json.dumps([s.strip() for s in sind_laborais.split("\\n") if s.strip()]) if sind_laborais else None,
                        "sindicatos_patronais_json_str": json.dumps([s.strip() for s in sind_patronais.split("\\n") if s.strip()]) if sind_patronais else None,
                        "numero_registro_mte": numero_reg,
                        "link_fonte_oficial": link_fonte,
                        "id_cct_base_fk": id_base or None,
                        "ids_clientes_afetados_lista_str": ids_afetados or json.dumps([id_cliente_atual]) # Garante que o cliente atual seja incluído se não especificado
                    }
                    files = {"file": (arquivo.name, arquivo.getvalue(), arquivo.type)}
                    
                    try:
                        resp = requests.post(
                            f"{settings.API_BASE_URL}/api/v1/ccts/upload",
                            data=payload,
                            files=files,
                            headers=get_auth_headers(api_token)
                        )
                        if resp.status_code == 401:
                            handle_api_error(resp.status_code)
                            st.rerun()
                            return
                        resp.raise_for_status()
                        data = resp.json()
                        st.success(f"CCT enviada com sucesso! ID: {data.get('id_cct_documento')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erro ao enviar CCT: {e}")
                    except Exception as e: # Captura outras exceções, como JSONDecodeError
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
            
            try:
                resp = requests.get(f"{settings.API_BASE_URL}/api/v1/ccts", params=params, headers=get_auth_headers(api_token))
                if resp.status_code == 401:
                    handle_api_error(resp.status_code)
                    st.rerun()
                    return
                resp.raise_for_status()
                ccts = resp.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Erro ao buscar CCTs: {e}")
                ccts = []
            except Exception as e:
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

        try:
            response = requests.get(f"{settings.API_BASE_URL}/api/v1/ccts/alerts", params=params, headers=get_auth_headers(api_token))
            if response.status_code == 401:
                handle_api_error(response.status_code)
                st.rerun()
                return
            response.raise_for_status()
            alerts = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar alertas: {e}")
            alerts = []
        except Exception as e:
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
                        try:
                            put_resp = requests.put(
                                f"{settings.API_BASE_URL}/api/v1/ccts/alerts/{alert.get('id_alerta_cct')}",
                                json={"status_alerta": new_status, "notas_admin": notes, "id_cliente": id_cliente_atual}, # Enviar id_cliente para auditoria/lógica de negócios no backend
                                headers=get_auth_headers(api_token)
                            )
                            if put_resp.status_code == 401:
                                handle_api_error(put_resp.status_code)
                                st.rerun()
                                return
                            put_resp.raise_for_status()
                            st.success(f"Alerta {alert.get('id_alerta_cct')} atualizado com sucesso.")
                            st.rerun() # Para refletir as mudanças na lista
                        except requests.exceptions.RequestException as e:
                            st.error(f"Erro ao atualizar alerta {alert.get('id_alerta_cct')}: {e}")
                        except Exception as e:
                            st.error(f"Erro inesperado ao processar a atualização do alerta: {e}")
                            
if __name__ == "__main__":
    # Simulação do st.session_state para fins de teste local
    if "api_token" not in st.session_state:
        st.session_state.api_token = "token_simulado_para_teste_cct" 
    if "id_cliente" not in st.session_state:
        st.session_state.id_cliente = "cliente_simulado_cct_123"
    if "user_info" not in st.session_state:
        st.session_state.user_info = {"nome": "Usuário Teste CCT", "empresa": "Empresa Teste CCT"}
    
    mostrar_pagina_gestao_cct()
