# src/pages/consultor_riscos_page.py
import streamlit as st
from datetime import datetime

def consultor_riscos_page():
    st.title("Consultor de Riscos Interativo 💬")

    # Inicializa o histórico do chat no session_state se não existir
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe as mensagens do histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do usuário
    if prompt := st.chat_input("Faça sua pergunta sobre riscos trabalhistas..."):
        # Adiciona a mensagem do usuário ao histórico e exibe
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Aqui virá a lógica para chamar o backend e obter a resposta da IA
        # Por enquanto, vamos simular uma resposta do assistente
        with st.chat_message("assistant"):
            response = f"Eco: {prompt}" # Simples eco por enquanto
            st.markdown(response)
        # Adiciona a resposta do assistente ao histórico
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    consultor_riscos_page()
