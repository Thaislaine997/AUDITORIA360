import streamlit as st
import sys # Add sys
import os # Add os

# --- Path Setup ---
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')) # Adjusted for pages subdir
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# --- End Path Setup ---

import requests
from datetime import date
import pandas as pd

from src.core.config import settings
# Ajustar import para usar os utilitários globais de forma consistente
from src.frontend.utils import (
    display_user_info_sidebar as global_display_user_info_sidebar, 
    handle_api_error, 
    get_api_token as get_global_api_token, 
    get_current_client_id as get_global_current_client_id, # Mantido para consistência, embora possa não ser usado diretamente
    get_auth_headers as get_global_auth_headers # Importar get_auth_headers global
)
from src.core.log_utils import logger # Adicionar import do logger

# Funções wrapper locais para consistência
def get_api_token() -> str | None:
    return get_global_api_token()

def get_current_client_id() -> str | None: # Admin pode não operar no contexto de um cliente específico
    return get_global_current_client_id()

def display_user_info_sidebar():
    global_display_user_info_sidebar()

def get_auth_headers_admin_params(): # Wrapper local para headers
    token = get_api_token()
    return get_global_auth_headers(token) # Chama o global com o token

def mostrar_pagina_admin_parametros_legais():
    st.set_page_config(page_title="Administração de Parâmetros Legais - AUDITORIA360", layout="wide") # Nome da página atualizado
    
    # --- Logo --- (Removido, display_user_info_sidebar cuida disso)
    # st.sidebar.markdown(\"---\") # Removido

    api_token = get_api_token()
    # id_cliente_atual = get_current_client_id() # Removido ou comentado, pois admin pode não ter cliente específico

    # Verificação de autenticação
    if not api_token: 
        st.warning("Acesso restrito. Por favor, faça login com uma conta administrativa.")
        if st.button("Retornar ao Login"):
            try:
                st.switch_page("painel.py")
            except AttributeError:
                st.page_link("painel.py", label="Retornar ao Login", icon="🏠")
            except Exception as e:
                 st.page_link("painel.py", label="Retornar ao Login", icon="🏠")
                 logger.warning(f"Falha ao usar st.switch_page para painel.py: {e}, usando page_link.")
        st.stop()
    
    # Adicionar verificação de perfil/role se disponível em st.session_state.user_info
    user_info = st.session_state.get("user_info", {})
    user_roles = user_info.get("roles", []) # Supondo que 'roles' seja uma lista de strings
    # Idealmente, o backend protegeria essas rotas, mas uma verificação no frontend é uma boa prática adicional.
    # if "admin" not in user_roles: # Descomentar e ajustar se a role 'admin' for usada
    #     st.error("Você não tem permissão para acessar esta página. Contate o administrador.")
    #     logger.warning(f"Usuário {user_info.get(\'username\', \'desconhecido\')} sem role \'admin\' tentou acessar Admin Parâmetros.")
    #     st.stop()

    display_user_info_sidebar()

    st.title("⚙️ Administração de Parâmetros Legais")
    st.caption("Gestão de tabelas de INSS, IRRF, Salário Família, Salário Mínimo, FGTS e outros.")
    # st.caption(f"Cliente ID: {id_cliente_atual}") # Removido ou comentado

    PARAMETROS_CONFIG = {
        "INSS": {"endpoint": "inss", "form_fields": {"id_parametro_inss": "ID (Opcional, deixe em branco para auto)", "data_inicio_vigencia": "Data Início Vigência", "faixa_salarial_de": "Faixa Salarial De (R$)", "faixa_salarial_ate": "Faixa Salarial Até (R$)", "aliquota_efetiva_percentual": "Alíquota Efetiva (%)", "parcela_a_deduzir": "Parcela a Deduzir (R$)", "descricao": "Descrição (Opcional)"}, "list_columns": ["id_parametro_inss", "data_inicio_vigencia", "faixa_salarial_de", "faixa_salarial_ate", "aliquota_efetiva_percentual", "parcela_a_deduzir", "descricao"]},
        "IRRF": {"endpoint": "irrf", "form_fields": {"id_parametro_irrf": "ID (Opcional)", "data_inicio_vigencia": "Data Início Vigência", "base_calculo_de": "Base Cálculo De (R$)", "base_calculo_ate": "Base Cálculo Até (R$)", "aliquota_percentual": "Alíquota (%)", "parcela_a_deduzir_imposto": "Parcela a Deduzir (R$)", "limite_deducao_simplificada": "Limite Dedução Simplificada (R$)", "descricao": "Descrição (Opcional)"}, "list_columns": ["id_parametro_irrf", "data_inicio_vigencia", "base_calculo_de", "base_calculo_ate", "aliquota_percentual", "parcela_a_deduzir_imposto", "limite_deducao_simplificada", "descricao"]},
        "Salário Família": {"endpoint": "salario-familia", "form_fields": {"id_parametro_salario_familia": "ID (Opcional)", "data_inicio_vigencia": "Data Início Vigência", "remuneracao_mensal_ate": "Remuneração Mensal Até (R$)", "valor_quota_por_filho": "Valor da Quota (R$)", "descricao": "Descrição (Opcional)"}, "list_columns": ["id_parametro_salario_familia", "data_inicio_vigencia", "remuneracao_mensal_ate", "valor_quota_por_filho", "descricao"]},
        "Salário Mínimo": {"endpoint": "salario-minimo", "form_fields": {"id_parametro_salario_minimo": "ID (Opcional)", "data_inicio_vigencia": "Data Início Vigência", "valor_mensal": "Valor Mensal (R$)", "valor_diario": "Valor Diário (R$)", "valor_hora": "Valor Hora (R$)", "norma_legal_referencia": "Norma Legal (Opcional)", "regiao_geografica_aplicavel": "Região (Opcional, ex: Nacional, SP, RJ)"}, "list_columns": ["id_parametro_salario_minimo", "data_inicio_vigencia", "valor_mensal", "valor_diario", "valor_hora", "norma_legal_referencia", "regiao_geografica_aplicavel"]},
        "FGTS": {"endpoint": "fgts", "form_fields": {"id_parametro_fgts": "ID (Opcional)", "data_inicio_vigencia": "Data Início Vigência", "percentual_aliquota_normal": "Alíquota Normal (%)", "percentual_aliquota_contrato_verde_amarelo": "Alíquota Contrato Verde/Amarelo (%)", "percentual_aliquota_menor_aprendiz": "Alíquota Menor Aprendiz (%)", "descricao": "Descrição (Opcional)"}, "list_columns": ["id_parametro_fgts", "data_inicio_vigencia", "percentual_aliquota_normal", "percentual_aliquota_contrato_verde_amarelo", "percentual_aliquota_menor_aprendiz", "descricao"]}
        # Adicionar outros parâmetros como "Outros Parâmetros Legais" se houver um endpoint genérico
    }

    aba_selecionada = st.selectbox("Escolha o parâmetro para gerenciar:", list(PARAMETROS_CONFIG.keys()), key="sel_param_legal")

    if aba_selecionada:
        config = PARAMETROS_CONFIG[aba_selecionada]
        endpoint_url = f"{settings.API_BASE_URL}/api/v1/parametros-legais-admin/{config['endpoint']}"
        headers = get_auth_headers_admin_params() # Usar a função wrapper

        st.header(f"Histórico de Parâmetros {aba_selecionada}")
        
        # Botão para Listar/Atualizar
        if st.button(f"Listar/Atualizar Parâmetros {aba_selecionada}", key=f"btn_list_{config['endpoint']}"):
            st.session_state[f"data_{config['endpoint']}"] = None # Forçar recarga

        # Carregar e exibir dados
        if f"data_{config['endpoint']}" not in st.session_state or st.session_state[f"data_{config['endpoint']}"] is None:
            try:
                logger.info(f"Buscando parâmetros para {aba_selecionada} em {endpoint_url}") # Logger
                r = requests.get(endpoint_url, headers=headers)
                if r.status_code == 401:
                    handle_api_error(r.status_code) # Chama o handler global
                    st.rerun()
                    return 
                r.raise_for_status()
                st.session_state[f"data_{config['endpoint']}"] = r.json()
            except requests.exceptions.HTTPError as http_err: # Tratamento de erro HTTP mais específico
                logger.error(f"Erro HTTP ao buscar parâmetros {aba_selecionada}: {http_err.response.status_code} - {http_err.response.text}")
                error_detail = http_err.response.text
                try:
                    error_detail = http_err.response.json().get("detail", error_detail)
                except ValueError: # json.JSONDecodeError é um subtipo de ValueError
                    pass
                st.error(f"Erro ao buscar parâmetros {aba_selecionada} (HTTP {http_err.response.status_code}): {error_detail}")
                st.session_state[f"data_{config['endpoint']}"] = []
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro de conexão ao buscar parâmetros {aba_selecionada}: {e}", exc_info=True)
                st.error(f"Erro de conexão ao buscar parâmetros {aba_selecionada}: {e}")
                st.session_state[f"data_{config['endpoint']}"] = []
            except ValueError: # Tratar JSONDecodeError
                logger.error(f"Erro ao decodificar JSON da busca de parâmetros {aba_selecionada}: {r.text if 'r' in locals() else 'Resposta não disponível'}")
                st.error(f"Erro ao processar a resposta do servidor (parâmetros {aba_selecionada}).")
                st.session_state[f"data_{config['endpoint']}"] = []
            except Exception as e: # Captura genérica
                logger.error(f"Erro inesperado ao processar parâmetros {aba_selecionada}: {e}", exc_info=True)
                st.error(f"Erro inesperado ao processar parâmetros {aba_selecionada}: {e}")
                st.session_state[f"data_{config['endpoint']}"] = []
        
        data_to_display = st.session_state.get(f"data_{config['endpoint']}", [])
        if data_to_display:
            df = pd.DataFrame(data_to_display)
            # Garantir que todas as colunas esperadas existam no DataFrame, preenchendo com None se faltarem
            for col_name in config["list_columns"]:
                if col_name not in df.columns:
                    df[col_name] = None
            st.dataframe(df[config["list_columns"]], use_container_width=True, hide_index=True)
        else:
            st.info(f"Nenhum parâmetro {aba_selecionada} encontrado ou erro ao carregar.")

        st.subheader(f"Adicionar/Editar Parâmetro {aba_selecionada}")
        # Usar um ID de formulário dinâmico para evitar conflitos entre abas se fossem renderizadas simultaneamente
        with st.form(f"form_novo_{config['endpoint']}", clear_on_submit=True):
            payload = {}
            # Campo para ID (para edição) - opcionalmente escondido ou apenas para referência
            param_id_for_edit = st.text_input("ID do Parâmetro para Editar (deixe em branco para criar novo)", key=f"id_edit_{config['endpoint']}")
            
            for field, label in config["form_fields"].items():
                if "data_inicio_vigencia" in field:
                    payload[field] = st.date_input(label, value=date.today(), key=f"{config['endpoint']}_{field}")
                elif any(keyword in field for keyword in ["percentual", "aliquota", "valor", "parcela", "faixa", "base_calculo", "limite"]):
                     # Tentar converter para float, mas manter como string se falhar ou se for uma faixa complexa
                    payload[field] = st.number_input(label, value=None, format="%.2f", key=f"{config['endpoint']}_{field}")
                else:
                    payload[field] = st.text_input(label, key=f"{config['endpoint']}_{field}")
            
            submitted = st.form_submit_button("Salvar Parâmetro")
            if submitted:
                # Converter datas para string ISO format
                for key, value in payload.items():
                    if isinstance(value, date):
                        payload[key] = value.isoformat()
                
                # Remover campos vazios do payload, exceto aqueles que podem ser intencionalmente None/null (ex: data_fim_vigencia)
                # A API deve tratar campos opcionais não enviados.
                final_payload = {k: v for k, v in payload.items() if v is not None and v != ""}
                
                # Lógica para POST (criar) ou PUT (atualizar)
                request_method = requests.post
                url_to_call = endpoint_url
                success_message = f"Parâmetro {aba_selecionada} salvo com sucesso!"

                if param_id_for_edit: # Se um ID foi fornecido, tentamos um PUT
                    # A API deve aceitar o ID no corpo ou no path. Se for no path:
                    url_to_call = f"{endpoint_url}/{param_id_for_edit}"
                    request_method = requests.put
                    # Remover o ID do payload se ele estiver no path e não for esperado no corpo do PUT
                    # if config["form_fields"].keys()[0] in final_payload: # Ex: id_parametro_inss
                    #    del final_payload[config["form_fields"].keys()[0]] 
                    # A linha acima é um exemplo, a lógica exata depende da API.
                    # Se o ID principal (ex: id_parametro_inss) está no payload e é usado para identificar o registro no PUT, mantenha-o.
                    # Se o ID é apenas para o path, e o payload é o restante dos dados, ajuste.
                    # Por simplicidade, vamos assumir que o ID pode estar no payload para PUT também, ou a API o ignora se estiver no path.

                try:
                    logger.info(f"Salvando parâmetro {aba_selecionada}. Método: {'PUT' if param_id_for_edit else 'POST'}, URL: {url_to_call}, Payload: {final_payload}") # Logger
                    r = request_method(url_to_call, json=final_payload, headers=headers)
                    if r.status_code == 401:
                        handle_api_error(r.status_code)
                        st.rerun() 
                        # Não retorna para exibir erro no form
                    elif r.status_code in [200, 201]: 
                        st.success(success_message)
                        logger.info(success_message) # Logger
                        st.session_state[f"data_{config['endpoint']}"] = None 
                        st.rerun()
                    else:
                        error_text = r.text
                        try:
                            error_text = r.json().get("detail", error_text)
                        except ValueError:
                            pass
                        st.error(f"Erro ao salvar parâmetro {aba_selecionada} (Cód: {r.status_code}): {error_text}")
                        logger.error(f"Erro HTTP ao salvar parâmetro {aba_selecionada} ({r.status_code}): {r.text}") # Logger
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro de conexão ao salvar parâmetro: {e}")
                    logger.error(f"Erro de conexão ao salvar parâmetro {aba_selecionada}: {e}", exc_info=True) # Logger
                except Exception as e:
                    st.error(f"Erro inesperado ao salvar parâmetro: {e}")
                    logger.error(f"Erro inesperado ao salvar parâmetro {aba_selecionada}: {e}", exc_info=True) # Logger

if __name__ == "__main__":
    # Simulação do st.session_state para fins de teste local
    if 'token' not in st.session_state: # Alterado de api_token para token
        st.session_state.token = "token_simulado_admin_params" 
    # client_id pode não ser relevante para admin global, mas mantido para consistência se utils depender dele
    if 'client_id' not in st.session_state: # Alterado de id_cliente para client_id
        st.session_state.client_id = "admin_sem_cliente_especifico" 
    if 'user_info' not in st.session_state:
        # Adicionar 'roles' para simular verificação de admin, se implementada
        st.session_state.user_info = {"name": "Admin Teste", "username": "superadmin", "roles": ["admin"]}
    
    mostrar_pagina_admin_parametros_legais()
