"""
Enhanced Monitoring Script for AUDITORIA360 (Refatorado)
Integrates with the advanced monitoring system and provides CLI interface.
Uses modularized monitoring utilities for better organization.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.utils.system_monitor import SystemMonitor
    from src.utils.error_handling import (
        error_handler, ErrorCategory, ErrorSeverity, handle_exceptions, safe_execute
    )
    import logging
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @handle_exceptions(ErrorCategory.SYSTEM, ErrorSeverity.HIGH)
    async def run_monitoring_system():
        """
        Executa o sistema de monitoramento completo usando módulos refatorados.
        
        Returns:
            dict: Resultado do monitoramento
        """
        try:
            # Criar instância do monitor do sistema
            monitor = SystemMonitor()
            
            # Executar monitoramento completo
            monitoring_result = await monitor.run_complete_monitoring()
            
            # Log do resultado
            logger.info("Monitoramento do sistema executado com sucesso")
            
            return monitoring_result
            
        except Exception as e:
            error = error_handler.create_error(
                message="Falha no sistema de monitoramento",
                category=ErrorCategory.SYSTEM,
                severity=ErrorSeverity.CRITICAL,
                details="Erro durante execução do monitoramento completo",
                original_exception=e
            )
            error_handler.handle_error(error)
            raise

    def display_monitoring_summary(result: dict) -> None:
        """
        Exibe resumo do resultado do monitoramento.
        
        Args:
            result: Resultado do monitoramento
        """
        print("\n📋 RESUMO DO MONITORAMENTO")
        print("=" * 40)
        
        # Status geral
        status = result.get('overall_status', 'unknown')
        status_icon = {
            'healthy': '✅',
            'degraded': '⚠️',
            'unhealthy': '❌',
            'error': '💥'
        }.get(status, '❓')
        
        print(f"Status Geral: {status_icon} {status.upper()}")
        print(f"Timestamp: {result.get('timestamp', 'N/A')}")
        print(f"Monitoramento Avançado: {'✅' if result.get('enhanced_monitoring') else '❌'}")
        
        # Resumo de serviços
        services = result.get('services', {})
        if services:
            healthy_services = sum(1 for s in services.values() if s.get('status') == 'healthy')
            total_services = len(services)
            print(f"Serviços: {healthy_services}/{total_services} saudáveis")
        
        # Resumo de infraestrutura
        infrastructure = result.get('infrastructure', {})
        if infrastructure:
            healthy_infra = sum(1 for i in infrastructure.values() if i.get('status') == 'healthy')
            total_infra = len(infrastructure)
            print(f"Infraestrutura: {healthy_infra}/{total_infra} componentes saudáveis")
        
        # Alertas
        alerts = result.get('alerts')
        if alerts and isinstance(alerts, list):
            critical_alerts = sum(1 for a in alerts if a.get('severity') == 'critical')
            print(f"Alertas: {len(alerts)} ativos ({critical_alerts} críticos)")
        elif alerts is None:
            print("Alertas: Sistema não disponível")
        else:
            print("Alertas: Nenhum alerta ativo")

    def save_monitoring_report(result: dict, output_file: str = "monitoring_report.json") -> None:
        """
        Salva relatório de monitoramento em arquivo.
        
        Args:
            result: Resultado do monitoramento
            output_file: Nome do arquivo de saída
        """
        def _save_report():
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"📄 Relatório salvo em: {output_file}")
            return True
        
        success = safe_execute(
            _save_report,
            default_value=False,
            category=ErrorCategory.SYSTEM
        )
        
        if not success:
            print(f"❌ Falha ao salvar relatório em {output_file}")

    async def main():
        """
        Função principal do monitoramento usando sistema modularizado.
        """
        print("=== AUDITORIA360 Enhanced System Monitor ===")
        print("Sistema de monitoramento refatorado e modularizado")
        print(f"Executado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        try:
            # Executar monitoramento
            monitoring_result = await run_monitoring_system()
            
            # Exibir resumo
            display_monitoring_summary(monitoring_result)
            
            # Salvar relatório
            save_monitoring_report(monitoring_result)
            
            # Verificar se há problemas críticos
            if monitoring_result.get('overall_status') in ['unhealthy', 'error']:
                print("\n⚠️  ATENÇÃO: Problemas críticos detectados!")
                print("Consulte o relatório detalhado e tome ações corretivas.")
                return 1
            elif monitoring_result.get('overall_status') == 'degraded':
                print("\n⚠️  Aviso: Sistema em estado degradado.")
                print("Alguns componentes precisam de atenção.")
                return 0
            else:
                print("\n✅ Sistema funcionando normalmente.")
                return 0
                
        except Exception as e:
            print(f"❌ Erro crítico durante monitoramento: {e}")
            logger.error(f"Erro crítico no monitoramento: {e}")
            return 1

    if __name__ == "__main__":
        try:
            import asyncio
            exit_code = asyncio.run(main())
            sys.exit(exit_code)
        except KeyboardInterrupt:
            print("\n⚠️  Monitoramento interrompido pelo usuário")
            sys.exit(130)  # Standard exit code for Ctrl+C

except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("\n🔧 Sistema de monitoramento básico:")
    print("O sistema modularizado não está disponível.")
    print("Executando monitoramento básico como fallback...")
    
    # Fallback para monitoramento básico
    import requests
    import asyncio
    from datetime import datetime

    async def basic_monitoring():
        """Monitoramento básico como fallback."""
        print("\n=== Monitoramento Básico ===")
        
        # Verificações básicas de serviço
        services = {
            "API Health": "http://localhost:8000/health",
            "API Root": "http://localhost:8000/",
        }
        
        results = {}
        
        for service_name, url in services.items():
            try:
                start_time = datetime.now()
                response = requests.get(url, timeout=5)
                response_time = (datetime.now() - start_time).total_seconds() * 1000
                
                if response.status_code == 200:
                    print(f"✅ {service_name}: OK ({response_time:.0f}ms)")
                    results[service_name] = "healthy"
                else:
                    print(f"❌ {service_name}: Falha ({response.status_code})")
                    results[service_name] = "unhealthy"
            except requests.exceptions.Timeout:
                print(f"⏱️  {service_name}: Timeout")
                results[service_name] = "timeout"
            except Exception as e:
                print(f"❌ {service_name}: Erro ({e})")
                results[service_name] = "error"
        
        # Verificação básica de arquivo
        important_files = ["src/main.py", "requirements.txt", "README.md"]
        for file in important_files:
            if Path(file).exists():
                print(f"✅ Arquivo {file}: Presente")
            else:
                print(f"❌ Arquivo {file}: Ausente")
        
        healthy_services = sum(1 for status in results.values() if status == "healthy")
        total_services = len(results)
        
        print(f"\n📊 Resumo: {healthy_services}/{total_services} serviços saudáveis")
        
        return 0 if healthy_services == total_services else 1

    if __name__ == "__main__":
        try:
            exit_code = asyncio.run(basic_monitoring())
            sys.exit(exit_code)
        except KeyboardInterrupt:
            print("\n⚠️  Monitoramento interrompido pelo usuário")
            sys.exit(130)
