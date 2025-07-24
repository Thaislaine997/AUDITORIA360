import pytest
from src.schemas.parametros_legais_schemas import TabelaINSS, TabelaIRRF, TabelaSalarioFamilia, TabelaSalarioMinimo, TabelaFGTS
from src_legacy_backup.backend.controllers import param_legais_controller
from datetime import date

# Mock para BigQuery e dependências externas
class MockClient:
    def __init__(self):
        self.dataset = lambda x: self
        self.table = lambda x: self
    def insert_rows_json(self, table_ref, rows):
        return []
    def query(self, query, job_config=None):
        class Job:
            def result(self): return None
            num_dml_affected_rows = 1
        return Job()

@pytest.fixture(autouse=True)
def mock_bigquery(monkeypatch):
    monkeypatch.setattr(param_legais_controller, "bigquery", type('bigquery', (), {'Client': lambda project=None: MockClient()}))
    monkeypatch.setattr(param_legais_controller, "PROJECT_ID", "mock_project")
    monkeypatch.setattr(param_legais_controller, "DATASET_ID", "mock_dataset")
    monkeypatch.setattr(param_legais_controller, "TABLE_ID_INSS", "mock_table_inss")
    monkeypatch.setattr(param_legais_controller, "TABLE_ID_IRRF", "mock_table_irrf")
    monkeypatch.setattr(param_legais_controller, "TABLE_ID_SALARIO_FAMILIA", "mock_table_sf")
    monkeypatch.setattr(param_legais_controller, "TABLE_ID_SALARIO_MINIMO", "mock_table_sm")
    monkeypatch.setattr(param_legais_controller, "TABLE_ID_FGTS", "mock_table_fgts")
    # Mock funções de busca assíncronas
    async def obter_tabela_inss_por_id(id_versao):
        return TabelaINSS(ano=2025, faixas=[], id_versao=id_versao, data_criacao_registro=None, data_ultima_modificacao=None, data_inativacao=None, data_inicio_vigencia="2025-01-01", data_fim_vigencia="2025-12-31")
    async def obter_tabela_irrf_por_id(id_versao):
        return TabelaIRRF(ano=2025, faixas=[], id_versao=id_versao, data_criacao_registro=None, data_ultima_modificacao=None, data_inativacao=None, data_inicio_vigencia="2025-01-01", data_fim_vigencia="2025-12-31")
    async def obter_tabela_salario_familia_por_id(id_versao):
        return TabelaSalarioFamilia(ano=2025, faixa="A", valor=100.0, id_versao=id_versao, data_criacao_registro=None, data_ultima_modificacao=None, data_inativacao=None, data_inicio_vigencia="2025-01-01", data_fim_vigencia="2025-12-31")
    async def obter_tabela_salario_minimo_por_id(id_versao):
        return TabelaSalarioMinimo(ano=2025, valor=1412.0, id_versao=id_versao, data_criacao_registro=None, data_ultima_modificacao=None, data_inativacao=None, data_inicio_vigencia="2025-01-01", data_fim_vigencia="2025-12-31")
    async def obter_tabela_fgts_por_id(id_versao):
        return TabelaFGTS(ano=2025, aliquota=8.0, id_versao=id_versao, data_criacao_registro=None, data_ultima_modificacao=None, data_inativacao=None, data_inicio_vigencia="2025-01-01", data_fim_vigencia="2025-12-31")
    monkeypatch.setattr(param_legais_controller, "obter_tabela_inss_por_id", obter_tabela_inss_por_id)
    monkeypatch.setattr(param_legais_controller, "obter_tabela_irrf_por_id", obter_tabela_irrf_por_id)
    monkeypatch.setattr(param_legais_controller, "obter_tabela_salario_familia_por_id", obter_tabela_salario_familia_por_id)
    monkeypatch.setattr(param_legais_controller, "obter_tabela_salario_minimo_por_id", obter_tabela_salario_minimo_por_id)
    monkeypatch.setattr(param_legais_controller, "obter_tabela_fgts_por_id", obter_tabela_fgts_por_id)
    # Mock da função _verificar_conflito_vigencia
    async def _verificar_conflito_vigencia(*args, **kwargs):
        return None
    monkeypatch.setattr(param_legais_controller, "_verificar_conflito_vigencia", _verificar_conflito_vigencia)

# Testes básicos de atualização de cada tabela legal
@pytest.mark.asyncio
async def test_atualizar_tabela_inss(mock_bigquery):
    data = TabelaINSS(
        ano=2025,
        faixas=[],
        id_versao="1",
        data_inicio_vigencia=date(2025, 1, 1).isoformat(),
        data_fim_vigencia=date(2025, 12, 31).isoformat(),
        data_criacao_registro=None,
        data_ultima_modificacao=None,
        data_inativacao=None
    )
    result = await param_legais_controller.atualizar_tabela_inss("1", data)
    assert result.id_versao != "1"
    assert result.data_criacao_registro is not None
    assert result.data_ultima_modificacao is not None

@pytest.mark.asyncio
async def test_atualizar_tabela_irrf(mock_bigquery):
    data = TabelaIRRF(
        ano=2025,
        faixas=[],
        id_versao="1",
        data_inicio_vigencia=date(2025, 1, 1).isoformat(),
        data_fim_vigencia=date(2025, 12, 31).isoformat(),
        data_criacao_registro=None,
        data_ultima_modificacao=None,
        data_inativacao=None
    )
    result = await param_legais_controller.atualizar_tabela_irrf("1", data)
    assert result.id_versao != "1"
    assert result.data_criacao_registro is not None
    assert result.data_ultima_modificacao is not None

@pytest.mark.asyncio
async def test_atualizar_tabela_salario_familia(mock_bigquery):
    data = TabelaSalarioFamilia(
        ano=2025,
        faixa="A",
        valor=100.0,
        id_versao="1",
        data_inicio_vigencia=date(2025, 1, 1).isoformat(),
        data_fim_vigencia=date(2025, 12, 31).isoformat(),
        data_criacao_registro=None,
        data_ultima_modificacao=None,
        data_inativacao=None
    )
    result = await param_legais_controller.atualizar_tabela_salario_familia("1", data)
    assert result.id_versao != "1"
    assert result.data_criacao_registro is not None
    assert result.data_ultima_modificacao is not None

@pytest.mark.asyncio
async def test_atualizar_tabela_salario_minimo(mock_bigquery):
    data = TabelaSalarioMinimo(
        ano=2025,
        valor=1412.0,
        id_versao="1",
        data_inicio_vigencia=date(2025, 1, 1).isoformat(),
        data_fim_vigencia=date(2025, 12, 31).isoformat(),
        data_criacao_registro=None,
        data_ultima_modificacao=None,
        data_inativacao=None
    )
    result = await param_legais_controller.atualizar_tabela_salario_minimo("1", data)
    assert result.id_versao != "1"
    assert result.data_criacao_registro is not None
    assert result.data_ultima_modificacao is not None

@pytest.mark.asyncio
async def test_atualizar_tabela_fgts(mock_bigquery):
    data = TabelaFGTS(
        ano=2025,
        aliquota=8.0,
        id_versao="1",
        data_inicio_vigencia=date(2025, 1, 1).isoformat(),
        data_fim_vigencia=date(2025, 12, 31).isoformat(),
        data_criacao_registro=None,
        data_ultima_modificacao=None,
        data_inativacao=None
    )
    result = await param_legais_controller.atualizar_tabela_fgts("1", data)
    assert result.id_versao != "1"
    assert result.data_criacao_registro is not None
    assert result.data_ultima_modificacao is not None
