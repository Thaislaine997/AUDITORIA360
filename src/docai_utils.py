# filepath: src/docai_utils.py
import json
import logging
import uuid
import os
from datetime import datetime, timezone
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from google.cloud import storage
from google.oauth2 import service_account

from .bq_loader import load_data_to_bigquery

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

# --- Carregar Configurações (Prioriza Variáveis de Ambiente) ---
ENV_GCP_PROJECT_ID = "GCP_PROJECT_ID"
ENV_GCP_LOCATION = "GCP_LOCATION"
ENV_DOCAI_PROCESSOR_ID = "DOCAI_PROCESSOR_ID"
ENV_GCS_INPUT_BUCKET = "GCS_INPUT_BUCKET"
ENV_BQ_DATASET_ID = "BQ_DATASET_ID"
ENV_BQ_TABLE_ID = "BQ_TABLE_ID"

config = {}

config["gcp_project_id"] = os.environ.get("GCP_PROJECT_ID")
config["gcp_location"] = os.environ.get("GCP_LOCATION")
config["docai_processor_id"] = os.environ.get("DOCAI_PROCESSOR_ID")
config["gcs_input_bucket"] = os.environ.get("GCS_INPUT_BUCKET")
config["bq_dataset_id"] = os.environ.get(ENV_BQ_DATASET_ID)
config["bq_table_id"] = os.environ.get(ENV_BQ_TABLE_ID)

if not all(config.values()):
    logging.warning("Uma ou mais variáveis de ambiente essenciais não definidas. Tentando carregar de config.json...")
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE_PATH = os.path.join(SCRIPT_DIR, "config.json")
    try:
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, 'r') as f:
                json_config = json.load(f)
            logging.info(f"Carregando configurações de fallback de '{CONFIG_FILE_PATH}'.")
            config["gcp_project_id"] = config["gcp_project_id"] or json_config.get("gcp_project_id")
            config["gcp_location"] = config["gcp_location"] or json_config.get("gcp_location")
            config["docai_processor_id"] = config["docai_processor_id"] or json_config.get("docai_processor_id")
            config["gcs_input_bucket"] = config["gcs_input_bucket"] or json_config.get("gcs_input_bucket")
            config["bq_dataset_id"] = config["bq_dataset_id"] or json_config.get("bq_dataset_id")
            config["bq_table_id"] = config["bq_table_id"] or json_config.get("bq_table_id")
        else:
            logging.error(f"Arquivo de configuração '{CONFIG_FILE_PATH}' não encontrado como fallback.")
    except Exception as e:
        logging.error(f"Erro ao carregar fallback de '{CONFIG_FILE_PATH}': {e}", exc_info=True)

GCP_PROJECT_ID = config.get("gcp_project_id")
GCP_LOCATION = config.get("gcp_location")
DOCAI_PROCESSOR_ID = config.get("docai_processor_id")
GCS_INPUT_BUCKET = config.get("gcs_input_bucket")
BQ_DATASET_ID = config.get("bq_dataset_id")
BQ_TABLE_ID = config.get("bq_table_id")

if not all([GCP_PROJECT_ID, GCP_LOCATION, DOCAI_PROCESSOR_ID, GCS_INPUT_BUCKET, BQ_DATASET_ID, BQ_TABLE_ID]):
    missing_keys = [k for k, v in config.items() if k in ["gcp_project_id", "gcp_location", "docai_processor_id", "gcs_input_bucket", "bq_dataset_id", "bq_table_id"] and not v]
    logging.error(f"Configurações essenciais não encontradas (via Env Vars ou config.json): {missing_keys}")
    raise ValueError(f"Configurações essenciais ausentes: {missing_keys}")

logging.info("Configurações carregadas com sucesso.")

def get_docai_client(key_path=None):
    """Cria e retorna um cliente Document AI."""
    client_options = ClientOptions(api_endpoint=f"{GCP_LOCATION}-documentai.googleapis.com")
    try:
        if key_path:
            logging.info(f"Criando cliente Document AI usando chave local: {key_path}")
            credentials = service_account.Credentials.from_service_account_file(key_path)
            client = documentai.DocumentProcessorServiceClient(credentials=credentials, client_options=client_options)
        else:
            logging.info("Criando cliente Document AI usando Application Default Credentials (ADC).")
            client = documentai.DocumentProcessorServiceClient(client_options=client_options)
        logging.info("Cliente Document AI criado com sucesso.")
        return client
    except Exception as e:
        logging.error(f"Falha ao criar cliente Document AI: {e}", exc_info=True)
        raise

def process_document_ocr(project_id: str, location: str, processor_id: str, gcs_uri: str, mime_type: str = "application/pdf", key_path: str = None) -> documentai.Document | None:
    docai_client = get_docai_client(key_path)
    resource_name = docai_client.processor_path(project_id, location, processor_id)
    logging.info(f"Usando processador: {resource_name}")

    gcs_document = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type=mime_type)
    gcs_documents = documentai.GcsDocuments(documents=[gcs_document])
    input_config = documentai.BatchDocumentsInputConfig(gcs_documents=gcs_documents)

    logging.info(f"Processando arquivo do GCS: {gcs_uri}")
    request = documentai.ProcessRequest(
        name=resource_name,
        input_documents=input_config
    )
    try:
        logging.info("Enviando requisição para processar arquivo do GCS...")
        result = docai_client.process_document(request=request)
        logging.info("Documento processado com sucesso.")
        return result.document
    except Exception as e:
        logging.error(f"Falha ao processar documento '{gcs_uri}' com Document AI: {e}", exc_info=True)
        return None

def extract_entities_from_docai_result(document: documentai.Document, filename: str, id_extracao_run: str) -> list[dict]:
    extracted_items = []
    if not document:
        logging.warning(f"Documento nulo fornecido para extração de entidades (arquivo: {filename}).")
        return extracted_items

    logging.info(f"Iniciando extração de entidades do arquivo '{filename}'. Texto detectado: {len(document.text)} caracteres.")
    logging.info(f"Total de entidades encontradas no documento: {len(document.entities)}")

    for entity_num, entity in enumerate(document.entities):
        page_number = None
        if entity.page_anchor and entity.page_anchor.page_refs:
            page_number = entity.page_anchor.page_refs[0].page + 1

        cleaned_value = entity.mention_text.replace("R$", "").replace(".", "").replace(",", ".").strip()
        numeric_value = None
        try:
            numeric_value = float(cleaned_value)
        except ValueError:
            cleaned_value_alt = ''.join(filter(lambda x: x.isdigit() or x == '.', cleaned_value.split()[0]))
            try:
                numeric_value = float(cleaned_value_alt)
            except ValueError:
                logging.warning(f"Campo '{entity.type_}' com valor '{entity.mention_text}' não pôde ser convertido para número no arquivo '{filename}'.")

        item = {
            "id_extracao": id_extracao_run,
            "id_item": f"item_{uuid.uuid4()}",
            "nome_arquivo_origem": filename,
            "pagina": page_number,
            "tipo_campo": entity.type_,
            "texto_extraido": entity.mention_text,
            "valor_limpo": cleaned_value,
            "valor_numerico": numeric_value,
            "confianca": entity.confidence,
        }
        extracted_items.append(item)
    logging.info(f"Extração de entidades do arquivo '{filename}' concluída. {len(extracted_items)} itens extraídos.")
    return extracted_items

def list_gcs_pdfs(bucket_name: str, key_path: str = None) -> list[storage.Blob]:
    """Lista todos os arquivos PDF em um bucket GCS."""
    blobs = []
    try:
        if key_path:
            logging.info(f"Criando cliente GCS usando chave local: {key_path}")
            credentials = service_account.Credentials.from_service_account_file(key_path)
            storage_client = storage.Client(credentials=credentials, project=GCP_PROJECT_ID)
        else:
            logging.info("Criando cliente GCS usando Application Default Credentials (ADC).")
            storage_client = storage.Client(project=GCP_PROJECT_ID)

        logging.info(f"Listando arquivos PDF no bucket GCS: gs://{bucket_name}")
        bucket = storage_client.bucket(bucket_name)
        for blob in bucket.list_blobs():
            if blob.name.lower().endswith(".pdf"):
                blobs.append(blob)
        logging.info(f"Encontrados {len(blobs)} arquivos PDF no bucket.")
    except Exception as e:
        logging.error(f"Erro ao listar arquivos PDF do bucket '{bucket_name}': {e}", exc_info=True)
    return blobs

def process_gcs_pdf(bucket_name: str, file_name: str, id_execucao: str | None = None):
    if not id_execucao:
        id_execucao = f"run_{uuid.uuid4()}"

    gcs_uri = f"gs://{bucket_name}/{file_name}"
    logging.info(f"[{id_execucao}] Iniciando processamento para: {gcs_uri}")
    items_loaded_count = 0

    try:
        document_result = process_document_ocr(
            project_id=GCP_PROJECT_ID,
            location=GCP_LOCATION,
            processor_id=DOCAI_PROCESSOR_ID,
            gcs_uri=gcs_uri,
            key_path=None
        )

        if document_result:
            extracted_items = extract_entities_from_docai_result(
                document=document_result,
                filename=file_name,
                id_extracao_run=id_execucao
            )
            if extracted_items:
                logging.info(f"[{id_execucao}] Extraídos {len(extracted_items)} itens de '{file_name}'.")
                load_data_to_bigquery(extracted_items, config=config)
                items_loaded_count = len(extracted_items)
                logging.info(f"[{id_execucao}] Carregamento de '{file_name}' para BigQuery solicitado com sucesso.")
            else:
                logging.warning(f"[{id_execucao}] Nenhum item extraído do arquivo '{file_name}'.")
        else:
            logging.error(f"[{id_execucao}] Falha ao processar o documento GCS '{gcs_uri}' com Document AI.")
    except Exception as e:
        logging.error(f"[{id_execucao}] Erro inesperado ao processar o arquivo GCS '{gcs_uri}': {e}", exc_info=True)
    return items_loaded_count

def cloud_function_entry_point(event, context):
    """ Ponto de entrada para a Google Cloud Function acionada por GCS. """
    try:
        file_name = event.get('name')
        bucket_name = event.get('bucket')
        event_id = context.event_id if context and hasattr(context, 'event_id') else f"cf_run_{uuid.uuid4()}"

        if not file_name or not bucket_name:
            logging.error("Evento GCS inválido: 'name' ou 'bucket' ausente. Evento: %s", event)
            return

        if not file_name.lower().endswith(".pdf"):
            logging.info(f"Ignorando arquivo não PDF: gs://{bucket_name}/{file_name}")
            return

        logging.info(f"Evento GCS recebido (ID: {event_id}): Processando arquivo '{file_name}' do bucket '{bucket_name}'.")
        items_loaded = process_gcs_pdf(bucket_name, file_name, id_execucao=event_id)
        logging.info(f"Evento GCS (ID: {event_id}) concluído. Itens carregados: {items_loaded}")

    except Exception as e:
        logging.error(f"Erro fatal no manipulador de eventos GCS (ID: {context.event_id if context else 'N/A'}): {e}. Evento: {event}", exc_info=True)

if __name__ == "__main__":
    logging.info("--- INÍCIO DA EXECUÇÃO LOCAL DO SCRIPT (docai_utils.py) ---")
    try:
        if not GCS_INPUT_BUCKET:
            logging.error("GCS_INPUT_BUCKET não definido na configuração para execução local.")
        else:
            pdf_blobs = list_gcs_pdfs(GCS_INPUT_BUCKET, None)
            if not pdf_blobs:
                logging.warning(f"Nenhum arquivo PDF encontrado no bucket GCS para teste local: gs://{GCS_INPUT_BUCKET}")
            else:
                logging.info(f"Encontrados {len(pdf_blobs)} arquivos PDF no GCS para processamento local.")
                total_itens_carregados_local = 0
                id_execucao_local = f"local_run_{uuid.uuid4()}"
                for blob in pdf_blobs:
                    items = process_gcs_pdf(blob.bucket.name, blob.name, id_execucao=id_execucao_local)
                    total_itens_carregados_local += items
                logging.info(f"Total de itens carregados no BigQuery nesta execução local: {total_itens_carregados_local}")
    except Exception as e:
        logging.critical(f"Erro fatal na execução local do script: {e}", exc_info=True)
    logging.info("--- FIM DA EXECUÇÃO LOCAL DO SCRIPT (docai_utils.py) ---")
