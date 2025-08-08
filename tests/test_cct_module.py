"""
Testes para o módulo de Convenções Coletivas de Trabalho (CCTs) e Sindicatos
"""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.api.routers.cct import router
from src.services.cct_service import CCTService


# Create a test app with the CCT router
app = FastAPI()
app.include_router(router, prefix="/cct", tags=["CCT"])

client = TestClient(app)


class TestCCTService:
    """Testes para o serviço CCT"""
    
    def test_init_without_supabase(self):
        """Testa inicialização do serviço sem Supabase disponível"""
        with patch('src.services.cct_service.SUPABASE_AVAILABLE', False):
            service = CCTService()
            assert service.client is None
    
    @patch('src.services.cct_service.get_supabase_client')
    def test_criar_sindicato_success(self, mock_get_client):
        """Testa criação de sindicato com sucesso"""
        # Mock do cliente Supabase
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [{"id": 1, "nome_sindicato": "Sindicato Teste"}]
        
        mock_client.from_.return_value.insert.return_value.execute.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        service = CCTService()
        dados = {"nome_sindicato": "Sindicato Teste", "cnpj": "12.345.678/0001-99"}
        
        resultado = service.criar_sindicato(dados)
        
        assert resultado["id"] == 1
        assert resultado["nome_sindicato"] == "Sindicato Teste"
        mock_client.from_.assert_called_with("Sindicatos")
    
    @patch('src.services.cct_service.get_supabase_client')
    def test_listar_sindicatos_success(self, mock_get_client):
        """Testa listagem de sindicatos com sucesso"""
        # Mock do cliente Supabase
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [
            {"id": 1, "nome_sindicato": "Sindicato A"},
            {"id": 2, "nome_sindicato": "Sindicato B"}
        ]
        
        mock_client.from_.return_value.select.return_value.range.return_value.execute.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        service = CCTService()
        resultados = service.listar_sindicatos()
        
        assert len(resultados) == 2
        assert resultados[0]["nome_sindicato"] == "Sindicato A"
        mock_client.from_.assert_called_with("Sindicatos")
    
    @patch('src.services.cct_service.get_supabase_client')
    def test_criar_convencao_coletiva_success(self, mock_get_client):
        """Testa criação de CCT com sucesso"""
        # Mock do cliente Supabase
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [{"id": 1, "sindicato_id": 1, "vigencia_inicio": "2024-01-01"}]
        
        mock_client.from_.return_value.insert.return_value.execute.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        service = CCTService()
        dados = {
            "sindicato_id": 1,
            "vigencia_inicio": "2024-01-01",
            "vigencia_fim": "2024-12-31"
        }
        
        resultado = service.criar_convencao_coletiva(dados)
        
        assert resultado["id"] == 1
        assert resultado["sindicato_id"] == 1
        mock_client.from_.assert_called_with("ConvencoesColetivas")
    
    def test_service_error_without_client(self):
        """Testa erro quando cliente não está disponível"""
        with patch('src.services.cct_service.SUPABASE_AVAILABLE', False):
            service = CCTService()
            
            with pytest.raises(RuntimeError, match="Supabase client not available"):
                service.criar_sindicato({"nome_sindicato": "Test"})


class TestCCTAPI:
    """Testes para a API CCT"""
    
    @patch('src.api.routers.cct.get_cct_service')
    def test_criar_sindicato_endpoint(self, mock_get_service):
        """Testa endpoint de criação de sindicato"""
        # Mock do serviço
        mock_service = Mock()
        mock_service.criar_sindicato.return_value = {"id": 1, "nome_sindicato": "Test"}
        mock_get_service.return_value = mock_service
        
        response = client.post("/cct/sindicatos", json={
            "nome_sindicato": "Test",
            "cnpj": "12.345.678/0001-99"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["id"] == 1
    
    @patch('src.api.routers.cct.get_cct_service')
    def test_listar_sindicatos_endpoint(self, mock_get_service):
        """Testa endpoint de listagem de sindicatos"""
        # Mock do serviço
        mock_service = Mock()
        mock_service.listar_sindicatos.return_value = [
            {"id": 1, "nome_sindicato": "Sindicato A"}
        ]
        mock_get_service.return_value = mock_service
        
        response = client.get("/cct/sindicatos")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) == 1
    
    @patch('src.api.routers.cct.get_cct_service')
    def test_criar_cct_endpoint(self, mock_get_service):
        """Testa endpoint de criação de CCT"""
        # Mock do serviço
        mock_service = Mock()
        mock_service.criar_convencao_coletiva.return_value = {
            "id": 1, 
            "sindicato_id": 1,
            "vigencia_inicio": "2024-01-01"
        }
        mock_get_service.return_value = mock_service
        
        response = client.post("/cct/", json={
            "sindicato_id": 1,
            "vigencia_inicio": "2024-01-01",
            "vigencia_fim": "2024-12-31"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["sindicato_id"] == 1
    
    @patch('src.api.routers.cct.get_cct_service')
    def test_obter_sindicato_not_found(self, mock_get_service):
        """Testa endpoint quando sindicato não é encontrado"""
        # Mock do serviço
        mock_service = Mock()
        mock_service.obter_sindicato.return_value = None
        mock_get_service.return_value = mock_service
        
        response = client.get("/cct/sindicatos/999")
        
        assert response.status_code == 404
        data = response.json()
        assert "não encontrado" in data["detail"]
    
    @patch('src.api.routers.cct.get_cct_service')
    def test_associar_empresa_sindicato_endpoint(self, mock_get_service):
        """Testa endpoint de associação empresa-sindicato"""
        # Mock do serviço
        mock_service = Mock()
        mock_service.associar_empresa_sindicato.return_value = {
            "id": 1,
            "sindicato_id": 1
        }
        mock_get_service.return_value = mock_service
        
        response = client.post("/cct/empresas/1/sindicato/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["sindicato_id"] == 1
    
    def test_compare_ccts_not_implemented(self):
        """Testa endpoint de comparação (não implementado)"""
        response = client.post("/cct/1/compare/2")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "not_implemented"
        assert "versão futura" in data["message"]


class TestDataValidation:
    """Testes de validação de dados"""
    
    def test_sindicato_create_validation(self):
        """Testa validação de dados para criação de sindicato"""
        # Teste com dados inválidos (falta nome_sindicato)
        response = client.post("/cct/sindicatos", json={
            "cnpj": "12.345.678/0001-99"
        })
        
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_cct_create_validation(self):
        """Testa validação de dados para criação de CCT"""
        # Teste com dados inválidos (falta sindicato_id)
        response = client.post("/cct/", json={
            "vigencia_inicio": "2024-01-01",
            "vigencia_fim": "2024-12-31"
        })
        
        assert response.status_code == 422  # Unprocessable Entity


def test_migration_script_exists():
    """Testa se o script de migração existe"""
    import os
    
    migration_path = "/home/runner/work/AUDITORIA360/AUDITORIA360/migrations/007_modulo_cct_sindicatos.sql"
    assert os.path.exists(migration_path), "Script de migração não encontrado"
    
    # Verifica se contém as tabelas esperadas
    with open(migration_path, 'r') as f:
        content = f.read()
        assert "Sindicatos" in content
        assert "ConvencoesColetivas" in content
        assert "sindicato_id" in content
        assert "ROW LEVEL SECURITY" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])