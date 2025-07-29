import logging

try:
    from google.cloud.functions_v1.context import Context
except ImportError:
    Context = None  # Permite rodar localmente sem o pacote
from services.ingestion.config_loader import load_config
from services.ingestion.docai_utils import process_pdf
from services.ingestion.bq_loader import load_data_to_bq
from services.ingestion.generate_data_hash import compute_hash


def main(event: dict, context: Context):
    cfg = load_config()
    logging.basicConfig(level=cfg["log_level"])

    bucket = event["bucket"]
    filename = event["name"]
    uri = f"gs://{bucket}/{filename}"

    file_hash = compute_hash(uri)
    logging.info(f"Iniciando processamento: {filename}, hash={file_hash}")

    entities = process_pdf(uri, cfg)
    for row in entities:
        row["file_hash"] = file_hash

    load_data_to_bq(entities, cfg)
    logging.info(f"Processamento concluído: {filename}")
