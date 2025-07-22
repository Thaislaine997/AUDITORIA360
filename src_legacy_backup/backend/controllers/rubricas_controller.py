# Controller para Dicionário de Rubricas Mestre e Rubricas do Cliente
from typing import List, Optional
from fastapi import HTTPException, Depends
from src.schemas import (
    RubricaMestreCreateSchema, RubricaMestreUpdateSchema, RubricaMestreResponseSchema,
    RubricaClienteConfigCreateSchema, RubricaClienteConfigUpdateSchema, RubricaClienteConfigResponseSchema
)
from datetime import datetime
from src.bq_loader import get_bigquery_client
from src.config_manager import get_current_config
from google.cloud import bigquery
import uuid

# --- Rubricas Mestre (BigQuery) ---
def criar_rubrica_mestre(dados: RubricaMestreCreateSchema, config: dict = Depends(get_current_config)) -> RubricaMestreResponseSchema:
    client = get_bigquery_client(config)
    table_id = f"{config['gcp_project_id']}.{config['bq_dataset_id']}.rubricas_mestre"
    now = datetime.now()
    id_rubrica = dados.id_rubrica_mestre or str(uuid.uuid4())
    rubrica_dict = dados.model_dump()
    rubrica_dict.update({
        "id_rubrica_mestre": id_rubrica,
        "data_criacao": now,
        "data_atualizacao": now,
        "ativo": True
    })
    errors = client.insert_rows_json(table_id, [rubrica_dict])
    if errors:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir rubrica mestre: {errors}")
    return RubricaMestreResponseSchema(**rubrica_dict)

def listar_rubricas_mestre(ativo: Optional[bool] = True, config: dict = Depends(get_current_config)) -> List[RubricaMestreResponseSchema]:
    client = get_bigquery_client(config)
    table_id = f"{config['gcp_project_id']}.{config['bq_dataset_id']}.rubricas_mestre"
    query = f"SELECT * FROM `{table_id}`"
    if ativo is not None:
        query += f" WHERE ativo = {str(ativo).upper()}"
    rows = client.query(query).result()
    return [RubricaMestreResponseSchema(**dict(row)) for row in rows]

def obter_rubrica_mestre_por_id(id_rubrica: str, config: dict = Depends(get_current_config)) -> RubricaMestreResponseSchema:
    client = get_bigquery_client(config)
    table_id = f"{config['gcp_project_id']}.{config['bq_dataset_id']}.rubricas_mestre"
    query = f"SELECT * FROM `{table_id}` WHERE id_rubrica_mestre = @id_rubrica LIMIT 1"
    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("id_rubrica", "STRING", id_rubrica)
    ])
    rows = list(client.query(query, job_config=job_config).result())
    if not rows:
        raise HTTPException(status_code=404, detail="Rubrica mestre não encontrada")
    return RubricaMestreResponseSchema(**dict(rows[0]))

def atualizar_rubrica_mestre(id_rubrica: str, dados: RubricaMestreUpdateSchema, usuario: str, config: dict = Depends(get_current_config)) -> RubricaMestreResponseSchema:
    client = get_bigquery_client(config)
    table_id = f"{config['gcp_project_id']}.{config['bq_dataset_id']}.rubricas_mestre"
    now = datetime.now()
    update_data = dados.model_dump(exclude_unset=True)
    update_data["data_atualizacao"] = now
    update_data["usuario_ultima_modificacao"] = usuario
    set_clause = ", ".join([f"{k} = @{k}" for k in update_data.keys()])
    query = f"""
        UPDATE `{table_id}` SET {set_clause}
        WHERE id_rubrica_mestre = @id_rubrica
    """
    params = [bigquery.ScalarQueryParameter("id_rubrica", "STRING", id_rubrica)] + [
        bigquery.ScalarQueryParameter(k, "STRING" if isinstance(v, str) else "BOOL" if isinstance(v, bool) else "TIMESTAMP", v)
        for k, v in update_data.items()
    ]
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    job = client.query(query, job_config=job_config)
    job.result()
    return obter_rubrica_mestre_por_id(id_rubrica, config)

def desativar_rubrica_mestre(id_rubrica: str, usuario: str, config: dict = Depends(get_current_config)) -> RubricaMestreResponseSchema:
    client = get_bigquery_client(config)
    table_id = f"{config['gcp_project_id']}.{config['bq_dataset_id']}.rubricas_mestre"
    now = datetime.now()
    query = f"""
        UPDATE `{table_id}` SET ativo = FALSE, data_atualizacao = @now, usuario_ultima_modificacao = @usuario
        WHERE id_rubrica_mestre = @id_rubrica
    """
    params = [
        bigquery.ScalarQueryParameter("now", "TIMESTAMP", now),
        bigquery.ScalarQueryParameter("usuario", "STRING", usuario),
        bigquery.ScalarQueryParameter("id_rubrica", "STRING", id_rubrica)
    ]
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    job = client.query(query, job_config=job_config)
    job.result()
    return obter_rubrica_mestre_por_id(id_rubrica, config)

# --- Rubricas Cliente (BigQuery) ---
def criar_rubrica_cliente(dados: RubricaClienteConfigCreateSchema, config: dict = Depends(get_current_config)) -> RubricaClienteConfigResponseSchema:
    client = get_bigquery_client(config)
    table_id = f"{config['gcp_project_id']}.{config['bq_dataset_id']}.rubricas_cliente"
    now = datetime.now()
    id_rubrica = dados.id_rubrica_cliente or str(uuid.uuid4())
    rubrica_dict = dados.model_dump()
    rubrica_dict.update({
        "id_rubrica_cliente": id_rubrica,
        "data_criacao_config": now,
        "data_modificacao_config": now,
        "ativo": True
    })
    errors = client.insert_rows_json(table_id, [rubrica_dict])
    if errors:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir rubrica cliente: {errors}")
    return RubricaClienteConfigResponseSchema(**rubrica_dict)

def listar_rubricas_cliente(id_cliente: Optional[str] = None, ativo: Optional[bool] = True, config: dict = Depends(get_current_config)) -> List[RubricaClienteConfigResponseSchema]:
    client = get_bigquery_client(config)
    table_id = f"{config['gcp_project_id']}.{config['bq_dataset_id']}.rubricas_cliente"
    query = f"SELECT * FROM `{table_id}`"
    where_clauses = []
    if id_cliente is not None:
        where_clauses.append(f"id_cliente = '{id_cliente}'")
    if ativo is not None:
        where_clauses.append(f"ativo = {str(ativo).upper()}")
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    rows = client.query(query).result()
    return [RubricaClienteConfigResponseSchema(**dict(row)) for row in rows]

def obter_rubrica_cliente_por_id(id_rubrica: str, config: dict = Depends(get_current_config)) -> RubricaClienteConfigResponseSchema:
    client = get_bigquery_client(config)
    table_id = f"{config['gcp_project_id']}.{config['bq_dataset_id']}.rubricas_cliente"
    query = f"SELECT * FROM `{table_id}` WHERE id_rubrica_cliente = @id_rubrica LIMIT 1"
    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ScalarQueryParameter("id_rubrica", "STRING", id_rubrica)
    ])
    rows = list(client.query(query, job_config=job_config).result())
    if not rows:
        raise HTTPException(status_code=404, detail="Rubrica cliente não encontrada")
    return RubricaClienteConfigResponseSchema(**dict(rows[0]))

def atualizar_rubrica_cliente(id_rubrica: str, dados: RubricaClienteConfigUpdateSchema, usuario: str, config: dict = Depends(get_current_config)) -> RubricaClienteConfigResponseSchema:
    client = get_bigquery_client(config)
    table_id = f"{config['gcp_project_id']}.{config['bq_dataset_id']}.rubricas_cliente"
    now = datetime.now()
    update_data = dados.model_dump(exclude_unset=True)
    update_data["data_modificacao_config"] = now
    update_data["usuario_modificacao_config"] = usuario
    set_clause = ", ".join([f"{k} = @{k}" for k in update_data.keys()])
    query = f"""
        UPDATE `{table_id}` SET {set_clause}
        WHERE id_rubrica_cliente = @id_rubrica
    """
    params = [bigquery.ScalarQueryParameter("id_rubrica", "STRING", id_rubrica)]
    for k, v in update_data.items():
        tipo = "STRING" if isinstance(v, str) else "BOOL" if isinstance(v, bool) else "TIMESTAMP"
        params.append(bigquery.ScalarQueryParameter(k, tipo, v))
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    job = client.query(query, job_config=job_config)
    job.result()
    return obter_rubrica_cliente_por_id(id_rubrica, config)

def desativar_rubrica_cliente(id_rubrica: str, usuario: str, config: dict = Depends(get_current_config)) -> RubricaClienteConfigResponseSchema:
    client = get_bigquery_client(config)
    table_id = f"{config['gcp_project_id']}.{config['bq_dataset_id']}.rubricas_cliente"
    now = datetime.now()
    query = f"""
        UPDATE `{table_id}` SET ativo = FALSE, data_modificacao_config = @now, usuario_modificacao_config = @usuario
        WHERE id_rubrica_cliente = @id_rubrica
    """
    params = [
        bigquery.ScalarQueryParameter("now", "TIMESTAMP", now),
        bigquery.ScalarQueryParameter("usuario", "STRING", usuario),
        bigquery.ScalarQueryParameter("id_rubrica", "STRING", id_rubrica)
    ]
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    job = client.query(query, job_config=job_config)
    job.result()
    return obter_rubrica_cliente_por_id(id_rubrica, config)
