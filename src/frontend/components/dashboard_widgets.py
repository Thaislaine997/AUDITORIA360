# Widgets para dashboard personalizado
import streamlit as st

def exibir_widget_tabela(dados):
    st.table(dados)

def exibir_widget_grafico(dados):
    st.line_chart(dados)
