# Versionamento Semântico - AUDITORIA360

## Estratégia de Versionamento

O projeto AUDITORIA360 adota o **Versionamento Semântico (SemVer)** seguindo o padrão MAJOR.MINOR.PATCH.

### Formato de Versão: X.Y.Z

- **MAJOR (X)**: Mudanças que quebram compatibilidade com versões anteriores
- **MINOR (Y)**: Adição de funcionalidades de forma compatível com versões anteriores  
- **PATCH (Z)**: Correções de bugs que mantêm compatibilidade

### Exemplos:

- `1.0.0` → `1.0.1` (correção de bug)
- `1.0.1` → `1.1.0` (nova funcionalidade)
- `1.1.0` → `2.0.0` (mudança que quebra compatibilidade)

## Implementação Atual

### Arquivos de Versão:
- **Backend**: `pyproject.toml` (projeto Python)
- **Frontend**: `package.json` (projeto Node.js)
- **Sistema**: Tags Git para releases

### Versão Atual:
- **Sistema**: 1.0.0
- **Backend API**: 1.0.0  
- **Frontend**: 1.0.0

## Processo de Release

### 1. Preparação:
```bash
# Executar testes completos
make test

# Validar qualidade do código
make check

# Executar checklist completo
make checklist-all
```

### 2. Atualização de Versão:
```bash
# Atualizar pyproject.toml
version = "1.1.0"

# Atualizar package.json
"version": "1.1.0"
```

### 3. Criação de Release:
```bash
# Commit das mudanças
git add .
git commit -m "chore: bump version to 1.1.0"

# Criar tag
git tag -a v1.1.0 -m "Release version 1.1.0"

# Push com tags
git push origin main --tags
```

### 4. Deploy Automático:
O GitHub Actions detecta novas tags e executa o deploy automático.

## Tipos de Mudanças

### PATCH (Z) - Correções:
- Correções de bugs
- Melhorias de performance sem mudanças de API
- Ajustes de documentação
- Correções de segurança menores

**Exemplo:** `1.0.0` → `1.0.1`
```
fix: corrigir cálculo de horas trabalhadas
docs: atualizar README com instruções de instalação
perf: otimizar consulta de relatórios
```

### MINOR (Y) - Funcionalidades:
- Novas funcionalidades compatíveis
- Melhorias na API mantendo compatibilidade
- Novos endpoints opcionais
- Novas configurações opcionais

**Exemplo:** `1.0.0` → `1.1.0`
```
feat: adicionar exportação de relatórios em Excel
feat: implementar notificações por email
feat: adicionar filtros avançados nos relatórios
```

### MAJOR (X) - Quebras de Compatibilidade:
- Mudanças na API que quebram compatibilidade
- Remoção de funcionalidades
- Mudanças nos formatos de dados
- Alterações nos endpoints existentes

**Exemplo:** `1.1.0` → `2.0.0`
```
BREAKING: alterar formato de resposta da API de relatórios
BREAKING: remover endpoint /api/v1/old-reports
BREAKING: atualizar esquema do banco de dados
```

## Convenções de Commit

### Tipos de Commit:
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação de código
- `refactor:` - Refatoração sem mudança de funcionalidade
- `test:` - Adição ou correção de testes
- `chore:` - Tarefas de build, configurações, etc.

### Formato:
```
<tipo>(<escopo>): <descrição>

<corpo da mensagem (opcional)>

<rodapé (opcional)>
```

### Exemplos:
```bash
feat(api): adicionar endpoint para exportação de relatórios
fix(frontend): corrigir validação de formulário de login
docs(readme): adicionar instruções de instalação do Docker
BREAKING CHANGE: alterar formato de resposta da API
```

## Automação com GitHub Actions

### Workflow de Release:
```yaml
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
```

### Detecção de Versão:
O sistema detecta automaticamente:
- Commits que indicam PATCH, MINOR ou MAJOR
- Tags de versão para triggers de deploy
- Mudanças nos arquivos de configuração

## CHANGELOG

### Formato:
Mantemos um arquivo `CHANGELOG.md` com todas as mudanças:

```markdown
# Changelog

## [1.1.0] - 2024-01-15
### Added
- Exportação de relatórios em Excel
- Notificações por email

### Fixed
- Cálculo de horas trabalhadas
- Validação de formulários

### Changed
- Interface de usuário mais intuitiva

## [1.0.0] - 2024-01-01
### Added
- Versão inicial do sistema
```

## Ambiente e Deploy

### Versionamento por Ambiente:
- **Development**: Versões `-dev` (ex: 1.1.0-dev)
- **Staging**: Versões `-rc` (ex: 1.1.0-rc.1)
- **Production**: Versões stable (ex: 1.1.0)

### Rollback:
```bash
# Rollback para versão anterior
git tag -d v1.1.0
git push --delete origin v1.1.0

# Deploy da versão anterior
git checkout v1.0.0
```

## Monitoramento de Versões

### Métricas:
- Tempo entre releases
- Número de patches por minor
- Compatibilidade entre versões
- Tempo de deploy por versão

### Dashboards:
- Grafana: métricas de versão em produção
- GitHub: histórico de releases
- API: endpoint `/version` com informações da versão atual

---

**Responsável**: AUDITORIA360 Team  
**Última atualização**: $(date)  
**Versão do documento**: 1.0.0