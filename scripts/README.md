# scripts/

Scripts auxiliares organizados por tipo para facilitar localização e uso.

## Estrutura Organizada

### `python/`
Scripts Python para automação, deploy, monitoramento e integrações:
- `api_healthcheck.py`: verificação de saúde da API
- `ci_notify_teams.py`: notificações para Teams no CI/CD
- `demo_mcp_integration.py`: demonstração de integração MCP
- `deploy_production.py`: script de deploy para produção
- `etl_elt.py`: processos de ETL/ELT
- `exportar_auditorias_csv.py`: exportação de auditorias
- `generate_data_hash.py`: cálculo de hash SHA256 para integridade
- `health_check.py`: verificações de saúde do sistema
- `main.py`: script principal
- `onboarding_cliente.py`: automação de onboarding
- `restore_neon_r2.py`: restore de dados Neon/R2
- `run_final_tests.py`: execução de testes finais
- `setup_advanced_monitoring.py`: configuração de monitoramento avançado
- `setup_monitoring.py`: configuração básica de monitoramento
- `test_mcp_simple.py`: testes simples MCP
- `verificar_progresso.py`: verificação de progresso

### `shell/`
Scripts Shell (.sh) para deploy, configuração e utilitários:
- `auditoria_gcp.sh`: auditoria de recursos GCP
- `cloudrun_deploy.sh`: deploy para Cloud Run
- `deploy_streamlit.sh`: deploy do Streamlit
- `deploy_vercel.sh`: deploy para Vercel
- `git_update_all.sh`: atualização em lote via Git
- `restore_db.sh`: restore de banco de dados
- `setup_dev_env.sh`: configuração do ambiente de desenvolvimento
- `setup_mcp_dev.sh`: configuração MCP para desenvolvimento

### `powershell/`
Scripts PowerShell (.ps1) para ambientes Windows:
- `cloudrun_deploy_backend.ps1`: deploy do backend no Cloud Run
- `cloudrun_deploy_streamlit.ps1`: deploy do Streamlit no Cloud Run
- `setup_dev_env.ps1`: configuração do ambiente de desenvolvimento

### `batch/`
Scripts Batch (.bat) para automação Windows:
- `agendar_auditoria_mensal.bat`: agendamento de auditoria mensal
- `compilar_instalador_windows.bat`: compilação de instalador Windows

## Outros Arquivos
- `merge_folhas.sql`: script SQL para merge de folhas
- `ml_training/`: diretório com scripts de treinamento ML

## Nota
Exemplos práticos de uso da stack (OCR, DuckDB, R2, etc.) estão centralizados na pasta `examples/`.
