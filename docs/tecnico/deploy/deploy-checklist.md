# Checklist de Deploy/Release - AUDITORIA360 White-Label

## 1. Testes Automatizados

- [ ] Todos os testes pytest passam (incluindo isolamento multi-cliente, login, PDF, branding)
- [ ] Cobertura de código revisada (recomenda-se >80%)
- [ ] Testes manuais de login, filtros, PDF e branding para todos os clientes ativos

## 2. Backup e Segurança

- [ ] Backup dos arquivos de configuração (`src/client_configs/`, `auth/login.yaml`)
- [ ] Backup dos dados críticos (BigQuery, Firestore, etc)
- [ ] Revisão de variáveis sensíveis (chaves, secrets, etc)

## 3. Atualização de Dependências

- [ ] `requirements.txt` revisado e atualizado
- [ ] Dependências de segurança auditadas (ex: `pip-audit`)

## 4. Build e Deploy

### 4.1 Deploy Manual (Scripts PowerShell)

- [ ] gcloud CLI autenticado e configurado
- [ ] Scripts PowerShell executados com sucesso:
  - [ ] Backend deploy: `.\deploy\cloudrun_deploy_backend.ps1 -ProjectId "PROJECT_ID" -ProcessorId "PROCESSOR_ID" -Verbose`
  - [ ] Frontend deploy: `.\deploy\cloudrun_deploy_streamlit.ps1 -ProjectId "PROJECT_ID" -ApiBaseUrl "BACKEND_URL" -Verbose`
- [ ] URLs dos serviços validadas e funcionando
- [ ] Variáveis de ambiente configuradas corretamente

### 4.2 Validação de Deploy

- [ ] Build do backend (FastAPI) e frontend (Streamlit) realizado sem erros
- [ ] Deploy em ambiente de staging/teste
- [ ] Validação do ambiente de staging (login, filtros, PDF, branding)
- [ ] Deploy em produção
- [x] Checklist inteligente de fechamento da folha testado em staging
- [x] Deploy do backend e frontend com endpoints do checklist
- [x] Validação do fluxo de seleção de folha e fechamento

## 5. Pós-Deploy

- [ ] Monitoramento de logs e alertas ativado
- [ ] Teste de login/logout em produção
- [ ] Teste de geração de PDF em produção
- [ ] Comunicação de release para clientes (se aplicável)
- [ ] Verificação de saúde dos serviços Cloud Run:
  - [ ] Backend: health check endpoint respondendo
  - [ ] Frontend: interface carregando corretamente
  - [ ] Conectividade entre frontend e backend funcionando

## 6. Scripts PowerShell - Validação Técnica

- [ ] Scripts refatorados seguindo padrões estabelecidos
- [ ] Tratamento de erros implementado
- [ ] Parâmetros validados e documentados
- [ ] Output colorido e informativo funcionando
- [ ] Documentação atualizada em `docs/tecnico/desenvolvimento/scripts-powershell.md`
- [ ] Testes dos scripts em ambiente limpo (sem dependências pre-instaladas)

---

> **Importante:** Execute este checklist antes de cada release em produção para garantir estabilidade e segurança do sistema white-label.

> **Novo:** Os scripts PowerShell foram refatorados para maior robustez e padronização. Consulte a [documentação completa](../desenvolvimento/scripts-powershell.md) para detalhes de uso.
