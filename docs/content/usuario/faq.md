# ❓ FAQ - Perguntas Frequentes

> **Respostas para as dúvidas mais comuns sobre o AUDITORIA360**

---

## 🎯 **GERAL**

### ❓ O que é o AUDITORIA360?

**R:** Portal seguro e integrado para centralizar, automatizar e auditar processos de folha de pagamento, obrigações sindicais e convenções coletivas. Elimina processos manuais e garante compliance total.

### ❓ Qual o status atual do projeto?

**R:** O projeto está **96% concluído**, com:

- ✅ Arquitetura serverless 100% implementada
- ✅ APIs e portal 100% funcionais
- ✅ Dashboards configurados
- 🟡 4% restante: testes finais e otimizações

### ❓ Como acessar o sistema?

**R:** O sistema estará disponível via web browser. Credenciais de acesso serão fornecidas pela administração conforme seu perfil de usuário.

---

## 👤 **PARA USUÁRIOS**

### ❓ Quais tipos de usuário existem?

**R:** O sistema possui 5 perfis:

- **Administrador**: Acesso total ao sistema
- **RH**: Gestão de funcionários e folha
- **Contador**: Relatórios e compliance
- **Colaborador**: Consulta de dados pessoais
- **Sindicato**: Acesso a CCTs e convenções

### ❓ Como consultar meu holerite?

**R:**

1. Faça login no portal
2. Acesse "Meus Dados" > "Holerites"
3. Selecione o período desejado
4. Visualize ou baixe o PDF

### ❓ Como alterar minha senha?

**R:**

1. Acesse "Configurações" > "Segurança"
2. Clique em "Alterar Senha"
3. Digite a senha atual e a nova senha
4. Confirme a alteração

---

## 👨‍💻 **PARA DESENVOLVEDORES**

### ❓ Qual stack tecnológica é usada?

**R:** Stack serverless moderna:

- **Frontend**: React.js + TypeScript
- **Backend**: FastAPI (Python)
- **Banco**: Neon PostgreSQL
- **Storage**: Cloudflare R2
- **Deploy**: Vercel + GitHub Actions

### ❓ Como configurar ambiente de desenvolvimento?

**R:** Consulte o **[Guia de Desenvolvimento](../tecnico/desenvolvimento/dev-guide.md)** completo com todas as instruções de setup.

### ❓ Onde encontro a documentação das APIs?

**R:** A documentação completa está em **[APIs Documentation](../tecnico/apis/api-documentation.md)** com exemplos e especificações.

---

## 🔒 **SEGURANÇA E COMPLIANCE**

### ❓ O sistema é seguro?

**R:** Sim! Implementamos:

- **OAuth2/JWT** para autenticação
- **Criptografia AES-256** para dados sensíveis
- **LGPD compliance** total
- **Backup automatizado**
- **Firewall Cloudflare** anti-DDoS

### ❓ Como funciona o LGPD compliance?

**R:**

- **Consentimento explícito** para coleta de dados
- **Anonimização** automática quando necessário
- **Direito ao esquecimento** implementado
- **Logs de auditoria** completos
- **Políticas de retenção** configuráveis

### ❓ Quem pode acessar meus dados?

**R:** Apenas usuários autorizados conforme:

- **Perfil de acesso** configurado
- **Permissões granulares** por recurso
- **Logs de auditoria** de todos os acessos
- **Princípio do menor privilégio**

---

## 📊 **RELATÓRIOS E DADOS**

### ❓ Que tipos de relatórios posso gerar?

**R:**

- **Holerites** individuais e em lote
- **Relatórios sintéticos** por departamento
- **Análises de compliance** automáticas
- **Dashboards** interativos em tempo real
- **Relatórios customizados** por período

### ❓ Como exportar dados?

**R:**

1. Acesse a seção de relatórios
2. Selecione o tipo de relatório
3. Configure filtros e período
4. Escolha formato (PDF, Excel, CSV)
5. Clique em "Exportar"

### ❓ Os dados são atualizados em tempo real?

**R:** Sim! O sistema possui:

- **Dashboards** atualizados em tempo real
- **Notificações** automáticas de alterações
- **Cache inteligente** para performance
- **Sincronização** automática entre módulos

---

## 🔧 **PROBLEMAS TÉCNICOS**

### ❓ O que fazer se o sistema estiver lento?

**R:**

1. Verifique sua conexão com internet
2. Limpe cache do browser (Ctrl+F5)
3. Tente em uma aba anônima
4. Se persistir, contate o suporte

### ❓ Esqueci minha senha, como recuperar?

**R:**

1. Na tela de login, clique "Esqueci minha senha"
2. Digite seu email/CPF
3. Verifique sua caixa de email
4. Siga as instruções recebidas
5. Defina uma nova senha

### ❓ Erro ao fazer upload de arquivo?

**R:** Verifique se:

- **Tamanho**: Máximo 10MB por arquivo
- **Formato**: PDF, DOCX, XLSX, PNG, JPG
- **Nome**: Sem caracteres especiais
- **Conexão**: Internet estável

---

## 📱 **MOBILE E ACESSIBILIDADE**

### ❓ Posso usar no celular?

**R:** Sim! O sistema é **totalmente responsivo**:

- Interface adaptada para mobile
- Funcionalidades completas
- Performance otimizada
- Touch-friendly

### ❓ O sistema é acessível?

**R:** Sim, seguimos padrões:

- **WCAG 2.1 AA** compliance
- **Leitores de tela** compatíveis
- **Alto contraste** disponível
- **Navegação por teclado** total

---

## 🆘 **SUPORTE**

### ❓ Como obter suporte técnico?

**R:**

- **Documentação**: Consulte primeiro este FAQ
- **Troubleshooting**: Ver [guia de problemas](troubleshooting.md)
- **Issues**: Abra um ticket no GitHub
- **Contato**: Email da equipe de desenvolvimento

### ❓ Horário de funcionamento do suporte?

**R:**

- **Sistema**: 24/7 disponível
- **Suporte técnico**: Segunda a sexta, 8h às 18h
- **Emergências**: Contato especial para casos críticos
- **Atualizações**: Geralmente aos domingos

---

## 🔄 **ATUALIZAÇÕES E ROADMAP**

### ❓ Com que frequência o sistema é atualizado?

**R:**

- **Correções**: Conforme necessário
- **Melhorias**: Mensalmente
- **Novas funcionalidades**: Trimestralmente
- **Major releases**: Semestralmente

### ❓ Onde posso ver o que está sendo desenvolvido?

**R:** Consulte nosso **[Roadmap Estratégico](../estrategico/roadmap-estrategico.md)** com planejamento 2025-2027.

---

## 📞 **CONTATOS ÚTEIS**

### 🔗 **Links Importantes**

- **[Início Rápido](../01-INICIO_RAPIDO.md)** - Primeiros passos
- **[Manual do Usuário](manual-usuario.md)** - Guia completo
- **[Troubleshooting](troubleshooting.md)** - Solução de problemas
- **[Status do Projeto](../relatorios/status-projeto.md)** - Situação atual

### 📧 **Suporte por Categoria**

- **Dúvidas gerais**: Consulte documentação
- **Problemas técnicos**: GitHub Issues
- **Solicitações**: Portal de demandas interno
- **Emergências**: Contato direto da equipe

---

> 💡 **Não encontrou sua dúvida?** Consulte a **[documentação completa](../00-INDICE_PRINCIPAL.md)** ou entre em contato com nossa equipe de suporte.

**Última atualização**: Janeiro 2025 | **Versão**: 4.0
