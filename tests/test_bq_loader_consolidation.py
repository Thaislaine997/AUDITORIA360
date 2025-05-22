import pytest
import pandas as pd
from google.cloud import bigquery  # Mantido para SchemaField, Table, mas o Client será mockado
from datetime import datetime, date, timezone
from unittest.mock import MagicMock, patch

from src.bq_loader import ControleFolhaLoader

TEST_PROJECT_ID = "mock-auditoria-folha"
TEST_DATASET_ID = "mock_controle_folha_test_dataset"
RAW_DATA_TABLE_ID = "control_folha_planilha_raw_data"
FOLHAS_TABLE_ID = "folhas"
EMPRESAS_TABLE_ID = "empresas"

# Estrutura em memória para simular o banco de dados
MOCK_DB = {}


def reset_mock_db():
    global MOCK_DB
    MOCK_DB = {
        EMPRESAS_TABLE_ID: pd.DataFrame(columns=["codigo_empresa", "cnpj", "nome_empresa", "client_id"]),
        RAW_DATA_TABLE_ID: pd.DataFrame(
            columns=["cnpj_empresa", "status_valor_cliente", "status_aba_origem", "mes_ano_referencia",
                     "data_processamento_gcs", "nome_arquivo_origem", "client_id"]),
        FOLHAS_TABLE_ID: pd.DataFrame(
            columns=["id_folha", "codigo_empresa", "cnpj_empresa", "mes_ano", "status", "data_envio_cliente",
                     "data_guia_fgts", "data_darf_inss", "observacoes", "data_ultima_atualizacao_bq", "client_id"])
    }


@pytest.fixture
def mock_bq_client():
    """Retorna um MagicMock configurado para simular o BigQuery client."""
    client = MagicMock(spec=bigquery.Client)
    client.project = TEST_PROJECT_ID

    def mock_query(query_string, job_config=None):
        mock_query_job = MagicMock(spec=bigquery.QueryJob)

        table_name_extracted = None
        if f"`{TEST_PROJECT_ID}.{TEST_DATASET_ID}.{EMPRESAS_TABLE_ID}`" in query_string:
            table_name_extracted = EMPRESAS_TABLE_ID
        elif f"`{TEST_PROJECT_ID}.{TEST_DATASET_ID}.{RAW_DATA_TABLE_ID}`" in query_string:
            table_name_extracted = RAW_DATA_TABLE_ID
        elif f"`{TEST_PROJECT_ID}.{TEST_DATASET_ID}.{FOLHAS_TABLE_ID}`" in query_string:
            table_name_extracted = FOLHAS_TABLE_ID

        if "SELECT" in query_string.upper() and table_name_extracted:
            client_id_filter = None
            if job_config and job_config.query_parameters:
                for param in job_config.query_parameters:
                    if param.name == "client_id":
                        client_id_filter = param.value
                        break

            df_to_return = MOCK_DB.get(table_name_extracted, pd.DataFrame()).copy()
            if client_id_filter and not df_to_return.empty and "client_id" in df_to_return.columns:
                df_to_return = df_to_return[df_to_return["client_id"] == client_id_filter]

            nome_arquivo_filter = None
            if job_config and job_config.query_parameters:
                for param in job_config.query_parameters:
                    if param.name == "nome_arquivo_origem":
                        nome_arquivo_filter = param.value
                        break
            if nome_arquivo_filter and not df_to_return.empty and "nome_arquivo_origem" in df_to_return.columns:
                df_to_return = df_to_return[df_to_return["nome_arquivo_origem"] == nome_arquivo_filter]

            mock_query_job.to_dataframe.return_value = df_to_return
            mock_query_job.result.return_value = None

        return mock_query_job

    client.query = MagicMock(side_effect=mock_query)

    def mock_insert_rows_json(table_ref, rows, *args, **kwargs):
        table_id = table_ref.table_id if hasattr(table_ref, 'table_id') else str(table_ref).split('.')[-1]

        if table_id not in MOCK_DB:
            MOCK_DB[table_id] = pd.DataFrame()

        current_df = MOCK_DB[table_id]
        new_rows_df = pd.DataFrame(rows)

        for col in current_df.columns:
            if col not in new_rows_df.columns:
                new_rows_df[col] = pd.NA
        for col in new_rows_df.columns:
            if col not in current_df.columns:
                current_df[col] = pd.NA

        new_rows_df = new_rows_df[current_df.columns.tolist()]

        for col in new_rows_df.columns:
            if col in current_df.columns and not current_df[col].empty:
                new_rows_df[col] = new_rows_df[col].astype(current_df[col].dtype, errors='ignore')

        MOCK_DB[table_id] = pd.concat([current_df, new_rows_df], ignore_index=True)
        return []

    client.insert_rows_json = MagicMock(side_effect=mock_insert_rows_json)

    def mock_insert_rows(table, rows_to_insert, selected_fields=None, **kwargs):
        table_id = table.table_id
        if table_id not in MOCK_DB:
            cols = [field.name for field in selected_fields] if selected_fields else [f"col{i}" for i in
                                                                                      range(len(rows_to_insert[0]))]
            MOCK_DB[table_id] = pd.DataFrame(columns=cols)

        df_rows = pd.DataFrame(rows_to_insert, columns=MOCK_DB[table_id].columns[:len(rows_to_insert[0])])

        current_df = MOCK_DB[table_id]
        for col in current_df.columns:
            if col not in df_rows.columns:
                df_rows[col] = pd.NA
        for col in df_rows.columns:
            if col not in current_df.columns:
                current_df[col] = pd.NA
        df_rows = df_rows[current_df.columns.tolist()]
        for col in df_rows.columns:
            if col in current_df.columns and not current_df[col].empty:
                df_rows[col] = df_rows[col].astype(current_df[col].dtype, errors='ignore')

        MOCK_DB[table_id] = pd.concat([MOCK_DB[table_id], df_rows], ignore_index=True)
        return []

    client.insert_rows = MagicMock(side_effect=mock_insert_rows)

    def mock_get_table(table_ref_str_or_obj):
        table_id = table_ref_str_or_obj.table_id if hasattr(table_ref_str_or_obj, 'table_id') else str(
            table_ref_str_or_obj).split('.')[-1]

        if table_id in MOCK_DB:
            mock_table = MagicMock(spec=bigquery.Table)
            mock_table.table_id = table_id
            mock_table.project = TEST_PROJECT_ID
            mock_table.dataset_id = TEST_DATASET_ID

            schema = []
            if not MOCK_DB[table_id].empty:
                for col_name in MOCK_DB[table_id].columns:
                    dtype = MOCK_DB[table_id][col_name].dtype
                    if pd.api.types.is_integer_dtype(dtype):
                        bq_type = "INTEGER"
                    elif pd.api.types.is_float_dtype(dtype):
                        bq_type = "FLOAT"
                    elif pd.api.types.is_datetime64_any_dtype(dtype):
                        bq_type = "TIMESTAMP"
                    elif pd.api.types.is_object_dtype(dtype):
                        bq_type = "STRING"
                    else:
                        bq_type = "STRING"
                    schema.append(bigquery.SchemaField(col_name, bq_type))
            mock_table.schema = schema
            return mock_table
        else:
            from google.cloud.exceptions import NotFound
            raise NotFound(f"Mock table {table_id} not found")

    client.get_table = MagicMock(side_effect=mock_get_table)

    client.delete_table = MagicMock()
    client.create_table = MagicMock()

    mock_dataset_ref = MagicMock()
    mock_table_ref = MagicMock()

    def dataset_side_effect(dataset_id_str):
        mock_dataset_ref.table = MagicMock(return_value=mock_table_ref)
        return mock_dataset_ref

    client.dataset = MagicMock(side_effect=dataset_side_effect)

    return client


@pytest.fixture
def controle_loader_test(mock_bq_client):
    """Retorna uma instância do ControleFolhaLoader com cliente BQ mockado."""
    config = {
        "gcp_project_id": TEST_PROJECT_ID,
        "control_bq_dataset_id": TEST_DATASET_ID,
        "client_id": "test_client_123",
    }
    with patch('src.bq_loader.get_bigquery_client', return_value=mock_bq_client):
        loader = ControleFolhaLoader(config)
        return loader


@pytest.fixture(autouse=True)
def setup_teardown_mock_db(mock_bq_client):
    """Limpa o MOCK_DB antes de cada teste e simula criação/deleção."""
    reset_mock_db()
    yield


def popular_tabela_empresas(client_or_loader, data_list):
    actual_client = client_or_loader.client if hasattr(client_or_loader, 'client') else client_or_loader
    client_id_to_use = "test_client_123"
    if hasattr(client_or_loader, 'client_id'):
        client_id_to_use = client_or_loader.client_id

    for row in data_list:
        if "client_id" not in row:
            row["client_id"] = client_id_to_use

    table_ref_mock = MagicMock()
    table_ref_mock.table_id = EMPRESAS_TABLE_ID
    table_ref_mock.dataset_id = TEST_DATASET_ID
    table_ref_mock.project = TEST_PROJECT_ID

    errors = actual_client.insert_rows_json(table_ref_mock, data_list)
    assert not errors, f"Erro ao popular tabela empresas (mock): {errors}"


def popular_tabela_raw_data(client_or_loader, data_list):
    actual_client = client_or_loader.client if hasattr(client_or_loader, 'client') else client_or_loader
    client_id_to_use = "test_client_123"
    if hasattr(client_or_loader, 'client_id'):
        client_id_to_use = client_or_loader.client_id
    for row in data_list:
        if "client_id" not in row:
            row["client_id"] = client_id_to_use

    table_ref_mock = MagicMock()
    table_ref_mock.table_id = RAW_DATA_TABLE_ID
    table_ref_mock.project = TEST_PROJECT_ID
    table_ref_mock.dataset_id = TEST_DATASET_ID

    errors = actual_client.insert_rows_json(table_ref_mock, data_list)
    assert not errors, f"Erro ao popular tabela raw_data (mock): {errors}"


def test_consolidacao_nova_folha(mock_bq_client, controle_loader_test):
    empresas_data = [
        {"codigo_empresa": 101, "cnpj": "11111111000111", "nome_empresa": "Empresa A"},
    ]
    popular_tabela_empresas(controle_loader_test, empresas_data)

    raw_data = [
        {
            "cnpj_empresa": "11111111000111", "status_valor_cliente": "OK",
            "status_aba_origem": "ChecklistInicial", "mes_ano_referencia": date(2025, 6, 1),
            "data_processamento_gcs": datetime.now(timezone.utc),
            "nome_arquivo_origem": "planilha_junho.xlsx"
        }
    ]
    popular_tabela_raw_data(controle_loader_test, raw_data)

    sucesso = controle_loader_test.consolidar_dados_planilha_para_folhas(
        nome_arquivo_origem_especifico="planilha_junho.xlsx"
    )
    assert sucesso, "A função de consolidação falhou"

    df_folhas = MOCK_DB[FOLHAS_TABLE_ID]
    df_folhas_filtrado = df_folhas[df_folhas["cnpj_empresa"] == "11111111000111"]

    assert len(df_folhas_filtrado) == 1
    folha = df_folhas_filtrado.iloc[0]
    assert folha["id_folha"] == "11111111000111_202506"
    assert folha["codigo_empresa"] == 101
    assert folha["status"] == "Pendente Documentação"
    assert pd.isna(folha["data_envio_cliente"])
    assert "Criado via planilha: planilha_junho.xlsx, aba: ChecklistInicial" in folha["observacoes"]
    assert folha["client_id"] == "test_client_123"


def test_consolidacao_atualiza_folha_existente(mock_bq_client, controle_loader_test):
    empresas_data = [
        {"codigo_empresa": 102, "cnpj": "22222222000122", "nome_empresa": "Empresa B"},
    ]
    popular_tabela_empresas(controle_loader_test, empresas_data)

    raw_data_inicial = [
        {
            "cnpj_empresa": "22222222000122", "status_valor_cliente": "OK",
            "status_aba_origem": "ChecklistInicial", "mes_ano_referencia": date(2025, 7, 1),
            "data_processamento_gcs": datetime.now(timezone.utc), "nome_arquivo_origem": "planilha_julho_v1.xlsx"
        }
    ]
    popular_tabela_raw_data(controle_loader_test, raw_data_inicial)
    controle_loader_test.consolidar_dados_planilha_para_folhas(nome_arquivo_origem_especifico="planilha_julho_v1.xlsx")

    folha_inicial = MOCK_DB[FOLHAS_TABLE_ID][MOCK_DB[FOLHAS_TABLE_ID]["id_folha"] == "22222222000122_202507"].iloc[0]
    assert folha_inicial["status"] == "Pendente Documentação"

    raw_data_atualizacao = [
        {
            "cnpj_empresa": "22222222000122", "status_valor_cliente": "Enviado",
            "status_aba_origem": "EnvioCliente", "mes_ano_referencia": date(2025, 7, 1),
            "data_processamento_gcs": datetime.now(timezone.utc), "nome_arquivo_origem": "planilha_julho_v2.xlsx"
        }
    ]
    MOCK_DB[RAW_DATA_TABLE_ID] = pd.DataFrame(columns=MOCK_DB[RAW_DATA_TABLE_ID].columns)
    popular_tabela_raw_data(controle_loader_test, raw_data_atualizacao)

    sucesso = controle_loader_test.consolidar_dados_planilha_para_folhas(
        nome_arquivo_origem_especifico="planilha_julho_v2.xlsx"
    )
    assert sucesso

    df_folhas_final = MOCK_DB[FOLHAS_TABLE_ID]
    folha_atualizada_series = df_folhas_final[df_folhas_final["id_folha"] == "22222222000122_202507"]

    assert len(folha_atualizada_series) == 1
    folha_atualizada = folha_atualizada_series.iloc[0]

    assert folha_atualizada["status"] == "Aguardando Cliente"
    assert not pd.isna(folha_atualizada["data_envio_cliente"])
    assert "Criado via planilha: planilha_julho_v1.xlsx, aba: ChecklistInicial" in folha_atualizada["observacoes"]
    assert "Atualizado via planilha: planilha_julho_v2.xlsx, aba: EnvioCliente" in folha_atualizada["observacoes"]
    assert folha_atualizada["client_id"] == "test_client_123"
