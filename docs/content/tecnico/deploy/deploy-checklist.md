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

---

> **Importante:** Execute este checklist antes de cada release em produção para garantir estabilidade e segurança do sistema white-label.
