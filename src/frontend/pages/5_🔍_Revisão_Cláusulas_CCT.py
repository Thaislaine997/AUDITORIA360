import streamlit as st
import requests
import json
import pandas as pd

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")

st.title("Revisão de Cláusulas Extraídas de CCTs")

if 'jwt_token' not in st.session_state:
    st.info("Faça login na página principal para acessar a revisão de cláusulas.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['jwt_token']}"}

st.sidebar.header("Filtros avançados")
tipo_clausula = st.sidebar.text_input("Tipo de cláusula")
status = st.sidebar.selectbox("Status revisão", ["", "PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"])
id_cct = st.sidebar.text_input("ID CCT")
data_inicial = st.sidebar.date_input("Data inicial", value=None)
data_final = st.sidebar.date_input("Data final", value=None)

params = {}
if tipo_clausula:
    params["tipo_clausula"] = tipo_clausula
if status:
    params["status"] = status
if id_cct:
    params["id_cct"] = id_cct
if data_inicial:
    params["data_inicial"] = str(data_inicial)
if data_final:
    params["data_final"] = str(data_final)

resp = requests.get(f"{API_BASE_URL}/api/v1/ccts/clausulas/revisao", headers=headers, params=params)
if resp.status_code != 200:
    st.error("Erro ao buscar cláusulas para revisão.")
    st.stop()
clausulas = resp.json()
if not clausulas:
    st.info("Nenhuma cláusula pendente de revisão.")
    st.stop()

# Dashboard de revisão
df = pd.DataFrame(clausulas)
if not df.empty:
    st.subheader("Dashboard de Revisão")
    st.metric("Pendentes", int((df.status_revisao_humana == "PENDENTE").sum()))
    st.metric("Aprovadas", int((df.status_revisao_humana == "APROVADA").sum()))
    st.metric("Ajustadas", int((df.status_revisao_humana == "AJUSTADA").sum()))
    st.metric("Rejeitadas", int((df.status_revisao_humana == "REJEITADA").sum()))
    st.bar_chart(df["tipo_clausula_identificada"].value_counts())

for clausula in clausulas:
    with st.expander(f"{clausula['tipo_clausula_identificada'] or 'Cláusula'} | CCT: {clausula['id_cct_documento_fk']}"):
        st.write(f"**Texto extraído:**\n{clausula['texto_clausula_extraido']}")
        st.write(f"**Página:** {clausula.get('pagina_aproximada_documento', '-')}")
        st.write(f"**Palavras-chave:** {', '.join(clausula.get('palavras_chave_clausula', []) or [])}")
        st.write(f"**Status atual:** {clausula['status_revisao_humana']}")
        novo_status = st.selectbox("Novo status", ["PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"], index=["PENDENTE", "APROVADA", "AJUSTADA", "REJEITADA"].index(clausula['status_revisao_humana']))
        notas = st.text_area("Notas do revisor", value=clausula.get("notas_revisao_humana") or "")
        if st.button("Salvar revisão", key=clausula['id_clausula_extraida']):
            payload = {
                "status_revisao_humana": novo_status,
                "usuario_revisao_humana": st.session_state.get("username", "admin"),
                "notas_revisao_humana": notas
            }
            put_resp = requests.put(
                f"{API_BASE_URL}/api/v1/ccts/clausulas/{clausula['id_clausula_extraida']}",
                json=payload,
                headers=headers
            )
            if put_resp.status_code == 200:
                st.success("Revisão salva com sucesso!")
            else:
                st.error("Erro ao salvar revisão.")
