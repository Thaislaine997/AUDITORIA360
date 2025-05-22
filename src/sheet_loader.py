import os
import pandas as pd
from google.cloud import storage, bigquery
from datetime import datetime, timezone  # Modificado para incluir timezone
import logging
import json  # Adicionado para carregar config.json
import sys  # Adicionado para argumentos de linha de comando

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

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
bq_client_global = None

def get_storage_client():
    global storage_client_global
    if storage_client_global is None:
        storage_client_global = storage.Client()
    return storage_client_global

def get_bq_client():
    global bq_client_global
    if bq_client_global is None:
        bq_client_global = bigquery.Client(project=BQ_PROJECT if BQ_PROJECT else None)
    return bq_client_global

def process_control_sheet(file_name: str, bucket_name: str, config_override: dict | None = None):
    """
    Processa uma planilha de controle do GCS, transforma os dados e os ingere no BigQuery.
    """
    config_override = config_override or {}
    config = get_sheet_loader_config(config_override)
    gcs_control_bucket = config.get("GCS_CONTROL_BUCKET")
    bq_project = config.get("BQ_PROJECT")
    bq_dataset = config.get("BQ_DATASET")
    bq_table_sheet_data = config.get("BQ_TABLE_SHEET_DATA")

    if not all([gcs_control_bucket, bq_project, bq_dataset, bq_table_sheet_data]):
        logger.error("Uma ou mais configurações essenciais (GCS_CONTROL_BUCKET, BQ_PROJECT, BQ_DATASET, BQ_TABLE_SHEET_DATA) não estão definidas. Abortando.")
        return

    # Valida se o bucket_name fornecido é o esperado (GCS_CONTROL_BUCKET)
    if bucket_name != gcs_control_bucket:
        logger.error(f"Bucket fornecido '{bucket_name}' é diferente do configurado GCS_CONTROL_BUCKET '{gcs_control_bucket}'. Abortando.")
        return

    s_client = get_storage_client()
    b_client = get_bq_client()
    local_path = None  # Definir local_path para garantir que exista no bloco finally/except

    try:
        bucket = s_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        if not blob.exists(s_client):  # Passar o cliente é opcional para blob.exists()
            logger.error(f"Arquivo {file_name} não encontrado no bucket {bucket_name}.")
            return

        # Garante que /tmp exista (relevante para alguns ambientes, boa prática)
        temp_dir = '/tmp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
        local_path = os.path.join(temp_dir, os.path.basename(file_name))

        blob.download_to_filename(local_path)
        logger.info(f"Arquivo {file_name} baixado para {local_path}")

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
        
        # Converter explicitamente cnpj_empresa para string para evitar problemas de tipo
        full_df['cnpj_empresa'] = full_df['cnpj_empresa'].astype(str)
        full_df['status_valor_cliente'] = full_df['status_valor_cliente'].astype(str)

        if full_df.empty:
            logger.info(f"Nenhum registro válido para ingestão após o processamento de {file_name}.")
            return  # local_path será removido no finally

        # Ajustar mes_ano_referencia para None se for pd.NaT ou NaN antes de converter para dict
        full_df['mes_ano_referencia'] = full_df['mes_ano_referencia'].apply(lambda x: None if pd.isna(x) else x)

        table_ref_str = f"{bq_project}.{bq_dataset}.{bq_table_sheet_data}"
        
        schema = [
            bigquery.SchemaField("cnpj_empresa", "STRING"),
            bigquery.SchemaField("status_valor_cliente", "STRING"),
            bigquery.SchemaField("status_aba_origem", "STRING"),
            bigquery.SchemaField("mes_ano_referencia", "DATE"), # BigQuery pode converter string 'YYYY-MM-DD' para DATE
            bigquery.SchemaField("data_processamento_gcs", "TIMESTAMP"), # BigQuery pode converter string ISO8601 para TIMESTAMP
            bigquery.SchemaField("nome_arquivo_origem", "STRING"),
        ]
        job_config = bigquery.LoadJobConfig(
            schema=schema, # Fornecer o schema é mais robusto
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        logger.info(f"Iniciando carregamento de {len(full_df)} linhas para {table_ref_str} usando load_table_from_dataframe.")
        load_job = b_client.load_table_from_dataframe(full_df, table_ref_str, job_config=job_config)
        load_job.result() # Espera o job completar

        if not load_job.errors:
            logger.info(f"Ingeridos {load_job.output_rows} registros de {file_name} para {table_ref_str} usando load_table_from_dataframe.")
            
            # Chamar a consolidação
            try:
                from .bq_loader import ControleFolhaLoader # Importar aqui para evitar dependência circular no nível do módulo se bq_loader importar sheet_loader
                gcp_project_id = bq_project
                control_bq_dataset_id = bq_dataset
                # Verifica se as variáveis essenciais não são None
                if not gcp_project_id or not control_bq_dataset_id:
                    logger.error("GCP_PROJECT_ID ou CONTROL_BQ_DATASET_ID não definidos. Não é possível instanciar ControleFolhaLoader.")
                else:
                    config_loader = {
                        "gcp_project_id": str(gcp_project_id),
                        "control_bq_dataset_id": str(control_bq_dataset_id),
                        "client_id": config.get("client_id", "default_client")
                    }
                    controle_loader = ControleFolhaLoader(config_loader)
                    
                    logger.info(f"Iniciando consolidação dos dados da planilha '{file_name}' para a tabela 'folhas'.")
                    sucesso_consolidacao = controle_loader.consolidar_dados_planilha_para_folhas(nome_arquivo_origem_especifico=file_name)
                    if sucesso_consolidacao:
                        logger.info(f"Consolidação para 'folhas' a partir de '{file_name}' bem-sucedida.")
                    else:
                        logger.error(f"Falha na consolidação para 'folhas' a partir de '{file_name}'.")
            except Exception as e_consolid:
                logger.exception(f"Erro ao tentar consolidar dados da planilha '{file_name}' para 'folhas': {e_consolid}")
        else:
            logger.error(f"Erros ao ingerir dados de {file_name} para {table_ref_str} usando load_table_from_dataframe: {load_job.errors}")

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

if __name__ == "__main__":
    logger.info("--- INÍCIO DA EXECUÇÃO LOCAL DO SCRIPT (sheet_loader.py) ---")
    if len(sys.argv) > 1:
        file_to_process = sys.argv[1]
        
        if not GCS_CONTROL_BUCKET:
            logger.error("GCS_CONTROL_BUCKET não definido na configuração. Não é possível executar o processamento.")
        else:
            logger.info(f"Processando arquivo específico: {file_to_process} do bucket {GCS_CONTROL_BUCKET}")
            process_control_sheet(file_name=file_to_process, bucket_name=GCS_CONTROL_BUCKET)
    else:
        logger.warning("Nenhum nome de arquivo fornecido. Uso: python -m src.sheet_loader <nome_do_arquivo.xlsx>")
    logger.info("--- FIM DA EXECUÇÃO LOCAL DO SCRIPT (sheet_loader.py) ---")