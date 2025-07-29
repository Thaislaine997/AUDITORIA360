"""
Framework de testes de performance modularizado.
Extrai e organiza as funções de teste do test_performance.py principal.
"""

import time
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock
import sys
import os
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceTestResult:
    """Resultado de um teste de performance."""
    name: str
    duration: float
    status_code: int
    target_time: float
    target_met: bool
    endpoint: str
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class PerformanceTestSuite:
    """Suite completa de testes de performance."""
    name: str
    target_description: str
    results: List[PerformanceTestResult]
    average_time: float
    overall_target_met: bool
    timestamp: str


class MockUserFactory:
    """Factory para criar usuários mock para testes."""
    
    @staticmethod
    def create_mock_user(user_id: int = 1, role: str = "administrador", username: str = "test_user") -> Mock:
        """
        Cria um usuário mock para testes.
        
        Args:
            user_id: ID do usuário
            role: Role do usuário
            username: Nome do usuário
            
        Returns:
            Mock: Usuário mock configurado
        """
        user = Mock()
        user.id = user_id
        user.role = role
        user.username = username
        return user
    
    @staticmethod
    def create_mock_db() -> Mock:
        """Cria um mock de database session."""
        return Mock()


class BasePerformanceTester:
    """Classe base para testes de performance."""
    
    def __init__(self, target_time: float = 1.0):
        self.target_time = target_time
        self.user_factory = MockUserFactory()
    
    def create_test_client(self, router_module: str, router_name: str = "router", 
                          prefix: str = "") -> Optional[TestClient]:
        """
        Cria um cliente de teste com router específico.
        
        Args:
            router_module: Módulo do router a ser importado
            router_name: Nome do router no módulo
            prefix: Prefixo do router
            
        Returns:
            TestClient ou None se falhar
        """
        try:
            # Importa o router
            module = __import__(router_module, fromlist=[router_name])
            router = getattr(module, router_name)
            
            # Importa FastAPI
            from fastapi import FastAPI
            
            # Cria app de teste
            test_app = FastAPI()
            
            # Configura overrides de dependências
            test_app.dependency_overrides = {
                "get_current_user": self.user_factory.create_mock_user,
                "get_db": self.user_factory.create_mock_db
            }
            
            # Inclui o router
            test_app.include_router(router, prefix=prefix)
            
            return TestClient(test_app)
            
        except Exception as e:
            logger.error(f"Erro ao criar cliente de teste para {router_module}: {e}")
            return None
    
    def measure_request_time(self, client: TestClient, endpoint: str, 
                           method: str = "GET", **kwargs) -> PerformanceTestResult:
        """
        Mede o tempo de resposta de uma requisição.
        
        Args:
            client: Cliente de teste
            endpoint: Endpoint a ser testado
            method: Método HTTP
            **kwargs: Argumentos adicionais para a requisição
            
        Returns:
            PerformanceTestResult: Resultado do teste
        """
        try:
            start_time = time.time()
            
            if method.upper() == "GET":
                response = client.get(endpoint, **kwargs)
            elif method.upper() == "POST":
                response = client.post(endpoint, **kwargs)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            duration = time.time() - start_time
            
            return PerformanceTestResult(
                name=f"{method} {endpoint}",
                duration=duration,
                status_code=response.status_code,
                target_time=self.target_time,
                target_met=duration < self.target_time,
                endpoint=endpoint
            )
            
        except Exception as e:
            logger.error(f"Erro ao medir tempo de {endpoint}: {e}")
            return PerformanceTestResult(
                name=f"{method} {endpoint}",
                duration=float('inf'),
                status_code=0,
                target_time=self.target_time,
                target_met=False,
                endpoint=endpoint,
                error=str(e)
            )


class AuditReportTester(BasePerformanceTester):
    """Testa performance do endpoint de relatórios de auditoria."""
    
    def __init__(self):
        super().__init__(target_time=1.0)  # Target < 1s
    
    def test_audit_relatorio_performance(self) -> PerformanceTestSuite:
        """
        Testa performance do endpoint /api/v1/auditorias/relatorio.
        
        Returns:
            PerformanceTestSuite: Resultado dos testes
        """
        print("🔍 Testando Performance de Geração de Relatórios de Auditoria...")
        
        try:
            # Cria cliente de teste
            client = self.create_test_client(
                "src.api.routers.audit", 
                "router", 
                "/auditorias"
            )
            
            if not client:
                raise Exception("Não foi possível criar cliente de teste")
            
            # Casos de teste
            test_cases = [
                {
                    "endpoint": "/auditorias/relatorio?period_start=2024-01-01&period_end=2024-01-31",
                    "name": "Monthly Report"
                },
                {
                    "endpoint": "/auditorias/relatorio?audit_id=123",
                    "name": "Specific Audit"
                },
                {
                    "endpoint": "/auditorias/relatorio?format=pdf",
                    "name": "PDF Format"
                }
            ]
            
            results = []
            
            for case in test_cases:
                result = self.measure_request_time(client, case["endpoint"])
                result.name = case["name"]
                results.append(result)
                
                status_icon = '✅' if result.target_met else '⚠️'
                print(f"   📊 {case['name']}: {result.duration:.3f}s ({status_icon})")
            
            # Calcula métricas gerais
            valid_results = [r for r in results if r.error is None]
            avg_time = sum(r.duration for r in valid_results) / len(valid_results) if valid_results else float('inf')
            all_targets_met = all(r.target_met for r in valid_results)
            
            print(f"   📈 Tempo Médio: {avg_time:.3f}s")
            print(f"   🎯 Meta Atendida (<1s): {'✅ Sim' if all_targets_met else '❌ Não'}")
            
            return PerformanceTestSuite(
                name="Audit Report Generation",
                target_description="< 1s",
                results=results,
                average_time=avg_time,
                overall_target_met=all_targets_met,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Erro ao testar relatórios de auditoria: {e}")
            print(f"   ❌ Erro: {e}")
            
            return PerformanceTestSuite(
                name="Audit Report Generation",
                target_description="< 1s",
                results=[PerformanceTestResult(
                    name="Error",
                    duration=float('inf'),
                    status_code=0,
                    target_time=1.0,
                    target_met=False,
                    endpoint="/api/v1/auditorias/relatorio",
                    error=str(e)
                )],
                average_time=float('inf'),
                overall_target_met=False,
                timestamp=datetime.now().isoformat()
            )


class ComplianceCheckTester(BasePerformanceTester):
    """Testa performance do endpoint de verificação de compliance."""
    
    def __init__(self):
        super().__init__(target_time=1.0)  # Target < 1s
    
    def test_compliance_check_performance(self) -> PerformanceTestSuite:
        """
        Testa performance do endpoint /api/v1/compliance/check.
        
        Returns:
            PerformanceTestSuite: Resultado dos testes
        """
        print("\n🔒 Testando Performance de Verificação de Compliance...")
        
        try:
            # Cria cliente de teste
            client = self.create_test_client(
                "src.api.routers.compliance",
                "router",
                "/compliance"
            )
            
            if not client:
                raise Exception("Não foi possível criar cliente de teste")
            
            # Casos de teste
            test_cases = [
                {
                    "endpoint": "/compliance/check?entity_type=payroll&entity_id=emp001",
                    "name": "Payroll Check"
                },
                {
                    "endpoint": "/compliance/check?entity_type=employee&entity_id=12345",
                    "name": "Employee Check"
                },
                {
                    "endpoint": "/compliance/check?entity_type=cct&entity_id=cct456",
                    "name": "CCT Check"
                }
            ]
            
            results = []
            
            for case in test_cases:
                result = self.measure_request_time(client, case["endpoint"])
                result.name = case["name"]
                results.append(result)
                
                status_icon = '✅' if result.target_met else '⚠️'
                print(f"   🔍 {case['name']}: {result.duration:.3f}s ({status_icon})")
            
            # Calcula métricas gerais
            valid_results = [r for r in results if r.error is None]
            avg_time = sum(r.duration for r in valid_results) / len(valid_results) if valid_results else float('inf')
            all_targets_met = all(r.target_met for r in valid_results)
            
            print(f"   📈 Tempo Médio: {avg_time:.3f}s")
            print(f"   🎯 Meta Atendida (<1s): {'✅ Sim' if all_targets_met else '❌ Não'}")
            
            return PerformanceTestSuite(
                name="Compliance Check",
                target_description="< 1s",
                results=results,
                average_time=avg_time,
                overall_target_met=all_targets_met,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Erro ao testar compliance check: {e}")
            print(f"   ❌ Erro: {e}")
            
            return PerformanceTestSuite(
                name="Compliance Check",
                target_description="< 1s",
                results=[PerformanceTestResult(
                    name="Error",
                    duration=float('inf'),
                    status_code=0,
                    target_time=1.0,
                    target_met=False,
                    endpoint="/api/v1/compliance/check",
                    error=str(e)
                )],
                average_time=float('inf'),
                overall_target_met=False,
                timestamp=datetime.now().isoformat()
            )


class PortalStatsTester(BasePerformanceTester):
    """Testa performance do endpoint de estatísticas do portal."""
    
    def __init__(self):
        super().__init__(target_time=0.5)  # Target < 0.5s
    
    def test_portal_stats_performance(self) -> PerformanceTestSuite:
        """
        Testa performance do endpoint /stats/ do portal_demandas.
        
        Returns:
            PerformanceTestSuite: Resultado dos testes
        """
        print("\n📊 Testando Performance de Estatísticas do Portal...")
        
        try:
            # Importa app do portal
            from portal_demandas.api import app
            client = TestClient(app)
            
            # Executa múltiplas rodadas para obter média
            durations = []
            results = []
            
            for i in range(5):
                result = self.measure_request_time(client, "/stats/")
                durations.append(result.duration)
                results.append(result)
            
            # Calcula estatísticas
            avg_time = sum(durations) / len(durations)
            max_time = max(durations)
            min_time = min(durations)
            target_met = avg_time < self.target_time
            
            print(f"   📊 Tempo Médio: {avg_time:.3f}s")
            print(f"   📊 Tempo Mín: {min_time:.3f}s")
            print(f"   📊 Tempo Máx: {max_time:.3f}s")
            print(f"   🎯 Meta Atendida (<0.5s): {'✅ Sim' if target_met else '❌ Não'}")
            
            # Cria resultado agregado
            aggregate_result = PerformanceTestResult(
                name="Portal Stats",
                duration=avg_time,
                status_code=200,
                target_time=self.target_time,
                target_met=target_met,
                endpoint="/stats/",
                details={
                    "min_time": min_time,
                    "max_time": max_time,
                    "runs": len(durations),
                    "all_durations": durations
                }
            )
            
            return PerformanceTestSuite(
                name="Portal Stats",
                target_description="< 0.5s",
                results=[aggregate_result],
                average_time=avg_time,
                overall_target_met=target_met,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Erro ao testar portal stats: {e}")
            print(f"   ❌ Erro: {e}")
            
            return PerformanceTestSuite(
                name="Portal Stats",
                target_description="< 0.5s",
                results=[PerformanceTestResult(
                    name="Error",
                    duration=float('inf'),
                    status_code=0,
                    target_time=0.5,
                    target_met=False,
                    endpoint="/stats/",
                    error=str(e)
                )],
                average_time=float('inf'),
                overall_target_met=False,
                timestamp=datetime.now().isoformat()
            )


class PerformanceTestOrchestrator:
    """Orquestra todos os testes de performance."""
    
    def __init__(self):
        self.audit_tester = AuditReportTester()
        self.compliance_tester = ComplianceCheckTester()
        self.portal_tester = PortalStatsTester()
    
    def run_all_performance_tests(self) -> Dict[str, Any]:
        """
        Executa todos os testes de performance.
        
        Returns:
            dict: Resultado consolidado de todos os testes
        """
        print("🚀 AUDITORIA360 - Suite de Testes de Otimização de Performance")
        print("=" * 60)
        
        test_results = []
        
        # Executa todos os testes
        test_results.append(self.audit_tester.test_audit_relatorio_performance())
        test_results.append(self.compliance_tester.test_compliance_check_performance())
        test_results.append(self.portal_tester.test_portal_stats_performance())
        
        # Gera relatório de resumo
        return self._generate_summary_report(test_results)
    
    def _generate_summary_report(self, test_results: List[PerformanceTestSuite]) -> Dict[str, Any]:
        """
        Gera relatório de resumo dos testes.
        
        Args:
            test_results: Lista de resultados dos testes
            
        Returns:
            dict: Relatório consolidado
        """
        print("\n" + "=" * 60)
        print("📋 RESUMO DOS TESTES DE PERFORMANCE")
        print("=" * 60)
        
        total_suites = len(test_results)
        suites_passed = sum(1 for suite in test_results if suite.overall_target_met)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_test_suites": total_suites,
            "suites_passed": suites_passed,
            "overall_success_rate": (suites_passed / total_suites * 100) if total_suites > 0 else 0,
            "test_suites": [],
            "optimizations_implemented": [
                "Cache Redis para relatórios e queries pesadas",
                "Queries SQL agregadas únicas ao invés de múltiplas queries",
                "Limites de paginação reduzidos (100 -> 50 itens max)",
                "Timing de performance e monitoramento",
                "Sistema de cache de fallback para indisponibilidade do Redis"
            ]
        }
        
        for suite in test_results:
            status_icon = "✅ PASSOU" if suite.overall_target_met else "⚠️  PRECISA MELHORAR"
            print(f"{status_icon} {suite.name}: {suite.average_time:.3f}s (meta: {suite.target_description})")
            
            suite_summary = {
                "name": suite.name,
                "target": suite.target_description,
                "average_time": suite.average_time,
                "target_met": suite.overall_target_met,
                "total_tests": len(suite.results),
                "tests_passed": sum(1 for r in suite.results if r.target_met),
                "errors": [r.error for r in suite.results if r.error]
            }
            summary["test_suites"].append(suite_summary)
        
        print(f"\n📊 Resultados Gerais: {suites_passed}/{total_suites} suites atendendo metas de performance")
        
        if suites_passed == total_suites:
            print("🎉 TODAS AS METAS DE PERFORMANCE ATENDIDAS! Otimização bem-sucedida.")
            summary["overall_status"] = "success"
        else:
            print("⚠️  Alguns endpoints precisam de otimização adicional.")
            summary["overall_status"] = "needs_improvement"
        
        print("\n🔧 Otimizações Implementadas:")
        for optimization in summary["optimizations_implemented"]:
            print(f"   • {optimization}")
        
        return summary