import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Carregamento das credenciais
with open("config_login.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login("main", "Login")

if st.session_state["authentication_status"]:
    user = st.session_state["username"]
    role = config["credentials"]["usernames"][user].get("role", "USER")

    st.sidebar.success(f"Bem-vindo, {user}")
    authenticator.logout("Sair", "sidebar")

    aba = st.sidebar.radio("Menu", ["Auditoria", "Histórico", "Usuários (Admin)"] if role == "ADMIN" else ["Auditoria", "Histórico"])

    if aba == "Auditoria":
        st.title("📥 Nova Auditoria")
        st.write("Área para envio de CCT e Extrato PDF")
        # upload, processamento, dossiê, chat...

    elif aba == "Histórico":
        st.title("🗃️ Histórico de Auditorias")
        st.write("Resultados anteriores com filtros por mês/empresa")

    elif aba == "Usuários (Admin)":
        st.title("👤 Gerenciamento de Usuários")
        st.write("Cadastro, redefinição e controle de acesso")

else:
    st.warning("Faça login para continuar.")
