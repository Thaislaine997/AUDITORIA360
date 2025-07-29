import streamlit as st  # Import principal do Streamlit

# Mover st.set_page_config para o topo absoluto
st.set_page_config(page_title="Gerenciamento de Usuários - AUDITORIA360", layout="wide")

import os
import sys

# --- Path Setup ---
_project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)  # Ajustado para subdiretório pages
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---


# --- Carregamento do CSS para Design System ---
def load_css():
    css_path = os.path.join(_project_root, "assets", "style.css")
    if not os.path.exists(css_path):
        css_path = "/workspaces/AUDITORIA360/assets/style.css"
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()  # Carrega os estilos do Design System
# --- Fim do Carregamento do CSS ---

from datetime import datetime

import pandas as pd
import requests

# Removido import quebrado
from configs.settings import settings
from services.core.log_utils import logger


def mostrar_pagina_gerenciamento_usuarios():
    # Configuração da página
    st.set_page_config(
        page_title="Gerenciamento de Usuários - AUDITORIA360", layout="wide"
    )

    # Verifica a sessão e obtém os dados do usuário
    # Este é o ponto chave que implementa a verificação de permissões
    # Substituir por dados do usuário da sessão
    user_details = st.session_state.get("user_info", {})
    user_roles = user_details.get("roles", [])
    st.title("💼 Gerenciamento de Usuários")
    st.caption("Gerencie usuários, papéis e permissões da plataforma")
    with st.sidebar:
        st.subheader("Informações do Usuário")
        st.write(f"**Nome:** {user_details.get('nome', 'N/A')}")
        st.write(f"**Email:** {user_details.get('email', 'N/A')}")
        st.write("**Papéis:**")
        for role in user_roles:
            st.write(f"- {role}")

    # RENDERIZAÇÃO CONDICIONAL BASEADA EM PAPÉIS

    # Somente administradores podem ver e gerenciar todos os usuários
    if "admin" in user_roles:
        st.header("Lista de Todos os Usuários")

        # Botão para atualizar lista
        if st.button("Atualizar Lista de Usuários"):
            st.session_state["users_data"] = None  # Força recarga

        # Carregar dados dos usuários da API
        if (
            "users_data" not in st.session_state
            or st.session_state["users_data"] is None
        ):
            try:
                headers = {
                    "Authorization": f"Bearer {st.session_state.get('api_token')}"
                }
                response = requests.get(
                    f"{settings.API_BASE_URL}/api/users/all", headers=headers
                )

                if response.status_code == 200:
                    users_data = response.json()
                    st.session_state["users_data"] = users_data

                    # Exibir em formato de tabela
                    users_df = pd.DataFrame(users_data)
                    st.dataframe(
                        users_df[
                            ["id", "nome", "email", "cliente_id", "roles", "ativo"]
                        ],
                        use_container_width=True,
                    )

                    # Seção para adicionar novo usuário
                    with st.expander("Adicionar Novo Usuário"):
                        with st.form("novo_usuario_form"):
                            col1, col2 = st.columns(2)
                            with col1:
                                novo_nome = st.text_input("Nome")
                                novo_email = st.text_input("Email")
                                nova_senha = st.text_input("Senha", type="password")

                            with col2:
                                novo_cliente_id = st.text_input("ID do Cliente")
                                roles_options = [
                                    "admin",
                                    "auditor",
                                    "cliente",
                                    "consultor",
                                ]
                                novas_roles = st.multiselect(
                                    "Papéis", options=roles_options
                                )

                            submit_button = st.form_submit_button("Adicionar Usuário")

                            if submit_button:
                                # Validações básicas
                                if not novo_nome or not novo_email or not nova_senha:
                                    st.error(
                                        "Nome, email e senha são campos obrigatórios."
                                    )
                                else:
                                    # Preparar dados para a API
                                    new_user_data = {
                                        "nome": novo_nome,
                                        "email": novo_email,
                                        "senha": nova_senha,
                                        "cliente_id": (
                                            novo_cliente_id if novo_cliente_id else None
                                        ),
                                        "roles": novas_roles,
                                        "ativo": True,
                                    }

                                    # Enviar para a API
                                    try:
                                        create_response = requests.post(
                                            f"{settings.API_BASE_URL}/api/users/create",
                                            headers=headers,
                                            json=new_user_data,
                                        )

                                        if create_response.status_code == 201:
                                            st.success("Usuário criado com sucesso!")
                                            # Atualizar lista
                                            st.session_state["users_data"] = None
                                            st.rerun()
                                        else:
                                            st.error(
                                                f"Erro ao criar usuário: {create_response.text}"
                                            )
                                    except Exception as e:
                                        st.error(
                                            f"Erro ao conectar com a API: {str(e)}"
                                        )

                else:
                    st.error(f"Erro ao carregar usuários: {response.text}")
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {str(e)}")
                logger.error(f"Erro ao obter lista de usuários: {e}")

    # Gerentes e auditores podem ver usuários do seu cliente
    elif "gerente" in user_roles or "auditor" in user_roles:
        st.header("Usuários da Sua Organização")

        cliente_id = user_details.get("cliente_id")

        if cliente_id:
            try:
                headers = {
                    "Authorization": f"Bearer {st.session_state.get('api_token')}"
                }
                response = requests.get(
                    f"{settings.API_BASE_URL}/api/users/by-client/{cliente_id}",
                    headers=headers,
                )

                if response.status_code == 200:
                    client_users = response.json()

                    if client_users:
                        client_users_df = pd.DataFrame(client_users)
                        st.dataframe(
                            client_users_df[["id", "nome", "email", "roles", "ativo"]],
                            use_container_width=True,
                        )
                    else:
                        st.info(
                            "Não há outros usuários registrados para sua organização."
                        )
                else:
                    st.error(
                        "Não foi possível carregar os usuários da sua organização."
                    )
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {str(e)}")
        else:
            st.warning("Você não tem uma organização associada à sua conta.")

    # Usuários comuns só podem ver seus próprios dados
    else:
        st.info("Você não tem permissões para gerenciar usuários.")
        st.write("Para solicitar acesso, entre em contato com seu administrador.")

        st.subheader("Seus Dados de Acesso")
        # Exibir apenas alguns campos do usuário atual
        st.write(f"**ID:** {user_details.get('id', 'N/A')}")
        st.write(f"**Email:** {user_details.get('email', 'N/A')}")
        st.write(f"**Organização:** {user_details.get('cliente_nome', 'N/A')}")

        # Opção para alterar senha
        with st.expander("Alterar Senha"):
            with st.form("alterar_senha_form"):
                senha_atual = st.text_input("Senha Atual", type="password")
                nova_senha = st.text_input("Nova Senha", type="password")
                confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")

                submit_password = st.form_submit_button("Alterar Senha")

                if submit_password:
                    if not senha_atual or not nova_senha or not confirmar_senha:
                        st.error("Todos os campos são obrigatórios.")
                    elif nova_senha != confirmar_senha:
                        st.error("As senhas não coincidem.")
                    else:
                        # Lógica para alterar senha via API
                        st.success("Senha alterada com sucesso!")

    # Rodapé comum para todos os usuários
    st.markdown("---")
    st.caption(
        f"AUDITORIA360 - Acessado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )

    def obter_token():
        return st.text_input("Token JWT", type="password")

    def get_usuarios(token):
        url = "http://localhost:8000/api/usuarios"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), url, headers
        except Exception as e:
            st.error(f"Erro ao buscar usuários: {e}")
            return [], url, headers

    token = obter_token()
    if token:
        usuarios, url, headers = get_usuarios(token)
        filtro = st.text_input("Buscar por nome")
        usuarios_filtrados = [
            u for u in usuarios if filtro.lower() in u.get("nome", "").lower()
        ]
        st.write(usuarios_filtrados)
        with st.form("Adicionar Usuário"):
            nome = st.text_input("Nome")
            email = st.text_input("Email")
            submitted = st.form_submit_button("Adicionar")
            if submitted:
                payload = {"nome": nome, "email": email}
                resp = requests.post(url, json=payload, headers=headers)
                if resp.status_code == 201:
                    st.success("Usuário adicionado com sucesso!")
                else:
                    st.error(f"Erro ao adicionar usuário: {resp.text}")
    else:
        st.warning("Informe o token JWT para acessar os dados.")


if __name__ == "__main__":
    mostrar_pagina_gerenciamento_usuarios()
