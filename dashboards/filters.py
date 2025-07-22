import streamlit as st

def sidebar_filters():
    st.sidebar.header('Filtros')
    periodo = st.sidebar.date_input('Período')
    entidade = st.sidebar.selectbox('Tipo de entidade', ['Todos', 'Nome', 'CPF', 'Salário', 'Descontos'])
    status_anomalia = st.sidebar.selectbox('Status de anomalia', ['Todos', 'Normal', 'Anomalia'])
    return periodo, entidade, status_anomalia
