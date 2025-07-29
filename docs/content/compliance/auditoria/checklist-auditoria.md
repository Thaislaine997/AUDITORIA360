# Checklist de Auditoria de Segurança e Dados - AUDITORIA360

## 1. Isolamento Multi-Cliente

- [ ] Todas as tabelas do BigQuery possuem coluna `client_id` obrigatória
- [ ] Todas as queries (SELECT, UPDATE, MERGE) usam filtro por `client_id`
- [ ] Testes automatizados de isolamento multi-cliente passam para todos os endpoints

## 2. Autenticação e Autorização

- [ ] Endpoints protegidos exigem autenticação
- [ ] Tentativas de acesso cruzado entre clientes são bloqueadas e logadas
- [ ] reCAPTCHA obrigatório no login

## 3. Logs e Auditoria

- [ ] Logs de acesso a dados sensíveis são armazenados e revisados periodicamente
- [ ] Logs de exportação/geração de PDF são auditáveis
- [ ] Logs de onboarding de novos clientes são mantidos

## 4. Dados e Privacidade

- [ ] Dados pessoais (nome, CPF, e-mail) são tratados conforme LGPD
- [ ] Dados de clientes não são compartilhados entre tenants
- [ ] Backups regulares dos dados críticos

## 5. Testes e Revisão de Código

- [ ] Cobertura de testes automatizados revisada (>80%)
- [ ] Revisão de código para endpoints críticos
- [ ] Testes manuais de login, filtros, PDF, exportação e dashboards

---

> **Recomendações:**
>
> - Execute este checklist a cada release e sempre que adicionar novos clientes ou integrações.
> - Mantenha evidências de auditoria para compliance e segurança.
