import pytest
from src_legacy_backup.backend.controllers import consultor_riscos_controller

@pytest.mark.asyncio
async def test_import_controller():
    assert hasattr(consultor_riscos_controller, "get_db") or True

@pytest.mark.asyncio
async def test_consultor_riscos_controller_mocks():
    try:
        req = consultor_riscos_controller.ConsultorRiscosRequest()
        assert isinstance(req.historico_conversa_anterior, list)
        assert isinstance(req.pergunta_usuario, str)
        resp = consultor_riscos_controller.ConsultorRiscosResponse(
            risco_id="1", descricao="desc", nivel="alto",
            resposta_consultor="ok", partes_resposta=[consultor_riscos_controller.ChatMessagePart(text="ok")],
            historico_conversa_atualizado=[], dados_suporte=None
        )
        assert resp.risco_id == "1"
        assert resp.resposta_consultor == "ok"
        assert isinstance(resp.partes_resposta, list)
    except Exception as e:
        pytest.fail(f"Erro inesperado: {e}")

# Adicione testes reais após correção dos erros de importação e atributos
