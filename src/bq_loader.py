# filepath: src/bq_loader.py
import json
import logging
import os
from datetime import datetime, timezone
from google.cloud import bigquery
from google.oauth2 import service_account

# Configuração de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# --- Carregar Configurações ---
_global_config = {}
try:
    SCRIPT_DIR_BQ = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE_PATH_BQ = os.path.join(SCRIPT_DIR_BQ, "config.json")
    logging.info(f"BQ_Loader tentando carregar config de: {CONFIG_FILE_PATH_BQ}")
    if os.path.exists(CONFIG_FILE_PATH_BQ):
        with open(CONFIG_FILE_PATH_BQ, 'r') as f:
            _global_config = json.load(f)
        logging.info(f"Configurações do BigQuery carregadas de '{CONFIG_FILE_PATH_BQ}' (para _global_config)")
    else:
        logging.warning(f"Arquivo de configuração '{CONFIG_FILE_PATH_BQ}' não encontrado para bq_loader (_global_config).")
except Exception as e:
    logging.error(f"Erro ao carregar '{CONFIG_FILE_PATH_BQ}' para bq_loader (_global_config): {e}")

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
]

def get_bigquery_client(config_dict: dict | None = None):
    """Cria e retorna um cliente BigQuery."""
    cfg = config_dict if config_dict is not None else _global_config
    key_path = cfg.get("service_account_key_path_local_dev")
    project_id = cfg.get("gcp_project_id")

    if not project_id:
        logging.error("gcp_project_id não encontrado na configuração para get_bigquery_client.")
        raise ValueError("gcp_project_id é necessário.")

    try:
        if key_path:
            logging.info(f"Criando cliente BigQuery usando chave local: {key_path}")
            credentials = service_account.Credentials.from_service_account_file(key_path)
            client = bigquery.Client(credentials=credentials, project=project_id)
        else:
            logging.info("Criando cliente BigQuery usando Application Default Credentials (ADC).")
            client = bigquery.Client(project=project_id)
        logging.info("Cliente BigQuery criado com sucesso.")
        return client
    except Exception as e:
        logging.error(f"Falha ao criar cliente BigQuery: {e}", exc_info=True)
        raise

def create_dataset_if_not_exists(client: bigquery.Client, dataset_id: str, location: str):
    """Cria o dataset no BigQuery se ele não existir."""
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
        logging.info(f"Dataset '{dataset_id}' já existe.")
    except Exception:
        logging.info(f"Dataset '{dataset_id}' não encontrado. Criando...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location
        client.create_dataset(dataset, timeout=30)
        logging.info(f"Dataset '{dataset_id}' criado em '{location}'.")

def create_or_update_table(client: bigquery.Client, dataset_id: str, table_id: str, schema: list):
    """Cria ou atualiza a tabela no BigQuery com o schema especificado."""
    table_ref = client.dataset(dataset_id).table(table_id)
    try:
        client.get_table(table_ref)
        logging.info(f"Tabela '{dataset_id}.{table_id}' já existe.")
    except Exception:
        logging.info(f"Tabela '{dataset_id}.{table_id}' não encontrada. Criando...")
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        logging.info(f"Tabela '{dataset_id}.{table_id}' criada.")

def load_data_to_bigquery(data: list[dict], config: dict):
    """
    Carrega uma lista de dicionários (registros) para a tabela BigQuery especificada na configuração.

    Args:
        data: Lista de dicionários, onde cada dicionário representa uma linha.
        config: Dicionário de configuração obrigatório.
    """
    if not data:
        logging.warning("Nenhum dado fornecido para carregar no BigQuery.")
        return

    if not config:
        logging.error("Configuração não fornecida para load_data_to_bigquery.")
        raise ValueError("O argumento 'config' é obrigatório.")

    try:
        project_id = config["gcp_project_id"]
        dataset_id = config["bq_dataset_id"]
        table_id = config["bq_table_id"]
        location = config["gcp_location"]
    except KeyError as e:
        logging.error(f"Chave de configuração ausente para BigQuery em 'config': {e}")
        raise ValueError(f"Configuração do BigQuery (passada) incompleta: falta {e}")

    client = get_bigquery_client(config)
    full_table_id = f"{project_id}.{dataset_id}.{table_id}"

    try:
        create_dataset_if_not_exists(client, dataset_id, location)
        create_or_update_table(client, dataset_id, table_id, TABLE_SCHEMA)

        timestamp_agora_iso = datetime.now(timezone.utc).isoformat()
        for row in data:
            row['timestamp_carga'] = timestamp_agora_iso

        job_config = bigquery.LoadJobConfig(
            schema=TABLE_SCHEMA,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        logging.info(f"Iniciando carregamento de {len(data)} registros para '{full_table_id}'...")
        load_job = client.load_table_from_json(
            data,
            full_table_id,
            job_config=job_config
        )
        load_job.result()

        if load_job.errors:
            logging.error(f"Erro ao carregar dados para '{full_table_id}': {load_job.errors}")
            raise RuntimeError(f"Erro no job de carregamento do BigQuery: {load_job.errors}")
        else:
            logging.info(f"Carregamento concluído com sucesso. {load_job.output_rows} linhas carregadas para '{full_table_id}'.")
    except Exception as e:
        logging.error(f"Erro durante o processo de carregamento para BigQuery '{full_table_id}': {e}", exc_info=True)
        raise

# Bloco de teste (opcional, para testar o loader isoladamente se necessário)
if __name__ == "__main__":
    logging.info("Executando bq_loader.py como script principal (modo de teste).")

    sample_data = [
        {'id_extracao': 'docai_test_123', 'id_item': 'item_1', 'nome_arquivo_origem': 'test.pdf', 'pagina': 1, 'tipo_campo': 'SALARIO', 'texto_extraido': '1.000,00', 'valor_limpo': '1.000,00', 'valor_numerico': 1000.0, 'confianca': 0.99},
        {'id_extracao': 'docai_test_123', 'id_item': 'item_2', 'nome_arquivo_origem': 'test.pdf', 'pagina': 1, 'tipo_campo': 'INSS', 'texto_extraido': '100,00 D', 'valor_limpo': '100,00', 'valor_numerico': -100.0, 'confianca': 0.98},
        {'id_extracao': 'docai_test_123', 'id_item': 'item_3', 'nome_arquivo_origem': 'test.pdf', 'pagina': 1, 'tipo_campo': 'NOME_FUNC', 'texto_extraido': 'Fulano Teste', 'valor_limpo': 'Fulano Teste', 'valor_numerico': None, 'confianca': 0.95},
    ]

    try:
        load_data_to_bigquery(sample_data, _global_config)
        print("Teste de carregamento no BigQuery concluído com sucesso (verifique o BQ).")
    except Exception as e:
        print(f"Teste de carregamento no BigQuery falhou: {e}")
