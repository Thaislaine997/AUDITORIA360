# src/checklist_page.py
import streamlit as st
import requests
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

# Configuração básica de logging
logger = logging.getLogger(__name__)

# Constantes (ajuste conforme necessário)
API_BASE_URL = "http://localhost:8000/api/v1" # Ou a URL da sua API FastAPI

# Funções de utilidade da sessão (podem ser movidas para um utils_streamlit.py comum)
def initialize_session_state_checklist():
    """Inicializa o estado da sessão para a página de checklist."""
    if "authenticated_checklist" not in st.session_state:
        st.session_state.authenticated_checklist = False
    if "user_checklist" not in st.session_state:
        st.session_state.user_checklist = None # Armazenará o objeto User
    if "checklist_items" not in st.session_state:
        st.session_state.checklist_items = []
    if "id_folha_processada_checklist" not in st.session_state:
        st.session_state.id_folha_processada_checklist = ""
    if "checklist_client_id" not in st.session_state: # Adicionado para armazenar o id_cliente
        st.session_state.checklist_client_id = ""
    if "dica_ia_cache" not in st.session_state:
        st.session_state.dica_ia_cache = {} # Cache para dicas de IA: {id_item: dica}

def get_api_token() -> Optional[str]:
    return st.session_state.get("api_token")

def get_logged_in_client_id() -> Optional[str]:
    return st.session_state.get("logged_in_client_id")

def get_current_folha_id_for_checklist() -> Optional[str]:
    return st.session_state.get("current_folha_id_for_checklist")

def set_current_folha_id_for_checklist(folha_id: Optional[str]):
    st.session_state.current_folha_id_for_checklist = folha_id

# Funções de interação com a API do Checklist
def fetch_checklist_items(id_cliente: str, id_folha_processada: str):
    """Busca os itens do checklist da API."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist",
            headers=get_auth_headers() # Adicionar cabeçalhos de autenticação
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar checklist: {e}")
        if e.response is not None:
            st.error(f"Detalhes: {e.response.text}")
        return None

def update_checklist_item_api(id_cliente: str, id_folha_processada: str, id_item_checklist: str, updates: dict):
    """Atualiza um item do checklist via API."""
    try:
        response = requests.put(
            f"{API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist/{id_item_checklist}",
            json=updates,
            headers=get_auth_headers() # Adicionar cabeçalhos de autenticação
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao atualizar item do checklist: {e}")
        if e.response is not None:
            st.error(f"Detalhes: {e.response.text}")
        return None

def mark_sheet_as_closed_api(id_cliente: str, id_folha_processada: str):
    """Marca a folha como fechada via API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/marcar-fechada",
            headers=get_auth_headers() # Adicionar cabeçalhos de autenticação
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao marcar folha como fechada: {e}")
        if e.response is not None:
            st.error(f"Detalhes: {e.response.text}")
        return None

def get_dica_ia_api(id_cliente: str, id_folha_processada: str, id_item_checklist: str, descricao_item: str):
    """Busca dica de IA para um item do checklist."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist/dica-ia",
            params={"id_item_checklist": id_item_checklist, "descricao_item": descricao_item},
            headers=get_auth_headers() # Adicionar cabeçalhos de autenticação
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dica de IA: {e}")
        if e.response is not None:
            st.error(f"Detalhes: {e.response.text}")
        return None

def fetch_folhas_disponiveis_para_checklist(id_cliente: str):
    """Busca as folhas processadas disponíveis para checklist para o cliente."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/clientes/{id_cliente}/folhas-processadas/disponiveis-para-checklist",
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar folhas disponíveis: {e}")
        if e.response is not None:
            st.error(f"Detalhes: {e.response.text}")
        return []

# Funções de login/logout (simplificadas, podem ser importadas de um módulo comum)
# Adaptado de dashboard_folha_page.py
def login_user_checklist(username, password):
    """Autentica o usuário (simulado ou via API)."""
    # Em um cenário real, aqui você chamaria seu endpoint de login
    # Por enquanto, vamos simular com base no nome de usuário
    # E definir um client_id com base no usuário (para teste)
    if username == "cliente1@example.com" and password == "senha123":
        st.session_state.authenticated_checklist = True
        # Simulando um objeto User como o esperado pelo backend
        st.session_state.user_checklist = {"username": username, "client_id": "cliente1", "is_admin": False, "token": "fake_token_cliente1"}
        st.session_state.checklist_client_id = "cliente1" # Definir o client_id na sessão
        st.success("Login bem-sucedido!")
        return True
    elif username == "admin@example.com" and password == "admin123":
        st.session_state.authenticated_checklist = True
        st.session_state.user_checklist = {"username": username, "client_id": None, "is_admin": True, "token": "fake_token_admin"}
        # Admin pode precisar selecionar um cliente, ou isso pode ser tratado de outra forma
        # Por agora, vamos deixar em branco e ele precisará informar o id_cliente para carregar a folha
        st.session_state.checklist_client_id = ""
        st.success("Login de administrador bem-sucedido!")
        return True
    else:
        st.error("Usuário ou senha inválidos.")
        return False

def logout_user_checklist():
    """Faz logout do usuário."""
    st.session_state.authenticated_checklist = False
    st.session_state.user_checklist = None
    st.session_state.checklist_items = []
    st.session_state.id_folha_processada_checklist = ""
    st.session_state.checklist_client_id = ""
    st.session_state.dica_ia_cache = {}
    st.success("Logout realizado.")

def get_auth_headers():
    token = None
    if 'user_checklist' in st.session_state and st.session_state.user_checklist:
        token = st.session_state.user_checklist.get('token')
    elif 'api_token' in st.session_state:
        token = st.session_state.get('api_token')
    headers = {}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    return headers

# Função principal para exibir a página do checklist
def mostrar_checklist_page():
    """Renderiza a página de checklist de fechamento da folha."""
    initialize_session_state_checklist()
    st.image("assets/logo.png", width=200) # Ajuste o caminho se necessário
    st.title("Checklist de Fechamento da Folha")

    if not st.session_state.authenticated_checklist:
        st.subheader("Login")
        with st.form("login_form_checklist"):
            username = st.text_input("Usuário (email)")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                login_user_checklist(username, password)
        return # Interrompe a execução se não estiver logado

    st.sidebar.subheader(f"Usuário: {st.session_state.user_checklist['username']}")
    if st.sidebar.button("Logout"):
        logout_user_checklist()
        st.rerun() # Reinicia a página para mostrar o formulário de login

    # Seleção de Cliente e Folha
    # Se admin, permitir input do id_cliente. Se não, usar o do token.
    client_id_input = st.session_state.checklist_client_id
    if st.session_state.user_checklist and st.session_state.user_checklist.get("is_admin"):
        client_id_input = st.text_input("ID do Cliente", value=st.session_state.get("admin_selected_client_id", ""), help="Administradores devem informar o ID do cliente.")
        st.session_state.admin_selected_client_id = client_id_input # Salva para persistir
    elif not client_id_input: # Se não for admin e não tiver client_id (deveria ter pelo login)
        st.warning("ID do Cliente não encontrado. Faça login novamente.")
        return

    folhas_disponiveis = fetch_folhas_disponiveis_para_checklist(client_id_input)
    folha_options = folhas_disponiveis if isinstance(folhas_disponiveis, list) else []
    folha_id_selecionada = None
    if folha_options:
        def folha_format_func(folha):
            # Garante string e mostra info útil
            return str(folha.get("descricao", folha.get("id_folha_processada", "Folha sem nome")))
        folha_id_selecionada = st.selectbox(
            "Selecione a Folha Processada",
            options=folha_options,
            format_func=folha_format_func,
            key="selectbox_folha_checklist"
        )
        if folha_id_selecionada:
            id_folha_input = folha_id_selecionada.get("id_folha_processada")
            st.session_state.id_folha_processada_checklist = id_folha_input
    else:
        id_folha_input = st.text_input(
            "ID da Folha Processada",
            value=st.session_state.id_folha_processada_checklist,
            key="id_folha_input_checklist"
        )
        st.info("Nenhuma folha disponível para seleção automática. Informe o ID manualmente.")

    if st.button("Carregar Checklist", key="load_checklist_btn"):
        if not client_id_input:
            st.error("ID do Cliente é obrigatório.")
        elif not st.session_state.id_folha_processada_checklist:
            st.error("ID da Folha Processada é obrigatório.")
        else:
            st.session_state.checklist_client_id = client_id_input # Garante que o client_id usado está na sessão
            with st.spinner("Carregando itens do checklist..."):
                items = fetch_checklist_items(client_id_input, st.session_state.id_folha_processada_checklist)
            if items is not None:
                st.session_state.checklist_items = sorted(items, key=lambda x: (x.get("categoria", ""), x.get("descricao", "")))
                st.success(f"Checklist para a folha {st.session_state.id_folha_processada_checklist} carregado.")
            else:
                st.session_state.checklist_items = [] # Limpa em caso de erro
                # A função fetch_checklist_items já mostra o erro

    if not st.session_state.checklist_items:
        st.write("Nenhum item de checklist carregado ou encontrado.")
        return

    # Métricas de Progresso
    # Exemplo de payload de resposta do checklist para desenvolvedores:
    # [
    #   {
    #     "id_item_checklist": "item1",
    #     "descricao": "Conferir INSS",
    #     "categoria": "Tributos",
    #     "status": "PENDENTE",
    #     "criticidade": "BLOQUEADOR",
    #     "notas": "",
    #     "responsavel": "Maria"
    #   },
    #   ...
    # ]
    total_items = len(st.session_state.checklist_items)
    concluidos = sum(1 for item in st.session_state.checklist_items if item.get("status") == "CONCLUIDO")
    pendentes = total_items - concluidos
    bloqueadores_pendentes = sum(1 for item in st.session_state.checklist_items if item.get("criticidade") == "BLOQUEADOR" and item.get("status") != "CONCLUIDO")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Itens", total_items)
    with col2:
        st.metric("Concluídos", concluidos)
    with col3:
        st.metric("Pendentes", pendentes)

    if bloqueadores_pendentes > 0:
        st.warning(f"⚠️ Atenção: Existem {bloqueadores_pendentes} item(ns) bloqueador(es) pendente(s)!")

    # Abas para visualização dos itens
    tab_pendentes, tab_concluidos, tab_bloqueadores = st.tabs(["Pendentes", "Concluídos", "Bloqueadores Pendentes"])

    status_options = ["PENDENTE", "EM ANDAMENTO", "CONCLUIDO", "NAO_APLICAVEL"]
    status_map_display = {
        "PENDENTE": "🔴 Pendente",
        "EM ANDAMENTO": "🟡 Em Andamento",
        "CONCLUIDO": "🟢 Concluído",
        "NAO_APLICAVEL": "⚪ Não Aplicável"
    }
    criticidade_map_display = {
        "BAIXA": "Baixa",
        "MEDIA": "Média",
        "ALTA": "Alta",
        "BLOQUEADOR": "🚫 BLOQUEADOR"
    }

    def render_item_expander(item, item_key_prefix):
        expander_title = f"{item.get('descricao', 'Item sem descrição')} ({status_map_display.get(item.get('status'), item.get('status'))})"
        if item.get('criticidade') == "BLOQUEADOR":
            expander_title = f"🚫 {expander_title}"

        with st.expander(expander_title):
            st.markdown(f"**Categoria:** {item.get('categoria', 'N/A')}")
            st.markdown(f"**Responsável:** {item.get('responsavel', 'N/A')}")
            st.markdown(f"**Criticidade:** {criticidade_map_display.get(item.get('criticidade'), item.get('criticidade'))}")

            # Encontrar o índice do status atual para o selectbox
            current_status_index = status_options.index(item.get("status")) if item.get("status") in status_options else 0

            new_status = st.selectbox(
                "Status",
                options=status_options,
                index=current_status_index,
                format_func=lambda x: str(status_map_display.get(x, x)),
                key=f"{item_key_prefix}_status_{item.get('id_item_checklist')}"
            )
            new_notas = st.text_area(
                "Notas",
                value=item.get("notas", ""),
                key=f"{item_key_prefix}_notas_{item.get('id_item_checklist')}"
            )

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Salvar Alterações", key=f"{item_key_prefix}_save_{item.get('id_item_checklist')}"):
                    updates = {"status": new_status, "notas": new_notas}
                    with st.spinner("Salvando..."):
                        updated_item = update_checklist_item_api(
                            st.session_state.checklist_client_id,
                            st.session_state.id_folha_processada_checklist,
                            item.get("id_item_checklist"),
                            updates
                        )
                    if updated_item:
                        # Atualizar o item na lista da sessão
                        for i, chk_item in enumerate(st.session_state.checklist_items):
                            if chk_item.get("id_item_checklist") == item.get("id_item_checklist"):
                                st.session_state.checklist_items[i] = updated_item
                                break
                        st.success(f"Item '{item.get('descricao')}' atualizado!")
                        st.rerun() # Recarrega para refletir o status no título do expander e nas métricas
                    else:
                        st.error(f"Falha ao atualizar o item '{item.get('descricao')}'.")
            with col_b2:
                if st.button("💡 Obter Dica IA", key=f"{item_key_prefix}_dica_{item.get('id_item_checklist')}"):
                    item_id = item.get("id_item_checklist")
                    if item_id in st.session_state.dica_ia_cache:
                        st.info(f"Dica (cache): {st.session_state.dica_ia_cache[item_id]}")
                    else:
                        with st.spinner("Buscando dica da IA..."):
                            dica = get_dica_ia_api(
                                st.session_state.checklist_client_id,
                                st.session_state.id_folha_processada_checklist,
                                item_id,
                                item.get("descricao")
                            )
                        if dica and "dica" in dica:
                            st.session_state.dica_ia_cache[item_id] = dica["dica"]
                            st.info(f"Dica: {dica['dica']}")
                        else:
                            st.warning("Não foi possível obter a dica da IA.")
            
            if item.get('id_item_checklist') in st.session_state.dica_ia_cache:
                 st.caption(f"Dica IA: {st.session_state.dica_ia_cache[item.get('id_item_checklist')]}")


    with tab_pendentes:
        st.subheader("Itens Pendentes ou Em Andamento")
        pendentes_list = [item for item in st.session_state.checklist_items if item.get("status") in ["PENDENTE", "EM ANDAMENTO"]]
        if not pendentes_list:
            st.info("Nenhum item pendente ou em andamento.")
        else:
            for item in sorted(pendentes_list, key=lambda x: (x.get("criticidade") != "BLOQUEADOR", x.get("categoria", ""), x.get("descricao", ""))): # Bloqueadores primeiro
                render_item_expander(item, "pend")

    with tab_concluidos:
        st.subheader("Itens Concluídos ou Não Aplicáveis")
        concluidos_list = [item for item in st.session_state.checklist_items if item.get("status") in ["CONCLUIDO", "NAO_APLICAVEL"]]
        if not concluidos_list:
            st.info("Nenhum item concluído ou não aplicável.")
        else:
            for item in sorted(concluidos_list, key=lambda x: (x.get("categoria", ""), x.get("descricao", ""))):
                render_item_expander(item, "conc")
    
    with tab_bloqueadores:
        st.subheader("Itens Bloqueadores Pendentes")
        bloqueadores_pendentes_list = [
            item for item in st.session_state.checklist_items 
            if item.get("criticidade") == "BLOQUEADOR" and item.get("status") not in ["CONCLUIDO", "NAO_APLICAVEL"]
        ]
        if not bloqueadores_pendentes_list:
            st.info("Nenhum item bloqueador pendente. Ótimo!")
        else:
            for item in sorted(bloqueadores_pendentes_list, key=lambda x: (x.get("categoria", ""), x.get("descricao", ""))):
                 render_item_expander(item, "bloq")


    st.divider()
    st.subheader("Finalizar Fechamento da Folha")

    if bloqueadores_pendentes > 0:
        st.error(f"Existem {bloqueadores_pendentes} itens bloqueadores que precisam ser concluídos antes de fechar a folha.")
    
    confirm_close = st.checkbox("Confirmo que revisei todos os itens e desejo marcar esta folha como fechada.", key="confirm_close_sheet_cb")

    if st.button("Marcar Folha como Fechada", key="mark_closed_btn", disabled=(bloqueadores_pendentes > 0 or not confirm_close)):
        if not st.session_state.checklist_client_id or not st.session_state.id_folha_processada_checklist:
            st.error("ID do Cliente e ID da Folha Processada são necessários.")
        else:
            if bloqueadores_pendentes > 0:
                st.error("Não é possível fechar a folha. Existem itens bloqueadores pendentes.")
            elif not confirm_close:
                st.warning("Você precisa confirmar a revisão dos itens para fechar a folha.")
            else:
                with st.spinner("Marcando folha como fechada..."):
                    response = mark_sheet_as_closed_api(st.session_state.checklist_client_id, st.session_state.id_folha_processada_checklist)
                if response and response.get("status_folha") == "FECHADA_CLIENTE":
                    st.success(f"Folha {st.session_state.id_folha_processada_checklist} marcada como fechada com sucesso!")
                    # Atualizar o status da folha localmente ou recarregar tudo se necessário
                    # Idealmente, a API retornaria os itens atualizados ou um status geral
                    # Por simplicidade, vamos apenas mostrar a mensagem.
                    # Poderia-se desabilitar mais interações ou recarregar os dados.
                    st.balloons()
                elif response:
                    st.warning(f"A folha foi processada, mas o status é: {response.get('message', 'Status desconhecido')}. Detalhes: {response.get('detail', '')}")
                else:
                    st.error("Falha ao marcar a folha como fechada.")
    elif (bloqueadores_pendentes > 0 or not confirm_close) and st.session_state.get("mark_closed_btn_clicked", False): # Para dar feedback se o botão estava desabilitado e foi clicado
         if bloqueadores_pendentes > 0:
            st.error("Ação bloqueada: Existem itens bloqueadores pendentes.")
         elif not confirm_close:
            st.warning("Ação bloqueada: Confirme a revisão dos itens.")
    
    # Guardar o estado do clique para feedback
    if "mark_closed_btn" in st.session_state and st.session_state.mark_closed_btn:
        st.session_state.mark_closed_btn_clicked = True
    else:
        st.session_state.mark_closed_btn_clicked = False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    st.set_page_config(layout="wide", page_title="Checklist de Fechamento")
    
    initialize_session_state_checklist()
    mostrar_checklist_page()
