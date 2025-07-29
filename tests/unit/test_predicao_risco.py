"""
Teste automatizado do pipeline preditivo de risco da folha
AUDITORIA360 – Módulo 3

- Simula envio de payload para o serviço de predição
- Valida resposta do endpoint
- (Opcional) Valida persistência no BigQuery
"""
import pytest
# Removido import inexistente
from services.api.main import app
import os
import asyncio

# --- Teste unitário do serviço ---
def test_gerar_predicoes_risco_folha():
    id_folha_processada = "test_folha_123"
    id_cliente = "test_cliente_456"
    resultado = asyncio.run(gerar_predicoes_risco_folha(id_folha_processada, id_cliente))
    assert resultado is not None
    assert "id_predicao_risco" in resultado
    assert resultado["id_folha_processada_fk"] == id_folha_processada
    assert resultado["id_cliente"] == id_cliente
    assert "probabilidade_risco_alta_severidade" in resultado
    assert "classe_risco_predita" in resultado
    assert "score_saude_folha_calculado" in resultado
    assert isinstance(resultado["probabilidade_risco_alta_severidade"], float)
    assert isinstance(resultado["score_saude_folha_calculado"], (int, float))

# --- Teste de integração do endpoint ---
PREDICAO_URL = os.getenv("PREDICAO_URL", "http://localhost:8000/predicao/risco-folha")

@pytest.fixture
def folha_payload():
    return {
        "id_folha": "folha_teste_123",
        "competencia": "2025-05",
        "id_empresa": "empresa_teste_001",
        "total_proventos": 10000.0,
        "total_descontos": 2500.0,
        "valor_liquido": 7500.0,
        "proporcao_descontos": 0.25
    }

def test_predicao_risco_folha(folha_payload):
    response = requests.post(PREDICAO_URL, json=folha_payload)
    assert response.status_code == 200
    data = response.json()
    assert "score_risco" in data
    assert "classe_risco" in data
    assert "explicacao" in data
    assert data["id_folha"] == folha_payload["id_folha"]
    print("Resposta da predição:", data)

# (Opcional) Teste de persistência no BigQuery pode ser adicionado usando mocks ou integração real
