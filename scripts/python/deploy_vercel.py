#!/usr/bin/env python3
"""
deploy_vercel.py - Script para deploy automatizado na Vercel

Este script é a versão Python migrada do deploy_vercel.sh, seguindo as
diretrizes estabelecidas no ADR-007 para unificação da stack de automação.

Usage:
    python deploy_vercel.py [OPTIONS]

Examples:
    python deploy_vercel.py --production
    python deploy_vercel.py --dry-run
    python deploy_vercel.py --verbose

Author: Equipe AUDITORIA360 
Version: 2.0 (migrado de shell para Python)
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DeploymentError(Exception):
    """Exception raised during deployment operations."""
    pass


class VercelDeployer:
    """Handles Vercel deployment operations for AUDITORIA360."""
    
    def __init__(self, production: bool = False, dry_run: bool = False, verbose: bool = False):
        self.production = production
        self.dry_run = dry_run  
        self.verbose = verbose
        self.project_root = Path(__file__).parent.parent.parent
        
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Verbose mode activated")
    
    def validate_prerequisites(self) -> None:
        """Validate all prerequisites for deployment."""
        logger.info("Validating prerequisites...")
        
        # Verify we're in the correct project directory
        if not (self.project_root / "package.json").exists() and not (self.project_root / "vercel.json").exists():
            raise DeploymentError(
                f"Execute o script a partir da raiz do projeto AUDITORIA360. "
                f"Arquivos esperados: package.json ou vercel.json não encontrados em {self.project_root}"
            )
        
        # Check if Vercel CLI is installed
        if not self._command_exists("vercel"):
            logger.warning("Vercel CLI não encontrado. Instalando...")
            self._install_vercel_cli()
        else:
            logger.info("✅ Vercel CLI encontrado")
        
        # Check if user is logged in to Vercel
        if not self._is_vercel_authenticated():
            logger.warning("Usuário não está logado na Vercel")
            if not self.dry_run:
                logger.info("Iniciando processo de login...")
                self._login_to_vercel()
            else:
                logger.info("Modo DRY-RUN: login seria necessário")
        else:
            user = self._get_vercel_user()
            logger.info(f"✅ Logado na Vercel como: {user}")
        
        logger.info("✅ Pré-requisitos validados")
    
    def validate_project_config(self) -> None:
        """Validate project configuration for deployment."""
        logger.info("Validando configuração do projeto...")
        
        # Check vercel.json configuration
        vercel_config = self.project_root / "vercel.json"
        if vercel_config.exists():
            logger.info("✅ Arquivo vercel.json encontrado")
            self._validate_json_file(vercel_config)
        else:
            logger.warning("Arquivo vercel.json não encontrado - usando configuração padrão")
        
        # Check environment files
        if self.production and (self.project_root / ".env.production").exists():
            logger.info("✅ Arquivo .env.production encontrado")
        elif (self.project_root / ".env.local").exists():
            logger.info("✅ Arquivo .env.local encontrado")
        else:
            logger.warning("Nenhum arquivo de ambiente encontrado")
        
        logger.info("✅ Configuração do projeto validada")
    
    def run_build(self) -> None:
        """Run local build if necessary."""
        logger.info("Verificando necessidade de build local...")
        
        package_json = self.project_root / "package.json"
        if package_json.exists():
            # Check if build script exists
            try:
                with open(package_json) as f:
                    package_data = json.load(f)
                    if "build" in package_data.get("scripts", {}):
                        logger.info("Script de build encontrado - executando build local...")
                        
                        if self.dry_run:
                            logger.warning("Modo DRY-RUN: build seria executado")
                        else:
                            self._run_command(["npm", "run", "build"], cwd=self.project_root)
                            logger.info("✅ Build local executado com sucesso")
                    else:
                        logger.info("Nenhum script de build encontrado")
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.warning(f"Erro ao ler package.json: {e}")
    
    def execute_deploy(self) -> Optional[str]:
        """Execute deployment to Vercel."""
        logger.info("Iniciando deploy na Vercel...")
        
        # Prepare deploy command
        cmd = ["vercel", "--confirm"]
        
        if self.production:
            cmd.append("--prod")
            logger.info("Fazendo deploy para PRODUÇÃO")
        else:
            logger.info("Fazendo deploy para PREVIEW")
        
        if self.dry_run:
            logger.warning("Modo DRY-RUN ativo - comando que seria executado:")
            logger.info(f"Command: {' '.join(cmd)}")
            return "https://dry-run-url.vercel.app"
        
        # Execute deploy
        try:
            logger.info(f"Executando: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info("✅ Deploy executado com sucesso!")
            
            # Extract URL from output if possible
            deploy_url = self._extract_deploy_url(result.stdout)
            if deploy_url:
                logger.info(f"✅ URL do deploy: {deploy_url}")
            
            return deploy_url
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Falha no deploy da Vercel: {e}")
            logger.error(f"Stdout: {e.stdout}")
            logger.error(f"Stderr: {e.stderr}")
            raise DeploymentError(f"Deploy failed: {e}")
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in the system PATH."""
        try:
            subprocess.run([command, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _install_vercel_cli(self) -> None:
        """Install Vercel CLI globally."""
        if not self._command_exists("npm"):
            raise DeploymentError("npm não encontrado. Instale Node.js primeiro")
        
        logger.info("Instalando Vercel CLI globalmente...")
        self._run_command(["npm", "install", "-g", "vercel"])
        
        if not self._command_exists("vercel"):
            raise DeploymentError("Falha na instalação do Vercel CLI")
        
        logger.info("✅ Vercel CLI instalado com sucesso")
    
    def _is_vercel_authenticated(self) -> bool:
        """Check if user is authenticated with Vercel."""
        try:
            subprocess.run(["vercel", "whoami"], capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _get_vercel_user(self) -> str:
        """Get current Vercel user."""
        try:
            result = subprocess.run(
                ["vercel", "whoami"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "unknown"
    
    def _login_to_vercel(self) -> None:
        """Login to Vercel."""
        try:
            subprocess.run(["vercel", "login"], check=True)
        except subprocess.CalledProcessError as e:
            raise DeploymentError(f"Falha no login da Vercel: {e}")
    
    def _validate_json_file(self, file_path: Path) -> None:
        """Validate JSON file syntax."""
        try:
            with open(file_path) as f:
                json.load(f)
        except json.JSONDecodeError as e:
            raise DeploymentError(f"Arquivo {file_path.name} contém JSON inválido: {e}")
    
    def _run_command(self, cmd: list, cwd: Optional[Path] = None) -> str:
        """Run a command and return its output."""
        logger.debug(f"Running command: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(cmd)}")
            logger.error(f"Stderr: {e.stderr}")
            raise DeploymentError(f"Command failed: {e}")
    
    def _extract_deploy_url(self, output: str) -> Optional[str]:
        """Extract deployment URL from Vercel output."""
        # Simple pattern matching for Vercel URLs
        lines = output.split('\n')
        for line in lines:
            if 'https://' in line and 'vercel.app' in line:
                # Extract URL (this is a simplified extraction)
                parts = line.split()
                for part in parts:
                    if 'https://' in part and 'vercel.app' in part:
                        return part.strip()
        return None


def main() -> int:
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Deploy AUDITORIA360 to Vercel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --production          Deploy to production
  %(prog)s --dry-run             Simulate deployment
  %(prog)s --verbose             Enable verbose output
        """
    )
    
    parser.add_argument(
        "-p", "--production",
        action="store_true",
        help="Deploy to production (default: preview)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true", 
        help="Simulate execution without deploying"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force deploy even with warnings (for future compatibility)"
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("🚀 Iniciando deploy_vercel.py...")
        
        deployer = VercelDeployer(
            production=args.production,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
        
        deployer.validate_prerequisites()
        deployer.validate_project_config()
        deployer.run_build()
        deploy_url = deployer.execute_deploy()
        
        logger.info("✅ deploy_vercel.py executado com sucesso!")
        
        if args.production:
            logger.info("🎉 Deploy de PRODUÇÃO realizado")
        else:
            logger.info("🔄 Deploy de PREVIEW realizado")
            
        if deploy_url and not args.dry_run:
            logger.info(f"🌐 Aplicação disponível em: {deploy_url}")
        
        return 0
        
    except DeploymentError as e:
        logger.error(f"❌ Deploy failed: {e}")
        return 1
    except KeyboardInterrupt:
        logger.warning("⏹️ Deploy interrompido pelo usuário")
        return 130
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())