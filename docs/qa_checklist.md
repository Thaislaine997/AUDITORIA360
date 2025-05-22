# Checklist de QA – AUDITORIA360

## 1. Testes de Isolamento Multi-Cliente

- Verificar se dados de um cliente não aparecem para outro
- Testar endpoints com diferentes client_id
- Validar logs de tentativas de acesso cruzado

## 2. Testes de Autenticação e Autorização

- Testar login com credenciais válidas e inválidas
- Validar bloqueio após tentativas incorretas
- Testar reCAPTCHA e SSO/OAuth (se aplicável)

## 3. Testes de Logs e Auditoria

- Conferir geração de logs para ações sensíveis
- Validar auditoria de exportação/PDF
- Testar logs de onboarding de clientes

## 4. Testes de Dados e Privacidade

- Validar tratamento de dados pessoais conforme LGPD
- Testar backup e restauração de dados
- Conferir segregação de dados entre tenants

## 5. Testes de Integração e Fluxos

- Testar integração com IA (Vertex, Gemini)
- Validar automações e dashboards
- Testar fluxos completos com dados reais

---

**Dica:** Utilize o checklist de deploy e monitore os logs após cada release para garantir a qualidade contínua.
