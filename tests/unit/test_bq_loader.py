from unittest.mock import MagicMock

import pandas as pd
import pytest
from google.cloud import bigquery

from services.ingestion.bq_loader import (
    ControleFolhaLoader,
    load_data_to_bq,
)


# --- Fixtures e Configs ---
@pytest.fixture
def config_cliente_a():
    return dict(
        gcp_project_id="fake-project",
        control_bq_dataset_id="fake_dataset",
        bq_dataset_id="fake_dataset",
        bq_table_id="fake_table",
        gcp_location="us-central1",
        client_id="cliente_a",
    )


@pytest.fixture
def config_cliente_b():
    return dict(
        gcp_project_id="fake-project",
        control_bq_dataset_id="fake_dataset",
        bq_dataset_id="fake_dataset",
        bq_table_id="fake_table",
        gcp_location="us-central1",
        client_id="cliente_b",
    )


# --- Testes de isolamento e validação de client_id ---
def test_loader_exige_client_id(config_cliente_a):
    loader = ControleFolhaLoader(config_cliente_a)
    assert loader.client_id == "cliente_a"
    config_sem_id = dict(config_cliente_a)
    config_sem_id.pop("client_id")
    with pytest.raises(ValueError):
        ControleFolhaLoader(config_sem_id)


def test_load_data_to_bigquery_exige_client_id(config_cliente_a):
    sample_data = [{"id_extracao": "1", "id_item": "1"}]
    config_sem_id = dict(config_cliente_a)
    config_sem_id.pop("client_id")
    full_table_id = f"{config_sem_id['gcp_project_id']}.{config_sem_id['bq_dataset_id']}.{config_sem_id['bq_table_id']}"
    from unittest.mock import MagicMock

    client = MagicMock()
    with pytest.raises(ValueError):
        load_data_to_bq(sample_data, full_table_id, client)


def test_listar_empresas_isolamento(monkeypatch, config_cliente_a, config_cliente_b):
    class FakeClient:
        def query(self, query, job_config=None):
            assert "client_id = @client_id" in query
            assert job_config is not None
            param = job_config.query_parameters[0]

            class FakeResult:
                def to_dataframe(self):
                    return [param.value]

            return FakeResult()

    monkeypatch.setattr(
        "services.ingestion.bq_loader.get_bigquery_client", lambda config: FakeClient()
    )
    loader_a = ControleFolhaLoader(config_cliente_a)
    loader_b = ControleFolhaLoader(config_cliente_b)
    result_a = loader_a.listar_todas_as_empresas()
    result_b = loader_b.listar_todas_as_empresas()
    if isinstance(result_a, pd.DataFrame):
        result_a = result_a.values.flatten().tolist()
    if isinstance(result_b, pd.DataFrame):
        result_b = result_b.values.flatten().tolist()
    assert result_a == ["cliente_a"]
    assert result_b == ["cliente_b"]


# --- Testes de integração e CRUD com mocks de DataFrame/BigQuery ---
# Estrutura em memória para simular o banco de dados
TEST_PROJECT_ID = "mock-auditoria-folha"
TEST_DATASET_ID = "mock_controle_folha_test_dataset"
RAW_DATA_TABLE_ID = "control_folha_planilha_raw_data"
FOLHAS_TABLE_ID = "folhas"
EMPRESAS_TABLE_ID = "empresas"
MOCK_DB = {}


def reset_mock_db():
    global MOCK_DB
    MOCK_DB = {
        EMPRESAS_TABLE_ID: pd.DataFrame(
            columns=["codigo_empresa", "cnpj", "nome_empresa", "client_id"]
        ),
        RAW_DATA_TABLE_ID: pd.DataFrame(
            columns=[
                "cnpj_empresa",
                "status_valor_cliente",
                "status_aba_origem",
                "mes_ano_referencia",
                "data_processamento_gcs",
                "nome_arquivo_origem",
                "client_id",
            ]
        ),
        FOLHAS_TABLE_ID: pd.DataFrame(
            columns=[
                "id_folha",
                "codigo_empresa",
                "cnpj_empresa",
                "mes_ano",
                "status",
                "data_envio_cliente",
                "data_guia_fgts",
                "data_darf_inss",
                "observacoes",
                "data_ultima_atualizacao_bq",
                "client_id",
            ]
        ),
    }


@pytest.fixture
def mock_bq_client():
    client = MagicMock(spec=bigquery.Client)
    client.project = TEST_PROJECT_ID

    def mock_query(query_string, job_config=None):
        mock_query_job = MagicMock(spec=bigquery.QueryJob)
        table_name_extracted = None
        if f"`{TEST_PROJECT_ID}.{TEST_DATASET_ID}.{EMPRESAS_TABLE_ID}`" in query_string:
            table_name_extracted = EMPRESAS_TABLE_ID
        elif (
            f"`{TEST_PROJECT_ID}.{TEST_DATASET_ID}.{RAW_DATA_TABLE_ID}`" in query_string
        ):
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
            if (
                client_id_filter
                and not df_to_return.empty
                and "client_id" in df_to_return.columns
            ):
                df_to_return = df_to_return[
                    df_to_return["client_id"] == client_id_filter
                ]
            nome_arquivo_filter = None
            if job_config and job_config.query_parameters:
                for param in job_config.query_parameters:
                    if param.name == "nome_arquivo_origem":
                        nome_arquivo_filter = param.value
                        break
            if (
                nome_arquivo_filter
                and not df_to_return.empty
                and "nome_arquivo_origem" in df_to_return.columns
            ):
                df_to_return = df_to_return[
                    df_to_return["nome_arquivo_origem"] == nome_arquivo_filter
                ]
            mock_query_job.to_dataframe.return_value = df_to_return
            mock_query_job.result.return_value = None
        return mock_query_job

    client.query = MagicMock(side_effect=mock_query)

    def mock_insert_rows_json(table_ref, rows, *args, **kwargs):
        table_id = (
            table_ref.table_id
            if hasattr(table_ref, "table_id")
            else str(table_ref).split(".")[-1]
        )
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
                new_rows_df[col] = new_rows_df[col].astype(
                    current_df[col].dtype, errors="ignore"
                )
        MOCK_DB[table_id] = pd.concat([current_df, new_rows_df], ignore_index=True)
        return []

    client.insert_rows_json = MagicMock(side_effect=mock_insert_rows_json)
    return client
