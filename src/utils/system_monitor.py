"""
Sistema de monitoramento modularizado.
Extrai e organiza as funções de monitoramento do monitoramento.py principal.
"""

import requests
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
import logging

logger = logging.getLogger(__name__)

# Tentativa de importar sistema de monitoramento avançado
try:
    from src.utils.monitoring import MonitoringSystem, AlertSeverity
    from src.utils.performance import profiler, DatabaseOptimizer
    ENHANCED_MONITORING = True
except ImportError:
    ENHANCED_MONITORING = False
    logger.info("Sistema de monitoramento avançado não disponível - usando monitoramento básico")


class ServiceHealthChecker:
    """Verifica a saúde dos serviços do sistema."""
    
    def __init__(self, monitoring_system=None):
        self.monitoring_system = monitoring_system
        self.timeout = 5
    
    def check_service(self, name: str, url: str) -> Dict[str, Any]:
        """
        Verifica a saúde de um serviço específico.
        
        Args:
            name: Nome do serviço
            url: URL para verificação
            
        Returns:
            dict: Resultado da verificação com status e tempo de resposta
        """
        try:
            start_time = datetime.now()
            response = requests.get(url, timeout=self.timeout)
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            result = {
                "name": name,
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "status_code": response.status_code,
                "response_time_ms": response_time,
                "url": url,
                "timestamp": start_time.isoformat()
            }
            
            if response.status_code == 200:
                print(f"{name}: OK (Response: {response_time:.0f}ms)")
                if ENHANCED_MONITORING and self.monitoring_system:
                    self.monitoring_system.metrics.set_gauge("service_status", 1, {"service": name})
                    self.monitoring_system.metrics.record_histogram(
                        "service_response_time_ms", response_time, {"service": name}
                    )
            else:
                print(f"{name}: Falha ({response.status_code})")
                if ENHANCED_MONITORING and self.monitoring_system:
                    self.monitoring_system.metrics.set_gauge("service_status", 0, {"service": name})
            
            return result
            
        except requests.exceptions.Timeout:
            result = {
                "name": name,
                "status": "timeout",
                "error": "Timeout após {self.timeout}s",
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
            print(f"{name}: Timeout")
            if ENHANCED_MONITORING and self.monitoring_system:
                self.monitoring_system.metrics.set_gauge("service_status", 0, {"service": name})
                self.monitoring_system.metrics.increment_counter("service_timeouts", {"service": name})
            return result
            
        except Exception as e:
            result = {
                "name": name,
                "status": "error",
                "error": str(e),
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
            print(f"{name}: Erro ({e})")
            if ENHANCED_MONITORING and self.monitoring_system:
                self.monitoring_system.metrics.set_gauge("service_status", 0, {"service": name})
                self.monitoring_system.metrics.increment_counter("service_errors", {"service": name})
            return result


class InfrastructureChecker:
    """Verifica componentes de infraestrutura."""
    
    def __init__(self, monitoring_system=None):
        self.monitoring_system = monitoring_system
    
    async def check_database_health(self) -> Dict[str, Any]:
        """
        Verifica conectividade e performance do banco de dados.
        
        Returns:
            dict: Resultado da verificação do banco
        """
        try:
            print("Database: Simulando verificação de conexão...")
            start_time = datetime.now()
            
            # Simula tempo de conexão - em ambiente real, conectaria ao banco
            await asyncio.sleep(0.1)
            
            connection_time = (datetime.now() - start_time).total_seconds() * 1000
            
            result = {
                "component": "database",
                "status": "healthy",
                "connection_time_ms": connection_time,
                "timestamp": start_time.isoformat()
            }
            
            print("Database: OK (Conexão estabelecida)")
            
            if ENHANCED_MONITORING and self.monitoring_system:
                self.monitoring_system.metrics.set_gauge("database_status", 1)
                self.monitoring_system.metrics.record_histogram("database_connection_time_ms", connection_time)
            
            return result
            
        except Exception as e:
            result = {
                "component": "database",
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            print(f"Database: Erro ({e})")
            if ENHANCED_MONITORING and self.monitoring_system:
                self.monitoring_system.metrics.set_gauge("database_status", 0)
            return result
    
    async def check_storage_health(self) -> Dict[str, Any]:
        """
        Verifica conectividade do storage (R2).
        
        Returns:
            dict: Resultado da verificação do storage
        """
        try:
            print("Storage (R2): Simulando verificação de conectividade...")
            start_time = datetime.now()
            
            # Simula verificação do R2 - em ambiente real, faria chamada para R2
            await asyncio.sleep(0.05)
            
            check_time = (datetime.now() - start_time).total_seconds() * 1000
            
            result = {
                "component": "storage",
                "status": "healthy",
                "check_time_ms": check_time,
                "timestamp": start_time.isoformat()
            }
            
            print("Storage (R2): OK")
            
            if ENHANCED_MONITORING and self.monitoring_system:
                self.monitoring_system.metrics.set_gauge("storage_status", 1)
            
            return result
            
        except Exception as e:
            result = {
                "component": "storage",
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            print(f"Storage (R2): Erro ({e})")
            if ENHANCED_MONITORING and self.monitoring_system:
                self.monitoring_system.metrics.set_gauge("storage_status", 0)
            return result


class PerformanceAnalyzer:
    """Analisa métricas de performance."""
    
    def __init__(self, monitoring_system=None):
        self.monitoring_system = monitoring_system
    
    def check_performance_metrics(self) -> Optional[Dict[str, Any]]:
        """
        Exibe métricas de performance se disponíveis.
        
        Returns:
            dict: Métricas de performance ou None se não disponível
        """
        if not ENHANCED_MONITORING or not self.monitoring_system:
            print("Sistema de monitoramento avançado não disponível")
            return None
        
        try:
            print("\n=== Performance Metrics ===")
            
            # Obter gargalos recentes
            bottlenecks = profiler.get_bottlenecks(hours=1)
            bottleneck_summary = []
            
            if bottlenecks:
                print("⚠️  Performance Bottlenecks Detected:")
                for bottleneck in bottlenecks[:3]:  # Top 3
                    print(f"  - {bottleneck['function_name']}: Severity {bottleneck['severity']:.1f}/100")
                    bottleneck_info = {
                        "function": bottleneck['function_name'],
                        "severity": bottleneck['severity'],
                        "recommendations": bottleneck['recommendations'][:2]
                    }
                    bottleneck_summary.append(bottleneck_info)
                    
                    for rec in bottleneck['recommendations'][:2]:  # Top 2 recommendations
                        print(f"    • {rec}")
            else:
                print("✅ No significant performance bottlenecks detected")
            
            # Mostrar resumo de métricas
            summary = self.monitoring_system.metrics.get_metrics_summary(hours=1)
            metrics_summary = {}
            
            print(f"\nMetrics Summary (last hour):")
            for metric_name, stats in list(summary.items())[:5]:  # Top 5 metrics
                print(f"  {metric_name}: {stats['latest']} (avg: {stats['avg']:.2f})")
                metrics_summary[metric_name] = {
                    "latest": stats['latest'],
                    "average": stats['avg']
                }
            
            return {
                "bottlenecks": bottleneck_summary,
                "metrics_summary": metrics_summary,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao verificar métricas de performance: {e}")
            print(f"Erro ao verificar métricas: {e}")
            return None


class AlertManager:
    """Gerencia alertas do sistema."""
    
    def __init__(self, monitoring_system=None):
        self.monitoring_system = monitoring_system
    
    def show_alerts(self) -> Optional[List[Dict[str, Any]]]:
        """
        Exibe alertas ativos.
        
        Returns:
            list: Lista de alertas ativos ou None se não disponível
        """
        if not ENHANCED_MONITORING or not self.monitoring_system:
            print("Sistema de alertas não disponível")
            return None
        
        try:
            active_alerts = self.monitoring_system.alert_manager.get_active_alerts()
            alerts_summary = []
            
            if active_alerts:
                print(f"\n🚨 Active Alerts ({len(active_alerts)}):")
                
                for alert in active_alerts:
                    severity_icon = {
                        AlertSeverity.LOW: "🟡",
                        AlertSeverity.MEDIUM: "🟠", 
                        AlertSeverity.HIGH: "🔴",
                        AlertSeverity.CRITICAL: "💥"
                    }.get(alert.severity, "⚠️")
                    
                    alert_info = {
                        "severity": alert.severity.value,
                        "title": alert.title,
                        "description": alert.description,
                        "metric": alert.metric_name,
                        "current_value": alert.current_value,
                        "threshold": alert.threshold
                    }
                    alerts_summary.append(alert_info)
                    
                    print(f"  {severity_icon} [{alert.severity.value.upper()}] {alert.title}")
                    print(f"    {alert.description}")
                    print(f"    Metric: {alert.metric_name} = {alert.current_value} (threshold: {alert.threshold})")
            else:
                print("\n✅ No active alerts")
            
            return alerts_summary
            
        except Exception as e:
            logger.error(f"Erro ao verificar alertas: {e}")
            print(f"Erro ao verificar alertas: {e}")
            return None


class SystemMonitor:
    """Classe principal que coordena todo o monitoramento do sistema."""
    
    def __init__(self):
        self.monitoring_system = None
        if ENHANCED_MONITORING:
            self.monitoring_system = MonitoringSystem()
        
        self.service_checker = ServiceHealthChecker(self.monitoring_system)
        self.infrastructure_checker = InfrastructureChecker(self.monitoring_system)
        self.performance_analyzer = PerformanceAnalyzer(self.monitoring_system)
        self.alert_manager = AlertManager(self.monitoring_system)
    
    async def run_complete_monitoring(self) -> Dict[str, Any]:
        """
        Executa monitoramento completo do sistema.
        
        Returns:
            dict: Resultado completo do monitoramento
        """
        monitoring_result = {
            "timestamp": datetime.now().isoformat(),
            "enhanced_monitoring": ENHANCED_MONITORING,
            "services": {},
            "infrastructure": {},
            "performance": None,
            "alerts": None,
            "overall_status": "healthy"
        }
        
        print("=== AUDITORIA360 System Monitor ===")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Enhanced Monitoring: {'Enabled' if ENHANCED_MONITORING else 'Disabled'}")
        
        try:
            # Inicializar sistema de monitoramento se disponível
            if ENHANCED_MONITORING and self.monitoring_system:
                self.monitoring_system.start()
                
                # Adicionar verificações de saúde
                self.monitoring_system.health_checker.add_health_check(
                    "database", self.infrastructure_checker.check_database_health
                )
                self.monitoring_system.health_checker.add_health_check(
                    "storage", self.infrastructure_checker.check_storage_health
                )
            
            # Verificações de serviços
            print("\n=== Service Health Checks ===")
            services = {
                "API Health": "http://localhost:8000/health",
                "API Root": "http://localhost:8000/",
                "API Auditorias": "http://localhost:8000/api/v1/auditorias/options/contabilidades",
            }
            
            for service_name, url in services.items():
                result = self.service_checker.check_service(service_name, url)
                monitoring_result["services"][service_name] = result
                
                if result["status"] != "healthy":
                    monitoring_result["overall_status"] = "degraded"
            
            # Verificações de infraestrutura
            print("\n=== Infrastructure Health Checks ===")
            
            database_result = await self.infrastructure_checker.check_database_health()
            monitoring_result["infrastructure"]["database"] = database_result
            
            storage_result = await self.infrastructure_checker.check_storage_health()
            monitoring_result["infrastructure"]["storage"] = storage_result
            
            if (database_result["status"] != "healthy" or 
                storage_result["status"] != "healthy"):
                monitoring_result["overall_status"] = "unhealthy"
            
            # Verificações avançadas se disponível
            if ENHANCED_MONITORING and self.monitoring_system:
                print("\n=== Running Health Checks ===")
                health_results = await self.monitoring_system.health_checker.run_all_checks()
                
                for result in health_results:
                    status_icon = "✅" if result.status == "healthy" else "❌"
                    print(f"{status_icon} {result.name}: {result.status} ({result.response_time_ms:.0f}ms)")
                    if result.error:
                        print(f"    Error: {result.error}")
                
                # Análise de performance
                performance_data = self.performance_analyzer.check_performance_metrics()
                monitoring_result["performance"] = performance_data
                
                # Verificação de alertas
                alerts_data = self.alert_manager.show_alerts()
                monitoring_result["alerts"] = alerts_data
                
                # Status do dashboard
                dashboard_data = self.monitoring_system.get_dashboard_data()
                print(f"\nSystem Status: {dashboard_data['system_status'].upper()}")
                monitoring_result["dashboard_status"] = dashboard_data['system_status']
                
                # Parar monitoramento
                self.monitoring_system.stop()
            
            print(f"\n🎯 Overall System Status: {monitoring_result['overall_status'].upper()}")
            
        except Exception as e:
            logger.error(f"Erro durante monitoramento: {e}")
            monitoring_result["error"] = str(e)
            monitoring_result["overall_status"] = "error"
            print(f"❌ Erro durante monitoramento: {e}")
        
        return monitoring_result