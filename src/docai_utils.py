# filepath: src/docai_utils.py
import json
import logging
import uuid
import os
import sys  # Adicionado import sys
from datetime import datetime, timezone
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from google.cloud import storage
from google.oauth2 import service_account
from unittest.mock import MagicMock  # Import MagicMock

from .bq_loader import load_data_to_bigquery

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

mock_logger_specific = MagicMock()

# --- Carregar Configurações (Removido carregamento global estático) ---
def get_docai_config(config_override: dict | None = None) -> dict:
    """
    Retorna um dicionário de configuração para uso no módulo docai_utils.
    Prioriza config_override, depois variáveis de ambiente, e por fim config.json.
    """
    # Define as chaves de configuração esperadas
    expected_keys = [
        "gcp_project_id", "gcp_location", "docai_processor_id",
        "gcs_input_bucket", "bq_dataset_id", "bq_table_id"
    ]
    config = {}

    # 1. Tenta carregar do ambiente
    for key in expected_keys:
        config[key] = os.environ.get(key)

    # 2. Tenta carregar do arquivo JSON para chaves ainda não definidas pelo ambiente
    # Verifica se alguma chave ainda é None para decidir se lê o arquivo
    # CORREÇÃO: needs_file_load deve ser True se QUALQUER chave essencial ainda for None
    # E não foi fornecida por override (se config_override existir e tiver a chave)
    needs_file_load = any(
        config[key] is None and (config_override is None or key not in config_override)
        for key in expected_keys
    )

    if needs_file_load:
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_FILE_PATH = os.path.join(SCRIPT_DIR, "config.json")
        json_config_from_file = {} 
        try:
            if os.path.exists(CONFIG_FILE_PATH):
                with open(CONFIG_FILE_PATH, 'r') as f:
                    json_config_from_file = json.load(f)
                logger.info(f"Configuração carregada de {CONFIG_FILE_PATH}")
            else:
                logger.info(f"Arquivo de configuração {CONFIG_FILE_PATH} não encontrado. Usando apenas variáveis de ambiente e overrides.")
                json_config_from_file = {} 
        except Exception as e:
            logger.warning(f"Não foi possível carregar ou processar o arquivo de configuração JSON: {CONFIG_FILE_PATH}. Erro: {e}")

        # Preenche apenas as chaves que ainda são None (não foram definidas pelas variáveis de ambiente)
        for key in expected_keys:
            if config[key] is None:
                config[key] = json_config_from_file.get(key)

    # 3. Aplica overrides, que têm a maior prioridade
    if config_override:
        config.update(config_override)

    # Validação final: Verifica se todas as chaves esperadas têm valores (não None)
    # Esta validação deve ocorrer DEPOIS de todas as fontes de configuração terem sido tentadas.
    missing_essential_keys = [key for key in expected_keys if config.get(key) is None]
    if missing_essential_keys:
        error_msg = f"Configuração do DocAI incompleta. Chaves essenciais ausentes ou não definidas: {', '.join(missing_essential_keys)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    return config

def get_docai_client(key_path=None):
    """Cria e retorna um cliente Document AI."""
    client_options = ClientOptions(api_endpoint=f"{os.environ.get('GCP_LOCATION')}-documentai.googleapis.com")
    try:
        if key_path:
            logger.info(f"Criando cliente Document AI usando chave local: {key_path}")
            credentials = service_account.Credentials.from_service_account_file(key_path)
            client = documentai.DocumentProcessorServiceClient(credentials=credentials, client_options=client_options)
        else:
            logger.info("Criando cliente Document AI usando Application Default Credentials (ADC).")
            client = documentai.DocumentProcessorServiceClient(client_options=client_options)
        logger.info("Cliente Document AI criado com sucesso.")
        return client
    except Exception as e:
        logger.error(f"Falha ao criar cliente Document AI: {e}", exc_info=True)
        raise

from typing import Optional

def process_document_ocr(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_uri: str,
    mime_type: str = "application/pdf",
    key_path: Optional[str] = None
) -> Optional[documentai.Document]:
    docai_client = get_docai_client(key_path)
    resource_name = docai_client.processor_path(project_id, location, processor_id)
    logger.info(f"Usando processador: {resource_name}")

    # Crie o GcsDocument diretamente para o ProcessRequest
    gcs_input = documentai.GcsDocument(gcs_uri=gcs_uri, mime_type=mime_type)

    logger.info(f"Processando arquivo do GCS: {gcs_uri}")
    request = documentai.ProcessRequest(
        name=resource_name,
        gcs_document=gcs_input  # CORRIGIDO: Use gcs_document diretamente
    )
    try:
        logger.info("Enviando requisição para processar arquivo do GCS...")
        result = docai_client.process_document(request=request)
        logger.info("Documento processado com sucesso.")
        return result.document
    except Exception as e:
        logger.error(f"Falha ao processar documento '{gcs_uri}' com Document AI: {e}", exc_info=True)
        return None

def extract_entities_from_docai_result(document: documentai.Document, filename: str, id_extracao_run: str) -> list[dict]:
    extracted_items = []
    if not document:
        logger.warning(f"Documento nulo fornecido para extração de entidades (arquivo: {filename}).")
        return extracted_items

    logger.info(f"Iniciando extração de entidades do arquivo '{filename}'. Texto detectado: {len(document.text)} caracteres.")
    logger.info(f"Total de entidades encontradas no documento: {len(document.entities)}")

    current_timestamp = datetime.now(timezone.utc).isoformat()  # Adicionado para timestamp_carga

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
                logger.warning(f"Campo '{entity.type_}' com valor '{entity.mention_text}' não pôde ser convertido para número no arquivo '{filename}'.")

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
            "timestamp_carga": current_timestamp  # Adicionado campo timestamp_carga
        }
        extracted_items.append(item)
    logger.info(f"Extração de entidades do arquivo '{filename}' concluída. {len(extracted_items)} itens extraídos.")
    return extracted_items

def list_gcs_pdfs(bucket_name, prefix=""):
    logger.info(f"Entrando em list_gcs_pdfs com bucket: {bucket_name}, prefix: {prefix}")
    pdf_uris = []
    try:
        client = storage.Client()
        logger.info(f"Cliente GCS criado: {type(client)}")
        
        logger.info(f"Tentando chamar client.list_blobs com bucket='{bucket_name}', prefix='{prefix}'")
        blobs = client.list_blobs(bucket_name, prefix=prefix)
        logger.info(f"client.list_blobs retornou: {type(blobs)}. Conteúdo (primeiros itens): {list(blobs)[:5]}")

        for blob in blobs:
            logger.debug(f"Processando blob: name='{blob.name}', content_type='{blob.content_type}'")
            is_pdf = blob.name.lower().endswith(".pdf")
            logger.debug(f"  '{blob.name}'.lower().endswith('.pdf') -> {is_pdf}")
            if is_pdf:
                uri = f"gs://{bucket_name}/{blob.name}"
                pdf_uris.append(uri)
                logger.debug(f"  Adicionado URI: {uri}")
        logger.info(f"PDFs encontrados: {pdf_uris}")
    except Exception as e:
        logger.error(f"Erro em list_gcs_pdfs: {e}", exc_info=True)
        return []
    
    logger.info(f"Saindo de list_gcs_pdfs. Retornando {len(pdf_uris)} URIs.")
    return pdf_uris

def process_gcs_pdf(bucket_name: str, file_name: str, id_execucao: str | None = None, config_override: dict | None = None):
    if not bucket_name or not isinstance(bucket_name, str):
        raise ValueError("bucket_name deve ser uma string não vazia.")
    config_override = config_override or {}
    config = get_docai_config(config_override)
    if not id_execucao:
        id_execucao = f"run_{uuid.uuid4()}"

    gcs_uri = f"gs://{bucket_name}/{file_name}"
    logger.info(f"[{id_execucao}] Iniciando processamento para: {gcs_uri}")
    items_loaded_count = 0

    try:
        # Verifica se as variáveis de configuração essenciais não são None e são do tipo str
        if not all(isinstance(x, str) and x for x in [config.get("gcp_project_id"), config.get("gcp_location"), config.get("docai_processor_id")]):
            raise ValueError("Configuração essencial ausente ou inválida: gcp_project_id, gcp_location ou docai_processor_id está None ou não é string.")

        document_result = process_document_ocr(
            project_id=str(config.get("gcp_project_id")),
            location=str(config.get("gcp_location")),
            processor_id=str(config.get("docai_processor_id")),
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
                logger.info(f"[{id_execucao}] Extraídos {len(extracted_items)} itens de '{file_name}'.")
                load_data_to_bigquery(extracted_items, config=config)
                items_loaded_count = len(extracted_items)
                logger.info(f"[{id_execucao}] Carregamento de '{file_name}' para BigQuery solicitado com sucesso.")
            else:
                logger.warning(f"[{id_execucao}] Nenhum item extraído do arquivo '{file_name}'.")
        else:
            logger.error(f"[{id_execucao}] Falha ao processar o documento GCS '{gcs_uri}' com Document AI.")
    except Exception as e:
        logger.error(f"[{id_execucao}] Erro inesperado ao processar o arquivo GCS '{gcs_uri}': {e}", exc_info=True)
    return items_loaded_count

def cloud_function_entry_point(event, context):
    """ Ponto de entrada para a Google Cloud Function acionada por GCS. """
    try:
        file_name = event.get('name')
        bucket_name = event.get('bucket')
        event_id = context.event_id if context and hasattr(context, 'event_id') else f"cf_run_{uuid.uuid4()}"

        if not file_name or not bucket_name:
            logger.error("Evento GCS inválido: 'name' ou 'bucket' ausente. Evento: %s", event)
            return

        if not file_name.lower().endswith(".pdf"):
            logger.info(f"Ignorando arquivo não PDF: gs://{bucket_name}/{file_name}")
            return

        logger.info(f"Evento GCS recebido (ID: {event_id}): Processando arquivo '{file_name}' do bucket '{bucket_name}'.")
        items_loaded = process_gcs_pdf(bucket_name, file_name, id_execucao=event_id)
        logger.info(f"Evento GCS (ID: {event_id}) concluído. Itens carregados: {items_loaded}")

    except Exception as e:
        logger.error(f"Erro fatal no manipulador de eventos GCS (ID: {context.event_id if context else 'N/A'}): {e}. Evento: {event}", exc_info=True)

if __name__ == "__main__":
    logger.info("--- INÍCIO DA EXECUÇÃO LOCAL DO SCRIPT (docai_utils.py) ---")
    try:
        config = get_docai_config()
        bucket = config.get("gcs_input_bucket")
        if not bucket or not isinstance(bucket, str):
            logger.error("gcs_input_bucket não definido ou inválido na configuração para execução local.")
        else:
            id_execucao_local = f"local_run_{uuid.uuid4()}"
            total_itens_carregados_local = 0

            if len(sys.argv) > 1:
                # Processar um arquivo específico passado como argumento
                file_to_process = sys.argv[1]
                logger.info(f"Processando arquivo específico fornecido como argumento: {file_to_process} do bucket {bucket}")
                # Verifica se o arquivo existe no bucket antes de tentar processar
                storage_client = storage.Client()
                bucket_obj = storage_client.bucket(bucket)
                blob_obj = bucket_obj.blob(file_to_process)

                if blob_obj.exists():
                    items = process_gcs_pdf(bucket, file_to_process, id_execucao=id_execucao_local, config_override=config)
                    total_itens_carregados_local += items
                else:
                    logger.error(f"Arquivo '{file_to_process}' não encontrado no bucket '{bucket}'.")

            else:
                # Comportamento original: processar todos os PDFs no bucket
                logger.warning("Nenhum arquivo PDF específico fornecido como argumento. Listando todos os PDFs no bucket para processamento.")
                client = storage.Client()
                blobs = client.list_blobs(bucket, prefix=None)
                
                pdf_files_to_process = [blob for blob in blobs if blob.name.lower().endswith(".pdf")]

                if not pdf_files_to_process:
                    logger.warning(f"Nenhum arquivo PDF encontrado no bucket GCS para teste local: gs://{bucket}")
                else:
                    logger.info(f"Encontrados {len(pdf_files_to_process)} arquivos PDF no GCS para processamento local.")
                    for blob_item in pdf_files_to_process:
                        logger.info(f"Processando: {blob_item.name} do bucket {blob_item.bucket.name}")
                        items = process_gcs_pdf(blob_item.bucket.name, blob_item.name, id_execucao=id_execucao_local, config_override=config)
                        total_itens_carregados_local += items
            
            logger.info(f"Total de itens carregados no BigQuery nesta execução local: {total_itens_carregados_local}")

    except Exception as e:
        logger.critical(f"Erro fatal na execução local do script: {e}", exc_info=True)
    logger.info("--- FIM DA EXECUÇÃO LOCAL DO SCRIPT (docai_utils.py) ---")
