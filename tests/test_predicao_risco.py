"""
Teste automatizado do pipeline preditivo de risco da folha
AUDITORIA360 – Módulo 3

- Simula envio de payload para o serviço de predição
- Valida resposta do endpoint
- (Opcional) Valida persistência no BigQuery
"""
import requests
import os
import pytest

# Ajuste a URL conforme ambiente de testes
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
        # ...adicione outras features se necessário...
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
