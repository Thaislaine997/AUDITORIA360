import pytest
from src import bq_loader

@pytest.fixture
def config_cliente_a():
    return {
        "gcp_project_id": "fake-project",
        "control_bq_dataset_id": "fake_dataset",
        "bq_dataset_id": "fake_dataset",
        "bq_table_id": "fake_table",
        "gcp_location": "us-central1",
        "client_id": "cliente_a"
    }

@pytest.fixture
def config_cliente_b():
    return {
        "gcp_project_id": "fake-project",
        "control_bq_dataset_id": "fake_dataset",
        "bq_dataset_id": "fake_dataset",
        "bq_table_id": "fake_table",
        "gcp_location": "us-central1",
        "client_id": "cliente_b"
    }

def test_loader_exige_client_id(config_cliente_a):
    # Deve inicializar corretamente com client_id
    loader = bq_loader.ControleFolhaLoader(config_cliente_a)
    assert loader.client_id == "cliente_a"

    # Se faltar client_id, deve lançar erro
    config_sem_id = dict(config_cliente_a)
    config_sem_id.pop("client_id")
    with pytest.raises(ValueError):
        bq_loader.ControleFolhaLoader(config_sem_id)

def test_load_data_to_bigquery_exige_client_id(config_cliente_a):
    # Se faltar client_id, deve lançar erro
    sample_data = [{"id_extracao": "1", "id_item": "1"}]
    config_sem_id = dict(config_cliente_a)
    config_sem_id.pop("client_id")
    with pytest.raises(ValueError):
        bq_loader.load_data_to_bigquery(bq_loader.get_bigquery_client(config_sem_id), sample_data, config_sem_id)

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
    monkeypatch.setattr(bq_loader, "get_bigquery_client", lambda config: FakeClient())
    
    loader_a = bq_loader.ControleFolhaLoader(config_cliente_a)
    loader_b = bq_loader.ControleFolhaLoader(config_cliente_b)
    
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
