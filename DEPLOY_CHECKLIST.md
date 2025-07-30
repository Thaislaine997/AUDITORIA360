# 📋 CHECKLIST DE DEPLOY E VALIDAÇÃO DE INFRAESTRUTURA - AUDITORIA360

## 🎯 Objetivo

Este checklist deve ser executado **obrigatoriamente** antes de qualquer deploy em produção para garantir que todas as configurações externas e de infraestrutura estejam funcionando corretamente.

## 📋 Como Usar

1. **Antes de cada deploy em produção**, crie uma Issue no GitHub com o título: "Checklist de Deploy para a Release vX.Y.Z"
2. **Copie e cole** o conteúdo deste checklist no corpo da Issue
3. **Marque cada item** (`[ ]` → `[x]`) à medida que a verificação é concluída
4. **Apenas após todos os itens serem verificados**, o deploy é autorizado

---

## 🌐 1. VERIFICAÇÃO DE DOMÍNIOS E DNS

### 📍 Domínio Principal (Aplicação)
- [ ] **auditoria360.com.br**
  - **Ferramenta**: [WhatsMyDNS.net](https://www.whatsmydns.net/)
  - **Verificar**: O registro A está apontando para o IP correto do servidor de produção?
  - **IP Esperado**: ________________ (preencher com o IP do servidor)
  - **Status**: 🔴 Pendente / 🟡 Propagando / 🟢 OK
  - **Observações**: ________________________________________________

### 🔗 Domínio da API
- [ ] **api.auditoria360.com.br**
  - **Ferramenta**: [WhatsMyDNS.net](https://www.whatsmydns.net/)
  - **Verificar**: O registro A ou CNAME está apontando para o IP/endereço correto do servidor da API?
  - **Destino Esperado**: ________________ (preencher com IP/CNAME)
  - **Status**: 🔴 Pendente / 🟡 Propagando / 🟢 OK
  - **Observações**: ________________________________________________

### 📧 Servidor de E-mail
- [ ] **dpeixerassessoria.com.br**
  - **Ferramenta**: [WhatsMyDNS.net](https://www.whatsmydns.net/) - Verificar MX Records
  - **Verificar**: O registro MX está apontando para o servidor de e-mail correto?
  - **MX Esperado**: ________________ (ex: smtp.google.com, outlook.com)
  - **Status**: 🔴 Pendente / 🟡 Propagando / 🟢 OK
  - **Observações**: ________________________________________________

---

## 🔐 2. VALIDAÇÃO DE CERTIFICADOS DE SEGURANÇA (SSL)

### 🌐 Domínio Principal
- [ ] **auditoria360.com.br**
  - **Ferramenta**: [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
  - **Verificar**: 
    - Resultado é nota "A" ou "A+"? ________________
    - Certificado não está expirado? ________________
    - Data de expiração: ________________
  - **Status**: 🔴 Falha / 🟡 Atenção / 🟢 OK
  - **Observações**: ________________________________________________

### 🔗 Domínio da API
- [ ] **api.auditoria360.com.br**
  - **Ferramenta**: [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
  - **Verificar**: 
    - Resultado é nota "A" ou "A+"? ________________
    - Certificado não está expirado? ________________
    - Data de expiração: ________________
  - **Status**: 🔴 Falha / 🟡 Atenção / 🟢 OK
  - **Observações**: ________________________________________________

---

## 🗄️ 3. CONECTIVIDADE COM BANCO DE DADOS EXTERNO

### 🔧 Verificação de Credenciais
- [ ] **Credenciais do Banco de Dados**
  - **Verificar**: As variáveis de ambiente no ambiente de produção correspondem às credenciais do painel do provedor?
    - `DB_HOST` / `DATABASE_URL`: ________________
    - `DB_NAME`: ________________
    - `DB_USER`: ________________
    - `DB_PASSWORD`: ✓ Verificado (não expor a senha)
  - **Provedor**: Neon / Vercel / AWS RDS / Outro: ________________
  - **Status**: 🔴 Falha / 🟢 OK
  - **Observações**: ________________________________________________

### 🧪 Teste de Conexão
- [ ] **Teste de Conectividade**
  - **Comando executado**: `python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); print('Conexão OK:', engine.connect())"`
  - **Resultado**: ________________________________________________
  - **Latência**: ________________ ms
  - **Status**: 🔴 Falha / 🟡 Lenta (>500ms) / 🟢 OK
  - **Observações**: ________________________________________________

### 📊 Verificação de Migrações
- [ ] **Status das Migrações**
  - **Comando**: `python manage.py showmigrations` ou equivalente
  - **Todas as migrações aplicadas?**: ________________
  - **Última migração**: ________________
  - **Status**: 🔴 Falha / 🟢 OK
  - **Observações**: ________________________________________________

---

## 🔗 4. CONFIGURAÇÃO DE SERVIÇOS DE TERCEIROS

### 📱 Twilio (SMS/WhatsApp)
- [ ] **Credenciais Twilio**
  - **TWILIO_ACCOUNT_SID**: Configurado e válido? ________________
  - **TWILIO_AUTH_TOKEN**: Configurado e válido? ________________
  - **FROM_PHONE**: Número configurado? ________________
  - **FROM_WHATSAPP**: Número WhatsApp configurado? ________________
  - **Status**: 🔴 Falha / 🟢 OK

- [ ] **Teste de Envio SMS**
  - **Comando**: Executar teste de envio para número de teste
  - **Número de teste**: ________________
  - **Mensagem enviada?**: ________________
  - **ID da mensagem**: ________________
  - **Status**: 🔴 Falha / 🟢 OK
  - **Observações**: ________________________________________________

- [ ] **Teste de Envio WhatsApp**
  - **Comando**: Executar teste de envio para WhatsApp de teste
  - **Número de teste**: ________________
  - **Mensagem enviada?**: ________________
  - **ID da mensagem**: ________________
  - **Status**: 🔴 Falha / 🟢 OK
  - **Observações**: ________________________________________________

### 📧 Serviço de E-mail
- [ ] **Credenciais de E-mail**
  - **EMAIL_HOST**: ________________ (ex: smtp.gmail.com, smtp.outlook.com)
  - **EMAIL_PORT**: ________________ (ex: 587, 465)
  - **EMAIL_HOST_USER**: ________________
  - **EMAIL_HOST_PASSWORD**: ✓ Configurado (não expor a senha)
  - **EMAIL_USE_TLS**: ________________
  - **EMAIL_USE_SSL**: ________________
  - **Status**: 🔴 Falha / 🟢 OK

- [ ] **Teste de Envio de E-mail**
  - **E-mail de teste**: ________________
  - **Assunto**: "Teste de Deploy - AUDITORIA360"
  - **E-mail enviado com sucesso?**: ________________
  - **E-mail recebido?**: ________________
  - **Tempo de entrega**: ________________
  - **Status**: 🔴 Falha / 🟡 Demorado / 🟢 OK
  - **Observações**: ________________________________________________

### ☁️ Cloudflare R2 (Armazenamento)
- [ ] **Credenciais Cloudflare R2**
  - **CLOUDFLARE_R2_ACCESS_KEY**: Configurado? ________________
  - **CLOUDFLARE_R2_SECRET_KEY**: Configurado? ________________
  - **CLOUDFLARE_R2_BUCKET**: Nome do bucket correto? ________________
  - **CLOUDFLARE_R2_ENDPOINT**: URL do endpoint? ________________
  - **Status**: 🔴 Falha / 🟢 OK

- [ ] **Teste de Upload/Download**
  - **Arquivo de teste**: upload_test.txt
  - **Upload bem-sucedido?**: ________________
  - **Download bem-sucedido?**: ________________
  - **URL pública funcional?**: ________________
  - **Status**: 🔴 Falha / 🟢 OK
  - **Observações**: ________________________________________________

### 🤖 OpenAI (IA)
- [ ] **Credenciais OpenAI**
  - **OPENAI_API_KEY**: Configurada e válida? ________________
  - **OPENAI_MODEL**: Modelo configurado (ex: gpt-4)? ________________
  - **OPENAI_MAX_TOKENS**: Limite configurado? ________________
  - **Status**: 🔴 Falha / 🟢 OK

- [ ] **Teste de Requisição IA**
  - **Prompt de teste**: "Teste de conectividade da API"
  - **Resposta recebida?**: ________________
  - **Tempo de resposta**: ________________ ms
  - **Tokens utilizados**: ________________
  - **Status**: 🔴 Falha / 🟡 Lento / 🟢 OK
  - **Observações**: ________________________________________________

---

## 🔧 5. CONFIGURAÇÕES DE APLICAÇÃO

### ⚙️ Variáveis de Ambiente Críticas
- [ ] **SECRET_KEY**: Configurada (mínimo 32 caracteres)? ________________
- [ ] **DEBUG**: Configurada como `False` em produção? ________________
- [ ] **ENVIRONMENT**: Configurada como `production`? ________________
- [ ] **LOG_LEVEL**: Configurado adequadamente (INFO/WARNING)? ________________
- [ ] **CORS_ALLOWED_ORIGINS**: Configurado com domínios corretos? ________________

### 🛡️ Configurações de Segurança
- [ ] **RATE_LIMIT_ENABLED**: Habilitado? ________________
- [ ] **RATE_LIMIT_REQUESTS_PER_MINUTE**: Configurado adequadamente? ________________
- [ ] **SESSION_TIMEOUT_MINUTES**: Configurado (recomendado: 30)? ________________
- [ ] **ENABLE_TENANT_ISOLATION**: Habilitado? ________________
- [ ] **SECURITY_HEADERS_ENABLED**: Habilitado? ________________

---

## 📊 6. MONITORAMENTO E OBSERVABILIDADE

### 📈 Métricas e Dashboards
- [ ] **Health Check Endpoint**
  - **URL**: https://api.auditoria360.com.br/health
  - **Status Code**: 200? ________________
  - **Response Time**: < 500ms? ________________
  - **Status**: 🔴 Falha / 🟡 Lento / 🟢 OK

- [ ] **Métricas Prometheus**
  - **Endpoint**: /metrics disponível? ________________
  - **Métricas sendo coletadas?**: ________________
  - **Status**: 🔴 Falha / 🟢 OK

- [ ] **Logs Centralizados**
  - **Logs sendo enviados para destino?**: ________________
  - **Formato estruturado (JSON)?**: ________________
  - **Status**: 🔴 Falha / 🟢 OK

### 🔔 Alertas
- [ ] **Configuração de Alertas**
  - **Alertas de erro configurados?**: ________________
  - **Alertas de performance configurados?**: ________________
  - **Canais de notificação funcionais?**: ________________
  - **Status**: 🔴 Falha / 🟢 OK

---

## ✅ 7. VALIDAÇÃO FINAL

### 🚀 Smoke Tests
- [ ] **Endpoint Principal**: https://auditoria360.com.br ➜ Status 200
- [ ] **API Health**: https://api.auditoria360.com.br/health ➜ Status 200
- [ ] **API Docs**: https://api.auditoria360.com.br/docs ➜ Acessível
- [ ] **Login Funcionando**: Processo de autenticação completo
- [ ] **Funcionalidade Crítica**: [Especificar teste específico do negócio]

### 📝 Documentação de Deploy
- [ ] **README.md**: Atualizado com informações da nova versão
- [ ] **CHANGELOG.md**: Atualizado com mudanças da release
- [ ] **API Documentation**: Atualizada se houver mudanças
- [ ] **Configurações**: Documentadas adequadamente

---

## 🎯 CRITÉRIOS DE APROVAÇÃO

**✅ DEPLOY AUTORIZADO APENAS SE:**
- [ ] **TODOS** os itens deste checklist foram verificados
- [ ] **TODAS** as verificações têm status 🟢 OK
- [ ] **NENHUM** item crítico tem status 🔴 Falha
- [ ] **Responsável técnico** assinou a aprovação
- [ ] **Backup** foi realizado antes do deploy

---

## 👥 APROVAÇÕES NECESSÁRIAS

**Verificado por:**
- [ ] **DevOps/SRE**: ________________ (nome e data)
- [ ] **Tech Lead**: ________________ (nome e data)
- [ ] **QA Lead**: ________________ (nome e data)

**Aprovação final:**
- [ ] **Engineering Manager/CTO**: ________________ (nome e data)

---

## 📞 CONTATOS DE EMERGÊNCIA

**Durante o Deploy:**
- **Tech Lead**: [Nome] - [Telefone] - [Slack: @tech-lead]
- **DevOps**: [Nome] - [Telefone] - [Slack: @devops]
- **Suporte 24/7**: +55 11 XXXX-XXXX

**Escalation:**
- **CTO**: [Nome] - [Telefone] - [Email]
- **Emergency**: emergency@auditoria360.com

---

> **⚠️ IMPORTANTE**: Este checklist é **OBRIGATÓRIO** e deve ser seguido integralmente. Qualquer item não verificado ou com falha deve ser corrigido antes do deploy em produção.

**Última atualização**: {DATA_ATUAL}
**Versão do checklist**: 1.0
**Próxima revisão**: Após cada deploy