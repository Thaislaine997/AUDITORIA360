import streamlit as st
import sys # Add sys
import os # Add os

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) # Adjusted for pages subdir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

# src/checklist_page.py
import streamlit as st
import requests
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging
import os

# 1. Importar settings para API_BASE_URL e remover constante local
from src.core.config import settings

# Configuração básica de logging
logger = logging.getLogger(__name__)

# Funções de utilidade da sessão (podem ser movidas para um utils_streamlit.py comum)
def initialize_session_state_checklist():
    """Inicializa o estado da sessão para a página de checklist."""
    # Remover estados de autenticação locais
    # if "authenticated_checklist" not in st.session_state:
    #     st.session_state.authenticated_checklist = False
    # if "user_checklist" not in st.session_state:
    #     st.session_state.user_checklist = None 
    if "checklist_items" not in st.session_state:
        st.session_state.checklist_items = []
    if "id_folha_processada_checklist" not in st.session_state:
        st.session_state.id_folha_processada_checklist = ""
    # Remover checklist_client_id local, usaremos o da sessão principal
    # if "checklist_client_id" not in st.session_state: 
    #     st.session_state.checklist_client_id = ""
    if "dica_ia_cache" not in st.session_state:
        st.session_state.dica_ia_cache = {} 

# 2. Funções para obter token e client_id da sessão principal (st.session_state)
def get_api_token() -> Optional[str]:
    return st.session_state.get("token") # Usar "token" conforme definido em painel.py

def get_current_client_id() -> Optional[str]:
    return st.session_state.get("id_cliente") # Usar "id_cliente" conforme definido em painel.py

def get_current_folha_id_for_checklist() -> Optional[str]:
    return st.session_state.get("current_folha_id_for_checklist")

def set_current_folha_id_for_checklist(folha_id: Optional[str]):
    st.session_state.current_folha_id_for_checklist = folha_id

# 3. Ajustar get_auth_headers para usar get_api_token()
def get_auth_headers():
    token = get_api_token() # Usar a função centralizada
    headers = {}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    return headers

# Funções de interação com a API do Checklist
def fetch_checklist_items(id_cliente: str, id_folha_processada: str):
    """Busca os itens do checklist da API."""
    try:
        response = requests.get(
            f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist", # Usar settings.API_BASE_URL
            headers=get_auth_headers() 
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar checklist: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                detail = e.response.json().get("detail", e.response.text)
            except requests.exceptions.JSONDecodeError:
                detail = e.response.text
            st.error(f"Detalhes: {detail}")
            if e.response.status_code == 401:
                st.warning("Sessão expirada ou token inválido. Por favor, retorne ao login.")
                #logout_user_checklist() # Não existe mais, o painel gerencia
                st.session_state.clear()
                st.rerun()
        return None

def update_checklist_item_api(id_cliente: str, id_folha_processada: str, id_item_checklist: str, updates: dict):
    """Atualiza um item do checklist via API."""
    try:
        response = requests.put(
            f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist/{id_item_checklist}", # Usar settings.API_BASE_URL
            json=updates,
            headers=get_auth_headers() 
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao atualizar item do checklist: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                detail = e.response.json().get("detail", e.response.text)
            except requests.exceptions.JSONDecodeError:
                detail = e.response.text
            st.error(f"Detalhes: {detail}")
            if e.response.status_code == 401:
                st.warning("Sessão expirada ou token inválido. Por favor, retorne ao login.")
                st.session_state.clear()
                st.rerun()
        return None

def mark_sheet_as_closed_api(id_cliente: str, id_folha_processada: str):
    """Marca a folha como fechada via API."""
    try:
        response = requests.post(
            f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/marcar-fechada", # Usar settings.API_BASE_URL
            headers=get_auth_headers() 
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao marcar folha como fechada: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                detail = e.response.json().get("detail", e.response.text)
            except requests.exceptions.JSONDecodeError:
                detail = e.response.text
            st.error(f"Detalhes: {detail}")
            if e.response.status_code == 401:
                st.warning("Sessão expirada ou token inválido. Por favor, retorne ao login.")
                st.session_state.clear()
                st.rerun()
        return None

def get_dica_ia_api(id_cliente: str, id_folha_processada: str, id_item_checklist: str, descricao_item: str):
    """Busca dica de IA para um item do checklist."""
    try:
        response = requests.get(
            f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist/dica-ia", # Usar settings.API_BASE_URL
            params={"id_item_checklist": id_item_checklist, "descricao_item": descricao_item},
            headers=get_auth_headers() 
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dica de IA: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                detail = e.response.json().get("detail", e.response.text)
            except requests.exceptions.JSONDecodeError:
                detail = e.response.text
            st.error(f"Detalhes: {detail}")
            if e.response.status_code == 401:
                st.warning("Sessão expirada ou token inválido. Por favor, retorne ao login.")
                st.session_state.clear()
                st.rerun()
        return None

def fetch_folhas_disponiveis_para_checklist(id_cliente: str):
    """Busca as folhas processadas disponíveis para checklist para o cliente."""
    try:
        response = requests.get(
            f"{settings.API_BASE_URL}/clientes/{id_cliente}/folhas-processadas/disponiveis-para-checklist", # Usar settings.API_BASE_URL
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar folhas disponíveis: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                detail = e.response.json().get("detail", e.response.text)
            except requests.exceptions.JSONDecodeError:
                detail = e.response.text
            st.error(f"Detalhes: {detail}")
            if e.response.status_code == 401:
                st.warning("Sessão expirada ou token inválido. Por favor, retorne ao login.")
                st.session_state.clear()
                st.rerun()
        return []

# Função principal para exibir a página do checklist
def mostrar_checklist_page():
    """Renderiza a página de checklist de fechamento da folha."""
    initialize_session_state_checklist() # Mantido para estados específicos da página
    
    # Usar logo da pasta assets na raiz do projeto
    # O Streamlit geralmente serve a pasta 'assets' se estiver na raiz do diretório da aplicação.
    # Se o script está em src/frontend/pages, e assets está na raiz do projeto (AUDITORIA360/assets),
    # o caminho relativo direto 'assets/logo.png' pode não funcionar como esperado sem configuração adicional
    # do servidor de media do Streamlit ou se o ponto de execução do Streamlit não for a raiz do projeto.
    # No entanto, é comum o Streamlit conseguir encontrar 'assets/logo.png' se a pasta 'assets' 
    # estiver no mesmo nível do script principal que inicia o app (ex: painel.py, se estiver na raiz de src/frontend ou src)
    # ou se o app for executado da raiz do projeto.
    # Para maior robustez em diferentes cenários de execução, um caminho absoluto ou relativo à raiz do projeto é melhor.
    # Mas para o comportamento padrão do Streamlit, vamos tentar o caminho relativo simples primeiro.
    logo_path = "assets/logo.png" # Simplificado - Streamlit tentará encontrar a partir do diretório de execução
    try:
        # Tentativa de carregar a imagem. Se falhar, o logger avisará.
        # Não é estritamente necessário verificar os.path.exists aqui se o Streamlit lida com isso.
        st.image(logo_path, width=200)
    except Exception as e:
        logger.warning(f"Falha ao carregar logo de '{logo_path}': {e}. Tentando caminho alternativo.")
        # Fallback para um caminho que assume que 'assets' está na raiz do projeto
        # e o script está alguns níveis abaixo.
        project_root_assets_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'assets', 'logo.png')
        if os.path.exists(project_root_assets_logo):
            st.image(project_root_assets_logo, width=200)
        else:
            logger.error(f"Logo também não encontrado em: {project_root_assets_logo}")
            st.warning("Logo da aplicação não encontrado.")

    st.title("📝 Checklist de Fechamento da Folha")

    # 5. Verificar autenticação centralizada
    api_token = get_api_token()
    id_cliente_atual = get_current_client_id()

    if not api_token or not id_cliente_atual:
        st.warning("Você precisa estar logado e ter um cliente associado para acessar esta página.")
        st.info("Por favor, retorne à página inicial para fazer login.")
        if st.button("Retornar ao Login"):
            try:
                # Assumindo que painel.py é o entrypoint principal do app Streamlit
                st.switch_page("painel.py")
            except Exception as e:
                st.page_link("painel.py", label="Retornar ao Login", icon="🏠")
                logger.warning(f"Falha ao usar st.switch_page para painel.py: {e}")
        return

    # Exibir informações do usuário logado (obtidas do painel.py via st.session_state)
    if st.session_state.get("name"): # 'name' é o nome de exibição do streamlit-authenticator
         st.sidebar.success(f"Logado como: {st.session_state.get('name')}")
    if id_cliente_atual:
         st.sidebar.caption(f"Cliente ID: {id_cliente_atual}")
    # O botão de logout é gerenciado pelo painel.py e streamlit-authenticator,
    # não precisa ser recriado aqui se o painel já o adiciona globalmente.
    # Se precisar de um logout específico nesta página que limpe estados locais:
    # if st.sidebar.button("Logout Desta Sessão de Checklist"):
    #     # Limpar estados específicos do checklist se necessário
    #     st.session_state.checklist_items = []
    #     st.session_state.id_folha_processada_checklist = ""
    #     # ... outros estados locais ...
    #     # Idealmente, o logout global do painel.py cuidaria de limpar st.session_state("token"), etc.
    #     st.success("Sessão do checklist encerrada. Para logout completo, use o menu principal.")
    #     st.rerun()


    # Seleção de Cliente e Folha
    # Usar o id_cliente_atual da sessão. A lógica de admin para selecionar cliente foi removida para simplificar.
    # Se essa funcionalidade for crucial, precisará ser reimplementada baseada em roles/claims do token JWT.
    client_id_input = id_cliente_atual 
    st.info(f"Exibindo checklist para o Cliente ID: {client_id_input}")


    folhas_disponiveis = fetch_folhas_disponiveis_para_checklist(client_id_input)
    folha_options = folhas_disponiveis if isinstance(folhas_disponiveis, list) else []
    folha_id_selecionada_obj = None # Alterado para armazenar o objeto completo
    if folha_options:
        def folha_format_func(folha_obj): # Alterado para receber o objeto
            return str(folha_obj.get("descricao", folha_obj.get("id_folha_processada", "Folha sem nome")))
        
        folha_id_selecionada_obj = st.selectbox( # Alterado para armazenar o objeto
            "Selecione a Folha Processada",
            options=folha_options,
            format_func=folha_format_func,
            key="selectbox_folha_checklist"
        )
        if folha_id_selecionada_obj: # Verificar se um objeto foi selecionado
            id_folha_input = folha_id_selecionada_obj.get("id_folha_processada")
            st.session_state.id_folha_processada_checklist = id_folha_input
        else: # Caso nenhuma folha seja selecionada (ex: lista vazia ou usuário desmarcou)
            st.session_state.id_folha_processada_checklist = "" # Limpa o ID da folha
            # st.info("Nenhuma folha selecionada.") # Opcional: feedback ao usuário
    else:
        # Mantém a entrada manual se não houver opções, mas isso pode ser menos comum agora
        id_folha_input_manual = st.text_input(
            "ID da Folha Processada (manual)",
            value=st.session_state.get("id_folha_processada_checklist", ""), # Usar .get para segurança
            key="id_folha_input_checklist_manual"
        )
        st.session_state.id_folha_processada_checklist = id_folha_input_manual
        if not folha_options and not id_folha_input_manual: # Adicionado para clareza
            st.info("Nenhuma folha disponível para seleção automática. Informe o ID manualmente se necessário.")
        elif not folha_options and id_folha_input_manual:
            st.info("ID da folha informado manualmente.")


    if st.button("Carregar Checklist", key="load_checklist_btn"):
        if not client_id_input: # client_id_input agora é id_cliente_atual que já foi validado
            st.error("ID do Cliente é obrigatório. Problema de sessão.") # Mensagem improvável agora
        elif not st.session_state.id_folha_processada_checklist:
            st.error("ID da Folha Processada é obrigatório. Selecione ou informe uma folha.")
        else:
            # st.session_state.checklist_client_id = client_id_input # Não é mais necessário, usamos id_cliente_atual
            with st.spinner("Carregando itens do checklist..."):
                items = fetch_checklist_items(client_id_input, st.session_state.id_folha_processada_checklist)
            if items is not None:
                # Ordenar por categoria e depois por descrição
                st.session_state.checklist_items = sorted(
                    items, 
                    key=lambda x: (str(x.get("categoria", "")).lower(), str(x.get("descricao", "")).lower())
                )
                st.success(f"Checklist para a folha {st.session_state.id_folha_processada_checklist} carregado.")
            else:
                st.session_state.checklist_items = [] # Limpa em caso de erro
                # A função fetch_checklist_items já mostra o erro

    if not st.session_state.checklist_items:
        # Ajustar mensagem para quando o botão "Carregar Checklist" ainda não foi pressionado
        if 'load_checklist_btn' not in st.session_state or not st.session_state.load_checklist_btn:
            st.info("Selecione uma folha e clique em 'Carregar Checklist' para visualizar os itens.")
        else: # Se o botão foi pressionado e ainda não há itens
            st.write("Nenhum item de checklist carregado ou encontrado para a folha selecionada.")
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

        # Remover a chave do expander, pois não é um parâmetro válido.
        # A unicidade dos controles internos será garantida pelas chaves dos widgets (selectbox, text_area, button)
        with st.expander(expander_title):
            st.markdown(f"**ID:** `{item.get('id_item_checklist', 'N/A')}`") # Mostrar ID do item
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
                            id_cliente_atual, # Usar id_cliente_atual
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
                            dica_response = get_dica_ia_api( # Renomeado para dica_response
                                id_cliente_atual, # Usar id_cliente_atual
                                st.session_state.id_folha_processada_checklist,
                                item_id,
                                item.get("descricao")
                            )
                        if dica_response and "dica" in dica_response: # Checar dica_response
                            st.session_state.dica_ia_cache[item_id] = dica_response["dica"]
                            st.info(f"Dica: {dica_response['dica']}") # Usar dica_response
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
        if not id_cliente_atual or not st.session_state.id_folha_processada_checklist: # Usar id_cliente_atual
            st.error("ID do Cliente e ID da Folha Processada são necessários.")
        else:
            if bloqueadores_pendentes > 0:
                st.error("Não é possível fechar a folha. Existem itens bloqueadores pendentes.")
            elif not confirm_close:
                st.warning("Você precisa confirmar a revisão dos itens para fechar a folha.")
            else:
                with st.spinner("Marcando folha como fechada..."):
                    response = mark_sheet_as_closed_api(id_cliente_atual, st.session_state.id_folha_processada_checklist) # Usar id_cliente_atual
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
    # Adicionar import de os para __main__ se for executar standalone e o logo path precisar dele
    import os 
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Configuração da página Streamlit
    st.set_page_config(
        layout="wide", 
        page_title="Checklist de Fechamento",
        page_icon="📝" # Adicionado ícone
    )
    
    # Simulação de st.session_state para execução standalone (REMOVER EM PRODUÇÃO OU QUANDO INTEGRADO)
    # Isso é apenas para permitir que a página seja executada diretamente para desenvolvimento.
    # Em um ambiente integrado, painel.py populacional esses valores.
    if 'token' not in st.session_state:
        st.session_state.token = "fake_dev_token" # Simule um token
    if 'id_cliente' not in st.session_state:
       st.session_state.id_cliente = "cliente_dev_001" # Simule um client_id
    if 'name' not in st.session_state:
       st.session_state.name = "Usuário Dev"

    initialize_session_state_checklist() # Ainda necessário para estados locais da página
    mostrar_checklist_page()
