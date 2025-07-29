"""
Tests for API health endpoints and basic functionality
"""

import pytest
from api.index import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check():
    """Test the basic health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "AUDITORIA360" in data["message"]
    assert "version" in data
    assert "modules" in data


def test_detailed_health():
    """Test the detailed health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "environment" in data
    assert "database" in data
    assert "version" in data


def test_legacy_contabilidades_options():
    """Test legacy contabilidades options endpoint"""
    response = client.get("/api/v1/auditorias/options/contabilidades")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    assert all("id" in item and "nome" in item for item in data["data"])


def test_legacy_contabilidades_options_old_route():
    """Test legacy contabilidades options endpoint (old route)"""
    response = client.get("/contabilidades/options")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0


def test_event_handler():
    """Test event handler endpoint"""
    response = client.post("/event-handler", json={"bucket": "test-bucket"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processed"
    assert data["bucket"] == "test-bucket"


def test_event_handler_without_data():
    """Test event handler endpoint without data"""
    response = client.post("/event-handler")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processed"
    assert data["bucket"] == "default"


def test_api_docs_available():
    """Test that API documentation is available"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_spec():
    """Test that OpenAPI specification is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "info" in data
    assert "paths" in data
