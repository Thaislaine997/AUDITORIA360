"""
Script manual para testar o fluxo de extração de texto de uma CCT real:
- Busca um registro de CCT no BigQuery com status 'PENDENTE_EXTRACAO'
- Executa o worker de extração de texto (OCR)
- Salva o texto no GCS e atualiza o status/URI no BigQuery

Requisitos:
- Variáveis de ambiente GCP configuradas
- Permissões de acesso ao BigQuery, GCS e Document AI
- Instale dependências: pip install google-cloud-bigquery google-cloud-storage google-cloud-documentai
"""
import os
import asyncio
from google.cloud import bigquery
# from src.processamento_cct import processar_extracao_texto_cct

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "seu-projeto-gcp")
BQ_DATASET_ID = os.getenv("BQ_DATASET_ID", "auditoria_folha_dataset")

bq_client = bigquery.Client(project=PROJECT_ID)

async def main():
    # 1. Buscar uma CCT com status 'PENDENTE_EXTRACAO'
    query = f"""
        SELECT id_cct_documento, gcs_uri_documento, id_cliente_principal_associado, data_inicio_vigencia
        FROM `{PROJECT_ID}.{BQ_DATASET_ID}.CCTsDocumentos`
        WHERE status_processamento_ia = 'PENDENTE_EXTRACAO'
        LIMIT 1
    """
    result = bq_client.query(query).result()
    row = next(result, None)
    if not row:
        print("Nenhuma CCT com status PENDENTE_EXTRACAO encontrada.")
        return
    id_cct = row.id_cct_documento
    gcs_uri_pdf = row.gcs_uri_documento
    id_cliente = row.id_cliente_principal_associado or "global"
    ano_vigencia = row.data_inicio_vigencia.year if row.data_inicio_vigencia else 2025
    print(f"Processando CCT: {id_cct}\nPDF: {gcs_uri_pdf}")
    # await processar_extracao_texto_cct(id_cct, gcs_uri_pdf, id_cliente, ano_vigencia)
    print("Processo concluído!")

if __name__ == "__main__":
    asyncio.run(main())
