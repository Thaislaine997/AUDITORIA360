import streamlit as st
st.set_page_config(layout="wide", page_title="Obrigações e Prazos - AUDITORIA360")

import pandas as pd
from datetime import date, datetime, timedelta
from typing import Optional
import requests
import json
import calendar
import sys
import os
from pathlib import Path

# Adicionar o diretório principal ao path para importar módulos
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# --- Carregamento do CSS para Design System ---
def load_css():
    # Obtenha o caminho para o diretório principal do projeto
    _project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    css_path = os.path.join(_project_root, "assets", "style.css")
    
    if not os.path.exists(css_path):
        css_path = "/workspaces/AUDITORIA360/assets/style.css"
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()  # Carrega os estilos do Design System
# --- Fim do Carregamento do CSS ---

from src.frontend.components.obrigacoes_componentes import (
    carregar_obrigacoes, 
    atualizar_status_obrigacao,
    exibir_lista_obrigacoes,
    exibir_visualizacao_calendario,
    exibir_estatisticas_obrigacoes
)
from src.frontend.utils.auth import verificar_autenticacao, obter_token
from src.frontend.utils.config import obter_config

st.set_page_config(
    page_title="Obrigações e Prazos",
    page_icon="🗓️",
    layout="wide",
)

# Verificar autenticação
usuario = verificar_autenticacao()
if not usuario:
    st.warning("Você precisa estar autenticado para acessar esta página.")
    st.stop()

# Obter configurações
config = obter_config()
API_BASE = config.get("API_BASE_URL", "http://localhost:8000")

# Obter token JWT
token = obter_token()
if not token:
    st.error("Não foi possível obter o token de autenticação.")
    st.stop()

# Título e introdução
st.title("🗓️ Gestão de Obrigações e Prazos")
st.write("Gerencie todas as obrigações legais, prazos e compromissos da sua empresa.")

# Selecionar cliente
clientes = usuario.get("clientes", [])
if not clientes:
    st.error("Você não tem acesso a nenhum cliente.")
    st.stop()

# Sidebar para filtros
with st.sidebar:
    st.header("Filtros")
    
    # Seleção de cliente
    id_cliente = None
    nome_cliente = None
    
    if len(clientes) == 1:
        id_cliente = clientes[0]["id"]
        nome_cliente = clientes[0]["nome"]
        st.info(f"Cliente: {nome_cliente}")
    else:
        cliente_selecionado = st.selectbox(
            "Selecione o cliente",
            options=clientes,
            format_func=lambda x: x["nome"]
        )
        if cliente_selecionado:
            id_cliente = cliente_selecionado["id"]
            nome_cliente = cliente_selecionado["nome"]
    
    # Definir visualização
    visualizacao = st.radio(
        "Tipo de visualização",
        options=["Calendário", "Lista", "Estatísticas"],
        index=0
    )
    
    # Filtro de período
    hoje = date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    if visualizacao == "Calendário":
        mes = st.selectbox(
            "Mês", 
            options=list(range(1, 13)),
            format_func=lambda x: calendar.month_name[x],  # Nome do mês
            index=mes_atual-1
        )
        ano = st.selectbox(
            "Ano", 
            options=list(range(ano_atual-2, ano_atual+3)),
            index=2
        )
    else:
        # Para lista e estatísticas
        periodo_opcoes = [
            "Mês atual",
            "Próximo mês",
            "Últimos 3 meses",
            "Próximos 3 meses",
            "Tudo"
        ]
        periodo_sel = st.selectbox("Período", options=periodo_opcoes, index=0)
        
        # Mapear seleção para datas
        if periodo_sel == "Mês atual":
            inicio = date(hoje.year, hoje.month, 1)
            proximo_mes = hoje.month + 1 if hoje.month < 12 else 1
            proximo_ano = hoje.year if hoje.month < 12 else hoje.year + 1
            fim = date(proximo_ano, proximo_mes, 1) - timedelta(days=1)
        elif periodo_sel == "Próximo mês":
            proximo_mes = hoje.month + 1 if hoje.month < 12 else 1
            proximo_ano = hoje.year if hoje.month < 12 else hoje.year + 1
            inicio = date(proximo_ano, proximo_mes, 1)
            mes_seguinte = proximo_mes + 1 if proximo_mes < 12 else 1
            ano_seguinte = proximo_ano if proximo_mes < 12 else proximo_ano + 1
            fim = date(ano_seguinte, mes_seguinte, 1) - timedelta(days=1)
        elif periodo_sel == "Últimos 3 meses":
            inicio = (hoje.replace(day=1) - timedelta(days=60)).replace(day=1)
            fim = date(hoje.year, hoje.month, 1) - timedelta(days=1)
        elif periodo_sel == "Próximos 3 meses":
            inicio = date(hoje.year, hoje.month, 1)
            fim = (inicio + timedelta(days=90)).replace(day=28)
        else:  # Tudo
            inicio = None
            fim = None
    
    # Filtro de status para a visualização em lista
    if visualizacao == "Lista":
        status_opcoes = ["Todos", "PENDENTE", "EM_ANDAMENTO", "CONCLUIDO", "ATRASADO"]
        status_sel = st.selectbox("Status", options=status_opcoes, index=0)
        status = status_sel if status_sel != "Todos" else None
    else:
        status = None

# Verificar se o cliente foi selecionado
if not id_cliente:
    st.warning("Selecione um cliente para continuar.")
    st.stop()

# Exibir visualização selecionada
try:
    if visualizacao == "Calendário":
        exibir_visualizacao_calendario(API_BASE, token, id_cliente, mes, ano)
    elif visualizacao == "Lista":
        exibir_lista_obrigacoes(API_BASE, token, id_cliente, inicio, status)
    elif visualizacao == "Estatísticas":
        exibir_estatisticas_obrigacoes(API_BASE, token, id_cliente)
except Exception as e:
    st.error(f"Erro ao carregar dados: {str(e)}")
    
# Botão para criar nova obrigação manual
with st.expander("Criar nova obrigação"):
    with st.form("nova_obrigacao"):
        st.write("Adicionar obrigação manual")
        
        descricao = st.text_input("Descrição", max_chars=200)
        col1, col2 = st.columns(2)
        with col1:
            tipo = st.selectbox(
                "Tipo", 
                ["FISCAL", "CONTABIL", "FOLHA", "SOCIETARIO", "LEGAL", "OUTRO"]
            )
            data_venc = st.date_input("Data de vencimento", value=hoje + timedelta(days=30))
        with col2:
            categoria = st.selectbox(
                "Categoria", 
                ["TRIBUTOS", "OBRIGACOES_ACESSORIAS", "FOLHA_PGTO", "DOCUMENTACAO", "CONFORMIDADE", "CONTABEIS", "OUTRO"]
            )
            severidade = st.selectbox("Severidade", ["BAIXA", "MEDIA", "ALTA"])
        observacoes = st.text_area("Observações", max_chars=500)
        submitted = st.form_submit_button("Criar obrigação")
        if submitted:
            if not descricao:
                st.error("A descrição é obrigatória.")
            elif not tipo or not data_venc or not categoria or not severidade:
                st.error("Preencha todos os campos obrigatórios.")
            else:
                dados = {
                    "id_cliente": id_cliente,
                    "tipo_obrigacao": tipo,
                    "descricao": descricao,
                    "data_vencimento": data_venc.isoformat(),
                    "periodo_referencia": date(hoje.year, hoje.month, 1).isoformat(),
                    "categoria": categoria,
                    "severidade": severidade,
                    "observacoes": observacoes
                }
                try:
                    headers = {"Authorization": f"Bearer {token}"}
                    response = requests.post(
                        f"{API_BASE}/obrigacoes/manual",
                        headers=headers,
                        json=dados
                    )
                    if response.status_code == 200:
                        st.success("Obrigação criada com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao criar obrigação: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Erro de comunicação: {str(e)}")
