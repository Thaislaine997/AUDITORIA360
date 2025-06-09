import streamlit as st
import sys # Add sys
import os # Add os

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) # Adjusted for pages subdir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

# src/pages/consultor_riscos_page.py
import requests
from src.core.config import settings
from src.frontend.utils import get_auth_headers, get_api_token, get_current_client_id, handle_api_error

def display_user_info_sidebar():
    """Exibe informações do usuário na barra lateral."""
    if "user_info" in st.session_state and st.session_state.user_info:
        user_info = st.session_state.user_info
        st.sidebar.markdown("---")
        st.sidebar.subheader(f"Usuário: {user_info.get('nome', 'N/A')}")
        st.sidebar.caption(f"Empresa: {user_info.get('empresa', 'N/A')}")
        st.sidebar.caption(f"ID Cliente: {st.session_state.get('id_cliente', 'N/A')}")
    else:
        st.sidebar.markdown("---")
        st.sidebar.caption("Informações do usuário não disponíveis.")

def consultor_riscos_page():
    st.set_page_config(layout="wide", page_title="Consultor de Riscos - AUDITORIA360")

    # --- Logo ---
    logo_path = "assets/logo.png" # Caminho simplificado
    try:
        st.logo(logo_path, link="https://auditoria360.com.br")
    except Exception as e:
        st.sidebar.image(logo_path, use_column_width=True)
        st.sidebar.markdown("[AUDITORIA360](https://auditoria360.com.br)")
        st.sidebar.warning(f"Não foi possível carregar o logo principal: {e}. Usando fallback na sidebar.")
    st.sidebar.markdown("---")

    api_token = get_api_token()
    id_cliente_atual = get_current_client_id()

    if not api_token or not id_cliente_atual:
        st.warning("Por favor, faça login para acessar esta página.")
        st.link_button("Ir para Login", "/") # Assumindo que a página de login é a raiz
        st.stop()

    display_user_info_sidebar()

    st.title("Consultor de Riscos Interativo 💬")

    # Inicializa o histórico do chat no session_state se não existir
    if "risks_messages" not in st.session_state: # Usar uma chave específica para esta página
        st.session_state.risks_messages = []

    # Exibe as mensagens do histórico
    for message in st.session_state.risks_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do usuário
    if prompt := st.chat_input("Faça sua pergunta sobre riscos trabalhistas..."):
        # Adiciona a mensagem do usuário ao histórico e exibe
        st.session_state.risks_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Lógica para chamar o backend e obter a resposta da IA
        with st.chat_message("assistant"):
            try:
                payload = {
                    "query": prompt,
                    "client_id": id_cliente_atual
                }
                # Endpoint da API para o consultor de riscos (ajustar conforme necessário)
                api_url = f"{settings.API_BASE_URL}/api/v1/risks/consult" # Exemplo de endpoint
                
                headers = get_auth_headers(api_token)
                response = requests.post(api_url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    api_response_data = response.json()
                    # Ajuste a chave conforme a resposta real da sua API
                    assistant_response = api_response_data.get("response", "Não foi possível obter uma resposta do consultor.") 
                elif response.status_code == 401:
                    handle_api_error(response.status_code)
                    st.rerun()
                    return # Adicionado para evitar processamento adicional
                else:
                    assistant_response = f"Erro ao contatar o consultor: {response.status_code} - {response.text}"
                
                st.markdown(assistant_response)
                # Adiciona a resposta do assistente ao histórico
                st.session_state.risks_messages.append({"role": "assistant", "content": assistant_response})

            except requests.exceptions.RequestException as e:
                st.error(f"Erro de conexão ao tentar contatar o consultor: {e}")
                assistant_response = "Desculpe, não consegui me conectar ao serviço de consultoria."
                # Não adiciona ao histórico de mensagens se houve erro de conexão
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")
                assistant_response = "Ocorreu um erro inesperado ao processar sua solicitação."
                # Não adiciona ao histórico de mensagens se houve erro inesperado

if __name__ == "__main__":
    # Simulação do st.session_state para fins de teste local
    # Remova ou comente estas linhas em produção ou quando integrado
    if "api_token" not in st.session_state:
        st.session_state.api_token = "token_simulado_para_teste" 
    if "id_cliente" not in st.session_state:
        st.session_state.id_cliente = "cliente_simulado_123"
    if "user_info" not in st.session_state:
        st.session_state.user_info = {"nome": "Usuário Teste", "empresa": "Empresa Teste"}
    # Inicializa 'risks_messages' também para o teste standalone
    if "risks_messages" not in st.session_state:
        st.session_state.risks_messages = []

    consultor_riscos_page()
