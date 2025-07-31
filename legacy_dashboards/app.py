import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st


# Environment detection and configuration
def get_environment():
    """Detect the current environment (development, production, etc.)"""
    try:
        # Try Streamlit secrets first
        if hasattr(st, "secrets") and "app" in st.secrets:
            return st.secrets["app"].get("environment", "development")
    except (KeyError, AttributeError):
        pass

    # Fallback to environment variable
    return os.environ.get("ENVIRONMENT", "development")


def is_production():
    """Check if running in production environment"""
    return get_environment().lower() == "production"


# Configure page
st.set_page_config(
    page_title="AUDITORIA360 - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Environment indicator
if not is_production():
    st.sidebar.warning(f"🔧 Ambiente: {get_environment().upper()}")
else:
    st.sidebar.success("🚀 Ambiente: PRODUÇÃO")


# Main dashboard
def main():
    st.title("🏢 AUDITORIA360 - Dashboard Principal")
    st.markdown("---")

    # Sidebar navigation
    st.sidebar.title("📋 Navegação")

    # Dashboard overview
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="📊 Documentos Processados", value="1,234", delta="12")

    with col2:
        st.metric(label="⚠️ Anomalias Detectadas", value="23", delta="-5")

    with col3:
        st.metric(label="✅ Taxa de Conformidade", value="94.2%", delta="2.1%")

    with col4:
        st.metric(label="🕒 Tempo Médio de Análise", value="3.4s", delta="-0.8s")

    st.markdown("---")

    # Sample data visualization
    st.subheader("📈 Análise de Anomalias")

    @st.cache_data
    def get_sample_data():
        return pd.DataFrame(
            {
                "Mês": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
                "Anomalias": [15, 23, 18, 31, 25, 19],
                "Processados": [1200, 1350, 1180, 1420, 1300, 1250],
            }
        )

    data = get_sample_data()

    col1, col2 = st.columns(2)

    with col1:
        fig_anomalies = px.line(
            data,
            x="Mês",
            y="Anomalias",
            title="Anomalias Detectadas por Mês",
            markers=True,
        )
        fig_anomalies.update_layout(showlegend=False)
        st.plotly_chart(fig_anomalies, use_container_width=True)

    with col2:
        fig_processed = px.bar(
            data, x="Mês", y="Processados", title="Documentos Processados por Mês"
        )
        fig_processed.update_layout(showlegend=False)
        st.plotly_chart(fig_processed, use_container_width=True)

    # Recent activity
    st.subheader("🕐 Atividade Recente")

    recent_data = pd.DataFrame(
        {
            "Timestamp": ["2025-01-28 14:30", "2025-01-28 14:15", "2025-01-28 14:00"],
            "Evento": [
                "Anomalia detectada",
                "Documento processado",
                "Análise concluída",
            ],
            "Status": ["⚠️ Atenção", "✅ Sucesso", "✅ Sucesso"],
        }
    )

    st.dataframe(recent_data, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #666;'>
        <p>AUDITORIA360 - Sistema de Auditoria Automatizada | v4.0</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
