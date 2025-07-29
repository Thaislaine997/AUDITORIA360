# 🛠️ Scripts Auxiliares - Organização e Uso

## 📋 Visão Geral

Os scripts auxiliares do AUDITORIA360 foram organizados em uma estrutura modular para facilitar localização, manutenção e uso. Esta organização segue as melhores práticas de gestão de código e padronização.

## 📁 Estrutura Organizada

### Diretório Principal: `/scripts/`

```
scripts/
├── README.md                    # Documentação da estrutura
├── python/                     # Scripts Python (.py)
├── shell/                      # Scripts Shell (.sh)  
├── powershell/                 # Scripts PowerShell (.ps1)
├── batch/                      # Scripts Batch (.bat)
├── ml_training/                # Scripts de Machine Learning
└── merge_folhas.sql           # Scripts SQL específicos
```

## 🐍 Scripts Python (`/scripts/python/`)

### Automação e Deploy
- **`deploy_production.py`**: Deploy automatizado para produção
- **`setup_advanced_monitoring.py`**: Configuração de monitoramento avançado
- **`setup_monitoring.py`**: Configuração básica de monitoramento

### Saúde e Verificação
- **`api_healthcheck.py`**: Verificação de saúde da API
- **`health_check.py`**: Verificações gerais de saúde do sistema
- **`run_final_tests.py`**: Execução de testes finais
- **`verificar_progresso.py`**: Verificação de progresso do sistema

### Processamento de Dados
- **`etl_elt.py`**: Processos de ETL/ELT
- **`exportar_auditorias_csv.py`**: Exportação de auditorias para CSV
- **`generate_data_hash.py`**: Cálculo de hash SHA256 para integridade
- **`restore_neon_r2.py`**: Restore de dados Neon/R2

### Integração e Comunicação
- **`ci_notify_teams.py`**: Notificações para Teams no CI/CD
- **`demo_mcp_integration.py`**: Demonstração de integração MCP
- **`test_mcp_simple.py`**: Testes simples MCP
- **`onboarding_cliente.py`**: Automação de onboarding de clientes

### Scripts Principais
- **`main.py`**: Script principal de execução
- **`__main__.py`**: Ponto de entrada para execução como módulo

## 🐚 Scripts Shell (`/scripts/shell/`)

### Deploy e Infraestrutura
- **`cloudrun_deploy.sh`**: Deploy para Google Cloud Run
- **`deploy_streamlit.sh`**: Deploy do dashboard Streamlit
- **`deploy_vercel.sh`**: Deploy para Vercel

### Configuração e Setup
- **`setup_dev_env.sh`**: Configuração do ambiente de desenvolvimento (Linux/macOS)
- **`setup_mcp_dev.sh`**: Configuração MCP para desenvolvimento

### Manutenção e Backup
- **`restore_db.sh`**: Restore de banco de dados
- **`git_update_all.sh`**: Atualização em lote via Git

### Auditoria e Monitoramento
- **`auditoria_gcp.sh`**: Auditoria de recursos e permissões GCP

## 💻 Scripts PowerShell (`/scripts/powershell/`)

### Deploy Windows
- **`cloudrun_deploy_backend.ps1`**: Deploy do backend no Google Cloud Run
- **`cloudrun_deploy_streamlit.ps1`**: Deploy do Streamlit no Google Cloud Run

### Configuração Windows
- **`setup_dev_env.ps1`**: Configuração do ambiente de desenvolvimento para Windows

## 📝 Scripts Batch (`/scripts/batch/`)

### Automação Windows
- **`agendar_auditoria_mensal.bat`**: Agendamento de auditoria mensal
- **`compilar_instalador_windows.bat`**: Compilação de instalador Windows

## 🤖 Machine Learning (`/scripts/ml_training/`)

### Treinamento de Modelos
- **`train_risk_model.py`**: Treinamento do modelo de risco
- **`evaluate_model.py`**: Avaliação de modelos ML
- **`utils.py`**: Utilitários para ML
- **`__init__.py`**: Inicialização do módulo

## 📊 Scripts SQL

### Processamento de Dados
- **`merge_folhas.sql`**: Merge de folhas de pagamento

## 🚀 Como Usar

### Execução de Scripts Python
```bash
# Executar script específico
python scripts/python/health_check.py

# Executar como módulo
python -m scripts.python.main

# Com permissões (se necessário)
chmod +x scripts/python/setup_monitoring.py
./scripts/python/setup_monitoring.py
```

### Execução de Scripts Shell
```bash
# Dar permissão de execução
chmod +x scripts/shell/deploy_streamlit.sh

# Executar script
./scripts/shell/deploy_streamlit.sh

# Executar com parâmetros
./scripts/shell/auditoria_gcp.sh > relatorio_$(date +%Y%m%d).txt
```

### Execução de Scripts PowerShell
```powershell
# Configurar política de execução (se necessário)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Executar script
.\scripts\powershell\setup_dev_env.ps1

# Executar deploy
.\scripts\powershell\cloudrun_deploy_backend.ps1
```

### Execução de Scripts Batch
```cmd
# Executar diretamente
scripts\batch\agendar_auditoria_mensal.bat

# Executar com agendamento
schtasks /create /tn "Auditoria Mensal" /tr "scripts\batch\agendar_auditoria_mensal.bat"
```

## 🔧 Configuração e Dependências

### Variáveis de Ambiente
Muitos scripts dependem de variáveis de ambiente configuradas em:
- `.env.local` (desenvolvimento)
- `.env.production` (produção)
- Secrets do Streamlit Cloud
- Variáveis do sistema

### Dependências Python
```bash
# Instalar dependências básicas
pip install -r requirements.txt

# Dependências específicas para alguns scripts
pip install prefect fastapi uvicorn streamlit
```

### Dependências Shell
```bash
# Ferramentas necessárias (Linux/macOS)
sudo apt-get install curl wget git jq

# Cloud CLI tools
curl https://sdk.cloud.google.com | bash
npm install -g vercel
```

### Dependências PowerShell
```powershell
# Módulos PowerShell necessários
Install-Module -Name Az -Force
Install-Module -Name Microsoft.PowerShell.SecretManagement -Force
```

## 📝 Padrões e Convenções

### Nomenclatura
- **Python**: `snake_case.py` (ex: `health_check.py`)
- **Shell**: `kebab-case.sh` ou `snake_case.sh` (ex: `deploy_streamlit.sh`)
- **PowerShell**: `PascalCase.ps1` ou `snake_case.ps1`
- **Batch**: `snake_case.bat`

### Estrutura Interna
Todos os scripts seguem uma estrutura padrão:
```python
#!/usr/bin/env python3
"""
Script description
Author: AUDITORIA360 Team
Usage: python script_name.py [args]
"""

import os
import sys
from pathlib import Path

def main():
    """Main function"""
    pass

if __name__ == "__main__":
    main()
```

### Documentação
- Cabeçalho com descrição, autor e uso
- Comentários explicativos em seções complexas
- Tratamento de erros adequado
- Logs informativos

## 🔍 Troubleshooting

### Problemas Comuns

**Permissão Negada (Linux/macOS)**
```bash
chmod +x scripts/shell/script_name.sh
```

**Política de Execução (Windows)**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Módulo não encontrado (Python)**
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python scripts/python/script_name.py
```

**Variáveis de ambiente não configuradas**
```bash
# Verificar se arquivo existe
ls -la .env.local

# Carregar variáveis manualmente
source .env.local
```

## 🔄 Migração de Scripts Antigos

### Referências Atualizadas
Se você tem scripts ou documentação que referenciam os caminhos antigos:

**Caminhos Antigos → Novos Caminhos**
- `./deploy_streamlit.sh` → `./scripts/shell/deploy_streamlit.sh`
- `./auditoria_gcp.sh` → `./scripts/shell/auditoria_gcp.sh`
- `installers/setup_dev_env.sh` → `scripts/shell/setup_dev_env.sh`
- `installers/setup_dev_env.ps1` → `scripts/powershell/setup_dev_env.ps1`
- `deploy/cloudrun_deploy.sh` → `scripts/shell/cloudrun_deploy.sh`

### Atualização de Referências
```bash
# Buscar e substituir referências em arquivos
find . -type f -name "*.md" -exec sed -i 's|installers/setup_dev_env.sh|scripts/shell/setup_dev_env.sh|g' {} +
find . -type f -name "*.py" -exec sed -i 's|deploy_streamlit.sh|scripts/shell/deploy_streamlit.sh|g' {} +
```

## 📊 Monitoramento e Logs

### Logs de Execução
Scripts importantes geram logs em:
- `logs/scripts/` (se configurado)
- Saída padrão com timestamps
- Logs específicos por script

### Métricas
- Tempo de execução
- Status de sucesso/falha
- Recursos utilizados
- Erros e exceções

## 🚀 Próximos Passos

### Melhorias Planejadas
1. **Containerização**: Docker containers para scripts complexos
2. **Orquestração**: Integração com Prefect para workflows
3. **Monitoring**: Dashboard de monitoramento de scripts
4. **Testing**: Testes automatizados para scripts críticos
5. **Documentation**: Auto-geração de documentação

### Contribuição
Para adicionar novos scripts:
1. Escolha o diretório apropriado por tipo
2. Siga as convenções de nomenclatura
3. Adicione documentação adequada
4. Atualize este README se necessário
5. Teste em ambiente de desenvolvimento

---

## 📞 Suporte

Para dúvidas ou problemas com scripts auxiliares:
- 📖 **Documentação**: Consulte este documento
- 🐛 **Issues**: Crie issue no GitHub
- 💬 **Discussões**: Use GitHub Discussions
- 📧 **Contato**: Entre em contato com a equipe AUDITORIA360

---

**Última atualização**: 29/07/2025
**Status**: ✅ Estrutura organizada e documentada