# Scripts e Automação - AUDITORIA360

## Visão Geral

Este diretório contém documentação sobre todos os scripts e automações do projeto AUDITORIA360, incluindo scripts Shell, PowerShell e Batch utilizados para desenvolvimento, deploy e operações.

## Estrutura de Scripts

### Scripts de Instalação e Configuração
- **[setup_dev_env.sh](../../../installers/setup_dev_env.sh)** - Configuração do ambiente de desenvolvimento (Linux/macOS)
- **[setup_dev_env.ps1](../../../installers/setup_dev_env.ps1)** - Configuração do ambiente de desenvolvimento (Windows)
- **[setup_mcp_dev.sh](../../../scripts/setup_mcp_dev.sh)** - Configuração do ambiente MCP para GitHub Copilot

### Scripts de Deploy
- **[deploy_streamlit.sh](../../../deploy_streamlit.sh)** - Deploy da aplicação Streamlit
- **[cloudrun_deploy_backend.ps1](../../../deploy/cloudrun_deploy_backend.ps1)** - Deploy do backend no Google Cloud Run
- **[cloudrun_deploy_streamlit.ps1](../../../deploy/cloudrun_deploy_streamlit.ps1)** - Deploy do Streamlit no Google Cloud Run
- **[deploy_vercel.sh](../../../scripts/deploy_vercel.sh)** - Deploy automático na Vercel

### Scripts de Operação e Manutenção
- **[auditoria_gcp.sh](../../../auditoria_gcp.sh)** - Auditoria recorrente de recursos GCP
- **[restore_db.sh](../../../scripts/restore_db.sh)** - Restauração de backup do banco de dados
- **[git_update_all.sh](../../../scripts/git_update_all.sh)** - Atualização automática do repositório

### Scripts de Automação
- **[agendar_auditoria_mensal.bat](../../../scripts/agendar_auditoria_mensal.bat)** - Agendamento de auditoria mensal (Windows)
- **[compilar_instalador_windows.bat](../../../installers/compilar_instalador_windows.bat)** - Compilação do instalador Windows

## Padrões de Codificação

Todos os scripts seguem padrões estabelecidos para garantir:
- **Legibilidade**: Código bem formatado e comentado
- **Segurança**: Validação de entrada e tratamento de erros
- **Manutenibilidade**: Estrutura consistente e documentação adequada

### Padrões para Scripts Shell (.sh)
- Shebang obrigatório: `#!/bin/bash`
- Header com descrição, uso e autor
- Tratamento de erros com `set -e`
- Funções de logging colorido
- Validação de pré-requisitos
- Comentários explicativos

### Padrões para Scripts PowerShell (.ps1)
- Header com descrição e parâmetros
- `$ErrorActionPreference = "Stop"`
- Funções de output colorido
- Validação de permissões quando necessário
- Try-catch para tratamento de erros
- Documentação de parâmetros

### Padrões para Scripts Batch (.bat)
- Header com descrição
- `@echo off` para limpeza de output
- Variáveis locais com `setlocal`
- Verificação de erros após comandos críticos
- Comentários com `REM`

## Documentação Técnica

- [Padrões de Scripts](padroes-scripts.md)
- [Guia de Deploy](guia-deploy.md)
- [Troubleshooting](troubleshooting-scripts.md)

## Contribuição

Ao criar ou modificar scripts:
1. Siga os padrões estabelecidos
2. Adicione documentação apropriada
3. Teste em ambiente de desenvolvimento
4. Atualize esta documentação se necessário

## Suporte

Para problemas com scripts:
1. Consulte a documentação de troubleshooting
2. Verifique os logs de execução
3. Abra uma issue no GitHub com detalhes do erro