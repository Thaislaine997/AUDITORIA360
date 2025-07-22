import logging
try:
    # For Cloud Functions v2 (current version)
    from functions_framework import Request
    Context = None  # Context not needed in v2
except ImportError:
    try:
        # Fallback to v1 context if available
        from google.cloud.functions_v1.context import Context
        Request = None
    except ImportError:
        # Allow running locally without the package
        Context = None
        Request = None
from services.ingestion.config_loader import load_config
from services.ingestion.docai_utils import process_pdf
from services.ingestion.bq_loader import load_data_to_bq
from services.ingestion.generate_data_hash import compute_hash

def main(event: dict, context=None):
    """
    Main function compatible with both Cloud Functions v1 and v2.
    
    Args:
        event: Event data (dict for v1, Request object for v2)
        context: Context object (v1 only, optional)
    """
    cfg = load_config()
    logging.basicConfig(level=cfg['log_level'])

    bucket = event['bucket']
    filename = event['name']
    uri = f"gs://{bucket}/{filename}"

    file_hash = compute_hash(uri)
    logging.info(f"Iniciando processamento: {filename}, hash={file_hash}")

    entities = process_pdf(uri, cfg)
    for row in entities:
        row['file_hash'] = file_hash

    load_data_to_bq(entities, cfg)
    logging.info(f"Processamento concluído: {filename}")