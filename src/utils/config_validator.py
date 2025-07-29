"""
Módulo de validação de configuração refatorado.
Extrai e organiza as funções de validação do validate_config.py principal.
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import configparser
import logging

logger = logging.getLogger(__name__)

class ColorOutput:
    """Gerencia códigos de cores para saída do console."""
    
    def __init__(self):
        self.colors = {
            'GREEN': '\033[0;32m',
            'RED': '\033[0;31m',
            'YELLOW': '\033[1;33m',
            'BLUE': '\033[0;34m',
            'NC': '\033[0m'  # No Color
        }
    
    def print_status(self, message: str, status: str = 'info') -> None:
        """Imprime mensagens de status coloridas."""
        try:
            if status == 'success':
                print(f"{self.colors['GREEN']}✅ {message}{self.colors['NC']}")
            elif status == 'error':
                print(f"{self.colors['RED']}❌ {message}{self.colors['NC']}")
            elif status == 'warning':
                print(f"{self.colors['YELLOW']}⚠️  {message}{self.colors['NC']}")
            else:
                print(f"{self.colors['BLUE']}ℹ️  {message}{self.colors['NC']}")
        except Exception as e:
            logger.warning(f"Erro ao imprimir status colorido: {e}")
            print(f"[{status.upper()}] {message}")


class FileValidator:
    """Valida existência e permissões de arquivos."""
    
    def __init__(self, color_output: ColorOutput):
        self.color_output = color_output
    
    def check_file_exists(self, filepath: str, description: str) -> bool:
        """Verifica se um arquivo existe e imprime status."""
        try:
            if Path(filepath).exists():
                self.color_output.print_status(f"{description}: {filepath}", 'success')
                return True
            else:
                self.color_output.print_status(f"{description} não encontrado: {filepath}", 'error')
                return False
        except Exception as e:
            logger.error(f"Erro ao verificar arquivo {filepath}: {e}")
            self.color_output.print_status(f"Erro ao verificar {description}: {e}", 'error')
            return False
    
    def check_executable_permission(self, filepath: str) -> bool:
        """Verifica se um arquivo tem permissão de execução."""
        try:
            script_path = Path(filepath)
            if script_path.exists():
                if os.access(script_path, os.X_OK):
                    self.color_output.print_status(f"Script {filepath} é executável", 'success')
                    return True
                else:
                    self.color_output.print_status(
                        f"Script {filepath} não é executável (execute: chmod +x {filepath})", 
                        'warning'
                    )
                    return False
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar permissões de {filepath}: {e}")
            return False


class DependencyValidator:
    """Valida dependências Python."""
    
    def __init__(self, color_output: ColorOutput):
        self.color_output = color_output
    
    def check_python_dependencies(self, required_deps: List[str]) -> bool:
        """Verifica se as dependências Python requeridas estão disponíveis."""
        self.color_output.print_status("Verificando dependências Python...")
        all_available = True
        
        for dep in required_deps:
            try:
                if importlib.util.find_spec(dep) is not None:
                    self.color_output.print_status(f"Dependência {dep} disponível", 'success')
                else:
                    self.color_output.print_status(f"Dependência {dep} não encontrada", 'error')
                    all_available = False
            except Exception as e:
                logger.error(f"Erro ao verificar dependência {dep}: {e}")
                self.color_output.print_status(f"Erro ao verificar {dep}: {e}", 'error')
                all_available = False
        
        return all_available


class StreamlitConfigValidator:
    """Valida configurações específicas do Streamlit."""
    
    def __init__(self, color_output: ColorOutput, file_validator: FileValidator):
        self.color_output = color_output
        self.file_validator = file_validator
    
    def validate_streamlit_config(self) -> bool:
        """Valida arquivos de configuração do Streamlit."""
        config_file = '.streamlit/config.toml'
        secrets_file = '.streamlit/secrets.toml'
        
        self.color_output.print_status("Validando configuração do Streamlit...")
        
        # Verifica config.toml
        if not self.file_validator.check_file_exists(config_file, "Configuração Streamlit"):
            return False
        
        # Verifica secrets.toml
        if not self.file_validator.check_file_exists(secrets_file, "Secrets Streamlit"):
            return False
        
        # Valida conteúdo do config.toml
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '[theme]' in content:
                    self.color_output.print_status("Tema configurado corretamente", 'success')
                else:
                    self.color_output.print_status("Configuração de tema não encontrada", 'warning')
        except Exception as e:
            logger.error(f"Erro ao ler {config_file}: {e}")
            self.color_output.print_status(f"Erro ao ler {config_file}: {e}", 'error')
            return False
        
        return True


class DashboardValidator:
    """Valida estrutura dos dashboards."""
    
    def __init__(self, color_output: ColorOutput, file_validator: FileValidator):
        self.color_output = color_output
        self.file_validator = file_validator
    
    def validate_dashboard_structure(self) -> bool:
        """Valida a estrutura dos dashboards."""
        self.color_output.print_status("Validando estrutura dos dashboards...")
        
        required_files = [
            'dashboards/app.py',
            'dashboards/requirements.txt',
            'dashboards/api_client.py',
            'dashboards/DEPLOY_README.md'
        ]
        
        all_present = True
        for file in required_files:
            if not self.file_validator.check_file_exists(file, "Arquivo dashboard"):
                all_present = False
        
        # Verifica diretório de páginas
        pages_dir = Path('dashboards/pages')
        try:
            if pages_dir.exists():
                page_files = list(pages_dir.glob('*.py'))
                self.color_output.print_status(f"Páginas encontradas: {len(page_files)}", 'success')
            else:
                self.color_output.print_status("Diretório de páginas não encontrado", 'warning')
        except Exception as e:
            logger.error(f"Erro ao verificar diretório de páginas: {e}")
            self.color_output.print_status(f"Erro ao verificar páginas: {e}", 'error')
        
        return all_present


class EnvironmentValidator:
    """Valida configurações de ambiente."""
    
    def __init__(self, color_output: ColorOutput, file_validator: FileValidator):
        self.color_output = color_output
        self.file_validator = file_validator
    
    def validate_environment_config(self) -> bool:
        """Valida configuração de ambiente."""
        self.color_output.print_status("Validando configuração de ambiente...")
        
        env_files = ['.env.production', '.env.cloudsql']
        
        for env_file in env_files:
            self.file_validator.check_file_exists(env_file, "Arquivo de ambiente")
        
        # Verifica variáveis críticas no .env.production
        if Path('.env.production').exists():
            try:
                with open('.env.production', 'r', encoding='utf-8') as f:
                    content = f.read()
                    critical_vars = [
                        'ENVIRONMENT=production',
                        'API_BASE_URL=',
                        'DATABASE_URL=',
                        'JWT_SECRET_KEY='
                    ]
                    
                    for var in critical_vars:
                        var_name = var.split('=')[0]
                        if var in content:
                            self.color_output.print_status(f"Variável {var_name} configurada", 'success')
                        else:
                            self.color_output.print_status(f"Variável {var_name} não encontrada", 'warning')
            except Exception as e:
                logger.error(f"Erro ao validar .env.production: {e}")
                self.color_output.print_status(f"Erro ao validar .env.production: {e}", 'error')
                return False
        
        return True


class ConfigurationValidator:
    """Classe principal que coordena todas as validações."""
    
    def __init__(self):
        self.color_output = ColorOutput()
        self.file_validator = FileValidator(self.color_output)
        self.dependency_validator = DependencyValidator(self.color_output)
        self.streamlit_validator = StreamlitConfigValidator(self.color_output, self.file_validator)
        self.dashboard_validator = DashboardValidator(self.color_output, self.file_validator)
        self.environment_validator = EnvironmentValidator(self.color_output, self.file_validator)
    
    def validate_deployment_scripts(self) -> bool:
        """Valida scripts de deploy e documentação."""
        self.color_output.print_status("Validando scripts de deploy...")
        
        deploy_files = ['deploy_streamlit.sh', 'streamlit_config.toml']
        
        all_valid = True
        for file in deploy_files:
            if not self.file_validator.check_file_exists(file, "Script de deploy"):
                all_valid = False
        
        # Verifica se script de deploy é executável
        if not self.file_validator.check_executable_permission('deploy_streamlit.sh'):
            all_valid = False
        
        return all_valid
    
    def run_all_validations(self, working_directory: Optional[str] = None) -> bool:
        """Executa todas as validações de configuração."""
        try:
            # Muda para o diretório de trabalho se especificado
            if working_directory:
                original_dir = os.getcwd()
                os.chdir(working_directory)
            
            self.color_output.print_status("Iniciando validação de configuração...")
            print()
            
            # Lista de validações a serem executadas
            validations = [
                ("Dependências Python", lambda: self.dependency_validator.check_python_dependencies([
                    'streamlit', 'pandas', 'plotly', 'requests'
                ])),
                ("Configuração Streamlit", self.streamlit_validator.validate_streamlit_config),
                ("Estrutura dos Dashboards", self.dashboard_validator.validate_dashboard_structure),
                ("Configuração de Ambiente", self.environment_validator.validate_environment_config),
                ("Scripts de Deploy", self.validate_deployment_scripts)
            ]
            
            all_checks_passed = True
            
            for check_name, check_func in validations:
                print(f"🔍 {check_name}:")
                try:
                    result = check_func()
                    if not result:
                        all_checks_passed = False
                except Exception as e:
                    logger.error(f"Erro durante {check_name}: {e}")
                    self.color_output.print_status(f"Erro durante {check_name}: {e}", 'error')
                    all_checks_passed = False
                print()
            
            # Restaura diretório original
            if working_directory:
                os.chdir(original_dir)
            
            return all_checks_passed
            
        except Exception as e:
            logger.error(f"Erro geral durante validação: {e}")
            self.color_output.print_status(f"Erro geral: {e}", 'error')
            return False