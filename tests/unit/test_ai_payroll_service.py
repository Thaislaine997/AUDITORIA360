"""
Unit tests for AI-powered PayrollService
Tests dynamic parameter lookup from RegrasValidadas table
"""

from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from src.services.payroll_service import AIPayrollService


class TestAIPayrollService:

    @pytest.fixture
    def mock_supabase_client(self):
        """Create a mock Supabase client"""
        mock_client = AsyncMock()
        return mock_client

    @pytest.fixture
    def ai_service(self, mock_supabase_client):
        """Create AIPayrollService instance with mocked client"""
        return AIPayrollService(mock_supabase_client)

    @pytest.mark.asyncio
    async def test_obter_parametro_success(self, ai_service, mock_supabase_client):
        """Test successful parameter lookup"""
        # Arrange
        mock_response = MagicMock()
        mock_response.data = [{"valor_parametro": "8.0"}]

        # Create a proper async mock chain
        mock_query = AsyncMock()
        mock_query.select = MagicMock(return_value=mock_query)
        mock_query.eq = MagicMock(return_value=mock_query)
        mock_query.lte = MagicMock(return_value=mock_query)
        mock_query.or_ = MagicMock(return_value=mock_query)
        mock_query.order = MagicMock(return_value=mock_query)
        mock_query.limit = MagicMock(return_value=mock_query)
        mock_query.execute = AsyncMock(return_value=mock_response)

        mock_supabase_client.from_ = MagicMock(return_value=mock_query)

        # Act
        resultado = await ai_service._obter_parametro(
            "aliquota_fgts_geral", date(2024, 1, 15)
        )

        # Assert
        assert resultado == "8.0"
        mock_supabase_client.from_.assert_called_once_with("RegrasValidadas")

    @pytest.mark.asyncio
    async def test_obter_parametro_not_found(self, ai_service, mock_supabase_client):
        """Test parameter not found scenario"""
        # Arrange
        mock_response = MagicMock()
        mock_response.data = []  # Empty response

        # Create a proper async mock chain
        mock_query = AsyncMock()
        mock_query.select = MagicMock(return_value=mock_query)
        mock_query.eq = MagicMock(return_value=mock_query)
        mock_query.lte = MagicMock(return_value=mock_query)
        mock_query.or_ = MagicMock(return_value=mock_query)
        mock_query.order = MagicMock(return_value=mock_query)
        mock_query.limit = MagicMock(return_value=mock_query)
        mock_query.execute = AsyncMock(return_value=mock_response)

        mock_supabase_client.from_ = MagicMock(return_value=mock_query)

        # Act & Assert
        with pytest.raises(ValueError, match="Parâmetro não encontrado"):
            await ai_service._obter_parametro(
                "parametro_inexistente", date(2024, 1, 15)
            )

    @pytest.mark.asyncio
    async def test_calcular_fgts_success(self, ai_service, mock_supabase_client):
        """Test FGTS calculation with dynamic parameter"""
        # Arrange - Mock the parameter lookup
        ai_service._obter_parametro = AsyncMock(return_value="8.0")

        # Act
        resultado = await ai_service.calcular_fgts(3000.0, date(2024, 1, 15))

        # Assert
        assert resultado == 240.0  # 3000 * 0.08
        ai_service._obter_parametro.assert_called_once_with(
            "aliquota_fgts_geral", date(2024, 1, 15)
        )

    @pytest.mark.asyncio
    async def test_calcular_fgts_parameter_not_found(
        self, ai_service, mock_supabase_client
    ):
        """Test FGTS calculation when parameter is not found"""
        # Arrange
        ai_service._obter_parametro = AsyncMock(
            side_effect=ValueError("Parâmetro não encontrado")
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await ai_service.calcular_fgts(3000.0, date(2024, 1, 15))

        assert exc_info.value.status_code == 422
        assert "Erro no cálculo do FGTS" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_calcular_inss_success(self, ai_service, mock_supabase_client):
        """Test INSS calculation with dynamic parameter"""

        # Arrange - Mock parameter lookups
        async def mock_obter_parametro(nome_param, data):
            if nome_param == "aliquota_inss_padrao":
                return "11.0"
            elif nome_param == "teto_inss":
                return "7087.22"
            raise ValueError("Parâmetro não encontrado")

        ai_service._obter_parametro = AsyncMock(side_effect=mock_obter_parametro)

        # Act
        resultado = await ai_service.calcular_inss(3000.0, date(2024, 1, 15))

        # Assert
        assert resultado["valor_inss"] == 330.0  # 3000 * 0.11
        assert resultado["aliquota_aplicada"] == 11.0
        assert resultado["base_calculo"] == 3000.0

    @pytest.mark.asyncio
    async def test_calcular_inss_with_ceiling(self, ai_service, mock_supabase_client):
        """Test INSS calculation that hits the ceiling"""

        # Arrange - Mock parameter lookups
        async def mock_obter_parametro(nome_param, data):
            if nome_param == "aliquota_inss_padrao":
                return "11.0"
            elif nome_param == "teto_inss":
                return "500.0"  # Low ceiling to test limit
            raise ValueError("Parâmetro não encontrado")

        ai_service._obter_parametro = AsyncMock(side_effect=mock_obter_parametro)

        # Act
        resultado = await ai_service.calcular_inss(10000.0, date(2024, 1, 15))

        # Assert - Should be limited by ceiling
        assert resultado["valor_inss"] == 500.0  # Ceiling applied
        assert resultado["base_calculo"] == 10000.0

    @pytest.mark.asyncio
    async def test_calcular_inss_parameter_not_found(
        self, ai_service, mock_supabase_client
    ):
        """Test INSS calculation when parameter is not found"""
        # Arrange
        ai_service._obter_parametro = AsyncMock(
            side_effect=ValueError("Parâmetro não encontrado")
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await ai_service.calcular_inss(3000.0, date(2024, 1, 15))

        assert exc_info.value.status_code == 422
        assert "Erro no cálculo do INSS" in str(exc_info.value.detail)
