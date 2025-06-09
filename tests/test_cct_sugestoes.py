import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_processar_sugestao_rejeitar(monkeypatch):
    # Mock do controller para simular resposta
    async def mock_processar_sugestao_usuario(id_sugestao_impacto, payload):
        return {"message": "Sugestão rejeitada com sucesso."}
    import src.controllers.cct_sugestoes_controller as controller
    monkeypatch.setattr(controller, "processar_sugestao_usuario", mock_processar_sugestao_usuario)

    payload = {
        "acao_usuario": "REJEITAR",
        "usuario_revisao": "admin_teste",
        "notas_revisao_usuario": "Não se aplica ao cliente.",
        "dados_sugestao_atualizados_json": None
    }
    response = client.post("/api/v1/ccts/sugestoes-impacto/123/processar", json=payload)
    assert response.status_code == 200
    assert response.json()["message"].startswith("Sugestão rejeitada")

def test_processar_sugestao_aprovar(monkeypatch):
    async def mock_processar_sugestao_usuario(id_sugestao_impacto, payload):
        return {"message": "Sugestão aplicada com sucesso!"}
    import src.controllers.cct_sugestoes_controller as controller
    monkeypatch.setattr(controller, "processar_sugestao_usuario", mock_processar_sugestao_usuario)

    payload = {
        "acao_usuario": "APROVAR_APLICAR",
        "usuario_revisao": "admin_teste",
        "notas_revisao_usuario": "Aprovada após revisão.",
        "dados_sugestao_atualizados_json": None
    }
    response = client.post("/api/v1/ccts/sugestoes-impacto/456/processar", json=payload)
    assert response.status_code == 200
    assert response.json()["message"].startswith("Sugestão aplicada")

def test_processar_sugestao_erro(monkeypatch):
    async def mock_processar_sugestao_usuario(id_sugestao_impacto, payload):
        return {"erro": "Sugestão não encontrada."}
    import src.controllers.cct_sugestoes_controller as controller
    monkeypatch.setattr(controller, "processar_sugestao_usuario", mock_processar_sugestao_usuario)

    payload = {
        "acao_usuario": "REJEITAR",
        "usuario_revisao": "admin_teste",
        "notas_revisao_usuario": "Não encontrada.",
        "dados_sugestao_atualizados_json": None
    }
    response = client.post("/api/v1/ccts/sugestoes-impacto/999/processar", json=payload)
    assert response.status_code == 400
    assert "Sugestão não encontrada" in response.text
