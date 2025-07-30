from unittest.mock import MagicMock

import pytest

from services.ingestion.bq_loader import ControleFolhaLoader, load_data_to_bq


@pytest.fixture
def config_cliente_a():
    return {
        "gcp_project_id": "fake-project",
        "control_bq_dataset_id": "fake_dataset",
        "bq_dataset_id": "fake_dataset",
        "bq_table_id": "fake_table",
        "gcp_location": "us-central1",
        "client_id": "cliente_a",
    }


@pytest.fixture
def config_cliente_b():
    return {
        "gcp_project_id": "fake-project",
        "control_bq_dataset_id": "fake_dataset",
        "bq_dataset_id": "fake_dataset",
        "bq_table_id": "fake_table",
        "gcp_location": "us-central1",
        "client_id": "cliente_b",
    }


# Definir um mock para get_bigquery_client
@pytest.fixture
def get_bigquery_client():
    return MagicMock()


def test_loader_exige_client_id(config_cliente_a):
    # Deve inicializar corretamente com client_id
    loader = ControleFolhaLoader(config_cliente_a)
    assert loader.client_id == "cliente_a"

    # Se faltar client_id, deve lançar erro
    config_sem_id = dict(config_cliente_a)
    config_sem_id.pop("client_id")
    with pytest.raises(ValueError):
        ControleFolhaLoader(config_sem_id)


def test_load_data_to_bigquery_exige_client_id(config_cliente_a):
    # Se faltar client_id, deve lançar erro
    sample_data = [{"id_extracao": "1", "id_item": "1"}]
    config_sem_id = dict(config_cliente_a)
    config_sem_id.pop("client_id")
    from unittest.mock import MagicMock

    client = MagicMock()  # Garante tipo correto
    full_table_id = f"{config_sem_id['gcp_project_id']}.{config_sem_id['bq_dataset_id']}.{config_sem_id['bq_table_id']}"
    with pytest.raises(ValueError):
        load_data_to_bq(sample_data, full_table_id, client)


# Teste de isolamento: simula que cada cliente só vê seus dados
# (mock do client/query, não faz acesso real ao BigQuery)
def test_listar_empresas_isolamento(monkeypatch, config_cliente_a, config_cliente_b):
    class FakeClient:
        def query(self, query, job_config=None):
            # Verifica se o filtro client_id está na query e no parâmetro
            assert "client_id = @client_id" in query
            assert job_config is not None
            param = job_config.query_parameters[0]

            # Retorna um objeto fake com to_dataframe
            class FakeResult:
                def to_dataframe(self):
                    return [param.value]  # Retorna o client_id para checagem

            return FakeResult()

    monkeypatch.setattr(
        "services.ingestion.bq_loader.get_bigquery_client", lambda config: FakeClient()
    )

    loader_a = ControleFolhaLoader(config_cliente_a)
    loader_b = ControleFolhaLoader(config_cliente_b)

    # Cada loader só "vê" seu próprio client_id
    result_a = loader_a.listar_todas_as_empresas()
    result_b = loader_b.listar_todas_as_empresas()

    # Se o resultado for DataFrame, converte para lista de valores
    import pandas as pd

    if isinstance(result_a, pd.DataFrame):
        result_a = result_a.values.flatten().tolist()
    if isinstance(result_b, pd.DataFrame):
        result_b = result_b.values.flatten().tolist()

    assert result_a == ["cliente_a"]
    assert result_b == ["cliente_b"]


# Exemplo de uso correto:
# client = MagicMock()
# full_table_id = "projeto.dataset.tabela"
# sample_data = [{"col1": "valor1"}]
# load_data_to_bq(sample_data, full_table_id, client, "projeto.dataset.tabela")
