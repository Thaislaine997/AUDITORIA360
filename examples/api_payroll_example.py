"""
Exemplo prático de uso da API de Folha de Pagamento do AUDITORIA360.

Este exemplo demonstra:
- Gestão de funcionários
- Cálculo de folha de pagamento
- Geração de relatórios
- Importação de dados
- Validação de folha

Requer: requests, pandas, python-dotenv
"""

import json
import pandas as pd
import requests
from datetime import datetime
from typing import Dict, List, Optional


class PayrollAPI:
    """Cliente para interagir com a API de Folha de Pagamento."""
    
    def __init__(self, base_url: str = "http://localhost:8000", token: str = None):
        self.base_url = base_url
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}" if token else ""
        }
    
    def create_employee(self, employee_data: Dict) -> Dict:
        """
        Cria um novo funcionário.
        
        Args:
            employee_data: Dados do funcionário
            
        Returns:
            dict: Dados do funcionário criado
        """
        url = f"{self.base_url}/api/v1/payroll/employees"
        
        try:
            response = requests.post(url, json=employee_data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Funcionário criado: {employee_data.get('name', 'N/A')}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao criar funcionário: {e}")
            return {"error": str(e)}
    
    def list_employees(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """
        Lista funcionários.
        
        Args:
            skip: Número de registros para pular
            limit: Limite de registros
            
        Returns:
            list: Lista de funcionários
        """
        url = f"{self.base_url}/api/v1/payroll/employees"
        params = {"skip": skip, "limit": limit}
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            employees = response.json()
            print(f"✅ Funcionários obtidos: {len(employees)} encontrados")
            return employees
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao listar funcionários: {e}")
            return []
    
    def calculate_payroll(self, calculation_data: Dict) -> Dict:
        """
        Calcula folha de pagamento.
        
        Args:
            calculation_data: Dados para cálculo
            
        Returns:
            dict: Resultado do cálculo
        """
        url = f"{self.base_url}/api/v1/payroll/calculate"
        
        try:
            response = requests.post(url, json=calculation_data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Folha calculada para {calculation_data.get('competency', 'N/A')}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao calcular folha: {e}")
            return {"error": str(e)}
    
    def generate_report(self, report_data: Dict) -> Dict:
        """
        Gera relatório de folha de pagamento.
        
        Args:
            report_data: Dados para geração do relatório
            
        Returns:
            dict: Dados do relatório gerado
        """
        url = f"{self.base_url}/api/v1/payroll/reports"
        
        try:
            response = requests.post(url, json=report_data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Relatório gerado: {result.get('report_type', 'N/A')}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao gerar relatório: {e}")
            return {"error": str(e)}
    
    def import_payroll_data(self, file_path: str, import_type: str = "csv") -> Dict:
        """
        Importa dados de folha de pagamento.
        
        Args:
            file_path: Caminho do arquivo
            import_type: Tipo de importação (csv, xlsx)
            
        Returns:
            dict: Resultado da importação
        """
        url = f"{self.base_url}/api/v1/payroll/import"
        
        try:
            with open(file_path, 'rb') as file:
                files = {"file": file}
                data = {"import_type": import_type}
                
                # Remove Content-Type header for file upload
                headers = self.headers.copy()
                del headers["Content-Type"]
                
                response = requests.post(url, files=files, data=data, headers=headers)
                response.raise_for_status()
                
                result = response.json()
                print(f"✅ Dados importados: {result.get('records_processed', 0)} registros")
                return result
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao importar dados: {e}")
            return {"error": str(e)}
        except FileNotFoundError:
            error_msg = f"Arquivo não encontrado: {file_path}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}


def example_employee_management():
    """Exemplo de gestão de funcionários."""
    print("\n👥 === EXEMPLO DE GESTÃO DE FUNCIONÁRIOS ===")
    
    # Simular token (em produção, obter via login)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = PayrollAPI(token=token)
    
    # Criar funcionário
    employee_data = {
        "name": "Maria Silva Santos",
        "cpf": "123.456.789-00",
        "pis": "12345678901",
        "email": "maria.silva@empresa.com",
        "department": "Recursos Humanos",
        "position": "Analista de RH",
        "admission_date": "2024-01-15",
        "salary": 4500.00,
        "status": "active",
        "address": {
            "street": "Rua das Flores, 123",
            "city": "São Paulo",
            "state": "SP",
            "zip_code": "01234-567"
        },
        "bank_info": {
            "bank_code": "001",
            "agency": "1234",
            "account": "12345-6",
            "account_type": "checking"
        }
    }
    
    result = api.create_employee(employee_data)
    
    if "id" in result:
        print(f"ID do funcionário: {result['id']}")
        print(f"Data de admissão: {result['admission_date']}")
        print(f"Salário: R$ {result['salary']:,.2f}")
    
    # Listar funcionários
    employees = api.list_employees(limit=5)
    
    if employees:
        print(f"\nPrimeiros funcionários cadastrados:")
        for emp in employees:
            print(f"- {emp.get('name', 'N/A')} ({emp.get('department', 'N/A')})")


def example_payroll_calculation():
    """Exemplo de cálculo de folha de pagamento."""
    print("\n💰 === EXEMPLO DE CÁLCULO DE FOLHA ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = PayrollAPI(token=token)
    
    # Dados para cálculo da folha
    calculation_data = {
        "competency": "2024-01",
        "payroll_type": "normal",
        "employees": [
            {
                "employee_id": 1,
                "salary": 4500.00,
                "overtime_hours": 10,
                "overtime_rate": 1.5,
                "allowances": [
                    {"type": "transport", "amount": 200.00},
                    {"type": "meal", "amount": 350.00}
                ],
                "deductions": [
                    {"type": "health_insurance", "amount": 150.00}
                ]
            }
        ],
        "calculation_rules": {
            "inss_ceiling": 7507.49,
            "irrf_deduction": 2112.00,
            "fgts_rate": 0.08
        }
    }
    
    result = api.calculate_payroll(calculation_data)
    
    if "calculation_id" in result:
        print(f"ID do cálculo: {result['calculation_id']}")
        print(f"Competência: {result['competency']}")
        print(f"Total de funcionários: {result.get('employees_count', 0)}")
        print(f"Total bruto: R$ {result.get('total_gross', 0):,.2f}")
        print(f"Total descontos: R$ {result.get('total_deductions', 0):,.2f}")
        print(f"Total líquido: R$ {result.get('total_net', 0):,.2f}")
        
        # Detalhes por funcionário
        if "employee_details" in result:
            print(f"\nDetalhes por funcionário:")
            for detail in result["employee_details"]:
                print(f"- {detail.get('employee_name', 'N/A')}: R$ {detail.get('net_salary', 0):,.2f}")


def example_payroll_reports():
    """Exemplo de geração de relatórios."""
    print("\n📊 === EXEMPLO DE RELATÓRIOS DE FOLHA ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = PayrollAPI(token=token)
    
    # Relatório sintético
    synthetic_report = {
        "report_type": "synthetic",
        "competency": "2024-01",
        "department": "all",
        "format": "pdf",
        "include_graphics": True
    }
    
    result = api.generate_report(synthetic_report)
    
    if "report_id" in result:
        print(f"Relatório sintético gerado:")
        print(f"- ID: {result['report_id']}")
        print(f"- URL: {result.get('download_url', 'N/A')}")
        print(f"- Tamanho: {result.get('file_size', 'N/A')} KB")
    
    # Relatório analítico
    analytical_report = {
        "report_type": "analytical",
        "competency": "2024-01",
        "filters": {
            "department": ["RH", "TI"],
            "salary_range": {"min": 3000, "max": 10000}
        },
        "format": "xlsx",
        "breakdown_by": ["department", "position"]
    }
    
    result = api.generate_report(analytical_report)
    
    if "report_id" in result:
        print(f"\nRelatório analítico gerado:")
        print(f"- Departamentos: {len(analytical_report['filters']['department'])}")
        print(f"- Formato: {analytical_report['format'].upper()}")


def example_data_import():
    """Exemplo de importação de dados."""
    print("\n📤 === EXEMPLO DE IMPORTAÇÃO DE DADOS ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = PayrollAPI(token=token)
    
    # Criar arquivo CSV de exemplo
    sample_data = pd.DataFrame({
        "name": ["João Silva", "Ana Costa", "Pedro Santos"],
        "cpf": ["111.111.111-11", "222.222.222-22", "333.333.333-33"],
        "salary": [3500, 4200, 5800],
        "department": ["TI", "RH", "Financeiro"],
        "admission_date": ["2024-01-10", "2024-02-15", "2024-03-20"]
    })
    
    csv_file = "/tmp/funcionarios_exemplo.csv"
    sample_data.to_csv(csv_file, index=False)
    
    print(f"Arquivo criado: {csv_file}")
    print(f"Registros: {len(sample_data)}")
    
    # Importar dados
    result = api.import_payroll_data(csv_file, "csv")
    
    if "records_processed" in result:
        print(f"✅ Importação concluída:")
        print(f"- Registros processados: {result['records_processed']}")
        print(f"- Registros válidos: {result.get('valid_records', 0)}")
        print(f"- Registros com erro: {result.get('error_records', 0)}")
        
        if result.get("errors"):
            print(f"Erros encontrados:")
            for error in result["errors"][:3]:  # Mostrar apenas os primeiros 3
                print(f"- Linha {error.get('line', 'N/A')}: {error.get('message', 'N/A')}")


def create_payroll_validation_example():
    """Exemplo de validação de folha de pagamento."""
    print("\n✅ === EXEMPLO DE VALIDAÇÃO DE FOLHA ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = PayrollAPI(token=token)
    
    # Dados para validação
    validation_data = {
        "competency": "2024-01",
        "validation_rules": [
            "salary_consistency",
            "tax_calculation",
            "mandatory_fields",
            "duplicate_employees",
            "benefit_limits"
        ],
        "severity_level": "warning"
    }
    
    url = f"{api.base_url}/api/v1/payroll/validate"
    
    try:
        response = requests.post(url, json=validation_data, headers=api.headers)
        response.raise_for_status()
        
        result = response.json()
        
        print(f"Validação concluída:")
        print(f"- Total de registros: {result.get('total_records', 0)}")
        print(f"- Registros válidos: {result.get('valid_records', 0)}")
        print(f"- Avisos: {result.get('warnings', 0)}")
        print(f"- Erros: {result.get('errors', 0)}")
        
        if result.get("validation_details"):
            print(f"\nDetalhes da validação:")
            for detail in result["validation_details"][:5]:
                severity = detail.get("severity", "info").upper()
                print(f"- [{severity}] {detail.get('message', 'N/A')}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na validação: {e}")


def main():
    """Função principal com todos os exemplos."""
    print("💼 EXEMPLOS DE USO - API DE FOLHA DE PAGAMENTO AUDITORIA360")
    print("=" * 70)
    
    try:
        example_employee_management()
        example_payroll_calculation()
        example_payroll_reports()
        example_data_import()
        create_payroll_validation_example()
        
        print("\n✅ Todos os exemplos executados com sucesso!")
        print("\n📚 Para mais informações, consulte:")
        print("- Documentação da API: http://localhost:8000/docs")
        print("- Manual de folha: docs/usuario/manual-folha-pagamento.md")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        print("Verifique se a API está rodando e o token é válido")


if __name__ == "__main__":
    main()