import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from fastapi import Request, HTTPException
import logging
from google.cloud import bigquery
from ..schemas import ControleMensalEmpresaSchema
from ..bq_loader import ControleFolhaLoader
from ..config_manager import config_manager
from ..vertex_utils import prever_rubrica_com_vertex
from ..gemini_utils import gerar_descricao_da_clausula_com_gemini

CSV_COLUMN_MAPPING_INTERNAL_NAMES = {
    'CNPJ': 'cnpj_csv',
    'NOME EMPRESA': 'nome_empresa_csv',
    'DADOS FOLHA': 'status_dados_pasta_csv',
    'Envio Cliente': 'documentos_enviados_cliente_csv',
    'Data de Envio da Folha': 'data_envio_documentos_cliente_csv',
    'Guia FGTS': 'guia_fgts_gerada_csv',
    'Data Guia FGTS': 'data_geracao_guia_fgts_csv',
    'DARF INSS': 'darf_inss_gerado_csv',
    'Data DARF INSS': 'data_geracao_darf_inss_csv',
    'eSocial/DCTFWeb': 'esocial_dctfweb_enviado_csv',
    'Data eSocial/DCTFWeb': 'data_envio_esocial_dctfweb_csv',
    'MOVIMENTAÇÃO': 'tipo_movimentacao_csv',
    'PARTICULARIDADES': 'particularidades_observacoes_csv',
    'Forma de Envio': 'forma_envio_preferencial_csv',
    'E-mail do Cliente': 'email_contato_folha_csv',
    'Sindicato': 'sindicato_nome_csv'
}
CSV_EMPRESA_ID_COLUMN = 'CNPJ'

logger = logging.getLogger(__name__)

def _text_to_bool(text: Any, true_values: List[str] = ['sim', 's', 'ok', 'gerada', 'enviada', 'transmitido']) -> Optional[bool]:
    if pd.isna(text) or str(text).strip() == '':
        return None
    return str(text).strip().lower() in true_values

def _text_to_date(text: Any) -> Optional[date]:
    if pd.isna(text) or str(text).strip() == '':
        return None
    try:
        dt_obj = pd.to_datetime(text, errors='coerce')
        return dt_obj.date() if pd.notna(dt_obj) else None
    except Exception:
        return None

def _safe_index_to_int(idx):
    try:
        return int(str(idx))
    except Exception:
        return 0

def buscar_sindicato_id_por_nome(loader, nome_sindicato: str) -> Optional[str]:
    if not nome_sindicato or not loader or not loader.client:
        return None
    table_id = f"{loader.project_id}.{loader.dataset_id}.sindicatos"
    query = f"SELECT id FROM `{table_id}` WHERE LOWER(nome) = @nome AND client_id = @client_id LIMIT 1"
    params = [
        bigquery.ScalarQueryParameter("nome", "STRING", nome_sindicato.strip().lower()),
        bigquery.ScalarQueryParameter("client_id", "STRING", loader.client_id)
    ]
    try:
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        df = loader.client.query(query, job_config=job_config).to_dataframe()
        if not df.empty:
            return str(df.iloc[0]["id"])
    except Exception as e:
        print(f"Erro ao buscar sindicato_id para '{nome_sindicato}': {e}")
    return None

async def processar_e_salvar_csv_controle_folha(
    dataframe: pd.DataFrame, ano_referencia: int, mes_referencia: int, request: Optional[Request] = None
) -> Dict[str, Any]:
    registros_para_bq: List[Dict[str, Any]] = []
    erros_processamento: List[str] = []
    total_linhas = len(dataframe)

    # Carrega config e instancia loader
    if request is None:
        # Este log deve ser mais específico para indicar que o request é None
        logger.error("processar_e_salvar_csv_controle_folha chamado sem um objeto Request.")
        erros_processamento.append("Erro crítico: O objeto Request é necessário para carregar a configuração e não foi fornecido.")
        return {
            "message": "Processamento do CSV falhou: Objeto Request ausente.",
            "erros_processamento": erros_processamento,
            "total_linhas_csv": total_linhas,
            "linhas_importadas_com_sucesso": 0
        }
    
    try:
        # get_config agora levanta ValueError se request for None, ou HTTPException se client_id não for encontrado.
        config = config_manager.get_config(request) 
    except ValueError as ve:
        logger.error(f"Falha ao obter configuração em processar_e_salvar_csv_controle_folha devido a ValueError (request pode ser None internamente ou outro problema): {ve}", exc_info=True)
        erros_processamento.append(f"Erro crítico ao obter configuração: {ve}")
        return {
            "message": f"Processamento do CSV falhou: {ve}",
            "erros_processamento": erros_processamento,
            "total_linhas_csv": total_linhas,
            "linhas_importadas_com_sucesso": 0
        }
    except HTTPException as he:
        logger.error(f"Falha ao obter configuração em processar_e_salvar_csv_controle_folha devido a HTTPException (problema com client_id): {he.detail}", exc_info=True)
        erros_processamento.append(f"Erro crítico ao obter configuração: {he.detail}")
        return {
            "message": f"Processamento do CSV falhou: {he.detail}",
            "erros_processamento": erros_processamento,
            "total_linhas_csv": total_linhas,
            "linhas_importadas_com_sucesso": 0
        }
    # Removida a verificação de config is None, pois get_config agora levanta exceção.

    loader = ControleFolhaLoader(config)
    empresas_df = loader.listar_todas_as_empresas()
    cnpj_to_empresa_id = {}
    if not empresas_df.empty:
        for _, row in empresas_df.iterrows():
            cnpj = str(row.get("cnpj", "")).replace(".", "").replace("/", "").replace("-", "")
            cnpj_to_empresa_id[cnpj] = row.get("id") or row.get("codigo_empresa") or row.get("id_empresa")

    for index, csv_row in dataframe.iterrows():
        idx_int = _safe_index_to_int(index)
        try:
            identificador_empresa_csv = csv_row.get(CSV_EMPRESA_ID_COLUMN)
            if pd.isna(identificador_empresa_csv) or str(identificador_empresa_csv).strip() == '':
                erros_processamento.append(f"Linha {idx_int + 9}: Identificador da empresa (CNPJ) ausente ou vazio.")
                continue
            cnpj_limpo = str(identificador_empresa_csv).replace(".", "").replace("/", "").replace("-", "")
            empresa_id_sistema = cnpj_to_empresa_id.get(cnpj_limpo)
            if not empresa_id_sistema:
                erros_processamento.append(f"Linha {idx_int + 9}: Empresa com CNPJ {identificador_empresa_csv} não encontrada no sistema.")
                continue
            sindicato_nome_csv = csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Sindicato'))
            sindicato_id_sistema = buscar_sindicato_id_por_nome(loader, sindicato_nome_csv) if sindicato_nome_csv else None
            dados_convertidos = {
                "empresa_id": empresa_id_sistema,
                "ano_referencia": ano_referencia,
                "mes_referencia": mes_referencia,
                "status_dados_pasta": str(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('DADOS FOLHA',''))).strip() if pd.notna(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('DADOS FOLHA'))) else None,
                "documentos_enviados_cliente": _text_to_bool(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Envio Cliente'))),
                "data_envio_documentos_cliente": _text_to_date(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Data de Envio da Folha'))),
                "guia_fgts_gerada": _text_to_bool(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Guia FGTS'))),
                "data_geracao_guia_fgts": _text_to_date(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Data Guia FGTS'))),
                "darf_inss_gerado": _text_to_bool(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('DARF INSS'))),
                "data_geracao_darf_inss": _text_to_date(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Data DARF INSS'))),
                "esocial_dctfweb_enviado": _text_to_bool(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('eSocial/DCTFWeb'))),
                "data_envio_esocial_dctfweb": _text_to_date(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Data eSocial/DCTFWeb'))),
                "tipo_movimentacao": str(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('MOVIMENTAÇÃO',''))).strip() if pd.notna(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('MOVIMENTAÇÃO'))) else None,
                "particularidades_observacoes": str(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('PARTICULARIDADES',''))).strip() if pd.notna(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('PARTICULARIDADES'))) else None,
                "forma_envio_preferencial": str(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Forma de Envio',''))).strip() if pd.notna(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Forma de Envio'))) else None,
                "email_contato_folha": str(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('E-mail do Cliente',''))).strip() if pd.notna(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('E-mail do Cliente'))) else None,
                "nome_contato_cliente_folha": str(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Contato / Responsável',''))).strip() if pd.notna(csv_row.get(CSV_COLUMN_MAPPING_INTERNAL_NAMES.get('Contato / Responsável'))) else None,
                "sindicato_id_aplicavel": sindicato_id_sistema,
                "data_ultima_modificacao": datetime.now(),
            }
            ControleMensalEmpresaSchema(**dados_convertidos)
            registros_para_bq.append(dados_convertidos)
        except Exception as e:
            erros_processamento.append(f"Linha {idx_int + 9}: Erro inesperado ao processar - {str(e)}")
            continue
    num_registros_validos = len(registros_para_bq)
    linhas_efetivamente_inseridas = 0
    if num_registros_validos > 0:
        for reg in registros_para_bq:
            try:
                loader.inserir_folha(
                    id_folha=f"{reg['empresa_id']}_{reg['ano_referencia']}{str(reg['mes_referencia']).zfill(2)}",
                    codigo_empresa=int(reg['empresa_id']),
                    cnpj_empresa="",  # Adapte se necessário
                    mes_ano=f"{reg['ano_referencia']}-{str(reg['mes_referencia']).zfill(2)}-01",
                    status=reg.get('status_dados_pasta') or "Pendente",
                    data_envio_cliente=reg.get('data_envio_documentos_cliente'),
                    data_guia_fgts=reg.get('data_geracao_guia_fgts'),
                    observacoes=reg.get('particularidades_observacoes')
                )
                linhas_efetivamente_inseridas += 1
            except Exception as e:
                empresa_id_para_erro = reg.get('empresa_id', 'Desconhecida')
                mes_ref_para_erro = reg.get('mes_referencia', 'N/A')
                ano_ref_para_erro = reg.get('ano_referencia', 'N/A')
                erros_processamento.append(
                    f"Erro ao inserir registro para empresa {empresa_id_para_erro} "
                    f"(Ref: {mes_ref_para_erro}/{ano_ref_para_erro}): {e}"
                )
    
    status_message = "Processamento do CSV concluído."
    if erros_processamento:
        status_message += f" Foram encontrados {len(erros_processamento)} erro(s)."
    
    return {
        "message": status_message,
        "erros_processamento": erros_processamento,
        "total_linhas_csv": total_linhas,
        "linhas_importadas_com_sucesso": linhas_efetivamente_inseridas
    }

async def buscar_controles_mensais(filtros: Dict[str, Any], request: Optional[Request] = None) -> List[ControleMensalEmpresaSchema]:
    if request is None:
        logger.error("buscar_controles_mensais chamado sem um objeto Request.")
        # Considerar levantar uma exceção aqui ou retornar uma lista vazia com log de erro.
        # Por enquanto, mantendo o comportamento de levantar ValueError para ser consistente com a ausência de config.
        raise ValueError("Request não pode ser None para buscar_controles_mensais, pois é necessário para a configuração.")

    try:
        config = config_manager.get_config(request)
    except ValueError as ve:
        logger.error(f"Falha ao obter configuração em buscar_controles_mensais devido a ValueError: {ve}", exc_info=True)
        raise # Relança para ser tratado pelo chamador ou FastAPI
    except HTTPException as he:
        logger.error(f"Falha ao obter configuração em buscar_controles_mensais devido a HTTPException: {he.detail}", exc_info=True)
        raise # Relança para ser tratado pelo chamador ou FastAPI
    # Removida a verificação de config is None

    loader = ControleFolhaLoader(config)
    table_id = f"{loader.project_id}.{loader.dataset_id}.folhas"
    query = f"SELECT * FROM `{table_id}` WHERE client_id = @client_id"
    params = [bigquery.ScalarQueryParameter("client_id", "STRING", loader.client_id)]
    if filtros.get("ano_referencia"):
        query += " AND EXTRACT(YEAR FROM mes_ano) = @ano"
        params.append(bigquery.ScalarQueryParameter("ano", "INT64", filtros["ano_referencia"]))
    if filtros.get("mes_referencia"):
        query += " AND EXTRACT(MONTH FROM mes_ano) = @mes"
        params.append(bigquery.ScalarQueryParameter("mes", "INT64", filtros["mes_referencia"]))
    if filtros.get("empresa_id"):
        query += " AND codigo_empresa = @empresa_id"
        params.append(bigquery.ScalarQueryParameter("empresa_id", "INT64", int(filtros["empresa_id"])))
    query += " ORDER BY codigo_empresa, mes_ano"
    try:
        if not loader.client:
            raise Exception("Cliente BigQuery não inicializado.")
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        df = loader.client.query(query, job_config=job_config).to_dataframe()
        return [ControleMensalEmpresaSchema(**row) for row in df.to_dict(orient="records")]
    except Exception as e:
        print(f"Erro ao buscar controles mensais no BigQuery: {e}")
        return []

def analisar_clausula_completa(texto_da_clausula: str) -> dict:
    resultado_analise = {
        "clausula": texto_da_clausula,
        "rubrica_vertex_ai": None,
        "descricao_gemini": None,
        "erros": []
    }
    # 1. Classificar com Vertex AI
    try:
        rubrica_vertex = prever_rubrica_com_vertex(texto_da_clausula)
        if "Erro" in rubrica_vertex:
            resultado_analise["erros"].append(f"Vertex AI: {rubrica_vertex}")
        else:
            resultado_analise["rubrica_vertex_ai"] = rubrica_vertex
    except Exception as e:
        resultado_analise["erros"].append(f"Exceção ao chamar Vertex AI: {str(e)}")
    # 2. Gerar descrição com Gemini
    try:
        rubrica_para_gemini = resultado_analise["rubrica_vertex_ai"] if resultado_analise["rubrica_vertex_ai"] and "Erro" not in resultado_analise["rubrica_vertex_ai"] else None
        info_gemini = gerar_descricao_da_clausula_com_gemini(
            texto_clausula=texto_da_clausula,
            rubrica_identificada=rubrica_para_gemini
        )
        if "erro" in info_gemini:
            resultado_analise["erros"].append(f"Gemini: {info_gemini['erro']}")
        elif "descricao" in info_gemini:
            resultado_analise["descricao_gemini"] = info_gemini["descricao"]
            if "rubrica" in info_gemini and not rubrica_para_gemini:
                resultado_analise["rubrica_gemini_sugerida"] = info_gemini["rubrica"]
        else:
            resultado_analise["erros"].append("Gemini: Descrição não retornada ou formato inesperado.")
    except Exception as e:
        resultado_analise["erros"].append(f"Exceção ao chamar Gemini: {str(e)}")
    return resultado_analise
