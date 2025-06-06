# filepath: c:\\Users\\55479\\Documents\\AUDITORIA360\\src\\bq_loader.py
import json
import logging
import os
import uuid # Adicionado para gerar UUIDs para empresa_id
from datetime import datetime, timezone, date # Adicionado date
from google.cloud import bigquery
from google.oauth2 import service_account
from typing import Optional, List, Dict, Any
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryError
import unittest.mock # Adicionado para o bloco __main__

# Configuração de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

# --- Schema da Tabela BigQuery ---
TABLE_SCHEMA = [
    bigquery.SchemaField("id_extracao", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("id_item", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("nome_arquivo_origem", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("pagina", "INTEGER", mode="NULLABLE"),
    bigquery.SchemaField("tipo_campo", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("texto_extraido", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("valor_limpo", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("valor_numerico", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("confianca", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("timestamp_carga", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),  # Isolamento multi-cliente obrigatório
]

EMPRESAS_TABLE_SCHEMA = [
    bigquery.SchemaField("empresa_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("nome_empresa", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("cnpj_empresa", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("data_cadastro", "TIMESTAMP", mode="NULLABLE"),
    bigquery.SchemaField("data_ultima_modificacao", "TIMESTAMP", mode="NULLABLE"),
]

FOLHAS_TABLE_SCHEMA = [
    bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("id_folha", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("codigo_empresa", "STRING", mode="REQUIRED"), # empresa_id
    bigquery.SchemaField("mes_ano", "STRING", mode="NULLABLE"), # YYYY-MM
    bigquery.SchemaField("tipo_folha", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("status", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("data_cadastro", "TIMESTAMP", mode="NULLABLE"), # Data do upload/criação
    bigquery.SchemaField("nome_arquivo_original", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("data_ultima_modificacao", "TIMESTAMP", mode="NULLABLE"),
]

# Schema para a tabela de resultados do cálculo do sistema (Motor de Cálculo da Folha AUDITORIA360)
RESULTADOS_CALCULO_SISTEMA_FOLHA_SCHEMA = [
    bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("id_resultado_calculo", "STRING", mode="REQUIRED"), # UUID
    bigquery.SchemaField("id_folha", "STRING", mode="REQUIRED"), # FK para folhas.id_folha
    bigquery.SchemaField("id_funcionario", "STRING", mode="REQUIRED"), # Identificador do funcionário
    bigquery.SchemaField("competencia", "STRING", mode="REQUIRED"), # Formato "YYYY-MM"
    bigquery.SchemaField("rubrica_codigo_sistema", "STRING", mode="REQUIRED"), # Código interno da rubrica calculada
    bigquery.SchemaField("rubrica_descricao_sistema", "STRING", mode="NULLABLE"), # Descrição da rubrica
    bigquery.SchemaField("base_calculo_inss_sistema", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("aliquota_inss_sistema", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("valor_inss_calculado_sistema", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("base_calculo_irrf_sistema", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("aliquota_irrf_sistema", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("parcela_deduzir_irrf_sistema", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("valor_irrf_calculado_sistema", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("base_calculo_fgts_sistema", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("valor_fgts_calculado_sistema", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("salario_familia_calculado_sistema", "FLOAT", mode="NULLABLE"),
    bigquery.SchemaField("outros_valores_dependentes_calculados_sistema", "STRING", mode="NULLABLE"), # JSON: {"dsr": 150.00, "periculosidade": 300.00}
    bigquery.SchemaField("data_calculo", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("versao_motor_calculo", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("parametros_calculo_utilizados", "STRING", mode="NULLABLE"), # JSON: versões de tabelas legais, etc.
]

# Schema para a tabela de resultados do cálculo do sistema (Motor de Cálculo da Folha AUDITORIA360) - VERSÃO DETALHADA ALINHADA COM O MOTOR
# Esta é a versão que será usada para a nova tabela.
RESULTADOS_CALCULO_SISTEMA_FOLHA_SCHEMA_DETALHADO = [
    bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("id_resultado_calculo", "STRING", mode="REQUIRED"), # UUID para este registro de resultado
    bigquery.SchemaField("id_folha_processada_fk", "STRING", mode="REQUIRED"), # FK para folhas.id_folha
    bigquery.SchemaField("id_funcionario", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("competencia_folha", "STRING", mode="REQUIRED"), # YYYY-MM
    bigquery.SchemaField("base_calculo_inss_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("valor_inss_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("aliquota_efetiva_inss_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("base_calculo_irrf_bruta_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("base_calculo_irrf_liquida_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("valor_irrf_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("base_calculo_fgts_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("valor_fgts_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("salario_familia_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("valor_periculosidade_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("valor_insalubridade_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("valor_adicional_noturno_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("valor_dsr_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("outras_verbas_calculadas_motor", "STRING", mode="NULLABLE"), # JSON String
    bigquery.SchemaField("total_vencimentos_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("total_descontos_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("total_liquido_calculado_sistema", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("logs_calculo", "STRING", mode="NULLABLE"), # JSON Array String
    bigquery.SchemaField("data_calculo", "TIMESTAMP", mode="REQUIRED"),
    # Adicionar campos que estavam na versão anterior do schema se ainda relevantes
    # bigquery.SchemaField("versao_motor_calculo", "STRING", mode="NULLABLE"),
    # bigquery.SchemaField("parametros_calculo_utilizados", "STRING", mode="NULLABLE"), 
]

# Remover a definição duplicada de RESULTADOS_CALCULO_SISTEMA_FOLHA_SCHEMA (linhas 120-133 do contexto original)
# A definição acima (RESULTADOS_CALCULO_SISTEMA_FOLHA_SCHEMA_DETALHADO) será a usada.

# ATENÇÃO: Todas as queries e cargas DEVEM usar o filtro client_id para garantir isolamento de dados entre clientes (white-label/multi-tenant).

def get_bigquery_client(config_dict: dict) -> bigquery.Client:
    """Cria e retorna um cliente BigQuery usando a configuração fornecida."""
    if not config_dict:
        raise ValueError("O argumento 'config_dict' é obrigatório para get_bigquery_client.")
    
    key_path = config_dict.get("service_account_key_path_local_dev")
    project_id = config_dict.get("gcp_project_id")

    if not project_id:
        logger.error("gcp_project_id não encontrado na configuração para get_bigquery_client.")
        raise ValueError("gcp_project_id é necessário na configuração.")

    try:
        if key_path:
            logger.info(f"Criando cliente BigQuery com chave de serviço: {key_path} para o projeto {project_id}")
            credentials = service_account.Credentials.from_service_account_file(
                key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            client = bigquery.Client(project=project_id, credentials=credentials)
        else:
            logger.info(f"Criando cliente BigQuery com credenciais padrão do ambiente para o projeto {project_id}")
            client = bigquery.Client(project=project_id)
        
        logger.info(f"Cliente BigQuery para o projeto '{project_id}' criado com sucesso.")
        return client
    except Exception as e:
        logger.error(f"Falha ao criar cliente BigQuery para o projeto '{project_id}': {e}", exc_info=True)
        raise

def create_dataset_if_not_exists(client: bigquery.Client, dataset_id: str, location: str):
    """Cria o dataset no BigQuery se ele não existir."""
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
        logger.info(f"Dataset '{dataset_id}' já existe.")
    except Exception:
        logger.info(f"Dataset '{dataset_id}' não encontrado. Criando...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location
        client.create_dataset(dataset, timeout=30)
        logger.info(f"Dataset '{dataset_id}' criado em '{location}'.")

def create_or_update_table(client: bigquery.Client, dataset_id: str, table_id: str, schema: list):
    """Cria ou atualiza a tabela no BigQuery com o schema especificado."""
    table_ref = client.dataset(dataset_id).table(table_id)
    try:
        client.get_table(table_ref)
        logger.info(f"Tabela '{dataset_id}.{table_id}' já existe.")
    except Exception:
        logger.info(f"Tabela '{dataset_id}.{table_id}' não encontrada. Criando...")
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        logging.info(f"Tabela '{dataset_id}.{table_id}' criada.") # Mantido o logging.info aqui, conforme original

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception), 
    reraise=True
)
def load_data_to_bigquery(client: bigquery.Client, data: list[dict], config: dict) -> int:
    """
    Carrega uma lista de dicionários (registros) para a tabela BigQuery especificada na configuração.
    Aplica retry em caso de falhas.

    Args:
        client: Instância do cliente BigQuery.
        data: Lista de dicionários, onde cada dicionário representa uma linha.
        config: Dicionário de configuração obrigatório.
    Returns:
        Número de linhas carregadas.
    """
    if not data:
        logger.warning("Nenhum dado fornecido para carregar no BigQuery.")
        return 0

    if not config:
        logger.error("Configuração não fornecida para load_data_to_bigquery.")
        raise ValueError("O argumento 'config' é obrigatório.")

    client_id_from_config = config.get("client_id")
    if not client_id_from_config:
        logger.error("O campo 'client_id' é obrigatório na configuração para isolamento multi-cliente.")
        raise ValueError("O campo 'client_id' é obrigatório na configuração.")

    try:
        project_id = config["gcp_project_id"]
        dataset_id = config["bq_dataset_id"]
        table_id = config["bq_table_id"]
        location = config["gcp_location"]
    except KeyError as e:
        logger.error(f"Chave de configuração ausente para BigQuery em 'config': {e}")
        raise ValueError(f"Configuração do BigQuery (passada) incompleta: falta {e}")

    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    try:
        create_dataset_if_not_exists(client, dataset_id, location)
        create_or_update_table(client, dataset_id, table_id, TABLE_SCHEMA)

        timestamp_agora_iso = datetime.now(timezone.utc).isoformat()
        for row in data:
            row['timestamp_carga'] = timestamp_agora_iso
            row['client_id'] = client_id_from_config

        job_config = bigquery.LoadJobConfig(
            schema=TABLE_SCHEMA,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        logger.info(f"[{client_id_from_config}] Iniciando carregamento de {len(data)} registros para '{full_table_id}'...")
        load_job = client.load_table_from_json(
            data, 
            full_table_id,
            job_config=job_config
        )
        load_job.result() 

        if load_job.errors:
            logger.error(f"[{client_id_from_config}] Erro ao carregar dados para '{full_table_id}': {load_job.errors}")
            raise RuntimeError(f"Erro no job de carregamento do BigQuery: {load_job.errors}")
        else:
            output_rows = load_job.output_rows if load_job.output_rows is not None else 0
            logger.info(f"[{client_id_from_config}] Carregamento concluído. {output_rows} linhas carregadas para '{full_table_id}'.")
            return output_rows
    except RetryError as re:
        logger.error(f"[{client_id_from_config}] Todas as tentativas de carregamento para BigQuery '{full_table_id}' falharam após retries: {re}")
        raise 
    except Exception as e:
        logger.error(f"[{client_id_from_config}] Erro durante o processo de carregamento para BigQuery '{full_table_id}': {e}", exc_info=True)
        raise

class ControleFolhaLoader:
    def __init__(self, config: dict): # Modificado: Apenas config
        if not config:
            raise ValueError("O dicionário de configuração é obrigatório.")
        
        self.config = config
        self.client_id = config.get("client_id")
        if not self.client_id:
            raise ValueError("client_id não encontrado na configuração fornecida para ControleFolhaLoader.")

        # Obter cliente BigQuery
        try:
            self.client = get_bigquery_client(config)
        except Exception as e_get_client:
            logger.error(f"[{self.client_id}] Falha ao obter cliente BigQuery no ControleFolhaLoader: {e_get_client}", exc_info=True)
            raise ValueError(f"Não foi possível inicializar o cliente BigQuery: {e_get_client}") from e_get_client

        self.project_id = config.get("gcp_project_id")
        # Garantir que dataset_id seja uma string e não None.
        _dataset_id_from_config = config.get("control_bq_dataset_id", config.get("bq_dataset_id"))
        if not isinstance(_dataset_id_from_config, str) or not _dataset_id_from_config:
            raise ValueError("Nem 'control_bq_dataset_id' nem 'bq_dataset_id' (como fallback) foram encontrados ou são válidos (string não vazia) na configuração para ControleFolhaLoader.")
        self.dataset_id: str = _dataset_id_from_config

        self.folhas_table_id = config.get("control_folhas_table_id", "folhas")
        self.empresas_table_id = config.get("control_empresas_table_id", "empresas")
        self.raw_data_table_id = config.get("control_raw_data_table_id", "controle_folha_raw_data")
        self.resultados_calculo_table_id = config.get("control_resultados_calculo_table_id", "resultados_calculo_sistema_folha") # Nova tabela
        self.location = config.get("gcp_location", "US")

        # Validações explícitas para project_id
        if not self.project_id:
            raise ValueError("gcp_project_id é obrigatório na configuração para ControleFolhaLoader.")
        
        # Neste ponto, self.project_id e self.dataset_id são str e não None.

        logger.info(f"ControleFolhaLoader inicializado para client_id: {self.client_id}, projeto: {self.project_id}, dataset: {self.dataset_id}")

        # Garantir que o dataset e as tabelas de controle existam com o schema correto
        try:
            # self.dataset_id é agora garantidamente uma string
            create_dataset_if_not_exists(self.client, self.dataset_id, self.location)
            create_or_update_table(self.client, self.dataset_id, self.empresas_table_id, EMPRESAS_TABLE_SCHEMA)
            create_or_update_table(self.client, self.dataset_id, self.folhas_table_id, FOLHAS_TABLE_SCHEMA)
            create_or_update_table(self.client, self.dataset_id, self.resultados_calculo_table_id, RESULTADOS_CALCULO_SISTEMA_FOLHA_SCHEMA_DETALHADO)
            logger.info(f"[{self.client_id}] Dataset e tabelas de controle verificados/criados.")
        except Exception as e_init_tables:
            logger.error(f"[{self.client_id}] Erro ao inicializar dataset/tabelas de controle: {e_init_tables}", exc_info=True)
            # Considerar se deve levantar a exceção aqui, dependendo da criticidade.
            # Por enquanto, apenas loga o erro.

    def _ensure_client(self):
        # Este método não é mais necessário, pois o cliente é injetado.
        # Pode ser removido ou deixado como pass se houver chamadas antigas.
        pass

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception), # Tenta novamente em exceções genéricas que podem indicar problemas transitórios
        reraise=True
    )
    def listar_todas_as_empresas(self) -> pd.DataFrame:
        # self._ensure_client() # Removido
        query = f"""
            SELECT empresa_id, nome_empresa, cnpj_empresa, data_cadastro
            FROM `{self.project_id}.{self.dataset_id}.{self.empresas_table_id}`
            WHERE client_id = @client_id
            ORDER BY nome_empresa
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id)
            ]
        )
        try:
            logger.info(f"[{self.client_id}] Executando query para listar todas as empresas.")
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.to_dataframe()
            logger.info(f"[{self.client_id}] Query para listar empresas concluída. {len(results)} empresas encontradas.")
            return results
        except RetryError as re:
            logger.error(f"[{self.client_id}] Todas as tentativas de executar a query para listar empresas falharam: {re}")
            raise
        except Exception as e:
            logger.error(f"[{self.client_id}] Erro ao executar query para listar empresas: {e}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def inserir_empresa(self, nome_empresa: str, cnpj_empresa: Optional[str] = None) -> dict:
        timestamp_cadastro = datetime.now(timezone.utc)
        cnpj_empresa_tratado = ''.join(filter(str.isdigit, cnpj_empresa)) if cnpj_empresa else None

        empresa_existente = None
        if cnpj_empresa_tratado:
            try:
                empresa_existente = self.get_empresa_by_cnpj(cnpj_empresa_tratado)
            except RetryError as re_get:
                logger.error(f"[{self.client_id}] Falha ao buscar empresa pelo CNPJ {cnpj_empresa_tratado} para inserção/atualização após retries: {re_get}")
                raise
            except Exception as e_get:
                logger.error(f"[{self.client_id}] Erro crítico ao verificar existência da empresa pelo CNPJ {cnpj_empresa_tratado}: {e_get}")
                raise

        if empresa_existente:
            empresa_id_final = empresa_existente["empresa_id"]
            logger.info(f"[{self.client_id}] Empresa com CNPJ {cnpj_empresa_tratado} já existe (ID: {empresa_id_final}). Atualizando nome para '{nome_empresa}'...")
            query = f"""
                UPDATE `{self.project_id}.{self.dataset_id}.{self.empresas_table_id}`
                SET nome_empresa = @nome_empresa, data_ultima_modificacao = @data_modificacao
                WHERE empresa_id = @empresa_id AND client_id = @client_id
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("nome_empresa", "STRING", nome_empresa),
                    bigquery.ScalarQueryParameter("data_modificacao", "TIMESTAMP", timestamp_cadastro), # Usar um campo de modificação
                    bigquery.ScalarQueryParameter("empresa_id", "STRING", empresa_id_final),
                    bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                ]
            )
            operation_type = "atualizar"
            # Mantém data_cadastro original, atualiza nome e data_modificacao
            ret_dict = {
                "empresa_id": empresa_id_final,
                "nome_empresa": nome_empresa,
                "cnpj_empresa": empresa_existente.get("cnpj_empresa"), # Usa o CNPJ existente
                "data_cadastro": empresa_existente.get("data_cadastro"), # Mantém data de cadastro original
                "data_ultima_modificacao": timestamp_cadastro.isoformat(),
                "client_id": self.client_id,
                "operation": "updated"
            }
        else:
            empresa_id_final = uuid.uuid4().hex
            logger.info(f"[{self.client_id}] Empresa com CNPJ {cnpj_empresa_tratado if cnpj_empresa_tratado else 'N/A'} não encontrada. Inserindo nova empresa '{nome_empresa}' com ID: {empresa_id_final}")
            query = f"""
            INSERT INTO `{self.project_id}.{self.dataset_id}.{self.empresas_table_id}`
            (empresa_id, client_id, nome_empresa, cnpj_empresa, data_cadastro, data_ultima_modificacao)
            VALUES (@empresa_id, @client_id, @nome_empresa, @cnpj_empresa, @data_cadastro, @data_ultima_modificacao)
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("empresa_id", "STRING", empresa_id_final),
                    bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                    bigquery.ScalarQueryParameter("nome_empresa", "STRING", nome_empresa),
                    bigquery.ScalarQueryParameter("cnpj_empresa", "STRING", cnpj_empresa_tratado),
                    bigquery.ScalarQueryParameter("data_cadastro", "TIMESTAMP", timestamp_cadastro),
                    bigquery.ScalarQueryParameter("data_ultima_modificacao", "TIMESTAMP", timestamp_cadastro),
                ]
            )
            operation_type = "inserir"
            ret_dict = {
                "empresa_id": empresa_id_final,
                "nome_empresa": nome_empresa,
                "cnpj_empresa": cnpj_empresa_tratado,
                "data_cadastro": timestamp_cadastro.isoformat(),
                "data_ultima_modificacao": timestamp_cadastro.isoformat(),
                "client_id": self.client_id,
                "operation": "inserted"
            }

        try:
            logger.info(f"[{self.client_id}] Tentando {operation_type} empresa '{nome_empresa}' (CNPJ: {cnpj_empresa_tratado if cnpj_empresa_tratado else 'N/A'})")
            query_job = self.client.query(query, job_config=job_config)
            query_job.result()
            logger.info(f"[{self.client_id}] Empresa '{nome_empresa}' ({operation_type}) com sucesso.")
            return ret_dict
        except RetryError as re_op:
            logger.error(f"[{self.client_id}] Todas as tentativas de {operation_type} empresa '{nome_empresa}' falharam: {re_op}")
            raise
        except Exception as e_op:
            logger.error(f"[{self.client_id}] Erro ao {operation_type} empresa '{nome_empresa}': {e_op}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def get_empresa_by_cnpj(self, cnpj: str) -> Optional[dict]:
        """Busca uma empresa pelo CNPJ."""
        if not self.client_id:
            raise ValueError("client_id não está configurado no ControleFolhaLoader.")
        query = f"""
            SELECT empresa_id, nome_empresa, cnpj_empresa, data_cadastro
            FROM `{self.project_id}.{self.dataset_id}.{self.empresas_table_id}`
            WHERE client_id = @client_id AND cnpj_empresa = @cnpj
            LIMIT 1
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                bigquery.ScalarQueryParameter("cnpj", "STRING", cnpj),
            ]
        )
        try:
            logger.info(f"[{self.client_id}] Buscando empresa pelo CNPJ: {cnpj}")
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.to_dataframe()
            if not results.empty:
                return results.iloc[0].to_dict()
            return None
        except RetryError as re_inner:
            logger.error(f"[{self.client_id}] Todas as tentativas de buscar empresa pelo CNPJ {cnpj} falharam: {re_inner}")
            raise
        except Exception as e_inner:
            logger.error(f"[{self.client_id}] Erro ao buscar empresa pelo CNPJ {cnpj}: {e_inner}", exc_info=True)
            raise 

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def upsert_folha_status(self, id_folha: str, competencia_folha: str, id_empresa: str, status: str, data_processamento: datetime, detalhes_processamento: Optional[Dict[str, Any]] = None, nome_arquivo_original: Optional[str] = None) -> None:
        """
        Insere ou atualiza o status de uma folha na tabela 'folhas'.
        Se a folha já existir (baseado em id_folha e client_id), atualiza os campos.
        Caso contrário, insere um novo registro.
        """
        if not self.client_id:
            raise ValueError("client_id não está configurado.")
        if not id_folha or not competencia_folha or not id_empresa or not status:
            raise ValueError("id_folha, competencia_folha, id_empresa e status são obrigatórios.")

        # self.dataset_id é garantidamente uma string aqui
        table_ref = self.client.dataset(self.dataset_id).table(self.folhas_table_id)
        
        # Tenta buscar a folha para ver se existe
        query_check = f"""
            SELECT id_folha FROM `{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}`
            WHERE client_id = @client_id AND id_folha = @id_folha
            LIMIT 1
        """
        job_config_check = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha),
            ]
        )
        
        folha_existente = False
        try:
            query_job_check = self.client.query(query_check, job_config=job_config_check)
            results = query_job_check.to_dataframe()
            if not results.empty:
                folha_existente = True
        except Exception as e_check:
            logger.error(f"[{self.client_id}] Erro ao verificar existência da folha {id_folha} antes do upsert: {e_check}", exc_info=True)
            # Prosseguir com a tentativa de inserção/atualização mesmo assim, o MERGE cuidará disso.
            # Ou levantar a exceção se for crítico. Por ora, prossegue.

        data_modificacao = datetime.now(timezone.utc)
        detalhes_json = json.dumps(detalhes_processamento) if detalhes_processamento else None

        if folha_existente:
            logger.info(f"[{self.client_id}] Folha {id_folha} existente. Atualizando status para {status}.")
            # Atualizar
            query_upsert = f"""
                UPDATE `{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}`
                SET 
                    status = @status,
                    data_ultima_modificacao = @data_modificacao,
                    detalhes_processamento = @detalhes_processamento
                    # Outros campos podem ser atualizados se necessário, ex: nome_arquivo_original
                    {", nome_arquivo_original = @nome_arquivo_original" if nome_arquivo_original else ""}
                WHERE client_id = @client_id AND id_folha = @id_folha
            """
            params_upsert = [
                bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha),
                bigquery.ScalarQueryParameter("status", "STRING", status),
                bigquery.ScalarQueryParameter("data_modificacao", "TIMESTAMP", data_modificacao),
                bigquery.ScalarQueryParameter("detalhes_processamento", "STRING", detalhes_json),
            ]
            if nome_arquivo_original:
                params_upsert.append(bigquery.ScalarQueryParameter("nome_arquivo_original", "STRING", nome_arquivo_original))
        else:
            logger.info(f"[{self.client_id}] Folha {id_folha} não existente. Inserindo com status {status}.")
            # Inserir
            query_upsert = f"""
                INSERT INTO `{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}`
                (client_id, id_folha, codigo_empresa, mes_ano, tipo_folha, status, data_cadastro, data_ultima_modificacao, nome_arquivo_original, detalhes_processamento)
                VALUES (@client_id, @id_folha, @codigo_empresa, @mes_ano, @tipo_folha, @status, @data_cadastro, @data_ultima_modificacao, @nome_arquivo_original, @detalhes_processamento)
            """
            # Para inserção, tipo_folha pode ser um placeholder se não conhecido
            tipo_folha_placeholder = detalhes_processamento.get("tipo_folha_original", "NAO_INFORMADO") if detalhes_processamento else "NAO_INFORMADO"

            params_upsert = [
                bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha),
                bigquery.ScalarQueryParameter("codigo_empresa", "STRING", id_empresa),
                bigquery.ScalarQueryParameter("mes_ano", "STRING", competencia_folha), # YYYY-MM
                bigquery.ScalarQueryParameter("tipo_folha", "STRING", tipo_folha_placeholder),
                bigquery.ScalarQueryParameter("status", "STRING", status),
                bigquery.ScalarQueryParameter("data_cadastro", "TIMESTAMP", data_processamento), # Data do evento que gerou este registro
                bigquery.ScalarQueryParameter("data_ultima_modificacao", "TIMESTAMP", data_modificacao),
                bigquery.ScalarQueryParameter("nome_arquivo_original", "STRING", nome_arquivo_original),
                bigquery.ScalarQueryParameter("detalhes_processamento", "STRING", detalhes_json),
            ]
        
        job_config_upsert = bigquery.QueryJobConfig(query_parameters=params_upsert)
        try:
            query_job_upsert = self.client.query(query_upsert, job_config=job_config_upsert)
            query_job_upsert.result() 
            logger.info(f"[{self.client_id}] Upsert do status da folha {id_folha} para {status} concluído.")
        except Exception as e_upsert:
            logger.error(f"[{self.client_id}] Erro durante o upsert do status da folha {id_folha}: {e_upsert}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def inserir_folha(self, empresa_id: str, competencia: str, tipo_folha: str, data_upload: datetime, nome_arquivo_original: str) -> str:
        # df_folha: pd.DataFrame removido da assinatura
        if not self.client_id:
            raise ValueError("client_id não está configurado no ControleFolhaLoader para inserir_folha.")
        if not empresa_id:
            raise ValueError("empresa_id é obrigatório para inserir_folha.")

        folha_id = f"FL-{empresa_id}-{competencia}-{tipo_folha}-{datetime.now().strftime('%Y%m%d%H%M%S%f')}" # Adicionado %f para microsegundos
        
        # Obter CNPJ da empresa para consistência, se necessário (opcional, mas bom para referência)
        # cnpj_da_empresa = self.get_empresa_by_id(empresa_id).get('cnpj_empresa') # Supondo que exista get_empresa_by_id

        query = f"""
        INSERT INTO `{self.project_id}.{self.dataset_id}.{self.folhas_table_id}` 
        (client_id, id_folha, codigo_empresa, mes_ano, tipo_folha, status, data_cadastro, 
         nome_arquivo_original, data_ultima_modificacao)
        VALUES (@client_id, @id_folha, @codigo_empresa, @mes_ano, @tipo_folha, @status, @data_cadastro, 
                @nome_arquivo_original, @data_ultima_modificacao)
        """
        
        current_ts = datetime.now(timezone.utc)
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                bigquery.ScalarQueryParameter("id_folha", "STRING", folha_id),
                bigquery.ScalarQueryParameter("codigo_empresa", "STRING", empresa_id), # Alterado para STRING se empresa_id for UUID
                bigquery.ScalarQueryParameter("mes_ano", "STRING", competencia),
                bigquery.ScalarQueryParameter("tipo_folha", "STRING", tipo_folha),
                bigquery.ScalarQueryParameter("status", "STRING", "PENDENTE_PROCESSAMENTO"),
                bigquery.ScalarQueryParameter("data_cadastro", "TIMESTAMP", data_upload),
                bigquery.ScalarQueryParameter("nome_arquivo_original", "STRING", nome_arquivo_original),
                bigquery.ScalarQueryParameter("data_ultima_modificacao", "TIMESTAMP", current_ts),
            ]
        )
        try:
            logger.info(f"[{self.client_id}] Inserindo folha ID: {folha_id} para a empresa {empresa_id}, competência {competencia}, tipo {tipo_folha}.")
            query_job = self.client.query(query, job_config=job_config)
            query_job.result()
            logger.info(f"[{self.client_id}] Folha ID {folha_id} inserida com sucesso.")
            return folha_id
        except RetryError as re_insert_folha:
            logger.error(f"[{self.client_id}] Todas as tentativas de inserir a folha {folha_id} falharam: {re_insert_folha}")
            raise
        except Exception as e_insert_folha:
            logger.error(f"[{self.client_id}] Erro ao inserir a folha {folha_id} para a empresa {empresa_id}: {e_insert_folha}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def consolidar_dados_planilha_para_folhas(self, empresa_id: str, competencia: str, tipo_folha: str, id_folha: str, df_consolidado: pd.DataFrame) -> int:
        if not self.client_id:
            logger.error(f"Client_id não configurado para consolidar_dados_planilha_para_folhas.")
            raise ValueError("client_id não está configurado.")

        if df_consolidado.empty:
            logger.warning(f"[{self.client_id}] DataFrame consolidado está vazio para id_folha {id_folha} (empresa: {empresa_id}, competência: {competencia}). Nada a carregar.")
            return 0

        # Preparar DataFrame para carregamento
        df_to_load = df_consolidado.copy()
        current_ts = datetime.now(timezone.utc)

        # Adicionar/sobrescrever colunas de controle
        df_to_load["client_id"] = self.client_id
        df_to_load["id_folha"] = id_folha
        df_to_load["timestamp_carga_raw"] = current_ts
        df_to_load["codigo_empresa"] = empresa_id
        df_to_load["mes_ano"] = competencia
        
        # id_extracao_planilha: usar id_folha se não existir no df_consolidado.
        # Este campo está no schema base, então garantimos que ele exista no DataFrame.
        if "id_extracao_planilha" not in df_to_load.columns:
            df_to_load["id_extracao_planilha"] = id_folha
        
        # cnpj_empresa: é NULLABLE no schema base. Se não estiver no df_consolidado,
        # o BigQuery permitirá nulo. Se estiver, será usado.

        # Construir o schema do BigQuery dinamicamente
        # Schema base (campos de controle principais)
        # Nota: cnpj_empresa é NULLABLE e pode ou não estar no df_consolidado.
        # Se estiver, seu tipo será inferido abaixo. Se não, o schema base o define como STRING NULLABLE.
        base_schema_fields = [
            bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("id_folha", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("timestamp_carga_raw", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("codigo_empresa", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("mes_ano", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("id_extracao_planilha", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("cnpj_empresa", "STRING", mode="NULLABLE"),
        ]
        
        final_schema_for_bq = {field.name: field for field in base_schema_fields}

        for col_name in df_to_load.columns:
            if col_name not in final_schema_for_bq:
                col_dtype = df_to_load[col_name].dtype
                bq_type = "STRING" # Default type
                if pd.api.types.is_integer_dtype(col_dtype):
                    bq_type = "INT64"
                elif pd.api.types.is_float_dtype(col_dtype):
                    bq_type = "FLOAT64"
                elif pd.api.types.is_bool_dtype(col_dtype):
                    bq_type = "BOOL"
                elif pd.api.types.is_datetime64_any_dtype(col_dtype) or pd.api.types.is_timedelta64_dtype(col_dtype):
                    bq_type = "TIMESTAMP"
                elif pd.api.types.is_object_dtype(col_dtype):
                    # Tentar converter para datetime se parecer uma data string, senão STRING
                    try:
                        # Testar apenas uma pequena amostra para performance
                        sample = df_to_load[col_name].dropna().iloc[:5]
                        if not sample.empty:
                             pd.to_datetime(sample, errors='raise')
                             bq_type = "TIMESTAMP" 
                    except (ValueError, TypeError, AttributeError): # AttributeError para caso de tipos mistos que não têm iloc
                        bq_type = "STRING"
                
                final_schema_for_bq[col_name] = bigquery.SchemaField(col_name, bq_type, mode="NULLABLE")

        ordered_final_schema = [final_schema_for_bq[name] for name in df_to_load.columns if name in final_schema_for_bq]
        # Adicionar campos do schema base que podem não estar no df_to_load (ex: se df_to_load for muito mínimo)
        for field in base_schema_fields:
            if field.name not in df_to_load.columns:
                 # Adiciona ao schema, mas o BQ vai inserir nulos se não estiver no dataframe
                 if field.name not in final_schema_for_bq: # Evitar duplicatas se já adicionado
                    final_schema_for_bq[field.name] = field # Adiciona o campo base
                    ordered_final_schema.append(field)


        full_raw_data_table_id = f"{self.project_id}.{self.dataset_id}.{self.raw_data_table_id}"
        
        try:
            create_dataset_if_not_exists(self.client, self.dataset_id, self.location)
            create_or_update_table(self.client, self.dataset_id, self.raw_data_table_id, ordered_final_schema)

            job_config = bigquery.LoadJobConfig(
                schema=ordered_final_schema, # Usar o schema construído
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            )
            
            logger.info(f"[{self.client_id}] Iniciando carregamento de {len(df_to_load)} linhas para '{full_raw_data_table_id}' (id_folha: {id_folha}). Schema com {len(ordered_final_schema)} campos.")
            
            load_job = self.client.load_table_from_dataframe(
                df_to_load, full_raw_data_table_id, job_config=job_config
            )
            load_job.result() 

            if load_job.errors:
                logger.error(f"[{self.client_id}] Erro ao carregar dados para '{full_raw_data_table_id}' (id_folha: {id_folha}): {load_job.errors}")
                raise RuntimeError(f"Erro no job de carregamento do BigQuery para raw_data: {load_job.errors}")
            else:
                output_rows = load_job.output_rows if load_job.output_rows is not None else 0
                logger.info(f"[{self.client_id}] Carregamento para raw_data concluído. {output_rows} linhas carregadas para '{full_raw_data_table_id}' (id_folha: {id_folha}).")
                return output_rows
        except RetryError as re_consolidate:
            logger.error(f"[{self.client_id}] Todas as tentativas de carregamento para raw_data '{full_raw_data_table_id}' (id_folha: {id_folha}) falharam: {re_consolidate}")
            raise
        except Exception as e_consolidate:
            logger.error(f"[{self.client_id}] Erro durante o processo de carregamento para raw_data '{full_raw_data_table_id}' (id_folha: {id_folha}): {e_consolidate}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def obter_dados_folha_para_processamento(self, id_folha: str) -> pd.DataFrame:
        if not self.client_id:
            raise ValueError("client_id não está configurado no ControleFolhaLoader.")

        query = f"""
            SELECT *
            FROM `{self.project_id}.{self.dataset_id}.{self.raw_data_table_id}`
            WHERE client_id = @client_id
              AND id_folha = @id_folha
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha),
            ]
        )
        try:
            logger.info(f"[{self.client_id}] Buscando dados da folha {id_folha} para processamento.")
            query_job = self.client.query(query, job_config=job_config)
            df_result = query_job.to_dataframe()
            logger.info(f"[{self.client_id}] {len(df_result)} registros encontrados para a folha {id_folha}.")
            return df_result
        except RetryError as re_get_data:
            logger.error(f"[{self.client_id}] Todas as tentativas de obter dados da folha {id_folha} falharam: {re_get_data}")
            raise
        except Exception as e_get_data:
            logger.error(f"[{self.client_id}] Erro ao obter dados da folha {id_folha}: {e_get_data}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def marcar_folha_como_processada(self, id_folha: str, status_processamento: str = "PROCESSADA", detalhes: Optional[Dict[str, Any]] = None) -> None:
        if not self.client_id:
            raise ValueError("client_id não está configurado no ControleFolhaLoader.")

        detalhes_json = json.dumps(detalhes) if detalhes else None
        query = f"""
            UPDATE `{self.project_id}.{self.dataset_id}.{self.folhas_table_id}`
            SET status = @status_processamento, 
                data_ultima_modificacao = @data_modificacao
                {", detalhes_processamento = @detalhes_json" if detalhes_json else ""}
            WHERE id_folha = @id_folha AND client_id = @client_id
        """
        params = [
            bigquery.ScalarQueryParameter("status_processamento", "STRING", status_processamento),
            bigquery.ScalarQueryParameter("data_modificacao", "TIMESTAMP", datetime.now(timezone.utc)),
            bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha),
            bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
        ]
        if detalhes_json:
            params.append(bigquery.ScalarQueryParameter("detalhes_json", "STRING", detalhes_json))
            
        job_config = bigquery.QueryJobConfig(query_parameters=params)
        try:
            logger.info(f"[{self.client_id}] Marcando folha {id_folha} como {status_processamento}.")
            query_job = self.client.query(query, job_config=job_config)
            query_job.result()
            logger.info(f"[{self.client_id}] Folha {id_folha} marcada como {status_processamento} com sucesso.")
        except RetryError as re_mark:
            logger.error(f"[{self.client_id}] Todas as tentativas de marcar folha {id_folha} como {status_processamento} falharam: {re_mark}")
            raise
        except Exception as e_mark:
            logger.error(f"[{self.client_id}] Erro ao marcar folha {id_folha} como {status_processamento}: {e_mark}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def _verificar_folha_existente_por_controle(self, empresa_id: str, competencia: str, tipo_folha: str, nome_arquivo_origem_controle: str) -> Optional[str]:
        """
        Verifica se uma folha, originada de um arquivo de controle específico, já existe.
        Retorna o id_folha se existente, caso contrário None.
        """
        if not self.client_id:
            raise ValueError("client_id não está configurado.")
        
        query = f"""
            SELECT id_folha
            FROM `{self.project_id}.{self.dataset_id}.{self.folhas_table_id}`
            WHERE client_id = @client_id
              AND codigo_empresa = @empresa_id
              AND mes_ano = @competencia
              AND tipo_folha = @tipo_folha
              AND nome_arquivo_original = @nome_arquivo_origem_controle
            LIMIT 1
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                bigquery.ScalarQueryParameter("empresa_id", "STRING", empresa_id),
                bigquery.ScalarQueryParameter("competencia", "STRING", competencia),
                bigquery.ScalarQueryParameter("tipo_folha", "STRING", tipo_folha),
                bigquery.ScalarQueryParameter("nome_arquivo_origem_controle", "STRING", nome_arquivo_origem_controle),
            ]
        )
        try:
            logger.info(f"[{self.client_id}] Verificando existência de folha de controle: Empresa {empresa_id}, Comp {competencia}, Tipo {tipo_folha}, Arquivo {nome_arquivo_origem_controle}")
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.to_dataframe()
            if not results.empty:
                id_folha_existente = results.iloc[0]['id_folha']
                logger.info(f"[{self.client_id}] Folha de controle já existe com ID: {id_folha_existente}.")
                return id_folha_existente
            return None
        except RetryError as re_check:
            logger.error(f"[{self.client_id}] Todas as tentativas de verificar folha de controle existente falharam: {re_check}")
            raise
        except Exception as e_check:
            logger.error(f"[{self.client_id}] Erro ao verificar folha de controle existente: {e_check}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def processar_dados_controle_para_folhas(self, nome_arquivo_origem_controle: str, tabela_dados_controle_id: str) -> dict:
        """
        Processa os dados de uma tabela de controle (preenchida pelo sheet_loader)
        e cria/atualiza registros na tabela 'folhas'.
        """
        if not self.client_id:
            raise ValueError("client_id não está configurado no ControleFolhaLoader.")
        if not nome_arquivo_origem_controle:
            raise ValueError("nome_arquivo_origem_controle é obrigatório.")
        if not tabela_dados_controle_id:
            raise ValueError("tabela_dados_controle_id é obrigatória.")

        full_control_table_id = f"{self.project_id}.{self.dataset_id}.{tabela_dados_controle_id}"
        logger.info(f"[{self.client_id}] Iniciando processamento de dados de controle do arquivo '{nome_arquivo_origem_controle}' da tabela '{full_control_table_id}'.")

        query = f"""
            SELECT
                cnpj_empresa,
                status_aba_origem,  -- Usado como tipo_folha
                mes_ano_referencia, -- Usado como competencia (DATE)
                data_processamento_gcs, -- Usado como data_upload
                nome_arquivo_origem
            FROM `{full_control_table_id}`
            WHERE client_id = @client_id
              AND nome_arquivo_origem = @nome_arquivo_origem
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                bigquery.ScalarQueryParameter("nome_arquivo_origem", "STRING", nome_arquivo_origem_controle),
            ]
        )

        empresas_processadas = 0
        folhas_criadas = 0
        erros = []

        try:
            logger.info(f"[{self.client_id}] Buscando dados da tabela de controle: {full_control_table_id} para o arquivo {nome_arquivo_origem_controle}")
            query_job = self.client.query(query, job_config=job_config)
            df_control_data = query_job.to_dataframe()
            
            if df_control_data.empty:
                logger.info(f"[{self.client_id}] Nenhum dado encontrado na tabela de controle para o arquivo '{nome_arquivo_origem_controle}'.")
                return {"empresas_processadas": 0, "folhas_criadas": 0, "erros": 0}

            logger.info(f"[{self.client_id}] {len(df_control_data)} registros encontrados na tabela de controle para processamento.")

            for index, row in df_control_data.iterrows():
                cnpj = row.get("cnpj_empresa")
                tipo_folha = row.get("status_aba_origem", "N/A")
                competencia_date = row.get("mes_ano_referencia")
                data_upload_ts = row.get("data_processamento_gcs")
                
                if not cnpj or competencia_date is None or data_upload_ts is None:
                    msg_erro = f"Registro ignorado devido a dados ausentes (CNPJ, competência ou data_upload): {row.to_dict()}"
                    logger.warning(f"[{self.client_id}] {msg_erro}")
                    erros.append(msg_erro)
                    continue

                competencia_str = competencia_date.strftime('%Y-%m') if isinstance(competencia_date, (datetime, pd.Timestamp, date)) else str(competencia_date)
                empresa_id = None # Inicializa empresa_id

                try:
                    nome_empresa_placeholder = f"Empresa CNPJ {cnpj} (Controle)"
                    empresa_info = self.inserir_empresa(nome_empresa=nome_empresa_placeholder, cnpj_empresa=cnpj)
                    empresa_id = empresa_info["empresa_id"]
                    empresas_processadas += 1 
                except Exception as e_emp:
                    msg_erro = f"Erro ao inserir/atualizar empresa com CNPJ {cnpj}: {e_emp}"
                    logger.error(f"[{self.client_id}] {msg_erro}", exc_info=True)
                    erros.append(msg_erro)
                    continue # Pula para o próximo registro do arquivo de controle
                
                # Se chegou aqui, empresa_id é válido.
                # Verificar se a folha de controle já existe
                id_folha_existente = None
                try:
                    id_folha_existente = self._verificar_folha_existente_por_controle(
                        empresa_id=empresa_id,
                        competencia=competencia_str,
                        tipo_folha=tipo_folha,
                        nome_arquivo_origem_controle=nome_arquivo_origem_controle
                    )
                except Exception as e_check_folha: # Captura exceção da verificação
                    msg_erro = f"Erro ao verificar existência da folha de controle para CNPJ {cnpj}, competência {competencia_str}: {e_check_folha}"
                    logger.error(f"[{self.client_id}] {msg_erro}", exc_info=True)
                    erros.append(msg_erro)
                    continue # Pula para o próximo registro

                if id_folha_existente:
                    logger.info(f"[{self.client_id}] Folha de controle para CNPJ {cnpj}, competência {competencia_str}, tipo {tipo_folha} (arquivo: {nome_arquivo_origem_controle}) já registrada com ID {id_folha_existente}. Pulando inserção.")
                    continue # Pula para o próximo registro do arquivo de controle

                # Inserir a folha (somente se não existir e a verificação não falhou)
                try:
                    if isinstance(data_upload_ts, str):
                        data_upload_dt = datetime.fromisoformat(data_upload_ts)
                    elif isinstance(data_upload_ts, pd.Timestamp):
                         data_upload_dt = data_upload_ts.to_pydatetime()
                    else: 
                        data_upload_dt = data_upload_ts

                    if data_upload_dt.tzinfo is None:
                        data_upload_dt = data_upload_dt.replace(tzinfo=timezone.utc)
                    
                    id_folha_criada = self.inserir_folha(
                        empresa_id=empresa_id, # empresa_id está definido aqui
                        competencia=competencia_str,
                        tipo_folha=tipo_folha,
                        data_upload=data_upload_dt,
                        nome_arquivo_original=nome_arquivo_origem_controle
                        # df_folha=dummy_df removido da chamada
                    )
                    self.marcar_folha_como_processada(id_folha_criada, status_processamento="PROCESSADO_CONTROLE")
                    folhas_criadas += 1
                    logger.info(f"[{self.client_id}] Folha de controle registrada com ID: {id_folha_criada} para CNPJ {cnpj}, competência {competencia_str}, tipo {tipo_folha}.")

                except Exception as e_folha: # Captura exceção da inserção/marcação
                    msg_erro = f"Erro ao registrar folha de controle para CNPJ {cnpj}, competência {competencia_str}: {e_folha}"
                    logger.error(f"[{self.client_id}] {msg_erro}", exc_info=True)
                    erros.append(msg_erro)
                    continue
            
            logger.info(f"[{self.client_id}] Processamento de dados de controle para '{nome_arquivo_origem_controle}' concluído. {folhas_criadas} folhas registradas. {len(erros)} erros.")
            return {"empresas_processadas": empresas_processadas, "folhas_criadas": folhas_criadas, "erros": len(erros), "detalhes_erros": erros}

        except RetryError as re_query:
            logger.error(f"[{self.client_id}] Todas as tentativas de buscar dados da tabela de controle '{full_control_table_id}' falharam: {re_query}")
            raise
        except Exception as e_query:
            logger.error(f"[{self.client_id}] Erro ao buscar dados da tabela de controle '{full_control_table_id}': {e_query}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def salvar_resultados_calculo_folha(self, id_folha_processada: str, resultados_calculo: List[Dict[str, Any]]) -> int:
        """
        Salva os resultados do cálculo da folha (do MotorCalculoFolhaService)
        na tabela `resultados_calculo_sistema_folha`.

        Args:
            id_folha_processada (str): O ID da folha que foi processada.
            resultados_calculo (List[Dict[str, Any]]): Uma lista de dicionários, onde cada dicionário
                                                       é o resultado de `calcular_folha_funcionario_audit360`.
        Returns:
            Número de registros de resultados salvos.
        """
        if not self.client_id:
            raise ValueError("client_id não está configurado no ControleFolhaLoader.")
        if not id_folha_processada:
            raise ValueError("id_folha_processada é obrigatório.")
        if not resultados_calculo:
            logger.info(f"[{self.client_id}] Nenhum resultado de cálculo fornecido para a folha {id_folha_processada}. Nada a salvar.")
            return 0

        full_results_table_id = f"{self.project_id}.{self.dataset_id}.{self.resultados_calculo_table_id}"
        logger.info(f"[{self.client_id}] Iniciando salvamento de {len(resultados_calculo)} resultados de cálculo para a folha {id_folha_processada} na tabela {full_results_table_id}.")

        registros_para_bq = []
        for resultado_func in resultados_calculo:
            # Garantir que todos os campos do schema existam no dicionário, preenchendo com None se ausente
            # e convertendo tipos se necessário (ex: JSON para string)
            registro = {
                "client_id": self.client_id,
                "id_resultado_calculo": str(uuid.uuid4()), # Gerar um novo UUID para cada resultado
                "id_folha_processada_fk": id_folha_processada,
                "id_funcionario": resultado_func.get("id_funcionario"),
                "competencia_folha": resultado_func.get("competencia_folha"),
                "base_calculo_inss_sistema": resultado_func.get("base_calculo_inss_sistema"),
                "valor_inss_calculado_sistema": resultado_func.get("valor_inss_calculado_sistema"),
                "aliquota_efetiva_inss_sistema": resultado_func.get("aliquota_efetiva_inss_sistema"),
                "base_calculo_irrf_bruta_sistema": resultado_func.get("base_calculo_irrf_bruta_sistema"),
                "base_calculo_irrf_liquida_sistema": resultado_func.get("base_calculo_irrf_liquida_sistema"),
                "valor_irrf_calculado_sistema": resultado_func.get("valor_irrf_calculado_sistema"),
                "base_calculo_fgts_sistema": resultado_func.get("base_calculo_fgts_sistema"),
                "valor_fgts_calculado_sistema": resultado_func.get("valor_fgts_calculado_sistema"),
                "salario_familia_calculado_sistema": resultado_func.get("salario_familia_calculado_sistema"),
                "valor_periculosidade_calculado_sistema": resultado_func.get("valor_periculosidade_calculado_sistema"),
                "valor_insalubridade_calculado_sistema": resultado_func.get("valor_insalubridade_calculado_sistema"),
                "valor_adicional_noturno_calculado_sistema": resultado_func.get("valor_adicional_noturno_calculado_sistema"),
                "valor_dsr_calculado_sistema": resultado_func.get("valor_dsr_calculado_sistema"),
                "outras_verbas_calculadas_motor": json.dumps(resultado_func.get("outras_verbas_calculadas_motor")) if resultado_func.get("outras_verbas_calculadas_motor") else None,
                "total_vencimentos_calculado_sistema": resultado_func.get("total_vencimentos_calculado_sistema"),
                "total_descontos_calculado_sistema": resultado_func.get("total_descontos_calculado_sistema"),
                "total_liquido_calculado_sistema": resultado_func.get("total_liquido_calculado_sistema"),
                "logs_calculo": json.dumps(resultado_func.get("logs_calculo")) if resultado_func.get("logs_calculo") else None,
                "data_calculo": resultado_func.get("data_calculo", datetime.now(timezone.utc).isoformat()),
            }
            registros_para_bq.append(registro)

        job_config = bigquery.LoadJobConfig(
            schema=RESULTADOS_CALCULO_SISTEMA_FOLHA_SCHEMA_DETALHADO,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        )

        try:
            load_job = self.client.load_table_from_json(
                registros_para_bq, 
                full_results_table_id, 
                job_config=job_config
            )
            load_job.result()  # Espera o job completar

            if load_job.errors:
                logger.error(f"[{self.client_id}] Erro ao carregar resultados de cálculo para a folha {id_folha_processada} na tabela {full_results_table_id}: {load_job.errors}")
                # Considerar levantar uma exceção mais específica ou tratar os erros individualmente
                raise RuntimeError(f"Erro no job de carregamento do BigQuery para resultados de cálculo: {load_job.errors}")
            else:
                output_rows = load_job.output_rows if load_job.output_rows is not None else 0
                logger.info(f"[{self.client_id}] Carregamento de {output_rows} resultados de cálculo para a folha {id_folha_processada} concluído com sucesso para {full_results_table_id}.")
                return output_rows
        except RetryError as re_save_results:
            logger.error(f"[{self.client_id}] Todas as tentativas de salvar resultados de cálculo para a folha {id_folha_processada} na tabela {full_results_table_id} falharam: {re_save_results}")
            # A lógica de tratamento de load_job.errors já está no bloco try principal.
            # Se chegamos aqui devido a RetryError, o job provavelmente não foi bem-sucedido ou não foi totalmente executado.
            # A exceção original (RetryError) será levantada pelo reraise=True no decorador @retry,
            # ou se quisermos adicionar mais contexto ou tratar especificamente aqui antes de relançar:
            if hasattr(load_job, 'errors') and load_job.errors: # Verificar se load_job existe e tem erros
                 logger.error(f"[{self.client_id}] Detalhes do erro no job após retries: {load_job.errors}")
                 # Poderia levantar um erro customizado aqui se necessário, mas o @retry já fará o reraise.
            raise
        except Exception as e_save_results:
            logger.error(f"[{self.client_id}] Erro ao salvar resultados de cálculo para a folha {id_folha_processada} na tabela {full_results_table_id}: {e_save_results}", exc_info=True)
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def obter_info_basica_folha(self, id_folha: str) -> Optional[Dict[str, Any]]:
        """Busca informações básicas de uma folha (id_empresa, competencia_folha) pelo id_folha."""
        if not self.client_id:
            raise ValueError("client_id não está configurado no ControleFolhaLoader.")
        
        # self.dataset_id é garantidamente uma string aqui
        table_ref = self.client.dataset(self.dataset_id).table(self.folhas_table_id)
        query = f"""
            SELECT codigo_empresa, mes_ano as competencia_folha, tipo_folha, status, nome_arquivo_original
            FROM `{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}`
            WHERE client_id = @client_id AND id_folha = @id_folha
            LIMIT 1
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("client_id", "STRING", self.client_id),
                bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha),
            ]
        )
        try:
            logger.info(f"[{self.client_id}] Buscando informações básicas da folha: {id_folha}")
            query_job = self.client.query(query, job_config=job_config)
            results_df = query_job.to_dataframe()
            if not results_df.empty:
                folha_info = results_df.iloc[0].to_dict()
                logger.info(f"[{self.client_id}] Informações básicas encontradas para folha {id_folha}: {folha_info}")
                return folha_info
            logger.warning(f"[{self.client_id}] Nenhuma informação básica encontrada para folha {id_folha}.")
            return None
        except Exception as e_get_info:
            logger.error(f"[{self.client_id}] Erro ao buscar informações básicas da folha {id_folha}: {e_get_info}", exc_info=True)
            raise

# --- Bloco de teste e execução direta (exemplo de uso) ---
if __name__ == "__main__":
    # Configuração de mock para testes diretos
    mock_config_main = {
        "client_id": "teste_client_id",
        "gcp_project_id": "teste_project_id",
        "bq_dataset_id": "teste_dataset_id",
        "bq_table_id": os.environ.get("BQ_TABLE_ID_TEST", "test_table_main_entities"),
        "control_bq_dataset_id": os.environ.get("CONTROL_BQ_DATASET_ID_TEST", "test_control_dataset_main"),
        "control_folhas_table_id": "folhas_test",
        "control_empresas_table_id": "empresas_test",
        "control_raw_data_table_id": "controle_folha_raw_data_test",
        "control_resultados_calculo_table_id": "resultados_calculo_sistema_folha_test", # Adicionado para cobrir a nova tabela
        "gcp_location": os.environ.get("GCP_LOCATION_TEST", "US"),
        # "service_account_key_path_local_dev": "path/to/your/service_account.json" # Descomente se necessário para teste local
    }

    # Validação básica da configuração de teste
    required_config_keys = [
        "client_id", "gcp_project_id", "bq_dataset_id", "bq_table_id", 
        "control_bq_dataset_id", "gcp_location"
    ]
    if any(not mock_config_main.get(key) for key in required_config_keys):
        logger.error(f"Configuração de teste incompleta em __main__ de bq_loader. Faltando chaves: {required_config_keys}. Config: {mock_config_main}")
        logger.error("Pulando execução dos testes em __main__ de bq_loader.")
        exit(1)

    # Mock do cliente BigQuery para evitar chamadas reais, a menos que explicitamente desejado
    # Para testes de integração reais, você usaria um cliente real.
    # Aqui, vamos assumir que get_bigquery_client pode funcionar se as credenciais estiverem configuradas no ambiente.
    try:
        test_bq_client = get_bigquery_client(config_dict=mock_config_main)
        logger.info(f"Cliente BigQuery de teste criado com sucesso para o projeto {mock_config_main['gcp_project_id']}")
    except Exception as e_client_main:
        logger.error(f"Falha ao criar cliente BigQuery para o teste __main__: {e_client_main}. Verifique as credenciais/configuração.")
        logger.error("Pulando testes que dependem do cliente BQ.")
        test_bq_client = None # Impede a execução de testes dependentes

    if test_bq_client:
        # Teste de load_data_to_bigquery
        try:
            logger.info("--- Testando load_data_to_bigquery ---")
            sample_data_docai = [
                {
                    "id_extracao": "run_test_main_docai", 
                    "id_item": "item_1", 
                    "nome_arquivo_origem": "test_doc.pdf",
                    "tipo_campo": "total_value", 
                    "texto_extraido": "100.00",
                    "client_id": mock_config_main["client_id"] # client_id já é adicionado pela função, mas bom ter no dado original
                }
            ]
            # A função load_data_to_bigquery irá adicionar/sobrescrever client_id e timestamp_carga
            # create_dataset_if_not_exists e create_or_update_table são chamadas dentro de load_data_to_bigquery
            # Para um teste real, garanta que o dataset/tabela de teste exista ou possa ser criado.
            # Aqui, vamos mockar as chamadas de criação para focar no load.
            original_create_dataset = create_dataset_if_not_exists
            original_create_table = create_or_update_table
            
            def mock_create_dataset(*args, **kwargs):
                logger.info(f"__main__ MOCK create_dataset_if_not_exists chamado com: {args}, {kwargs}")
            def mock_create_table(*args, **kwargs):
                logger.info(f"__main__ MOCK create_or_update_table chamado com: {args}, {kwargs}")
            
            create_dataset_if_not_exists = mock_create_dataset
            create_or_update_table = mock_create_table
            
            # Mock da chamada de carregamento real para evitar escrita no BQ durante teste simples
            # Para teste de integração, remova este mock.
            with unittest.mock.patch.object(test_bq_client, 'load_table_from_json', autospec=True) as mock_load_json:
                mock_job = unittest.mock.MagicMock()
                mock_job.result.return_value = None
                mock_job.errors = None
                mock_job.output_rows = len(sample_data_docai)
                mock_load_json.return_value = mock_job
                
                rows_loaded = load_data_to_bigquery(client=test_bq_client, data=sample_data_docai, config=mock_config_main)
                logger.info(f"load_data_to_bigquery (simulado) carregou {rows_loaded} linhas.")
                assert rows_loaded == len(sample_data_docai)
                mock_load_json.assert_called_once()
                # Verificar se client_id foi adicionado aos dados passados para load_table_from_json
                called_data = mock_load_json.call_args[0][0]
                for row in called_data:
                    assert row["client_id"] == mock_config_main["client_id"]
                    assert "timestamp_carga" in row
            
            create_dataset_if_not_exists = original_create_dataset # Restaurar
            create_or_update_table = original_create_table # Restaurar
            logger.info("--- Teste de load_data_to_bigquery concluído (simulado) ---")

        except Exception as e_load_main:
            logger.error(f"Erro no teste __main__ de load_data_to_bigquery: {e_load_main}", exc_info=True)

        # Teste de ControleFolhaLoader
        try:
            logger.info("--- Testando ControleFolhaLoader ---")
            # Corrigido: Passar apenas config
            loader_controle = ControleFolhaLoader(config=mock_config_main) 
            
            # Teste inserir_empresa (com mock para evitar escrita)
            with unittest.mock.patch.object(loader_controle.client, 'query', autospec=True) as mock_query_empresa:
                mock_query_job_empresa = unittest.mock.MagicMock()
                mock_query_job_empresa.result.return_value = None # Para INSERT/UPDATE
                # Para get_empresa_by_cnpj, simular um DataFrame vazio (não encontrado)
                mock_query_job_empresa.to_dataframe.return_value = pd.DataFrame()
                mock_query_empresa.return_value = mock_query_job_empresa

                empresa_criada = loader_controle.inserir_empresa(nome_empresa="Empresa Teste Main", cnpj_empresa="00111222000133")
                logger.info(f"inserir_empresa (simulado) retornou: {empresa_criada}")
                assert empresa_criada["client_id"] == mock_config_main["client_id"]
                assert empresa_criada["operation"] == "inserted"
                # Verificar se a query de SELECT (get_empresa_by_cnpj) e INSERT foram chamadas
                # A ordem das chamadas pode variar dependendo se a empresa já existe.
                # Aqui, assumimos que não existe, então SELECT e depois INSERT.
                assert mock_query_empresa.call_count >= 2 # Pelo menos uma para SELECT e uma para INSERT/UPDATE

            # Teste inserir_folha (com mock)
            with unittest.mock.patch.object(loader_controle.client, 'query', autospec=True) as mock_query_folha:
                mock_query_job_folha = unittest.mock.MagicMock()
                mock_query_job_folha.result.return_value = None
                mock_query_folha.return_value = mock_query_job_folha

                # Supondo que empresa_criada["empresa_id"] existe
                id_empresa_teste = empresa_criada.get("empresa_id", "emp_test_id_main")
                sample_df_folha = pd.DataFrame({'col1': [1,2], 'col2': ['a','b']})
                
                id_folha_criada = loader_controle.inserir_folha(
                    empresa_id=id_empresa_teste,
                    competencia="2023-12", 
                    tipo_folha="Mensal",
                    data_upload=datetime.now(timezone.utc),
                    nome_arquivo_original="planilha_teste_main.xlsx"
                    # df_folha=sample_df_folha # Removido, pois o parâmetro não existe mais
                )
                logger.info(f"inserir_folha (simulado) retornou ID: {id_folha_criada}")
                assert id_folha_criada is not None
                mock_query_folha.assert_called_once()
                # Verificar se client_id foi usado no ScalarQueryParameter
                call_args_list = mock_query_folha.call_args_list
                found_client_id_param = False
                for call_arg in call_args_list:
                    _, kwargs_call = call_arg
                    job_config_call = kwargs_call.get('job_config')
                    if job_config_call and job_config_call.query_parameters:
                        for param in job_config_call.query_parameters:
                            if param.name == "client_id" and param.value == mock_config_main["client_id"]:
                                found_client_id_param = True
                                break
                    if found_client_id_param: break
                assert found_client_id_param, "client_id não encontrado nos parâmetros da query de inserir_folha"

            # Teste consolidar_dados_planilha_para_folhas (com mock)
            with unittest.mock.patch.object(loader_controle.client, 'load_table_from_dataframe', autospec=True) as mock_load_df:
                mock_job_df = unittest.mock.MagicMock()
                mock_job_df.result.return_value = None
                mock_job_df.output_rows = len(sample_df_folha)
                mock_load_df.return_value = mock_job_df

                rows_consolidadas = loader_controle.consolidar_dados_planilha_para_folhas(
                    empresa_id=id_empresa_teste,
                    competencia="2023-12",
                    tipo_folha="Mensal",
                    id_folha=id_folha_criada,
                    df_consolidado=sample_df_folha
                )
                logger.info(f"consolidar_dados_planilha_para_folhas (simulado) carregou {rows_consolidadas} linhas.")
                assert rows_consolidadas == len(sample_df_folha)
                mock_load_df.assert_called_once()
                # Verificar se client_id foi adicionado ao DataFrame carregado
                df_passed_to_load = mock_load_df.call_args[0][0]
                assert "client_id" in df_passed_to_load.columns
                assert all(df_passed_to_load["client_id"] == mock_config_main["client_id"])
                assert "id_folha" in df_passed_to_load.columns
                assert all(df_passed_to_load["id_folha"] == id_folha_criada)

            logger.info("--- Testes de ControleFolhaLoader concluídos (simulados) ---")

        except Exception as e_ctrl_loader_main:
            logger.error(f"Erro no teste __main__ de ControleFolhaLoader: {e_ctrl_loader_main}", exc_info=True)
    
    else:
        logger.warning("Cliente BigQuery de teste não pôde ser criado. Pulando testes dependentes do BQ no __main__ de bq_loader.")

    logger.info("Fim da execução do bloco de teste __main__ para bq_loader.py.")
