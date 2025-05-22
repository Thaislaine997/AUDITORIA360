# filepath: src/bq_loader.py
import json
import logging
import os
from datetime import datetime, timezone
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from typing import Optional

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

# ATENÇÃO: Todas as queries e cargas DEVEM usar o filtro client_id para garantir isolamento de dados entre clientes (white-label/multi-tenant).

def get_bigquery_client(config_dict: dict):
    """Cria e retorna um cliente BigQuery usando a configuração fornecida."""
    if not config_dict:
        raise ValueError("O argumento 'config_dict' é obrigatório para get_bigquery_client.")
    key_path = config_dict.get("service_account_key_path_local_dev")
    project_id = config_dict.get("gcp_project_id")

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

    client_id = config.get("client_id")
    if not client_id:
        raise ValueError("O campo 'client_id' é obrigatório na configuração para isolamento multi-cliente.")

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
            row['client_id'] = client_id  # Garante isolamento multi-cliente

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

if __name__ == "__main__":
    logging.info("Executando bq_loader.py como script principal (modo de teste).")
    print("\n[INFO] Para testar este módulo, execute: python -m src.bq_loader (a partir da raiz do projeto)")
    try:
        from src.config_manager import config_manager, CLIENT_CONFIGS_DIR
        
        CLIENT_ID_TESTE_STANDALONE = "test_client_standalone" 
        config_teste = None
        try:
            standalone_client_config_path = os.path.join(CLIENT_CONFIGS_DIR, f"{CLIENT_ID_TESTE_STANDALONE}.json")
            
            if os.path.exists(standalone_client_config_path):
                logger.info(f"Tentando carregar configuração para o cliente de teste standalone: {CLIENT_ID_TESTE_STANDALONE} a partir de {standalone_client_config_path}")
                with open(standalone_client_config_path, 'r') as f_config_client:
                    client_specific_config = json.load(f_config_client)
                config_teste = config_manager.base_config.copy()
                config_teste.update(client_specific_config)
                config_teste["client_id"] = CLIENT_ID_TESTE_STANDALONE
            else:
                logger.warning(f"Arquivo de configuração para cliente de teste standalone '{standalone_client_config_path}' não encontrado.")
                logger.info("Usando configuração base para o teste standalone do bq_loader e adicionando client_id.")
                config_teste = config_manager.base_config.copy()
                config_teste["client_id"] = CLIENT_ID_TESTE_STANDALONE

            default_values = {
                "gcp_project_id": "default-project-for-standalone",
                "bq_dataset_id": "default_dataset_standalone",
                "bq_table_id": "default_table_standalone",
                "gcp_location": "us-central1",
                "service_account_key_path_local_dev": config_manager.base_config.get("service_account_key_path_local_dev"),
                "control_bq_dataset_id": config_manager.base_config.get("control_bq_dataset_id", "default_control_dataset")
            }
            for key, value in default_values.items():
                if key not in config_teste or not config_teste[key]:
                    config_teste[key] = value
            
            if "client_id" not in config_teste:
                config_teste["client_id"] = CLIENT_ID_TESTE_STANDALONE

        except Exception as e_config:
            logger.error(f"Erro ao tentar carregar configuração para teste standalone: {e_config}. Usando base_config com defaults.")
            config_teste = config_manager.base_config.copy()
            config_teste["client_id"] = CLIENT_ID_TESTE_STANDALONE
            default_values_fallback = {
                "gcp_project_id": "default-project-for-standalone",
                "bq_dataset_id": "default_dataset_standalone",
                "bq_table_id": "default_table_standalone",
                "gcp_location": "us-central1",
                "service_account_key_path_local_dev": config_manager.base_config.get("service_account_key_path_local_dev"),
                "control_bq_dataset_id": config_manager.base_config.get("control_bq_dataset_id", "default_control_dataset")
            }
            for key, value in default_values_fallback.items():
                if key not in config_teste or not config_teste[key]:
                    config_teste[key] = value

        if not config_teste:
            logger.error("Configuração de teste não pôde ser carregada. Teste de bq_loader não executado.")
            print("Configuração de teste não carregada, teste de carregamento no BigQuery não executado.")
        else:
            logger.info(f"Configuração para teste standalone do bq_loader: {config_teste}")
            sample_data = [
                {'id_extracao': 'docai_test_123', 'id_item': 'item_1', 'nome_arquivo_origem': 'test.pdf', 'pagina': 1, 'tipo_campo': 'SALARIO', 'texto_extraido': '1.000,00', 'valor_limpo': '1.000,00', 'valor_numerico': 1000.0, 'confianca': 0.99},
                {'id_extracao': 'docai_test_123', 'id_item': 'item_2', 'nome_arquivo_origem': 'test.pdf', 'pagina': 1, 'tipo_campo': 'INSS', 'texto_extraido': '100,00 D', 'valor_limpo': '100,00', 'valor_numerico': -100.0, 'confianca': 0.98},
                {'id_extracao': 'docai_test_123', 'id_item': 'item_3', 'nome_arquivo_origem': 'test.pdf', 'pagina': 1, 'tipo_campo': 'NOME_FUNC', 'texto_extraido': 'Fulano Teste', 'valor_limpo': 'Fulano Teste', 'valor_numerico': None, 'confianca': 0.95},
            ]
            
            required_keys_for_load = ["gcp_project_id", "bq_dataset_id", "bq_table_id", "gcp_location", "client_id"]
            missing_keys = [key for key in required_keys_for_load if key not in config_teste or not config_teste[key]]
            if missing_keys:
                logger.error(f"Configuração de teste incompleta para load_data_to_bigquery. Chaves ausentes ou vazias: {missing_keys}. Config: {config_teste}")
                print(f"Configuração de teste incompleta. Chaves ausentes ou vazias: {missing_keys}")
            else:
                import json
                load_data_to_bigquery(sample_data, config_teste)
                print("Teste de carregamento no BigQuery concluído (verifique o BQ e os logs).")

    except ImportError as ie:
        print(f"Erro de importação ao testar bq_loader.py: {ie}. Certifique-se de que o PYTHONPATH está configurado.")
    except ValueError as ve:
        print(f"Erro de valor (possivelmente configuração) ao testar bq_loader.py: {ve}")
    except Exception as e:
        print(f"Teste de carregamento no BigQuery falhou: {e}")
        logger.exception("Falha no teste standalone do bq_loader.")
