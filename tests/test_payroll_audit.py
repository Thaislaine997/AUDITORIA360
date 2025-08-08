"""
Test suite for the AI-powered payroll auditing system
"""

import pytest
import json
from fastapi.testclient import TestClient
from datetime import datetime, timezone

from portal_demandas.api import app
from portal_demandas.db import get_db, ContabilidadeDB, EmpresaDB, ProcessamentosFolhaDB


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def test_db():
    """Test database fixture"""
    db = next(get_db())
    
    # Create test data
    contabilidade = ContabilidadeDB(
        id=999,
        nome_contabilidade='Test Contabilidade',
        cnpj='99.999.999/0001-99'
    )
    db.add(contabilidade)
    
    empresa = EmpresaDB(
        id=999,
        nome='Test Company',
        contabilidade_id=999
    )
    db.add(empresa)
    
    try:
        db.commit()
        yield db
    finally:
        # Clean up
        db.query(ProcessamentosFolhaDB).filter(ProcessamentosFolhaDB.empresa_id == 999).delete()
        db.query(EmpresaDB).filter(EmpresaDB.id == 999).delete()
        db.query(ContabilidadeDB).filter(ContabilidadeDB.id == 999).delete()
        db.commit()
        db.close()


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "portal_demandas"


def test_payroll_audit_endpoint_validation(client):
    """Test payroll audit endpoint parameter validation"""
    # Test missing file
    response = client.post("/v1/folha/auditar?empresa_id=1&mes=7&ano=2024")
    assert response.status_code == 422  # Validation error
    
    # Test invalid month
    response = client.post("/v1/folha/auditar?empresa_id=1&mes=13&ano=2024")
    assert response.status_code == 400
    assert "Mês deve estar entre 1 e 12" in response.json()["detail"]
    
    # Test invalid year
    response = client.post("/v1/folha/auditar?empresa_id=1&mes=7&ano=2019")
    assert response.status_code == 400
    assert "Ano deve estar entre 2020 e 2030" in response.json()["detail"]


def test_payroll_audit_company_not_found(client):
    """Test payroll audit with non-existent company"""
    test_pdf_content = b"%PDF-1.4\ntest content"
    
    response = client.post(
        "/v1/folha/auditar?empresa_id=99999&mes=7&ano=2024",
        files={"arquivo_pdf": ("test.pdf", test_pdf_content, "application/pdf")}
    )
    assert response.status_code == 404
    assert "Empresa não encontrada" in response.json()["detail"]


def test_payroll_audit_invalid_file_type(client):
    """Test payroll audit with invalid file type"""
    test_content = b"not a pdf"
    
    response = client.post(
        "/v1/folha/auditar?empresa_id=1&mes=7&ano=2024",
        files={"arquivo_pdf": ("test.txt", test_content, "text/plain")}
    )
    assert response.status_code == 400
    assert "Apenas arquivos PDF são aceitos" in response.json()["detail"]


def test_list_payroll_processings_company_not_found(client):
    """Test listing processings for non-existent company"""
    response = client.get("/v1/folha/processamentos/99999")
    assert response.status_code == 404
    assert "Empresa não encontrada" in response.json()["detail"]


def test_list_payroll_processings_empty(client):
    """Test listing processings for company with no processings"""
    response = client.get("/v1/folha/processamentos/1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])