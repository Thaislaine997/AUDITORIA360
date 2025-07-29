# Widget para carregamento assíncrono
import time

import streamlit as st


def async_loader(message="Carregando..."):
    with st.spinner(message):
        time.sleep(1)
        st.success("Carregamento concluído!")
