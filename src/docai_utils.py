# filepath: src/docai_utils.py
import json
import logging
import uuid
import os
import sys
from datetime import datetime, timezone
from google.api_core.client_options import ClientOptions
from google.cloud import documentai, storage, bigquery
from google.oauth2 import service_account
from unittest.mock import MagicMock
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type # Adicionado tenacity

from .bq_loader import load_data_to_bigquery, get_bigquery_client

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

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(Exception), # Tenta novamente em qualquer exceção genérica da API
    reraise=True # Re-levanta a exceção original se todas as tentativas falharem
)
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
        raise # Re-levanta para que o tenacity possa lidar com isso

def extract_entities_from_docai_result(document: documentai.Document, filename: str, id_extracao_run: str, client_id: str) -> list[dict]: # Added client_id parameter
    extracted_items = []
    if not document:
        logger.warning(f"[{client_id}] Documento nulo fornecido para extração de entidades (arquivo: {filename}).")
        return extracted_items

    logger.info(f"[{client_id}] Iniciando extração de entidades do arquivo '{filename}'. Texto detectado: {len(document.text)} caracteres.")
    logger.info(f"[{client_id}] Total de entidades encontradas no documento: {len(document.entities)}")

    current_timestamp = datetime.now(timezone.utc).isoformat()

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
                logger.warning(f"[{client_id}] Campo '{entity.type_}' com valor '{entity.mention_text}' não pôde ser convertido para número no arquivo '{filename}'.")

        item = {
            "client_id": client_id, # Added client_id to the item
            "id_extracao": id_extracao_run,
            "id_item": f"item_{uuid.uuid4()}",
            "nome_arquivo_origem": filename,
            "pagina": page_number,
            "tipo_campo": entity.type_,
            "texto_extraido": entity.mention_text,
            "valor_limpo": cleaned_value,
            "valor_numerico": numeric_value,
            "confianca": entity.confidence,
            "timestamp_carga": current_timestamp
        }
        extracted_items.append(item)
    logger.info(f"[{client_id}] Extração de entidades do arquivo '{filename}' concluída. {len(extracted_items)} itens extraídos.")
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

def process_gcs_pdf(
    bucket_name: str, 
    file_name: str, 
    id_execucao: str | None = None, 
    config_override: dict | None = None,
    bq_client: bigquery.Client | None = None
):
    if not bucket_name or not isinstance(bucket_name, str):
        # Consider adding client_id to this error log if available early, though config is not yet processed
        raise ValueError("bucket_name deve ser uma string não vazia.")
    
    config_override = config_override if config_override is not None else {}
    config = get_docai_config(config_override) # This will include client_id if in config_override
    
    # client_id is now guaranteed by ConfigManager and passed via config_override
    client_id = config["client_id"] 

    if not id_execucao:
        id_execucao = f"run_{uuid.uuid4()}"

    gcs_uri = f"gs://{bucket_name}/{file_name}"
    logger.info(f"[{client_id}][{id_execucao}] Iniciando processamento para: {gcs_uri}")
    items_loaded_count = 0

    internal_bq_client = False
    if bq_client is None:
        try:
            logger.info(f"[{client_id}][{id_execucao}] Cliente BigQuery não injetado. Criando um novo cliente BQ a partir da configuração.")
            bq_client = get_bigquery_client(config) 
            internal_bq_client = True
            logger.info(f"[{client_id}][{id_execucao}] Novo cliente BigQuery criado internamente.")
        except Exception as e_bq_client:
            logger.error(f"[{client_id}][{id_execucao}] Falha ao criar cliente BigQuery internamente: {e_bq_client}", exc_info=True)
            raise
    
    try:
        # Ensure essential config keys for DocAI are present (gcp_project_id, gcp_location, docai_processor_id)
        # get_docai_config already validates these.

        document_result = process_document_ocr(
            project_id=str(config["gcp_project_id"]), # Already validated by get_docai_config
            location=str(config["gcp_location"]),   # Already validated
            processor_id=str(config["docai_processor_id"]), # Already validated
            gcs_uri=gcs_uri,
            key_path=config.get("service_account_key_path_local_dev")
        )

        if document_result:
            extracted_items = extract_entities_from_docai_result(
                document=document_result,
                filename=file_name,
                id_extracao_run=id_execucao,
                client_id=client_id # Pass client_id here
            )
            if extracted_items:
                logger.info(f"[{client_id}][{id_execucao}] Extraídos {len(extracted_items)} itens de '{file_name}'.")
                # load_data_to_bigquery will use the config which contains client_id for table/dataset names
                # and now extracted_items also contains client_id as a column.
                load_data_to_bigquery(client=bq_client, data=extracted_items, config=config)
                items_loaded_count = len(extracted_items)
                logger.info(f"[{client_id}][{id_execucao}] Carregamento de '{file_name}' para BigQuery solicitado com sucesso.")
            else:
                logger.warning(f"[{client_id}][{id_execucao}] Nenhum item extraído do arquivo '{file_name}'.")
        else:
            logger.error(f"[{client_id}][{id_execucao}] Falha ao processar o documento GCS '{gcs_uri}' com Document AI.")
    except Exception as e:
        logger.error(f"[{client_id}][{id_execucao}] Erro inesperado ao processar o arquivo GCS '{gcs_uri}': {e}", exc_info=True)
        # Consider re-raising or specific error handling if this task is part of a larger flow
    finally:
        if internal_bq_client and bq_client:
            logger.info(f"[{client_id}][{id_execucao}] Cliente BigQuery criado internamente não requer fechamento explícito.")
            pass

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
    bq_client_main = None # Inicializa o cliente BQ para o escopo do __main__
    try:
        config = get_docai_config() # Carrega a configuração geral primeiro

        # Tenta criar um cliente BigQuery para ser reutilizado nas chamadas de process_gcs_pdf
        # Isso assume que a config carregada por get_docai_config() também é suficiente para get_bigquery_client()
        # ou que get_bigquery_client() pode lidar com as chaves presentes.
        # Adicione "client_id" à configuração se não estiver lá, pois bq_loader espera.
        if "client_id" not in config:
            config["client_id"] = "docai_utils_main_default_client" # Ou um valor mais significativo
            logger.info(f"Adicionado client_id padrão \'{config['client_id']}\' à configuração para bq_client.")

        try:
            logger.info("Tentando criar cliente BigQuery compartilhado para a execução __main__...")
            bq_client_main = get_bigquery_client(config)
            logger.info(f"Cliente BigQuery compartilhado ({type(bq_client_main)}) criado para __main__.")
        except Exception as e_bq_main:
            logger.error(f"Falha ao criar cliente BigQuery compartilhado para __main__: {e_bq_main}. As chamadas a process_gcs_pdf criarão seus próprios clientes se necessário.", exc_info=True)
            # Continuar sem o cliente compartilhado; process_gcs_pdf tentará criar o seu.

        bucket = config.get("gcs_input_bucket")
        if not bucket or not isinstance(bucket, str):
            logger.error("gcs_input_bucket não definido ou inválido na configuração para execução local.")
        else:
            id_execucao_local = f"local_run_{uuid.uuid4()}"
            total_itens_carregados_local = 0

            if len(sys.argv) > 1:
                file_to_process = sys.argv[1]
                logger.info(f"Processando arquivo específico fornecido como argumento: {file_to_process} do bucket {bucket}")
                storage_client = storage.Client()
                bucket_obj = storage_client.bucket(bucket)
                blob_obj = bucket_obj.blob(file_to_process)

                if blob_obj.exists():
                    # Passa o bq_client_main para process_gcs_pdf
                    items = process_gcs_pdf(bucket, file_to_process, id_execucao=id_execucao_local, config_override=config, bq_client=bq_client_main)
                    total_itens_carregados_local += items
                else:
                    logger.error(f"Arquivo \'{file_to_process}\' não encontrado no bucket \'{bucket}\'.")
            else:
                logger.warning("Nenhum arquivo PDF específico fornecido como argumento. Listando todos os PDFs no bucket para processamento.")
                client = storage.Client() # Storage client para listar blobs
                blobs = client.list_blobs(bucket, prefix=None)
                
                pdf_files_to_process = [blob for blob in blobs if blob.name.lower().endswith(".pdf")]

                if not pdf_files_to_process:
                    logger.warning(f"Nenhum arquivo PDF encontrado no bucket GCS para teste local: gs://{bucket}")
                else:
                    logger.info(f"Encontrados {len(pdf_files_to_process)} arquivos PDF no GCS para processamento local.")
                    for blob_item in pdf_files_to_process:
                        logger.info(f"Processando: {blob_item.name} do bucket {blob_item.bucket.name}")
                        # Passa o bq_client_main para process_gcs_pdf
                        items = process_gcs_pdf(blob_item.bucket.name, blob_item.name, id_execucao=id_execucao_local, config_override=config, bq_client=bq_client_main)
                        total_itens_carregados_local += items
            
            logger.info(f"Total de itens carregados no BigQuery nesta execução local: {total_itens_carregados_local}")

    except Exception as e:
        logger.critical(f"Erro fatal na execução local do script: {e}", exc_info=True)
    # finally:
        # Se bq_client_main foi criado, teoricamente poderia ser fechado aqui.
        # Mas, como dito antes, geralmente não é necessário para google-cloud-bigquery client.
        # if bq_client_main:
        #     logger.info("Fechando cliente BigQuery compartilhado do __main__.")
        #     # bq_client_main.close() # Descomente se necessário
    logger.info("--- FIM DA EXECUÇÃO LOCAL DO SCRIPT (docai_utils.py) ---")
