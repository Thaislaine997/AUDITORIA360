"""
Página de Benchmarking Anonimizado e Agregado.

Este módulo implementa a interface de usuário para:
1. Visualizar e comparar KPIs anonimizados e agregados
2. Gerenciar o consentimento da empresa para participação no benchmark
3. Analisar como a empresa se posiciona em relação ao mercado
"""

import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# --- Path Setup ---
_project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)  # Path for pages subfolder
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

from src.frontend.api_client_v2 import APIClient
from src.frontend.components.layout import footer, header
from src.frontend.utils.auth import verificar_autenticacao

# Cliente API
api_client = APIClient()

# Configurações da página
st.set_page_config(
    page_title="Benchmarking Anonimizado - Auditoria360", page_icon="📊", layout="wide"
)

# Autenticar usuário
if not verificar_autenticacao(redirecionar=True):
    st.stop()

# Constantes
UNIDADE_FORMATACAO = {
    "percentual": "{:.2%}",
    "valor_monetario": "R$ {:.2f}",
    "dias": "{:.0f} dias",
    "quantidade": "{:.0f}",
    None: "{:.2f}",
}


# Funções de formatação
def formatar_valor(valor, unidade_medida):
    """Formata um valor conforme a unidade de medida."""
    if valor is None:
        return "-"

    formato = UNIDADE_FORMATACAO.get(unidade_medida, "{:.2f}")
    return formato.format(valor)


# Funções principais
def carregar_consentimento():
    """Carrega o status de consentimento da empresa atual."""
    try:
        resposta = api_client.get("/api/benchmark/consentimento")
        if resposta.status_code == 200:
            return resposta.json()
        else:
            st.error(f"Erro ao carregar consentimento: {resposta.text}")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar consentimento: {e}")
        return None


def atualizar_consentimento(status: bool, observacoes: str = ""):
    """Atualiza o status de consentimento da empresa."""
    try:
        dados = {"status_consentimento": status, "observacoes": observacoes}
        resposta = api_client.post("/api/benchmark/consentimento", json=dados)
        if resposta.status_code == 200:
            st.success("Preferências de benchmark atualizadas com sucesso!")
            st.session_state.consentimento = resposta.json()
            return True
        else:
            st.error(f"Erro ao atualizar consentimento: {resposta.text}")
            return False
    except Exception as e:
        st.error(f"Erro ao atualizar consentimento: {e}")
        return False


def carregar_metadados():
    """Carrega metadados para filtros do benchmark."""
    try:
        resposta = api_client.get("/api/benchmark/metadata")
        if resposta.status_code == 200:
            return resposta.json()
        else:
            st.error(f"Erro ao carregar metadados: {resposta.text}")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar metadados: {e}")
        return None


def carregar_kpis():
    """Carrega lista de KPIs disponíveis."""
    try:
        resposta = api_client.get("/api/benchmark/kpis")
        if resposta.status_code == 200:
            return resposta.json()
        else:
            st.error(f"Erro ao carregar KPIs: {resposta.text}")
            return []
    except Exception as e:
        st.error(f"Erro ao carregar KPIs: {e}")
        return []


def carregar_dados_benchmark(filtros=None):
    """
    Carrega dados de benchmark com os filtros especificados.

    Args:
        filtros: Dicionário com filtros a serem aplicados

    Returns:
        Dados de benchmark ou None em caso de erro
    """
    try:
        # Construir parâmetros da query
        params = {}
        if filtros:
            if filtros.get("periodo"):
                params["periodo"] = filtros["periodo"]
            if filtros.get("setor"):
                params["setor"] = filtros["setor"]
            if filtros.get("porte"):
                params["porte"] = filtros["porte"]
            if filtros.get("regiao"):
                params["regiao"] = filtros["regiao"]
            if filtros.get("categoria"):
                params["categoria"] = filtros["categoria"]
            if filtros.get("kpi"):
                params["kpi"] = filtros["kpi"]

        # Fazer requisição à API
        resposta = api_client.get("/api/benchmark/dados", params=params)

        if resposta.status_code == 200:
            return resposta.json()
        elif resposta.status_code == 403:
            st.warning(
                "É necessário dar consentimento para acessar os dados de benchmark."
            )
            return None
        else:
            st.error(f"Erro ao carregar dados de benchmark: {resposta.text}")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar dados de benchmark: {e}")
        return None


def plotar_boxplot(dados_kpi, titulo, unidade_medida):
    """
    Gera um gráfico box plot para comparar a posição da empresa.

    Args:
        dados_kpi: Dados do KPI específico
        titulo: Título do gráfico
        unidade_medida: Unidade de medida para formatação

    Returns:
        Figura do Plotly
    """
    fig = go.Figure()

    # Adicionar boxplot
    fig.add_trace(
        go.Box(
            q1=[dados_kpi["percentil_25"]],
            median=[dados_kpi["mediana"]],
            q3=[dados_kpi["percentil_75"]],
            lowerfence=[dados_kpi["percentil_10"]],
            upperfence=[dados_kpi["percentil_90"]],
            mean=[dados_kpi["valor_medio"]],
            name=titulo,
            boxmean=True,
        )
    )

    # Ajustar layout
    fig.update_layout(
        title=f"{titulo}",
        height=350,
        margin=dict(l=5, r=5, b=5, t=50),
        xaxis_title="",
        yaxis_title=unidade_medida,
    )

    return fig


def plotar_comparacao_setores(dados, kpi_nome, kpi_titulo, unidade_medida):
    """
    Gera um gráfico de barras comparando o KPI entre diferentes setores.

    Args:
        dados: Lista de dados de benchmark
        kpi_nome: Nome do KPI a ser plotado
        kpi_titulo: Título amigável do KPI
        unidade_medida: Unidade de medida para formatação
    """
    # Filtrar apenas os dados do KPI selecionado
    df = pd.DataFrame([d for d in dados if d["kpi_nome"] == kpi_nome])

    if df.empty:
        return go.Figure()

    # Agrupar por setor
    df_plot = (
        df[["setor_empresa", "valor_medio", "mediana"]]
        .groupby("setor_empresa")
        .agg({"valor_medio": "mean", "mediana": "mean"})
        .reset_index()
    )

    # Criar gráfico
    fig = px.bar(
        df_plot,
        x="setor_empresa",
        y="valor_medio",
        text_auto=True,
        labels={"setor_empresa": "Setor", "valor_medio": kpi_titulo},
        title=f"{kpi_titulo} - Comparação por Setor",
    )

    # Ajustar layout
    fig.update_layout(
        height=400,
        margin=dict(l=5, r=5, b=5, t=50),
        yaxis_title=unidade_medida or kpi_titulo,
        xaxis_title="Setor",
    )

    # Formatar valores no tooltip conforme unidade de medida
    if unidade_medida == "percentual":
        fig.update_traces(hovertemplate="Setor: %{x}<br>Valor: %{y:.2%}")
        fig.update_yaxis(tickformat=".1%")
    elif unidade_medida == "valor_monetario":
        fig.update_traces(hovertemplate="Setor: %{x}<br>Valor: R$ %{y:.2f}")
        fig.update_yaxis(tickprefix="R$ ")

    return fig


def plotar_comparacao_portes(dados, kpi_nome, kpi_titulo, unidade_medida):
    """
    Gera um gráfico de barras comparando o KPI entre diferentes portes de empresa.
    """
    # Filtrar apenas os dados do KPI selecionado
    df = pd.DataFrame([d for d in dados if d["kpi_nome"] == kpi_nome])

    if df.empty:
        return go.Figure()

    # Ordem lógica dos portes
    ordem_portes = ["pequeno", "medio", "grande"]

    # Agrupar por porte
    df_plot = (
        df[["porte_empresa", "valor_medio", "mediana"]]
        .groupby("porte_empresa")
        .agg({"valor_medio": "mean", "mediana": "mean"})
        .reset_index()
    )

    # Ordenar por porte (pequeno, médio, grande)
    df_plot["porte_ordem"] = df_plot["porte_empresa"].apply(
        lambda x: ordem_portes.index(x.lower()) if x.lower() in ordem_portes else 999
    )
    df_plot = df_plot.sort_values("porte_ordem")

    # Criar gráfico
    fig = px.bar(
        df_plot,
        x="porte_empresa",
        y="valor_medio",
        text_auto=True,
        labels={"porte_empresa": "Porte da Empresa", "valor_medio": kpi_titulo},
        title=f"{kpi_titulo} - Comparação por Porte",
    )

    # Ajustar layout
    fig.update_layout(
        height=400,
        margin=dict(l=5, r=5, b=5, t=50),
        yaxis_title=unidade_medida or kpi_titulo,
        xaxis_title="Porte da Empresa",
    )

    # Formatar valores no tooltip conforme unidade de medida
    if unidade_medida == "percentual":
        fig.update_traces(hovertemplate="Porte: %{x}<br>Valor: %{y:.2%}")
        fig.update_yaxis(tickformat=".1%")
    elif unidade_medida == "valor_monetario":
        fig.update_traces(hovertemplate="Porte: %{x}<br>Valor: R$ %{y:.2f}")
        fig.update_yaxis(tickprefix="R$ ")

    return fig


def plotar_tendencia_tempo(dados, kpi_nome, kpi_titulo, unidade_medida):
    """
    Gera um gráfico de linha mostrando a tendência do KPI ao longo do tempo.
    """
    # Filtrar apenas os dados do KPI selecionado
    df = pd.DataFrame([d for d in dados if d["kpi_nome"] == kpi_nome])

    if df.empty or len(df["periodo_referencia"].unique()) < 2:
        return go.Figure()

    # Agrupar por período
    df_plot = (
        df[["periodo_referencia", "valor_medio", "mediana"]]
        .groupby("periodo_referencia")
        .agg({"valor_medio": "mean", "mediana": "mean"})
        .reset_index()
    )

    # Ordenar por período
    df_plot = df_plot.sort_values("periodo_referencia")

    # Criar gráfico
    fig = px.line(
        df_plot,
        x="periodo_referencia",
        y="valor_medio",
        markers=True,
        labels={"periodo_referencia": "Período", "valor_medio": kpi_titulo},
        title=f"{kpi_titulo} - Tendência ao Longo do Tempo",
    )

    # Ajustar layout
    fig.update_layout(
        height=400,
        margin=dict(l=5, r=5, b=5, t=50),
        yaxis_title=unidade_medida or kpi_titulo,
        xaxis_title="Período",
    )

    # Formatar valores no tooltip conforme unidade de medida
    if unidade_medida == "percentual":
        fig.update_traces(hovertemplate="Data: %{x}<br>Valor: %{y:.2%}")
        fig.update_yaxis(tickformat=".1%")
    elif unidade_medida == "valor_monetario":
        fig.update_traces(hovertemplate="Data: %{x}<br>Valor: R$ %{y:.2f}")
        fig.update_yaxis(tickprefix="R$ ")

    return fig


def exibir_secao_consentimento():
    """Exibe a seção de gerenciamento de consentimento."""
    st.subheader("Configurações de Participação")

    consentimento = st.session_state.get("consentimento")
    status_atual = (
        consentimento.get("status_consentimento", False) if consentimento else False
    )

    with st.container():
        st.markdown(
            """
        ### Participação no Benchmarking Anonimizado
        
        O sistema de Benchmarking Anonimizado permite comparar métricas chave da sua empresa com outras do mesmo
        setor, porte e região, sem identificar informações individuais de nenhuma empresa. 
        
        **Benefícios da participação:**
        - Comparação direta com o mercado e concorrentes
        - Identificação de áreas de melhoria
        - Visualização de tendências do setor
        
        **Garantias de privacidade:**
        - Todos os dados são agregados e anonimizados
        - Empresas só são incluídas em grupos com no mínimo 5 participantes
        - Não há armazenamento de dados individuais identificáveis
        - Valores extremos são protegidos por técnicas de privacidade diferencial
        """
        )

        col1, col2 = st.columns([1, 2])

        with col1:
            status = st.radio(
                "Deseja participar do benchmarking?",
                ["Sim, quero participar", "Não, prefiro não participar"],
                index=0 if status_atual else 1,
            )

            observacoes = st.text_area(
                "Observações (opcional)",
                value=consentimento.get("observacoes", "") if consentimento else "",
                help="Observações opcionais sobre sua preferência de participação",
            )

            if st.button("Atualizar Preferências", use_container_width=True):
                novo_status = status == "Sim, quero participar"
                atualizar_consentimento(novo_status, observacoes)

        with col2:
            st.info(
                """
            **Como funciona:**
            
            1. O sistema coleta KPIs agregados mensalmente (sem dados pessoais de funcionários)
            2. Os dados são anonimizados e agrupados por setor, porte e região
            3. Métricas estatísticas são calculadas (média, mediana, percentis)
            4. Você visualiza como sua empresa se compara ao mercado
            
            Sua participação é totalmente voluntária e pode ser cancelada a qualquer momento.
            """
            )

            if consentimento:
                st.caption(
                    f"""
                Status atual: **{"Participando" if status_atual else "Não participando"}**  
                Última atualização: {consentimento.get("data_consentimento", "").split("T")[0]}
                """
                )


def exibir_graficos_benchmark(dados, kpi_selecionado):
    """
    Exibe os gráficos de benchmark para o KPI selecionado.

    Args:
        dados: Lista de dados de benchmark
        kpi_selecionado: Nome do KPI selecionado
    """
    # Filtrar apenas os dados do KPI selecionado
    kpi_dados = [d for d in dados if d["kpi_nome"] == kpi_selecionado]

    if not kpi_dados:
        st.warning(f"Não há dados disponíveis para o KPI selecionado.")
        return

    # Extrair informações do KPI
    kpi_titulo = kpi_dados[0]["kpi_titulo"]
    kpi_dados[0]["kpi_categoria"]
    unidade_medida = kpi_dados[0]["unidade_medida"]

    # Colunas para diferentes gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            plotar_comparacao_setores(
                dados, kpi_selecionado, kpi_titulo, unidade_medida
            ),
            use_container_width=True,
        )

    with col2:
        st.plotly_chart(
            plotar_comparacao_portes(
                dados, kpi_selecionado, kpi_titulo, unidade_medida
            ),
            use_container_width=True,
        )

    st.plotly_chart(
        plotar_tendencia_tempo(dados, kpi_selecionado, kpi_titulo, unidade_medida),
        use_container_width=True,
    )

    # Exibir os dados em uma tabela detalhada
    with st.expander("Ver dados detalhados"):
        # Transformar em DataFrame para facilitar a exibição
        df = pd.DataFrame(kpi_dados)

        # Selecionar colunas relevantes
        colunas = [
            "periodo_referencia",
            "setor_empresa",
            "porte_empresa",
            "regiao",
            "valor_medio",
            "mediana",
            "percentil_25",
            "percentil_75",
            "valor_minimo",
            "valor_maximo",
            "quantidade_empresas",
        ]

        # Filtrar apenas colunas existentes
        colunas_existentes = [col for col in colunas if col in df.columns]

        # Exibir tabela
        st.dataframe(df[colunas_existentes], use_container_width=True)


def carregar_e_exibir_dados():
    """Carrega os dados e exibe os gráficos de benchmark."""
    # Carregar metadados se ainda não estiverem carregados
    if "metadados" not in st.session_state:
        st.session_state.metadados = carregar_metadados()

    if "kpis" not in st.session_state:
        st.session_state.kpis = carregar_kpis()

    metadados = st.session_state.get("metadados", {})
    kpis = st.session_state.get("kpis", [])

    if not metadados:
        st.warning("Não foi possível carregar os metadados de benchmark.")
        return

    # Preparar opções para os filtros
    opcoes_setor = ["Todos"] + metadados.get("setores", [])
    opcoes_porte = ["Todos"] + metadados.get("portes", [])
    opcoes_regiao = ["Todos"] + metadados.get("regioes", [])
    opcoes_periodo = metadados.get("periodos", [])
    opcoes_categorias = ["Todas"] + metadados.get("categorias", [])

    # Opções de KPIs agrupados por categoria
    kpis_por_categoria = {}
    for kpi in kpis:
        categoria = kpi.get("kpi_categoria", "Outros")
        if categoria not in kpis_por_categoria:
            kpis_por_categoria[categoria] = []
        kpis_por_categoria[categoria].append(kpi)

    # Controles de filtro
    with st.container():
        st.subheader("Filtros")

        col1, col2, col3 = st.columns(3)

        with col1:
            filtro_periodo = st.selectbox(
                "Período de referência",
                options=opcoes_periodo,
                index=0 if opcoes_periodo else None,
                format_func=lambda x: x.split("T")[0] if isinstance(x, str) else x,
            )

            filtro_setor = st.selectbox("Setor", options=opcoes_setor, index=0)

        with col2:
            filtro_porte = st.selectbox(
                "Porte da empresa", options=opcoes_porte, index=0
            )

            filtro_regiao = st.selectbox("Região", options=opcoes_regiao, index=0)

        with col3:
            filtro_categoria = st.selectbox(
                "Categoria de KPI", options=opcoes_categorias, index=0
            )

            # Lista de KPIs filtrada por categoria
            opcoes_kpi = []
            if filtro_categoria == "Todas":
                opcoes_kpi = kpis
            else:
                opcoes_kpi = kpis_por_categoria.get(filtro_categoria, [])

            if opcoes_kpi:
                kpi_selecionado = st.selectbox(
                    "KPI",
                    options=[k["kpi_nome"] for k in opcoes_kpi],
                    format_func=lambda x: next(
                        (k["kpi_titulo"] for k in kpis if k["kpi_nome"] == x), x
                    ),
                )
            else:
                st.warning("Nenhum KPI disponível para a categoria selecionada.")
                kpi_selecionado = None

    # Construir filtros para a API
    filtros = {}
    if filtro_periodo:
        filtros["periodo"] = filtro_periodo

    if filtro_setor != "Todos":
        filtros["setor"] = filtro_setor

    if filtro_porte != "Todos":
        filtros["porte"] = filtro_porte

    if filtro_regiao != "Todos":
        filtros["regiao"] = filtro_regiao

    if filtro_categoria != "Todas":
        filtros["categoria"] = filtro_categoria

    # Carregar dados com os filtros aplicados
    dados_benchmark = carregar_dados_benchmark(filtros)

    if not dados_benchmark:
        st.info(
            "Não há dados disponíveis para os filtros selecionados ou é necessário consentimento para acessar os dados."
        )
        return

    # Exibir KPI selecionado
    if kpi_selecionado and dados_benchmark:
        exibir_graficos_benchmark(dados_benchmark, kpi_selecionado)
    else:
        st.info("Selecione um KPI para visualizar os gráficos de benchmark.")


# Interface principal
def main():
    # Cabeçalho
    header("Benchmarking Anonimizado e Agregado", "📊")

    # Carregar consentimento se não estiver na sessão
    if "consentimento" not in st.session_state:
        st.session_state.consentimento = carregar_consentimento()

    # Abas para separar as seções
    tab_dashboard, tab_config = st.tabs(
        ["Dashboard de Benchmarking", "Configurações de Participação"]
    )

    with tab_dashboard:
        st.markdown(
            """
        # Dashboard de Benchmarking
        
        Compare os indicadores da sua empresa com as médias do mercado usando dados anonimizados e agregados.
        Os dados são exibidos apenas para grupos com no mínimo 5 empresas para garantir a privacidade.
        """
        )

        carregar_e_exibir_dados()

    with tab_config:
        exibir_secao_consentimento()

    # Rodapé
    footer()


if __name__ == "__main__":
    main()

st.title("Benchmarking Anonimizado")


def obter_token():
    return st.text_input("Token JWT", type="password")


def get_benchmarking(token):
    url = "http://localhost:8000/api/benchmarking"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json(), url, headers
    except Exception as e:
        st.error(f"Erro ao buscar benchmarking: {e}")
        return [], url, headers


token = obter_token()
if token:
    benchmarking, url, headers = get_benchmarking(token)
    filtro = st.text_input("Buscar por empresa")
    benchmarking_filtrado = [
        b for b in benchmarking if filtro.lower() in b.get("empresa", "").lower()
    ]
    st.write(benchmarking_filtrado)
    with st.form("Adicionar Benchmark"):
        empresa = st.text_input("Empresa")
        valor = st.text_input("Valor")
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            payload = {"empresa": empresa, "valor": valor}
            resp = requests.post(url, json=payload, headers=headers)
            if resp.status_code == 201:
                st.success("Benchmark adicionado com sucesso!")
            else:
                st.error(f"Erro ao adicionar benchmark: {resp.text}")
else:
    st.warning("Informe o token JWT para acessar os dados.")
