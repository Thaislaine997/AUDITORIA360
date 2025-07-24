import pytest
from src_legacy_backup.backend.controllers import predicao_risco_controller
import asyncio

def test_obter_dados_predicao_para_dashboard():
    # Mock data for testing
    id_folha_processada = "folha_com_predicao_existente"
    id_cliente = "test_cliente_456"

    # Instanciar o controller
    from src_legacy_backup.backend.controllers.predicao_risco_controller import PredicaoRiscoController
    controller = PredicaoRiscoController()

    # Chamar o método assíncrono
    resultado = asyncio.run(controller.obter_dados_predicao_para_dashboard(id_folha_processada, id_cliente))

    # Assertions para o schema retornado
    assert resultado is not None
    assert resultado.score_saude_folha == 85.0
    assert resultado.classe_risco_geral == "MEDIO"
    assert isinstance(resultado.principais_riscos_previstos, list)
    assert len(resultado.principais_riscos_previstos) > 0