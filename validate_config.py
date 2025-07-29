#!/usr/bin/env python3
"""
🔍 AUDITORIA360 - Configuration Validation Script
Validates deployment configuration for Streamlit Cloud
"""

import os
import sys
import importlib.util
from pathlib import Path
import configparser

def check_colors():
    """Return color codes for console output"""
    return {
        'GREEN': '\033[0;32m',
        'RED': '\033[0;31m',
        'YELLOW': '\033[1;33m',
        'BLUE': '\033[0;34m',
        'NC': '\033[0m'  # No Color
    }

def print_status(message, status='info'):
    """Print colored status messages"""
    colors = check_colors()
    if status == 'success':
        print(f"{colors['GREEN']}✅ {message}{colors['NC']}")
    elif status == 'error':
        print(f"{colors['RED']}❌ {message}{colors['NC']}")
    elif status == 'warning':
        print(f"{colors['YELLOW']}⚠️  {message}{colors['NC']}")
    else:
        print(f"{colors['BLUE']}ℹ️  {message}{colors['NC']}")

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    if Path(filepath).exists():
        print_status(f"{description}: {filepath}", 'success')
        return True
    else:
        print_status(f"{description} não encontrado: {filepath}", 'error')
        return False

def check_python_dependencies():
    """Check if required Python dependencies are available"""
    required_deps = [
        'streamlit',
        'pandas', 
        'plotly',
        'requests'
    ]
    
    print_status("Verificando dependências Python...")
    all_available = True
    
    for dep in required_deps:
        if importlib.util.find_spec(dep) is not None:
            print_status(f"Dependência {dep} disponível", 'success')
        else:
            print_status(f"Dependência {dep} não encontrada", 'error')
            all_available = False
    
    return all_available

def validate_streamlit_config():
    """Validate Streamlit configuration files"""
    config_file = '.streamlit/config.toml'
    secrets_file = '.streamlit/secrets.toml'
    
    print_status("Validando configuração do Streamlit...")
    
    # Check config.toml
    if not check_file_exists(config_file, "Configuração Streamlit"):
        return False
    
    # Check secrets.toml
    if not check_file_exists(secrets_file, "Secrets Streamlit"):
        return False
    
    # Validate config.toml content
    try:
        with open(config_file, 'r') as f:
            content = f.read()
            if '[theme]' in content:
                print_status("Tema configurado corretamente", 'success')
            else:
                print_status("Configuração de tema não encontrada", 'warning')
    except Exception as e:
        print_status(f"Erro ao ler {config_file}: {e}", 'error')
        return False
    
    return True

def validate_dashboard_structure():
    """Validate dashboard folder structure"""
    print_status("Validando estrutura dos dashboards...")
    
    required_files = [
        'dashboards/app.py',
        'dashboards/requirements.txt',
        'dashboards/api_client.py',
        'dashboards/DEPLOY_README.md'
    ]
    
    all_present = True
    for file in required_files:
        if not check_file_exists(file, "Arquivo dashboard"):
            all_present = False
    
    # Check pages directory
    pages_dir = Path('dashboards/pages')
    if pages_dir.exists():
        page_files = list(pages_dir.glob('*.py'))
        print_status(f"Páginas encontradas: {len(page_files)}", 'success')
    else:
        print_status("Diretório de páginas não encontrado", 'warning')
    
    return all_present

def validate_environment_config():
    """Validate environment configuration"""
    print_status("Validando configuração de ambiente...")
    
    env_files = [
        '.env.production',
        '.env.cloudsql'
    ]
    
    for env_file in env_files:
        check_file_exists(env_file, f"Arquivo de ambiente")
    
    # Check for critical environment variables in .env.production
    if Path('.env.production').exists():
        try:
            with open('.env.production', 'r') as f:
                content = f.read()
                critical_vars = [
                    'ENVIRONMENT=production',
                    'API_BASE_URL=',
                    'DATABASE_URL=',
                    'JWT_SECRET_KEY='
                ]
                
                for var in critical_vars:
                    if var in content:
                        print_status(f"Variável {var.split('=')[0]} configurada", 'success')
                    else:
                        print_status(f"Variável {var.split('=')[0]} não encontrada", 'warning')
        except Exception as e:
            print_status(f"Erro ao validar .env.production: {e}", 'error')

def validate_deployment_scripts():
    """Validate deployment scripts and documentation"""
    print_status("Validando scripts de deploy...")
    
    deploy_files = [
        'deploy_streamlit.sh',
        'streamlit_config.toml'
    ]
    
    for file in deploy_files:
        check_file_exists(file, "Script de deploy")
    
    # Check if deploy script is executable
    deploy_script = Path('deploy_streamlit.sh')
    if deploy_script.exists():
        if os.access(deploy_script, os.X_OK):
            print_status("Script de deploy é executável", 'success')
        else:
            print_status("Script de deploy não é executável (execute: chmod +x deploy_streamlit.sh)", 'warning')

def main():
    """Main validation function"""
    print("🔍 AUDITORIA360 - Validação de Configuração para Deploy")
    print("=" * 60)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    all_checks_passed = True
    
    # Run all validation checks
    checks = [
        ("Dependências Python", check_python_dependencies),
        ("Configuração Streamlit", validate_streamlit_config),
        ("Estrutura dos Dashboards", validate_dashboard_structure),
        ("Configuração de Ambiente", validate_environment_config),
        ("Scripts de Deploy", validate_deployment_scripts)
    ]
    
    print_status("Iniciando validação...")
    print()
    
    for check_name, check_func in checks:
        print(f"🔍 {check_name}:")
        try:
            result = check_func()
            if not result:
                all_checks_passed = False
        except Exception as e:
            print_status(f"Erro durante {check_name}: {e}", 'error')
            all_checks_passed = False
        print()
    
    # Final summary
    print("=" * 60)
    if all_checks_passed:
        print_status("🎉 Todas as verificações passaram! Pronto para deploy.", 'success')
        print()
        print("📋 Próximos passos:")
        print("1. Execute: ./deploy_streamlit.sh")
        print("2. Acesse: https://share.streamlit.io")
        print("3. Configure o repositório: Thaislaine997/AUDITORIA360")
        print("4. Defina o arquivo principal: dashboards/app.py")
        print("5. Adicione os secrets no painel do Streamlit Cloud")
        return 0
    else:
        print_status("❌ Algumas verificações falharam. Corrija os problemas antes do deploy.", 'error')
        return 1

if __name__ == "__main__":
    sys.exit(main())