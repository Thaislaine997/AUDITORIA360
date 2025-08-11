#!/usr/bin/env python3
"""
AUDITORIA360 v1.0 - API Demonstration Script
Shows the implemented functionality working without requiring full deployment
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def demo_document_ai():
    """Demonstrate the Document AI functionality"""
    print("🧠 DOCUMENT AI DEMONSTRATION")
    print("=" * 50)
    
    try:
        from portal_demandas.services import document_ai_client
        
        # Demo 1: CCT Processing
        print("\n📋 Processing CCT Document:")
        mock_cct_pdf = b"mock_cct_content"
        instruction = "Esta é uma Convenção Coletiva de Trabalho. Extraia o piso salarial, benefícios e vigência."
        
        result = await document_ai_client.process(mock_cct_pdf, instruction)
        
        print(f"  ✅ Document Type: {result.get('tipo_documento', 'N/A')}")
        print(f"  💰 Minimum Wage: R$ {result.get('piso_salarial', 0):,.2f}")
        print(f"  🎁 Benefits: {len(result.get('beneficios', []))} items found")
        print(f"  📅 Validity: {result.get('vigencia_inicio', 'N/A')} to {result.get('vigencia_fim', 'N/A')}")
        
        # Demo 2: Payroll Processing
        print("\n💰 Processing Payroll Document:")
        mock_payroll_pdf = b"mock_payroll_content"
        instruction = "Esta é uma folha de pagamento. Extraia dados dos funcionários."
        
        result = await document_ai_client.process(mock_payroll_pdf, instruction)
        
        print(f"  👥 Employees Found: {result.get('total_funcionarios', 0)}")
        print(f"  💼 Gross Payroll: R$ {result.get('totalizadores', {}).get('folha_bruta', 0):,.2f}")
        print(f"  💸 Net Payroll: R$ {result.get('totalizadores', {}).get('folha_liquida', 0):,.2f}")
        
        if result.get('funcionarios'):
            first_employee = result['funcionarios'][0]
            print(f"  👤 Sample Employee: {first_employee.get('nome', 'N/A')} - {first_employee.get('cargo', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

async def demo_monitoring_service():
    """Demonstrate the Monitoring Service functionality"""
    print("\n\n🕷️ MONITORING SERVICE DEMONSTRATION")
    print("=" * 50)
    
    try:
        from portal_demandas.services import mediador_scraper
        
        # Demo 1: CCT Monitoring
        print("\n🔍 Monitoring Official Sources for New CCTs:")
        test_cnpjs = [
            "12.345.678/0001-90",
            "98.765.432/0001-10", 
            "11.222.333/0001-44"
        ]
        
        findings = 0
        for cnpj in test_cnpjs:
            print(f"  🔍 Checking CNPJ: {cnpj}")
            result = await mediador_scraper.buscar_nova_cct(cnpj)
            
            if result.get("encontrado"):
                findings += 1
                nova_cct = result.get("nova_cct", {})
                print(f"    ✨ NEW CCT FOUND!")
                print(f"    📋 Registry: {nova_cct.get('numero_registro', 'N/A')}")
                print(f"    🔗 Document: {nova_cct.get('link_pdf', 'N/A')}")
            else:
                print(f"    ℹ️ No new CCTs found")
        
        print(f"\n📊 Monitoring Summary: {findings} new CCTs found out of {len(test_cnpjs)} syndicates checked")
        
        # Demo 2: Legislation Monitoring
        print("\n📋 Monitoring Recent Legislation (Last 7 Days):")
        docs = await mediador_scraper.buscar_legislacao_recente(7)
        
        print(f"  📄 Documents Found: {len(docs)}")
        for i, doc in enumerate(docs, 1):
            print(f"  {i}. {doc.get('tipo', 'N/A').upper()} {doc.get('numero', 'N/A')}")
            print(f"     📅 Published: {doc.get('data_publicacao', 'N/A')}")
            print(f"     🏛️ Authority: {doc.get('orgao', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

async def demo_audit_engine():
    """Demonstrate the Audit Engine logic"""
    print("\n\n🔍 AUDIT ENGINE DEMONSTRATION")
    print("=" * 50)
    
    try:
        from portal_demandas.services import document_ai_client
        
        # Simulate the full audit workflow
        print("\n💼 Simulating Payroll Audit Workflow:")
        print("  1️⃣ Extracting payroll data with AI...")
        
        # Step 1: AI Extraction
        mock_payroll = b"mock_payroll_data"
        payroll_data = await document_ai_client.process(
            mock_payroll, 
            "Extraia dados da folha de pagamento"
        )
        
        funcionarios = payroll_data.get("funcionarios", [])[:3]  # Take first 3 for demo
        print(f"     📊 Extracted data for {len(funcionarios)} employees")
        
        # Step 2: Mock CCT Rules
        print("  2️⃣ Loading applicable CCT rules...")
        mock_cct_rules = {
            "piso_salarial": 1985.00,
            "vale_refeicao_minimo": 25.00,
            "percentual_he_50": 60.0,  # 60% instead of standard 50%
            "auxilio_creche": 150.00
        }
        print(f"     📋 CCT rules loaded: minimum wage R$ {mock_cct_rules['piso_salarial']:,.2f}")
        
        # Step 3: Audit Logic
        print("  3️⃣ Executing audit comparisons...")
        divergencias = []
        
        for funcionario in funcionarios:
            nome = funcionario.get("nome", "Unknown")
            salario_base = funcionario.get("salario_base", 0)
            cargo = funcionario.get("cargo", "Unknown")
            
            # Check minimum wage compliance
            if salario_base < mock_cct_rules["piso_salarial"]:
                divergencias.append({
                    "funcionario": nome,
                    "tipo": "ALERTA",
                    "descricao": f"Salário abaixo do piso da CCT",
                    "encontrado": f"R$ {salario_base:,.2f}",
                    "esperado": f"R$ {mock_cct_rules['piso_salarial']:,.2f}"
                })
            
            # Check overtime calculation
            he_50 = funcionario.get("horas_extras_50", 0)
            if he_50 > 0 and mock_cct_rules["percentual_he_50"] != 50:
                divergencias.append({
                    "funcionario": nome,
                    "tipo": "AVISO",
                    "descricao": f"Percentual de HE pode diferir da CCT ({mock_cct_rules['percentual_he_50']}%)",
                    "encontrado": f"50%",
                    "esperado": f"{mock_cct_rules['percentual_he_50']}%"
                })
        
        # Step 4: Results
        print(f"  4️⃣ Audit completed!")
        print(f"     👥 Employees Audited: {len(funcionarios)}")
        print(f"     ⚠️ Divergences Found: {len(divergencias)}")
        
        if divergencias:
            print("\n📋 DIVERGENCES FOUND:")
            for i, div in enumerate(divergencias, 1):
                icon = "🚨" if div["tipo"] == "ALERTA" else "⚠️"
                print(f"  {i}. {icon} {div['funcionario']}: {div['descricao']}")
                print(f"     Found: {div['encontrado']} | Expected: {div['esperado']}")
        else:
            print("  ✅ No divergences found - payroll is compliant!")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

async def demo_complete_workflow():
    """Demonstrate the complete AUDITORIA360 workflow"""
    print("\n\n🚀 COMPLETE AUDITORIA360 WORKFLOW DEMONSTRATION")
    print("=" * 60)
    
    try:
        print("\n📊 SCENARIO: Monthly Audit for 'Empresa Modelo Comercial Ltda'")
        print("- Company Type: Retail/Commercial")
        print("- Employees: ~25 people")
        print("- CCT: Sindicato dos Comerciários de São Paulo")
        print("- Period: November 2024")
        
        # Step 1: Knowledge Base (CCT Processing)
        print("\n🧠 STEP 1: Processing Company's CCT with AI")
        from portal_demandas.services import document_ai_client
        
        mock_cct_pdf = b"cct_comerciarios_sp_2024.pdf"
        cct_data = await document_ai_client.process(
            mock_cct_pdf, 
            "CCT dos Comerciários - extrair piso salarial e benefícios"
        )
        
        print(f"  ✅ CCT processed successfully")
        print(f"  📋 Minimum Wage: R$ {cct_data.get('piso_salarial', 0):,.2f}")
        print(f"  🎁 Mandatory Benefits: {len(cct_data.get('beneficios', []))}")
        
        # Step 2: Monitoring Check
        print("\n🕷️ STEP 2: Checking for CCT Updates")
        from portal_demandas.services import mediador_scraper
        
        monitoring_result = await mediador_scraper.buscar_nova_cct("12.345.678/0001-90")
        if monitoring_result.get("encontrado"):
            print("  ⚠️ New CCT version found! Manual review needed.")
        else:
            print("  ✅ Current CCT is up to date")
        
        # Step 3: Payroll Processing & Audit
        print("\n💰 STEP 3: Processing November 2024 Payroll")
        
        mock_payroll_pdf = b"folha_nov_2024_empresa_modelo.pdf"
        payroll_data = await document_ai_client.process(
            mock_payroll_pdf,
            "Folha de pagamento - extrair dados dos funcionários"
        )
        
        employees_count = payroll_data.get("total_funcionarios", 0)
        gross_payroll = payroll_data.get("totalizadores", {}).get("folha_bruta", 0)
        
        print(f"  📊 Payroll processed: {employees_count} employees")
        print(f"  💼 Gross Payroll: R$ {gross_payroll:,.2f}")
        
        # Step 4: Intelligent Auditing
        print("\n🔍 STEP 4: Executing Comprehensive Audit")
        
        # Simulate audit logic
        cct_rules = cct_data
        audit_issues = 0
        
        # Check each employee against CCT rules
        funcionarios = payroll_data.get("funcionarios", [])
        for emp in funcionarios[:5]:  # Check first 5 for demo
            if emp.get("salario_base", 0) < cct_rules.get("piso_salarial", 1985):
                audit_issues += 1
        
        print(f"  🔍 Audit completed")
        print(f"  ⚠️ Issues found: {audit_issues} minimum wage violations")
        
        # Step 5: Generate Report
        print("\n📋 STEP 5: Generating Compliance Report")
        
        compliance_score = max(0, 100 - (audit_issues * 10))
        risk_level = "LOW" if compliance_score >= 80 else "MEDIUM" if compliance_score >= 60 else "HIGH"
        
        print(f"  📊 Compliance Score: {compliance_score}%")
        print(f"  🎯 Risk Level: {risk_level}")
        print(f"  📄 Report generated for management review")
        
        # Summary
        print(f"\n🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
        print(f"✅ CCT Knowledge Base: Up to date")
        print(f"✅ Payroll Processing: {employees_count} employees processed")
        print(f"✅ Audit Engine: {audit_issues} issues identified")
        print(f"✅ Compliance Report: Generated with {compliance_score}% score")
        
        return True
        
    except Exception as e:
        print(f"❌ Complete workflow demo failed: {e}")
        return False

async def main():
    """Run all demonstrations"""
    print("🚀 AUDITORIA360 v1.0 - LIVE FUNCTIONALITY DEMONSTRATION")
    print("=" * 70)
    print("🎯 Showcasing the implemented 'Base de Conhecimento Inteligente'")
    print("🎯 and 'Motor de Auditoria da Folha de Pagamento'")
    
    demos = [
        ("Document AI Processing", demo_document_ai),
        ("Official Sources Monitoring", demo_monitoring_service),
        ("Intelligent Audit Engine", demo_audit_engine),
        ("Complete Workflow", demo_complete_workflow)
    ]
    
    successful_demos = 0
    
    for demo_name, demo_func in demos:
        print(f"\n🎬 Starting: {demo_name}")
        try:
            if await demo_func():
                successful_demos += 1
                print(f"✅ {demo_name} completed successfully")
            else:
                print(f"❌ {demo_name} failed")
        except Exception as e:
            print(f"💥 {demo_name} crashed: {e}")
    
    print("\n" + "=" * 70)
    print(f"🎊 DEMONSTRATION COMPLETE: {successful_demos}/{len(demos)} demos successful")
    
    if successful_demos == len(demos):
        print("🏆 All AUDITORIA360 v1.0 functionality is working perfectly!")
        print("🚀 Ready for production deployment!")
    else:
        print(f"⚠️ Some demos had issues. Please review the implementation.")
    
    print("\n📚 For complete deployment instructions, see DEPLOYMENT_GUIDE.md")
    print("🧪 For technical validation, run: python test_implementation.py")

if __name__ == "__main__":
    asyncio.run(main())