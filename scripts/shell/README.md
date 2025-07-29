# 🐚 Shell Scripts

Scripts auxiliares em Shell/Bash para automação de tarefas do AUDITORIA360.

## Scripts Disponíveis

### Auditoria e Monitoramento
- `auditoria_gcp.sh` - Auditoria recorrente de recursos e permissões GCP
- `git_update_all.sh` - Atualização automática de repositórios Git

### Deploy e Infraestrutura  
- `deploy_streamlit.sh` - Deploy automatizado para Streamlit Cloud
- `deploy_vercel.sh` - Deploy para Vercel
- `cloudrun_deploy.sh` - Deploy para Google Cloud Run

### Setup e Configuração
- `setup_dev_env.sh` - Configuração do ambiente de desenvolvimento
- `setup_mcp_dev.sh` - Setup do ambiente MCP para desenvolvimento

### Banco de Dados
- `restore_db.sh` - Restauração de backup do banco de dados

## Como Usar

1. Torne o script executável:
```bash
chmod +x scripts/shell/nome-do-script.sh
```

2. Execute o script:
```bash
./scripts/shell/nome-do-script.sh
```

## Convenções

- Todos os scripts seguem o padrão bash com `set -e` para tratamento de erros
- Scripts incluem comentários de documentação no cabeçalho
- Utilizam variáveis readonly para configurações importantes
- Implementam verificações de dependências quando necessário