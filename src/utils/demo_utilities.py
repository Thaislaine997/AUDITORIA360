"""
Utilitários de demonstração modularizados.
Extrai e organiza as funções de demonstração do demo_first_stage.py principal.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ReportGeneratorDemo:
    """Demonstra o sistema de geração de relatórios unificados."""
    
    def __init__(self, output_dir: str = "./demo_reports"):
        self.output_dir = output_dir
        self.reports = []
    
    def generate_demo_reports(self) -> List[Dict[str, Any]]:
        """
        Gera relatórios de demonstração.
        
        Returns:
            list: Lista de relatórios gerados
        """
        try:
            # Tentativa de importar sistema de relatórios
            from services.reporting import UnifiedReportGenerator, ReportType, ReportFormat
            
            print("📊 1. Gerando Relatórios Unificados...")
            
            # Inicializar gerador de relatórios
            generator = UnifiedReportGenerator(output_dir=self.output_dir)
            
            # Gerar diferentes tipos de relatórios
            report_configs = [
                {
                    "type": ReportType.DAILY,
                    "name": "Relatório Diário",
                    "icon": "📅"
                },
                {
                    "type": ReportType.WEEKLY,
                    "name": "Relatório Semanal",
                    "icon": "📆"
                },
                {
                    "type": ReportType.MONTHLY,
                    "name": "Relatório Mensal",
                    "icon": "📊"
                }
            ]
            
            for config in report_configs:
                print(f"   {config['icon']} Gerando {config['name'].lower()}...")
                try:
                    report = generator.generate_unified_report(
                        config["type"],
                        include_charts=True,
                        format_output=ReportFormat.JSON
                    )
                    self.reports.append(report)
                    logger.info(f"Relatório {config['name']} gerado com sucesso")
                except Exception as e:
                    logger.error(f"Erro ao gerar {config['name']}: {e}")
                    # Criar relatório simulado em caso de erro
                    self.reports.append(self._create_mock_report(config["type"], config["name"]))
            
            print(f"\n✅ Gerados {len(self.reports)} relatórios com sucesso!")
            return self.reports
            
        except ImportError as e:
            logger.warning(f"Sistema de relatórios não disponível: {e}")
            print("⚠️  Sistema de relatórios não disponível - criando relatórios simulados")
            return self._create_mock_reports()
        except Exception as e:
            logger.error(f"Erro ao gerar relatórios de demonstração: {e}")
            print(f"❌ Erro ao gerar relatórios: {e}")
            return []
    
    def _create_mock_report(self, report_type: str, name: str) -> Dict[str, Any]:
        """Cria um relatório simulado para demonstração."""
        return {
            "id": f"demo_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": name,
            "type": report_type,
            "period_start": datetime.now() - timedelta(days=7),
            "period_end": datetime.now(),
            "metrics": {
                "total_audits": 150,
                "compliance_score": 94.5,
                "issues_found": 12,
                "recommendations": 8
            },
            "charts_data": {
                "compliance_trend": {
                    "config": {
                        "type": "line",
                        "title": "Trend de Compliance"
                    },
                    "data": {
                        "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
                        "datasets": [{"data": [92, 94, 91, 95, 94]}]
                    }
                },
                "audit_distribution": {
                    "config": {
                        "type": "pie", 
                        "title": "Distribuição de Auditorias"
                    },
                    "data": {
                        "labels": ["Completas", "Pendentes", "Em Progresso"],
                        "datasets": [{"data": [70, 20, 10]}]
                    }
                }
            },
            "recommendations": [
                {
                    "title": "Melhorar documentação de processos",
                    "priority": "high",
                    "category": "documentation",
                    "description": "Atualizar documentação de processos críticos"
                },
                {
                    "title": "Implementar controles adicionais",
                    "priority": "medium",
                    "category": "controls",
                    "description": "Adicionar controles automatizados"
                }
            ],
            "generated_at": datetime.now(),
            "status": "completed"
        }
    
    def _create_mock_reports(self) -> List[Dict[str, Any]]:
        """Cria relatórios simulados quando o sistema real não está disponível."""
        mock_types = [
            ("daily", "Relatório Diário"),
            ("weekly", "Relatório Semanal"),
            ("monthly", "Relatório Mensal")
        ]
        
        reports = []
        for report_type, name in mock_types:
            reports.append(self._create_mock_report(report_type, name))
        
        return reports


class ReportDisplayManager:
    """Gerencia a exibição de relatórios na demonstração."""
    
    def __init__(self):
        pass
    
    def display_report_summary(self, reports: List[Dict[str, Any]]) -> None:
        """
        Exibe resumo dos relatórios gerados.
        
        Args:
            reports: Lista de relatórios para exibir
        """
        if not reports:
            print("⚠️  Nenhum relatório disponível para exibir")
            return
        
        print("\n📋 2. Resumo dos Relatórios:")
        print("-" * 40)
        
        for report in reports:
            try:
                print(f"   📊 {report.get('title', 'Relatório')}")
                print(f"      ID: {report.get('id', 'N/A')}")
                
                # Formatação de período
                period_start = report.get('period_start')
                period_end = report.get('period_end')
                
                if period_start and period_end:
                    if hasattr(period_start, 'strftime'):
                        start_str = period_start.strftime('%Y-%m-%d')
                    else:
                        start_str = str(period_start)
                    
                    if hasattr(period_end, 'strftime'):
                        end_str = period_end.strftime('%Y-%m-%d')
                    else:
                        end_str = str(period_end)
                    
                    print(f"      Período: {start_str} to {end_str}")
                
                # Métricas
                metrics = report.get('metrics', {})
                if metrics:
                    total_audits = metrics.get('total_audits', 0)
                    compliance_score = metrics.get('compliance_score', 0)
                    print(f"      Métricas: {total_audits} auditorias, {compliance_score}% compliance")
                
                # Charts
                charts_data = report.get('charts_data', {})
                print(f"      Gráficos: {len(charts_data)} visualizações")
                
                # Recomendações
                recommendations = report.get('recommendations', [])
                print(f"      Recomendações: {len(recommendations)} itens")
                print()
                
            except Exception as e:
                logger.error(f"Erro ao exibir relatório: {e}")
                print(f"      ❌ Erro ao exibir este relatório: {e}")
    
    def display_chart_structure(self, reports: List[Dict[str, Any]]) -> None:
        """
        Exibe estrutura dos gráficos do primeiro relatório.
        
        Args:
            reports: Lista de relatórios
        """
        if not reports:
            return
        
        print("📈 3. Estrutura dos Dados de Gráfico (Exemplo):")
        print("-" * 40)
        
        try:
            sample_report = reports[0]  # Usar primeiro relatório
            charts_data = sample_report.get('charts_data', {})
            
            for chart_name, chart_data in charts_data.items():
                print(f"   📊 {chart_name}:")
                
                config = chart_data.get('config', {})
                print(f"      Tipo: {config.get('type', 'N/A')}")
                print(f"      Título: {config.get('title', 'N/A')}")
                
                data = chart_data.get('data', {})
                labels = data.get('labels', [])
                if labels:
                    print(f"      Pontos de dados: {len(labels)}")
                print()
                
        except Exception as e:
            logger.error(f"Erro ao exibir estrutura de gráficos: {e}")
            print(f"   ❌ Erro ao exibir estrutura de gráficos: {e}")
    
    def display_recommendations(self, reports: List[Dict[str, Any]], max_recommendations: int = 3) -> None:
        """
        Exibe recomendações do primeiro relatório.
        
        Args:
            reports: Lista de relatórios
            max_recommendations: Número máximo de recomendações para exibir
        """
        if not reports:
            return
        
        print("💡 4. Recomendações de Exemplo:")
        print("-" * 40)
        
        try:
            sample_report = reports[0]
            recommendations = sample_report.get('recommendations', [])
            
            for i, rec in enumerate(recommendations[:max_recommendations], 1):
                title = rec.get('title', 'Recomendação sem título')
                priority = rec.get('priority', 'unknown')
                category = rec.get('category', 'general')
                description = rec.get('description', 'Sem descrição')
                
                print(f"   {i}. {title} ({priority} priority)")
                print(f"      Categoria: {category}")
                print(f"      Descrição: {description}")
                print()
                
        except Exception as e:
            logger.error(f"Erro ao exibir recomendações: {e}")
            print(f"   ❌ Erro ao exibir recomendações: {e}")


class BenefitsPresenter:
    """Apresenta os benefícios alcançados na primeira etapa."""
    
    def __init__(self):
        pass
    
    def show_first_stage_benefits(self) -> None:
        """Exibe os benefícios alcançados na primeira etapa."""
        print("🎯 5. Benefícios da Primeira Etapa Alcançados:")
        print("-" * 40)
        
        benefits = [
            "✅ Estrutura de documentação centralizada (docs/documentos/)",
            "✅ Sistema de relatórios unificado com gráficos",
            "✅ Dashboard aprimorado com gráficos interativos",
            "✅ Arquitetura modular para futuros PRs",
            "✅ Estruturas de dados otimizadas para performance",
            "✅ Formatos e APIs de relatórios padronizados"
        ]
        
        for benefit in benefits:
            print(f"   {benefit}")
        print()
    
    def show_next_pr_preparation(self) -> None:
        """Exibe preparação para os próximos PRs."""
        print("🚀 6. Preparação para Próximos PRs:")
        print("-" * 40)
        
        next_prs = [
            "📝 PR #2: Integração completa com banco de dados",
            "📈 PR #3: Analytics avançados do dashboard",
            "⚡ PR #4: Otimização de performance e cache",
            "🤖 PR #5: Integração ML/AI"
        ]
        
        for pr in next_prs:
            print(f"   {pr}")
        print()


class FileStructurePresenter:
    """Apresenta a estrutura de arquivos criada na primeira etapa."""
    
    def __init__(self):
        pass
    
    def show_file_structure(self) -> None:
        """Exibe a estrutura de arquivos criada na primeira etapa."""
        print("\n📁 Estrutura de Arquivos da Primeira Etapa:")
        print("-" * 40)
        
        structure = {
            "docs/documentos/": [
                "README.md (Índice da documentação)",
                "relatorios/relatorio-unificado.md",
                "relatorios/status-implementacao.md", 
                "arquitetura/visao-geral.md",
                "apis/api-documentation.md",
                "manuais/ (preparado)",
                "compliance/ (preparado)",
                "instalacao/ (preparado)",
                "templates/ (preparado)"
            ],
            "services/reporting/": [
                "__init__.py (Definição do pacote)",
                "unified_reports.py (Implementação principal)"
            ],
            "src/utils/": [
                "config_validator.py (Validação de configuração)",
                "system_monitor.py (Monitoramento do sistema)",
                "demo_utilities.py (Utilitários de demonstração)"
            ],
            "dashboards/": [
                "enhanced_dashboard.py (App Streamlit melhorado)"
            ]
        }
        
        for folder, files in structure.items():
            print(f"   📂 {folder}")
            for file in files:
                print(f"      📄 {file}")
            print()


class DemoOrchestrator:
    """Orquestra toda a demonstração da primeira etapa."""
    
    def __init__(self, output_dir: str = "./demo_reports"):
        self.report_generator = ReportGeneratorDemo(output_dir)
        self.display_manager = ReportDisplayManager()
        self.benefits_presenter = BenefitsPresenter()
        self.file_structure_presenter = FileStructurePresenter()
    
    def run_complete_demo(self) -> Dict[str, Any]:
        """
        Executa a demonstração completa da primeira etapa.
        
        Returns:
            dict: Resultado da demonstração
        """
        print("🚀 AUDITORIA360 - Demonstração da Implementação da Primeira Etapa")
        print("=" * 60)
        
        demo_result = {
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "reports_generated": 0,
            "errors": []
        }
        
        try:
            # 1. Gerar relatórios
            reports = self.report_generator.generate_demo_reports()
            demo_result["reports_generated"] = len(reports)
            
            # 2. Exibir resumo dos relatórios
            self.display_manager.display_report_summary(reports)
            
            # 3. Exibir estrutura dos gráficos
            self.display_manager.display_chart_structure(reports)
            
            # 4. Exibir recomendações
            self.display_manager.display_recommendations(reports)
            
            # 5. Exibir benefícios alcançados
            self.benefits_presenter.show_first_stage_benefits()
            
            # 6. Exibir preparação para próximos PRs
            self.benefits_presenter.show_next_pr_preparation()
            
            # 7. Mostrar estrutura de arquivos
            self.file_structure_presenter.show_file_structure()
            
            print("✨ Implementação da Primeira Etapa: CONCLUÍDA")
            print("=" * 60)
            
            demo_result["completion_message"] = "Demonstração executada com sucesso"
            
        except Exception as e:
            logger.error(f"Erro durante demonstração: {e}")
            demo_result["status"] = "error"
            demo_result["errors"].append(str(e))
            print(f"❌ Erro durante demonstração: {e}")
        
        return demo_result
    
    def show_usage_instructions(self) -> None:
        """Exibe instruções de uso."""
        print("\n🎉 Demonstração concluída com sucesso!")
        print("\nPara executar o dashboard aprimorado:")
        print("   streamlit run dashboards/enhanced_dashboard.py")
        print("\nPara gerar relatórios programaticamente:")
        print("   python services/reporting/unified_reports.py")
        print("\nPara executar o monitoramento do sistema:")
        print("   python -m src.utils.system_monitor")
        print("\nPara validar configuração:")
        print("   python -m src.utils.config_validator")