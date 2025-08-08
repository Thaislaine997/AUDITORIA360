#!/usr/bin/env python3
"""
🧪 DEMO SCRIPT - NOT FOR PRODUCTION USE 🧪

AUDITORIA360 - First Stage Integration Example
Demonstrates the unified reporting system with dashboard integration

⚠️  WARNING: This is a demonstration script only.
⚠️  DO NOT use in production environments.
⚠️  For production deployment, use the main application in src/

This script shows how the first stage components work together:
1. Generate unified reports
2. Display dashboard with graphics
3. Export results in multiple formats

Melhorias da refatoração:
- Configuração centralizada
- Tratamento de erros aprimorado
- Logging estruturado
- Validação de pré-requisitos
- Melhor modularidade
"""

import logging
import sys
from pathlib import Path
from typing import Any, List

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from config import demo_config
except ImportError:
    # Fallback config if module not available
    class MockDemoConfig:
        @property
        def report_config(self):
            return {
                "output_dir": "./demo_reports",
                "include_charts": True,
                "max_recommendations": 3,
            }

        @property
        def ui_config(self):
            return {
                "success_icon": "✅",
                "error_icon": "❌",
                "separator": "=" * 60,
                "sub_separator": "-" * 40,
            }

        def ensure_output_dir(self):
            Path("./demo_reports").mkdir(parents=True, exist_ok=True)

        def get_troubleshooting_steps(self):
            return [
                "Make sure you're in the project root directory",
                "Check that all dependencies are installed",
                "Verify file permissions",
            ]

    demo_config = MockDemoConfig()

try:
    from services.reporting import ReportFormat, ReportType, UnifiedReportGenerator

    REPORTING_AVAILABLE = True
except ImportError:
    REPORTING_AVAILABLE = False

    # Mock classes for when reporting module is not available
    class ReportFormat:
        JSON = "JSON"

    class ReportType:
        DAILY = "DAILY"
        WEEKLY = "WEEKLY"
        MONTHLY = "MONTHLY"

    class UnifiedReportGenerator:
        def __init__(self, output_dir):
            self.output_dir = output_dir

        def generate_unified_report(
            self, report_type, include_charts=True, format_output="JSON"
        ):
            # Mock report object
            from datetime import datetime, timedelta

            class MockReport:
                def __init__(self, report_type):
                    self.id = f"mock-{report_type.lower()}-{datetime.now().strftime('%Y%m%d')}"
                    self.title = f"{report_type.title()} Report"
                    self.period_start = datetime.now() - timedelta(days=1)
                    self.period_end = datetime.now()
                    self.metrics = type(
                        "Metrics", (), {"total_audits": 42, "compliance_score": 85}
                    )()
                    self.charts_data = {
                        "compliance_chart": {
                            "config": {"type": "bar", "title": "Compliance Score"},
                            "data": {
                                "labels": ["Q1", "Q2", "Q3"],
                                "values": [80, 85, 90],
                            },
                        }
                    }
                    self.recommendations = [
                        {
                            "title": "Improve documentation",
                            "priority": "high",
                            "category": "compliance",
                            "description": "Update audit procedures",
                        },
                        {
                            "title": "Enhance monitoring",
                            "priority": "medium",
                            "category": "operations",
                            "description": "Add real-time alerts",
                        },
                    ]

            return MockReport(report_type)


# Configure logging with better format
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

try:

    def validate_prerequisites() -> bool:
        """
        Valida pré-requisitos para execução da demonstração.

        Returns:
            bool: True se todos os pré-requisitos estão atendidos
        """
        ui = demo_config.ui_config
        logger.info("Validando pré-requisitos para demo first stage")

        try:
            # Ensure output directory exists
            demo_config.ensure_output_dir()

            # Check Python version
            if sys.version_info < (3, 8):
                print(f"{ui['error_icon']} Python 3.8+ é necessário")
                return False

            # Check if reporting module is available
            if not REPORTING_AVAILABLE:
                logger.warning("Módulo de relatórios não disponível - usando simulação")
                print(
                    f"{ui['warning_icon']} Módulo de relatórios não disponível - usando modo simulação"
                )

            logger.info("Pré-requisitos validados com sucesso")
            return True

        except Exception as e:
            logger.error(f"Falha na validação de pré-requisitos: {e}")
            print(f"{ui['error_icon']} Erro na validação: {e}")
            return False

    def generate_reports_safely() -> List[Any]:
        """
        Gera relatórios com tratamento de erros robusto.

        Returns:
            List[Any]: Lista de relatórios gerados
        """
        ui = demo_config.ui_config
        config = demo_config.report_config
        reports = []

        try:
            # Initialize report generator with config
            generator = UnifiedReportGenerator(output_dir=config["output_dir"])

            report_types = [
                (ReportType.DAILY, "📅", "daily"),
                (ReportType.WEEKLY, "📆", "weekly"),
                (ReportType.MONTHLY, "📊", "monthly"),
            ]

            for report_type, icon, name in report_types:
                try:
                    print(f"   {icon} Generating {name} report...")
                    logger.info(f"Gerando relatório {name}")

                    report = generator.generate_unified_report(
                        report_type,
                        include_charts=config["include_charts"],
                        format_output=ReportFormat.JSON,
                    )
                    reports.append(report)

                    logger.info(f"Relatório {name} gerado com sucesso: {report.id}")

                except Exception as e:
                    logger.error(f"Erro ao gerar relatório {name}: {e}")
                    print(f"   {ui['error_icon']} Falha ao gerar relatório {name}: {e}")
                    # Continue with other reports

            return reports

        except Exception as e:
            logger.error(f"Erro crítico na geração de relatórios: {e}")
            print(f"{ui['error_icon']} Erro crítico: {e}")
            return []

    def display_report_summary(reports: List[Any]) -> None:
        """
        Exibe resumo dos relatórios com tratamento de erros.

        Args:
            reports: Lista de relatórios para exibir
        """
        ui = demo_config.ui_config

        if not reports:
            print(f"\n{ui['error_icon']} Nenhum relatório foi gerado")
            return

        print("\n📋 2. Report Summary:")
        print(ui["sub_separator"])

        for report in reports:
            try:
                print(f"   📊 {report.title}")
                print(f"      ID: {report.id}")
                print(
                    f"      Period: {report.period_start.strftime('%Y-%m-%d')} to {report.period_end.strftime('%Y-%m-%d')}"
                )
                print(
                    f"      Metrics: {report.metrics.total_audits} audits, {report.metrics.compliance_score}% compliance"
                )
                print(f"      Charts: {len(report.charts_data)} visualizations")
                print(f"      Recommendations: {len(report.recommendations)} items")
                print()

            except Exception as e:
                logger.error(
                    f"Erro ao exibir relatório {getattr(report, 'id', 'unknown')}: {e}"
                )
                print(f"   {ui['error_icon']} Erro ao exibir relatório: {e}")

    def display_chart_structure(reports: List[Any]) -> None:
        """
        Exibe estrutura de dados dos gráficos.

        Args:
            reports: Lista de relatórios
        """
        ui = demo_config.ui_config

        if not reports:
            return

        print("📈 3. Chart Data Structure Example:")
        print(ui["sub_separator"])

        try:
            sample_report = reports[0]  # Use daily report
            for chart_name, chart_data in sample_report.charts_data.items():
                print(f"   📊 {chart_name}:")
                print(f"      Type: {chart_data['config']['type']}")
                print(f"      Title: {chart_data['config']['title']}")
                if "data" in chart_data and "labels" in chart_data["data"]:
                    print(f"      Data points: {len(chart_data['data']['labels'])}")
                print()

        except Exception as e:
            logger.error(f"Erro ao exibir estrutura de gráficos: {e}")
            print(f"   {ui['error_icon']} Erro ao exibir gráficos: {e}")

    def display_recommendations(reports: List[Any]) -> None:
        """
        Exibe recomendações dos relatórios.

        Args:
            reports: Lista de relatórios
        """
        ui = demo_config.ui_config
        config = demo_config.report_config

        if not reports:
            return

        print("💡 4. Sample Recommendations:")
        print(ui["sub_separator"])

        try:
            sample_report = reports[0]
            max_recommendations = config.get("max_recommendations", 3)

            for i, rec in enumerate(
                sample_report.recommendations[:max_recommendations], 1
            ):
                print(f"   {i}. {rec['title']} ({rec['priority']} priority)")
                print(f"      Category: {rec['category']}")
                print(f"      Description: {rec['description']}")
                print()

        except Exception as e:
            logger.error(f"Erro ao exibir recomendações: {e}")
            print(f"   {ui['error_icon']} Erro ao exibir recomendações: {e}")

    def demo_first_stage():
        """
        Demonstra implementação do primeiro estágio com tratamento de erros aprimorado.

        Returns:
            List[Any]: Relatórios gerados ou lista vazia em caso de erro
        """
        ui = demo_config.ui_config
        logger.info("Iniciando demonstração first stage")

        print("🚀 AUDITORIA360 - First Stage Implementation Demo")
        print(ui["separator"])

        # Validate prerequisites first
        if not validate_prerequisites():
            return []

        print("\n📊 1. Generating Unified Reports...")

        # Generate reports with error handling
        reports = generate_reports_safely()

        if reports:
            print(
                f"\n{ui['success_icon']} Generated {len(reports)} reports successfully!"
            )

            # Display report information
            display_report_summary(reports)
            display_chart_structure(reports)
            display_recommendations(reports)
        else:
            print(f"\n{ui['error_icon']} Failed to generate reports")
            return []

        # Display benefits and next steps
        print("🎯 5. First Stage Benefits Achieved:")
        print(ui["sub_separator"])
        print("   ✅ Centralized documentation structure (docs/documentos/)")
        print("   ✅ Unified reporting system with graphics")
        print("   ✅ Enhanced dashboard with interactive charts")
        print("   ✅ Modular architecture for future PRs")
        print("   ✅ Performance-optimized data structures")
        print("   ✅ Standardized report formats and APIs")
        print()

        print("🚀 6. Next PR Preparation:")
        print(ui["sub_separator"])
        print("   📝 PR #2: Complete database integration")
        print("   📈 PR #3: Advanced dashboard analytics")
        print("   ⚡ PR #4: Performance optimization & caching")
        print("   🤖 PR #5: ML/AI integration")
        print()

        print("✨ First Stage Implementation: COMPLETED")
        print(ui["separator"])

        logger.info("Demonstração first stage concluída com sucesso")
        return reports

    def show_file_structure():
        """Show the file structure created in first stage"""
        print("\n📁 First Stage File Structure:")
        print("-" * 40)

        structure = {
            "docs/documentos/": [
                "README.md (Documentation index)",
                "relatorios/relatorio-unificado.md",
                "relatorios/status-implementacao.md",
                "arquitetura/visao-geral.md",
                "apis/api-documentation.md",
                "manuais/ (prepared)",
                "compliance/ (prepared)",
                "instalacao/ (prepared)",
                "templates/ (prepared)",
            ],
            "services/reporting/": [
                "__init__.py (Package definition)",
                "unified_reports.py (Main implementation)",
            ],
            "dashboards/": ["enhanced_dashboard.py (Improved Streamlit app)"],
        }

        for folder, files in structure.items():
            print(f"   📂 {folder}")
            for file in files:
                print(f"      📄 {file}")
            print()

    if __name__ == "__main__":
        try:
            ui = demo_config.ui_config

            # Run the demo
            reports = demo_first_stage()

            # Show file structure
            show_file_structure()

            if reports:
                print("🎉 Demo completed successfully!")
                print("\nTo run the enhanced dashboard:")
                print("   streamlit run dashboards/enhanced_dashboard.py")
                print("\nTo generate reports programmatically:")
                print("   python services/reporting/unified_reports.py")
                exit_code = 0
            else:
                print("⚠️  Demo completed with warnings - check logs")
                exit_code = 1

            sys.exit(exit_code)

        except KeyboardInterrupt:
            print("\n🛑 Demo interrupted by user")
            logger.info("Demo interrupted by user")
            sys.exit(130)

        except Exception as e:
            ui = demo_config.ui_config
            logger.error(f"Demo failed: {e}", exc_info=True)
            print(f"\n{ui['error_icon']} Error: {e}")

            print("\n🔧 Troubleshooting:")
            for i, step in enumerate(demo_config.get_troubleshooting_steps(), 1):
                print(f"   {i}. {step}")

            sys.exit(2)

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\n🔧 Setup Instructions:")
    print("1. Make sure you're in the AUDITORIA360 project root")
    print("2. Install required dependencies:")
    print("   pip install streamlit plotly pandas")
    print("3. Run this demo again")
    sys.exit(3)
