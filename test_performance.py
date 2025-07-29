"""
Performance Test Suite for AUDITORIA360 Optimized Endpoints (Refatorado)
Tests the performance improvements implemented for the three critical endpoints
Uses modularized performance testing framework for better organization.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.utils.performance_testing import PerformanceTestOrchestrator
    from src.utils.error_handling import (
        error_handler, ErrorCategory, ErrorSeverity, handle_exceptions, safe_execute
    )
    import logging
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @handle_exceptions(ErrorCategory.PERFORMANCE, ErrorSeverity.HIGH)
    def run_performance_test_suite() -> dict:
        """
        Executa suite completa de testes de performance usando sistema modularizado.
        
        Returns:
            dict: Resultado consolidado dos testes
        """
        try:
            # Criar orquestrador de testes
            orchestrator = PerformanceTestOrchestrator()
            
            # Executar todos os testes
            results = orchestrator.run_all_performance_tests()
            
            logger.info("Suite de testes de performance executada com sucesso")
            return results
            
        except Exception as e:
            error = error_handler.create_error(
                message="Falha durante execução dos testes de performance",
                category=ErrorCategory.PERFORMANCE,
                severity=ErrorSeverity.HIGH,
                details="Erro durante execução da suite de testes",
                original_exception=e
            )
            error_handler.handle_error(error)
            raise

    def save_performance_report(results: dict, output_file: str = "performance_test_report.json") -> None:
        """
        Salva relatório de performance em arquivo.
        
        Args:
            results: Resultados dos testes
            output_file: Nome do arquivo de saída
        """
        def _save_report():
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"\n📄 Relatório detalhado salvo em: {output_file}")
            return True
        
        success = safe_execute(
            _save_report,
            default_value=False,
            category=ErrorCategory.SYSTEM
        )
        
        if not success:
            print(f"❌ Falha ao salvar relatório em {output_file}")

    def display_performance_summary(results: dict) -> None:
        """
        Exibe resumo dos resultados de performance.
        
        Args:
            results: Resultados dos testes
        """
        print("\n📊 RESUMO EXECUTIVO DOS TESTES")
        print("=" * 40)
        
        # Métricas gerais
        total_suites = results.get('total_test_suites', 0)
        suites_passed = results.get('suites_passed', 0)
        success_rate = results.get('overall_success_rate', 0)
        
        print(f"Total de Suites: {total_suites}")
        print(f"Suites Aprovadas: {suites_passed}")
        print(f"Taxa de Sucesso: {success_rate:.1f}%")
        
        # Status geral
        status = results.get('overall_status', 'unknown')
        status_icon = {
            'success': '✅',
            'needs_improvement': '⚠️',
            'error': '❌'
        }.get(status, '❓')
        
        print(f"Status Geral: {status_icon} {status.replace('_', ' ').title()}")
        
        # Recomendações
        if status != 'success':
            print("\n💡 Recomendações:")
            print("   • Revisar endpoints com performance abaixo da meta")
            print("   • Considerar otimizações adicionais de cache")
            print("   • Analisar queries de banco de dados")
            print("   • Implementar mais paralelização")

    def main():
        """
        Função principal dos testes de performance usando sistema modularizado.
        """
        try:
            print("🚀 AUDITORIA360 - Suite de Testes de Performance Refatorada")
            print("Sistema de testes modularizado e otimizado")
            print()
            
            # Executar testes
            test_results = run_performance_test_suite()
            
            # Exibir resumo
            display_performance_summary(test_results)
            
            # Salvar relatório
            save_performance_report(test_results)
            
            # Determinar código de saída baseado nos resultados
            if test_results.get('overall_status') == 'success':
                print("\n🎉 Todos os testes de performance passaram!")
                return 0
            elif test_results.get('overall_status') == 'needs_improvement':
                print("\n⚠️  Alguns endpoints precisam de otimização.")
                return 1
            else:
                print("\n❌ Falhas significativas nos testes de performance.")
                return 2
                
        except Exception as e:
            print(f"❌ Erro durante testes de performance: {e}")
            logger.error(f"Erro nos testes de performance: {e}")
            return 3

    if __name__ == "__main__":
        try:
            exit_code = main()
            sys.exit(exit_code)
        except KeyboardInterrupt:
            print("\n⚠️  Testes interrompidos pelo usuário")
            sys.exit(130)  # Standard exit code for Ctrl+C

except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("\n🔧 Testes básicos de performance:")
    print("O sistema modularizado não está disponível.")
    print("Executando testes básicos como fallback...")
    
    # Fallback para testes básicos
    import time
    import requests
    from datetime import datetime

    def basic_performance_test():
        """Testes básicos de performance como fallback."""
        print("\n🏃 Testes Básicos de Performance")
        print("=" * 40)
        
        # Teste simples de resposta
        test_urls = [
            ("API Health", "http://localhost:8000/health"),
            ("API Root", "http://localhost:8000/"),
        ]
        
        results = []
        
        for name, url in test_urls:
            try:
                print(f"\n🔍 Testando {name}...")
                
                # Múltiplas requisições para média
                durations = []
                for i in range(3):
                    start_time = time.time()
                    response = requests.get(url, timeout=5)
                    duration = time.time() - start_time
                    durations.append(duration)
                
                avg_duration = sum(durations) / len(durations)
                
                print(f"   Tempo médio: {avg_duration:.3f}s")
                print(f"   Status: {response.status_code}")
                
                # Avaliação básica
                if avg_duration < 1.0:
                    print("   ✅ Performance adequada")
                    results.append(True)
                else:
                    print("   ⚠️  Performance pode ser melhorada")
                    results.append(False)
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                results.append(False)
        
        # Resumo
        passed_tests = sum(results)
        total_tests = len(results)
        
        print(f"\n📊 Resumo: {passed_tests}/{total_tests} testes passaram")
        
        if passed_tests == total_tests:
            print("✅ Todos os testes básicos passaram")
            return 0
        else:
            print("⚠️  Alguns testes precisam de atenção")
            return 1

    if __name__ == "__main__":
        try:
            exit_code = basic_performance_test()
            sys.exit(exit_code)
        except KeyboardInterrupt:
            print("\n⚠️  Testes interrompidos pelo usuário")
            sys.exit(130)