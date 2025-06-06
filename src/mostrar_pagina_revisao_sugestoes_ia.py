"""
Função para mostrar a página de revisão de sugestões da IA.
Esta página permite listar, visualizar detalhes, editar, aprovar e rejeitar sugestões geradas pela IA.
"""
import streamlit as st
import requests
import json
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime, date

# Centralização de mensagens
MESSAGES = {
    "login_required": "Faça login para acessar esta funcionalidade.",
    "no_suggestions": "Nenhuma sugestão com status '{status}' encontrada.",
    "success_apply": "Parâmetro legal aplicado com sucesso: {title}",
    "error_required": "Campo obrigatório não preenchido: {field}",
    "error_json": "Formato JSON inválido para o campo {label}",
    "error_connection": "Erro de conexão: {e}",
    "error_unexpected": "Erro inesperado: {e}",
}

def get_schema_por_tipo_parametro(tipo_parametro: str) -> Dict[str, Any]:
    """
    Retorna o schema de edição para cada tipo de parâmetro legal.
    Isso define a estrutura do formulário de edição.
    """
    tipo_parametro = tipo_parametro.upper()
    
    # Definição de schema para INSS
    if tipo_parametro == "INSS":
        return {
            "fields": [
                {
                    "name": "data_inicio_vigencia",
                    "type": "date",
                    "label": "Data Início Vigência",
                    "required": True,
                    "help": "Data em que esta tabela começa a valer"
                },
                {
                    "name": "data_fim_vigencia",
                    "type": "date",
                    "label": "Data Fim Vigência (opcional)",
                    "required": False,
                    "help": "Data em que esta tabela deixa de valer. Deixe em branco para vigência indefinida."
                },
                {
                    "name": "faixas",
                    "type": "json_array",
                    "label": "Faixas de Contribuição (JSON)",
                    "required": True,
                    "help": "Lista de faixas no formato [{'valor_inicial': 0, 'valor_final': 1412.00, 'aliquota': 7.5}, ...]",
                    "height": 200,
                    "structure": [
                        {"field": "valor_inicial", "type": "number", "required": True},
                        {"field": "valor_final", "type": "number", "required": False},
                        {"field": "aliquota", "type": "number", "required": True}
                    ]
                },
                {
                    "name": "valor_teto_contribuicao",
                    "type": "number",
                    "label": "Valor Teto Contribuição",
                    "required": False,
                    "help": "Valor máximo para base de cálculo do INSS",
                    "step": 0.01
                },
                {
                    "name": "observacao",
                    "type": "text",
                    "label": "Observação (opcional)",
                    "required": False
                }
            ],
            "api_endpoint": "/param-legais/inss/",
            "title": "Tabela INSS"
        }
    
    # Definição de schema para IRRF
    elif tipo_parametro == "IRRF":
        return {
            "fields": [
                {
                    "name": "data_inicio_vigencia",
                    "type": "date",
                    "label": "Data Início Vigência",
                    "required": True,
                    "help": "Data em que esta tabela começa a valer"
                },
                {
                    "name": "data_fim_vigencia",
                    "type": "date",
                    "label": "Data Fim Vigência (opcional)",
                    "required": False,
                    "help": "Data em que esta tabela deixa de valer. Deixe em branco para vigência indefinida."
                },
                {
                    "name": "faixas",
                    "type": "json_array",
                    "label": "Faixas de IRRF (JSON)",
                    "required": True,
                    "help": "Lista de faixas no formato [{'base_calculo_inicial': 0, 'base_calculo_final': 2259.20, 'aliquota': 0, 'parcela_a_deduzir': 0}, ...]",
                    "height": 200,
                    "structure": [
                        {"field": "base_calculo_inicial", "type": "number", "required": True},
                        {"field": "base_calculo_final", "type": "number", "required": False},
                        {"field": "aliquota", "type": "number", "required": True},
                        {"field": "parcela_a_deduzir", "type": "number", "required": True}
                    ]
                },
                {
                    "name": "deducao_por_dependente",
                    "type": "number",
                    "label": "Dedução por Dependente (R$)",
                    "required": True,
                    "help": "Valor de dedução por dependente",
                    "step": 0.01
                },
                {
                    "name": "limite_desconto_simplificado",
                    "type": "number",
                    "label": "Limite Desconto Simplificado (R$)",
                    "required": False,
                    "help": "Valor limite para desconto simplificado mensal",
                    "step": 0.01
                },
                {
                    "name": "observacao",
                    "type": "text",
                    "label": "Observação (opcional)",
                    "required": False
                }
            ],
            "api_endpoint": "/param-legais/irrf/",
            "title": "Tabela IRRF"
        }
    
    # Definição de schema para FGTS
    elif tipo_parametro == "FGTS":
        return {
            "fields": [
                {
                    "name": "data_inicio_vigencia",
                    "type": "date",
                    "label": "Data Início Vigência",
                    "required": True,
                    "help": "Data em que este parâmetro começa a valer"
                },
                {
                    "name": "data_fim_vigencia",
                    "type": "date",
                    "label": "Data Fim Vigência (opcional)",
                    "required": False,
                    "help": "Data em que este parâmetro deixa de valer. Deixe em branco para vigência indefinida."
                },
                {
                    "name": "aliquota_mensal",
                    "type": "number",
                    "label": "Alíquota Mensal (%)",
                    "required": True,
                    "help": "Percentual de depósito mensal do FGTS",
                    "step": 0.1
                },
                {
                    "name": "aliquota_multa_rescisoria",
                    "type": "number",
                    "label": "Alíquota Multa Rescisória (%)",
                    "required": True,
                    "help": "Percentual da multa rescisória do FGTS",
                    "step": 0.1
                },
                {
                    "name": "observacao",
                    "type": "text",
                    "label": "Observação (opcional)",
                    "required": False
                }
            ],
            "api_endpoint": "/param-legais/fgts/",
            "title": "Parâmetros FGTS"
        }
    
    # Definição de schema para Salário Mínimo
    elif tipo_parametro == "SALARIO_MINIMO":
        return {
            "fields": [
                {
                    "name": "data_inicio_vigencia",
                    "type": "date",
                    "label": "Data Início Vigência",
                    "required": True,
                    "help": "Data em que este valor de salário mínimo começa a valer"
                },
                {
                    "name": "data_fim_vigencia",
                    "type": "date",
                    "label": "Data Fim Vigência (opcional)",
                    "required": False,
                    "help": "Data em que este valor de salário mínimo deixa de valer. Deixe em branco para vigência indefinida."
                },
                {
                    "name": "valor_nacional",
                    "type": "number",
                    "label": "Valor Nacional (R$)",
                    "required": True,
                    "help": "Valor do salário mínimo nacional",
                    "step": 0.01
                },
                {
                    "name": "valores_regionais",
                    "type": "json_object",
                    "label": "Valores Regionais (JSON, opcional)",
                    "required": False,
                    "help": "Valores regionais no formato {'SP': 1500.00, 'RJ': 1450.00}",
                    "height": 150
                },
                {
                    "name": "observacao",
                    "type": "text",
                    "label": "Observação (opcional)",
                    "required": False
                }
            ],
            "api_endpoint": "/param-legais/salario-minimo/",
            "title": "Salário Mínimo"
        }
    
    # Definição de schema para Salário Família
    elif tipo_parametro == "SALARIO_FAMILIA":
        return {
            "fields": [
                {
                    "name": "data_inicio_vigencia",
                    "type": "date",
                    "label": "Data Início Vigência",
                    "required": True,
                    "help": "Data em que esta tabela começa a valer"
                },
                {
                    "name": "data_fim_vigencia",
                    "type": "date",
                    "label": "Data Fim Vigência (opcional)",
                    "required": False,
                    "help": "Data em que esta tabela deixa de valer. Deixe em branco para vigência indefinida."
                },
                {
                    "name": "faixas",
                    "type": "json_array",
                    "label": "Faixas de Salário Família (JSON)",
                    "required": True,
                    "help": "Lista de faixas no formato [{'valor_renda_minima': 0, 'valor_renda_maxima': 1819.26, 'valor_quota': 62.04}, ...]",
                    "height": 200,
                    "structure": [
                        {"field": "valor_renda_minima", "type": "number", "required": True},
                        {"field": "valor_renda_maxima", "type": "number", "required": True},
                        {"field": "valor_quota", "type": "number", "required": True}
                    ]
                },
                {
                    "name": "observacao",
                    "type": "text",
                    "label": "Observação (opcional)",
                    "required": False
                }
            ],
            "api_endpoint": "/param-legais/salario-familia/",
            "title": "Tabela Salário Família"
        }
    
    # Schema genérico se o tipo não for reconhecido
    return {
        "fields": [
            {
                "name": "data_inicio_vigencia",
                "type": "date",
                "label": "Data Início Vigência",
                "required": True
            },
            {
                "name": "data_fim_vigencia",
                "type": "date",
                "label": "Data Fim Vigência (opcional)",
                "required": False
            },
            {
                "name": "dados_json",
                "type": "json",
                "label": "Dados (JSON)",
                "required": True,
                "height": 300
            },
            {
                "name": "observacao",
                "type": "text",
                "label": "Observação (opcional)",
                "required": False
            }
        ],
        "api_endpoint": "/param-legais/outros/",
        "title": f"Parâmetro {tipo_parametro}"
    }

def extrair_dados_sugestao_para_formulario(dados_sugeridos: Dict[str, Any], tipo_parametro: str) -> Dict[str, Any]:
    """
    Extrai e formata os dados da sugestão da IA para um formato compatível com o formulário de edição.
    """
    # Se os dados_sugeridos for uma string JSON, tenta parsear
    if isinstance(dados_sugeridos, str):
        try:
            dados_sugeridos = json.loads(dados_sugeridos)
        except json.JSONDecodeError:
            return {}
    
    # Se houver dados_extraidos dentro de dados_sugeridos, usa-os
    dados_extraidos = dados_sugeridos.get("dados_extraidos", {})
    if not dados_extraidos:
        dados_extraidos = dados_sugeridos
    
    # Padroniza o tipo de parâmetro para comparação
    tipo_parametro = tipo_parametro.upper()
    
    # Garante valores padrão para campos essenciais
    resultado = {
        "data_inicio_vigencia": dados_extraidos.get("data_inicio_vigencia", 
                                                  dados_sugeridos.get("data_inicio_vigencia", 
                                                                    datetime.now().date().isoformat())),
        "data_fim_vigencia": dados_extraidos.get("data_fim_vigencia", 
                                               dados_sugeridos.get("data_fim_vigencia")),
        "observacao": dados_extraidos.get("observacao", 
                                        dados_sugeridos.get("observacao", 
                                                         f"Criado automaticamente a partir de sugestão da IA em {datetime.now().strftime('%d/%m/%Y %H:%M')}"))
    }
    
    # Dados específicos por tipo de parâmetro
    if tipo_parametro == "INSS":
        resultado.update({
            "faixas": dados_extraidos.get("faixas", []),
            "valor_teto_contribuicao": dados_extraidos.get("valor_teto_contribuicao", 
                                                         dados_extraidos.get("teto_contribuicao", None))
        })
    elif tipo_parametro == "IRRF":
        resultado.update({
            "faixas": dados_extraidos.get("faixas", []),
            "deducao_por_dependente": dados_extraidos.get("deducao_por_dependente", 0),
            "limite_desconto_simplificado": dados_extraidos.get("limite_desconto_simplificado", 
                                                              dados_extraidos.get("limite_deducao_simplificada_mensal", 0))
        })
    elif tipo_parametro == "FGTS":
        resultado.update({
            "aliquota_mensal": dados_extraidos.get("aliquota_mensal", 
                                                 dados_extraidos.get("aliquota_deposito_mensal", 8.0)),
            "aliquota_multa_rescisoria": dados_extraidos.get("aliquota_multa_rescisoria", 
                                                           dados_extraidos.get("aliquota_multa", 40.0))
        })
    elif tipo_parametro == "SALARIO_MINIMO":
        resultado.update({
            "valor_nacional": dados_extraidos.get("valor_nacional", 
                                                dados_extraidos.get("valor", 
                                                                  dados_extraidos.get("salario_minimo", 0))),
            "valores_regionais": dados_extraidos.get("valores_regionais", {})
        })
    elif tipo_parametro == "SALARIO_FAMILIA":
        resultado.update({
            "faixas": dados_extraidos.get("faixas", [])
        })
    
    return resultado

def criar_formulario_edicao(schema: Dict[str, Any], dados_iniciais: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    """
    Cria um formulário dinâmico baseado no schema e nos dados iniciais.
    Retorna os valores preenchidos no formulário.
    """
    valores_formulario = {}
    
    for field in schema.get("fields", []):
        field_name = field["name"]
        field_key = f"{prefix}_{field_name}"
        field_type = field["type"]
        required = field.get("required", False)
        label = field.get("label", field_name)
        help_text = field.get("help", "")
        
        # Obtenha o valor inicial se existir
        valor_inicial = dados_iniciais.get(field_name)
        
        # Renderize o campo apropriado baseado no tipo
        if field_type == "date":
            if valor_inicial and isinstance(valor_inicial, str):
                try:
                    # Tenta converter a string em data
                    valor_inicial = datetime.fromisoformat(valor_inicial.replace('Z', '+00:00')).date()
                except (ValueError, TypeError):
                    valor_inicial = date.today()
            elif valor_inicial and isinstance(valor_inicial, datetime):
                valor_inicial = valor_inicial.date()
            else:
                valor_inicial = date.today()
                
            valores_formulario[field_name] = st.date_input(
                label=label,
                value=valor_inicial,
                key=field_key,
                help=help_text
            )
            
        elif field_type == "number":
            step = field.get("step", 1.0)
            if valor_inicial is None:
                valor_inicial = 0.0
                
            valores_formulario[field_name] = st.number_input(
                label=label,
                value=float(valor_inicial),
                step=step,
                key=field_key,
                help=help_text
            )
            
        elif field_type == "text":
            if valor_inicial is None:
                valor_inicial = ""
                
            valores_formulario[field_name] = st.text_area(
                label=label,
                value=str(valor_inicial),
                key=field_key,
                help=help_text
            )
            
        elif field_type == "json_array" or field_type == "json_object" or field_type == "json":
            height = field.get("height", 200)
            
            # Converte para JSON formatado para melhor visualização
            if not valor_inicial:
                if field_type == "json_array":
                    valor_inicial = []
                elif field_type == "json_object":
                    valor_inicial = {}
                else:
                    valor_inicial = {}
                
            valor_inicial_json = json.dumps(valor_inicial, indent=2, ensure_ascii=False)
            
            valor_json = st.text_area(
                label=label,
                value=valor_inicial_json,
                height=height,
                key=field_key,
                help=help_text
            )
            
            # Tente parsear o JSON inserido
            try:
                valores_formulario[field_name] = json.loads(valor_json)
            except json.JSONDecodeError:
                st.error(f"Formato JSON inválido para o campo {label}")
                valores_formulario[field_name] = None
    
    return valores_formulario

def validar_campos_formulario(schema, valores_formulario):
    """
    Valida campos obrigatórios e tipos básicos do formulário.
    """
    erros = []
    for field in schema.get("fields", []):
        name = field["name"]
        if field.get("required", False):
            if name not in valores_formulario or valores_formulario[name] in (None, ""):
                erros.append(MESSAGES["error_required"].format(field=field.get("label", name)))
        if field["type"] == "number":
            try:
                float(valores_formulario.get(name, 0))
            except Exception:
                erros.append(f"Campo {field.get('label', name)} deve ser numérico.")
        if field["type"] == "date":
            val = valores_formulario.get(name)
            if val and not isinstance(val, date):
                erros.append(f"Campo {field.get('label', name)} deve ser uma data.")
    return erros

def aplicar_parametro_legal(API_BASE_URL: str, dados_formulario: Dict[str, Any], schema: Dict[str, Any], usuario: str) -> Dict[str, Any]:
    """
    Aplica o parâmetro legal no sistema, chamando a API apropriada.
    """
    # Verifica campos obrigatórios
    for field in schema.get("fields", []):
        if field.get("required", False) and (field["name"] not in dados_formulario or dados_formulario[field["name"]] is None):
            return {
                "success": False,
                "message": f"Campo obrigatório não preenchido: {field.get('label', field['name'])}"
            }
    
    # Prepara os dados para o formato esperado pela API
    payload = {}
    for field in schema.get("fields", []):
        field_name = field["name"]
        if field_name in dados_formulario:
            # Converte date para string ISO
            if field["type"] == "date" and dados_formulario[field_name]:
                payload[field_name] = dados_formulario[field_name].isoformat()
            else:
                payload[field_name] = dados_formulario[field_name]
    
    # Adiciona o usuário que está realizando a operação
    payload["usuario_cadastro"] = usuario
    
    # Endpoint da API
    endpoint = f"{API_BASE_URL}{schema.get('api_endpoint', '')}"
    
    try:
        # Faz a requisição POST para criar o novo parâmetro
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        
        return {
            "success": True,
            "message": f"Parâmetro legal aplicado com sucesso: {schema.get('title', 'Parâmetro')}",
            "data": response.json()
        }
    except requests.HTTPError as e:
        error_body = e.response.json() if e.response.content else {}
        detail = error_body.get("detail", e.response.text)
        return {
            "success": False,
            "message": f"Erro ao aplicar parâmetro ({e.response.status_code}): {detail}"
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Erro de conexão: {e}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Erro inesperado: {e}"
        }

def mostrar_pagina_revisao_sugestoes_ia():
    st.header("🔎 Revisão de Sugestões da IA")
    # Verifica se o usuário está logado
    if 'username' not in st.session_state or not st.session_state.username:
        st.warning(MESSAGES["login_required"])
        return
    usuario_atual = st.session_state.username
    API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")
    
    # Estado para armazenar a sugestão selecionada para detalhe/ação
    if 'sugestao_selecionada_id' not in st.session_state:
        st.session_state.sugestao_selecionada_id = None
    if 'justificativa_rejeicao_temp' not in st.session_state:
        st.session_state.justificativa_rejeicao_temp = ""
    if 'modo_edicao_sugestao' not in st.session_state:
        st.session_state.modo_edicao_sugestao = False

    @st.cache_data(ttl=60)
    def fetch_sugestoes_ia(status_filtro: Optional[str] = "pendente"):
        try:
            params = {}
            if status_filtro:
                params["status"] = status_filtro
            
            response = requests.get(f"{API_BASE_URL}/api/v1/parametros/assistente-atualizacao/sugestoes", params=params)
            response.raise_for_status()
            sugestoes_data = response.json()
            
            # Tentar parsear dados_sugeridos_json se for uma string JSON
            for sugestao in sugestoes_data:
                if isinstance(sugestao.get("dados_sugeridos_json"), str):
                    try:
                        sugestao["dados_sugeridos_json"] = json.loads(sugestao["dados_sugeridos_json"])
                    except json.JSONDecodeError:
                        sugestao["dados_sugeridos_json"] = {"erro": "Falha ao parsear JSON de dados sugeridos."}
            return sugestoes_data
        except requests.RequestException as e:
            st.error(f"Erro ao buscar sugestões da IA: {e}")
            return []
        except json.JSONDecodeError:
            st.error("Erro ao decodificar resposta da API de sugestões.")
            return []

    def aprovar_sugestao_api(id_sugestao: str, usuario_aprovador: str):
        try:
            payload = {"usuario_aprovador": usuario_aprovador}
            response = requests.post(f"{API_BASE_URL}/api/v1/parametros/assistente-atualizacao/sugestoes/{id_sugestao}/aprovar", json=payload)
            response.raise_for_status()
            st.success(f"Sugestão {id_sugestao} aprovada com sucesso!")
            st.cache_data.clear() # Limpa o cache para recarregar os dados
            st.session_state.sugestao_selecionada_id = None # Limpa seleção
            st.session_state.modo_edicao_sugestao = False
            return True
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao aprovar sugestão {id_sugestao} ({e.response.status_code}): {detail}")
            return False
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao aprovar sugestão {id_sugestao}: {e}")
            return False

    def rejeitar_sugestao_api(id_sugestao: str, usuario_aprovador: str, justificativa: str):
        try:
            payload = {"usuario_aprovador": usuario_aprovador, "justificativa_rejeicao": justificativa}
            response = requests.post(f"{API_BASE_URL}/api/v1/parametros/assistente-atualizacao/sugestoes/{id_sugestao}/rejeitar", json=payload)
            response.raise_for_status()
            st.success(f"Sugestão {id_sugestao} rejeitada com sucesso!")
            st.cache_data.clear() # Limpa o cache para recarregar os dados
            st.session_state.sugestao_selecionada_id = None # Limpa seleção
            st.session_state.justificativa_rejeicao_temp = "" # Limpa justificativa
            st.session_state.modo_edicao_sugestao = False
            return True
        except requests.HTTPError as e:
            error_body = e.response.json() if e.response.content else {}
            detail = error_body.get("detail", e.response.text)
            st.error(f"Erro ao rejeitar sugestão {id_sugestao} ({e.response.status_code}): {detail}")
            return False
        except requests.RequestException as e:
            st.error(f"Erro de conexão ao rejeitar sugestão {id_sugestao}: {e}")
            return False

    # SIDEBAR - FILTROS
    st.sidebar.subheader("Filtros de Revisão")
    status_filtro = st.sidebar.selectbox("Status da Sugestão", ["pendente", "aprovada", "rejeitada"], index=0, key="revisao_status_filtro")

    # LISTA DE SUGESTÕES
    sugestoes = fetch_sugestoes_ia(status_filtro)
    if not sugestoes:
        st.info(MESSAGES["no_suggestions"].format(status=status_filtro))
        return

    st.markdown(f"**Exibindo {len(sugestoes)} sugestões com status: {status_filtro}**")
    st.markdown("---")

    for idx, sugestao_item in enumerate(sugestoes):
        sugestao_id = sugestao_item.get("id_sugestao")
        col_info, col_acao = st.columns([3, 1])
        with col_info:
            st.markdown(f"##### Sugestão ID: `{sugestao_id}`")
            st.markdown(f"**Tipo de Parâmetro:** {sugestao_item.get('tipo_parametro', 'N/A')}")
            data_sugestao_str = sugestao_item.get('data_sugestao')
            if data_sugestao_str:
                try:
                    data_sugestao_dt = datetime.fromisoformat(data_sugestao_str.replace("Z", "+00:00")) if isinstance(data_sugestao_str, str) else data_sugestao_str
                    st.markdown(f"**Data da Sugestão:** {data_sugestao_dt.strftime('%d/%m/%Y %H:%M:%S') if data_sugestao_dt else 'N/A'}")
                except Exception:
                    st.markdown(f"**Data da Sugestão:** {data_sugestao_str} (formato inválido)")
            else:
                st.markdown(f"**Data da Sugestão:** N/A")
            st.markdown(f"**Solicitante:** {sugestao_item.get('usuario_solicitante', 'N/A')}")
            st.markdown(f"**Fonte:** {sugestao_item.get('nome_documento_fonte', 'N/A')}")
            with st.expander("Ver Resumo e Dados Sugeridos pela IA"):
                st.markdown("**Resumo da IA:**")
                st.caption(sugestao_item.get('resumo_ia_sugestao', 'Nenhum resumo disponível.'))
                st.markdown("**Dados Sugeridos (JSON):**")
                dados_sugeridos = sugestao_item.get("dados_sugeridos_json", {})
                if isinstance(dados_sugeridos, str):
                    try:
                        dados_sugeridos = json.loads(dados_sugeridos)
                    except json.JSONDecodeError:
                        dados_sugeridos = {"erro": "Falha ao parsear JSON de dados sugeridos."}
                st.json(dados_sugeridos)
                # Validação (se houver)
                validacao = dados_sugeridos.get("validacao", {})
                if isinstance(validacao, dict):
                    if validacao.get("erros"):
                        st.error(f"Erros de validação da IA: {', '.join(validacao.get('erros', []))}")
                    if validacao.get("avisos"):
                        st.warning(f"Avisos de validação da IA: {', '.join(validacao.get('avisos', []))}")
            if sugestao_item.get("status_sugestao") == "rejeitada" and sugestao_item.get("justificativa_rejeicao"):
                st.info(f"**Justificativa da Rejeição:** {sugestao_item.get('justificativa_rejeicao')}")
            if sugestao_item.get("status_sugestao") in ["aprovada", "rejeitada"] and sugestao_item.get("usuario_aprovador"):
                 data_aprovacao_str = sugestao_item.get('data_aprovacao')
                 data_aprovacao_fmt = ""
                 if data_aprovacao_str:
                    try:
                        data_aprovacao_dt = datetime.fromisoformat(data_aprovacao_str.replace("Z", "+00:00")) if isinstance(data_aprovacao_str, str) else data_aprovacao_str
                        data_aprovacao_fmt = f" em {data_aprovacao_dt.strftime('%d/%m/%Y %H:%M')}" if data_aprovacao_dt else ""
                    except Exception:
                        data_aprovacao_fmt = f" em {data_aprovacao_str} (formato inválido)"

                 status_map = {"aprovada": "Aprovada", "rejeitada": "Rejeitada"}
                 st.markdown(f"**Status:** {status_map.get(sugestao_item.get('status_sugestao'))} por **{sugestao_item.get('usuario_aprovador')}**{data_aprovacao_fmt}")

        with col_acao:
            if sugestao_item.get("status_sugestao") == "pendente":
                if st.button("🔍 Revisar/Aprovar", key=f"revisar_{sugestao_id}_{idx}"):
                    st.session_state.sugestao_selecionada_id = sugestao_id
                    st.session_state.justificativa_rejeicao_temp = "" # Limpa ao selecionar nova
                    st.session_state.modo_edicao_sugestao = False
                    st.rerun() # Força o rerender para mostrar o modal/form de ação
            else:
                st.markdown(f"Status: **{sugestao_item.get('status_sugestao').capitalize()}**")
        
        st.markdown("---")

    # MODO DE EDIÇÃO/APROVAÇÃO - Formulário para sugestão selecionada
    if st.session_state.sugestao_selecionada_id:
        sugestao_para_acao = next((s for s in sugestoes if s.get("id_sugestao") == st.session_state.sugestao_selecionada_id), None)
        if sugestao_para_acao:
            tipo_parametro = sugestao_para_acao.get('tipo_parametro', '').upper()
            dados_sugeridos = sugestao_para_acao.get("dados_sugeridos_json", {})
            if isinstance(dados_sugeridos, str):
                try:
                    dados_sugeridos = json.loads(dados_sugeridos)
                except json.JSONDecodeError:
                    dados_sugeridos = {"erro": "Falha ao parsear JSON."}
            # ...existing code...
            if st.session_state.modo_edicao_sugestao:
                st.sidebar.markdown("### Edição de Parâmetros")
                schema = get_schema_por_tipo_parametro(tipo_parametro)
                dados_iniciais = extrair_dados_sugestao_para_formulario(dados_sugeridos, tipo_parametro)
                with st.sidebar.form(key=f"form_edicao_{sugestao_para_acao.get('id_sugestao')}"):
                    st.markdown(f"### Edição de {schema.get('title', 'Parâmetro')}")
                    valores_formulario = criar_formulario_edicao(
                        schema=schema,
                        dados_iniciais=dados_iniciais,
                        prefix=f"edit_{sugestao_para_acao.get('id_sugestao')}"
                    )
                    submitted = st.form_submit_button("✅ Aplicar e Aprovar")
                    if submitted:
                        erros = validar_campos_formulario(schema, valores_formulario)
                        if erros:
                            for erro in erros:
                                st.error(erro)
                        else:
                            with st.spinner(f"Aplicando parâmetros de {schema.get('title', 'Parâmetro')}..."):
                                resultado = aplicar_parametro_legal(
                                    API_BASE_URL=API_BASE_URL,
                                    dados_formulario=valores_formulario,
                                    schema=schema,
                                    usuario=usuario_atual
                                )
                                if resultado["success"]:
                                    st.success(resultado["message"])
                                    if aprovar_sugestao_api(sugestao_para_acao.get('id_sugestao'), usuario_atual):
                                        st.rerun()
                                else:
                                    st.error(resultado["message"])
            else:
                st.sidebar.markdown("### Dados Sugeridos")
                if "dados_extraidos" in dados_sugeridos and dados_sugeridos["dados_extraidos"]:
                    st.sidebar.json(dados_sugeridos["dados_extraidos"])
                else:
                    st.sidebar.json(dados_sugeridos)
                col_aprovar, col_rejeitar = st.sidebar.columns(2)
                with col_aprovar:
                    if st.button("✅ Aprovar Direto", key=f"aprovar_direct_{sugestao_para_acao.get('id_sugestao')}"):
                        confirma = st.sidebar.checkbox("Confirmar aprovação sem edição?", key=f"confirma_aprovacao_{sugestao_para_acao.get('id_sugestao')}")
                        if confirma:
                            schema = get_schema_por_tipo_parametro(tipo_parametro)
                            dados_iniciais = extrair_dados_sugestao_para_formulario(dados_sugeridos, tipo_parametro)
                            with st.spinner(f"Aplicando parâmetros de {schema.get('title', 'Parâmetro')}..."):
                                resultado = aplicar_parametro_legal(
                                    API_BASE_URL=API_BASE_URL,
                                    dados_formulario=dados_iniciais,
                                    schema=schema,
                                    usuario=usuario_atual
                                )
                                if resultado["success"]:
                                    st.success(resultado["message"])
                                    if aprovar_sugestao_api(sugestao_para_acao.get('id_sugestao'), usuario_atual):
                                        st.rerun()
                                else:
                                    st.error(resultado["message"])
                
            # Campo de justificativa para rejeição (sempre visível)
            st.sidebar.markdown("### Rejeição")
            st.session_state.justificativa_rejeicao_temp = st.sidebar.text_area(
                "Justificativa para Rejeição:", 
                value=st.session_state.justificativa_rejeicao_temp, 
                key=f"just_rej_{sugestao_para_acao.get('id_sugestao')}"
            )

            if st.sidebar.button("❌ Rejeitar Sugestão", key=f"rejeitar_final_{sugestao_para_acao.get('id_sugestao')}"):
                if not st.session_state.justificativa_rejeicao_temp:
                    st.sidebar.error("A justificativa é obrigatória para rejeitar.")
                else:
                    if rejeitar_sugestao_api(sugestao_para_acao.get('id_sugestao'), usuario_atual, st.session_state.justificativa_rejeicao_temp):
                        st.rerun()
            
            if st.sidebar.button("Cancelar Ação", key=f"cancelar_acao_{sugestao_para_acao.get('id_sugestao')}"):
                st.session_state.sugestao_selecionada_id = None
                st.session_state.justificativa_rejeicao_temp = ""
                st.session_state.modo_edicao_sugestao = False
                st.rerun()
