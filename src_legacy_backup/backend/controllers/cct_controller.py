# src/controllers/cct_controller.py
"""
Controlador para Convenções Coletivas de Trabalho (CCTs).
Implementa lógica de negócios, integração com GCS e BigQuery.
"""
import io
import uuid
import json
import os
import hashlib
from datetime import date, datetime
from fastapi import UploadFile
from typing import List, Optional
from src.schemas_cct import CCTDocumentoResponse, CCTDocumentoCreateRequest, AlertaCCTResponse, UpdateAlertaStatusRequest
from src.utils.gcs_utils import upload_file_to_gcs
from src.utils.bq_utils import BigQueryUtils

# Configurações via variáveis de ambiente
GCP_PROJECT = os.environ.get("GCP_PROJECT")
BQ_DATASET = os.environ.get("BQ_DATASET", "auditoria_folha_dataset")
# Instancia client BigQuery
bq_utils = BigQueryUtils(project_id=GCP_PROJECT)
# Referências para tabelas
TABLE_CCTS = f"{GCP_PROJECT}.{BQ_DATASET}.CCTsDocumentos"
TABLE_CCT_CLIENTES = f"{GCP_PROJECT}.{BQ_DATASET}.CCTsClientesAfetados"

async def salvar_documento_cct_e_metadados(
    file: UploadFile,
    nome_documento_original: str,
    data_inicio_vigencia: date,
    data_fim_vigencia: Optional[date],
    sindicatos_laborais_json_str: Optional[str],
    sindicatos_patronais_json_str: Optional[str],
    numero_registro_mte: Optional[str],
    link_fonte_oficial: Optional[str],
    id_cct_base_fk: Optional[str],
    id_cliente_principal: Optional[str],
    ids_clientes_afetados: Optional[str]
) -> CCTDocumentoResponse:
    # Gera ID único e lê arquivo
    id_cct = str(uuid.uuid4())
    content = await file.read()

    # Upload para GCS
    bucket = os.environ.get("GCS_BUCKET_CCTS", "auditoria360-ccts-docs")
    dest = f"clientes/{id_cliente_principal or 'global'}/{data_inicio_vigencia.year}/{id_cct}/{file.filename}"
    # file.content_type pode ser None
    content_type = file.content_type or 'application/octet-stream'
    gcs_uri = upload_file_to_gcs(bucket, dest, content, content_type)

    # Preparar registro BigQuery
    row = {
        "id_cct_documento": id_cct,
        "id_cliente_principal_associado": id_cliente_principal,
        "nome_documento_original": nome_documento_original,
        "tipo_mime_documento": content_type,
        "tamanho_arquivo_bytes": len(content),
        "hash_conteudo_arquivo": hashlib.sha256(content).hexdigest(),
        "gcs_uri_documento": gcs_uri,
        "usuario_upload": file.filename,
        "data_inicio_vigencia": data_inicio_vigencia.isoformat(),
        "data_fim_vigencia": data_fim_vigencia.isoformat() if data_fim_vigencia else None,
        "sindicatos_laborais": json.loads(sindicatos_laborais_json_str) if sindicatos_laborais_json_str else None,
        "sindicatos_patronais": json.loads(sindicatos_patronais_json_str) if sindicatos_patronais_json_str else None,
        "numero_registro_mte": numero_registro_mte,
        "link_fonte_oficial": link_fonte_oficial,
        "id_cct_base_referencia": id_cct_base_fk,
        "status_processamento_ia": "PENDENTE_EXTRACAO",
        "data_criacao_registro": datetime.now().isoformat(),
        "data_ultima_modificacao": datetime.now().isoformat()
    }
    bq_utils.insert_rows_json(TABLE_CCTS, [row])

    # Insert associações de clientes
    clientes = json.loads(ids_clientes_afetados) if ids_clientes_afetados else []
    if id_cliente_principal:
        clientes.append(id_cliente_principal)
    rows_clientes = []
    for cli in set(clientes):
        rows_clientes.append({
            "id_cct_documento_fk": id_cct,
            "id_cliente_afetado": cli,
            "data_associacao": datetime.now().isoformat(),
            "usuario_associacao": file.filename
        })
    if rows_clientes:
        bq_utils.insert_rows_json(TABLE_CCT_CLIENTES, rows_clientes)

    return CCTDocumentoResponse(
        id_cct_documento=id_cct,
        nome_documento_original=nome_documento_original,
        gcs_uri_documento=gcs_uri,
        data_inicio_vigencia_cct=data_inicio_vigencia,
        data_fim_vigencia_cct=data_fim_vigencia,
        sindicatos_laborais=json.loads(sindicatos_laborais_json_str) if sindicatos_laborais_json_str else None,
        sindicatos_patronais=json.loads(sindicatos_patronais_json_str) if sindicatos_patronais_json_str else None,
        status_processamento_ia="PENDENTE_EXTRACAO"
    )

async def listar_ccts(
    id_cliente_afetado: Optional[str] = None,
    sindicato_nome_contem: Optional[str] = None,
    data_vigencia_em: Optional[date] = None
) -> List[CCTDocumentoResponse]:
    # Constrói a query base com aliases para campos esperados pelo schema
    base_sql = f"SELECT id_cct_documento, nome_documento_original, gcs_uri_documento, " \
               f"data_inicio_vigencia AS data_inicio_vigencia_cct, " \
               f"data_fim_vigencia AS data_fim_vigencia_cct, " \
               f"sindicatos_laborais, sindicatos_patronais, status_processamento_ia " \
               f"FROM `{GCP_PROJECT}.{BQ_DATASET}.CCTsDocumentos`"
    filters = []
    # Filtro por cliente afetado
    if id_cliente_afetado:
        sub = f"SELECT id_cct_documento_fk FROM `{GCP_PROJECT}.{BQ_DATASET}.CCTsClientesAfetados` " \
              f"WHERE id_cliente_afetado = '{id_cliente_afetado}'"
        filters.append(f"id_cct_documento IN ({sub})")
    # Filtro por sindicato (busca substring na coluna JSON)
    if sindicato_nome_contem:
        keyword = sindicato_nome_contem.lower()
        filters.append(
            f"REGEXP_CONTAINS(LOWER(CAST(sindicatos_laborais AS STRING)), r'{keyword}')"
        )
    # Filtro por data de vigência
    if data_vigencia_em:
        date_str = data_vigencia_em.isoformat()
        filters.append(
            f"DATE(data_inicio_vigencia) <= '{date_str}' AND (data_fim_vigencia IS NULL OR DATE(data_fim_vigencia) >= '{date_str}')"
        )
    # Aplica filtros
    if filters:
        base_sql += " WHERE " + " AND ".join(filters)
    # Executa query
    df = bq_utils.fetch_data(base_sql)
    # Converte para lista de schemas
    records = df.to_dict(orient='records') if not df.empty else []
    return [CCTDocumentoResponse(**rec) for rec in records]

async def atualizar_metadata_cct(id_cct: str, payload: CCTDocumentoCreateRequest) -> CCTDocumentoResponse:
    # TODO: Atualizar metadados no BigQuery
    return CCTDocumentoResponse(
        id_cct_documento=id_cct,
        nome_documento_original=payload.nome_documento_original,
        gcs_uri_documento="",
        data_inicio_vigencia_cct=payload.data_inicio_vigencia_cct,
        data_fim_vigencia_cct=payload.data_fim_vigencia_cct,
        sindicatos_laborais=None,
        sindicatos_patronais=None,
        status_processamento_ia="ATUALIZADO"
    )

async def desativar_cct(id_cct: str) -> None:
    # TODO: Marcar registro como inativo no BigQuery
    pass

async def listar_alertas(status: Optional[str] = None) -> List[AlertaCCTResponse]:
    # Lista alertas de CCT do BigQuery, filtrando por status se fornecido
    sql = f"SELECT * FROM `{GCP_PROJECT}.{BQ_DATASET}.AlertasNovasCCTsEncontradas`"
    if status:
        sql += f" WHERE status_alerta = '{status}'"
    df = bq_utils.fetch_data(sql)  # já retorna pandas.DataFrame
    records = df.to_dict(orient='records') if not df.empty else []
    return [AlertaCCTResponse(**row) for row in records]

async def atualizar_status_alerta(id_alerta: str, payload: UpdateAlertaStatusRequest) -> AlertaCCTResponse:
    # Atualiza status e notas de um alerta existente
    update_sql = f"""
        UPDATE `{GCP_PROJECT}.{BQ_DATASET}.AlertasNovasCCTsEncontradas`
        SET status_alerta = '{payload.status_alerta}', notas_admin = '{payload.notas_admin or ''}', data_revisao_admin = CURRENT_TIMESTAMP()
        WHERE id_alerta_cct = '{id_alerta}'
    """
    bq_utils.run_query(update_sql)
    # Busca registro atualizado
    select_sql = f"SELECT * FROM `{GCP_PROJECT}.{BQ_DATASET}.AlertasNovasCCTsEncontradas` WHERE id_alerta_cct = '{id_alerta}'"
    df = bq_utils.fetch_data(select_sql)  # DataFrame
    if df.empty:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    return AlertaCCTResponse(**df.iloc[0].to_dict())
