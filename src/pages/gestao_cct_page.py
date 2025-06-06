# src/pages/gestao_cct_page.py
"""
Página Streamlit para Gestão de Convenções Coletivas de Trabalho (CCTs)
"""
import streamlit as st
import requests
import json
from datetime import date

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")

# --- Login ---
if 'jwt_token' not in st.session_state:
    st.session_state['jwt_token'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'is_authenticated' not in st.session_state:
    st.session_state['is_authenticated'] = False

with st.expander('🔐 Login para ações administrativas', expanded=not st.session_state['is_authenticated']):
    username = st.text_input('Usuário', value=st.session_state['username'])
    password = st.text_input('Senha', type='password')
    if st.button('Entrar'):
        if not username or not password:
            st.warning('Preencha usuário e senha.')
        else:
            try:
                resp = requests.post(f"{API_BASE_URL}/auth/token", data={
                    'username': username,
                    'password': password
                })
                if resp.status_code == 200:
                    token = resp.json().get('access_token')
                    st.session_state['jwt_token'] = token
                    st.session_state['username'] = username
                    st.session_state['is_authenticated'] = True
                    st.success('Login realizado com sucesso!')
                else:
                    st.session_state['jwt_token'] = None
                    st.session_state['is_authenticated'] = False
                    st.error('Usuário ou senha inválidos.')
            except Exception as e:
                st.error(f'Erro ao autenticar: {e}')

if not st.session_state['is_authenticated']:
    st.info('Faça login para acessar upload e monitoramento de alertas.')

# Função principal para renderizar a página de gestão de CCTs
def mostrar_pagina_gestao_cct():
    st.title("🗂️ Gestão de Convenções Coletivas de Trabalho (CCTs)")

    tab_upload, tab_listar, tab_monitor = st.tabs([
        "📤 Upload de CCT",
        "🔎 Listar/Buscar CCTs",
        "⚙️ Monitoramento de Alertas"
    ])

    # Aba de Upload
    with tab_upload:
        if not st.session_state['is_authenticated']:
            st.warning('Login obrigatório para upload de CCT.')
        else:
            st.subheader("📤 Upload de Novo Documento de CCT/Aditivo")
            with st.form("form_upload_cct", clear_on_submit=True):
                nome = st.text_input("Nome Documento CCT")
                arquivo = st.file_uploader("Arquivo (PDF/DOCX)", type=["pdf", "docx"])
                data_inicio = st.date_input("Data Início Vigência", value=date.today())
                data_fim = st.date_input("Data Fim Vigência (opcional)", value=None)
                sind_laborais = st.text_area("Sindicato(s) Laboral(is)")
                sind_patronais = st.text_area("Sindicato(s) Patronal(is)")
                numero_reg = st.text_input("Nº Registro MTE")
                link_fonte = st.text_input("Link Fonte Oficial")
                id_base = st.text_input("ID CCT Base (opcional)")
                ids_afetados = st.text_input("IDs Clientes Afetados (JSON lista)")
                submit_btn = st.form_submit_button("Salvar Documento CCT")
                if submit_btn:
                    if not nome or not arquivo:
                        st.warning("Nome e arquivo são obrigatórios.")
                    else:
                        payload = {
                            "nome_documento_original": nome,
                            "data_inicio_vigencia_cct": data_inicio.isoformat(),
                            "data_fim_vigencia_cct": data_fim.isoformat() if data_fim else None,
                            "sindicatos_laborais_json_str": json.dumps([s.strip() for s in sind_laborais.split("\n") if s.strip()]) if sind_laborais else None,
                            "sindicatos_patronais_json_str": json.dumps([s.strip() for s in sind_patronais.split("\n") if s.strip()]) if sind_patronais else None,
                            "numero_registro_mte": numero_reg,
                            "link_fonte_oficial": link_fonte,
                            "id_cct_base_fk": id_base or None,
                            "ids_clientes_afetados_lista_str": ids_afetados or None
                        }
                        files = {"file": (arquivo.name, arquivo.getvalue(), arquivo.type)}
                        headers = {"Authorization": f"Bearer {st.session_state['jwt_token']}"}
                        try:
                            resp = requests.post(
                                f"{API_BASE_URL}/api/v1/ccts/upload",
                                data=payload,
                                files=files,
                                headers=headers
                            )
                            resp.raise_for_status()
                            data = resp.json()
                            st.success(f"CCT enviada com sucesso! ID: {data.get('id_cct_documento')}")
                        except Exception as e:
                            st.error(f"Erro ao enviar CCT: {e}")

    # Aba de Listar/Buscar CCTs
    with tab_listar:
        st.subheader("🔎 Listar e Buscar CCTs")
        # Filtros de busca
        col1, col2, col3 = st.columns(3)
        cliente_filter = col1.text_input("ID Cliente Afetado", key="filter_cliente")
        sindicato_filter = col2.text_input("Filtro Sindicato (nome)", key="filter_sindicato")
        data_filter = col3.date_input("Data Vigência em", value=None, key="filter_data")
        if st.button("Buscar CCTs"):
            params = {}
            if cliente_filter:
                params["id_cliente_afetado"] = cliente_filter
            if sindicato_filter:
                params["sindicato_nome_contem"] = sindicato_filter
            if data_filter:
                params["data_vigencia_em"] = data_filter.isoformat()
            try:
                resp = requests.get(f"{API_BASE_URL}/api/v1/ccts", params=params)
                resp.raise_for_status()
                ccts = resp.json()
            except Exception as e:
                st.error(f"Erro ao buscar CCTs: {e}")
                ccts = []
            if not ccts:
                st.info("Nenhuma CCT encontrada.")
            else:
                import pandas as pd
                # Montar DataFrame para exibição
                table_data = []
                for doc in ccts:
                    table_data.append({
                        "ID": doc.get("id_cct_documento"),
                        "Nome": doc.get("nome_documento_original"),
                        "Início Vigência": doc.get("data_inicio_vigencia_cct"),
                        "Fim Vigência": doc.get("data_fim_vigencia_cct", "-"),
                        "Sind. Laborais": ", ".join(json.loads(doc.get("sindicatos_laborais_json_str", "[]"))),
                        "Sind. Patronais": ", ".join(json.loads(doc.get("sindicatos_patronais_json_str", "[]"))),
                        "Status IA": doc.get("status_processamento_ia"),
                        "Download": f'[Baixar]({doc.get("gcs_uri_documento")})'
                    })
                df = pd.DataFrame(table_data)
                st.markdown("**Resultados:**")
                st.write("Clique em 'Baixar' para acessar o documento.")
                st.write(df.to_markdown(index=False), unsafe_allow_html=True)

    # Aba de Monitoramento de Alertas
    with tab_monitor:
        if not st.session_state['is_authenticated']:
            st.warning('Login obrigatório para monitorar e atualizar alertas.')
        else:
            st.subheader("⚙️ Monitoramento de Alertas de Novas CCTs")
            status_filter = st.selectbox(
                "Filtrar status de alerta",
                options=["TODOS", "NOVO", "EM_REVISAO_ADMIN", "CCT_IMPORTADA", "DESCARTADO"],
                key="status_filter"
            )
            params = {}
            if status_filter and status_filter != "TODOS":
                params["status"] = status_filter
            try:
                response = requests.get(f"{API_BASE_URL}/api/v1/ccts/alerts", params=params)
                response.raise_for_status()
                alerts = response.json()
            except Exception as e:
                st.error(f"Erro ao buscar alertas: {e}")
                alerts = []

            if not alerts:
                st.info("Nenhum alerta encontrado.")
            else:
                for alert in alerts:
                    with st.expander(f"Alerta {alert['id_alerta_cct']} (Status: {alert['status_alerta']})"):
                        st.markdown(f"**Registro MTE:** {alert.get('numero_registro_mte_detectado', '-')}")
                        st.markdown(f"**Vigência Início:** {alert.get('vigencia_inicio_detectada', '-')}")
                        st.markdown(f"**Sindicato(s):** {alert.get('sindicatos_partes_detectados', '-')}")
                        st.markdown(f"**Detectado em:** {alert.get('data_deteccao', '-')}")
                        new_status = st.selectbox(
                            "Novo status",
                            options=["CCT_IMPORTADA", "DESCARTADO"],
                            key=f"status_{alert['id_alerta_cct']}"
                        )
                        notes = st.text_area(
                            "Notas do Admin",
                            key=f"notes_{alert['id_alerta_cct']}"
                        )
                        if st.button("Atualizar Alerta", key=f"btn_{alert['id_alerta_cct']}"):
                            headers = {"Authorization": f"Bearer {st.session_state['jwt_token']}"}
                            try:
                                put_resp = requests.put(
                                    f"{API_BASE_URL}/api/v1/ccts/alerts/{alert['id_alerta_cct']}",
                                    json={"status_alerta": new_status, "notas_admin": notes},
                                    headers=headers
                                )
                                put_resp.raise_for_status()
                                st.success("Alerta atualizado com sucesso.")
                                st.info("Atualização concluída. Recarregue a página para ver as mudanças.")
                            except Exception as e:
                                st.error(f"Erro ao atualizar alerta: {e}")
