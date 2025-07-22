import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Auditoria de Folha + ML')
st.write('Dashboard interativo para análise de dados extraídos e resultados de ML.')

@st.cache_data
def get_anomalies():
    """Função para obter dados simulados de anomalias."""
    return pd.DataFrame({
        'CPF': ['12345678909', '98765432100'],
        'Salário': [10000, 5000],
        'Score Anomalia': [0.98, 0.85],
        'Explicação': ['Salário fora do padrão', 'Desconto elevado']
    })

anomalies = get_anomalies()

st.subheader('Anomalias Detectadas')
st.dataframe(anomalies)

fig = px.bar(anomalies, x='CPF', y='Score Anomalia', color='Explicação', title='Scores de Anomalia por CPF')
st.plotly_chart(fig)
