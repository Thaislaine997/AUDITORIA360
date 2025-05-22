# Onboarding White-Label – AUDITORIA360

## 1. Provisionamento do Cliente

- Criar projeto e dataset no BigQuery
- Gerar credenciais de serviço
- Configurar variáveis de ambiente

```bash
gcloud projects create <projeto_cliente>
gcloud iam service-accounts create <conta_servico>
```

## 2. Configuração Inicial

- Definir parâmetros no painel de administração
- Vincular client_id ao usuário master
- Ajustar permissões de acesso

## 3. Integração e Testes

- Testar endpoints protegidos
- Validar isolamento multi-cliente
- Executar testes de integração

## 4. Treinamento e Entrega

- Treinar usuários-chave do cliente
- Entregar documentação de uso
- Validar checklist de QA e deploy

---

**Dica:** Mantenha registro de cada etapa do onboarding para auditoria e compliance.
