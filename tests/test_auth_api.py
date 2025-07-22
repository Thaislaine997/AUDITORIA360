import pytest
from fastapi.testclient import TestClient
from services.api.main import app
import json

client = TestClient(app)

class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_health_check(self):
        """Test API health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "auth" in data["services"]
    
    def test_auth_health_check(self):
        """Test auth service health check."""
        response = client.get("/auth/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "authentication"
        assert "users_count" in data
    
    def test_login_valid_credentials(self):
        """Test login with valid credentials."""
        login_data = {
            "email": "admin@auditoria360.com",
            "password": "admin123"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_at" in data
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        login_data = {
            "email": "admin@auditoria360.com",
            "password": "wrong_password"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
        data = response.json()
        assert "Email ou senha incorretos" in data["detail"]
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent user."""
        login_data = {
            "email": "nonexistent@test.com",
            "password": "any_password"
        }
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 401
    
    def test_get_current_user_without_token(self):
        """Test accessing protected endpoint without token."""
        response = client.get("/auth/me")
        assert response.status_code == 403  # No token provided
    
    def test_get_current_user_with_invalid_token(self):
        """Test accessing protected endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_full_auth_flow(self):
        """Test complete authentication flow: login -> get user info."""
        # Login
        login_data = {
            "email": "demo@empresa.com",
            "password": "demo123"
        }
        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == 200
        token_data = login_response.json()
        
        # Use token to get user info
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        user_response = client.get("/auth/me", headers=headers)
        assert user_response.status_code == 200
        user_data = user_response.json()
        assert user_data["email"] == "demo@empresa.com"
        assert user_data["full_name"] == "Usuário Demonstração"
        assert user_data["is_active"] is True
    
    def test_register_new_user(self):
        """Test user registration."""
        register_data = {
            "email": "newuser@test.com",
            "password": "newpassword123",
            "full_name": "Novo Usuário",
            "empresa_id": "empresa_test"
        }
        response = client.post("/auth/register", json=register_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@test.com"
        assert data["full_name"] == "Novo Usuário"
        assert data["empresa_id"] == "empresa_test"
        assert data["is_active"] is True
    
    def test_register_duplicate_email(self):
        """Test registration with existing email."""
        register_data = {
            "email": "admin@auditoria360.com",  # Already exists
            "password": "newpassword123", 
            "full_name": "Duplicate User"
        }
        response = client.post("/auth/register", json=register_data)
        assert response.status_code == 400
        data = response.json()
        assert "Email já cadastrado" in data["detail"]
    
    def test_logout(self):
        """Test logout endpoint."""
        response = client.post("/auth/logout")
        assert response.status_code == 200
        data = response.json()
        assert "Logout realizado com sucesso" in data["message"]

class TestAPIIntegration:
    """Test API integration and overall functionality."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns project info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Auditoria360" in data["message"]
        assert data["version"] == "0.2.0"
        assert "features" in data
        assert "Authentication system" in data["features"]
    
    def test_explainability_endpoint(self):
        """Test explainability endpoint is accessible."""
        test_event = {"test": "data"}
        response = client.post("/explainability/executar-pipeline", json=test_event)
        assert response.status_code == 200
        # Should return pipeline execution result