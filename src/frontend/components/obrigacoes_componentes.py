# Componente de obrigações para uso em dashboards/pages/5_🗓️_Obrigações_e_Prazos.py
import streamlit as st

def mostrar_obrigacoes(obrigacoes):
    st.subheader("Lista de Obrigações")
    for o in obrigacoes:
        st.write(f"Descrição: {o.get('descricao', '')} | Prazo: {o.get('prazo', '')}")
