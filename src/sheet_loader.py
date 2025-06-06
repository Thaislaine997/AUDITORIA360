import os
import pandas as pd
from google.cloud import storage, bigquery
from google.cloud.exceptions import GoogleCloudError, NotFound, ServiceUnavailable # Adicionado para tenacity
from datetime import datetime, timezone
import logging
import json
import sys
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, RetryCallState # Adicionado RetryCallState

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

# Tenacity retry configuration
RETRY_WAIT_SECONDS = 5
RETRY_MAX_ATTEMPTS = 3

def get_sheet_loader_config(config_override: dict | None = None) -> dict:
    config_override = config_override or {}
    config_values = {}
    config_keys_map = {
        "GCS_CONTROL_BUCKET": "gcs_control_bucket",
        "BQ_PROJECT": "gcp_project_id",
        "BQ_DATASET": "control_bq_dataset_id",
        "BQ_TABLE_SHEET_DATA": "control_sheet_data_table_id"
    }
    for env_var, json_key in config_keys_map.items():
        config_values[env_var] = os.environ.get(env_var)
    if not all(config_values.values()):
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_FILE_PATH = os.path.join(SCRIPT_DIR, "config.json")
        try:
            if os.path.exists(CONFIG_FILE_PATH):
                with open(CONFIG_FILE_PATH, 'r') as f:
                    json_config = json.load(f)
                for env_var, json_key in config_keys_map.items():
                    config_values[env_var] = config_values[env_var] or json_config.get(json_key)
        except Exception:
            pass
    if config_override:
        config_values.update(config_override)
    return config_values

# --- Carregar Configurações (Prioriza Variáveis de Ambiente) ---
config_values = get_sheet_loader_config()

GCS_CONTROL_BUCKET = config_values.get("GCS_CONTROL_BUCKET")
BQ_PROJECT = config_values.get("BQ_PROJECT")
BQ_DATASET = config_values.get("BQ_DATASET")
BQ_TABLE_SHEET_DATA = config_values.get("BQ_TABLE_SHEET_DATA")

if not all([GCS_CONTROL_BUCKET, BQ_PROJECT, BQ_DATASET, BQ_TABLE_SHEET_DATA]):
    missing_vars = [k for k, v in config_values.items() if not v]
    logger.error(f"Configurações essenciais para sheet_loader não encontradas (via Env Vars ou config.json): {missing_vars}")
    # Não levantar exceção aqui para permitir importação, mas process_control_sheet irá falhar.

# Inicialização dos clientes
storage_client_global = None

def get_storage_client():
    global storage_client_global
    if storage_client_global is None:
        storage_client_global = storage.Client()
    return storage_client_global

def get_bq_client(project_id: str | None = None) -> bigquery.Client:
    """Cria e retorna um cliente BigQuery.

    Args:
        project_id: O ID do projeto GCP. Se None, tentará usar o padrão do ambiente.
    """
    try:
        # Usa o project_id fornecido, ou o BQ_PROJECT da configuração global se project_id for None
        # Ou permite que o cliente BigQuery descubra o projeto se ambos forem None.
        effective_project_id = project_id if project_id else BQ_PROJECT
        logger.info(f"Criando cliente BigQuery para o projeto: {effective_project_id if effective_project_id else 'Padrão do Ambiente'}.")
        client = bigquery.Client(project=effective_project_id)
        logger.info("Cliente BigQuery criado com sucesso.")
        return client
    except Exception as e:
        logger.error(f"Falha ao criar cliente BigQuery: {e}", exc_info=True)
        raise

def process_control_sheet(
    file_name: str, 
    bucket_name: str, 
    config_override: dict | None = None,
    bq_client_injected: bigquery.Client | None = None
):
    """
    Processa uma planilha de controle do GCS, transforma os dados e os ingere no BigQuery.
    """
    config_override = config_override or {}
    current_config = get_sheet_loader_config(config_override)
    
    gcs_control_bucket_from_config = current_config.get("GCS_CONTROL_BUCKET")
    bq_project_from_config = current_config.get("BQ_PROJECT")
    bq_dataset_from_config = current_config.get("BQ_DATASET")
    bq_table_sheet_data_from_config = current_config.get("BQ_TABLE_SHEET_DATA")
    client_id_from_config = current_config.get("client_id", "sheet_loader_default_client")

    if not all([gcs_control_bucket_from_config, bq_project_from_config, bq_dataset_from_config, bq_table_sheet_data_from_config]):
        logger.error("Uma ou mais configurações essenciais (GCS_CONTROL_BUCKET, BQ_PROJECT, BQ_DATASET, BQ_TABLE_SHEET_DATA) não estão definidas na configuração atual. Abortando.")
        return

    if bucket_name != gcs_control_bucket_from_config:
        logger.error(f"Bucket fornecido \'{bucket_name}\' é diferente do configurado GCS_CONTROL_BUCKET \'{gcs_control_bucket_from_config}\'. Abortando.")
        return

    s_client = get_storage_client()
    
    bq_client_to_use: bigquery.Client
    internal_bq_client_created = False
    if bq_client_injected:
        bq_client_to_use = bq_client_injected
        logger.info("Usando cliente BigQuery injetado.")
    else:
        logger.info("Cliente BigQuery não injetado. Criando um novo cliente.")
        try:
            bq_client_to_use = get_bq_client(project_id=bq_project_from_config)
            internal_bq_client_created = True
        except Exception as e_bq_create:
            logger.error(f"Falha ao criar cliente BigQuery internamente para process_control_sheet: {e_bq_create}", exc_info=True)
            return

    local_path = None

    try:
        bucket = s_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        if not blob.exists(s_client):
            logger.error(f"Arquivo {file_name} não encontrado no bucket {bucket_name}.")
            return

        temp_dir = '/tmp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
        local_path = os.path.join(temp_dir, os.path.basename(file_name))

        @retry(
            wait=wait_fixed(RETRY_WAIT_SECONDS),
            stop=stop_after_attempt(RETRY_MAX_ATTEMPTS),
            retry=retry_if_exception_type((GoogleCloudError, ServiceUnavailable)),
            reraise=True
        )
        def download_with_retry(retry_state):
            logger.info(f"Tentando baixar {file_name} para {local_path} (tentativa: {retry_state.attempt_number})...")
            blob.download_to_filename(local_path)
            logger.info(f"Arquivo {file_name} baixado com sucesso para {local_path}.")

        download_with_retry(None) # Pode remover type: ignore se o linter/type checker estiver satisfeito

        xls = pd.read_excel(local_path, sheet_name=None)
        all_records_df_list = []

        file_base_name = os.path.splitext(os.path.basename(file_name))[0]
        mes_ano_str = None
        try:
            # Tenta MM-YYYY ou YYYY-MM
            parsed_date = None
            try:
                parsed_date = pd.to_datetime(file_base_name, format='%m-%Y').to_pydatetime().date()
            except ValueError:
                parsed_date = pd.to_datetime(file_base_name, format='%Y-%m').to_pydatetime().date()
            
            mes_ano_str = parsed_date.replace(day=1).strftime('%Y-%m-%d')
            logger.info(f"Extraído mes_ano '{mes_ano_str}' do nome do arquivo '{file_name}'.")
        except ValueError:
            logger.warning(f"Não foi possível extrair mes_ano (formato MM-YYYY ou YYYY-MM) do nome do arquivo '{file_name}'. 'mes_ano_referencia' será nulo.")

        for sheet_name, df in xls.items():
            if df.empty:
                logger.warning(f"Planilha '{file_name}', aba '{sheet_name}' está vazia e será ignorada.")
                continue
            if df.columns.empty:
                logger.warning(f"Planilha '{file_name}', aba '{sheet_name}' ignorada: sem colunas válidas.")
                continue

            df_long = df.melt(var_name='cnpj_empresa', value_name='status_valor_cliente')
            df_long['status_aba_origem'] = sheet_name
            df_long['mes_ano_referencia'] = mes_ano_str
            df_long['data_processamento_gcs'] = datetime.now(timezone.utc).isoformat()  # CORRIGIDO
            df_long['nome_arquivo_origem'] = file_name
            
            all_records_df_list.append(df_long)

        if not all_records_df_list:
            logger.warning(f"Nenhuma aba processável ou com dados encontrada em {file_name}.")
            return  # local_path será removido no finally

        full_df = pd.concat(all_records_df_list, ignore_index=True)
        full_df.dropna(subset=['cnpj_empresa', 'status_valor_cliente'], inplace=True)
        
        full_df['cnpj_empresa'] = full_df['cnpj_empresa'].astype(str)
        full_df['status_valor_cliente'] = full_df['status_valor_cliente'].astype(str)
        # Adicionar client_id ao DataFrame antes de carregar no BQ.
        full_df['client_id'] = client_id_from_config

        if full_df.empty:
            logger.info(f"Nenhum registro válido para ingestão após o processamento de {file_name}.")
            return  # local_path será removido no finally

        # Ajustar mes_ano_referencia para None se for pd.NaT ou NaN antes de converter para dict
        full_df['mes_ano_referencia'] = full_df['mes_ano_referencia'].apply(lambda x: None if pd.isna(x) else x)

        table_ref_str = f"{bq_project_from_config}.{bq_dataset_from_config}.{bq_table_sheet_data_from_config}"
        
        schema = [
            bigquery.SchemaField("cnpj_empresa", "STRING"),
            bigquery.SchemaField("status_valor_cliente", "STRING"),
            bigquery.SchemaField("status_aba_origem", "STRING"),
            bigquery.SchemaField("mes_ano_referencia", "DATE"),
            bigquery.SchemaField("data_processamento_gcs", "TIMESTAMP"),
            bigquery.SchemaField("nome_arquivo_origem", "STRING"),
            bigquery.SchemaField("client_id", "STRING"),
        ]
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        @retry(
            wait=wait_fixed(RETRY_WAIT_SECONDS),
            stop=stop_after_attempt(RETRY_MAX_ATTEMPTS),
            retry=retry_if_exception_type((GoogleCloudError, ServiceUnavailable)),
            reraise=True
        )
        def load_to_bq_with_retry(*args, **kwargs):
            logger.info(f"Tentando carregar DataFrame para BigQuery {table_ref_str} (tentativa: {getattr(kwargs.get('retry_state', None), 'attempt_number', 1)})...")
            job = bq_client_to_use.load_table_from_dataframe(full_df, table_ref_str, job_config=job_config)
            job.result() # Espera o job completar e levanta exceção em caso de erro
            logger.info(f"Dados carregados com sucesso para BigQuery. Linhas de saída: {job.output_rows}.")
            return job

        logger.info(f"Iniciando carregamento de {len(full_df)} linhas para {table_ref_str} usando load_table_from_dataframe.")
        load_job = None 
        try:
            load_job = load_to_bq_with_retry() # Corrigido: chamada sem argumentos
        except Exception as e_load_bq:
            logger.error(f"Falha ao carregar dados para BigQuery após {RETRY_MAX_ATTEMPTS} tentativas: {e_load_bq}", exc_info=True)
            # Não retorna aqui, permite que o finally seja executado

        if load_job and not load_job.errors:
            logger.info(f"Ingeridos {load_job.output_rows} registros de {file_name} para {table_ref_str}.")
            
            if not isinstance(bq_table_sheet_data_from_config, str) or not bq_table_sheet_data_from_config.strip():
                logger.error(f"[{client_id_from_config}] ID da tabela de dados de controle (BQ_TABLE_SHEET_DATA) é inválido ou não configurado: \'{bq_table_sheet_data_from_config}\'. Não é possível processar para a tabela \'folhas\'.")
            else:
                try:
                    from .bq_loader import ControleFolhaLoader
                    
                    config_for_loader = {
                        "gcp_project_id": bq_project_from_config,
                        "control_bq_dataset_id": bq_dataset_from_config,
                        "client_id": client_id_from_config,
                        "control_folhas_table_id": current_config.get("control_folhas_table_id", "folhas"),
                        "control_empresas_table_id": current_config.get("control_empresas_table_id", "empresas"),
                        "control_raw_data_table_id": current_config.get("control_raw_data_table_id", "controle_folha_raw_data")
                    }

                    logger.info(f"Instanciando ControleFolhaLoader com config: {config_for_loader} e client_id: {client_id_from_config}")
                    controle_loader = ControleFolhaLoader(config=config_for_loader)
                    
                    logger.info(f"[{client_id_from_config}] Iniciando processamento dos dados de controle do arquivo \'{file_name}\' para a tabela \'folhas\'.")
                    resultado_processamento = controle_loader.processar_dados_controle_para_folhas(
                        nome_arquivo_origem_controle=file_name, 
                        tabela_dados_controle_id=bq_table_sheet_data_from_config
                    )
                    logger.info(f"[{client_id_from_config}] Processamento de dados de controle para \'{file_name}\' concluído: {resultado_processamento}")

                except ImportError as ie:
                    logger.error(f"Erro de importação ao tentar carregar ControleFolhaLoader: {ie}", exc_info=True)
                except Exception as e_consolid:
                    logger.exception(f"[{client_id_from_config}] Erro ao tentar processar dados de controle da planilha \'{file_name}\' para \'folhas\': {e_consolid}")
        elif load_job and load_job.errors:
            logger.error(f"Erros ao ingerir dados de {file_name} para {table_ref_str} usando load_table_from_dataframe: {load_job.errors}")
        elif not load_job: # Se load_job ainda é None, significa que load_to_bq_with_retry falhou e a exceção foi capturada
            logger.error(f"Carregamento para BigQuery de {file_name} falhou e não produziu um objeto de job. Verifique logs anteriores para detalhes da exceção.")
        # Não há necessidade de um 'else' aqui, pois os casos (sucesso, erro no job, falha no retry) são cobertos.

    except FileNotFoundError:
        logger.error(f"Arquivo temporário {local_path} não encontrado. Pode já ter sido removido.")
    except Exception as e:
        logger.exception(f"Erro ao processar planilha {file_name} do bucket {bucket_name}: {str(e)}")
    finally:
        if local_path and os.path.exists(local_path):
            try:
                os.remove(local_path)
                logger.info(f"Arquivo temporário {local_path} removido com sucesso.")
            except OSError as e:
                logger.warning(f"Não foi possível remover o arquivo temporário {local_path}: {e}")
        
        # Se o cliente BQ foi criado internamente e não precisa mais ser usado,
        # teoricamente poderia ser fechado. No entanto, para google-cloud-bigquery,
        # o fechamento explícito não é tipicamente necessário pois gerencia conexões.
        if internal_bq_client_created:
            logger.info("Cliente BigQuery criado internamente por process_control_sheet não requer fechamento explícito.")
            # bq_client_to_use.close() # Descomentar apenas se estritamente necessário.

if __name__ == "__main__":
    logger.info("--- INÍCIO DA EXECUÇÃO LOCAL DO SCRIPT (sheet_loader.py) ---")
    
    # Carrega a configuração para a execução __main__
    # Idealmente, __main__ também teria um arquivo de configuração dedicado ou usaria env vars.
    main_config = get_sheet_loader_config()
    main_gcs_bucket = main_config.get("GCS_CONTROL_BUCKET")
    main_bq_project = main_config.get("BQ_PROJECT")
    # Adicionar client_id à configuração principal se não estiver lá, para testes
    if "client_id" not in main_config:
        main_config["client_id"] = "sheet_loader_main_test_client"

    if len(sys.argv) > 1:
        file_to_process = sys.argv[1]
        
        if not main_gcs_bucket:
            logger.error("GCS_CONTROL_BUCKET não definido na configuração. Não é possível executar o processamento.")
        elif not main_bq_project:
            logger.error("BQ_PROJECT não definido na configuração. Não é possível criar cliente BigQuery para teste.")
        else:
            logger.info(f"Processando arquivo específico: {file_to_process} do bucket {main_gcs_bucket}")
            # Criar um cliente BigQuery para o teste __main__
            bq_client_for_main = None
            try:
                logger.info(f"Criando cliente BigQuery para execução __main__ (projeto: {main_bq_project})")
                bq_client_for_main = get_bq_client(project_id=main_bq_project)
                logger.info("Cliente BigQuery para __main__ criado com sucesso.")
                
                # Passa o cliente BQ criado e a configuração carregada para process_control_sheet
                process_control_sheet(
                    file_name=file_to_process, 
                    bucket_name=main_gcs_bucket, 
                    config_override=main_config,  # Passa a configuração que pode incluir client_id, etc.
                    bq_client_injected=bq_client_for_main
                )
            except Exception as e_main_run:
                logger.error(f"Erro durante a execução __main__ com cliente BQ: {e_main_run}", exc_info=True)
            # finally:
                # if bq_client_for_main: # Fechamento não usualmente necessário
                #     logger.info("Fechando cliente BigQuery do __main__.")
                #     # bq_client_for_main.close()

    else:
        logger.warning("Nenhum nome de arquivo fornecido. Uso: python -m src.sheet_loader <nome_do_arquivo.xlsx>")
    logger.info("--- FIM DA EXECUÇÃO LOCAL DO SCRIPT (sheet_loader.py) ---")