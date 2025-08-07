# Guia de Contribuição - AUDITORIA360

## 🐍 Política de Automação: Python First

### Princípio Fundamental

**Python é a linguagem padrão para todos os novos scripts de automação no AUDITORIA360.**

Esta decisão estratégica visa:
- ✅ Consolidar a stack de automação em uma única linguagem
- ✅ Reduzir a complexidade de manutenção 
- ✅ Aproveitar o rico ecossistema Python para automação
- ✅ Facilitar a colaboração entre desenvolvedores
- ✅ Melhorar a testabilidade e debugabilidade dos scripts

### Diretrizes para Scripts de Automação

#### 🔧 Para Novos Scripts
- **OBRIGATÓRIO**: Todos os novos scripts de automação devem ser escritos em Python
- **Localização**: `scripts/python/` para scripts específicos
- **Nomenclatura**: Use snake_case (ex: `deploy_production.py`)
- **Documentação**: Inclua docstrings detalhadas e comentários explicativos

#### 🔄 Para Scripts Existentes
- **Migração Progressiva**: Scripts em shell (.sh) e PowerShell (.ps1) serão migrados progressivamente
- **Prioridade**: Scripts críticos de CI/CD têm prioridade na migração
- **Compatibilidade**: Mantenha versões antigas funcionais durante a transição

#### 📚 Bibliotecas Recomendadas
Para automação em Python, utilize preferencialmente:
- `subprocess` - Para execução de comandos shell
- `pathlib` - Para manipulação de caminhos
- `click` ou `argparse` - Para interfaces de linha de comando
- `shutil` - Para operações de arquivo
- `requests` - Para requisições HTTP
- `python-dotenv` - Para variáveis de ambiente

### Estrutura Recomendada para Scripts

```python
#!/usr/bin/env python3
"""
Script Description: Brief description of what the script does
Author: AUDITORIA360 Team
Version: 1.0
"""

import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function with clear error handling."""
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Script logic here
        logger.info("Script execution started")
        # ... implementation ...
        logger.info("Script execution completed successfully")
        
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        raise

if __name__ == "__main__":
    main()
```

### 🔍 Padrões de Qualidade

#### Code Style
- Siga o PEP 8 para formatação de código
- Use `black` para formatação automática
- Use `isort` para organização de imports
- Use `flake8` para linting

#### Testes
- Scripts críticos devem incluir testes unitários
- Use `pytest` como framework de testes
- Coloque testes em `tests/unit/scripts/`

#### Documentação
- Docstrings obrigatórias para funções públicas
- Comentários para lógica complexa
- README específico se o script for parte de um módulo maior

### 🚀 Exemplos de Migração

#### Shell → Python
```bash
# Antes (deploy.sh)
#!/bin/bash
if [ "$1" = "production" ]; then
    echo "Deploying to production..."
    npm run build
    vercel --prod
fi
```

```python
# Depois (deploy.py)
#!/usr/bin/env python3
import subprocess
import sys

def deploy(environment="preview"):
    """Deploy application to specified environment."""
    if environment == "production":
        print("Deploying to production...")
        subprocess.run(["npm", "run", "build"], check=True)
        subprocess.run(["vercel", "--prod"], check=True)
    else:
        subprocess.run(["vercel"], check=True)

if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) > 1 else "preview"
    deploy(env)
```

### 🎯 Próximos Passos

1. **Migração Prioritária**: 
   - `deploy_vercel.sh` → `deploy_vercel.py`
   - `cloudrun_deploy.sh` → `cloudrun_deploy.py`
   - Scripts de CI/CD críticos

2. **Ferramentas de Suporte**:
   - Criação de utilitários Python para operações comuns
   - Desenvolvimento de templates para novos scripts

3. **Documentação**:
   - Criação de exemplos de migração
   - Guias específicos para casos de uso comuns

### 📞 Suporte

Para dúvidas sobre migração de scripts ou implementação de novos scripts em Python:
- Consulte a documentação em `docs/`
- Revise exemplos em `scripts/python/`
- Abra uma issue para discussões técnicas

---

**Lembre-se**: Esta política visa fortalecer nossa arquitetura tecnológica através da consolidação e padronização. Cada script migrado ou criado em Python contribui para um ecossistema mais robusto e maintível.