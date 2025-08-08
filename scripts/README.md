# scripts/ - Scripts de Automação

## Propósito

Diretório contendo scripts de automação para diversas tarefas do sistema AUDITORIA360, organizados por linguagem e função.

## Principais Funcionalidades

- **python/**: Scripts Python para automação, monitoramento e utilitários
- **shell/**: Scripts shell para deploy, backup e operações de sistema
- **powershell/**: Scripts PowerShell para ambiente Windows
- **batch/**: Scripts batch para compatibilidade Windows
- **master_execution_checklist.py**: Validação de checklist principal
- **quick_checklist.py**: Checklist rápido de validação

### 🆕 Scripts Multi-Tenant (Novos)

- **migracao.py**: Script para migração de dados de PDFs para Supabase
- **validate_multi_tenant_implementation.py**: Validação da implementação multi-tenant
- **requirements-migration.txt**: Dependências para scripts de migração

## Instruções de Uso

### Scripts Python

```bash
# Executar script específico
python scripts/python/monitoramento.py

# Health check geral
python scripts/python/health_check.py

# Deploy para produção
python scripts/python/deploy_production.py
```

### Scripts Shell

```bash
# Tornar executável
chmod +x scripts/shell/nome_script.sh

# Executar
./scripts/shell/nome_script.sh
```

### Scripts PowerShell

```powershell
# Executar no PowerShell
.\scripts\powershell\nome_script.ps1
```

## Exemplos

### Scripts Multi-Tenant (Novos)

```bash
# Validar implementação multi-tenant
python scripts/validate_multi_tenant_implementation.py

# Migrar dados de PDFs (configure .env primeiro)
python scripts/migracao.py

# Instalar dependências para migração
pip install -r scripts/requirements-migration.txt
```

### Checklist Principal

```bash
# Validação rápida
python scripts/quick_checklist.py

# Relatório completo
python scripts/master_execution_checklist.py --output json

# Seção específica
python scripts/quick_checklist.py --section PARTE_1_ALICERCE_E_GOVERNANCA
```

### Monitoramento

```bash
# Health check
python scripts/python/health_check.py

# Monitoramento completo
python scripts/python/monitoramento.py --verbose
```

## Dependências

### Python Scripts
- Python 3.8+
- Dependências específicas em cada script
- requirements.txt para dependências principais

### Shell Scripts
- Bash 4.0+
- Ferramentas Unix padrão (grep, awk, sed, etc.)

### PowerShell Scripts
- PowerShell 5.1+ ou PowerShell Core 6.0+
- Módulos específicos conforme necessário

## Convenções

- Scripts Python seguem PEP 8
- Include docstrings e logging adequado
- Tratamento de exceções robusto
- Parâmetros via argparse quando aplicável
- Scripts executáveis têm shebang apropriado