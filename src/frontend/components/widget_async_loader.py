# Widget para carregamento assíncrono
import streamlit as st
import time

def async_loader(message="Carregando..."):
    with st.spinner(message):
        time.sleep(1)
        st.success("Carregamento concluído!")
