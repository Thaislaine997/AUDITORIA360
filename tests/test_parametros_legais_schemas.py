import pytest
from src.schemas.parametros_legais_schemas import TabelaSalarioMinimo, TabelaSalarioFamilia, TabelaFGTS, TabelaIRRF, FaixaIRRF, TabelaINSS, FaixaINSS

def test_tabela_salario_minimo():
    obj = TabelaSalarioMinimo(ano=2025, valor=1500.0)
    assert obj.ano == 2025
    assert obj.valor == 1500.0

def test_tabela_salario_familia():
    obj = TabelaSalarioFamilia(ano=2025, faixa="A", valor=50.0)
    assert obj.faixa == "A"
    assert obj.valor == 50.0

def test_tabela_fgts():
    obj = TabelaFGTS(ano=2025, aliquota=8.0)
    assert obj.aliquota == 8.0

def test_tabela_irrf():
    faixa = FaixaIRRF(faixa="1", valor=100.0)
    obj = TabelaIRRF(ano=2025, faixas=[faixa])
    assert obj.faixas[0].valor == 100.0

def test_tabela_inss():
    faixa = FaixaINSS(faixa="1", valor=200.0)
    obj = TabelaINSS(ano=2025, faixas=[faixa])
    assert obj.faixas[0].valor == 200.0
