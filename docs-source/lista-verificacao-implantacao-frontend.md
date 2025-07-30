# Checklist de Deploy Frontend SPA

## ✅ Verificações Pré-Deploy

### 📁 Arquivos de Build
- [ ] Todos os arquivos de build estão presentes no servidor
  - [ ] `index.html` (arquivo principal da SPA)
  - [ ] `assets/style.css` (arquivos de estilo)
  - [ ] `assets/logo.png` (recursos visuais)
  - [ ] Todos os arquivos JS compilados

### 🔗 Configuração de Caminhos
- [ ] Caminhos relativos nas referências JS/CSS no `index.html`
- [ ] Verificar se não há referências absolutas quebradas
- [ ] Assets estão no diretório correto (`/assets/`)

### 🌐 Configuração do Servidor Web
- [ ] **Nginx**: Arquivo `infra/nginx.conf` configurado
  - [ ] Regra `try_files $uri $uri/ /index.html;` implementada
  - [ ] Proxy para API configurado (`/api/` → backend)
  - [ ] Cache headers configurados para assets
- [ ] **Apache**: Arquivo `infra/.htaccess` configurado
  - [ ] Mod_rewrite habilitado
  - [ ] Regras de rewrite para SPA implementadas
  - [ ] Headers de segurança configurados

### 🔒 HTTPS e Segurança
- [ ] Certificado SSL instalado e configurado
- [ ] Redirecionamento HTTP → HTTPS funcionando
- [ ] Headers de segurança implementados:
  - [ ] `X-Frame-Options: DENY`
  - [ ] `X-Content-Type-Options: nosniff`
  - [ ] `X-XSS-Protection: 1; mode=block`
  - [ ] `Strict-Transport-Security` (HSTS)

## 🧪 Testes de Navegação

### 🗺️ Rotas da Aplicação
Testar navegação para todas as rotas internas:

- [ ] `/` (página inicial/login)
- [ ] `/dashboard` (dashboard principal)
- [ ] `/portal_demandas` (portal de demandas)
- [ ] `/relatorios` (relatórios)
- [ ] `/checklist` (checklist de auditoria)
- [ ] `/consultor` (consultor de riscos)
- [ ] `/ccts` (gestão de CCTs)
- [ ] `/revisao` (revisão de cláusulas)
- [ ] `/obrigacoes` (obrigações e prazos)
- [ ] `/parametros` (parâmetros legais)
- [ ] `/sugestoes` (sugestões CCT)
- [ ] `/benchmarking` (benchmarking)
- [ ] `/trilha` (trilha de auditoria)

### 🔄 Tipos de Navegação
- [ ] **Navegação direta**: Acessar URL diretamente no navegador
- [ ] **Navegação interna**: Cliques nos links/botões da aplicação
- [ ] **Refresh da página**: F5 em qualquer rota interna
- [ ] **Botão voltar**: Histórico do navegador funcionando

### 🧹 Cache e Performance
- [ ] Testar após limpeza de cache do navegador
- [ ] Verificar se assets são carregados corretamente
- [ ] Validar se compressão gzip está funcionando
- [ ] Confirmar tempos de carregamento aceitáveis

## 🔍 Validações Técnicas

### 📡 Network e Console
- [ ] **Console do navegador**: Sem erros 404 ou de recursos
- [ ] **Network tab**: Todos os recursos carregando corretamente
- [ ] **API calls**: Endpoints `/api/*` funcionando
- [ ] **WebSocket**: Conexões em tempo real (se aplicável)

### 🎯 Funcionalidades Core
- [ ] **Login/Logout**: Sistema de autenticação funcionando
- [ ] **Navegação por perfil**: Super Admin, Contabilidade, Cliente Final
- [ ] **Proteção de rotas**: Acesso restrito por tipo de usuário
- [ ] **Persistência de sessão**: Session storage funcionando

### 📱 Responsividade
- [ ] **Desktop**: Layout e navegação funcionando
- [ ] **Tablet**: Interface adaptativa
- [ ] **Mobile**: Menu responsivo e navegação touch

## 🚨 Checklist de Emergência (Rollback)

Caso algo dê errado:

- [ ] **Backup dos arquivos anteriores** disponível
- [ ] **Procedimento de rollback** documentado
- [ ] **Contatos da equipe técnica** acessíveis
- [ ] **Logs de erro** sendo monitorados

## 📋 Pós-Deploy

### 🎯 Validação Final
- [ ] Testar com diferentes navegadores (Chrome, Firefox, Safari, Edge)
- [ ] Validar funcionalidades críticas em produção
- [ ] Confirmar que métricas de monitoramento estão funcionando
- [ ] Verificar se backup automático está operacional

### 📊 Monitoramento
- [ ] **Uptime**: Serviço rodando sem interrupções
- [ ] **Performance**: Tempos de resposta dentro do esperado
- [ ] **Erros**: Logs sem erros críticos
- [ ] **Usuários**: Feedback positivo dos usuários finais

## 🆘 Contatos de Suporte

- **Equipe DevOps**: devops@auditoria360.com.br
- **Equipe Frontend**: frontend@auditoria360.com.br
- **Emergência 24h**: +55 (11) 99999-9999

---

> **⚠️ IMPORTANTE**: Este checklist deve ser executado integralmente antes de qualquer deploy em produção. Todos os itens marcados como obrigatórios devem estar ✅ antes de prosseguir.