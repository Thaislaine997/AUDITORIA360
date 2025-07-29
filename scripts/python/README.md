# 🐍 Python Scripts

Scripts auxiliares em Python para automação, monitoramento e utilitários diversos.

## Scripts Disponíveis

### Monitoramento e Health Check

- `monitoramento.py` - Sistema de monitoramento abrangente
- `api_healthcheck.py` - Verificação de saúde das APIs
- `health_check.py` - Health check geral do sistema
- `setup_monitoring.py` - Configuração do sistema de monitoramento
- `setup_advanced_monitoring.py` - Setup de monitoramento avançado

### Deploy e Produção

- `deploy_production.py` - Script de deploy para produção
- `run_final_tests.py` - Execução de testes finais antes do deploy

### Integração e MCP

- `demo_mcp_integration.py` - Demonstração da integração MCP
- `test_mcp_simple.py` - Testes simples do MCP

### ETL e Dados

- `etl_elt.py` - Processos de ETL/ELT
- `exportar_auditorias_csv.py` - Exportação de auditorias para CSV
- `generate_data_hash.py` - Geração de hash para dados

### Utilitários e Validação

- `validate_config.py` - Validação de configurações
- `generate_hash.py` - Geração de hashes diversos
- `verificar_progresso.py` - Verificação de progresso de tarefas

### Cliente e Onboarding

- `onboarding_cliente.py` - Script de onboarding de novos clientes

### Backup e Restore

- `restore_neon_r2.py` - Restauração de dados do Neon para R2

### Notificações e CI/CD

- `ci_notify_teams.py` - Notificações para Teams no CI/CD

## Como Usar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute o script:

```bash
python scripts/python/nome-do-script.py
```

## Convenções

- Scripts compatíveis com Python 3.8+
- Incluem docstrings para documentação
- Implementam logging adequado
- Seguem PEP 8 para estilo de código
- Utilizam argparse para parâmetros de linha de comando quando aplicável
- Incluem tratamento de exceções adequado
