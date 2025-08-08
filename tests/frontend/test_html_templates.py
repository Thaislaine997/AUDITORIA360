"""
Frontend Template Tests
Testes para validar estrutura e conteúdo dos templates HTML
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


class TestHTMLTemplates:
    """Testes para templates HTML"""

    def get_template_path(self, template_name):
        """Obtém o caminho para um template"""
        base_path = Path(__file__).parent.parent.parent
        return base_path / "templates" / "components" / template_name

    def load_template(self, template_name):
        """Carrega um template HTML"""
        template_path = self.get_template_path(template_name)
        if not template_path.exists():
            pytest.skip(f"Template {template_name} não encontrado")

        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_navigation_template_structure(self):
        """Testa a estrutura básica do template de navegação"""
        content = self.load_template("navigation.html")
        soup = BeautifulSoup(content, "html.parser")

        # Verifica se existe elemento nav
        nav = soup.find("nav")
        assert nav is not None, "Template deve conter elemento <nav>"

        # Verifica se tem classe main-navigation
        assert "main-navigation" in nav.get(
            "class", []
        ), "Nav deve ter classe main-navigation"

        # Verifica atributos de acessibilidade
        assert nav.get("role") == "navigation", "Nav deve ter role='navigation'"
        assert nav.get("aria-label") is not None, "Nav deve ter aria-label"

    def test_navigation_template_handlebars_syntax(self):
        """Testa se o template usa sintaxe Handlebars correta"""
        content = self.load_template("navigation.html")

        # Verifica condicionais Handlebars
        assert (
            "{{#if navigationTitle}}" in content
        ), "Template deve usar condicional para título"
        assert (
            "{{#if navigationItems}}" in content
        ), "Template deve usar condicional para itens"
        assert (
            "{{#each navigationItems}}" in content
        ), "Template deve usar loop para itens"

        # Verifica variáveis
        assert "{{url}}" in content, "Template deve usar variável url"
        assert "{{text}}" in content, "Template deve usar variável text"

    def test_header_template_exists(self):
        """Testa se o template de header existe e tem estrutura básica"""
        content = self.load_template("header.html")
        soup = BeautifulSoup(content, "html.parser")

        # Verifica se não está vazio
        assert content.strip() != "", "Template header não deve estar vazio"

    def test_footer_template_exists(self):
        """Testa se o template de footer existe e tem estrutura básica"""
        content = self.load_template("footer.html")
        soup = BeautifulSoup(content, "html.parser")

        # Verifica se não está vazio
        assert content.strip() != "", "Template footer não deve estar vazio"

    def test_status_indicator_template(self):
        """Testa o template de indicador de status"""
        content = self.load_template("status-indicator.html")
        soup = BeautifulSoup(content, "html.parser")

        # Verifica se tem estrutura básica
        assert content.strip() != "", "Template status-indicator não deve estar vazio"

    def test_metric_card_template(self):
        """Testa o template de cartão de métrica"""
        content = self.load_template("metric-card.html")
        soup = BeautifulSoup(content, "html.parser")

        # Verifica se tem estrutura básica
        assert content.strip() != "", "Template metric-card não deve estar vazio"

    def test_alert_container_template(self):
        """Testa o template de container de alertas"""
        content = self.load_template("alert-container.html")
        soup = BeautifulSoup(content, "html.parser")

        # Verifica se tem estrutura básica
        assert content.strip() != "", "Template alert-container não deve estar vazio"


class TestTemplateAccessibility:
    """Testes de acessibilidade para templates"""

    def get_template_path(self, template_name):
        """Obtém o caminho para um template"""
        base_path = Path(__file__).parent.parent.parent
        return base_path / "templates" / "components" / template_name

    def load_template(self, template_name):
        """Carrega um template HTML"""
        template_path = self.get_template_path(template_name)
        if not template_path.exists():
            pytest.skip(f"Template {template_name} não encontrado")

        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def test_navigation_accessibility(self):
        """Testa acessibilidade do template de navegação"""
        content = self.load_template("navigation.html")
        soup = BeautifulSoup(content, "html.parser")

        nav = soup.find("nav")
        if nav:
            # Verifica atributos ARIA
            assert nav.get("role") == "navigation"
            assert nav.get("aria-label") is not None

            # Verifica se listas têm role="list"
            lists = soup.find_all("ul")
            for ul in lists:
                if "navigation-list" in ul.get("class", []):
                    assert ul.get("role") == "list"


class TestTemplateIntegration:
    """Testes de integração dos templates"""

    def test_all_templates_exist(self):
        """Verifica se todos os templates esperados existem"""
        base_path = Path(__file__).parent.parent.parent / "templates" / "components"

        expected_templates = [
            "navigation.html",
            "header.html",
            "footer.html",
            "status-indicator.html",
            "metric-card.html",
            "alert-container.html",
        ]

        for template in expected_templates:
            template_path = base_path / template
            assert template_path.exists(), f"Template {template} deve existir"

    def test_template_encoding(self):
        """Verifica se templates usam codificação UTF-8"""
        base_path = Path(__file__).parent.parent.parent / "templates" / "components"

        for template_file in base_path.glob("*.html"):
            try:
                with open(template_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Se chegou até aqui, a codificação está correta
                    assert len(content) >= 0
            except UnicodeDecodeError:
                pytest.fail(f"Template {template_file.name} não está em UTF-8")
