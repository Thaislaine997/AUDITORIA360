import pytest
from src.backend.services.predicao_risco_service import *
import asyncio

def test_gerar_predicoes_risco_folha():
    # Mock data for testing
    id_folha_processada = "test_folha_123"
    id_cliente = "test_cliente_456"

    # Call the function to test
    resultado = asyncio.run(gerar_predicoes_risco_folha(id_folha_processada, id_cliente))

    # Assertions to validate the output
    assert resultado is not None
    assert "id_predicao_risco" in resultado
    assert resultado["id_folha_processada_fk"] == id_folha_processada
    assert resultado["id_cliente"] == id_cliente
    assert "probabilidade_risco_alta_severidade" in resultado
    assert "classe_risco_predita" in resultado
    assert "score_saude_folha_calculado" in resultado
    assert isinstance(resultado["probabilidade_risco_alta_severidade"], float)
    assert isinstance(resultado["score_saude_folha_calculado"], (int, float))