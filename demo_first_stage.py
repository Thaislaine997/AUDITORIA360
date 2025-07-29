#!/usr/bin/env python3
"""
AUDITORIA360 - First Stage Integration Example (Refatorado)
Demonstrates the unified reporting system with dashboard integration
Uses modularized demonstration utilities for better organization.

This script shows how the first stage components work together:
1. Generate unified reports
2. Display dashboard with graphics  
3. Export results in multiple formats
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.utils.demo_utilities import DemoOrchestrator
    from src.utils.error_handling import (
        error_handler, ErrorCategory, ErrorSeverity, handle_exceptions, safe_execute
    )
    import logging
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @handle_exceptions(ErrorCategory.SYSTEM, ErrorSeverity.HIGH)
    def run_first_stage_demo(output_dir: str = "./demo_reports") -> dict:
        """
        Executa demonstração da primeira etapa usando sistema modularizado.
        
        Args:
            output_dir: Diretório de saída para relatórios
            
        Returns:
            dict: Resultado da demonstração
        """
        try:
            # Criar orquestrador da demonstração
            demo = DemoOrchestrator(output_dir=output_dir)
            
            # Executar demonstração completa
            result = demo.run_complete_demo()
            
            logger.info("Demonstração da primeira etapa executada com sucesso")
            return result
            
        except Exception as e:
            error = error_handler.create_error(
                message="Falha durante demonstração da primeira etapa",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.HIGH,
                details=f"Diretório de saída: {output_dir}",
                original_exception=e
            )
            error_handler.handle_error(error)
            raise

    def show_usage_instructions():
        """Exibe instruções de uso do sistema."""
        print("\n🎉 Demonstração concluída com sucesso!")
        print("\nPara executar o dashboard aprimorado:")
        print("   streamlit run dashboards/enhanced_dashboard.py")
        print("\nPara gerar relatórios programaticamente:")
        print("   python services/reporting/unified_reports.py")
        print("\nPara executar o monitoramento do sistema:")
        print("   python monitoramento.py")
        print("\nPara validar configuração:")
        print("   python validate_config.py")

    def main():
        """
        Função principal da demonstração usando sistema modularizado.
        """
        try:
            # Executar demonstração
            demo_result = run_first_stage_demo()
            
            # Verificar resultado
            if demo_result.get('status') == 'success':
                # Mostrar instruções de uso
                demo = DemoOrchestrator()
                demo.show_usage_instructions()
                
                print(f"\n📊 Resumo da Execução:")
                print(f"   Relatórios gerados: {demo_result.get('reports_generated', 0)}")
                print(f"   Status: {demo_result.get('status', 'unknown')}")
                print(f"   Timestamp: {demo_result.get('timestamp', 'N/A')}")
                
                return 0
            else:
                print(f"❌ Demonstração falhou: {demo_result}")
                return 1
                
        except Exception as e:
            print(f"❌ Erro durante demonstração: {e}")
            logger.error(f"Erro na demonstração: {e}")
            return 1

    if __name__ == "__main__":
        try:
            exit_code = main()
            sys.exit(exit_code)
        except KeyboardInterrupt:
            print("\n⚠️  Demonstração interrompida pelo usuário")
            sys.exit(130)  # Standard exit code for Ctrl+C

except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("\n🔧 Demonstração básica:")
    print("O sistema modularizado não está disponível.")
    print("Executando demonstração básica como fallback...")
    
    # Fallback para demonstração básica
    def basic_demo():
        """Demonstração básica como fallback."""
        print("\n🚀 AUDITORIA360 - Demonstração Básica da Primeira Etapa")
        print("=" * 60)
        
        # Verificações básicas
        basic_structure = {
            "src/": "Código fonte principal",
            "docs/": "Documentação",
            "dashboards/": "Dashboards Streamlit",
            "tests/": "Testes automatizados"
        }
        
        print("📁 Verificando estrutura básica do projeto:")
        for folder, description in basic_structure.items():
            if Path(folder).exists():
                print(f"   ✅ {folder} - {description}")
            else:
                print(f"   ❌ {folder} - {description} (não encontrado)")
        
        # Relatórios simulados
        print("\n📊 Simulando geração de relatórios:")
        report_types = ["Diário", "Semanal", "Mensal"]
        for report in report_types:
            print(f"   📄 Relatório {report}: Simulado")
        
        print("\n✨ Demonstração básica concluída")
        print("Para funcionalidade completa, instale as dependências:")
        print("   pip install -r requirements.txt")
        
        return 0

    if __name__ == "__main__":
        try:
            exit_code = basic_demo()
            sys.exit(exit_code)
        except KeyboardInterrupt:
            print("\n⚠️  Demonstração interrompida pelo usuário")
            sys.exit(130)