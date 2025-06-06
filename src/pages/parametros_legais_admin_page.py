import streamlit as st
import requests

st.set_page_config(page_title="Administração de Parâmetros Legais", layout="wide")
st.title("Administração de Parâmetros Legais (INSS, IRRF, Salário Família, Salário Mínimo, FGTS)")

API_URL = st.secrets.get("API_URL") or "http://localhost:8000"

aba = st.selectbox("Escolha o parâmetro para gerenciar:", ["INSS", "IRRF", "Salário Família", "Salário Mínimo", "FGTS"])

if aba == "INSS":
    st.header("Histórico de Parâmetros INSS")
    if st.button("Listar Parâmetros INSS"):
        r = requests.get(f"{API_URL}/api/v1/parametros-legais-admin/inss")
        if r.status_code == 200:
            st.dataframe(r.json())
        else:
            st.error("Erro ao buscar parâmetros INSS.")
    with st.form("Novo INSS"):
        id_parametro_inss = st.text_input("ID Parâmetro INSS")
        data_inicio = st.date_input("Data Início Vigência")
        valor = st.text_input("Descrição/Valor")
        submitted = st.form_submit_button("Criar")
        if submitted:
            payload = {"id_parametro_inss": id_parametro_inss, "data_inicio_vigencia": str(data_inicio), "descricao": valor}
            r = requests.post(f"{API_URL}/api/v1/parametros-legais-admin/inss", json=payload)
            if r.status_code == 200:
                st.success("Parâmetro INSS criado!")
            else:
                st.error("Erro ao criar parâmetro INSS.")
# (Repetir para IRRF, Salário Família, Salário Mínimo, FGTS)
