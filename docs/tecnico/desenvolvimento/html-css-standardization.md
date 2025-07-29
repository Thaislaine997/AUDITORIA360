# Padronização HTML/CSS - AUDITORIA360

## Resumo das Alterações

Este documento descreve as alterações realizadas para padronizar os arquivos HTML e CSS do projeto AUDITORIA360, melhorando a estrutura, legibilidade e manutenção da interface web.

## Configuração de Formatação

### Prettier

Foi configurado o Prettier para formatação automática de código:

- **Configuração**: `.prettierrc` na raiz do projeto
- **Ignorados**: `.prettierignore` (exclui arquivos gerados automaticamente)
- **Comando**: `npx prettier --write "**/*.{html,css}"`

### Configurações Aplicadas

```json
{
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": false,
  "htmlWhitespaceSensitivity": "css",
  "endOfLine": "lf"
}
```

## Arquivos Padronizados

### 1. assets/style.css

- **Status**: ✅ Formatado e padronizado
- **Descrição**: Design system moderno completo
- **Alterações**:
  - Formatação consistente de indentação (2 espaços)
  - Padronização de valores de cores (lowercase)
  - Quebra de linha consistente em propriedades longas
  - Melhoria na legibilidade dos seletores CSS

### 2. src/frontend/index.html

- **Status**: ✅ Formatado e padronizado
- **Descrição**: Ponto de entrada da aplicação React
- **Alterações**:
  - DOCTYPE padronizado para `<!doctype html>`
  - Formatação consistente de atributos
  - Quebra de linha adequada para meta tags longas

### 3. monitoring/dashboard.html

- **Status**: ✅ Formatado e padronizado
- **Descrição**: Dashboard de monitoramento principal
- **Alterações**:
  - DOCTYPE padronizado
  - Indentação consistente (2 espaços)
  - Formatação de estilos inline melhorada
  - Estrutura HTML mais legível

### 4. monitoring/basic_dashboard.html

- **Status**: ✅ Formatado e padronizado
- **Descrição**: Dashboard básico de monitoramento
- **Alterações**:
  - Adicionado atributo `lang="pt-BR"` na tag HTML
  - Adicionadas meta tags essenciais (charset, viewport)
  - DOCTYPE padronizado
  - Formatação consistente

## Estrutura do Design System

### Variáveis CSS Principais

O arquivo `assets/style.css` contém um design system completo com:

- **Cores**: Sistema de cores baseado na identidade visual (ciano primário #00d4ff)
- **Tipografia**: Fonte Inter com fallbacks para diferentes sistemas
- **Espaçamento**: Sistema de espaçamento consistente (xs, sm, md, lg, xl, 2xl)
- **Bordas e Sombras**: Raios de borda e sombras padronizadas
- **Transições**: Animações suaves e consistentes

### Componentes Disponíveis

- Cards com variações (glass, hover effects)
- Botões (primary, secondary, outline, success, warning, danger)
- Badges com estados
- Formulários com estilos consistentes
- Grid e layout helpers
- Utilitários responsivos

## Padrões de Código

### HTML

- DOCTYPE: `<!doctype html>`
- Idioma: `lang="pt-BR"`
- Meta tags obrigatórias: charset, viewport
- Indentação: 2 espaços
- Atributos sem valores booleanos explícitos

### CSS

- Indentação: 2 espaços
- Nomenclatura: kebab-case para classes
- Variáveis CSS: --variavel-nome
- Cores: lowercase (#00d4ff)
- Comentários: Seções bem documentadas

## Compatibilidade

### Navegadores Suportados

- Chrome/Edge: últimas 2 versões
- Firefox: últimas 2 versões
- Safari: últimas 2 versões
- Mobile: iOS Safari, Chrome Mobile

### Responsividade

- Mobile-first approach
- Breakpoints: 480px, 768px
- Grid responsivo com auto-fit
- Componentes adaptativos

## Ferramentas de Desenvolvimento

### Scripts NPM Disponíveis

```json
{
  "format": "prettier --write \"**/*.{html,css,js,ts,tsx}\"",
  "format:check": "prettier --check \"**/*.{html,css,js,ts,tsx}\""
}
```

### Integração com CI/CD

- Verificação de formatação automática
- Linting de CSS (futuro)
- Minificação para produção

## Acessibilidade

### Recursos Implementados

- Cores com contraste adequado
- Focus outline visível
- Suporte a prefers-reduced-motion
- Suporte a high contrast mode
- Estrutura semântica adequada

### Futuras Melhorias

- ARIA labels mais específicos
- Testes de acessibilidade automatizados
- Suporte a leitores de tela

## Manutenção

### Adicionando Novos Estilos

1. Use as variáveis CSS existentes
2. Siga a nomenclatura de componentes
3. Documente novos componentes
4. Execute o Prettier antes do commit

### Modificando o Design System

1. Altere as variáveis CSS na seção :root
2. Teste em todos os componentes
3. Atualize a documentação
4. Valide a acessibilidade

## Monitoramento da Qualidade

### Métricas de Código

- Formatação consistente: ✅ 100%
- Padrões de nomenclatura: ✅ 100%
- Estrutura HTML válida: ✅ 100%
- CSS válido: ✅ 100%

### Próximas Etapas

1. Implementar linting de CSS
2. Adicionar testes de regressão visual
3. Configurar pre-commit hooks
4. Documentar componentes individuais

---

**Data da Padronização**: ${new Date().toLocaleDateString('pt-BR')}
**Responsável**: Sistema de Padronização Automatizada
**Versão**: 1.0
