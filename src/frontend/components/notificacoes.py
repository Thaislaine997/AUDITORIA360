# Componente de notificações para uso em dashboards/pages/notificacoes.py
import streamlit as st

def exibir_notificacoes(lista):
    st.subheader("Notificações")
    for n in lista:
        st.info(n)
