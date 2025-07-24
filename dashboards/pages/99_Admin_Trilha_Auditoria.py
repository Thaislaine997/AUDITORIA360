"""
Página administrativa para visualização da trilha de auditoria detalhada do sistema.
Esta página permite aos administradores da Dpeixer analisar todas as ações realizadas
na plataforma, com diversos filtros e visualizações.
"""
import streamlit as st
import pandas as pd
import altair as alt
import requests
import json
from datetime import datetime, timedelta
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

from src.frontend.utils.auth import verificar_autenticacao, obter_token
from src.frontend.components.layout import criar_sidebar_admin

# Configuração da página
st.set_page_config(
    page_title="Trilha de Auditoria | Admin",
    page_icon="🔍",
    layout="wide"
)

# Verificação de autenticação e permissões de administrador
usuario = verificar_autenticacao()
if not usuario:
    st.warning("Você precisa estar autenticado para acessar esta página.")
    st.stop()

# Verificar se o usuário é administrador
if not verificar_admin(usuario):
    st.error("Você não tem permissão para acessar esta página administrativa.")
    st.stop()

# Configurações do sistema
API_BASE = config.get("API_BASE_URL", "http://localhost:8000")

# Sidebar de navegação admin
criar_sidebar_admin("trilha_auditoria")

# Título principal
st.title("🔍 Trilha de Auditoria do Sistema")
st.write("Visualize e analise todas as ações realizadas na plataforma AUDITORIA360.")

# Criar abas para diferentes visualizações
tab_logs, tab_estatisticas, tab_seguranca = st.tabs([
    "📋 Registros de Atividade", 
    "📊 Estatísticas", 
    "🔒 Segurança"
])

# Token para requisições à API
token = obter_token()
headers = {"Authorization": f"Bearer {token}"}

# Funções de suporte
def formatar_timestamp(ts_str):
    """Formata um timestamp para exibição amigável"""
    try:
        if isinstance(ts_str, str):
            dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        else:
            dt = ts_str
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return ts_str

def truncar_texto(texto, max_len=50):
    """Trunca um texto longo para exibição na tabela"""
    if not texto:
        return ""
    return f"{texto[:max_len]}..." if len(texto) > max_len else texto

def obter_nome_cliente(cliente_id):
    """Obtém o nome do cliente a partir do ID"""
    if not cliente_id:
        return "N/A"
    # Cache de nomes de clientes para evitar múltiplas requisições
    if 'clientes_cache' not in st.session_state:
        st.session_state.clientes_cache = {}
    
    if cliente_id in st.session_state.clientes_cache:
        return st.session_state.clientes_cache[cliente_id]
    
    try:
        # Implementar requisição para obter nome do cliente
        # ...
        nome = f"Cliente {cliente_id[:8]}"  # Placeholder
        st.session_state.clientes_cache[cliente_id] = nome
        return nome
    except:
        return f"Cliente {cliente_id[:8]}"

# TAB 1: REGISTROS DE ATIVIDADE
with tab_logs:
    st.header("Registros de Atividade")
    
    # Filtros em colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dias = st.slider("Período (dias atrás)", 1, 90, 7)
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=dias)
        st.caption(f"De {formatar_timestamp(data_inicio)} até {formatar_timestamp(data_fim)}")
    
    with col2:
        tipos_acao_opcoes = [
            "LOGIN", "LOGOUT", "CREATE", "UPDATE", "DELETE", 
            "UPLOAD_FOLHA", "DOWNLOAD_REPORT", "EXPORT_DATA",
            "APPROVE", "REJECT", "CONSULTA"
        ]
        tipos_acao = st.multiselect("Tipos de ação", tipos_acao_opcoes)
    
    with col3:
        status = st.selectbox("Status da operação", ["Todos", "SUCESSO", "FALHA"])
        if status == "Todos":
            status = None
    
    # Segunda linha de filtros
    col1, col2 = st.columns(2)
    
    with col1:
        # Idealmente, aqui deveria haver uma chamada à API para obter a lista de clientes
        cliente_id = st.text_input("ID do Cliente (opcional)")
        if not cliente_id:
            cliente_id = None
    
    with col2:
        # Idealmente, aqui deveria haver uma chamada à API para obter a lista de usuários
        usuario_id = st.text_input("ID do Usuário (opcional)")
        if not usuario_id:
            usuario_id = None
    
    # Botão para filtrar
    if st.button("🔍 Filtrar Registros", type="primary"):
        with st.spinner("Carregando registros de auditoria..."):
            # Preparar parâmetros
            params = {"dias": dias}
            if cliente_id:
                params["cliente_id"] = cliente_id
            if usuario_id:
                params["usuario_id"] = usuario_id
            if tipos_acao:
                params["tipo_acao"] = tipos_acao
            if status:
                params["status"] = status
                
            # Fazer requisição à API
            try:
                response = requests.get(
                    f"{API_BASE}/audit-logs/",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    logs = response.json()
                    
                    if not logs or len(logs) == 0:
                        st.info("Nenhum registro encontrado com os filtros selecionados.")
                    else:
                        # Formatar dados para exibição
                        df = pd.DataFrame(logs)
                        
                        # Transformações nos dados
                        if 'timestamp_evento' in df.columns:
                            df['timestamp_formatado'] = df['timestamp_evento'].apply(formatar_timestamp)
                        
                        # Adicionar nome do cliente se disponível
                        if 'id_cliente_contexto' in df.columns:
                            df['cliente'] = df['id_cliente_contexto'].apply(obter_nome_cliente)
                        
                        # Truncar detalhes
                        if 'detalhes_alteracao' in df.columns:
                            df['detalhes_resumo'] = df['detalhes_alteracao'].apply(
                                lambda x: truncar_texto(json.dumps(x) if x else "")
                            )
                        
                        # Ordenar e selecionar colunas para exibição
                        colunas_exibir = [
                            'timestamp_formatado', 'email_usuario_acao', 
                            'cliente', 'tipo_acao', 'recurso_afetado',
                            'status_operacao', 'detalhes_resumo'
                        ]
                        
                        # Filtrar apenas colunas que existem
                        colunas_exibir = [col for col in colunas_exibir if col in df.columns]
                        
                        st.dataframe(
                            df[colunas_exibir],
                            use_container_width=True,
                            column_config={
                                "timestamp_formatado": "Data/Hora",
                                "email_usuario_acao": "Usuário",
                                "cliente": "Cliente",
                                "tipo_acao": "Ação",
                                "recurso_afetado": "Recurso",
                                "status_operacao": "Status",
                                "detalhes_resumo": "Detalhes"
                            }
                        )
                        
                        # Exibir contagem total
                        st.caption(f"Total de registros: {len(logs)}")
                        
                        # Botão para exportar para CSV
                        if st.download_button(
                            "📥 Exportar para CSV",
                            data=df.to_csv(index=False).encode('utf-8'),
                            file_name=f"trilha_auditoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        ):
                            pass
                else:
                    st.error(f"Erro ao obter registros: {response.status_code}")
                    if response.text:
                        st.code(response.text)
            except Exception as e:
                st.error(f"Erro ao processar a requisição: {str(e)}")
    
    st.divider()
    
    # Visualização detalhada de um registro
    st.subheader("Visualizar Detalhes de um Log")
    
    id_log = st.text_input("ID do Log de Auditoria")
    if id_log:
        if st.button("🔎 Visualizar Detalhes"):
            st.info("Esta funcionalidade será implementada em breve.")

# TAB 2: ESTATÍSTICAS
with tab_estatisticas:
    st.header("Estatísticas de Auditoria")
    
    # Filtro de período para estatísticas
    dias_estatisticas = st.slider("Analisar dados dos últimos dias", 1, 90, 30, key="dias_estatisticas")
    
    if st.button("📊 Gerar Estatísticas", type="primary"):
        with st.spinner("Calculando estatísticas..."):
            # Fazer requisição à API
            try:
                response = requests.get(
                    f"{API_BASE}/audit-logs/estatisticas",
                    headers=headers,
                    params={"dias": dias_estatisticas}
                )
                
                if response.status_code == 200:
                    dados = response.json()
                    
                    # Layout em duas colunas para métricas e gráficos
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # Métricas gerais
                        if 'contagens' in dados:
                            st.subheader("Contagens Gerais")
                            contagens = dados['contagens']
                            
                            # Criar métricas
                            st.metric("Total de Eventos", contagens.get('total_geral', 0))
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.metric("Sucesso", contagens.get('total_sucesso', 0))
                            with col_b:
                                st.metric("Falhas", contagens.get('total_falha', 0))
                        
                        # Usuários mais ativos
                        if 'por_usuario' in dados and dados['por_usuario']:
                            st.subheader("Usuários Mais Ativos")
                            usuarios = dados['por_usuario']
                            df_usuarios = pd.DataFrame([
                                {"Usuário": u.get('email_usuario_acao', 'N/A'), "Ações": u.get('total', 0)}
                                for u in usuarios
                            ])
                            st.dataframe(df_usuarios, hide_index=True, use_container_width=True)
                    
                    with col2:
                        # Gráfico de eventos por tipo
                        if 'por_tipo' in dados and dados['por_tipo']:
                            st.subheader("Eventos por Tipo")
                            eventos_tipo = dados['por_tipo']
                            df_tipo = pd.DataFrame([
                                {"Tipo": t.get('tipo_acao', 'Desconhecido'), "Quantidade": t.get('total', 0)}
                                for t in eventos_tipo
                            ])
                            
                            # Criar gráfico de barras
                            chart = alt.Chart(df_tipo).mark_bar().encode(
                                x=alt.X('Quantidade:Q', title='Quantidade'),
                                y=alt.Y('Tipo:N', title='Tipo de Ação', sort='-x'),
                                tooltip=['Tipo', 'Quantidade']
                            ).properties(
                                title='Eventos por Tipo de Ação',
                                height=400
                            )
                            
                            st.altair_chart(chart, use_container_width=True)
                    
                    # Segunda linha - gráficos adicionais
                    if 'por_recurso' in dados and dados['por_recurso']:
                        st.subheader("Recursos mais Acessados/Modificados")
                        recursos = dados['por_recurso']
                        df_recursos = pd.DataFrame([
                            {"Recurso": r.get('recurso_afetado', 'Desconhecido'), "Acessos": r.get('total', 0)}
                            for r in recursos
                        ])
                        
                        # Filtrar apenas os 10 principais recursos
                        df_recursos = df_recursos.nlargest(10, 'Acessos')
                        
                        # Criar gráfico de pizza
                        chart = alt.Chart(df_recursos).mark_arc().encode(
                            theta=alt.Theta(field="Acessos", type="quantitative"),
                            color=alt.Color(field="Recurso", type="nominal"),
                            tooltip=['Recurso', 'Acessos']
                        ).properties(
                            title='Top 10 Recursos Acessados',
                            width=500,
                            height=300
                        )
                        
                        st.altair_chart(chart, use_container_width=True)
                else:
                    st.error(f"Erro ao obter estatísticas: {response.status_code}")
                    if response.text:
                        st.code(response.text)
            except Exception as e:
                st.error(f"Erro ao processar a requisição: {str(e)}")

# TAB 3: SEGURANÇA
with tab_seguranca:
    st.header("Análise de Segurança")
    
    st.info("""
    Esta seção destaca possíveis problemas de segurança identificados através da análise
    dos logs de auditoria, como tentativas repetidas de login mal-sucedidas,
    ações suspeitas, ou acessos de IPs não reconhecidos.
    """)
    
    # Filtro para analisar dias
    dias_seguranca = st.slider("Analisar alertas dos últimos dias", 1, 30, 7, key="dias_seguranca")
    
    if st.button("🔒 Verificar Alertas de Segurança", type="primary"):
        with st.spinner("Analisando logs de segurança..."):
            # Fazer requisição à API
            try:
                response = requests.get(
                    f"{API_BASE}/audit-logs/falhas-seguranca",
                    headers=headers,
                    params={"dias": dias_seguranca}
                )
                
                if response.status_code == 200:
                    falhas = response.json()
                    
                    if not falhas or len(falhas) == 0:
                        st.success("Nenhum alerta de segurança identificado no período analisado.")
                    else:
                        st.warning(f"Foram encontrados {len(falhas)} alertas de segurança potenciais.")
                        
                        # Converter para DataFrame
                        df_falhas = pd.DataFrame(falhas)
                        
                        # Formatar datas
                        if 'primeira_tentativa' in df_falhas.columns:
                            df_falhas['primeira_tentativa'] = df_falhas['primeira_tentativa'].apply(formatar_timestamp)
                        if 'ultima_tentativa' in df_falhas.columns:
                            df_falhas['ultima_tentativa'] = df_falhas['ultima_tentativa'].apply(formatar_timestamp)
                        
                        # Renomear colunas para exibição
                        df_falhas = df_falhas.rename(columns={
                            "email_usuario_acao": "Usuário",
                            "ip_origem": "IP",
                            "user_agent": "Navegador/App",
                            "total_falhas": "Tentativas",
                            "primeira_tentativa": "Primeira Tentativa",
                            "ultima_tentativa": "Última Tentativa"
                        })
                        
                        # Exibir em formato tabular
                        st.dataframe(df_falhas, use_container_width=True)
                        
                        # Instruções para ações
                        st.subheader("Ações Recomendadas")
                        st.markdown("""
                        Para usuários com múltiplas tentativas de login falhas:
                        
                        1. **Verificar com o usuário** se foi ele tentando acessar o sistema.
                        2. **Resetar a senha** do usuário se necessário.
                        3. **Monitorar** atividades subsequentes desse usuário.
                        4. **Bloquear IPs** suspeitos se os padrões de tentativa indicarem um ataque.
                        """)
                else:
                    st.error(f"Erro ao obter dados de segurança: {response.status_code}")
                    if response.text:
                        st.code(response.text)
            except Exception as e:
                st.error(f"Erro ao processar a requisição: {str(e)}")
    
    # Seção de informação sobre política de senhas
    with st.expander("ℹ️ Política de Segurança do Sistema"):
        st.markdown("""
        ### Política de Senhas
        - Senhas devem ter no mínimo 8 caracteres.
        - Devem incluir letras maiúsculas, minúsculas, números e caracteres especiais.
        - São bloqueadas após 5 tentativas falhas consecutivas.
        - Expiram a cada 90 dias.
        
        ### Monitoramento de Segurança
        - Todas as ações críticas são registradas na trilha de auditoria.
        - Logins de novas localizações geram alertas.
        - IPs suspeitos são automaticamente bloqueados temporariamente após múltiplas tentativas falhas.
        """)

# Rodapé
st.divider()
st.caption("Trilha de Auditoria | AUDITORIA360 | Acesso exclusivo Dpeixer Admin")
