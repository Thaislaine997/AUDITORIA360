#!/usr/bin/env python3
"""
Test script for AUDITORIA360 v1.0 implementation
Tests the core functionality without requiring full dependency installation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that core modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        from portal_demandas.services import document_ai_client, mediador_scraper
        print("✅ Services module imported successfully")
        
        from portal_demandas.db import SindicatoDB, ConvencaoColetivaCCTDB, ProcessamentosFolhaDB
        print("✅ Database models imported successfully")
        
        print("✅ All core modules imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_ai_service():
    """Test the AI service functionality"""
    print("\n🤖 Testing AI service functionality...")
    
    try:
        import asyncio
        from portal_demandas.services import document_ai_client
        
        async def run_ai_test():
            # Test CCT processing
            mock_pdf = b"mock_pdf_content"
            instruction = "Esta é uma CCT. Extraia piso salarial e benefícios."
            result = await document_ai_client.process(mock_pdf, instruction)
            
            assert "piso_salarial" in result
            assert "beneficios" in result
            print(f"✅ AI CCT processing test passed - extracted {len(result)} fields")
            
            # Test payroll processing
            instruction = "Esta é uma folha de pagamento."
            result = await document_ai_client.process(mock_pdf, instruction)
            
            assert "funcionarios" in result
            print(f"✅ AI payroll processing test passed - found {len(result.get('funcionarios', []))} employees")
            
        asyncio.run(run_ai_test())
        return True
        
    except Exception as e:
        print(f"❌ AI service test failed: {e}")
        return False

def test_monitoring_service():
    """Test the monitoring service functionality"""
    print("\n🕷️ Testing monitoring service functionality...")
    
    try:
        import asyncio
        from portal_demandas.services import mediador_scraper
        
        async def run_monitoring_test():
            # Test CCT monitoring
            result = await mediador_scraper.buscar_nova_cct("12.345.678/0001-90")
            
            assert "encontrado" in result
            assert "cnpj_pesquisado" in result
            print(f"✅ Monitoring service test passed - result: {result.get('encontrado', False)}")
            
            # Test legislation monitoring  
            docs = await mediador_scraper.buscar_legislacao_recente(7)
            print(f"✅ Legislation monitoring test passed - found {len(docs)} documents")
            
        asyncio.run(run_monitoring_test())
        return True
        
    except Exception as e:
        print(f"❌ Monitoring service test failed: {e}")
        return False

def test_database_schema():
    """Test database schema creation"""
    print("\n🗄️ Testing database schema...")
    
    try:
        # Check if SQL file exists and is valid
        sql_file = "data_base/migrations/001_create_v1_0_tables.sql"
        if not os.path.exists(sql_file):
            print(f"❌ SQL migration file not found: {sql_file}")
            return False
            
        with open(sql_file, 'r') as f:
            sql_content = f.read()
            
        # Check for required tables
        required_tables = [
            "Sindicatos",
            "ConvencoesColetivas", 
            "ProcessamentosFolha",
            "DocumentosLegislacao"
        ]
        
        for table in required_tables:
            if table not in sql_content:
                print(f"❌ Required table '{table}' not found in SQL")
                return False
                
        print(f"✅ Database schema validation passed - {len(required_tables)} tables defined")
        print(f"📊 SQL migration file: {len(sql_content)} characters")
        return True
        
    except Exception as e:
        print(f"❌ Database schema test failed: {e}")
        return False

def test_frontend_components():
    """Test frontend component existence"""
    print("\n🎨 Testing frontend components...")
    
    try:
        frontend_files = [
            "src/frontend/src/pages/CCTPage.tsx",
            "src/frontend/src/pages/PayrollPage.tsx"
        ]
        
        for file_path in frontend_files:
            if not os.path.exists(file_path):
                print(f"❌ Frontend component not found: {file_path}")
                return False
                
            # Check file has meaningful content
            with open(file_path, 'r') as f:
                content = f.read()
                if len(content) < 1000:
                    print(f"❌ Frontend component too small: {file_path}")
                    return False
                    
        print(f"✅ Frontend components validation passed - {len(frontend_files)} files found")
        return True
        
    except Exception as e:
        print(f"❌ Frontend components test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AUDITORIA360 v1.0 - Implementation Validation Tests")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("AI Service", test_ai_service),
        ("Monitoring Service", test_monitoring_service),
        ("Database Schema", test_database_schema),
        ("Frontend Components", test_frontend_components)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AUDITORIA360 v1.0 implementation is ready.")
        return 0
    else:
        print(f"⚠️ {total - passed} tests failed. Please review the implementation.")
        return 1

if __name__ == "__main__":
    exit(main())