"""
Exemplo prático de uso completo do sistema AUDITORIA360.

Este exemplo demonstra:
- Fluxo completo de um processo de auditoria
- Integração entre diferentes módulos
- Casos de uso reais
- Best practices de implementação

Requer: requests, pandas, python-dotenv
"""

import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class AuditoriaFlowManager:
    """Gerenciador de fluxo completo de auditoria."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.session_data = {}
        self.headers = {"Content-Type": "application/json"}
    
    def authenticate(self, email: str, password: str) -> bool:
        """
        Autentica usuário no sistema.
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            bool: True se autenticação foi bem-sucedida
        """
        url = f"{self.base_url}/api/v1/auth/login"
        data = {"email": email, "password": password}
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            login_data = response.json()
            self.token = login_data.get("access_token")
            
            if self.token:
                self.headers["Authorization"] = f"Bearer {self.token}"
                print(f"✅ Autenticado como: {email}")
                return True
            
            return False
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na autenticação: {e}")
            return False
    
    def start_audit_process(self, audit_config: Dict) -> Optional[str]:
        """
        Inicia processo de auditoria.
        
        Args:
            audit_config: Configuração da auditoria
            
        Returns:
            str: ID do processo de auditoria
        """
        url = f"{self.base_url}/api/v1/audit/start"
        
        try:
            response = requests.post(url, json=audit_config, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            audit_id = result.get("audit_id")
            
            print(f"🔍 Auditoria iniciada: {audit_id}")
            print(f"Tipo: {audit_config.get('audit_type', 'N/A')}")
            print(f"Escopo: {audit_config.get('scope', 'N/A')}")
            
            return audit_id
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao iniciar auditoria: {e}")
            return None
    
    def upload_documents_for_audit(self, audit_id: str, documents: List[Dict]) -> List[str]:
        """
        Faz upload de documentos para auditoria.
        
        Args:
            audit_id: ID da auditoria
            documents: Lista de documentos para upload
            
        Returns:
            list: IDs dos documentos enviados
        """
        uploaded_docs = []
        
        for doc in documents:
            url = f"{self.base_url}/api/v1/documents/upload"
            
            # Simular upload de documento
            doc_data = {
                "title": doc["title"],
                "category": doc["category"],
                "audit_id": audit_id,
                "process_ocr": True
            }
            
            try:
                # Em um cenário real, enviaria o arquivo
                response = requests.post(url, json=doc_data, headers=self.headers)
                response.raise_for_status()
                
                result = response.json()
                doc_id = result.get("id")
                uploaded_docs.append(doc_id)
                
                print(f"📄 Documento enviado: {doc['title']} (ID: {doc_id})")
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Erro no upload de {doc['title']}: {e}")
        
        return uploaded_docs
    
    def run_compliance_checks(self, audit_id: str) -> Dict:
        """
        Executa verificações de compliance.
        
        Args:
            audit_id: ID da auditoria
            
        Returns:
            dict: Resultado das verificações
        """
        url = f"{self.base_url}/api/v1/compliance/check"
        
        check_config = {
            "audit_id": audit_id,
            "check_types": [
                "payroll_consistency",
                "tax_compliance",
                "labor_law_compliance",
                "document_completeness",
                "calculation_accuracy"
            ],
            "severity_level": "high"
        }
        
        try:
            response = requests.post(url, json=check_config, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            
            print(f"⚖️ Verificações de compliance executadas:")
            print(f"Total de verificações: {result.get('total_checks', 0)}")
            print(f"Aprovadas: {result.get('passed_checks', 0)}")
            print(f"Reprovadas: {result.get('failed_checks', 0)}")
            print(f"Avisos: {result.get('warnings', 0)}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro nas verificações: {e}")
            return {}
    
    def generate_audit_findings(self, audit_id: str) -> List[Dict]:
        """
        Gera achados de auditoria.
        
        Args:
            audit_id: ID da auditoria
            
        Returns:
            list: Lista de achados
        """
        url = f"{self.base_url}/api/v1/audit/{audit_id}/findings"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            findings = response.json()
            
            print(f"🔍 Achados de auditoria gerados:")
            
            # Categorizar achados por severidade
            by_severity = {}
            for finding in findings:
                severity = finding.get("severity", "unknown")
                if severity not in by_severity:
                    by_severity[severity] = []
                by_severity[severity].append(finding)
            
            for severity, items in by_severity.items():
                print(f"- {severity.upper()}: {len(items)} achados")
            
            # Mostrar alguns achados principais
            critical_findings = [f for f in findings if f.get("severity") == "critical"]
            if critical_findings:
                print(f"\n🚨 Achados críticos:")
                for finding in critical_findings[:3]:
                    print(f"- {finding.get('description', 'N/A')}")
            
            return findings
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao gerar achados: {e}")
            return []
    
    def create_corrective_actions(self, findings: List[Dict]) -> List[Dict]:
        """
        Cria planos de ação corretiva.
        
        Args:
            findings: Lista de achados
            
        Returns:
            list: Lista de ações corretivas
        """
        url = f"{self.base_url}/api/v1/audit/corrective-actions"
        
        # Criar ações para achados críticos e altos
        critical_findings = [
            f for f in findings 
            if f.get("severity") in ["critical", "high"]
        ]
        
        actions = []
        
        for finding in critical_findings:
            action_data = {
                "finding_id": finding.get("id"),
                "action_type": "corrective",
                "priority": "high" if finding.get("severity") == "critical" else "medium",
                "responsible_party": "RH",
                "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
                "description": f"Corrigir: {finding.get('description', 'N/A')}"
            }
            
            try:
                response = requests.post(url, json=action_data, headers=self.headers)
                response.raise_for_status()
                
                result = response.json()
                actions.append(result)
                
                print(f"📋 Ação criada: {result.get('id')} - {action_data['description'][:50]}...")
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Erro ao criar ação: {e}")
        
        return actions
    
    def generate_final_report(self, audit_id: str) -> Dict:
        """
        Gera relatório final de auditoria.
        
        Args:
            audit_id: ID da auditoria
            
        Returns:
            dict: Dados do relatório final
        """
        url = f"{self.base_url}/api/v1/audit/{audit_id}/report"
        
        report_config = {
            "format": "pdf",
            "include_sections": [
                "executive_summary",
                "methodology",
                "findings",
                "recommendations",
                "corrective_actions",
                "appendices"
            ],
            "detail_level": "comprehensive"
        }
        
        try:
            response = requests.post(url, json=report_config, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            
            print(f"📊 Relatório final gerado:")
            print(f"- ID: {result.get('report_id')}")
            print(f"- Formato: {report_config['format'].upper()}")
            print(f"- Páginas: {result.get('total_pages', 'N/A')}")
            print(f"- URL: {result.get('download_url', 'N/A')}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao gerar relatório: {e}")
            return {}


def example_complete_payroll_audit():
    """Exemplo de auditoria completa de folha de pagamento."""
    print("\n💼 === AUDITORIA COMPLETA DE FOLHA DE PAGAMENTO ===")
    
    # Inicializar sistema
    audit_manager = AuditoriaFlowManager()
    
    # 1. Autenticação
    if not audit_manager.authenticate("auditor@auditoria360.com", "auditor123"):
        print("❌ Falha na autenticação")
        return
    
    # 2. Configurar auditoria
    audit_config = {
        "audit_type": "payroll_compliance",
        "scope": "full_organization",
        "period": {
            "start_date": "2024-01-01",
            "end_date": "2024-03-31"
        },
        "departments": ["all"],
        "risk_level": "medium",
        "compliance_standards": ["CLT", "LGPD", "SOX"]
    }
    
    # 3. Iniciar auditoria
    audit_id = audit_manager.start_audit_process(audit_config)
    if not audit_id:
        print("❌ Falha ao iniciar auditoria")
        return
    
    # 4. Upload de documentos
    documents = [
        {"title": "Folha de Pagamento Janeiro 2024", "category": "payroll"},
        {"title": "Folha de Pagamento Fevereiro 2024", "category": "payroll"},
        {"title": "Folha de Pagamento Março 2024", "category": "payroll"},
        {"title": "Contratos de Trabalho", "category": "contracts"},
        {"title": "Demonstrativo INSS", "category": "tax_documents"},
        {"title": "DIRF 2024", "category": "tax_documents"}
    ]
    
    uploaded_doc_ids = audit_manager.upload_documents_for_audit(audit_id, documents)
    
    # 5. Executar verificações de compliance
    compliance_results = audit_manager.run_compliance_checks(audit_id)
    
    # 6. Gerar achados
    findings = audit_manager.generate_audit_findings(audit_id)
    
    # 7. Criar ações corretivas
    corrective_actions = audit_manager.create_corrective_actions(findings)
    
    # 8. Gerar relatório final
    final_report = audit_manager.generate_final_report(audit_id)
    
    print(f"\n✅ Auditoria completa finalizada!")
    print(f"Documentos processados: {len(uploaded_doc_ids)}")
    print(f"Achados identificados: {len(findings)}")
    print(f"Ações corretivas: {len(corrective_actions)}")


def example_cct_compliance_check():
    """Exemplo de verificação de compliance com CCT."""
    print("\n📋 === VERIFICAÇÃO DE COMPLIANCE COM CCT ===")
    
    audit_manager = AuditoriaFlowManager()
    
    # Autenticar
    audit_manager.authenticate("compliance@auditoria360.com", "compliance123")
    
    # Configurar verificação específica de CCT
    cct_audit_config = {
        "audit_type": "cct_compliance",
        "scope": "technology_sector",
        "cct_reference": "CCT Sindicato Tecnologia 2024-2025",
        "focus_areas": [
            "salary_adjustments",
            "benefits_compliance",
            "working_hours",
            "overtime_calculation",
            "health_safety"
        ]
    }
    
    audit_id = audit_manager.start_audit_process(cct_audit_config)
    
    if audit_id:
        # Upload documentos específicos de CCT
        cct_documents = [
            {"title": "CCT Vigente 2024-2025", "category": "cct"},
            {"title": "Acordos Sindicais", "category": "agreements"},
            {"title": "Relatórios de Implementação", "category": "implementation"}
        ]
        
        audit_manager.upload_documents_for_audit(audit_id, cct_documents)
        
        # Verificações específicas de CCT
        url = f"{audit_manager.base_url}/api/v1/cct/compliance-check"
        cct_check_data = {
            "audit_id": audit_id,
            "cct_clauses": [
                "salary_adjustment_clause_15",
                "meal_allowance_clause_22",
                "health_plan_clause_31"
            ]
        }
        
        try:
            response = requests.post(url, json=cct_check_data, headers=audit_manager.headers)
            response.raise_for_status()
            
            result = response.json()
            
            print(f"📊 Verificação CCT concluída:")
            print(f"Cláusulas verificadas: {len(result.get('clause_results', []))}")
            print(f"Conformidade geral: {result.get('overall_compliance', 0):.1f}%")
            
            # Mostrar resultados por cláusula
            for clause_result in result.get('clause_results', []):
                status = "✅" if clause_result.get('compliant') else "❌"
                print(f"{status} {clause_result.get('clause_name', 'N/A')}: {clause_result.get('status', 'N/A')}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na verificação CCT: {e}")


def example_realtime_monitoring():
    """Exemplo de monitoramento em tempo real."""
    print("\n📊 === MONITORAMENTO EM TEMPO REAL ===")
    
    audit_manager = AuditoriaFlowManager()
    audit_manager.authenticate("monitor@auditoria360.com", "monitor123")
    
    # Configurar alertas em tempo real
    monitoring_config = {
        "alert_types": [
            "payroll_anomalies",
            "compliance_violations",
            "calculation_errors",
            "document_inconsistencies"
        ],
        "notification_channels": ["email", "webhook"],
        "severity_threshold": "medium"
    }
    
    url = f"{audit_manager.base_url}/api/v1/monitoring/configure"
    
    try:
        response = requests.post(url, json=monitoring_config, headers=audit_manager.headers)
        response.raise_for_status()
        
        print("🔔 Monitoramento configurado com sucesso")
        
        # Simular verificação de alertas
        alerts_url = f"{audit_manager.base_url}/api/v1/monitoring/alerts"
        
        for i in range(3):
            print(f"\n🔍 Verificando alertas... ({i+1}/3)")
            
            response = requests.get(alerts_url, headers=audit_manager.headers)
            response.raise_for_status()
            
            alerts = response.json()
            
            if alerts:
                print(f"🚨 {len(alerts)} alertas encontrados:")
                for alert in alerts[:2]:
                    severity = alert.get('severity', 'unknown').upper()
                    print(f"- [{severity}] {alert.get('message', 'N/A')}")
            else:
                print("✅ Nenhum alerta pendente")
            
            time.sleep(2)  # Aguardar antes da próxima verificação
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro no monitoramento: {e}")


def example_integration_workflow():
    """Exemplo de workflow integrado entre módulos."""
    print("\n🔗 === WORKFLOW INTEGRADO ===")
    
    audit_manager = AuditoriaFlowManager()
    audit_manager.authenticate("integration@auditoria360.com", "integration123")
    
    # 1. Criar funcionário via API
    employee_data = {
        "name": "João Integration Test",
        "cpf": "987.654.321-00",
        "department": "TI",
        "salary": 5000.00
    }
    
    emp_url = f"{audit_manager.base_url}/api/v1/payroll/employees"
    try:
        response = requests.post(emp_url, json=employee_data, headers=audit_manager.headers)
        response.raise_for_status()
        employee = response.json()
        employee_id = employee.get("id")
        
        print(f"👤 Funcionário criado: {employee_id}")
        
        # 2. Calcular folha para o funcionário
        payroll_data = {
            "competency": "2024-04",
            "employees": [{"employee_id": employee_id, "salary": 5000.00}]
        }
        
        calc_url = f"{audit_manager.base_url}/api/v1/payroll/calculate"
        response = requests.post(calc_url, json=payroll_data, headers=audit_manager.headers)
        response.raise_for_status()
        calculation = response.json()
        
        print(f"💰 Folha calculada: ID {calculation.get('calculation_id')}")
        
        # 3. Gerar documento de holerite
        doc_data = {
            "calculation_id": calculation.get("calculation_id"),
            "document_type": "payslip",
            "format": "pdf"
        }
        
        doc_url = f"{audit_manager.base_url}/api/v1/documents/generate"
        response = requests.post(doc_url, json=doc_data, headers=audit_manager.headers)
        response.raise_for_status()
        document = response.json()
        
        print(f"📄 Holerite gerado: {document.get('document_id')}")
        
        # 4. Executar auditoria automática
        auto_audit_config = {
            "audit_type": "automated_check",
            "target_employee": employee_id,
            "check_calculation": True
        }
        
        audit_id = audit_manager.start_audit_process(auto_audit_config)
        
        if audit_id:
            print(f"🔍 Auditoria automática iniciada: {audit_id}")
            
            # 5. Verificar resultado
            time.sleep(2)  # Simular processamento
            findings = audit_manager.generate_audit_findings(audit_id)
            
            if not findings:
                print("✅ Nenhum problema encontrado - processo está conforme!")
            else:
                print(f"⚠️ {len(findings)} achados identificados para correção")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro no workflow integrado: {e}")


def main():
    """Função principal com todos os exemplos."""
    print("🔄 EXEMPLOS DE WORKFLOW COMPLETO - AUDITORIA360")
    print("=" * 55)
    
    try:
        example_complete_payroll_audit()
        example_cct_compliance_check()
        example_realtime_monitoring()
        example_integration_workflow()
        
        print("\n✅ Todos os workflows executados com sucesso!")
        print("\n📚 Para mais informações, consulte:")
        print("- Documentação completa: docs/00-INDICE_PRINCIPAL.md")
        print("- Guia de workflows: docs/tecnico/workflow-guide.md")
        print("- APIs disponíveis: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        print("Verifique se todos os serviços estão rodando")


if __name__ == "__main__":
    main()