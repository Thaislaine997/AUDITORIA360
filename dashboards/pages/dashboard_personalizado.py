"""
Módulo da página Dashboard Personalizado - Painel customizável pelo usuário.
"""

import streamlit as st

st.set_page_config(page_title="Dashboard Personalizado - AUDITORIA360", layout="wide")

import os
import random
import sys

import requests

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

from src.frontend.api_client import APIClient
from src.frontend.auth_verify import verify_auth
from src.frontend.components.dashboard_interativo import (
    criar_html_widget_interativo,
    injetar_recursos_interativos,
)
from src.frontend.components.dashboard_widgets import WIDGETS_CATALOG, get_widget_by_id
from src.frontend.components.layout_sharing import GerenciadorLayoutsCompartilhados
from src.frontend.components.streamlit_bidirectional import (
    dashboard_bidirectional_component,
)
from src.frontend.components.widget_async_loader import (
    limpar_cache_widget,
    load_widget_async,
)

# Ajusta estilo para o grid do dashboard
GRID_CSS = """
<style>
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        grid-auto-rows: minmax(150px, auto);
        gap: 10px;
        padding: 10px;
        width: 100%;
    }
    
    .dashboard-widget {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    .dashboard-widget:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .widget-editor-toolbar {
        display: flex;
        justify-content: space-between;
        padding: 5px;
        background-color: #f0f2f6;
        border-radius: 4px;
        margin-bottom: 5px;
    }
    
    .stButton button {
        padding: 2px 8px;
        font-size: 0.8rem;
    }
</style>
"""


def main():
    """
    Função principal da página de dashboard personalizado.
    """
    st.title("Dashboard Personalizado")

    # Verificar autenticação
    auth_data = verify_auth()
    if not auth_data:
        st.error("Você precisa estar logado para acessar esta página.")
        st.stop()

    # Inicializar o modo do dashboard se não existir
    if "modo_dashboard" not in st.session_state:
        st.session_state.modo_dashboard = "visualizar"

    # Controles da barra lateral
    st.sidebar.title("Controles")

    # Opções de modo
    modo_opcoes = ["Visualizar Dashboard", "Configurar Layout"]

    # Adicionar opção Admin para usuários com permissão
    if auth_data.get("role") in ["admin", "super_admin"]:
        modo_opcoes.append("Administrar Layouts")

    modo_selecionado = st.sidebar.radio("Modo:", modo_opcoes)

    # Mapear seleção para modo interno
    if modo_selecionado == "Visualizar Dashboard":
        st.session_state.modo_dashboard = "visualizar"
    elif modo_selecionado == "Configurar Layout":
        st.session_state.modo_dashboard = "editor"
    elif modo_selecionado == "Administrar Layouts":
        st.session_state.modo_dashboard = "admin"

    # Utilizar cliente API v2
    api_client = APIClient()
    api_client.set_token(auth_data.get("token"))

    # Gerenciar o modo atual
    if st.session_state.modo_dashboard == "visualizar":
        # Carregar preferências do usuário
        preferencias = api_client.get_dashboard_layouts()

        if preferencias:
            # Permitir seleção entre layouts salvos
            if "layout_preferencia_id" not in st.session_state:
                # Procurar layout padrão
                default_layout = next(
                    (p for p in preferencias if p["is_default"]), preferencias[0]
                )
                st.session_state.layout_preferencia_id = default_layout[
                    "id_preferencia"
                ]

            # Seletor de layout
            layout_selecionado = st.sidebar.selectbox(
                "Selecione um layout:",
                options=preferencias,
                format_func=lambda p: p["nome_layout"],
                index=(
                    [p["id_preferencia"] for p in preferencias].index(
                        st.session_state.layout_preferencia_id
                    )
                    if st.session_state.layout_preferencia_id
                    in [p["id_preferencia"] for p in preferencias]
                    else 0
                ),
            )

            # Botão para visualizar layouts compartilhados
            if st.sidebar.button("Ver Layouts Compartilhados"):
                st.session_state.modo_dashboard = "compartilhados"
                st.rerun()

            # Atualizar ID do layout selecionado
            st.session_state.layout_preferencia_id = layout_selecionado[
                "id_preferencia"
            ]

            # Renderizar o layout selecionado
            renderizar_dashboard(layout_selecionado)
        else:
            # Exibir dashboard padrão se não houver layouts salvos
            st.info(
                "Você ainda não tem layouts personalizados. Crie um novo layout na seção 'Configurar Layout'."
            )
            exibir_dashboard_padrao()

    elif st.session_state.modo_dashboard == "editor":
        # Interface de edição do dashboard
        exibir_editor_dashboard(auth_data)

    elif st.session_state.modo_dashboard == "admin":
        # Interface de administração de layouts (apenas para admins)
        if auth_data.get("role") in ["admin", "super_admin"]:
            pagina_admin_layouts()
        else:
            st.error("Você não tem permissão para acessar esta página.")

    elif st.session_state.modo_dashboard == "compartilhados":
        # Interface para visualizar e usar layouts compartilhados
        exibir_layouts_compartilhados()

        # Botão para voltar ao modo visualização
        if st.sidebar.button("Voltar ao Meu Dashboard"):
            st.session_state.modo_dashboard = "visualizar"
            st.rerun()


def dashboard_personalizado():
    """
    Renderiza a página de dashboard personalizado para o AUDITORIA360.
    """
    # Verificar autenticação do usuário
    auth_data = verify_auth()
    if not auth_data:
        st.warning("Você precisa estar autenticado para acessar esta página.")
        st.stop()

    # Aplicar CSS personalizado
    st.markdown(GRID_CSS, unsafe_allow_html=True)

    # Título da página
    st.title("Dashboard Personalizado")
    st.write("Configure seu dashboard com as informações mais relevantes para você.")

    # Separador para organizar a interface
    tabs = st.tabs(["Meu Dashboard", "Configurar Layout"])

    # Tab do dashboard principal
    with tabs[0]:
        exibir_dashboard(auth_data)

    # Tab de configuração
    with tabs[1]:
        configurar_dashboard(auth_data)


def exibir_dashboard(auth_data):
    """
    Exibe o dashboard personalizado do usuário.

    Args:
        auth_data: Dados de autenticação do usuário
    """
    # Carregar as preferências salvas do usuário
    preferencias = carregar_preferencias_dashboard(auth_data)

    # Se não tiver preferências, mostrar mensagem
    if not preferencias:
        st.info(
            "Você ainda não tem um layout personalizado. Crie um na aba 'Configurar Layout'."
        )
        exibir_dashboard_padrao()
        return

    # Se tiver preferências, mostrar o seletor de layout
    if len(preferencias) > 1:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            opcao_selecionada = st.selectbox(
                "Selecione um layout:",
                options=[p["id_preferencia"] for p in preferencias],
                format_func=lambda x: next(
                    (
                        p["nome_layout"]
                        for p in preferencias
                        if p["id_preferencia"] == x
                    ),
                    x,
                ),
                key="layout_selector",
            )

        # Encontrar a preferência selecionada
        preferencia_atual = next(
            (p for p in preferencias if p["id_preferencia"] == opcao_selecionada),
            preferencias[0],
        )
    else:
        preferencia_atual = preferencias[0]
        st.info(f"Layout carregado: {preferencia_atual['nome_layout']}")

    # Renderizar o layout
    renderizar_layout(preferencia_atual)


def configurar_dashboard(auth_data):
    """
    Interface para criar e editar layouts de dashboard.

    Args:
        auth_data: Dados de autenticação do usuário
    """
    st.header("Configuração de Layout")
    st.caption(
        "Adicione, remova e configure widgets para criar seu dashboard personalizado."
    )

    # Inicializar o estado para o editor
    if "editor_config" not in st.session_state:
        st.session_state.editor_config = {
            "nome_layout": "Meu Layout Personalizado",
            "widgets": [],
            "layout_em_edicao": None,
            "widget_em_edicao": None,
        }

    # Carregar preferências existentes para edição
    preferencias = carregar_preferencias_dashboard(auth_data)

    # Opções para criar novo ou editar existente
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Criar novo layout")

        # Nome para o novo layout
        nome_layout = st.text_input(
            "Nome do layout", value=st.session_state.editor_config["nome_layout"]
        )
        st.session_state.editor_config["nome_layout"] = nome_layout

        # Botão para criar novo
        if st.button("✨ Criar Novo Layout", use_container_width=True):
            st.session_state.editor_config = {
                "nome_layout": nome_layout,
                "widgets": [],
                "layout_em_edicao": None,
                "widget_em_edicao": None,
            }
            st.success(
                f"Novo layout '{nome_layout}' iniciado. Adicione widgets abaixo."
            )

    with col2:
        st.subheader("Editar layout existente")
        if preferencias:
            # Lista de layouts existentes para editar
            layout_para_editar = st.selectbox(
                "Selecione um layout para editar",
                options=[p["id_preferencia"] for p in preferencias],
                format_func=lambda x: next(
                    (
                        p["nome_layout"]
                        for p in preferencias
                        if p["id_preferencia"] == x
                    ),
                    x,
                ),
            )

            # Botão para carregar o layout selecionado
            if st.button("✏️ Editar Layout", use_container_width=True):
                # Encontrar a preferência selecionada
                preferencia = next(
                    (
                        p
                        for p in preferencias
                        if p["id_preferencia"] == layout_para_editar
                    ),
                    None,
                )
                if preferencia:
                    # Carregar no editor
                    st.session_state.editor_config = {
                        "nome_layout": preferencia["nome_layout"],
                        "widgets": preferencia["configuracao"]["widgets"],
                        "layout_em_edicao": preferencia["id_preferencia"],
                        "widget_em_edicao": None,
                    }
                    st.success(
                        f"Layout '{preferencia['nome_layout']}' carregado para edição."
                    )
                    st.rerun()
        else:
            st.info("Você ainda não tem layouts salvos.")

    # Linha separadora
    st.divider()

    # Editor de layout
    st.subheader("Editor de Layout")
    col1, col2 = st.columns([2, 1])

    # Coluna para preview do layout
    with col1:
        st.subheader("Preview do Layout")

        # Se tiver widgets, mostrar o layout
        if st.session_state.editor_config["widgets"]:
            # Mostrar dimensões do grid
            st.caption("Grid do dashboard (6 colunas)")

            # Renderizar os widgets no editor
            renderizar_editor_layout()
        else:
            st.info("Adicione widgets para visualizar o layout.")

    # Coluna para ferramentas do editor
    with col2:
        st.subheader("Ferramentas")

        # Seção para adicionar widgets
        with st.expander("➕ Adicionar Widget", expanded=True):
            # Lista de widgets disponíveis
            widget_options = list(WIDGETS_CATALOG.keys())
            selected_widget = st.selectbox(
                "Selecione um widget",
                options=widget_options,
                format_func=lambda x: (
                    WIDGETS_CATALOG[x].nome if x in WIDGETS_CATALOG else x
                ),
            )

            # Mostrar informações do widget selecionado
            if selected_widget in WIDGETS_CATALOG:
                widget_class = WIDGETS_CATALOG[selected_widget]
                st.caption(f"{widget_class.icone} {widget_class.descricao}")

                # Campos de posição e tamanho
                col1, col2 = st.columns(2)
                with col1:
                    coluna = st.number_input(
                        "Coluna", min_value=1, max_value=6, value=1
                    )
                with col2:
                    linha = st.number_input("Linha", min_value=1, max_value=10, value=1)

                col1, col2 = st.columns(2)
                with col1:
                    largura = st.number_input(
                        "Largura",
                        min_value=1,
                        max_value=6,
                        value=widget_class.tamanho_padrao["largura"],
                    )
                with col2:
                    altura = st.number_input(
                        "Altura",
                        min_value=1,
                        max_value=4,
                        value=widget_class.tamanho_padrao["altura"],
                    )

                # Botão para adicionar
                if st.button("➕ Adicionar ao Layout", use_container_width=True):
                    novo_widget = {
                        "id": selected_widget,
                        "posicao": {"coluna": coluna, "linha": linha},
                        "tamanho": {"largura": largura, "altura": altura},
                        "configs_adicionais": widget_class.config_opcoes.copy(),
                    }
                    st.session_state.editor_config["widgets"].append(novo_widget)
                    st.success(f"Widget {widget_class.nome} adicionado!")
                    st.rerun()

        # Seção para configurar widgets existentes
        if st.session_state.editor_config["widgets"]:
            with st.expander("⚙️ Configurar Widget"):
                # Lista de widgets no layout
                widgets = st.session_state.editor_config["widgets"]
                widget_names = [
                    f"{idx+1}. {WIDGETS_CATALOG[w['id']].nome}"
                    for idx, w in enumerate(widgets)
                ]

                selected_idx = st.selectbox(
                    "Selecione um widget para configurar",
                    options=list(range(len(widgets))),
                    format_func=lambda i: (
                        widget_names[i] if i < len(widget_names) else ""
                    ),
                )

                # Mostrar configurações do widget selecionado
                if selected_idx is not None and selected_idx < len(widgets):
                    widget = widgets[selected_idx]
                    widget_class = WIDGETS_CATALOG[widget["id"]]

                    st.caption(f"Configurando: {widget_class.nome}")

                    # Tabs para separar configurações básicas e avançadas
                    config_tabs = st.tabs(
                        ["Posição e Tamanho", "Configurações Específicas"]
                    )

                    # Configurações de posição e tamanho
                    with config_tabs[0]:
                        col1, col2 = st.columns(2)
                        with col1:
                            widget["posicao"]["coluna"] = st.number_input(
                                "Coluna",
                                min_value=1,
                                max_value=6,
                                value=widget["posicao"]["coluna"],
                            )
                        with col2:
                            widget["posicao"]["linha"] = st.number_input(
                                "Linha",
                                min_value=1,
                                max_value=10,
                                value=widget["posicao"]["linha"],
                            )

                        col1, col2 = st.columns(2)
                        with col1:
                            widget["tamanho"]["largura"] = st.number_input(
                                "Largura",
                                min_value=1,
                                max_value=6,
                                value=widget["tamanho"]["largura"],
                            )
                        with col2:
                            widget["tamanho"]["altura"] = st.number_input(
                                "Altura",
                                min_value=1,
                                max_value=4,
                                value=widget["tamanho"]["altura"],
                            )

                    # Configurações específicas do widget
                    with config_tabs[1]:
                        st.caption("Configurações específicas deste widget")
                        # Usar o método de configuração específico de cada widget
                        widget["configs_adicionais"] = widget_class.renderizar_config()

                    # Botões de ação para o widget
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🗑️ Remover Widget", use_container_width=True):
                            st.session_state.editor_config["widgets"].pop(selected_idx)
                            st.success(f"Widget removido do layout!")
                            st.rerun()
                    with col2:
                        if st.button("✅ Aplicar Mudanças", use_container_width=True):
                            st.success("Configurações aplicadas!")
                            st.rerun()

        # Seção para salvar o layout
        with st.expander("💾 Salvar Layout", expanded=True):
            # Campo para definir o nome final
            nome_final = st.text_input(
                "Nome para salvar o layout",
                value=st.session_state.editor_config["nome_layout"],
            )

            # Opção para tornar padrão
            layout_padrao = st.checkbox("Definir como layout padrão", value=False)

            # Contexto do cliente (opcional)
            id_cliente = st.text_input("ID do cliente (opcional)", value="")

            # Botão para salvar
            if st.button("💾 Salvar Layout", use_container_width=True, type="primary"):
                if not st.session_state.editor_config["widgets"]:
                    st.error("Adicione pelo menos um widget antes de salvar o layout.")
                else:
                    try:
                        # Preparar dados para salvar
                        layout_data = {
                            "nome_layout": nome_final,
                            "is_default": layout_padrao,
                            "id_cliente": id_cliente if id_cliente else None,
                            "configuracao": {
                                "widgets": st.session_state.editor_config["widgets"],
                                "opcoes_visuais": {
                                    "tema": "claro",
                                    "densidade": "normal",
                                },
                            },
                        }

                        # Se estiver editando um layout existente
                        layout_id = st.session_state.editor_config["layout_em_edicao"]
                        if layout_id:
                            # Atualizar layout existente
                            salvar_layout_existente(auth_data, layout_id, layout_data)
                        else:
                            # Criar novo layout
                            criar_novo_layout(auth_data, layout_data)

                    except Exception as e:
                        st.error(f"Erro ao salvar o layout: {str(e)}")


def exibir_editor_dashboard(dados=None):
    import streamlit as st

    st.subheader("Editor de Dashboard")
    st.write("Edite seu dashboard aqui.")
    if dados:
        st.json(dados)


def renderizar_editor_layout():
    """
    Renderiza o layout atual no editor com controles interativos.
    """
    # Injetar CSS e JavaScript para as funcionalidades interativas
    injetar_recursos_interativos()

    # Iniciar o grid do dashboard com HTML
    html = """<div class="dashboard-grid">"""

    # Para cada widget no layout
    for idx, widget in enumerate(st.session_state.editor_config["widgets"]):
        # Obter classe do widget
        widget_class = get_widget_by_id(widget["id"])
        if not widget_class:
            continue

        # Criar widget HTML interativo
        widget_html = criar_html_widget_interativo(
            id_widget=f"widget_{idx}",
            nome_widget=widget_class.nome,
            icone=widget_class.icone,
            posicao=widget["posicao"],
            tamanho=widget["tamanho"],
        )

        html += widget_html

    # Fechar o grid
    html += """</div>"""

    # Renderizar o HTML
    st.markdown(html, unsafe_allow_html=True)

    # Renderizar o conteúdo de cada widget em containers separados
    for idx, widget in enumerate(st.session_state.editor_config["widgets"]):
        # Criar um container para o widget
        with st.container():
            st.markdown(
                f"""<div id="widget_content_widget_{idx}" style="display:none;">""",
                unsafe_allow_html=True,
            )

            # Obter classe do widget
            widget_class = get_widget_by_id(widget["id"])
            if widget_class:
                # Renderizar o widget
                widget_class.renderizar(widget["configs_adicionais"])

            st.markdown("""</div>""", unsafe_allow_html=True)

    # Listener para eventos do JavaScript
    if "last_widget_event" not in st.session_state:
        st.session_state.last_widget_event = None

    # Receber dados de eventos do JavaScript (em uma implementação completa)
    # Aqui precisaria usar um componente customizado do Streamlit ou
    # alguma solução de websocket para comunicação bidirecional


def renderizar_layout(preferencia):
    """
    Renderiza o layout escolhido pelo usuário.

    Args:
        preferencia: Dados da preferência de dashboard
    """
    try:
        # Verificar se temos widgets para renderizar
        if not preferencia.get("configuracao") or not preferencia["configuracao"].get(
            "widgets"
        ):
            st.warning("Este layout não possui widgets configurados.")
            return

        # Injetar CSS para estilizar o grid (sem o JavaScript de edição)
        st.markdown(
            """
        <style>
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(6, 1fr);
                grid-auto-rows: minmax(150px, auto);
                gap: 10px;
                padding: 10px;
                width: 100%;
            }
            
            .dashboard-widget {
                background-color: white;
                border-radius: 8px;
                padding: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .widget-header {
                font-size: 0.8rem;
                color: #6c757d;
                margin-bottom: 8px;
                padding-bottom: 4px;
                border-bottom: 1px solid #f0f2f6;
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

        # Iniciar o grid do dashboard com HTML
        html = """<div class="dashboard-grid">"""

        # Para cada widget no layout
        for idx, widget_config in enumerate(preferencia["configuracao"]["widgets"]):
            # Obter classe do widget
            widget_class = get_widget_by_id(widget_config["id"])
            if not widget_class:
                continue

            # Calcular posicionamento no grid
            coluna = widget_config["posicao"]["coluna"]
            linha = widget_config["posicao"]["linha"]
            largura = widget_config["tamanho"]["largura"]
            altura = widget_config["tamanho"]["altura"]

            # Estilo CSS para posicionamento
            style = f"""
                grid-column: {coluna} / span {largura};
                grid-row: {linha} / span {altura};
            """

            # Adicionar div para o widget com estilo
            html += f"""
                <div class="dashboard-widget" style="{style}" id="widget_{idx}">
                    <div class="widget-header">{widget_class.icone} {widget_class.nome}</div>
                    <div id="widget_content_{idx}"></div>
                </div>
            """

        # Fechar o grid
        html += """</div>"""

        # Renderizar o HTML
        st.markdown(html, unsafe_allow_html=True)

        # Renderizar o conteúdo de cada widget em containers separados
        for idx, widget_config in enumerate(preferencia["configuracao"]["widgets"]):
            # Criar um container para o widget
            with st.container():
                st.markdown(
                    f"""<div id="widget_content_{idx}" style="display:none;">""",
                    unsafe_allow_html=True,
                )

                # Obter classe do widget
                widget_class = get_widget_by_id(widget_config["id"])
                if widget_class:
                    # Renderizar o widget
                    widget_class.renderizar(widget_config.get("configs_adicionais"))

                st.markdown("""</div>""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro ao renderizar o layout: {str(e)}")
        st.exception(e)


def exibir_dashboard_padrao():
    """
    Exibe um dashboard padrão quando o usuário não tem layouts personalizados.
    """
    # Cria um layout padrão simples
    st.subheader("Dashboard Padrão")
    st.caption(
        "Aqui está um layout inicial. Você pode personalizar seu próprio layout na aba 'Configurar Layout'."
    )

    # Criar um layout básico com 4 widgets
    col1, col2 = st.columns(2)

    with col1:
        # KPI Total da Folha
        st.markdown("### Total da Folha")
        valor = "{:,.2f}".format(random.uniform(50000, 200000))
        st.markdown(
            f"<div style='font-size: 2.5rem; color: #1f77b4; text-align: center; font-weight: bold;'>R$ {valor}</div>",
            unsafe_allow_html=True,
        )

    with col2:
        # KPI Média Salarial
        st.markdown("### Média Salarial")
        valor = "{:,.2f}".format(random.uniform(2000, 6000))
        st.markdown(
            f"<div style='font-size: 2.5rem; color: #2ca02c; text-align: center; font-weight: bold;'>R$ {valor}</div>",
            unsafe_allow_html=True,
        )

    # Gráficos
    st.markdown("### Evolução da Folha")

    # Gerar dados mock para o gráfico
    import random
    from datetime import datetime, timedelta

    import pandas as pd
    import plotly.express as px

    # Gerar datas para os últimos 30 dias
    hoje = datetime.now()
    datas = [(hoje - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30, 0, -1)]

    # Gerar valores com tendência
    valores = []
    valor_base = 100000
    for i in range(30):
        # Adicionar tendência e variação aleatória
        valor_base = max(0, valor_base * 1.01 + random.uniform(-2000, 2000))
        valores.append(valor_base)

    df = pd.DataFrame({"data": datas, "valor": valores})

    # Criar gráfico
    fig = px.line(df, x="data", y="valor", title="Evolução da Folha de Pagamento")
    st.plotly_chart(fig, use_container_width=True)

    # Alertas recentes
    st.markdown("### Alertas Recentes")

    # Gerar alguns alertas mock
    alertas = [
        {"tipo": "Crítico", "descricao": "FGTS não recolhido", "data": "Hoje"},
        {"tipo": "Médio", "descricao": "Férias vencidas", "data": "Ontem"},
        {"tipo": "Crítico", "descricao": "INSS divergente", "data": "2 dias atrás"},
    ]

    # Exibir alertas
    for alerta in alertas:
        cor = {"Crítico": "🔴", "Médio": "🟠", "Baixo": "🟡"}.get(alerta["tipo"], "⚪")
        st.markdown(
            f"{cor} **{alerta['descricao']}** - {alerta['tipo']} - {alerta['data']}"
        )


def carregar_preferencias_dashboard(auth_data):
    """
    Carrega as preferências de dashboard do usuário a partir da API.

    Args:
        auth_data: Dados de autenticação do usuário

    Returns:
        Lista de preferências de dashboard ou lista vazia se ocorrer erro
    """
    try:
        token = auth_data.get("token")
        if not token:
            return []

        # URL da API
        # OBS: Em produção, recuperar do config.py
        base_url = "http://localhost:8000"  # Ajustar conforme necessário

        # Fazer a requisição para a API
        response = requests.get(
            f"{base_url}/dashboard-preferences/",
            headers={"Authorization": f"Bearer {token}"},
        )

        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            return response.json()
        else:
            # Em caso de erro, registrar para debug
            print(f"Erro ao carregar preferências: {response.status_code}")
            print(response.text)
            return []

    except Exception as e:
        # Em caso de exceção, apenas retornar lista vazia
        # Em produção, registrar o erro em um log
        print(f"Erro ao carregar preferências: {str(e)}")
        return []


def criar_novo_layout(auth_data, layout_data):
    """
    Cria um novo layout de dashboard.

    Args:
        auth_data: Dados de autenticação do usuário
        layout_data: Dados do layout a ser criado

    Returns:
        True se criado com sucesso, False caso contrário
    """
    try:
        token = auth_data.get("token")
        if not token:
            st.error("Erro de autenticação. Faça login novamente.")
            return False

        # URL da API
        # OBS: Em produção, recuperar do config.py
        base_url = "http://localhost:8000"  # Ajustar conforme necessário

        # Fazer a requisição para a API
        response = requests.post(
            f"{base_url}/dashboard-preferences/",
            headers={"Authorization": f"Bearer {token}"},
            json=layout_data,
        )

        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 201:
            response.json()
            st.success(f"Layout '{layout_data['nome_layout']}' criado com sucesso!")

            # Limpar o editor e recarregar a página
            st.session_state.editor_config = {
                "nome_layout": "Meu Layout Personalizado",
                "widgets": [],
                "layout_em_edicao": None,
                "widget_em_edicao": None,
            }
            st.rerun()
            return True
        else:
            # Em caso de erro, mostrar mensagem
            st.error(f"Erro ao criar layout: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        # Em caso de exceção, mostrar mensagem
        st.error(f"Erro ao criar layout: {str(e)}")
        return False


def salvar_layout_existente(auth_data, layout_id, layout_data):
    """
    Atualiza um layout existente.

    Args:
        auth_data: Dados de autenticação do usuário
        layout_id: ID do layout a ser atualizado
        layout_data: Novos dados do layout

    Returns:
        True se atualizado com sucesso, False caso contrário
    """
    try:
        token = auth_data.get("token")
        if not token:
            st.error("Erro de autenticação. Faça login novamente.")
            return False

        # URL da API
        # OBS: Em produção, recuperar do config.py
        base_url = "http://localhost:8000"  # Ajustar conforme necessário

        # Preparar dados para atualização
        update_data = {
            "nome_layout": layout_data["nome_layout"],
            "is_default": layout_data["is_default"],
            "configuracao": layout_data["configuracao"],
        }

        # Fazer a requisição para a API
        response = requests.put(
            f"{base_url}/dashboard-preferences/{layout_id}",
            headers={"Authorization": f"Bearer {token}"},
            json=update_data,
        )

        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            st.success(f"Layout '{layout_data['nome_layout']}' atualizado com sucesso!")

            # Limpar o editor e recarregar a página
            st.session_state.editor_config = {
                "nome_layout": "Meu Layout Personalizado",
                "widgets": [],
                "layout_em_edicao": None,
                "widget_em_edicao": None,
            }
            st.rerun()
            return True
        else:
            # Em caso de erro, mostrar mensagem
            st.error(
                f"Erro ao atualizar layout: {response.status_code} - {response.text}"
            )
            return False

    except Exception as e:
        # Em caso de exceção, mostrar mensagem
        st.error(f"Erro ao atualizar layout: {str(e)}")
        return False


def renderizar_dashboard(preferencia):
    """
    Renderiza um dashboard a partir de uma configuração de preferência.

    Args:
        preferencia: Dicionário com a configuração do layout
    """
    try:
        # Injetar CSS e JS para dashboard interativo
        injetar_recursos_interativos()

        # Configurar comunicação bidirecional para eventos de widgets
        eventos = dashboard_bidirectional_component(key="dashboard_events", debug=False)

        # Processar eventos recebidos do JavaScript
        if eventos and "action" in eventos:
            if (
                eventos["action"] == "widget_moved"
                or eventos["action"] == "widget_resized"
            ):
                # Atualizar posição/tamanho do widget
                for widget in preferencia["configuracao"]["widgets"]:
                    if widget["id"] == eventos["widgetId"]:
                        widget["posicao"]["coluna"] = eventos["position"]["col"]
                        widget["posicao"]["linha"] = eventos["position"]["row"]
                        widget["tamanho"]["largura"] = eventos["position"]["width"]
                        widget["tamanho"]["altura"] = eventos["position"]["height"]

                        # Aqui salvaria a alteração no backend
                        st.success(
                            f"Layout atualizado: {widget['id']} movido/redimensionado"
                        )
                        # TODO: Implementar salvamento automático

            elif eventos["action"] == "refresh_widget":
                # Limpar cache e forçar atualização do widget
                limpar_cache_widget(eventos["widgetId"])
                st.rerun()

            elif eventos["action"] == "config_widget":
                # Direcionar para a tela de configuração do widget
                st.session_state.editor_widget_selecionado = eventos["widgetId"]
                st.session_state.modo_dashboard = "editor"
                st.rerun()

        # Iniciar grid do dashboard
        st.markdown(
            '<div class="dashboard-grid" id="dashboard-grid">', unsafe_allow_html=True
        )

        # Renderizar cada widget
        for idx, widget_config in enumerate(preferencia["configuracao"]["widgets"]):
            widget_id = widget_config["id"]
            widget_class = get_widget_by_id(widget_id)

            if not widget_class:
                st.error(f"Widget não encontrado: {widget_id}")
                continue

            # Verificar se o widget deve ser carregado assincronamente
            carregamento_assincrono = widget_config.get(
                "carregamento_assincrono", False
            )

            # Criar o HTML do widget no grid
            widget_html = criar_html_widget_interativo(
                id_widget=f"widget_{widget_id}_{idx}",
                nome_widget=widget_class.nome,
                icone=widget_class.icone,
                posicao=widget_config["posicao"],
                tamanho=widget_config["tamanho"],
                carregamento_assincrono=carregamento_assincrono,
            )

            st.markdown(widget_html, unsafe_allow_html=True)

            # Container para o conteúdo do widget
            widget_container = st.container()

            # Decidir se carrega assincronamente ou imediatamente
            with widget_container:
                if carregamento_assincrono:
                    # Callback quando os dados forem carregados
                    def on_widget_loaded(widget_id, config, data):
                        # Enviar evento para esconder o carregamento
                        st.session_state[f"widget_data_{widget_id}_{idx}"] = data

                        # Forçar re-renderização se necessário
                        if st.session_state.get(
                            f"widget_loading_{widget_id}_{idx}", True
                        ):
                            st.session_state[f"widget_loading_{widget_id}_{idx}"] = (
                                False
                            )

                    # Verificar se já temos dados em cache para este widget
                    if (
                        f"widget_data_{widget_id}_{idx}" in st.session_state
                        and not st.session_state.get(
                            f"widget_loading_{widget_id}_{idx}", True
                        )
                    ):
                        # Usar dados em cache
                        dados = st.session_state[f"widget_data_{widget_id}_{idx}"]
                        widget_class.renderizar(
                            widget_config.get("configs_adicionais"), dados=dados
                        )
                    else:
                        # Marcar como carregando
                        st.session_state[f"widget_loading_{widget_id}_{idx}"] = True

                        # Carregar assincronamente
                        prioridade = widget_config.get("prioridade_carga", 1)
                        load_widget_async(
                            widget_id=widget_id,
                            config=widget_config.get("configs_adicionais", {}),
                            load_func=lambda cfg: (
                                widget_class.carregar_dados(cfg)
                                if hasattr(widget_class, "carregar_dados")
                                else {}
                            ),
                            callback=on_widget_loaded,
                            priority=prioridade,
                            expiry_minutes=preferencia["configuracao"].get(
                                "tempo_cache_minutos", 15
                            ),
                        )
                else:
                    # Carregar imediatamente
                    widget_class.renderizar(widget_config.get("configs_adicionais"))

        # Fechar o grid
        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erro ao renderizar o layout: {str(e)}")
        st.exception(e)


def pagina_admin_layouts():
    """
    Página de administração para gerenciamento de layouts compartilhados.
    """
    st.title("Administração de Layouts de Dashboard")

    # Criar instância do gerenciador de layouts compartilhados
    api_client = APIClient()
    gerenciador = GerenciadorLayoutsCompartilhados(api_client)

    # Renderizar a interface de administração
    gerenciador.renderizar_interface_admin()


def exibir_layouts_compartilhados():
    """
    Exibe os layouts compartilhados disponíveis para o usuário.
    """
    st.subheader("Layouts Compartilhados")

    # Criar instância do gerenciador de layouts compartilhados
    api_client = APIClient()
    gerenciador = GerenciadorLayoutsCompartilhados(api_client)

    layouts_compartilhados = gerenciador.obter_layouts_compartilhados()

    if not layouts_compartilhados:
        st.info("Não há layouts compartilhados disponíveis para você.")
        return

    # Exibir os layouts compartilhados disponíveis
    layout_selecionado = st.selectbox(
        "Selecione um layout compartilhado:",
        options=layouts_compartilhados,
        format_func=lambda l: f"{l['nome_layout']} ({l.get('tipo_compartilhamento', 'compartilhado')})",
    )

    if layout_selecionado:
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Visualizar Layout"):
                # Armazenar na sessão e redirecionar para visualização
                st.session_state.layout_compartilhado_selecionado = layout_selecionado
                st.session_state.modo_dashboard = "visualizar"
                st.rerun()

        with col2:
            if st.button("Copiar para Meus Layouts"):
                novo_nome = st.text_input(
                    "Nome para o novo layout:",
                    f"Cópia de {layout_selecionado['nome_layout']}",
                )

                if st.button("Confirmar Cópia", type="primary"):
                    id_nova_preferencia = gerenciador.copiar_layout_compartilhado(
                        layout_selecionado["id_preferencia"], novo_nome=novo_nome
                    )

                    if id_nova_preferencia:
                        st.success("Layout copiado com sucesso!")
                        st.session_state.layout_preferencia_id = id_nova_preferencia
                        st.session_state.modo_dashboard = "visualizar"
                        st.rerun()
