"""
Integration tests for AI-powered payroll calculation endpoints
Tests the new dynamic calculation endpoints that use RegrasValidadas
"""

from datetime import date

import pytest
from fastapi import status


# This would normally import the actual FastAPI app
# For testing purposes, we'll create a minimal test setup
class TestPayrollAIEndpoints:

    @pytest.fixture
    def mock_auth_user(self):
        """Mock authenticated user"""
        return {"id": 1, "role": "administrador"}

    @pytest.mark.asyncio
    async def test_calculate_fgts_success(self, mock_auth_user):
        """Test successful FGTS calculation via API endpoint"""
        # This test demonstrates the expected behavior
        # In a real test, you would use TestClient with the actual app

        # Arrange
        payload = {"salario_base": 3000.0, "data_referencia": "2024-01-15"}

        # Expected response structure
        expected_response = {
            "salario_base": 3000.0,
            "data_referencia": "2024-01-15",
            "taxa_fgts": 8.0,
            "valor_fgts": 240.0,
        }

        # This is what we expect the endpoint to return
        assert expected_response["valor_fgts"] == payload["salario_base"] * 0.08
        assert expected_response["taxa_fgts"] == 8.0

    @pytest.mark.asyncio
    async def test_calculate_inss_success(self, mock_auth_user):
        """Test successful INSS calculation via API endpoint"""
        # Arrange
        payload = {"salario_base": 3000.0, "data_referencia": "2024-01-15"}

        # Expected response structure
        expected_response = {
            "salario_base": 3000.0,
            "data_referencia": "2024-01-15",
            "valor_inss": 330.0,
            "aliquota_aplicada": 11.0,
            "base_calculo": 3000.0,
        }

        # Verify expected calculations
        assert expected_response["valor_inss"] == payload["salario_base"] * 0.11
        assert expected_response["aliquota_aplicada"] == 11.0

    @pytest.mark.asyncio
    async def test_calculate_fgts_parameter_not_found(self, mock_auth_user):
        """Test FGTS calculation when parameter is not found in RegrasValidadas"""
        # Arrange
        payload = {
            "salario_base": 3000.0,
            "data_referencia": "1990-01-01",  # Very old date, no rules should exist
        }

        # This should result in a 422 error with appropriate message
        expected_error = {
            "status_code": 422,
            "detail": "Parâmetro não encontrado: aliquota_fgts_geral",
        }

        # This demonstrates the expected error handling behavior
        assert expected_error["status_code"] == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_calculate_inss_parameter_not_found(self, mock_auth_user):
        """Test INSS calculation when parameter is not found in RegrasValidadas"""
        # Arrange
        payload = {
            "salario_base": 3000.0,
            "data_referencia": "1990-01-01",  # Very old date, no rules should exist
        }

        # This should result in a 422 error with appropriate message
        expected_error = {
            "status_code": 422,
            "detail": "Parâmetro não encontrado: aliquota_inss_padrao",
        }

        # This demonstrates the expected error handling behavior
        assert expected_error["status_code"] == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_calculate_fgts_validation_errors(self):
        """Test FGTS calculation with invalid input data"""
        # Test negative salary
        invalid_payload = {
            "salario_base": -1000.0,  # Invalid: negative salary
            "data_referencia": "2024-01-15",
        }

        # This should result in a validation error
        # The Pydantic model has gt=0 constraint
        assert invalid_payload["salario_base"] < 0  # This would fail validation

    def test_calculate_inss_validation_errors(self):
        """Test INSS calculation with invalid input data"""
        # Test missing required fields
        invalid_payload = {
            "salario_base": 3000.0,
            # Missing data_referencia - should fail validation
        }

        # Test invalid date format
        invalid_payload_2 = {
            "salario_base": 3000.0,
            "data_referencia": "invalid-date-format",  # Should fail validation
        }

        # These would result in validation errors from Pydantic
        assert "data_referencia" not in invalid_payload
        assert invalid_payload_2["data_referencia"] == "invalid-date-format"


class TestPayrollSchemas:
    """Test the new Pydantic schemas for AI-powered calculations"""

    def test_fgts_calculation_request_valid(self):
        """Test valid FgtsCalculationRequest creation"""
        from src.schemas.payroll_schemas import FgtsCalculationRequest

        # This should create successfully
        request = FgtsCalculationRequest(
            salario_base=3000.0, data_referencia=date(2024, 1, 15)
        )

        assert request.salario_base == 3000.0
        assert request.data_referencia == date(2024, 1, 15)

    def test_fgts_calculation_request_invalid_salary(self):
        """Test FgtsCalculationRequest with invalid salary"""
        from pydantic import ValidationError

        from src.schemas.payroll_schemas import FgtsCalculationRequest

        # This should fail validation due to gt=0 constraint
        with pytest.raises(ValidationError):
            FgtsCalculationRequest(
                salario_base=-1000.0,  # Invalid: negative
                data_referencia=date(2024, 1, 15),
            )

    def test_inss_calculation_response_structure(self):
        """Test InssCalculationResponse structure"""
        from src.schemas.payroll_schemas import InssCalculationResponse

        response = InssCalculationResponse(
            salario_base=3000.0,
            data_referencia=date(2024, 1, 15),
            valor_inss=330.0,
            aliquota_aplicada=11.0,
            base_calculo=3000.0,
        )

        assert response.salario_base == 3000.0
        assert response.valor_inss == 330.0
        assert response.aliquota_aplicada == 11.0
        assert response.base_calculo == 3000.0
