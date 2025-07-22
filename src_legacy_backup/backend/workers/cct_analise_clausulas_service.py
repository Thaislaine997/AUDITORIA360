"""
Worker para análise de cláusulas relevantes em CCTs usando Gemini, a partir do texto extraído salvo no GCS.
Salva as cláusulas extraídas na tabela CCTsClausulasExtraidas (BigQuery) e atualiza o status da CCT.
"""
import os
import json
import uuid
from datetime import datetime
from google.cloud import storage, bigquery
from vertexai.preview.generative_models import GenerativeModel

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "seu-projeto-gcp")
CCT_TEXT_BUCKET_NAME = os.getenv("CCT_TEXT_BUCKET_NAME", "auditoria360-ccts-textos-extraidos")
BQ_DATASET_ID = os.getenv("BQ_DATASET_ID", "auditoria_folha_dataset")
MAX_TEXT_LENGTH_FOR_GEMINI = 30000
CHUNK_OVERLAP = 500

storage_client = storage.Client(project=PROJECT_ID)
bq_client = bigquery.Client(project=PROJECT_ID)

def gerar_resposta_estruturada_gemini(prompt: str) -> str:
    model = GenerativeModel("gemini-1.5-pro-preview-0409")
    response = model.generate_content(
        [prompt],
        generation_config={
            "max_output_tokens": 4096,
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
    )
    return response.text

async def analisar_e_extrair_clausulas_cct(id_cct_documento: str, texto_extraido_gcs_uri: str):
    print(f"Iniciando análise de cláusulas para CCT Documento ID: {id_cct_documento}")
    try:
        # 1. Ler texto do GCS
        parts = texto_extraido_gcs_uri.replace("gs://", "").split("/", 1)
        bucket_name_text = parts[0]
        blob_name_text = parts[1]
        bucket_text = storage_client.bucket(bucket_name_text)
        blob_text = bucket_text.blob(blob_name_text)
        texto_completo_cct = blob_text.download_as_text(encoding="utf-8")
        # 2. Chunking
        chunks_de_texto = []
        if len(texto_completo_cct) > MAX_TEXT_LENGTH_FOR_GEMINI:
            start = 0
            while start < len(texto_completo_cct):
                end = min(start + MAX_TEXT_LENGTH_FOR_GEMINI, len(texto_completo_cct))
                chunks_de_texto.append(texto_completo_cct[start:end])
                start += MAX_TEXT_LENGTH_FOR_GEMINI - CHUNK_OVERLAP
                if start >= len(texto_completo_cct): break
        else:
            chunks_de_texto.append(texto_completo_cct)
        print(f"Texto dividido em {len(chunks_de_texto)} chunk(s) para análise.")
        clausulas_extraidas_agregadas = []
        for i, chunk in enumerate(chunks_de_texto):
            print(f"Analisando chunk {i+1}/{len(chunks_de_texto)}...")
            prompt_gemini_clausulas = f"""
            Analise o seguinte trecho de uma Convenção Coletiva de Trabalho (CCT) brasileira.
            Identifique e extraia APENAS as cláusulas que tratam diretamente de:
            - Pisos salariais ou salários normativos (por função ou geral)
            - Reajustes salariais (percentuais, datas base)
            - Adicionais (horas extras, noturno, periculosidade, insalubridade, por tempo de serviço, etc.)
            - Benefícios (vale-refeição, vale-alimentação, vale-transporte, assistência médica, seguro de vida, auxílio creche, etc.)
            - Contribuições sindicais (laboral e patronal)
            - Regras sobre jornada de trabalho que impactam cálculos (ex: divisor de horas, banco de horas)
            - Estabilidades provisórias
            - Regras sobre férias (abono, início)
            - Regras sobre 13º salário (adiantamento)
            - Condições especiais de trabalho ou pagamento.

            Para cada cláusula relevante identificada, retorne um objeto JSON com os seguintes campos:
            - "tipo_clausula_sugerido": Uma categoria curta e descritiva (ex: "PISO_SALARIAL_MOTORISTA", "REAJUSTE_SALARIAL_PERCENTUAL", "VALE_REFEICAO_VALOR_DIARIO", "ADICIONAL_PERICULOSIDADE_PERCENTUAL", "CONTRIBUICAO_ASSISTENCIAL_LABORAL").
            - "texto_clausula_literal": O texto exato e completo da cláusula como aparece no documento.
            - "pagina_aproximada": Se possível inferir do contexto do chunk, a página aproximada (INT). (Opcional, pode ser difícil sem metadados de página no texto puro)
            - "palavras_chave": Uma lista de 3-5 palavras-chave relevantes da cláusula.

            Se nenhuma cláusula relevante for encontrada neste trecho, retorne um array JSON vazio.
            Formato de saída esperado: um array JSON de objetos.
            """
            resposta_gemini_json_str = gerar_resposta_estruturada_gemini(prompt_gemini_clausulas)
            try:
                clausulas_do_chunk = json.loads(resposta_gemini_json_str)
                if isinstance(clausulas_do_chunk, list):
                    for clausula_data in clausulas_do_chunk:
                        clausulas_extraidas_agregadas.append({
                            "id_clausula_extraida": str(uuid.uuid4()),
                            "id_cct_documento_fk": id_cct_documento,
                            "tipo_clausula_identificada": clausula_data.get("tipo_clausula_sugerido"),
                            "texto_clausula_extraido": clausula_data.get("texto_clausula_literal"),
                            "pagina_aproximada_documento": clausula_data.get("pagina_aproximada"),
                            "palavras_chave_clausula": clausula_data.get("palavras_chave"),
                            "confianca_extracao_ia": clausula_data.get("confianca_extracao_ia"),
                            "status_revisao_humana": "PENDENTE",
                            "timestamp_extracao_clausula": datetime.now().isoformat()
                        })
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON do Gemini para chunk {i+1} da CCT {id_cct_documento}: {e}. Resposta: {resposta_gemini_json_str}")
        # 3. Salvar cláusulas no BigQuery (mock)
        if clausulas_extraidas_agregadas:
            # bq_client.insert_rows_json(f"{PROJECT_ID}.{BQ_DATASET_ID}.CCTsClausulasExtraidas", clausulas_extraidas_agregadas)
            print(f"MOCK BQ: Inserindo {len(clausulas_extraidas_agregadas)} cláusulas para CCT {id_cct_documento}")
        status_final_analise = 'ANALISE_CLAUSULAS_PENDENTE_REVISAO' if clausulas_extraidas_agregadas else 'ANALISE_CONCLUIDA_SEM_CLAUSULAS_RELEVANTES'
        print(f"MOCK BQ: Status final CCT {id_cct_documento}: {status_final_analise}")
    except Exception as e:
        print(f"Falha na análise de cláusulas para CCT {id_cct_documento}: {e}")
        # bq_utils.update_cct_status(id_cct_documento, 'FALHA_ANALISE_CLAUSULAS', detalhes_erro=str(e))
        raise
