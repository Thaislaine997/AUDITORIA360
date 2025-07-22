from fastapi import HTTPException
from src.schemas_models import TabelaINSS, TabelaIRRF, TabelaSalarioFamilia, TabelaSalarioMinimo, TabelaFGTS
from google.cloud import bigquery
from datetime import datetime, date, timedelta
from typing import Optional, List
import uuid
import json

PROJECT_ID = "auditoria-folha"
DATASET_ID = "Tabelas_legais_dataseet"
TABLE_ID_INSS = "ParametrosLegais_INSS_Historico"
TABLE_ID_IRRF = "ParametrosLegais_IRRF_Historico"
TABLE_ID_SALARIO_FAMILIA = "ParametrosLegais_SalarioFamilia_Historico"
TABLE_ID_SALARIO_MINIMO = "TabelaSalarioMinimoHistorico"
TABLE_ID_FGTS = "TabelaFGTSParametros"
TABLE_ID_LOG_VERIFICACAO = "LogVerificacaoManualParametros"

async def _verificar_conflito_vigencia(
    client: bigquery.Client,
    table_id: str,
    data_inicio_nova: date,
    data_fim_nova: Optional[date],
    id_versao_ignorada: Optional[str] = None
):
    query_params = [
        bigquery.ScalarQueryParameter("data_inicio_nova", "DATE", data_inicio_nova),
        bigquery.ScalarQueryParameter("data_fim_nova", "DATE", data_fim_nova if data_fim_nova else None),
        bigquery.ScalarQueryParameter("id_versao_ignorada", "STRING", id_versao_ignorada if id_versao_ignorada else None),
    ]

    query = f"""
        SELECT id_versao, data_inicio_vigencia, data_fim_vigencia
        FROM `{PROJECT_ID}.{DATASET_ID}.{table_id}`
        WHERE
            data_inativacao IS NULL
            AND (@id_versao_ignorada IS NULL OR id_versao != @id_versao_ignorada)
            AND (
                (
                    @data_fim_nova IS NOT NULL AND
                    data_inicio_vigencia <= @data_fim_nova AND
                    (data_fim_vigencia IS NULL OR data_fim_vigencia >= @data_inicio_nova)
                )
                OR
                (
                    @data_fim_nova IS NULL AND
                    (data_fim_vigencia IS NULL OR data_fim_vigencia >= @data_inicio_nova)
                )
            )
        LIMIT 1
    """
    
    job_config = bigquery.QueryJobConfig(query_parameters=query_params)
    
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        conflito = None
        for row in results:
            conflito = row
            break 
        
        if conflito:
            mensagem = (
                f"Conflito de vigência detectado com a tabela existente (id_versao: {conflito['id_versao']}). "
                f"Período existente: {conflito['data_inicio_vigencia']} até {conflito['data_fim_vigencia'] if conflito['data_fim_vigencia'] else 'aberto'}. "
                f"Período da nova tabela: {data_inicio_nova} até {data_fim_nova if data_fim_nova else 'aberto'}."
            )
            raise HTTPException(status_code=409, detail=mensagem)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao verificar conflito de vigência na tabela {table_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno ao verificar conflito de vigência: {str(e)}")

async def criar_nova_tabela_inss(tabela_inss_data: TabelaINSS) -> TabelaINSS:
    client = bigquery.Client(project=PROJECT_ID)
    
    tabela_inss_data.id_versao = str(uuid.uuid4())
    now = datetime.now()
    tabela_inss_data.data_criacao_registro = now
    tabela_inss_data.data_ultima_modificacao = now
    tabela_inss_data.data_inativacao = None

    await _verificar_conflito_vigencia(
        client,
        TABLE_ID_INSS,
        tabela_inss_data.data_inicio_vigencia,
        tabela_inss_data.data_fim_vigencia
    )
    
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_INSS)
    row_to_insert = tabela_inss_data.model_dump(by_alias=True)
    errors = client.insert_rows_json(table_ref, [row_to_insert])

    if not errors:
        return tabela_inss_data
    else:
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        print(f"Erro ao inserir nova versão da tabela INSS no BigQuery: {detailed_error_message}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar nova tabela INSS no BigQuery. Detalhes: {detailed_error_message}")

async def criar_nova_tabela_irrf(tabela_irrf_data: TabelaIRRF) -> TabelaIRRF:
    client = bigquery.Client(project=PROJECT_ID)

    tabela_irrf_data.id_versao = str(uuid.uuid4())
    now = datetime.now()
    tabela_irrf_data.data_criacao_registro = now
    tabela_irrf_data.data_ultima_modificacao = now
    tabela_irrf_data.data_inativacao = None

    await _verificar_conflito_vigencia(
        client,
        TABLE_ID_IRRF,
        tabela_irrf_data.data_inicio_vigencia,
        tabela_irrf_data.data_fim_vigencia
    )

    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_IRRF)
    row_to_insert = tabela_irrf_data.model_dump(by_alias=True)
    errors = client.insert_rows_json(table_ref, [row_to_insert])
    
    if not errors:
        return tabela_irrf_data
    else:
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        print(f"Erro ao inserir nova versão da tabela IRRF no BigQuery: {detailed_error_message}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar nova tabela IRRF no BigQuery. Detalhes: {detailed_error_message}")

async def criar_nova_tabela_salario_familia(tabela_sf_data: TabelaSalarioFamilia) -> TabelaSalarioFamilia:
    client = bigquery.Client(project=PROJECT_ID)

    tabela_sf_data.id_versao = str(uuid.uuid4())
    now = datetime.now()
    tabela_sf_data.data_criacao_registro = now
    tabela_sf_data.data_ultima_modificacao = now
    tabela_sf_data.data_inativacao = None

    await _verificar_conflito_vigencia(
        client,
        TABLE_ID_SALARIO_FAMILIA,
        tabela_sf_data.data_inicio_vigencia,
        tabela_sf_data.data_fim_vigencia
    )

    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_SALARIO_FAMILIA)
    row_to_insert = tabela_sf_data.model_dump(by_alias=True)
    errors = client.insert_rows_json(table_ref, [row_to_insert])
    
    if not errors:
        return tabela_sf_data
    else:
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        print(f"Erro ao inserir nova versão da tabela Salário Família no BigQuery: {detailed_error_message}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar nova tabela Salário Família no BigQuery. Detalhes: {detailed_error_message}")

async def criar_nova_tabela_salario_minimo(tabela_sm_data: TabelaSalarioMinimo) -> TabelaSalarioMinimo:
    client = bigquery.Client(project=PROJECT_ID)
    
    tabela_sm_data.id_versao = str(uuid.uuid4())
    now = datetime.now()
    tabela_sm_data.data_criacao_registro = now
    tabela_sm_data.data_ultima_modificacao = now
    tabela_sm_data.data_inativacao = None

    await _verificar_conflito_vigencia(
        client,
        TABLE_ID_SALARIO_MINIMO,
        tabela_sm_data.data_inicio_vigencia,
        tabela_sm_data.data_fim_vigencia
    )
    
    row_to_insert = tabela_sm_data.model_dump(by_alias=True)
    if row_to_insert.get('valores_regionais') is not None:
        row_to_insert['valores_regionais'] = json.dumps(row_to_insert['valores_regionais'])
    else:
        row_to_insert['valores_regionais'] = None

    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_SALARIO_MINIMO)
    errors = client.insert_rows_json(table_ref, [row_to_insert])

    if not errors:
        return tabela_sm_data
    else:
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        print(f"Erro ao inserir nova versão da tabela Salário Mínimo no BigQuery: {detailed_error_message}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar nova tabela Salário Mínimo no BigQuery. Detalhes: {detailed_error_message}")

async def criar_nova_tabela_fgts(tabela_fgts_data: TabelaFGTS) -> TabelaFGTS:
    client = bigquery.Client(project=PROJECT_ID)
    
    tabela_fgts_data.id_versao = str(uuid.uuid4())
    now = datetime.now()
    tabela_fgts_data.data_criacao_registro = now
    tabela_fgts_data.data_ultima_modificacao = now
    tabela_fgts_data.data_inativacao = None

    await _verificar_conflito_vigencia(
        client,
        TABLE_ID_FGTS,
        tabela_fgts_data.data_inicio_vigencia,
        tabela_fgts_data.data_fim_vigencia
    )
    
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_FGTS)
    row_to_insert = tabela_fgts_data.model_dump(by_alias=True)
    errors = client.insert_rows_json(table_ref, [row_to_insert])

    if not errors:
        return tabela_fgts_data
    else:
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        print(f"Erro ao inserir nova versão da tabela FGTS no BigQuery: {detailed_error_message}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar nova tabela FGTS no BigQuery. Detalhes: {detailed_error_message}")

async def listar_tabelas_inss(skip: int = 0, limit: int = 100) -> List[TabelaINSS]:
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_INSS}`
        WHERE data_inativacao IS NULL
        ORDER BY data_inicio_vigencia DESC, data_criacao_registro DESC
        LIMIT @limit OFFSET @skip
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
            bigquery.ScalarQueryParameter("skip", "INT64", skip),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        tabelas = [TabelaINSS(**dict(row)) for row in results]
        return tabelas
    except Exception as e:
        print(f"Erro ao listar tabelas INSS do BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados do INSS no BigQuery: {str(e)}")

async def listar_tabelas_irrf(skip: int = 0, limit: int = 100) -> List[TabelaIRRF]:
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_IRRF}`
        WHERE data_inativacao IS NULL
        ORDER BY data_inicio_vigencia DESC, data_criacao_registro DESC
        LIMIT @limit OFFSET @skip
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
            bigquery.ScalarQueryParameter("skip", "INT64", skip),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        tabelas = [TabelaIRRF(**dict(row)) for row in results]
        return tabelas
    except Exception as e:
        print(f"Erro ao listar tabelas IRRF do BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados do IRRF no BigQuery: {str(e)}")

async def listar_tabelas_salario_familia(skip: int = 0, limit: int = 100) -> List[TabelaSalarioFamilia]:
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_SALARIO_FAMILIA}`
        WHERE data_inativacao IS NULL
        ORDER BY data_inicio_vigencia DESC, data_criacao_registro DESC
        LIMIT @limit OFFSET @skip
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
            bigquery.ScalarQueryParameter("skip", "INT64", skip),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        tabelas = [TabelaSalarioFamilia(**dict(row)) for row in results]
        return tabelas
    except Exception as e:
        print(f"Erro ao listar tabelas Salário Família do BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados do Salário Família no BigQuery: {str(e)}")

async def listar_tabelas_salario_minimo(skip: int = 0, limit: int = 100) -> List[TabelaSalarioMinimo]:
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_SALARIO_MINIMO}`
        WHERE data_inativacao IS NULL
        ORDER BY data_inicio_vigencia DESC, data_criacao_registro DESC
        LIMIT @limit OFFSET @skip
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
            bigquery.ScalarQueryParameter("skip", "INT64", skip),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        tabelas = []
        for row in results:
            row_dict = dict(row)
            if 'valores_regionais' in row_dict and isinstance(row_dict['valores_regionais'], str):
                try:
                    row_dict['valores_regionais'] = json.loads(row_dict['valores_regionais'])
                except json.JSONDecodeError:
                    row_dict['valores_regionais'] = None
            elif 'valores_regionais' not in row_dict:
                 row_dict['valores_regionais'] = None
            tabelas.append(TabelaSalarioMinimo(**row_dict))
        return tabelas
    except Exception as e:
        print(f"Erro ao listar tabelas Salário Mínimo do BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados do Salário Mínimo no BigQuery: {str(e)}")

async def listar_tabelas_fgts(skip: int = 0, limit: int = 100) -> List[TabelaFGTS]:
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_FGTS}`
        WHERE data_inativacao IS NULL
        ORDER BY data_inicio_vigencia DESC, data_criacao_registro DESC
        LIMIT @limit OFFSET @skip
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("limit", "INT64", limit),
            bigquery.ScalarQueryParameter("skip", "INT64", skip),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        tabelas = [TabelaFGTS(**dict(row)) for row in results]
        return tabelas
    except Exception as e:
        print(f"Erro ao listar tabelas FGTS do BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados do FGTS no BigQuery: {str(e)}")

async def obter_tabela_inss_por_id(id_versao: str) -> TabelaINSS:
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_INSS}`
        WHERE id_versao = @id_versao
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_versao", "STRING", id_versao),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        row = None
        for r in results: 
            row = r
            break
        
        if row:
            return TabelaINSS(**dict(row))
        else:
            raise HTTPException(status_code=404, detail=f"Versão da tabela INSS com id_versao '{id_versao}' não encontrada.")
    except Exception as e:
        print(f"Erro ao obter tabela INSS por id_versao do BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados da tabela INSS no BigQuery: {str(e)}")

async def obter_tabela_irrf_por_id(id_versao: str) -> TabelaIRRF:
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_IRRF}`
        WHERE id_versao = @id_versao
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_versao", "STRING", id_versao),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        row = None
        for r in results:
            row = r
            break
            
        if row:
            return TabelaIRRF(**dict(row))
        else:
            raise HTTPException(status_code=404, detail=f"Versão da tabela IRRF com id_versao '{id_versao}' não encontrada.")
    except Exception as e:
        print(f"Erro ao obter tabela IRRF por id_versao do BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados da tabela IRRF no BigQuery: {str(e)}")

async def obter_tabela_salario_familia_por_id(id_versao: str) -> TabelaSalarioFamilia:
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_SALARIO_FAMILIA}`
        WHERE id_versao = @id_versao
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_versao", "STRING", id_versao),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()

        row = None
        for r in results:
            row = r
            break

        if row:
            return TabelaSalarioFamilia(**dict(row))
        else:
            raise HTTPException(status_code=404, detail=f"Versão da tabela Salário Família com id_versao '{id_versao}' não encontrada.")
    except Exception as e:
        print(f"Erro ao obter tabela Salário Família por id_versao do BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados da tabela Salário Família no BigQuery: {str(e)}")

async def obter_tabela_salario_minimo_por_id(id_versao: str) -> TabelaSalarioMinimo:
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_SALARIO_MINIMO}`
        WHERE id_versao = @id_versao
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_versao", "STRING", id_versao),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        row = None
        for r in results: 
            row = r
            break
        
        if row:
            row_dict = dict(row)
            if 'valores_regionais' in row_dict and isinstance(row_dict['valores_regionais'], str):
                try:
                    row_dict['valores_regionais'] = json.loads(row_dict['valores_regionais'])
                except json.JSONDecodeError:
                    row_dict['valores_regionais'] = None
            elif 'valores_regionais' not in row_dict:
                 row_dict['valores_regionais'] = None
            return TabelaSalarioMinimo(**row_dict)
        else:
            raise HTTPException(status_code=404, detail=f"Versão da tabela Salário Mínimo com id_versao '{id_versao}' não encontrada.")
    except Exception as e:
        print(f"Erro ao obter tabela Salário Mínimo por id_versao do BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados da tabela Salário Mínimo no BigQuery: {str(e)}")

async def obter_tabela_fgts_por_id(id_versao: str) -> TabelaFGTS:
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_FGTS}`
        WHERE id_versao = @id_versao
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_versao", "STRING", id_versao),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        row = None
        for r in results:
            row = r
            break
            
        if row:
            return TabelaFGTS(**dict(row))
        else:
            raise HTTPException(status_code=404, detail=f"Versão da tabela FGTS com id_versao '{id_versao}' não encontrada.")
    except Exception as e:
        print(f"Erro ao obter tabela FGTS por id_versao do BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados da tabela FGTS no BigQuery: {str(e)}")

async def atualizar_tabela_inss(id_versao_anterior: str, tabela_inss_update_data: TabelaINSS) -> TabelaINSS:
    client = bigquery.Client(project=PROJECT_ID)
    now = datetime.now()

    # 1. Obter e validar a versão anterior
    try:
        versao_anterior = await obter_tabela_inss_por_id(id_versao_anterior)
        if versao_anterior.data_inativacao:
            raise HTTPException(status_code=400, detail=f"A versão anterior (id: {id_versao_anterior}) da tabela INSS já está inativada e não pode ser a base para uma atualização.")
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Versão anterior da tabela INSS (id: {id_versao_anterior}) não encontrada para ser atualizada.")
        raise e 
    except Exception as e: 
        print(f"Erro inesperado ao buscar versão anterior da tabela INSS para atualização: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao verificar versão anterior da tabela INSS: {str(e)}")

    # 2. Determinar se a versão anterior precisa ser fechada e calcular a nova data de fim de vigência
    fechar_versao_anterior = False
    nova_data_fim_vigencia_anterior = None

    if tabela_inss_update_data.data_inicio_vigencia > versao_anterior.data_inicio_vigencia:
        # A nova tabela começa depois da anterior.
        # Se a anterior está aberta ou se sobrepõe, precisamos fechá-la.
        if versao_anterior.data_fim_vigencia is None or versao_anterior.data_fim_vigencia >= tabela_inss_update_data.data_inicio_vigencia:
            fechar_versao_anterior = True
            nova_data_fim_vigencia_anterior = tabela_inss_update_data.data_inicio_vigencia - timedelta(days=1)
            
            # Validação para garantir que a nova data de fim não seja anterior à data de início da versão anterior
            if nova_data_fim_vigencia_anterior < versao_anterior.data_inicio_vigencia:
                raise HTTPException(
                    status_code=409, # Conflito
                    detail=(
                        f"Conflito ao tentar fechar a vigência da tabela INSS anterior (id: {id_versao_anterior}). "
                        f"A nova data de início ({tabela_inss_update_data.data_inicio_vigencia}) resultaria em uma data de fim ({nova_data_fim_vigencia_anterior}) "
                        f"anterior à data de início existente ({versao_anterior.data_inicio_vigencia}) para a tabela anterior."
                    )
                )
    # Não permitir que a data de início da nova versão seja anterior à data de início da versão base
    elif tabela_inss_update_data.data_inicio_vigencia < versao_anterior.data_inicio_vigencia:
        raise HTTPException(
            status_code=400,
            detail=f"A data de início da nova tabela ({tabela_inss_update_data.data_inicio_vigencia}) "
                   f"não pode ser anterior à data de início da tabela base ({versao_anterior.data_inicio_vigencia})."
        )
    # Se as datas de início são iguais, a atualização é uma substituição direta da versão anterior.
    # A versão anterior será inativada, e uma nova será criada com os mesmos dados de vigência (ou novos, se fornecidos).
    # Neste caso, não "fechamos" a vigência da anterior com uma data_fim_vigencia, mas a inativamos.
    # No entanto, o fluxo atual de "atualizar" implica criar uma nova entrada e, opcionalmente, fechar a anterior.
    # Se a intenção é uma edição direta da versão existente (sem criar nova), seria outra lógica (PUT no mesmo ID).
    # Assumindo que "atualizar" sempre cria uma nova versão e a anterior é ajustada/fechada.

    # 3. Fechar a vigência da versão anterior, se necessário
    if fechar_versao_anterior and nova_data_fim_vigencia_anterior is not None:
        query_update_anterior = f"""
            UPDATE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_INSS}`
            SET 
                data_fim_vigencia = @nova_data_fim, 
                data_ultima_modificacao = @mod_time
            WHERE id_versao = @id_anterior AND data_inativacao IS NULL 
        """ # Corrigido aqui para f""" em vez de f\"\"\"
        job_config_update = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("nova_data_fim", "DATE", nova_data_fim_vigencia_anterior),
                bigquery.ScalarQueryParameter("mod_time", "TIMESTAMP", now),
                bigquery.ScalarQueryParameter("id_anterior", "STRING", id_versao_anterior),
            ]
        )
        try:
            update_job = client.query(query_update_anterior, job_config=job_config_update)
            update_job.result() # Aguarda a conclusão
            # Verificar se alguma linha foi realmente afetada
            if update_job.num_dml_affected_rows is None or update_job.num_dml_affected_rows == 0:
                # Isso pode acontecer se a tabela já foi fechada ou inativada por outro processo
                # ou se o ID não correspondeu a uma tabela ativa.
                # Considerar se isso deve ser um erro crítico ou um aviso.
                # Por ora, vamos lançar um erro se a intenção era fechar e nada foi alterado.
                error_msg = (
                    f"Falha ao tentar fechar a vigência da tabela INSS anterior (id: {id_versao_anterior}). "
                    "Nenhuma linha foi afetada pela atualização. A tabela anterior pode já estar inativada ou não foi encontrada."
                )
                print(error_msg) # Log para o servidor
                # Não vamos levantar exceção aqui, pois a criação da nova tabela é o principal.
                # Apenas logamos, pois a nova tabela ainda pode ser válida.
                # No entanto, se a lógica de negócio EXIGE que a anterior seja fechada, uma exceção seria apropriada.
                # Re-avaliando: se fechar_versao_anterior é True, esperamos que algo aconteça.
                raise HTTPException(status_code=500, detail=error_msg)

        except Exception as e:
            print(f"Erro ao fechar vigência da tabela INSS anterior (id: {id_versao_anterior}): {e}")
            raise HTTPException(status_code=500, detail=f"Erro técnico ao tentar fechar vigência da tabela INSS anterior: {str(e)}")

    # 4. Preparar e inserir a nova versão da tabela
    nova_id_versao = str(uuid.uuid4())
    tabela_inss_update_data.id_versao = nova_id_versao
    tabela_inss_update_data.data_criacao_registro = now
    tabela_inss_update_data.data_ultima_modificacao = now
    tabela_inss_update_data.data_inativacao = None # Nova tabela sempre ativa

    # Verificar conflito de vigência para a nova tabela (ignorando a si mesma, o que não é o caso aqui pois é nova)
    # E também ignorando a versão anterior que acabamos de (tentar) fechar, se aplicável.
    # A lógica de _verificar_conflito_vigencia já lida com não conflitar com si mesma se um ID for passado.
    # Aqui, como é uma nova tabela, não passamos id_versao_ignorada para ela.
    # O conflito principal seria com outras tabelas ativas.
    await _verificar_conflito_vigencia(
        client,
        TABLE_ID_INSS,
        tabela_inss_update_data.data_inicio_vigencia,
        tabela_inss_update_data.data_fim_vigencia,
        id_versao_ignorada=None # Não estamos editando uma tabela existente, mas criando uma nova
                                # A versão anterior já foi (ou deveria ter sido) tratada.
    )
    
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_INSS)
    row_to_insert = tabela_inss_update_data.model_dump(by_alias=True)
    
    errors = client.insert_rows_json(table_ref, [row_to_insert])

    if not errors:
        return tabela_inss_update_data
    else:
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        print(f"Erro ao inserir nova versão da tabela INSS no BigQuery: {detailed_error_message}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar (criar nova versão) dados da tabela INSS no BigQuery. Detalhes: {detailed_error_message}")

async def atualizar_tabela_irrf(id_versao_anterior: str, tabela_irrf_update_data: TabelaIRRF) -> TabelaIRRF:
    client = bigquery.Client(project=PROJECT_ID)
    now = datetime.now()

    try:
        versao_anterior = await obter_tabela_irrf_por_id(id_versao_anterior)
        if versao_anterior.data_inativacao:
            raise HTTPException(status_code=400, detail=f"A versão anterior (id: {id_versao_anterior}) da tabela IRRF já está inativada e não pode ser a base para uma atualização.")
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Versão anterior da tabela IRRF (id: {id_versao_anterior}) não encontrada para ser atualizada.")
        raise e
    except Exception as e:
        print(f"Erro inesperado ao buscar versão anterior da tabela IRRF para atualização: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao verificar versão anterior da tabela IRRF: {str(e)}")

    fechar_versao_anterior = False
    nova_data_fim_vigencia_anterior = None

    if tabela_irrf_update_data.data_inicio_vigencia > versao_anterior.data_inicio_vigencia:
        if versao_anterior.data_fim_vigencia is None or versao_anterior.data_fim_vigencia >= tabela_irrf_update_data.data_inicio_vigencia:
            fechar_versao_anterior = True
            nova_data_fim_vigencia_anterior = tabela_irrf_update_data.data_inicio_vigencia - timedelta(days=1)
            
            if nova_data_fim_vigencia_anterior < versao_anterior.data_inicio_vigencia:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Conflito ao tentar fechar a vigência da tabela IRRF anterior (id: {id_versao_anterior}). "
                        f"A nova data de início ({tabela_irrf_update_data.data_inicio_vigencia}) resultaria em uma data de fim ({nova_data_fim_vigencia_anterior}) "
                        f"anterior à data de início existente ({versao_anterior.data_inicio_vigencia}) para a tabela anterior."
                    )
                )
    
    if fechar_versao_anterior and nova_data_fim_vigencia_anterior is not None:
        query_update_anterior = f"""
            UPDATE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_IRRF}`
            SET data_fim_vigencia = @nova_data_fim, data_ultima_modificacao = @mod_time
            WHERE id_versao = @id_anterior AND data_inativacao IS NULL
        """
        job_config_update = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("nova_data_fim", "DATE", nova_data_fim_vigencia_anterior),
                bigquery.ScalarQueryParameter("mod_time", "TIMESTAMP", now),
                bigquery.ScalarQueryParameter("id_anterior", "STRING", id_versao_anterior),
            ]
        )
        try:
            update_job = client.query(query_update_anterior, job_config=job_config_update)
            update_job.result()
            if update_job.num_dml_affected_rows is None or update_job.num_dml_affected_rows == 0:
                error_msg = (
                    f"Falha ao tentar fechar a vigência da tabela IRRF anterior (id: {id_versao_anterior}). "
                    "Nenhuma linha foi afetada pela atualização. A tabela anterior pode já estar inativada ou não foi encontrada."
                )
                print(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            print(f"Erro ao fechar vigência da tabela IRRF anterior (id: {id_versao_anterior}): {e}")
            raise HTTPException(status_code=500, detail=f"Erro técnico ao tentar fechar vigência da tabela IRRF anterior: {str(e)}")

    nova_id_versao = str(uuid.uuid4())
    tabela_irrf_update_data.id_versao = nova_id_versao
    tabela_irrf_update_data.data_criacao_registro = now
    tabela_irrf_update_data.data_ultima_modificacao = now
    tabela_irrf_update_data.data_inativacao = None 

    await _verificar_conflito_vigencia(
        client,
        TABLE_ID_IRRF,
        tabela_irrf_update_data.data_inicio_vigencia,
        tabela_irrf_update_data.data_fim_vigencia,
        id_versao_ignorada=None 
    )
    
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_IRRF)
    row_to_insert = tabela_irrf_update_data.model_dump(by_alias=True)
    errors = client.insert_rows_json(table_ref, [row_to_insert])

    if not errors:
        return tabela_irrf_update_data
    else:
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        print(f"Erro ao inserir nova versão da tabela IRRF no BigQuery: {detailed_error_message}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar (criar nova versão) dados da tabela IRRF no BigQuery. Detalhes: {detailed_error_message}")


async def atualizar_tabela_salario_familia(id_versao_anterior: str, tabela_sf_update_data: TabelaSalarioFamilia) -> TabelaSalarioFamilia:
    client = bigquery.Client(project=PROJECT_ID)
    now = datetime.now()

    try:
        versao_anterior = await obter_tabela_salario_familia_por_id(id_versao_anterior)
        if versao_anterior.data_inativacao:
            raise HTTPException(status_code=400, detail=f"A versão anterior (id: {id_versao_anterior}) da tabela Salário Família já está inativada e não pode ser a base para uma atualização.")
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Versão anterior da tabela Salário Família (id: {id_versao_anterior}) não encontrada para ser atualizada.")
        raise e
    except Exception as e:
        print(f"Erro inesperado ao buscar versão anterior da tabela Salário Família para atualização: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao verificar versão anterior da tabela Salário Família: {str(e)}")

    fechar_versao_anterior = False
    nova_data_fim_vigencia_anterior = None

    if tabela_sf_update_data.data_inicio_vigencia > versao_anterior.data_inicio_vigencia:
        if versao_anterior.data_fim_vigencia is None or versao_anterior.data_fim_vigencia >= tabela_sf_update_data.data_inicio_vigencia:
            fechar_versao_anterior = True
            nova_data_fim_vigencia_anterior = tabela_sf_update_data.data_inicio_vigencia - timedelta(days=1)
            
            if nova_data_fim_vigencia_anterior < versao_anterior.data_inicio_vigencia:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Conflito ao tentar fechar a vigência da tabela Salário Família anterior (id: {id_versao_anterior}). "
                        f"A nova data de início ({tabela_sf_update_data.data_inicio_vigencia}) resultaria em uma data de fim ({nova_data_fim_vigencia_anterior}) "
                        f"anterior à data de início existente ({versao_anterior.data_inicio_vigencia}) para a tabela anterior."
                    )
                )
    
    if fechar_versao_anterior and nova_data_fim_vigencia_anterior is not None:
        query_update_anterior = f"""
            UPDATE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_SALARIO_FAMILIA}`
            SET data_fim_vigencia = @nova_data_fim, data_ultima_modificacao = @mod_time
            WHERE id_versao = @id_anterior AND data_inativacao IS NULL
        """
        job_config_update = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("nova_data_fim", "DATE", nova_data_fim_vigencia_anterior),
                bigquery.ScalarQueryParameter("mod_time", "TIMESTAMP", now),
                bigquery.ScalarQueryParameter("id_anterior", "STRING", id_versao_anterior),
            ]
        )
        try:
            update_job = client.query(query_update_anterior, job_config=job_config_update)
            update_job.result()
            if update_job.num_dml_affected_rows is None or update_job.num_dml_affected_rows == 0:
                error_msg = (
                    f"Falha ao tentar fechar a vigência da tabela Salário Família anterior (id: {id_versao_anterior}). "
                    "Nenhuma linha foi afetada pela atualização. A tabela anterior pode já estar inativada ou não foi encontrada."
                )
                print(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            print(f"Erro ao fechar vigência da tabela Salário Família anterior (id: {id_versao_anterior}): {e}")
            raise HTTPException(status_code=500, detail=f"Erro técnico ao tentar fechar vigência da tabela Salário Família anterior: {str(e)}")

    nova_id_versao = str(uuid.uuid4())
    tabela_sf_update_data.id_versao = nova_id_versao
    tabela_sf_update_data.data_criacao_registro = now
    tabela_sf_update_data.data_ultima_modificacao = now
    tabela_sf_update_data.data_inativacao = None

    await _verificar_conflito_vigencia(
        client,
        TABLE_ID_SALARIO_FAMILIA,
        tabela_sf_update_data.data_inicio_vigencia,
        tabela_sf_update_data.data_fim_vigencia,
        id_versao_ignorada=None
    )
    
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_SALARIO_FAMILIA)
    row_to_insert = tabela_sf_update_data.model_dump(by_alias=True)
    errors = client.insert_rows_json(table_ref, [row_to_insert])

    if not errors:
        return tabela_sf_update_data
    else:
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        print(f"Erro ao inserir nova versão da tabela Salário Família no BigQuery: {detailed_error_message}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar (criar nova versão) dados da tabela Salário Família no BigQuery. Detalhes: {detailed_error_message}")

async def atualizar_tabela_salario_minimo(id_versao_anterior: str, tabela_sm_update_data: TabelaSalarioMinimo) -> TabelaSalarioMinimo:
    client = bigquery.Client(project=PROJECT_ID)
    now = datetime.now()

    try:
        versao_anterior = await obter_tabela_salario_minimo_por_id(id_versao_anterior)
        if versao_anterior.data_inativacao:
            raise HTTPException(status_code=400, detail=f"A versão anterior (id: {id_versao_anterior}) da tabela Salário Mínimo já está inativada e não pode ser a base para uma atualização.")
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Versão anterior da tabela Salário Mínimo (id: {id_versao_anterior}) não encontrada para ser atualizada.")
        raise e
    except Exception as e: 
        print(f"Erro inesperado ao buscar versão anterior da tabela Salário Mínimo para atualização: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao verificar versão anterior da tabela Salário Mínimo: {str(e)}")

    fechar_versao_anterior = False
    nova_data_fim_vigencia_anterior = None

    if tabela_sm_update_data.data_inicio_vigencia > versao_anterior.data_inicio_vigencia:
        if versao_anterior.data_fim_vigencia is None or versao_anterior.data_fim_vigencia >= tabela_sm_update_data.data_inicio_vigencia:
            fechar_versao_anterior = True
            nova_data_fim_vigencia_anterior = tabela_sm_update_data.data_inicio_vigencia - timedelta(days=1)
            
            if nova_data_fim_vigencia_anterior < versao_anterior.data_inicio_vigencia:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Conflito ao tentar fechar a vigência da tabela Salário Mínimo anterior (id: {id_versao_anterior}). "
                        f"A nova data de início ({tabela_sm_update_data.data_inicio_vigencia}) resultaria em uma data de fim ({nova_data_fim_vigencia_anterior}) "
                        f"anterior à data de início existente ({versao_anterior.data_inicio_vigencia}) para a tabela anterior."
                    )
                )
    
    if fechar_versao_anterior and nova_data_fim_vigencia_anterior is not None:
        query_update_anterior = f"""
            UPDATE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_SALARIO_MINIMO}`
            SET data_fim_vigencia = @nova_data_fim, data_ultima_modificacao = @mod_time
            WHERE id_versao = @id_anterior AND data_inativacao IS NULL
        """
        job_config_update = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("nova_data_fim", "DATE", nova_data_fim_vigencia_anterior),
                bigquery.ScalarQueryParameter("mod_time", "TIMESTAMP", now),
                bigquery.ScalarQueryParameter("id_anterior", "STRING", id_versao_anterior),
            ]
        )
        try:
            update_job = client.query(query_update_anterior, job_config=job_config_update)
            update_job.result() 
            if update_job.num_dml_affected_rows is None or update_job.num_dml_affected_rows == 0:
                error_msg = (
                    f"Falha ao tentar fechar a vigência da tabela Salário Mínimo anterior (id: {id_versao_anterior}). "
                    "Nenhuma linha foi afetada pela atualização. A tabela anterior pode já estar inativada ou não foi encontrada."
                )
                print(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            print(f"Erro ao fechar vigência da tabela Salário Mínimo anterior (id: {id_versao_anterior}): {e}")
            raise HTTPException(status_code=500, detail=f"Erro técnico ao tentar fechar vigência da tabela Salário Mínimo anterior: {str(e)}")

    nova_id_versao = str(uuid.uuid4())
    tabela_sm_update_data.id_versao = nova_id_versao
    tabela_sm_update_data.data_criacao_registro = now
    tabela_sm_update_data.data_ultima_modificacao = now
    tabela_sm_update_data.data_inativacao = None

    await _verificar_conflito_vigencia(
        client,
        TABLE_ID_SALARIO_MINIMO,
        tabela_sm_update_data.data_inicio_vigencia,
        tabela_sm_update_data.data_fim_vigencia,
        id_versao_ignorada=None 
    )
    
    row_to_insert = tabela_sm_update_data.model_dump(by_alias=True)
    if row_to_insert.get('valores_regionais') is not None:
        row_to_insert['valores_regionais'] = json.dumps(row_to_insert['valores_regionais'])
    else:
        row_to_insert['valores_regionais'] = None

    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_SALARIO_MINIMO)
    errors = client.insert_rows_json(table_ref, [row_to_insert])

    if not errors:
        return tabela_sm_update_data
    else:
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        print(f"Erro ao inserir nova versão da tabela Salário Mínimo no BigQuery: {detailed_error_message}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar (criar nova versão) dados da tabela Salário Mínimo no BigQuery. Detalhes: {detailed_error_message}")

async def atualizar_tabela_fgts(id_versao_anterior: str, tabela_fgts_update_data: TabelaFGTS) -> TabelaFGTS:
    client = bigquery.Client(project=PROJECT_ID)
    now = datetime.now()

    try:
        versao_anterior = await obter_tabela_fgts_por_id(id_versao_anterior)
        if versao_anterior.data_inativacao:
            raise HTTPException(status_code=400, detail=f"A versão anterior (id: {id_versao_anterior}) da tabela FGTS já está inativada e não pode ser a base para uma atualização.")
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Versão anterior da tabela FGTS (id: {id_versao_anterior}) não encontrada para ser atualizada.")
        raise e
    except Exception as e:
        print(f"Erro inesperado ao buscar versão anterior da tabela FGTS para atualização: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao verificar versão anterior da tabela FGTS: {str(e)}")

    fechar_versao_anterior = False
    nova_data_fim_vigencia_anterior = None

    if tabela_fgts_update_data.data_inicio_vigencia > versao_anterior.data_inicio_vigencia:
        if versao_anterior.data_fim_vigencia is None or versao_anterior.data_fim_vigencia >= tabela_fgts_update_data.data_inicio_vigencia:
            fechar_versao_anterior = True
            nova_data_fim_vigencia_anterior = tabela_fgts_update_data.data_inicio_vigencia - timedelta(days=1)
            
            if nova_data_fim_vigencia_anterior < versao_anterior.data_inicio_vigencia:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"Conflito ao tentar fechar a vigência da tabela FGTS anterior (id: {id_versao_anterior}). "
                        f"A nova data de início ({tabela_fgts_update_data.data_inicio_vigencia}) resultaria em uma data de fim ({nova_data_fim_vigencia_anterior}) "
                        f"anterior à data de início existente ({versao_anterior.data_inicio_vigencia}) para a tabela anterior."
                    )
                )
    
    if fechar_versao_anterior and nova_data_fim_vigencia_anterior is not None:
        query_update_anterior = f"""
            UPDATE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_FGTS}`
            SET data_fim_vigencia = @nova_data_fim, data_ultima_modificacao = @mod_time
            WHERE id_versao = @id_anterior AND data_inativacao IS NULL
        """
        job_config_update = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("nova_data_fim", "DATE", nova_data_fim_vigencia_anterior),
                bigquery.ScalarQueryParameter("mod_time", "TIMESTAMP", now),
                bigquery.ScalarQueryParameter("id_anterior", "STRING", id_versao_anterior),
            ]
        )
        try:
            update_job = client.query(query_update_anterior, job_config=job_config_update)
            update_job.result() 
            if update_job.num_dml_affected_rows is None or update_job.num_dml_affected_rows == 0:
                error_msg = (
                    f"Falha ao tentar fechar a vigência da tabela FGTS anterior (id: {id_versao_anterior}). "
                    "Nenhuma linha foi afetada pela atualização. A tabela anterior pode já estar inativada ou não foi encontrada."
                )
                print(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            print(f"Erro ao fechar vigência da tabela FGTS anterior (id: {id_versao_anterior}): {e}")
            raise HTTPException(status_code=500, detail=f"Erro técnico ao tentar fechar vigência da tabela FGTS anterior: {str(e)}")

    nova_id_versao = str(uuid.uuid4())
    tabela_fgts_update_data.id_versao = nova_id_versao
    tabela_fgts_update_data.data_criacao_registro = now
    tabela_fgts_update_data.data_ultima_modificacao = now
    tabela_fgts_update_data.data_inativacao = None

    await _verificar_conflito_vigencia(
        client,
        TABLE_ID_FGTS,
        tabela_fgts_update_data.data_inicio_vigencia,
        tabela_fgts_update_data.data_fim_vigencia,
        id_versao_ignorada=None
    )
    
    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_FGTS)
    row_to_insert = tabela_fgts_update_data.model_dump(by_alias=True)
    errors = client.insert_rows_json(table_ref, [row_to_insert])

    if not errors:
        return tabela_fgts_update_data
    else:
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        print(f"Erro ao inserir nova versão da tabela FGTS no BigQuery: {detailed_error_message}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar (criar nova versão) dados da tabela FGTS no BigQuery. Detalhes: {detailed_error_message}")

# Funções de exclusão (inativação)
async def deletar_tabela_inss(id_versao: str) -> dict:
    client = bigquery.Client(project=PROJECT_ID)
    
    try:
        tabela_existente = await obter_tabela_inss_por_id(id_versao)
        if tabela_existente.data_inativacao is not None:
            return {"message": f"Versão da tabela INSS com id_versao '{id_versao}' já está inativada."}
    except HTTPException as e:
        if e.status_code == 404: 
            raise HTTPException(status_code=404, detail=f"Versão da tabela INSS com id_versao '{id_versao}' não encontrada para deleção.")
        raise e
    except Exception as e:
        print(f"Erro inesperado ao buscar tabela INSS para deleção: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao verificar tabela INSS para deleção: {str(e)}")

    now_timestamp = datetime.now()
    query = f"""
        UPDATE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_INSS}`
        SET 
            data_inativacao = @data_inativacao_ts,
            data_ultima_modificacao = @data_ultima_modificacao_ts
        WHERE id_versao = @id_versao_param AND data_inativacao IS NULL
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("data_inativacao_ts", "TIMESTAMP", now_timestamp),
            bigquery.ScalarQueryParameter("data_ultima_modificacao_ts", "TIMESTAMP", now_timestamp),
            bigquery.ScalarQueryParameter("id_versao_param", "STRING", id_versao),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        query_job.result()  

        if query_job.num_dml_affected_rows is not None and query_job.num_dml_affected_rows > 0:
            return {"message": f"Versão da tabela INSS com id_versao '{id_versao}' inativada com sucesso."}
        else:
            tabela_atualizada = await obter_tabela_inss_por_id(id_versao)
            if tabela_atualizada.data_inativacao is not None:
                 return {"message": f"Versão da tabela INSS com id_versao '{id_versao}' foi inativada concorrentemente ou já se encontrava assim."}
            raise HTTPException(status_code=500, detail=f"Falha ao inativar tabela INSS com id_versao '{id_versao}'. Nenhuma linha foi afetada e o registro não parece ter sido inativado concorrentemente.")

    except Exception as e:
        print(f"Erro ao inativar tabela INSS id_versao {id_versao} no BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao inativar dados da tabela INSS no BigQuery: {str(e)}")

async def deletar_tabela_irrf(id_versao: str):
    client = bigquery.Client(project=PROJECT_ID)
    
    try:
        tabela_existente = await obter_tabela_irrf_por_id(id_versao)
        if tabela_existente.data_inativacao is not None:
            return {"message": f"Versão da tabela IRRF com id_versao '{id_versao}' já está inativada."}
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Versão da tabela IRRF com id_versao '{id_versao}' não encontrada para deleção.")
        raise e
    except Exception as e:
        print(f"Erro inesperado ao buscar tabela IRRF para deleção: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao verificar tabela IRRF para deleção: {str(e)}")

    now_timestamp = datetime.now()
    query = f"""
        UPDATE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_IRRF}`
        SET 
            data_inativacao = @data_inativacao_ts,
            data_ultima_modificacao = @data_ultima_modificacao_ts
        WHERE id_versao = @id_versao_param AND data_inativacao IS NULL
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("data_inativacao_ts", "TIMESTAMP", now_timestamp),
            bigquery.ScalarQueryParameter("data_ultima_modificacao_ts", "TIMESTAMP", now_timestamp),
            bigquery.ScalarQueryParameter("id_versao_param", "STRING", id_versao),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        query_job.result() 

        if query_job.num_dml_affected_rows is not None and query_job.num_dml_affected_rows > 0:
            return {"message": f"Versão da tabela IRRF com id_versao '{id_versao}' inativada com sucesso."}
        else:
            tabela_atualizada = await obter_tabela_irrf_por_id(id_versao)
            if tabela_atualizada.data_inativacao is not None:
                 return {"message": f"Versão da tabela IRRF com id_versao '{id_versao}' foi inativada concorrentemente ou já se encontrava assim."}
            raise HTTPException(status_code=500, detail=f"Falha ao inativar tabela IRRF com id_versao '{id_versao}'. Nenhuma linha foi afetada e o registro não parece ter sido inativado concorrentemente.")

    except Exception as e:
        print(f"Erro ao inativar tabela IRRF id_versao {id_versao} no BigQuery: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao inativar dados da tabela IRRF no BigQuery: {str(e)}")

async def deletar_tabela_salario_familia(id_versao: str):
    client = bigquery.Client(project=PROJECT_ID)
    
    try:
        tabela_existente = await obter_tabela_salario_familia_por_id(id_versao)
        if tabela_existente.data_inativacao is not None:
            return {"message": f"Versão da tabela Salário Família com id_versao '{id_versao}' já está inativada."}
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Versão da tabela Salário Família com id_versao '{id_versao}' não encontrada para deleção.")
        raise e
    except Exception as e:
        print(f"Erro inesperado ao buscar tabela Salário Família para deleção: {e}")
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail=f"Erro ao verificar tabela Salário Família para deleção: {str(e)}")
        else:
            raise e

    now_timestamp = datetime.now()
    query = f"""
        UPDATE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_SALARIO_FAMILIA}`
        SET 
            data_inativacao = @data_inativacao_ts,
            data_ultima_modificacao = @data_ultima_modificacao_ts
        WHERE id_versao = @id_versao_param AND data_inativacao IS NULL
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("data_inativacao_ts", "TIMESTAMP", now_timestamp),
            bigquery.ScalarQueryParameter("data_ultima_modificacao_ts", "TIMESTAMP", now_timestamp),
            bigquery.ScalarQueryParameter("id_versao_param", "STRING", id_versao),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        query_job.result()

        if query_job.num_dml_affected_rows is not None and query_job.num_dml_affected_rows > 0:
            return {"message": f"Versão da tabela Salário Família com id_versao '{id_versao}' inativada com sucesso."}
        else:
            try:
                tabela_atualizada = await obter_tabela_salario_familia_por_id(id_versao)
                if tabela_atualizada.data_inativacao is not None:
                    return {"message": f"Versão da tabela Salário Família com id_versao '{id_versao}' foi inativada concorrentemente ou já se encontrava assim."}
                else:
                    raise HTTPException(status_code=500, detail=f"Falha ao inativar tabela Salário Família com id_versao '{id_versao}'. Nenhuma linha foi afetada e o registro não parece ter sido inativado concorrentemente.")
            except HTTPException as he_check:
                if he_check.status_code == 404:
                     raise HTTPException(status_code=500, detail=f"Falha crítica ao inativar tabela Salário Família com id_versao '{id_versao}'. A tabela não foi encontrada após a tentativa de atualização.")
                raise he_check
            except Exception as e_check:
                print(f"Erro ao re-verificar tabela Salário Família id_versao {id_versao}: {e_check}")
                raise HTTPException(status_code=500, detail=f"Erro ao verificar o estado da tabela Salário Família após tentativa de inativação: {str(e_check)}")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao inativar tabela Salário Família id_versao {id_versao} no BigQuery: {e}")
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail=f"Erro ao inativar dados da tabela Salário Família no BigQuery: {str(e)}")
        else:
            raise e

async def deletar_tabela_salario_minimo(id_versao: str):
    client = bigquery.Client(project=PROJECT_ID)
    
    try:
        tabela_existente = await obter_tabela_salario_minimo_por_id(id_versao)
        if tabela_existente.data_inativacao is not None:
            return {"message": f"Versão da tabela Salário Mínimo com id_versao '{id_versao}' já está inativada."}
    except HTTPException as e:
        if e.status_code == 404: 
            raise HTTPException(status_code=404, detail=f"Versão da tabela Salário Mínimo com id_versao '{id_versao}' não encontrada para deleção.")
        raise e
    except Exception as e: 
        print(f"Erro inesperado ao buscar tabela Salário Mínimo para deleção: {e}")
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail=f"Erro ao verificar tabela Salário Mínimo para deleção: {str(e)}")
        else:
            raise e

    now_timestamp = datetime.now()
    query = f"""
        UPDATE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_SALARIO_MINIMO}`
        SET 
            data_inativacao = @data_inativacao_ts,
            data_ultima_modificacao = @data_ultima_modificacao_ts
        WHERE id_versao = @id_versao_param AND data_inativacao IS NULL
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("data_inativacao_ts", "TIMESTAMP", now_timestamp),
            bigquery.ScalarQueryParameter("data_ultima_modificacao_ts", "TIMESTAMP", now_timestamp),
            bigquery.ScalarQueryParameter("id_versao_param", "STRING", id_versao),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        query_job.result()  

        if query_job.num_dml_affected_rows is not None and query_job.num_dml_affected_rows > 0:
            return {"message": f"Versão da tabela Salário Mínimo com id_versao '{id_versao}' inativada com sucesso."}
        else:
            try:
                tabela_atualizada = await obter_tabela_salario_minimo_por_id(id_versao)
                if tabela_atualizada.data_inativacao is not None:
                    return {"message": f"Versão da tabela Salário Mínimo com id_versao '{id_versao}' foi inativada concorrentemente ou já se encontrava assim."}
                else:
                    raise HTTPException(status_code=500, detail=f"Falha ao inativar tabela Salário Mínimo com id_versao '{id_versao}'. Nenhuma linha foi afetada e o registro não parece ter sido inativado concorrentemente.")
            except HTTPException as he_check:
                if he_check.status_code == 404:
                     raise HTTPException(status_code=500, detail=f"Falha crítica ao inativar tabela Salário Mínimo com id_versao '{id_versao}'. A tabela não foi encontrada após a tentativa de atualização.")
                raise he_check
            except Exception as e_check:
                print(f"Erro ao re-verificar tabela Salário Mínimo id_versao {id_versao}: {e_check}")
                raise HTTPException(status_code=500, detail=f"Erro ao verificar o estado da tabela Salário Mínimo após tentativa de inativação: {str(e_check)}")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao inativar tabela Salário Mínimo id_versao {id_versao} no BigQuery: {e}")
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail=f"Erro ao inativar dados da tabela Salário Mínimo no BigQuery: {str(e)}")
        else:
            raise e

async def deletar_tabela_fgts(id_versao: str):
    client = bigquery.Client(project=PROJECT_ID)
    
    try:
        tabela_existente = await obter_tabela_fgts_por_id(id_versao)
        if tabela_existente.data_inativacao is not None:
            return {"message": f"Versão da tabela FGTS com id_versao '{id_versao}' já está inativada."}
    except HTTPException as e:
        if e.status_code == 404: 
            raise HTTPException(status_code=404, detail=f"Versão da tabela FGTS com id_versao '{id_versao}' não encontrada para deleção.")
        raise e
    except Exception as e:
        print(f"Erro inesperado ao buscar tabela FGTS para deleção: {e}")
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail=f"Erro ao verificar tabela FGTS para deleção: {str(e)}")
        else:
            raise e

    now_timestamp = datetime.now()
    query = f"""
        UPDATE `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_FGTS}`
        SET 
            data_inativacao = @data_inativacao_ts,
            data_ultima_modificacao = @data_ultima_modificacao_ts
        WHERE id_versao = @id_versao_param AND data_inativacao IS NULL
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("data_inativacao_ts", "TIMESTAMP", now_timestamp),
            bigquery.ScalarQueryParameter("data_ultima_modificacao_ts", "TIMESTAMP", now_timestamp),
            bigquery.ScalarQueryParameter("id_versao_param", "STRING", id_versao),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        query_job.result()  

        if query_job.num_dml_affected_rows is not None and query_job.num_dml_affected_rows > 0:
            return {"message": f"Versão da tabela FGTS com id_versao '{id_versao}' inativada com sucesso."}
        else:
            try:
                tabela_atualizada = await obter_tabela_fgts_por_id(id_versao) 
                if tabela_atualizada.data_inativacao is not None:
                    return {"message": f"Versão da tabela FGTS com id_versao '{id_versao}' foi inativada concorrentemente ou já se encontrava assim."}
                else:
                    raise HTTPException(status_code=500, detail=f"Falha ao inativar tabela FGTS com id_versao '{id_versao}'. Nenhuma linha foi afetada e o registro não parece ter sido inativado concorrentemente.")
            except HTTPException as he_check:
                if he_check.status_code == 404:
                     raise HTTPException(status_code=500, detail=f"Falha crítica ao inativar tabela FGTS com id_versao '{id_versao}'. A tabela não foi encontrada após a tentativa de atualização.")
                raise he_check
            except Exception as e_check:
                print(f"Erro ao re-verificar tabela FGTS id_versao {id_versao}: {e_check}")
                raise HTTPException(status_code=500, detail=f"Erro ao verificar o estado da tabela FGTS após tentativa de inativação: {str(e_check)}")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao inativar tabela FGTS id_versao {id_versao} no BigQuery: {e}")
        if not isinstance(e, HTTPException):
            raise HTTPException(status_code=500, detail=f"Erro ao inativar dados da tabela FGTS no BigQuery: {str(e)}")
        else:
            raise e

# Funções para Verificação Manual de Parâmetros Legais

async def registrar_log_verificacao_manual(
    tipo_parametro: str,
    link_verificado: str,
    houve_alteracao: bool,
    observacao_verificacao: Optional[str],
    usuario_verificacao: str # Este virá do sistema de autenticação no futuro
) -> dict: # Retornará um dicionário representando o LogVerificacaoResponse
    client = bigquery.Client(project=PROJECT_ID)
    log_id = str(uuid.uuid4())
    data_verificacao_atual = datetime.now() # Data e hora da verificação
    data_criacao_log = datetime.now() # Data e hora da criação do log (pode ser o mesmo)

    row_to_insert = {
        "id_log_verificacao": log_id,
        "tipo_parametro": tipo_parametro,
        "data_verificacao": data_verificacao_atual.isoformat(), # Formato ISO para BQ
        "usuario_verificacao": usuario_verificacao,
        "link_verificado": link_verificado,
        "houve_alteracao": houve_alteracao,
        "observacao_verificacao": observacao_verificacao,
        "data_criacao": data_criacao_log.isoformat() # Formato ISO para BQ
    }

    table_ref = client.dataset(DATASET_ID).table(TABLE_ID_LOG_VERIFICACAO)
    errors = client.insert_rows_json(table_ref, [row_to_insert])

    if not errors:
        # Retornar o objeto como ele será serializado pela rota, incluindo datetimes
        return {
            "id_log_verificacao": log_id,
            "tipo_parametro": tipo_parametro,
            "data_verificacao": data_verificacao_atual, # Objeto datetime
            "usuario_verificacao": usuario_verificacao,
            "link_verificado": link_verificado,
            "houve_alteracao": houve_alteracao,
            "observacao_verificacao": observacao_verificacao,
            "data_criacao": data_criacao_log # Objeto datetime
        }
    else:
        print(f"Erro ao inserir log de verificação manual no BigQuery: {errors}")
        error_details = []
        for error_entry in errors:
            error_details.append(f"Index: {error_entry['index']}, Errors: {error_entry['errors']}")
        detailed_error_message = "; ".join(error_details)
        raise HTTPException(status_code=500, detail=f"Erro ao registrar log de verificação no BigQuery: {detailed_error_message}")

async def obter_ultimo_log_verificacao(tipo_parametro: str) -> Optional[dict]: # Retornará um dict ou None
    client = bigquery.Client(project=PROJECT_ID)
    query = f"""
        SELECT 
            
            id_log_verificacao,
            tipo_parametro,
            data_verificacao,
            usuario_verificacao,
            link_verificado,
            houve_alteracao,
            observacao_verificacao,
            data_criacao
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_LOG_VERIFICACAO}`
        WHERE tipo_parametro = @tipo_parametro
        ORDER BY data_verificacao DESC
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("tipo_parametro", "STRING", tipo_parametro),
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        row = None
        for r in results:
            row = r
            break
        
        if row:
            # Converter a linha do BigQuery (Row) para um dicionário
            log_data = dict(row.items())
            # Assegurar que campos de data/hora sejam objetos datetime para Pydantic
            # O cliente BigQuery já deve retornar objetos datetime para campos TIMESTAMP/DATETIME
            # mas uma verificação/conversão explícita pode ser útil se vierem como string.
            if 'data_verificacao' in log_data and not isinstance(log_data['data_verificacao'], datetime):
                # Tentar parsear se for string, ou lidar com outros tipos se necessário
                if isinstance(log_data['data_verificacao'], str):
                    log_data['data_verificacao'] = datetime.fromisoformat(log_data['data_verificacao'])
                # Adicionar mais lógica de conversão se BQ retornar outros tipos (ex: Arrow timestamp)
            
            if 'data_criacao' in log_data and not isinstance(log_data['data_criacao'], datetime):
                if isinstance(log_data['data_criacao'], str):
                    log_data['data_criacao'] = datetime.fromisoformat(log_data['data_criacao'])
            return log_data
        else:
            return None
    except Exception as e:
        print(f"Erro ao obter último log de verificação do BigQuery para {tipo_parametro}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar último log de verificação: {str(e)}")

async def obter_config_fontes_oficiais() -> dict:
    try:
        # Ajuste o caminho para o seu arquivo config.json
        with open("src/config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        fontes = config.get("fontes_oficiais_parametros", {})
        return fontes
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Arquivo de configuração (config.json) não encontrado.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Erro ao decodificar o arquivo de configuração (config.json).")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler configuração de fontes oficiais: {str(e)}")