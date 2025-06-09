"""
Script manual para testar o fluxo de sumarização e comparação de CCTs:
- Busca uma CCT com status 'ANALISE_CLAUSULAS_PENDENTE_REVISAO' (ou 'TEXTO_EXTRAIDO')
- Executa a função de sumarização/comparação
- Atualiza o resumo e análise comparativa no BigQuery

Requisitos:
- Variáveis de ambiente GCP configuradas
- Permissões de acesso ao BigQuery e GCS
- Instale dependências: pip install google-cloud-bigquery google-cloud-storage
"""
import os
import asyncio
import json
from google.cloud import bigquery
from datetime import datetime

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "seu-projeto-gcp")
BQ_DATASET_ID = os.getenv("BQ_DATASET_ID", "auditoria_folha_dataset")
CCT_TEXT_BUCKET_NAME = os.getenv("CCT_TEXT_BUCKET_NAME", "auditoria360-ccts-textos-extraidos")
MAX_TEXT_LENGTH_FOR_GEMINI = 30000

bq_client = bigquery.Client(project=PROJECT_ID)

def ler_texto_do_gcs(gcs_uri):
    from google.cloud import storage
    parts = gcs_uri.replace("gs://", "").split("/", 1)
    bucket_name = parts[0]
    blob_name = parts[1]
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return blob.download_as_text(encoding="utf-8")

async def sumarizar_e_comparar_cct_textos_gcs(id_cct_documento_atual, texto_atual_gcs_uri, id_cct_base_referencia=None):
    print(f"Iniciando sumarização/comparação para CCT ID: {id_cct_documento_atual}")
    texto_cct_atual = ler_texto_do_gcs(texto_atual_gcs_uri)
    prompt_sumarizacao = f"""
    Você é um especialista em legislação trabalhista brasileira. Analise o seguinte texto completo de uma Convenção Coletiva de Trabalho (CCT) ou Aditivo:
    ---
    {texto_cct_atual[:MAX_TEXT_LENGTH_FOR_GEMINI]}
    ---
    Gere um resumo executivo conciso (máximo 5-7 tópicos principais) que destaque:
    - Os principais temas abordados (ex: Reajuste Salarial, Pisos, Benefícios, Jornada, Contribuições).
    - Mudanças ou pontos de atenção críticos para o Departamento Pessoal.
    - O período de vigência, se identificável.
    """
    resumo_executivo_ia = f"MOCK Resumo: A CCT {id_cct_documento_atual} estabelece novo piso, reajuste e altera VR." # Substitua por chamada Gemini real
    analise_comparativa_ia_json = None
    if id_cct_base_referencia:
        print(f"Comparando CCT {id_cct_documento_atual} com base {id_cct_base_referencia}")
        # Buscar o texto da CCT base
        query = f"SELECT texto_extraido_gcs_uri FROM `{PROJECT_ID}.{BQ_DATASET_ID}.CCTsDocumentos` WHERE id_cct_documento = @id_base"
        job_config = bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter("id_base", "STRING", id_cct_base_referencia)])
        result = bq_client.query(query, job_config=job_config).result()
        row = next(result, None)
        if row and row.texto_extraido_gcs_uri:
            texto_cct_base = ler_texto_do_gcs(row.texto_extraido_gcs_uri)
        else:
            texto_cct_base = ""
        prompt_comparacao = f"""
        Compare o texto da CCT anterior e atual e destaque as principais mudanças relevantes para folha de pagamento.
        ---
        ANTERIOR: {texto_cct_base[:15000]}
        ---
        ATUAL: {texto_cct_atual[:15000]}
        ---
        Liste as mudanças em formato JSON.
        """
        analise_comparativa_ia_json = json.dumps([
            {"tipo_mudanca": "REAJUSTE_SALARIAL_MOCK", "descricao_mudanca_observada": "Reajuste aumentou de 4% para 5%.", "impacto_estimado_folha": "MEDIO"},
            {"tipo_mudanca": "REMOCAO_CLAUSULA_MOCK", "descricao_mudanca_observada": "Cláusula sobre abono especial foi removida.", "impacto_estimado_folha": "BAIXO"}
        ])
    # Atualizar no BigQuery
    query_update = f"""
        UPDATE `{PROJECT_ID}.{BQ_DATASET_ID}.CCTsDocumentos`
        SET status_processamento_ia = 'ANALISE_COMPLETA_CONCLUIDA',
            resumo_executivo_ia = @resumo,
            analise_comparativa_ia_json = @comparacao,
            data_ultima_modificacao = CURRENT_TIMESTAMP()
        WHERE id_cct_documento = @id_cct_doc
    """
    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("resumo", "STRING", resumo_executivo_ia),
        bigquery.ScalarQueryParameter("comparacao", "STRING", analise_comparativa_ia_json),
        bigquery.ScalarQueryParameter("id_cct_doc", "STRING", id_cct_documento_atual),
    ])
    bq_client.query(query_update, job_config=job_config).result()
    print(f"Resumo e comparação atualizados para CCT {id_cct_documento_atual}!")

async def main():
    # Buscar uma CCT pronta para sumarização/comparação
    query = f"""
        SELECT id_cct_documento, texto_extraido_gcs_uri, id_cct_base_referencia
        FROM `{PROJECT_ID}.{BQ_DATASET_ID}.CCTsDocumentos`
        WHERE status_processamento_ia IN ('TEXTO_EXTRAIDO', 'ANALISE_CLAUSULAS_PENDENTE_REVISAO')
        LIMIT 1
    """
    result = bq_client.query(query).result()
    row = next(result, None)
    if not row:
        print("Nenhuma CCT pronta para sumarização/comparação encontrada.")
        return
    await sumarizar_e_comparar_cct_textos_gcs(row.id_cct_documento, row.texto_extraido_gcs_uri, row.id_cct_base_referencia)

if __name__ == "__main__":
    asyncio.run(main())
