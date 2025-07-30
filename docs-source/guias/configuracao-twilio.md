# Configuração da Integração Twilio - AUDITORIA360

## Visão Geral

Este guia técnico fornece instruções detalhadas para configurar a integração do AUDITORIA360 com a API da Twilio, permitindo o envio e recebimento de mensagens via SMS e WhatsApp de forma bidirecional.

## Pré-requisitos

- Conta ativa na Twilio ([twilio.com](https://www.twilio.com))
- Acesso de administrador ao sistema AUDITORIA360
- Conhecimento básico de webhooks e APIs REST

## 1. Configuração da Conta Twilio

### 1.1 Criação da Conta e Obtenção de Credenciais

1. **Acesse o Console da Twilio**: Faça login em [console.twilio.com](https://console.twilio.com)

2. **Localize suas credenciais principais**:
   - Vá para **Account → Account Info**
   - Anote os seguintes valores:
     - **Account SID** (formato: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
     - **Auth Token** (clique em "View" para revelar)

### 1.2 Configuração do Número de Telefone

#### Para SMS:
1. Vá para **Phone Numbers → Manage → Buy a number**
2. Selecione um número com capacidade de SMS
3. Configure o webhook para mensagens recebidas:
   - **Webhook URL**: `https://seu-dominio.com/api/notifications/webhook/twilio`
   - **HTTP Method**: POST

#### Para WhatsApp:
1. Vá para **Messaging → Try it out → Send a WhatsApp message**
2. Para produção, solicite aprovação do WhatsApp Business:
   - Vá para **Messaging → Senders → WhatsApp senders**
   - Clique em "Request Access"
   - Siga o processo de aprovação do WhatsApp

### 1.3 Configuração de Webhooks

1. **Acesse as configurações do número**:
   - Vá para **Phone Numbers → Manage → Active numbers**
   - Clique no número desejado

2. **Configure os webhooks**:
   - **A message comes in**: `https://seu-dominio.com/api/notifications/webhook/twilio`
   - **HTTP Method**: POST
   - **Primary Handler Fails**: (opcional) Configure URL de fallback

3. **Salve as configurações**

## 2. Configuração no AUDITORIA360

### 2.1 Variáveis de Ambiente

Adicione as seguintes variáveis ao arquivo `.env`:

```bash
# Twilio Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+15551234567
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# GitHub Integration (opcional)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_REPO_OWNER=seu-usuario
GITHUB_REPO_NAME=AUDITORIA360
```

### 2.2 Configuração da Interface

1. **Acesse as Configurações**:
   - Faça login como administrador
   - Vá para **Configurações → Conexões de Mensageria**

2. **Selecione o Provedor Twilio**:
   - Provider: `Twilio`
   - Account SID: Cole o valor obtido da Twilio
   - Auth Token: Cole o token de autenticação
   - Número SMS: Seu número Twilio (formato: +15551234567)
   - Número WhatsApp: Seu número WhatsApp (formato: whatsapp:+14155238886)

3. **Teste a Configuração**:
   - Use o botão "Testar Conexão" para verificar as credenciais
   - Envie uma mensagem de teste

## 3. Configuração de Segurança

### 3.1 Validação de Webhook (Recomendado)

Para garantir que apenas a Twilio pode enviar webhooks:

1. **Obtenha o Webhook Signature**:
   - No console Twilio, vá para **Account → Security**
   - Copie o "Primary Auth Token"

2. **Configure a validação no código**:
```python
from twilio.request_validator import RequestValidator

# Adicione ao webhook endpoint
def validate_twilio_signature(request, auth_token):
    validator = RequestValidator(auth_token)
    twilio_signature = request.headers.get('X-Twilio-Signature', '')
    url = str(request.url)
    form_data = dict(request.form)
    
    return validator.validate(url, form_data, twilio_signature)
```

### 3.2 Configuração de IP Whitelist (Opcional)

1. **Configure lista de IPs permitidos**:
   - Vá para **Account → Security → IP Access Control**
   - Adicione os IPs da Twilio: [Lista oficial](https://www.twilio.com/docs/usage/security#ip-addresses)

## 4. Teste da Integração

### 4.1 Teste de Envio

1. **Via Interface do Sistema**:
   - Acesse **Notificações → Enviar Mensagem**
   - Selecione "Twilio" como provedor
   - Escolha tipo: SMS ou WhatsApp
   - Digite o número de destino
   - Envie uma mensagem de teste

2. **Via API**:
```bash
curl -X POST "https://seu-dominio.com/api/notifications/send-enhanced" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "+5511999999999",
    "message": "Teste de integração AUDITORIA360",
    "type": "sms",
    "provider": "twilio"
  }'
```

### 4.2 Teste de Recebimento

1. **Envie uma mensagem para o número Twilio**:
   - SMS: Envie um SMS para o número configurado
   - WhatsApp: Envie uma mensagem para o número WhatsApp

2. **Verifique a criação da Issue**:
   - Acesse o repositório GitHub configurado
   - Verifique se uma nova Issue foi criada automaticamente
   - A Issue deve conter as labels apropriadas (`via-twilio-sms` ou `via-twilio-whatsapp`)

## 5. Monitoramento e Logs

### 5.1 Logs da Twilio

1. **Console Twilio**:
   - Vá para **Monitor → Logs → Errors**
   - Monitore erros de webhook e entrega

2. **Logs de Mensagens**:
   - Vá para **Monitor → Logs → Messages**
   - Visualize todas as mensagens enviadas/recebidas

### 5.2 Logs do Sistema

```bash
# Visualizar logs do gateway de comunicação
tail -f logs/communication_gateway.log

# Verificar status dos provedores
curl "https://seu-dominio.com/api/notifications/gateway/status"
```

## 6. Solução de Problemas Comuns

### 6.1 Webhook não está sendo recebido

**Possíveis causas**:
- URL do webhook incorreta
- Firewall bloqueando requisições da Twilio
- Certificado SSL inválido

**Soluções**:
1. Verifique a URL no console Twilio
2. Teste o endpoint manualmente
3. Use ngrok para desenvolvimento local

### 6.2 Mensagens não estão sendo enviadas

**Possíveis causas**:
- Credenciais incorretas
- Número de destino inválido
- Saldo insuficiente na conta Twilio

**Soluções**:
1. Verifique Account SID e Auth Token
2. Confirme formato do número (+55DDD9XXXXXXXX)
3. Verifique saldo no console Twilio

### 6.3 Issues não estão sendo criadas

**Possíveis causas**:
- Token GitHub inválido
- Repositório não encontrado
- Permissões insuficientes

**Soluções**:
1. Gere novo Personal Access Token no GitHub
2. Verifique nome do repositório
3. Confirme permissões de escrita

## 7. Manutenção

### 7.1 Rotação de Credenciais

**Periodicidade recomendada**: A cada 90 dias

1. **Twilio Auth Token**:
   - Gere novo token no console Twilio
   - Atualize variável de ambiente
   - Reinicie o serviço

2. **GitHub Token**:
   - Gere novo Personal Access Token
   - Atualize configuração
   - Revogue token antigo

### 7.2 Monitoramento de Custos

1. **Configure alertas de billing**:
   - Acesse **Account → Billing**
   - Configure notificações de consumo

2. **Monitore uso mensal**:
   - Analise relatórios de uso
   - Otimize tipos de mensagem baseado no custo

## 8. Considerações de Produção

### 8.1 Limitações da API

- **SMS**: 1600 caracteres por mensagem
- **WhatsApp**: 4096 caracteres por mensagem
- **Rate Limits**: Varia por tipo de conta

### 8.2 Conformidade

- **LGPD**: Obtenha consentimento antes de enviar mensagens
- **WhatsApp**: Siga políticas de spam do WhatsApp
- **SMS**: Respeite horários e frequência de envio

---

## Suporte

Para suporte técnico:
- **Twilio**: [help.twilio.com](https://help.twilio.com)
- **AUDITORIA360**: Consulte a documentação interna ou contate a equipe de desenvolvimento

---
*Documentação atualizada em: Janeiro 2024*
*Versão: 1.0*