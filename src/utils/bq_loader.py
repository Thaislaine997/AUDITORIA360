import json
import logging
import os
import uuid
from datetime import datetime, timezone, date
from google.cloud import bigquery
from google.cloud import exceptions as google_exceptions
from google.oauth2 import service_account
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryError
import pandas as pd # Mantido para possível uso futuro
from typing import Optional, List, Dict, Any, Sequence, Union, cast

logger = logging.getLogger(__name__)

# Exportação explícita dos símbolos principais
__all__ = [
    'get_bigquery_client',
    'ControleFolhaLoader',
    'load_data_to_bq',
    'ensure_dataset_exists',
    'ensure_table_exists_or_updated',
]

# --- Implementações Mínimas ---

def get_bigquery_client(config: Optional[Dict[str, Any]] = None) -> Optional[bigquery.Client]:
    """
    Cria e retorna um cliente BigQuery.
    A configuração pode vir de variáveis de ambiente (GOOGLE_APPLICATION_CREDENTIALS)
    ou de um arquivo de conta de serviço especificado na config.
    """
    try:
        credentials = None
        project_id_from_config = config.get("GCP_PROJECT_ID") if config else None

        if config and config.get("GCP_SERVICE_ACCOUNT_FILE"):
            credentials_path = config["GCP_SERVICE_ACCOUNT_FILE"]
            if os.path.exists(credentials_path):
                logger.info(f"Tentando inicializar BigQuery Client com arquivo de conta de serviço: {credentials_path}")
                credentials = service_account.Credentials.from_service_account_file(credentials_path)
                # O projeto do arquivo de credenciais tem precedência se não houver um na config principal
                project_id_from_config = project_id_from_config or credentials.project_id
            else:
                logger.error(f"Arquivo de conta de serviço especificado não encontrado: {credentials_path}")
                return None
        
        client_kwargs: Dict[str, Any] = {}
        if credentials:
            client_kwargs['credentials'] = credentials
        if project_id_from_config:
            client_kwargs['project'] = project_id_from_config
            logger.info(f"Usando GCP_PROJECT_ID: {project_id_from_config} para o cliente BigQuery.")
        else:
            logger.info("Tentando inicializar BigQuery Client com credenciais padrão do ambiente e projeto inferido.")
        
        client = bigquery.Client(**client_kwargs)
        
        # Verifica se o cliente tem um projeto (seja da config, credenciais ou ambiente)
        if client.project:
             logger.info(f"BigQuery Client inicializado com sucesso. Projeto: {client.project}")
        else:
            logger.warning("BigQuery Client inicializado, mas o projeto não foi determinado. "
                           "Operações que exigem um projeto explícito podem falhar. "
                           "Considere definir GOOGLE_CLOUD_PROJECT ou passar GCP_PROJECT_ID na configuração.")
        return client
        
    except google_exceptions.GoogleCloudError as e:
        logger.error(f"Erro específico do Google Cloud ao inicializar cliente BigQuery: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"Erro genérico ao inicializar cliente BigQuery: {e}", exc_info=True)
        return None

class ControleFolhaLoader:
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa o loader para a tabela de controle de folhas.
        'config' deve conter 'GCP_PROJECT_ID' e 'CONTROL_BQ_DATASET_ID'.
        Opcionalmente, 'GCP_SERVICE_ACCOUNT_FILE' para autenticação e 'CONTROL_BQ_TABLE_ID'.
        """
        self.project_id: str 
        self.dataset_id: str = cast(str, config.get("CONTROL_BQ_DATASET_ID")) # Cast para informar ao linter
        self.table_name: str = config.get("CONTROL_BQ_TABLE_ID", "FolhasControle")

        # Tenta obter o project_id da configuração primeiro
        project_id_from_config = config.get("GCP_PROJECT_ID")
        # Inicializa o cliente BQ. Ele pode inferir o projeto se as credenciais do ambiente estiverem configuradas.
        self.client = get_bigquery_client(config)
        if not self.client:
            raise ConnectionError("Falha ao inicializar o cliente BigQuery para ControleFolhaLoader.")
        
        # Determina o project_id a ser usado
        if project_id_from_config:
            self.project_id = project_id_from_config
            # Se o cliente foi inicializado sem projeto explícito, mas temos um na config, reconfigure o cliente.
            # Acessar _credentials é interno e pode ser instável. Melhor re-inicializar com a config.
            if not self.client.project:
                logger.info(f"Reconfigurando cliente BigQuery com projeto explícito: {self.project_id} usando a configuração original.")
                # Passa a config original, que get_bigquery_client sabe como usar para credenciais e projeto.
                # Adiciona/sobrescreve o project_id na config para garantir que seja usado.
                temp_config = config.copy()
                temp_config["GCP_PROJECT_ID"] = self.project_id 
                reconfigured_client = get_bigquery_client(temp_config)
                if not reconfigured_client:
                    logger.error(f"Falha ao reconfigurar cliente com projeto {self.project_id} usando get_bigquery_client.")
                    raise ConnectionError(f"Falha ao reconfigurar cliente com projeto {self.project_id}")
                self.client = reconfigured_client
        elif self.client.project: # Se a config não tinha, mas o cliente inferiu
            self.project_id = self.client.project
            logger.info(f"Usando projeto inferido pelo cliente BigQuery: {self.project_id}")
        else: # Nem config, nem cliente inferiu
            raise ValueError("GCP_PROJECT_ID é obrigatório na configuração ou deve ser inferível pelas credenciais do ambiente.")

        if not self.dataset_id: # dataset_id é sempre obrigatório da config
            raise ValueError("CONTROL_BQ_DATASET_ID é obrigatório na configuração.")
        
        # Garante que o cliente BQ tenha um projeto associado para as operações seguintes
        if not self.client.project: # Checagem final
             raise ConnectionError(f"Cliente BigQuery não tem projeto associado após tentativas de configuração. Projeto necessário: {self.project_id}")

        self.full_table_id = f"{self.project_id}.{self.dataset_id}.{self.table_name}"
        logger.info(f"ControleFolhaLoader inicializado para {self.full_table_id}")
        self._ensure_controle_table_exists() 

    def _get_controle_folha_schema(self) -> List[bigquery.SchemaField]:
        return [
            bigquery.SchemaField("id_folha", "STRING", mode="REQUIRED", description="ID único da folha de pagamento, preferencialmente UUID"),
            bigquery.SchemaField("id_cliente", "STRING", mode="REQUIRED", description="ID do cliente/empresa principal dona dos dados"),
            bigquery.SchemaField("codigo_empresa_folha", "STRING", mode="NULLABLE", description="Código interno da empresa/filial na folha de pagamento de origem"),
            bigquery.SchemaField("cnpj_empresa_folha", "STRING", mode="NULLABLE", description="CNPJ da empresa/filial na folha de pagamento de origem"),
            bigquery.SchemaField("competencia_folha", "DATE", mode="REQUIRED", description="Mês e ano de competência da folha (primeiro dia do mês, ex: YYYY-MM-01)"),
            bigquery.SchemaField("tipo_folha", "STRING", mode="REQUIRED", description="Tipo da folha (ex: MENSAL, ADIANTAMENTO, 13_SALARIO_1A_PARCELA, 13_SALARIO_2A_PARCELA, PLR, FERIAS, RESCISAO)"),
            bigquery.SchemaField("status_processamento", "STRING", mode="REQUIRED", description="Status do processamento (PENDENTE, RECEBIDO, VALIDANDO, PROCESSANDO, CONCLUIDO_SUCESSO, CONCLUIDO_ERROS, ERRO_FATAL)"),
            bigquery.SchemaField("data_upload_cliente", "TIMESTAMP", mode="REQUIRED", description="Data e hora UTC do upload do arquivo pelo cliente/sistema"),
            bigquery.SchemaField("data_inicio_processamento", "TIMESTAMP", mode="NULLABLE", description="Data e hora UTC do início do processamento da folha"),
            bigquery.SchemaField("data_fim_processamento", "TIMESTAMP", mode="NULLABLE", description="Data e hora UTC da conclusão ou erro final do processamento"),
            bigquery.SchemaField("nome_arquivo_original", "STRING", mode="NULLABLE", description="Nome do arquivo original enviado pelo cliente"),
            bigquery.SchemaField("hash_arquivo", "STRING", mode="NULLABLE", description="Hash (ex: SHA256) do arquivo original para detecção de duplicatas e integridade"),
            bigquery.SchemaField("caminho_gcs_arquivo_original", "STRING", mode="NULLABLE", description="Caminho no Google Cloud Storage do arquivo original"),
            bigquery.SchemaField("caminho_gcs_arquivo_processado", "STRING", mode="NULLABLE", description="Caminho no GCS do arquivo após conversão/limpeza inicial (se aplicável)"),
            bigquery.SchemaField("numero_linhas_arquivo", "INTEGER", mode="NULLABLE", description="Número de linhas no arquivo original (informativo)"),
            bigquery.SchemaField("numero_colaboradores_unicos", "INTEGER", mode="NULLABLE", description="Número de colaboradores únicos identificados na folha processada"),
            bigquery.SchemaField("total_proventos", "NUMERIC", mode="NULLABLE", description="Soma total de proventos da folha processada"),
            bigquery.SchemaField("total_descontos", "NUMERIC", mode="NULLABLE", description="Soma total de descontos da folha processada"),
            bigquery.SchemaField("total_liquido", "NUMERIC", mode="NULLABLE", description="Soma total líquido da folha processada"),
            bigquery.SchemaField("data_vencimento_guia_fgts", "DATE", mode="NULLABLE", description="Data de vencimento da guia FGTS (se aplicável e extraída)"),
            bigquery.SchemaField("data_vencimento_darf_inss", "DATE", mode="NULLABLE", description="Data de vencimento do DARF INSS (se aplicável e extraída)"),
            bigquery.SchemaField("data_vencimento_darf_irrf", "DATE", mode="NULLABLE", description="Data de vencimento do DARF IRRF (se aplicável e extraída)"),
            bigquery.SchemaField("observacoes_processamento", "STRING", mode="NULLABLE", description="Observações ou logs resumidos do processo de importação/validação"),
            bigquery.SchemaField("detalhes_erros_processamento", "STRING", mode="NULLABLE", description="Detalhes de erros ocorridos durante o processamento (pode ser JSON stringified)"),
            bigquery.SchemaField("usuario_responsavel_upload", "STRING", mode="NULLABLE", description="Identificador do usuário ou sistema que realizou o upload"),
            bigquery.SchemaField("id_job_processamento", "STRING", mode="NULLABLE", description="ID do job ou tarefa que processou esta folha (para rastreabilidade)"),
            bigquery.SchemaField("data_criacao_registro", "TIMESTAMP", mode="REQUIRED", description="Data e hora UTC da criação deste registro na tabela de controle"),
            bigquery.SchemaField("data_ultima_atualizacao_registro", "TIMESTAMP", mode="REQUIRED", description="Data e hora UTC da última atualização deste registro")
        ]

    def _ensure_controle_table_exists(self):
        if not self.client or not self.project_id or not self.dataset_id:
            raise ConnectionError("Cliente BigQuery, project_id ou dataset_id não configurados corretamente.")
        
        ensure_dataset_exists(self.dataset_id, self.project_id, self.client)
        ensure_table_exists_or_updated(self.full_table_id, self._get_controle_folha_schema(), self.client)

    def inserir_folha(self, dados_folha: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        if not self.client:
            logger.error("Cliente BigQuery não inicializado em inserir_folha.")
            return [{"message": "Cliente BigQuery não inicializado."}]

        now_utc = datetime.now(timezone.utc)
        row_to_insert = dados_folha.copy()
        row_to_insert.setdefault("id_folha", str(uuid.uuid4()))
        row_to_insert.setdefault("status_processamento", "PENDENTE")
        row_to_insert["data_criacao_registro"] = now_utc
        row_to_insert["data_ultima_atualizacao_registro"] = now_utc

        for key, value in row_to_insert.items():
            if isinstance(value, datetime):
                row_to_insert[key] = value.isoformat()
            elif isinstance(value, date):
                row_to_insert[key] = value.isoformat()

        logger.debug(f"Tentando inserir linha na tabela {self.full_table_id}: {row_to_insert}")
        try:
            errors_bq: Sequence[Dict[str, Any]] = self.client.insert_rows_json(self.full_table_id, [row_to_insert])
            if not errors_bq:
                logger.info(f"Registro de folha {row_to_insert['id_folha']} inserido com sucesso em {self.full_table_id}.")
                return None
            else:
                # Convertendo para o tipo esperado explicitamente
                error_list: List[Dict[str, Any]] = list(errors_bq) 
                logger.error(f"Erro ao inserir registro de folha em {self.full_table_id}: {error_list}")
                return error_list
        except google_exceptions.GoogleCloudError as e:
            logger.error(f"Erro do Google Cloud ao inserir dados na tabela {self.full_table_id}: {e}", exc_info=True)
            return [{ "message": f"Erro do Google Cloud: {str(e)}"}]
        except Exception as e:
            logger.error(f"Erro inesperado ao inserir dados na tabela {self.full_table_id}: {e}", exc_info=True)
            return [{ "message": f"Erro inesperado: {str(e)}"}]

    def atualizar_status_folha(self, id_folha: str, novo_status: str, detalhes_adicionais: Optional[Dict[str, Any]] = None) -> Optional[List[Dict[str, Any]]]:
        if not self.client:
            logger.error("Cliente BigQuery não inicializado em atualizar_status_folha.")
            return [{"message": "Cliente BigQuery não inicializado."}]

        now_utc_iso = datetime.now(timezone.utc).isoformat()
        set_clauses = ["status_processamento = @novo_status", "data_ultima_atualizacao_registro = @timestamp_atualizacao"]
        query_params = [
            bigquery.ScalarQueryParameter("id_folha_param", "STRING", id_folha),
            bigquery.ScalarQueryParameter("novo_status", "STRING", novo_status),
            bigquery.ScalarQueryParameter("timestamp_atualizacao", "TIMESTAMP", now_utc_iso),
        ]

        if detalhes_adicionais:
            for key, value in detalhes_adicionais.items():
                param_name = f"param_{key}"
                set_clauses.append(f"{key} = @{param_name}")
                param_type = "STRING"
                if isinstance(value, bool): param_type = "BOOL"
                elif isinstance(value, int): param_type = "INT64"
                elif isinstance(value, float): param_type = "FLOAT64"
                elif isinstance(value, datetime): 
                    param_type = "TIMESTAMP"; value = value.isoformat()
                elif isinstance(value, date): 
                    param_type = "DATE"; value = value.isoformat()
                query_params.append(bigquery.ScalarQueryParameter(param_name, param_type, value))

        query = f"UPDATE `{self.full_table_id}` SET {', '.join(set_clauses)} WHERE id_folha = @id_folha_param"
        logger.debug(f"Executando atualização na tabela {self.full_table_id} para id_folha {id_folha}. Query: {query}")
        job_config = bigquery.QueryJobConfig(query_parameters=query_params)
        try:
            query_job = self.client.query(query, job_config=job_config)
            query_job.result()
            if query_job.errors:
                error_list_update: List[Dict[str, Any]] = list(cast(Sequence[Dict[str,Any]], query_job.errors))
                logger.error(f"Erro ao executar query de atualização para folha {id_folha}: {error_list_update}")
                return error_list_update
            if query_job.num_dml_affected_rows is not None and query_job.num_dml_affected_rows > 0:
                logger.info(f"Status da folha {id_folha} atualizado. Linhas afetadas: {query_job.num_dml_affected_rows}")
                return None
            else:
                logger.warning(f"Nenhuma linha atualizada para folha {id_folha}. A folha pode não existir.")
                return [{"message": f"Nenhuma linha afetada para id_folha {id_folha}."}]
        except google_exceptions.GoogleCloudError as e:
            logger.error(f"Erro Google Cloud ao atualizar folha {id_folha}: {e}", exc_info=True)
            return [{ "message": f"Erro Google Cloud: {str(e)}"}]
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar folha {id_folha}: {e}", exc_info=True)
            return [{ "message": f"Erro inesperado: {str(e)}"}]

# Funções utilitárias genéricas para BigQuery (fora da classe)
def load_data_to_bq(data: List[Dict[str, Any]], 
                      full_table_id: str, 
                      client: bigquery.Client, 
                      schema: Optional[List[bigquery.SchemaField]] = None, 
                      write_disposition: str = "WRITE_APPEND",
                      create_disposition: str = "CREATE_IF_NEEDED") -> Optional[List[Dict[str, Any]]]:
    if not client:
        logger.error("Cliente BigQuery não fornecido para load_data_to_bq.")
        return [{"message": "Cliente BigQuery não fornecido."}]
    if not data:
        logger.info("Nenhum dado fornecido para carregar no BigQuery.")
        return None

    job_config = bigquery.LoadJobConfig(
        schema=schema if schema else [], # Passar lista vazia se None para evitar erro de tipo
        autodetect=True if not schema else False, # Autodetectar apenas se schema não for fornecido
        write_disposition=write_disposition,
        create_disposition=create_disposition,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )
    logger.info(f"Iniciando carregamento de {len(data)} linhas para {full_table_id}...")
    try:
        load_job = client.load_table_from_json(data, full_table_id, job_config=job_config)
        load_job.result()
        if load_job.errors:
            error_list_load: List[Dict[str, Any]] = list(cast(Sequence[Dict[str,Any]], load_job.errors))
            logger.error(f"Erro durante o carregamento para {full_table_id}: {error_list_load}")
            return error_list_load
        else:
            logger.info(f"Dados carregados para {full_table_id}. Linhas: {load_job.output_rows}")
            return None
    except google_exceptions.GoogleCloudError as e:
        logger.error(f"Erro Google Cloud ao carregar para {full_table_id}: {e}", exc_info=True)
        return [{ "message": f"Erro Google Cloud: {str(e)}"}]
    except Exception as e:
        logger.error(f"Erro inesperado ao carregar para {full_table_id}: {e}", exc_info=True)
        return [{ "message": f"Erro inesperado: {str(e)}"}]

def ensure_dataset_exists(dataset_id: str, project_id: str, client: bigquery.Client, location: str = "US") -> Optional[bigquery.Dataset]:
    if not client:
        logger.error("Cliente BigQuery não fornecido para ensure_dataset_exists.")
        return None
    if not project_id:
        logger.error("Project_id não fornecido para ensure_dataset_exists.")
        return None 

    full_dataset_id = f"{project_id}.{dataset_id}"
    dataset_ref = client.dataset(dataset_id, project=project_id)
    try:
        dataset = client.get_dataset(dataset_ref)
        logger.info(f"Dataset {full_dataset_id} já existe em {dataset.location}.")
        return dataset
    except google_exceptions.NotFound:
        logger.info(f"Dataset {full_dataset_id} não encontrado. Criando em {location}...")
        dataset_obj = bigquery.Dataset(dataset_ref); dataset_obj.location = location
        try:
            created_dataset = client.create_dataset(dataset_obj, timeout=30)
            logger.info(f"Dataset {full_dataset_id} criado em {location}.")
            return created_dataset
        except google_exceptions.GoogleCloudError as e:
            logger.error(f"Falha ao criar dataset {full_dataset_id}: {e}", exc_info=True); return None
        except Exception as e:
            logger.error(f"Erro genérico ao criar dataset {full_dataset_id}: {e}", exc_info=True); return None
    except google_exceptions.GoogleCloudError as e:
        logger.error(f"Erro Google Cloud ao verificar dataset {full_dataset_id}: {e}", exc_info=True); return None
    except Exception as e:
        logger.error(f"Erro desconhecido ao verificar dataset {full_dataset_id}: {e}", exc_info=True); return None

def ensure_table_exists_or_updated(full_table_id: str, 
                                     schema: List[bigquery.SchemaField], 
                                     client: bigquery.Client, 
                                     clustering_fields: Optional[List[str]] = None,
                                     time_partitioning: Optional[bigquery.TimePartitioning] = None,
                                     range_partitioning: Optional[bigquery.RangePartitioning] = None
                                     ) -> Optional[bigquery.Table]:
    if not client:
        logger.error("Cliente BigQuery não fornecido para ensure_table_exists_or_updated.")
        return None

    table = bigquery.Table(full_table_id, schema=schema)
    if time_partitioning: table.time_partitioning = time_partitioning
    if range_partitioning: table.range_partitioning = range_partitioning
    if clustering_fields: table.clustering_fields = clustering_fields

    try:
        existing_table = client.get_table(full_table_id)
        logger.info(f"Tabela {full_table_id} já existe. Verificando configuração...")
        
        needs_update = False
        # Comparar schemas pode ser complexo devido à ordem e metadados. Uma comparação simples pode falhar.
        # A biblioteca cliente do BigQuery pode lidar com isso de forma mais inteligente ao tentar atualizar.
        # Por simplicidade, verificamos se os schemas são diferentes. Para uma comparação robusta, seria necessário
        # normalizar os schemas antes de comparar (ex: converter para dicts e ordenar).
        if existing_table.schema != schema: # Esta comparação pode ser superficial
            logger.info(f"Schema da tabela {full_table_id} difere do esperado.")
            needs_update = True
        if existing_table.time_partitioning != time_partitioning:
            logger.info(f"Configuração de TimePartitioning da tabela {full_table_id} difere.")
            needs_update = True
        if existing_table.range_partitioning != range_partitioning:
            logger.info(f"Configuração de RangePartitioning da tabela {full_table_id} difere.")
            needs_update = True
        if set(existing_table.clustering_fields or []) != set(clustering_fields or []):
            logger.info(f"Configuração de ClusteringFields da tabela {full_table_id} difere.")
            needs_update = True

        if needs_update:
            logger.info(f"Tentando atualizar a configuração da tabela {full_table_id}.")
            # Passa o objeto `table` que contém todas as configurações desejadas (schema, part., cluster)
            # e especifica quais campos devem ser atualizados.
            fields_to_update = ["schema"] # Sempre tenta atualizar o schema se for diferente
            if time_partitioning is not None or existing_table.time_partitioning is not None: # Se um deles está definido
                fields_to_update.append("time_partitioning")
            if range_partitioning is not None or existing_table.range_partitioning is not None:
                fields_to_update.append("range_partitioning")
            if clustering_fields is not None or existing_table.clustering_fields is not None:
                 fields_to_update.append("clustering_fields")
            
            updated_table = client.update_table(table, fields=fields_to_update)
            logger.info(f"Tabela {full_table_id} atualizada com sucesso.")
            return updated_table
        else:
            logger.info(f"Tabela {full_table_id} está com a configuração atualizada.")
            return existing_table
    except google_exceptions.NotFound:
        logger.info(f"Tabela {full_table_id} não encontrada. Tentando criar...")
        try:
            created_table = client.create_table(table)
            logger.info(f"Tabela {full_table_id} criada com sucesso.")
            return created_table
        except google_exceptions.GoogleCloudError as e:
            logger.error(f"Falha ao criar tabela {full_table_id}: {e}", exc_info=True); return None
        except Exception as e:
            logger.error(f"Erro genérico ao criar tabela {full_table_id}: {e}", exc_info=True); return None
    except google_exceptions.GoogleCloudError as e:
        logger.error(f"Erro Google Cloud ao acessar/atualizar {full_table_id}: {e}", exc_info=True); return None
    except Exception as e:
        logger.error(f"Erro desconhecido ao acessar/atualizar {full_table_id}: {e}", exc_info=True); return None
