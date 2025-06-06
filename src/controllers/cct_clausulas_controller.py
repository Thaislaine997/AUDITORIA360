"""
Controller para revisão/admin de cláusulas extraídas de CCTs.
"""
from typing import List
from src.schemas_cct import ClausulaExtraidaResponse, UpdateClausulaRevisaoRequest
from src.utils.bq_utils import BigQueryUtils
import os
from datetime import datetime

GCP_PROJECT = os.environ.get("GCP_PROJECT_ID", "seu-projeto-gcp")
BQ_DATASET = os.environ.get("BQ_DATASET_ID", "auditoria_folha_dataset")
TABLE_CLAUSULAS = f"{GCP_PROJECT}.{BQ_DATASET}.CCTsClausulasExtraidas"

bq_utils = BigQueryUtils(project_id=GCP_PROJECT)

async def listar_clausulas_para_revisao(tipo_clausula=None, status=None, id_cct=None, data_inicial=None, data_final=None) -> List[ClausulaExtraidaResponse]:
    where = []
    if status:
        where.append(f"status_revisao_humana = '{status}'")
    else:
        where.append("status_revisao_humana = 'PENDENTE'")
    if tipo_clausula:
        where.append(f"tipo_clausula_identificada = '{tipo_clausula}'")
    if id_cct:
        where.append(f"id_cct_documento_fk = '{id_cct}'")
    if data_inicial:
        where.append(f"timestamp_extracao_clausula >= '{data_inicial}'")
    if data_final:
        where.append(f"timestamp_extracao_clausula <= '{data_final}'")
    where_sql = " AND ".join(where)
    query = f"""
        SELECT * FROM `{TABLE_CLAUSULAS}`
        WHERE {where_sql}
        ORDER BY timestamp_extracao_clausula DESC
        LIMIT 100
    """
    rows = bq_utils.query(query)
    return [ClausulaExtraidaResponse(**row) for row in rows]

async def atualizar_clausula_extraida(id_clausula: str, payload: UpdateClausulaRevisaoRequest) -> ClausulaExtraidaResponse:
    query = f"""
        UPDATE `{TABLE_CLAUSULAS}`
        SET status_revisao_humana = @status,
            usuario_revisao_humana = @usuario,
            data_revisao_humana = @data,
            notas_revisao_humana = @notas
        WHERE id_clausula_extraida = @id
    """
    params = [
        {"name": "status", "parameterType": {"type": "STRING"}, "parameterValue": {"value": payload.status_revisao_humana}},
        {"name": "usuario", "parameterType": {"type": "STRING"}, "parameterValue": {"value": payload.usuario_revisao_humana}},
        {"name": "data", "parameterType": {"type": "TIMESTAMP"}, "parameterValue": {"value": datetime.now().isoformat()}},
        {"name": "notas", "parameterType": {"type": "STRING"}, "parameterValue": {"value": payload.notas_revisao_humana}},
        {"name": "id", "parameterType": {"type": "STRING"}, "parameterValue": {"value": id_clausula}},
    ]
    bq_utils.query_with_params(query, params)
    # Buscar a cláusula atualizada
    rows = bq_utils.query(f"SELECT * FROM `{TABLE_CLAUSULAS}` WHERE id_clausula_extraida = '{id_clausula}'")
    if not rows:
        raise Exception("Cláusula não encontrada após atualização.")
    return ClausulaExtraidaResponse(**rows[0])
