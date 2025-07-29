import streamlit as st
from filters import sidebar_filters

st.set_page_config(page_title="Auditoria360", layout="wide")
st.title("Dashboard Auditoria de Folha + ML")

periodo, entidade, status_anomalia = sidebar_filters()
st.write(f"Filtros selecionados: {periodo}, {entidade}, {status_anomalia}")

# Exemplo de métrica
st.metric("Documentos processados", 123)
st.metric("Anomalias detectadas", 5)
