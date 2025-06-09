import streamlit as st
import sys # Add sys
import os # Add os

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) # Adjusted for pages subdir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

import requests
import json
from src.core.config import settings
from src.frontend.utils import (
    get_auth_headers,
    get_api_token,
    get_current_client_id,
    handle_api_error,
    display_user_info_sidebar
)

# Configuração da página (deve ser a primeira chamada do Streamlit)
st.set_page_config(page_title="Sugestões de Impacto das CCTs", layout="wide", initial_sidebar_state="expanded")

# Caminho para o logo
logo_path = os.path.join(_project_root, "assets", "logo.png")

# Logo da empresa na barra lateral
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_column_width=True)
else:
    st.sidebar.warning(f"Logo não encontrado em: {logo_path}")

# Informações do usuário na barra lateral
if 'user_info' not in st.session_state: # Simulação para desenvolvimento standalone
    st.session_state.user_info = {'nome': 'Usuário Teste', 'empresa': 'Empresa Teste'}
    st.session_state.id_cliente = 'TEST_CLIENT_ID'
    st.session_state.api_token = 'test_token' # Token de teste, se necessário para desenvolvimento local
    st.session_state.authenticated = True
    st.session_state.username = "testuser"

display_user_info_sidebar()

st.title("💡 Sugestões de Impacto das CCTs - Revisão e Aprovação")

# Verifica autenticação
api_token = get_api_token()
if not api_token:
    st.warning("Por favor, faça login para acessar esta página.")
    st.stop()

auth_headers = get_auth_headers(api_token)
API_BASE_URL = settings.API_BASE_URL

# Filtros iniciais
# id_cliente = st.text_input("ID do Cliente (para filtrar)") # Removido, será pego da sessão
client_id = get_current_client_id()
if not client_id:
    st.error("ID do Cliente não encontrado na sessão. Por favor, refaça o login.")
    st.stop()

st.info(f"Exibindo sugestões para o Cliente ID: {client_id}")
id_cct_documento = st.text_input("ID do Documento CCT (opcional, para filtrar)")

if st.button("Buscar Sugestões Pendentes"):
    with st.spinner("Buscando sugestões..."):
        params = {"id_cliente_afetado": client_id} # Usa client_id da sessão
        if id_cct_documento:
            params["id_cct_documento_fk"] = id_cct_documento
        try:
            response = requests.get(
                f"{API_BASE_URL}/api/v1/ccts/sugestoes-impacto",
                headers=auth_headers,
                params=params
            )
            if response.status_code == 401:
                handle_api_error(response.status_code)
                st.stop()
            response.raise_for_status()
            sugestoes = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar sugestões: {e}")
            sugestoes = []
        except Exception as e: # Captura outras exceções, como JSONDecodeError
            st.error(f"Erro inesperado ao processar a resposta: {e}")
            sugestoes = []


    if not sugestoes:
        st.info("Nenhuma sugestão pendente encontrada para os filtros aplicados.")
    else:
        for sugestao in sugestoes:
            with st.expander(f"Sugestão ID {sugestao.get('id_sugestao_impacto', 'N/A')} - Tipo: {sugestao.get('tipo_sugestao', 'N/A')}"):
                st.markdown(f"**Cláusula Base:** {sugestao.get('texto_clausula_cct_base', 'N/A')}")
                st.markdown(f"**Justificativa IA:** {sugestao.get('justificativa_sugestao_ia', 'N/A')}")
                st.markdown(f"**Data de Vigência Sugerida:** {sugestao.get('data_inicio_vigencia_sugerida', 'N/A')}")
                st.markdown(f"**Status:** {sugestao.get('status_sugestao', 'PENDENTE')}")
                
                dados_editados = {}
                # Usar .get() com fallback para evitar KeyError se os campos não existirem
                if sugestao.get('tipo_sugestao') == 'ALTERACAO_RUBRICA_CLIENTE':
                    st.markdown(f"**Rubrica Afetada:** {sugestao.get('codigo_rubrica_cliente_existente', 'N/A')}")
                    try:
                        alteracoes_str = sugestao.get('json_alteracoes_sugeridas_rubrica')
                        alteracoes = json.loads(alteracoes_str) if alteracoes_str else []
                        for alt in alteracoes:
                            novo_valor = st.text_input(
                                f"{alt.get('campo_a_alterar', 'Campo Desconhecido')}",
                                value=str(alt.get('novo_valor_sugerido', '')),
                                key=f"{sugestao.get('id_sugestao_impacto')}_{alt.get('campo_a_alterar')}"
                            )
                            alt['novo_valor_sugerido'] = novo_valor
                        dados_editados['json_alteracoes_sugeridas_rubrica'] = json.dumps(alteracoes)
                    except json.JSONDecodeError:
                        st.error("Erro ao decodificar JSON de alterações sugeridas.")
                        dados_editados['json_alteracoes_sugeridas_rubrica'] = sugestao.get('json_alteracoes_sugeridas_rubrica', '[]')


                elif sugestao.get('tipo_sugestao') == 'NOVA_RUBRICA_CLIENTE':
                    dados_editados['codigo_sugerido_nova_rubrica'] = st.text_input("Código Nova Rubrica", value=sugestao.get('codigo_sugerido_nova_rubrica', ''))
                    dados_editados['descricao_sugerida_nova_rubrica'] = st.text_input("Descrição Nova Rubrica", value=sugestao.get('descricao_sugerida_nova_rubrica', ''))
                    dados_editados['tipo_sugerido_nova_rubrica'] = st.text_input("Tipo Nova Rubrica", value=sugestao.get('tipo_sugerido_nova_rubrica', ''))
                    dados_editados['natureza_esocial_sugerida'] = st.text_input("Natureza eSocial", value=sugestao.get('natureza_esocial_sugerida', ''))
                    try:
                        incidencias_str = sugestao.get('json_sugestao_incidencias_completa_nova_rubrica')
                        incidencias = json.loads(incidencias_str) if incidencias_str else {}
                        for k, v in incidencias.items():
                            incidencias[k] = st.text_input(
                                f"{k}",
                                value=str(v),
                                key=f"{sugestao.get('id_sugestao_impacto')}_{k}"
                            )
                        dados_editados['json_sugestao_incidencias_completa_nova_rubrica'] = json.dumps(incidencias)
                    except json.JSONDecodeError:
                        st.error("Erro ao decodificar JSON de incidências sugeridas.")
                        dados_editados['json_sugestao_incidencias_completa_nova_rubrica'] = sugestao.get('json_sugestao_incidencias_completa_nova_rubrica', '{}')

                elif sugestao.get('tipo_sugestao', '').startswith('ATUALIZACAO_PARAMETRO_LEGAL'):
                    dados_editados['novo_valor_sugerido_parametro'] = st.text_input("Novo Valor Sugerido", value=sugestao.get('novo_valor_sugerido_parametro', ''))
                
                notas = st.text_area("Notas de Revisão", key=f"notas_{sugestao.get('id_sugestao_impacto')}")
                
                col1, col2 = st.columns(2)
                username = st.session_state.get("username", "usuário_desconhecido")
                if 'user_info' in st.session_state and st.session_state.user_info.get('username'):
                    username = st.session_state.user_info.get('username')


                with col1:
                    if st.button("Aprovar e Aplicar", key=f"aprovar_{sugestao.get('id_sugestao_impacto')}"):
                        payload = {
                            "acao_usuario": "APROVAR_APLICAR",
                            "usuario_revisao": username,
                            "notas_revisao_usuario": notas,
                            "dados_sugestao_atualizados_json": json.dumps(dados_editados) if dados_editados else None
                        }
                        try:
                            response_process = requests.post(
                                f"{API_BASE_URL}/api/v1/ccts/sugestoes-impacto/{sugestao.get('id_sugestao_impacto')}/processar",
                                headers=auth_headers,
                                json=payload
                            )
                            if response_process.status_code == 401:
                                handle_api_error(response_process.status_code)
                                # Não usar st.stop() aqui para permitir que outros botões funcionem
                            else:
                                response_process.raise_for_status()
                                st.success(f"Sugestão {sugestao.get('id_sugestao_impacto')} aprovada e aplicada com sucesso!")
                                st.rerun() # Recarrega para atualizar a lista
                        except requests.exceptions.RequestException as e:
                            st.error(f"Erro ao aprovar sugestão {sugestao.get('id_sugestao_impacto')}: {e}")
                        except Exception as e:
                             st.error(f"Erro inesperado ao processar aprovação: {e}")

                with col2:
                    if st.button("Rejeitar", key=f"rejeitar_{sugestao.get('id_sugestao_impacto')}"):
                        payload = {
                            "acao_usuario": "REJEITAR",
                            "usuario_revisao": username,
                            "notas_revisao_usuario": notas,
                            "dados_sugestao_atualizados_json": None # Não envia dados editados ao rejeitar
                        }
                        try:
                            response_process = requests.post(
                                f"{API_BASE_URL}/api/v1/ccts/sugestoes-impacto/{sugestao.get('id_sugestao_impacto')}/processar",
                                headers=auth_headers,
                                json=payload
                            )
                            if response_process.status_code == 401:
                                handle_api_error(response_process.status_code)
                            else:
                                response_process.raise_for_status()
                                st.success(f"Sugestão {sugestao.get('id_sugestao_impacto')} rejeitada com sucesso!")
                                st.rerun() # Recarrega para atualizar a lista
                        except requests.exceptions.RequestException as e:
                            st.error(f"Erro ao rejeitar sugestão {sugestao.get('id_sugestao_impacto')}: {e}")
                        except Exception as e:
                             st.error(f"Erro inesperado ao processar rejeição: {e}")

# Adicionar um bloco de simulação para quando o arquivo é executado diretamente
if __name__ == "__main__":
    # Simula o estado da sessão para teste local, se não estiver já configurado no topo
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = True
        st.session_state.api_token = "your_local_dev_token" # Use um token válido se sua API local exigir
        st.session_state.user_info = {"nome": "Dev User", "empresa": "Dev Company", "username": "devuser"}
        st.session_state.id_cliente = "DEV_CLIENT_001" # ID de cliente para teste
        # Certifique-se de que API_BASE_URL está acessível ou defina um valor de teste
        # settings.API_BASE_URL = "http://localhost:8001" # Exemplo, se diferente do padrão

    if not st.session_state.get("authenticated"):
        st.error("Simulação: Usuário não autenticado.")
    else:
        st.success("Simulação: Usuário autenticado. Carregando página...")
        # O restante do código da página será executado normalmente
        # Se precisar de mais simulações específicas para esta página, adicione aqui.
        pass
