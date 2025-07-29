#!/usr/bin/env python3
"""
🔍 AUDITORIA360 - Configuration Validation Script (Refatorado)
Validates deployment configuration for Streamlit Cloud
Uses modularized validation utilities for better maintainability.
"""

import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.utils.config_validator import ConfigurationValidator
    from src.utils.error_handling import (
        error_handler, ErrorCategory, ErrorSeverity, handle_exceptions
    )
    import logging
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @handle_exceptions(ErrorCategory.CONFIGURATION, ErrorSeverity.HIGH)
    def main():
        """
        Função principal de validação usando sistema modularizado.
        
        Returns:
            int: Código de saída (0 para sucesso, 1 para falha)
        """
        print("🔍 AUDITORIA360 - Validação de Configuração para Deploy")
        print("=" * 60)
        
        # Change to script directory
        script_dir = Path(__file__).parent
        original_dir = os.getcwd()
        
        try:
            os.chdir(script_dir)
            
            # Create configuration validator
            validator = ConfigurationValidator()
            
            # Run all validations
            all_checks_passed = validator.run_all_validations()
            
            # Final summary and next steps
            print("=" * 60)
            if all_checks_passed:
                validator.color_output.print_status(
                    "🎉 Todas as verificações passaram! Pronto para deploy.", 
                    'success'
                )
                print()
                print("📋 Próximos passos:")
                print("1. Execute: ./deploy_streamlit.sh")
                print("2. Acesse: https://share.streamlit.io")
                print("3. Configure o repositório: Thaislaine997/AUDITORIA360")
                print("4. Defina o arquivo principal: dashboards/app.py")
                print("5. Adicione os secrets no painel do Streamlit Cloud")
                
                logger.info("Validação de configuração concluída com sucesso")
                return 0
            else:
                validator.color_output.print_status(
                    "❌ Algumas verificações falharam. Corrija os problemas antes do deploy.", 
                    'error'
                )
                
                logger.warning("Validação de configuração falhou")
                return 1
                
        except Exception as e:
            # Error handling através do sistema centralizado
            error = error_handler.create_error(
                message="Falha durante validação de configuração",
                category=ErrorCategory.CONFIGURATION,
                severity=ErrorSeverity.CRITICAL,
                details=f"Diretório de trabalho: {script_dir}",
                original_exception=e
            )
            error_handler.handle_error(error)
            
            print(f"❌ Erro crítico durante validação: {e}")
            return 1
            
        finally:
            # Restore original directory
            os.chdir(original_dir)

    if __name__ == "__main__":
        sys.exit(main())

except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("\n🔧 Instruções de configuração:")
    print("1. Certifique-se de estar no diretório raiz do projeto AUDITORIA360")
    print("2. Instale as dependências necessárias:")
    print("   pip install -r requirements.txt")
    print("3. Execute este script novamente")
    print("\n📝 Fallback - Executando validação básica...")
    
    # Fallback para validação básica se imports falharem
    def basic_validation():
        """Validação básica como fallback."""
        print("Executando validação básica...")
        
        # Check basic file existence
        basic_files = [
            'requirements.txt',
            'README.md',
            'src/main.py'
        ]
        
        all_exist = True
        for file in basic_files:
            if Path(file).exists():
                print(f"✅ {file} encontrado")
            else:
                print(f"❌ {file} não encontrado")
                all_exist = False
        
        if all_exist:
            print("✅ Validação básica passou")
            return 0
        else:
            print("❌ Validação básica falhou")
            return 1
    
    sys.exit(basic_validation())