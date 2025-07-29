# 💙 PowerShell Scripts

Scripts auxiliares em PowerShell para automação e deploy no Windows/Azure.

## Scripts Disponíveis

### Deploy e Cloud

- `cloudrun_deploy_backend.ps1` - Deploy do backend para Google Cloud Run
- `cloudrun_deploy_streamlit.ps1` - Deploy do Streamlit para Google Cloud Run
- `setup_dev_env.ps1` - Configuração do ambiente de desenvolvimento no Windows

## Como Usar

1. Abra o PowerShell como Administrador
2. Configure a política de execução se necessário:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Execute o script:

```powershell
.\scripts\powershell\nome-do-script.ps1
```

## Convenções

- Scripts compatíveis com PowerShell 5.1+ e PowerShell Core
- Incluem verificações de dependências e ferramentas necessárias
- Implementam tratamento de erros com `$ErrorActionPreference`
- Utilizam cmdlets nativos do PowerShell quando possível
- Suportam parâmetros para configuração flexível
