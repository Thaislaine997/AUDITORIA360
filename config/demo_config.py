"""
Configuração para scripts de demonstração do AUDITORIA360.
Centraliza valores configuráveis para melhorar modularidade.
"""

from pathlib import Path
from typing import Any, Dict


class DemoConfig:
    """Configuração centralizada para scripts de demonstração."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.output_dir = self.project_root / "demo_reports"

    @property
    def report_config(self) -> Dict[str, Any]:
        """Configurações para geração de relatórios."""
        return {
            "output_dir": str(self.output_dir),
            "include_charts": True,
            "default_format": "JSON",
            "max_recommendations": 3,
        }

    @property
    def demo_data(self) -> Dict[str, Any]:
        """Dados de exemplo para demonstrações."""
        return {
            "sample_cpf": "123.456.789-09",
            "sample_email": "test@example.com",
            "demo_user": "demo",
            "test_file": "test.pdf",
            "test_bucket": "test-bucket",
        }

    @property
    def ui_config(self) -> Dict[str, str]:
        """Configurações de interface do usuário."""
        return {
            "success_icon": "✅",
            "error_icon": "❌",
            "info_icon": "📊",
            "warning_icon": "⚠️",
            "separator": "=" * 60,
            "sub_separator": "-" * 40,
        }

    def ensure_output_dir(self) -> None:
        """Garante que o diretório de saída existe."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_troubleshooting_steps(self) -> list:
        """Retorna passos de solução de problemas."""
        return [
            "Make sure you're in the project root directory",
            "Check that all dependencies are installed",
            "Verify file permissions",
            "Ensure services are running correctly",
            "Check network connectivity if needed",
        ]

    def get_setup_instructions(self) -> list:
        """Retorna instruções de configuração."""
        return [
            "Make sure you're in the AUDITORIA360 project root",
            "Install required dependencies:",
            "   pip install streamlit plotly pandas",
            "Run this demo again",
        ]


# Instância global para reutilização
demo_config = DemoConfig()
