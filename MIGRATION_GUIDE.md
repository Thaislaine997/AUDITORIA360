# AUDITORIA360 - Guia de Migração Frontend

## Resumo da Migração

O sistema AUDITORIA360 foi migrado com sucesso de um backend Python com páginas em `dashboards/pages/*.py` para um frontend SPA (Single Page Application) moderno em React. Esta migração moderniza a arquitetura e melhora a experiência do usuário.

## Estrutura Atual

### Frontend React (Principal)
- **Localização**: `/src/frontend/`
- **Tecnologias**: React 18, TypeScript, Vite, Material-UI
- **Build**: `/src/frontend/dist/` → Publicado na raiz `/`

### Páginas Migradas

Todas as funcionalidades das antigas páginas Python foram migradas para componentes React:

| Funcionalidade Antiga | Componente React | Rota |
|------------------------|------------------|------|
| Dashboard Principal | `Dashboard.tsx` | `/dashboard` |
| Gestão da Folha | `PayrollPage.tsx` | `/payroll/*` |
| Gerenciamento de Usuários | `GerenciamentoUsuarios.tsx` | `/gestao/usuarios` |
| Portal de Demandas | `PortalDemandas.tsx` | `/demandas` |
| Consultor de Riscos | `ConsultorRiscos.tsx` | `/consultor-riscos` |
| Gestão de Clientes | `GestaoClientes.tsx` | `/gestao/clientes` |
| Gestão de Contabilidades | `GestaoContabilidades.tsx` | `/gestao/contabilidades` |
| Relatórios Avançados | `RelatoriosAvancados.tsx` | `/relatorios/avancados` |
| Configurações | `Templates.tsx` | `/configuracoes/templates` |
| Minha Conta | `MinhaConta.tsx` | `/configuracoes/minha-conta` |
| CCT | `CCTPage.tsx` | `/cct/*` |
| Auditoria | `AuditPage.tsx` | `/audit/*` |
| Documentos | `DocumentsPage.tsx` | `/documents/*` |
| Chatbot | `ChatbotPage.tsx` | `/chatbot` |

## Navegação e Arquitetura

### Estrutura de Navegação
- **OPERAÇÃO**: Dashboard, Portal de Demandas, Consultor de Riscos
- **GESTÃO**: Clientes, Usuários, Contabilidades  
- **RELATÓRIOS**: Relatórios Avançados
- **CONFIGURAÇÕES**: Minha Conta, Templates

### Roteamento SPA
- **Router**: React Router v6
- **Lazy Loading**: Componentes carregados sob demanda
- **Fallbacks**: Loading spinners durante carregamento

## Configuração do Servidor

### Apache (.htaccess)
```apache
# Configuração para SPA React
Options -MultiViews
RewriteEngine On

# Redireciona todas as rotas para index.html
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]

# Cache de assets estáticos
<IfModule mod_expires.c>
    ExpiresActive on
    ExpiresByType text/css "access plus 1 year"
    ExpiresByType application/javascript "access plus 1 year"
</IfModule>

# Previne acesso a arquivos internos
RedirectMatch 404 ^/src/.*$
RedirectMatch 404 ^/node_modules/.*$
```

### Nginx (nginx.conf.example)
```nginx
server {
    listen 80;
    root /path/to/your/app;
    index index.html;

    # Assets estáticos com cache
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Roteamento SPA
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Bloqueia acesso a arquivos internos
    location ~ ^/(src|node_modules)/ {
        return 404;
    }
}
```

## Desenvolvimento

### Estrutura de Arquivos
```
src/frontend/
├── src/
│   ├── components/     # Componentes reutilizáveis
│   ├── pages/         # Páginas principais  
│   ├── stores/        # Estado global (Zustand)
│   ├── services/      # Integração com APIs
│   ├── hooks/         # Custom hooks
│   └── styles/        # Estilos globais
├── package.json       # Dependências
└── vite.config.ts     # Configuração do bundler
```

### Scripts Disponíveis
```bash
# Desenvolvimento
npm run dev          # Servidor de desenvolvimento

# Build de produção  
npm run build        # Gera build otimizado

# Testes
npm run test         # Executa testes
npm run test:coverage # Cobertura de testes

# Qualidade de código
npm run lint         # ESLint
npm run format       # Prettier
```

## Deployment

### Build e Publicação
1. **Build**: `cd src/frontend && npm run build`
2. **Deploy**: Copiar conteúdo de `dist/` para raiz pública
3. **Configuração**: Aplicar configuração de servidor (.htaccess/nginx)

### Processo Automatizado
```bash
# Build automático
cd src/frontend
npm ci                    # Instala dependências
npm run build            # Gera build
cp -r dist/* ../..       # Copia para raiz
```

## Monitoramento e Troubleshooting

### Logs e Debug
- **Console do Browser**: Errors e warnings aparecem no DevTools
- **Network Tab**: Monitorar requisições para API
- **React DevTools**: Debug de componentes e estado

### Problemas Comuns

#### 1. Página 404 em Refresh
**Causa**: Servidor não configurado para SPA
**Solução**: Aplicar configuração de rewrite rules

#### 2. Assets Não Carregam
**Causa**: Caminhos incorretos ou cache
**Solução**: Verificar build e limpar cache

#### 3. API Inacessível  
**Causa**: CORS ou endpoint incorreto
**Solução**: Verificar configuração da API

## Segurança

### Medidas Implementadas
- **Headers de Segurança**: CSP, XSS Protection
- **Bloqueio de Arquivos**: Source maps e arquivos internos
- **Sanitização**: Inputs validados
- **Autenticação**: Sistema de auth integrado

### Arquivos Protegidos
- `/src/` - Código fonte não exposto
- `/node_modules/` - Dependências não expostas  
- `*.map` - Source maps bloqueados em produção

## Manutenção Futura

### Adicionando Novas Páginas
1. Criar componente em `/src/frontend/src/pages/`
2. Adicionar rota em `App.tsx`
3. Adicionar link na navegação se necessário
4. Fazer build e deploy

### Atualizações de Dependências
```bash
npm audit              # Verificar vulnerabilidades
npm update             # Atualizar dependências
npm run test           # Validar após atualizações
```

### Backup e Recovery
- **Código**: Versionado no Git
- **Build**: Pode ser regenerado a partir do código
- **Configuração**: Documentada neste guia

## Compatibilidade

### Navegadores Suportados
- Chrome 90+
- Firefox 88+  
- Safari 14+
- Edge 90+

### Dispositivos
- Desktop: Totalmente suportado
- Tablet: Responsivo 
- Mobile: Layout adaptado

---

## Contato e Suporte

Para questões sobre a migração ou funcionamento do sistema:
1. Verificar este guia primeiro
2. Consultar logs do navegador
3. Verificar configuração do servidor
4. Contatar equipe de desenvolvimento

*Última atualização: 31/07/2025*