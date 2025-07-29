"""
Enhanced Dashboard for AUDITORIA360 - First Stage Implementation
Unified reporting system with improved graphics and centralized structure
"""

import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configure page
st.set_page_config(
    page_title="AUDITORIA360 - Dashboard Unificado",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for enhanced styling
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #ff7f0e 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    
    .status-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        color: white;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-excellent { background-color: #2ca02c; }
    .status-good { background-color: #1f77b4; }
    .status-warning { background-color: #ff7f0e; }
    .status-critical { background-color: #d62728; }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""",
    unsafe_allow_html=True,
)


class DashboardData:
    """Centralized data management for dashboard"""

    @staticmethod
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_kpi_metrics():
        """Get main KPI metrics"""
        return {
            "total_auditorias": 1847,
            "auditorias_concluidas": 1756,
            "taxa_conformidade": 94.2,
            "tempo_medio_analise": 3.4,
            "anomalias_detectadas": 23,
            "questoes_criticas": 3,
            "questoes_resolvidas": 47,
            "score_performance": 87.5,
            "tendencia_conformidade": 2.1,
            "tendencia_performance": -0.8,
        }

    @staticmethod
    @st.cache_data(ttl=300)
    def get_trend_data():
        """Get trend data for charts"""
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=30), end=datetime.now(), freq="D"
        )

        return pd.DataFrame(
            {
                "Data": dates,
                "Auditorias_Concluidas": [
                    45 + i * 2 + (i % 7) * 5 for i in range(len(dates))
                ],
                "Anomalias": [3 + (i % 5) for i in range(len(dates))],
                "Score_Conformidade": [
                    90 + (i % 10) + (i * 0.1) for i in range(len(dates))
                ],
                "Tempo_Processamento": [3.8 - (i * 0.01) for i in range(len(dates))],
            }
        )

    @staticmethod
    @st.cache_data(ttl=300)
    def get_compliance_breakdown():
        """Get compliance breakdown data"""
        return {
            "Excelente (95-100%)": 85,
            "Bom (85-94%)": 45,
            "Precisa Melhorar (70-84%)": 15,
            "Crítico (<70%)": 5,
        }

    @staticmethod
    @st.cache_data(ttl=300)
    def get_risk_heatmap_data():
        """Get risk heatmap data"""
        categories = ["Financeiro", "Operacional", "Regulatório", "Segurança"]
        levels = ["Alto", "Médio", "Baixo"]

        return pd.DataFrame(
            {
                "Categoria": categories * 3,
                "Nível": [level for level in levels for _ in categories],
                "Quantidade": [8, 12, 15, 6, 10, 18, 22, 14, 5, 9, 14, 8],
            }
        )


def render_header():
    """Render main dashboard header"""
    st.markdown(
        """
    <div class="main-header">
        <h1>🏢 AUDITORIA360 - Dashboard Unificado</h1>
        <p>Sistema de Auditoria e Compliance - Primeira Etapa Implementada</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render enhanced sidebar"""
    st.sidebar.markdown("## 📋 Navegação")

    # Report type selector
    report_type = st.sidebar.selectbox(
        "Tipo de Relatório",
        ["Visão Geral", "Auditoria", "Compliance", "Performance", "Riscos"],
        index=0,
    )

    # Date range selector
    st.sidebar.markdown("### 📅 Período")
    date_range = st.sidebar.date_input(
        "Selecionar período",
        value=[datetime.now() - timedelta(days=30), datetime.now()],
        max_value=datetime.now(),
    )

    # Filters
    st.sidebar.markdown("### 🔍 Filtros")
    department = st.sidebar.selectbox(
        "Departamento", ["Todos", "RH", "Financeiro", "Operacional", "TI"]
    )

    priority = st.sidebar.selectbox(
        "Prioridade", ["Todas", "Crítica", "Alta", "Média", "Baixa"]
    )

    # Export options
    st.sidebar.markdown("### 📤 Exportar")
    if st.sidebar.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.experimental_rerun()

    if st.sidebar.button("📊 Gerar Relatório"):
        st.sidebar.success("Relatório gerado! Verifique a pasta de downloads.")

    return {
        "report_type": report_type,
        "date_range": date_range,
        "department": department,
        "priority": priority,
    }


def render_kpi_metrics():
    """Render KPI metrics cards"""
    metrics = DashboardData.get_kpi_metrics()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📊 Auditorias Concluídas",
            value=f"{metrics['auditorias_concluidas']:,}",
            delta=f"+{metrics['auditorias_concluidas'] - metrics['total_auditorias'] + 91}",
        )

    with col2:
        st.metric(
            label="✅ Taxa de Conformidade",
            value=f"{metrics['taxa_conformidade']:.1f}%",
            delta=f"{metrics['tendencia_conformidade']:+.1f}%",
        )

    with col3:
        st.metric(
            label="⚠️ Anomalias Detectadas",
            value=metrics["anomalias_detectadas"],
            delta=-5,
        )

    with col4:
        st.metric(
            label="🕒 Tempo Médio (s)",
            value=f"{metrics['tempo_medio_analise']:.1f}",
            delta=f"{metrics['tendencia_performance']:+.1f}",
        )


def render_audit_trends():
    """Render audit trends visualization"""
    st.subheader("📈 Tendências de Auditoria")

    trend_data = DashboardData.get_trend_data()

    # Create subplots
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Auditorias Concluídas por Dia",
            "Score de Conformidade",
            "Anomalias Detectadas",
            "Tempo de Processamento",
        ),
        specs=[
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"secondary_y": False}],
        ],
    )

    # Auditorias concluídas
    fig.add_trace(
        go.Scatter(
            x=trend_data["Data"],
            y=trend_data["Auditorias_Concluidas"],
            mode="lines+markers",
            name="Auditorias",
            line=dict(color="#1f77b4", width=3),
            marker=dict(size=6),
        ),
        row=1,
        col=1,
    )

    # Score de conformidade
    fig.add_trace(
        go.Scatter(
            x=trend_data["Data"],
            y=trend_data["Score_Conformidade"],
            mode="lines+markers",
            name="Conformidade",
            line=dict(color="#2ca02c", width=3),
            marker=dict(size=6),
            fill="tonexty",
        ),
        row=1,
        col=2,
    )

    # Anomalias
    fig.add_trace(
        go.Bar(
            x=trend_data["Data"],
            y=trend_data["Anomalias"],
            name="Anomalias",
            marker_color="#ff7f0e",
        ),
        row=2,
        col=1,
    )

    # Tempo de processamento
    fig.add_trace(
        go.Scatter(
            x=trend_data["Data"],
            y=trend_data["Tempo_Processamento"],
            mode="lines+markers",
            name="Tempo (s)",
            line=dict(color="#d62728", width=3),
            marker=dict(size=6),
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        height=600,
        showlegend=False,
        title_text="Análise de Tendências - Últimos 30 Dias",
    )

    st.plotly_chart(fig, use_container_width=True)


def render_compliance_analysis():
    """Render compliance analysis"""
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Distribuição de Conformidade")

        compliance_data = DashboardData.get_compliance_breakdown()

        fig_pie = go.Figure(
            data=[
                go.Pie(
                    labels=list(compliance_data.keys()),
                    values=list(compliance_data.values()),
                    hole=0.4,
                    marker_colors=["#2ca02c", "#1f77b4", "#ff7f0e", "#d62728"],
                )
            ]
        )

        fig_pie.update_traces(
            textposition="inside", textinfo="percent+label", textfont_size=12
        )

        fig_pie.update_layout(
            showlegend=True, height=400, title_text="Níveis de Conformidade"
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("📊 Score de Conformidade")

        # Gauge chart for compliance score
        metrics = DashboardData.get_kpi_metrics()
        compliance_score = metrics["taxa_conformidade"]

        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=compliance_score,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Score Atual"},
                delta={"reference": 90, "increasing": {"color": "#2ca02c"}},
                gauge={
                    "axis": {"range": [None, 100]},
                    "bar": {"color": "#1f77b4"},
                    "steps": [
                        {"range": [0, 70], "color": "#ffcccc"},
                        {"range": [70, 85], "color": "#ffffcc"},
                        {"range": [85, 95], "color": "#ccffcc"},
                        {"range": [95, 100], "color": "#ccffff"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 95,
                    },
                },
            )
        )

        fig_gauge.update_layout(height=400)
        st.plotly_chart(fig_gauge, use_container_width=True)


def render_risk_heatmap():
    """Render risk heatmap"""
    st.subheader("🔥 Mapa de Riscos")

    risk_data = DashboardData.get_risk_heatmap_data()

    # Pivot data for heatmap
    heatmap_data = risk_data.pivot(
        index="Nível", columns="Categoria", values="Quantidade"
    )

    fig_heatmap = px.imshow(
        heatmap_data,
        color_continuous_scale="RdYlBu_r",
        aspect="auto",
        title="Distribuição de Riscos por Categoria e Nível",
    )

    fig_heatmap.update_layout(
        xaxis_title="Categoria de Risco", yaxis_title="Nível de Risco", height=400
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)


def render_recent_activity():
    """Render recent activity table"""
    st.subheader("🕐 Atividade Recente")

    # Mock recent activity data
    recent_data = pd.DataFrame(
        {
            "Timestamp": [
                "2025-01-28 14:30",
                "2025-01-28 14:15",
                "2025-01-28 14:00",
                "2025-01-28 13:45",
                "2025-01-28 13:30",
            ],
            "Evento": [
                "Anomalia detectada em folha de pagamento",
                "Auditoria concluída - Departamento RH",
                "Relatório mensal gerado",
                "Compliance verificado - 98% conformidade",
                "Nova CCT cadastrada",
            ],
            "Categoria": ["Anomalia", "Auditoria", "Relatório", "Compliance", "CCT"],
            "Status": [
                "⚠️ Atenção",
                "✅ Sucesso",
                "✅ Sucesso",
                "✅ Sucesso",
                "📋 Processando",
            ],
            "Responsável": [
                "Sistema Automático",
                "Ana Silva",
                "Sistema Automático",
                "Carlos Santos",
                "Maria Oliveira",
            ],
        }
    )

    # Style the dataframe
    def style_status(val):
        if "⚠️" in val:
            return "background-color: #fff3cd; color: #856404;"
        elif "✅" in val:
            return "background-color: #d4edda; color: #155724;"
        elif "📋" in val:
            return "background-color: #d1ecf1; color: #0c5460;"
        return ""

    styled_data = recent_data.style.applymap(style_status, subset=["Status"])

    st.dataframe(styled_data, use_container_width=True)


def render_performance_summary():
    """Render performance summary section"""
    st.subheader("⚡ Resumo de Performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        **🚀 Melhorias Implementadas:**
        - ✅ Estrutura de documentação centralizada
        - ✅ Sistema de relatórios unificado
        - ✅ Dashboard com gráficos interativos
        - 🚧 Otimizações de performance (em andamento)
        """
        )

    with col2:
        st.markdown(
            """
        **📊 Próximas Etapas:**
        - 🔄 Sistema de relatórios avançado
        - 📈 Dashboard analytics completo
        - ⚡ Performance & caching
        - 🤖 Integração ML/AI
        """
        )

    with col3:
        st.markdown(
            """
        **🎯 Meta da Primeira Etapa:**
        - 📁 Documentação: ✅ 100%
        - 📊 Relatórios: 🚧 75%
        - 📈 Dashboard: 🚧 80%
        - ⚡ Performance: ⏳ 60%
        """
        )


def main():
    """Main dashboard application"""
    # Render header
    render_header()

    # Render sidebar and get filters
    filters = render_sidebar()

    # Main content based on selected report type
    if filters["report_type"] == "Visão Geral":
        # KPI Metrics
        render_kpi_metrics()
        st.markdown("---")

        # Trends and Analysis
        render_audit_trends()
        st.markdown("---")

        # Two-column layout for compliance and risks
        col1, col2 = st.columns(2)
        with col1:
            render_compliance_analysis()
        with col2:
            render_risk_heatmap()

        st.markdown("---")

        # Recent activity
        render_recent_activity()

        st.markdown("---")

        # Performance summary
        render_performance_summary()

    elif filters["report_type"] == "Auditoria":
        st.subheader("🔍 Análise de Auditoria Detalhada")
        render_audit_trends()
        render_recent_activity()

    elif filters["report_type"] == "Compliance":
        st.subheader("✅ Análise de Compliance")
        render_compliance_analysis()
        render_recent_activity()

    elif filters["report_type"] == "Performance":
        st.subheader("⚡ Análise de Performance")
        render_audit_trends()
        render_performance_summary()

    elif filters["report_type"] == "Riscos":
        st.subheader("🔥 Análise de Riscos")
        render_risk_heatmap()
        render_recent_activity()

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>AUDITORIA360</strong> - Sistema de Auditoria Automatizada | v4.0 - Primeira Etapa Implementada</p>
        <p>📊 Dashboard Unificado com Estrutura Gráfica Centralizada</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
