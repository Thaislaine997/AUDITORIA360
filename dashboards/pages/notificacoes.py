"""
Página de notificações do sistema AUDITORIA360.
"""

import os
import sys

import streamlit as st

# --- Path Setup ---
_project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)  # Adjusted for pages subdir
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

from src.frontend.auth_verify import verify_session
from src.frontend.components.notificacoes import exibir_aba_notificacoes

# Configurar a página
st.set_page_config(
    page_title="Notificações - AUDITORIA360",
    page_icon="🔔",
    layout="wide",
)

# Verificar a sessão (e exibir o sino)
user_details = verify_session()

# Título da página
st.title("📬 Central de Notificações")
st.write("Visualize e gerencie todas as suas notificações do sistema.")

# Exibir notificações
exibir_aba_notificacoes()

# Sidebar (botões de navegação já exibidos por auth_verify)
