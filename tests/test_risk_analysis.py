#!/usr/bin/env python3
"""
Test script for the Risk Analysis API endpoint
Tests the core functionality of the Consultor de Riscos
"""

import asyncio
import json
import sys
from datetime import datetime

# Add portal_demandas to path
sys.path.append('.')

from portal_demandas.api import app
from portal_demandas.db import get_db, EmpresaDB, ContabilidadeDB
from portal_demandas.models import AnaliseRiscoRequest
from fastapi.testclient import TestClient

def test_risk_analysis_endpoint():
    """Test the risk analysis API endpoint"""
    
    print("🧪 Testing Risk Analysis API Endpoint")
    print("=" * 50)
    
    # Create test client
    client = TestClient(app)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    health_response = client.get("/health")
    print(f"   Health status: {health_response.status_code}")
    if health_response.status_code == 200:
        print(f"   ✅ {health_response.json()['status']}")
    
    # Test 2: Create test data (if needed)
    print("\n2. Setting up test data...")
    try:
        db = next(get_db())
        
        # Check if test company exists, create if not
        test_company = db.query(EmpresaDB).filter(EmpresaDB.id == 1).first()
        if not test_company:
            # Create test accounting firm first
            contabilidade = ContabilidadeDB(
                nome_contabilidade="Teste Contabilidade Ltda",
                cnpj="12.345.678/0001-90"
            )
            db.add(contabilidade)
            db.commit()
            db.refresh(contabilidade)
            
            # Create test company
            empresa = EmpresaDB(
                nome="Empresa Teste de Riscos S/A",
                contabilidade_id=contabilidade.id
            )
            db.add(empresa)
            db.commit()
            db.refresh(empresa)
            print(f"   ✅ Created test company: {empresa.nome} (ID: {empresa.id})")
        else:
            print(f"   ✅ Using existing test company: {test_company.nome} (ID: {test_company.id})")
        
        db.close()
    except Exception as e:
        print(f"   ⚠️  Error setting up test data: {e}")
    
    # Test 3: Risk analysis endpoint
    print("\n3. Testing risk analysis endpoint...")
    
    analysis_request = {
        "empresa_id": 1
    }
    
    response = client.post("/v1/riscos/analisar", json=analysis_request)
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Risk Analysis Completed Successfully!")
        print(f"   📊 Company: {result['empresa_nome']}")
        print(f"   📊 Risk Score: {result['score_risco']}/100")
        print(f"   📊 Risk Level: {result['nivel_risco']}")
        print(f"   📊 Total Risks Found: {result['total_riscos']}")
        print(f"   📊 Critical Risks: {result['riscos_criticos']}")
        print(f"   📊 High Risks: {result['riscos_altos']}")
        print(f"   📊 Medium Risks: {result['riscos_medios']}")
        print(f"   📊 Low Risks: {result['riscos_baixos']}")
        
        # Display found risks
        if result['riscos_encontrados']:
            print(f"\n   📋 Detailed Risk Analysis:")
            for i, risco in enumerate(result['riscos_encontrados'][:3], 1):  # Show first 3 risks
                print(f"      {i}. [{risco['categoria']}] {risco['tipo_risco']}")
                print(f"         Severity: {risco['severidade']}/5")
                print(f"         Description: {risco['descricao'][:100]}...")
        
        print(f"\n   📈 Analysis Progress:")
        for step, status in result['progresso_analise'].items():
            print(f"      - {step}: {status}")
    
    elif response.status_code == 404:
        print(f"   ❌ Company not found - this is expected for the test")
        print(f"   Response: {response.text}")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   Response: {response.text}")
    
    # Test 4: Risk history endpoint
    print("\n4. Testing risk history endpoint...")
    
    history_response = client.get("/v1/riscos/historico/1")
    print(f"   Status Code: {history_response.status_code}")
    
    if history_response.status_code == 200:
        history = history_response.json()
        print(f"   ✅ Retrieved {len(history)} historical analyses")
        if history:
            latest = history[0]
            print(f"   📊 Latest analysis: Score {latest['score_risco']}/100 on {latest['data_analise']}")
    else:
        print(f"   Response: {history_response.text}")
    
    print("\n" + "=" * 50)
    print("🏁 Risk Analysis API Test Complete!")
    
    return response.status_code == 200


if __name__ == "__main__":
    success = test_risk_analysis_endpoint()
    sys.exit(0 if success else 1)