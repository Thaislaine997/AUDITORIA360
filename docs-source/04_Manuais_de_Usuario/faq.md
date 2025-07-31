# ❓ FAQ - Perguntas Frequentes

> **Encontre respostas rápidas para as dúvidas mais comuns sobre o AUDITORIA360**

---

## 🎯 **GERAL**

### ❓ **O que é o AUDITORIA360?**
**R:** Portal seguro e inteligente que centraliza, automatiza e audita todos os processos de folha de pagamento, obrigações sindicais e convenções coletivas, eliminando processos manuais e garantindo compliance total.

### ❓ **Qual o status atual do projeto?**
**R:** Sistema **100% operacional** em produção, com:
- ✅ Arquitetura serverless completa
- ✅ APIs e portal funcionais  
- ✅ Dashboards configurados
- ✅ 90%+ de cobertura de testes
- ✅ Segurança e compliance implementados

### ❓ **Como acessar o sistema?**
**R:** Acesse via navegador web em `https://app.auditoria360.com`. Credenciais são fornecidas pelo administrador conforme seu perfil.

### ❓ **O sistema funciona em dispositivos móveis?**
**R:** Sim! Interface totalmente responsiva que funciona em tablets e smartphones. App móvel nativo em desenvolvimento.

---

## 👤 **USUÁRIOS E ACESSO**

### ❓ **Quais perfis de usuário existem?**
**R:** O sistema possui 5 perfis principais:

| Perfil | Acesso | Funcionalidades |
|--------|--------|----------------|
| 🔧 **Administrador** | Total | Configurações, usuários, relatórios |
| 👥 **RH** | Gestão pessoal | Folha, funcionários, benefícios |
| 📊 **Contador** | Fiscal/financeiro | Compliance, obrigações, relatórios |
| 👤 **Colaborador** | Dados pessoais | Holerites, informações pessoais |
| 🤝 **Sindicato** | CCTs | Convenções coletivas, negociações |

### ❓ **Como alterar minha senha?**
**R:**
1. Faça login no sistema
2. Vá em **"Configurações"** > **"Segurança"**
3. Clique em **"Alterar Senha"**
4. Digite senha atual e nova senha
5. Confirme a alteração

### ❓ **Como ativar autenticação em dois fatores (2FA)?**
**R:**
1. **"Configurações"** > **"Segurança"** 
2. Clique em **"Ativar 2FA"**
3. Escaneie QR Code com app autenticador
4. Digite código de verificação
5. Salve códigos de backup

### ❓ **Esqueci minha senha, como recuperar?**
**R:**
1. Na tela de login, clique **"Esqueci minha senha"**
2. Digite seu email cadastrado
3. Verifique email com link de recuperação
4. Siga instruções para criar nova senha

---

## 📋 **FUNCIONALIDADES**

### ❓ **Como processar uma nova folha de pagamento?**
**R:**
1. **"Folha de Pagamento"** > **"Nova Folha"**
2. Selecione período (mensal/semanal)
3. Importe dados ou digite manualmente
4. Execute validação automática
5. Revise inconsistências
6. Confirme processamento

### ❓ **O que é o Checklist de Fechamento?**
**R:** Ferramenta inteligente que guia o fechamento mensal da folha com:
- ✅ Validações automáticas obrigatórias
- 🤖 Dicas de IA para cada item
- 📋 Controle de responsáveis e prazos
- 🚨 Alertas para itens críticos

### ❓ **Como iniciar uma auditoria?**
**R:**
1. **"Auditoria"** > **"Nova Análise"**
2. Escolha tipo: Folha, CCT, Compliance, etc.
3. Faça upload dos documentos
4. Aguarde processamento automático
5. Analise resultados e recomendações

### ❓ **Como consultar convenções coletivas (CCT)?**
**R:**
1. **"CCT"** > **"Buscar Convenção"**
2. Use filtros: sindicato, categoria, região
3. Visualize cláusulas importantes
4. Sistema verifica compliance automaticamente

---

## 📊 **RELATÓRIOS E DADOS**

### ❓ **Que tipos de relatórios posso gerar?**
**R:**
- 📈 **Gerenciais**: Visão estratégica e KPIs
- 📋 **Operacionais**: Detalhes de processos
- 🔍 **Auditoria**: Compliance e conformidade
- 📊 **Analíticos**: Tendências e insights
- 💰 **Financeiros**: Custos e projeções

### ❓ **Como exportar dados?**
**R:**
1. Acesse **"Relatórios"**
2. Selecione tipo desejado
3. Configure filtros e período
4. Escolha formato: PDF, Excel, CSV
5. Clique em **"Exportar"**

### ❓ **Os dados são atualizados em tempo real?**
**R:** Sim! O sistema oferece:
- 📊 Dashboards em tempo real
- 🔔 Notificações automáticas
- ⚡ Cache inteligente para performance
- 🔄 Sincronização entre módulos

### ❓ **Como consultar meu holerite?**
**R:**
1. Faça login no portal
2. **"Meus Dados"** > **"Holerites"**
3. Selecione período desejado
4. Visualize online ou baixe PDF

---

## 🔒 **SEGURANÇA E PRIVACIDADE**

### ❓ **O sistema é seguro?**
**R:** Absolutamente! Implementamos:
- 🔐 **OAuth2/JWT** para autenticação
- 🛡️ **Criptografia AES-256** para dados sensíveis  
- 📋 **LGPD compliance** total
- 💾 **Backup automatizado** diário
- 🔥 **Firewall Cloudflare** anti-DDoS
- 🔍 **Logs de auditoria** completos

### ❓ **Como funciona o compliance LGPD?**
**R:** Sistema 100% aderente à LGPD:
- ✅ **Consentimento explícito** para coleta
- 🎭 **Anonimização** automática
- 🗑️ **Direito ao esquecimento** implementado
- 📝 **Logs de auditoria** detalhados
- ⏰ **Políticas de retenção** configuráveis

### ❓ **Quem pode acessar meus dados?**
**R:** Apenas usuários autorizados:
- 👤 **Perfil de acesso** específico
- 🔐 **Permissões granulares** por recurso
- 📊 **Logs de auditoria** de todos os acessos
- 🛡️ **Princípio do menor privilégio**

---

## 👨‍💻 **PARA DESENVOLVEDORES**

### ❓ **Qual stack tecnológica é usada?**
**R:** Stack serverless moderna:
- **Frontend**: React.js + TypeScript
- **Backend**: FastAPI (Python) 
- **Banco**: PostgreSQL (Neon)
- **Storage**: Cloudflare R2
- **Deploy**: Vercel + GitHub Actions
- **Monitoramento**: Observabilidade completa

### ❓ **Como configurar ambiente de desenvolvimento?**
**R:** Consulte o [**Guia de Desenvolvimento**](../developer-guides/development-setup) completo com instruções detalhadas de setup.

### ❓ **Onde encontro documentação das APIs?**
**R:** Documentação completa em [**API Reference**](../api-reference/README) com:
- 📡 Especificações OpenAPI
- 💻 Exemplos de código
- 🔧 Guias de integração
- 🧪 Ambiente de testes

---

## 🔧 **PROBLEMAS TÉCNICOS**

### ❓ **O que fazer se o sistema estiver lento?**
**R:**
1. Verifique sua **conexão** de internet
2. Feche **abas desnecessárias** do navegador
3. **Limpe cache** do navegador
4. Tente em **horário alternativo**
5. Contate **suporte** se persistir

### ❓ **Erro ao fazer upload de arquivo**
**R:**
1. Verifique **formato** aceito (PDF, XLS, CSV)
2. Confirme **tamanho** máximo (50MB)
3. Teste com **arquivo menor**
4. Use **templates** disponíveis
5. Verifique **conexão** estável

### ❓ **Não consigo fazer login**
**R:**
1. Verifique **email** e **senha**
2. Tente **recuperar senha**
3. Limpe **cache** e **cookies**
4. Desative **bloqueadores** de popup
5. Teste em **navegador diferente**

### ❓ **Dados não aparecem no dashboard**
**R:**
1. Verifique **filtros** aplicados
2. Confirme **permissões** de acesso
3. Aguarde **atualização** (até 5 min)
4. **Recarregue** a página
5. Contate **suporte** com detalhes

---

## 📞 **SUPORTE E CONTATO**

### ❓ **Como entrar em contato com o suporte?**
**R:** Múltiplas opções disponíveis:
- 💬 **Chat**: Canto inferior direito (horário comercial)
- 📧 **Email**: suporte@auditoria360.com.br
- 📞 **Telefone**: 0800-XXX-XXXX
- 🎫 **Ticket**: Dentro do sistema > "Ajuda"

### ❓ **Qual horário de funcionamento do suporte?**
**R:**
- **Chat/Telefone**: Segunda a sexta, 8h às 18h
- **Email/Ticket**: 24h (resposta em até 24h)
- **Emergências**: Suporte 24/7 para clientes premium

### ❓ **Como solicitar nova funcionalidade?**
**R:**
1. Use **"Sugestões"** dentro do sistema
2. Descreva detalhadamente a necessidade
3. Inclua **justificativa** de negócio
4. Nossa equipe avaliará e responderá

### ❓ **Onde encontro tutoriais e treinamentos?**
**R:**
- 🎥 **Vídeos**: Biblioteca interna do sistema
- 📚 **Documentação**: Esta Wiki atualizada
- 🎓 **Webinars**: Quinzenais (calendário no sistema)
- 🏆 **Certificação**: Programa de usuários certificados

---

## 🔄 **ATUALIZAÇÕES E NOVIDADES**

### ❓ **Como fico sabendo de novas funcionalidades?**
**R:**
- 🔔 **Notificações** no sistema
- 📧 **Newsletter** mensal
- 📱 **Release notes** automáticas
- 🎉 **Tours** interativos para novidades

### ❓ **O sistema é atualizado automaticamente?**
**R:** Sim! Todas as atualizações são:
- 🚀 **Automáticas** em produção
- 🧪 **Testadas** extensivamente
- 📋 **Documentadas** em changelog
- 🔄 **Sem interrupção** de serviço

---

> **💡 Não encontrou sua resposta?** Entre em contato conosco! Nossa equipe está sempre pronta para ajudar você a aproveitar ao máximo o AUDITORIA360.