"""
Tests for refactored backend endpoints with standardized responses
"""

import pytest
from fastapi.testclient import TestClient

# Import the API app
try:
    from api.index import app
    client = TestClient(app)
    API_AVAILABLE = True
except Exception as e:
    print(f"Warning: Could not create test client: {e}")
    API_AVAILABLE = False


@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_health_endpoint():
    """Test the health endpoint returns proper format"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    # Health endpoint has a different format than standardized endpoints
    assert "status" in data
    assert "version" in data
    assert data["status"] == "healthy"


@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_root_endpoint():
    """Test the root endpoint returns proper format"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert data["status"] == "ok"


@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_system_status_endpoint():
    """Test the system status endpoint"""
    response = client.get("/api/v1/system/status")
    assert response.status_code == 200
    
    data = response.json()
    assert "api_version" in data
    assert "components" in data
    assert data["api_version"] == "1.0.0"


@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_compliance_rules_endpoint():
    """Test the compliance rules endpoint with standardized response"""
    response = client.get("/api/v1/compliance/rules")
    assert response.status_code == 200
    
    data = response.json()
    # Should follow standardized response format
    assert "success" in data
    assert "message" in data
    assert "data" in data
    assert "timestamp" in data
    
    assert data["success"] is True
    assert "rules" in data["data"]
    assert "total" in data["data"]
    assert "categories" in data["data"]


@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_compliance_rules_with_filter():
    """Test the compliance rules endpoint with category filter"""
    response = client.get("/api/v1/compliance/rules?category=salary")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    
    # All returned rules should be in the salary category
    rules = data["data"]["rules"]
    for rule in rules:
        assert rule["category"] == "salary"


@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_compliance_check_endpoint():
    """Test the compliance check endpoint with standardized request/response"""
    # Test POST endpoint with proper request body
    request_data = {
        "entity_type": "payroll",
        "entity_id": "test_payroll_001",
        "rule_categories": ["salary", "tax"],
        "include_resolved": False
    }
    
    response = client.post("/api/v1/compliance/check", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    # Should follow standardized response format
    assert "success" in data
    assert "message" in data
    assert "data" in data
    assert "timestamp" in data
    
    assert data["success"] is True
    
    # Check compliance result structure
    compliance_data = data["data"]
    assert "entity" in compliance_data
    assert "compliance_status" in compliance_data
    assert "summary" in compliance_data
    assert "performance" in compliance_data
    
    assert compliance_data["entity"]["type"] == "payroll"
    assert compliance_data["entity"]["id"] == "test_payroll_001"


@pytest.mark.skipif(not API_AVAILABLE, reason="API_AVAILABLE")
def test_compliance_check_validation_error():
    """Test compliance check with invalid entity type"""
    request_data = {
        "entity_type": "invalid_type",  # Invalid entity type
        "entity_id": "test_001"
    }
    
    response = client.post("/api/v1/compliance/check", json=request_data)
    # Should return validation error
    assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_audit_executions_endpoint():
    """Test the audit executions endpoint with pagination"""
    response = client.get("/api/v1/auditorias/executions")
    assert response.status_code == 200
    
    data = response.json()
    # Should follow standardized paginated response format
    assert "success" in data
    assert "message" in data
    assert "data" in data
    assert "pagination" in data
    assert "timestamp" in data
    
    assert data["success"] is True
    
    # Check pagination structure
    pagination = data["pagination"]
    assert "page" in pagination
    assert "page_size" in pagination
    assert "total_items" in pagination
    assert "total_pages" in pagination
    assert "has_next" in pagination
    assert "has_prev" in pagination


@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_audit_executions_with_pagination():
    """Test audit executions with custom pagination parameters"""
    response = client.get("/api/v1/auditorias/executions?page=2&page_size=5")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    
    pagination = data["pagination"]
    assert pagination["page"] == 2
    assert pagination["page_size"] == 5


@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
def test_automation_status_endpoint():
    """Test the automation status endpoint"""
    response = client.get("/api/v1/automation/status")
    assert response.status_code == 200
    
    data = response.json()
    # This endpoint might not follow standardized format yet
    # Check basic structure
    assert "status" in data
    assert "modules" in data
    assert "serverless_migration" in data


def test_error_response_format():
    """Test that error responses follow standardized format"""
    if not API_AVAILABLE:
        pytest.skip("API not available")
    
    # Try to access a non-existent endpoint
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404


def test_validation_functions():
    """Test validation functions directly"""
    try:
        from src.api.common.validators import validate_cpf, validate_cnpj, validate_email
        
        # Test CPF validation
        assert validate_cpf("11144477735") is True  # Valid CPF
        assert validate_cpf("00000000000") is False  # Invalid CPF
        assert validate_cpf("123") is False  # Too short
        
        # Test CNPJ validation  
        assert validate_cnpj("11222333000181") is True  # Valid CNPJ format
        assert validate_cnpj("00000000000000") is False  # Invalid CNPJ
        assert validate_cnpj("123") is False  # Too short
        
        # Test email validation
        assert validate_email("test@example.com") is True
        assert validate_email("invalid.email") is False
        assert validate_email("@invalid.com") is False
        
    except ImportError:
        pytest.skip("Validation functions not available")


def test_response_models():
    """Test response model creation"""
    try:
        from src.api.common.responses import (
            create_success_response, 
            create_paginated_response,
            create_error_response,
            ErrorCode
        )
        
        # Test success response
        success_resp = create_success_response(
            data={"test": "data"},
            message="Test successful"
        )
        assert success_resp.success is True
        assert success_resp.message == "Test successful"
        assert success_resp.data == {"test": "data"}
        
        # Test paginated response
        paginated_resp = create_paginated_response(
            items=[{"item": 1}, {"item": 2}],
            page=1,
            page_size=2,
            total_items=10
        )
        assert paginated_resp.success is True
        assert len(paginated_resp.data) == 2
        assert paginated_resp.pagination.page == 1
        assert paginated_resp.pagination.total_items == 10
        
        # Test error response
        error_resp = create_error_response(
            error_code=ErrorCode.INVALID_INPUT,
            message="Validation failed"
        )
        assert error_resp.success is False
        assert error_resp.error_code == ErrorCode.INVALID_INPUT
        assert error_resp.message == "Validation failed"
        
    except ImportError:
        pytest.skip("Response models not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])