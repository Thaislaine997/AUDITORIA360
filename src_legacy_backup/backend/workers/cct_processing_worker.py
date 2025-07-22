"""
Worker para extração de texto de CCTs (OCR via Document AI) e upload do texto para GCS.
Atualiza o status e o URI do texto extraído na tabela CCTsDocumentos (BigQuery).
"""
import os
from google.cloud import documentai, storage, bigquery
from datetime import datetime
import uuid
from vertexai.preview.generative_models import GenerativeModel

# Configurações (ajustar conforme ambiente)
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "seu-projeto-gcp")
DOCAI_LOCATION = os.getenv("DOCAI_LOCATION", "us")
CCT_EXTRATOR_PROCESSOR_ID = os.getenv("CCT_EXTRATOR_PROCESSOR_ID", "seu-processador-ocr-id")
CCT_TEXT_BUCKET_NAME = os.getenv("CCT_TEXT_BUCKET_NAME", "auditoria360-ccts-textos-extraidos")
BQ_DATASET_ID = os.getenv("BQ_DATASET_ID", "auditoria_folha_dataset")

# Inicialização dos clientes
storage_client = storage.Client(project=PROJECT_ID)
bq_client = bigquery.Client(project=PROJECT_ID)
docai_client = documentai.DocumentProcessorServiceClient()

def gerar_resumo_gemini(prompt: str) -> str:
    model = GenerativeModel("gemini-1.5-pro-preview-0409")
    response = model.generate_content(
        [prompt],
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.2,
            "response_mime_type": "text/plain"
        }
    )
    return response.text

async def processar_extracao_texto_cct(id_cct_documento: str, gcs_uri_pdf_original: str, id_cliente_ou_global: str, ano_vigencia: int):
    """
    Extrai texto de um PDF de CCT, salva em GCS e atualiza o BigQuery.
    """
    print(f"Iniciando extração de texto para CCT Documento ID: {id_cct_documento}")
    # 1. Atualizar status no BigQuery para 'EM_EXTRACAO_TEXTO'
    # (Implementar update real via bq_client se necessário)
    try:
        # 2. Chamar Document AI para extrair texto (mock para dev local)
        # TODO: Substituir pelo utilitário real de OCR
        class MockDocumentPage:
            pass
        class MockDocument:
            def __init__(self, text, num_pages):
                self.text = text
                self.pages = [MockDocumentPage() for _ in range(num_pages)]
        document_obj = MockDocument(text=f"Texto extraído da CCT {id_cct_documento}...", num_pages=10)
        # Fim do mock
        if not document_obj or not document_obj.text:
            raise ValueError("Document AI OCR não retornou texto.")
        texto_extraido_cct = document_obj.text
        numero_paginas = len(document_obj.pages)
        # 3. Salvar Texto Extraído no GCS
        gcs_txt_blob_name = f"{id_cliente_ou_global}/{ano_vigencia}/{id_cct_documento}.txt"
        bucket = storage_client.bucket(CCT_TEXT_BUCKET_NAME)
        blob = bucket.blob(gcs_txt_blob_name)
        blob.upload_from_string(texto_extraido_cct, content_type="text/plain; charset=utf-8")
        gcs_uri_texto_extraido = f"gs://{CCT_TEXT_BUCKET_NAME}/{gcs_txt_blob_name}"
        print(f"Texto extraído salvo em: {gcs_uri_texto_extraido}")
        # 4. Atualizar Tabela CCTsDocumentos no BigQuery com o URI e novo status
        query_update_bq = f"""
            UPDATE `{PROJECT_ID}.{BQ_DATASET_ID}.CCTsDocumentos`
            SET status_processamento_ia = 'TEXTO_EXTRAIDO', 
                texto_extraido_gcs_uri = @gcs_uri_texto,
                numero_paginas_ocr = @num_paginas,
                data_ultima_modificacao = CURRENT_TIMESTAMP()
            WHERE id_cct_documento = @id_cct_doc
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("gcs_uri_texto", "STRING", gcs_uri_texto_extraido),
                bigquery.ScalarQueryParameter("num_paginas", "INT64", numero_paginas),
                bigquery.ScalarQueryParameter("id_cct_doc", "STRING", id_cct_documento),
            ]
        )
        # bq_client.query(query_update_bq, job_config=job_config).result()
        print(f"MOCK BQ: Atualizando CCT {id_cct_documento} com URI: {gcs_uri_texto_extraido}, Páginas: {numero_paginas}, Status: TEXTO_EXTRAIDO")
    except Exception as e:
        print(f"Falha na extração de texto para CCT {id_cct_documento}: {e}")
        # Atualizar status no BigQuery para 'FALHA_EXTRACAO_TEXTO' (implementação real)
        raise
