import pytest
from fastapi.testclient import TestClient
from portal_demandas.api import app
from portal_demandas.models import Ticket
from datetime import datetime, timedelta

client = TestClient(app)

def test_criar_e_obter_ticket():
    payload = {
        "titulo": "Teste Ticket",
        "descricao": "Descrição de teste",
        "etapa": "inicial",
        "prazo": (datetime.now() + timedelta(days=2)).isoformat(),
        "responsavel": "dev"
    }
    response = client.post("/tickets/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == payload["titulo"]
    assert data["descricao"] == payload["descricao"]
    assert data["etapa"] == payload["etapa"]
    assert data["responsavel"] == payload["responsavel"]
    assert isinstance(data["prazo"], str)
    ticket_id = data["id"]

    response_get = client.get(f"/tickets/{ticket_id}")
    assert response_get.status_code == 200
    data_get = response_get.json()
    assert data_get["id"] == ticket_id
    assert data_get["titulo"] == payload["titulo"]

def test_listar_tickets():
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
