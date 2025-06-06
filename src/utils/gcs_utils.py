# src/utils/gcs_utils.py
"""
Funções utilitárias para upload de arquivos no Google Cloud Storage (GCS).
"""
from google.cloud import storage

def upload_file_to_gcs(
    bucket_name: str,
    destination_blob_name: str,
    file_bytes: bytes,
    content_type: str
) -> str:
    """
    Faz upload de um arquivo (em bytes) para um bucket GCS e retorna a URI 'gs://'.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(file_bytes, content_type=content_type)
    return f"gs://{bucket_name}/{destination_blob_name}"
