"""
Demonstration script for AI-powered payroll calculations
Shows how the system now uses dynamic rules from RegrasValidadas instead of hard-coded values
"""

import asyncio
from datetime import date
from unittest.mock import AsyncMock, MagicMock

from src.services.payroll_service import AIPayrollService


async def demo_ai_payroll_calculations():
    """
    Demonstra como o sistema agora utiliza regras dinâmicas da tabela RegrasValidadas
    em vez de valores hard-coded.
    """
    print("🚀 DEMONSTRAÇÃO: IA-INTEGRAÇÃO NO MOTOR DE AUDITORIA")
    print("=" * 60)

    # Create a mock Supabase client (in production, this would be real)
    mock_supabase = AsyncMock()

    # Simulate database responses with current Brazilian tax rates
    def mock_query_response(param_name, date_ref):
        # Simulate different parameters stored in RegrasValidadas table
        mock_data = {
            "aliquota_fgts_geral": "8.0",  # 8%
            "aliquota_inss_padrao": "11.0",  # 11% simplified
            "teto_inss": "7087.22",  # 2024 ceiling
        }
        if param_name in mock_data:
            response = MagicMock()
            response.data = [{"valor_parametro": mock_data[param_name]}]
            return response
        else:
            # Parameter not found
            response = MagicMock()
            response.data = []
            return response

    # Mock the Supabase query chain
    mock_query = AsyncMock()
    mock_query.select = MagicMock(return_value=mock_query)
    mock_query.eq = MagicMock(return_value=mock_query)
    mock_query.lte = MagicMock(return_value=mock_query)
    mock_query.or_ = MagicMock(return_value=mock_query)
    mock_query.order = MagicMock(return_value=mock_query)
    mock_query.limit = MagicMock(return_value=mock_query)

    # Create AI service
    ai_service = AIPayrollService(mock_supabase)
    mock_supabase.from_ = MagicMock(return_value=mock_query)

    # Test scenarios
    test_cases = [
        {
            "name": "FGTS Calculation - Current Rules",
            "salario": 3500.00,
            "data": date(2024, 8, 1),
            "param": "aliquota_fgts_geral"
        },
        {
            "name": "INSS Calculation - Current Rules", 
            "salario": 5000.00,
            "data": date(2024, 8, 1),
            "param": "aliquota_inss_padrao"
        },
        {
            "name": "FGTS Calculation - Historical Date (Error Expected)",
            "salario": 3500.00,
            "data": date(1990, 1, 1),
            "param": "aliquota_fgts_geral"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📊 Teste {i}: {test_case['name']}")
        print("-" * 50)
        
        try:
            if "FGTS" in test_case['name']:
                # Setup mock response
                if test_case['data'].year >= 2024:
                    mock_query.execute = AsyncMock(
                        return_value=mock_query_response(test_case['param'], test_case['data'])
                    )
                else:
                    # Old date - no rules found
                    mock_query.execute = AsyncMock(
                        return_value=mock_query_response("nonexistent", test_case['data'])
                    )
                
                resultado = await ai_service.calcular_fgts(test_case['salario'], test_case['data'])
                print(f"💰 Salário Base: R$ {test_case['salario']:,.2f}")
                print(f"📅 Data Referência: {test_case['data']}")
                print(f"✅ FGTS Calculado: R$ {resultado:,.2f}")
                print(f"📈 Taxa Aplicada: 8% (obtida dinamicamente da RegrasValidadas)")
                
            elif "INSS" in test_case['name']:
                # Setup mock response for INSS
                mock_query.execute = AsyncMock(
                    return_value=mock_query_response(test_case['param'], test_case['data'])
                )
                
                resultado = await ai_service.calcular_inss(test_case['salario'], test_case['data'])
                print(f"💰 Salário Base: R$ {test_case['salario']:,.2f}")
                print(f"📅 Data Referência: {test_case['data']}")
                print(f"✅ INSS Calculado: R$ {resultado['valor_inss']:,.2f}")
                print(f"📈 Alíquota Aplicada: {resultado['aliquota_aplicada']:.1f}% (obtida dinamicamente da RegrasValidadas)")
                print(f"🔒 Base de Cálculo: R$ {resultado['base_calculo']:,.2f}")
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            print("💡 Isto demonstra o tratamento de erro quando parâmetros não são encontrados na RegrasValidadas")

    print(f"\n🎯 RESUMO DA TRANSFORMAÇÃO")
    print("=" * 60)
    print("✅ ANTES: Valores hard-coded no código (ex: TAXA_FGTS = 0.08)")
    print("✅ DEPOIS: Consulta dinâmica à tabela RegrasValidadas")
    print("✅ Sistema agora é 'vivo' e se adapta automaticamente a novas regras")
    print("✅ IA extrai regras → Humano valida → Sistema usa automaticamente")
    print("✅ Auditorias sempre atualizadas com a legislação mais recente")
    
    print(f"\n📚 PRÓXIMOS PASSOS PARA TESTE COMPLETO")
    print("=" * 60) 
    print("1. Configurar as credenciais do Supabase no .env")
    print("2. Popular a tabela RegrasValidadas com parâmetros reais")
    print("3. Testar os endpoints via FastAPI docs (/docs)")
    print("4. Usar POST /payroll/calculate-fgts com data_referencia")
    print("5. Usar POST /payroll/calculate-inss com data_referencia")


if __name__ == "__main__":
    asyncio.run(demo_ai_payroll_calculations())