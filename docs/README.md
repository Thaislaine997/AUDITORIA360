# 📚 Documentação AUDITORIA360

Bem-vindo à documentação completa do sistema AUDITORIA360!

## 📂 Estrutura da Documentação Reorganizada

### 📖 [content/](./content/)
Documentação principal do projeto, incluindo guias técnicos, manuais de usuário e relatórios de desenvolvimento.

### 📊 [relatorios/](./relatorios/)
Relatórios centralizados do sistema, incluindo:
- Relatórios de auditoria e análise
- Status de implementação e validação  
- Logs de monitoramento
- Relatórios de changelog e execução

### 🔍 [analises/](./analises/)
Análises detalhadas do repositório e sistema:
- Análises de estrutura de código
- Relatórios de análise de repositório
- Dados de análise em formato JSON

### 📖 [manuais/](./manuais/)
Manuais e documentação operacional:
- Manuais de usuário
- Guias de instalação
- Documentação de produção
- Procedimentos operacionais

### 🏗️ [sphinx/](./sphinx/)
Documentação técnica gerada automaticamente usando Sphinx para APIs e módulos Python.

### 🛠️ [tecnico/](./tecnico/)
Documentação técnica específica e exemplos práticos de uso.

## 🚀 Links Rápidos

- **[Início Rápido](./content/01-INICIO_RAPIDO.md)** - Guia para começar rapidamente
- **[Índice Principal](./content/00-INDICE_PRINCIPAL.md)** - Navegação completa
- **[Documentação de APIs](./content/api/intro.md)** - Referência de APIs
- **[Manuais de Usuário](./content/usuario/manual-usuario.md)** - Guias para usuários finais
- **[Guias Técnicos](./content/tecnico/desenvolvimento/dev-guide.md)** - Para desenvolvedores

## 📊 Relatórios e Status Centralizados

- **[CHANGELOG](./relatorios/CHANGELOG.md)** - Histórico de mudanças
- **[Relatório de Auditoria Abrangente](./relatorios/COMPREHENSIVE_AUDIT_REPORT.md)** - Auditoria completa
- **[Relatório de Validação Final](./relatorios/FINAL_VALIDATION_REPORT.md)** - Validação final
- **[Status do Projeto](./content/relatorios/status-projeto.md)** - Status atual de implementação
- **[Relatório Unificado](./content/relatorios/relatorio-unificado.md)** - Relatório consolidado
- **[Performance](./content/relatorios/performance.md)** - Métricas de desempenho

## 🔍 Análises e Diagnósticos

- **[Análise do Repositório](./analises/REPOSITORY_ANALYSIS_REPORT.md)** - Análise detalhada
- **[Dados de Análise](./analises/repository_analysis_report.json)** - Dados estruturados

## 📖 Manuais e Produção

- **[Preparação para Produção](./manuais/PRODUCTION_READINESS.md)** - Guia de produção

## 🔧 Documentação Técnica

- **[Arquitetura Geral](./content/tecnico/arquitetura/visao-geral.md)** - Visão geral da arquitetura
- **[Banco de Dados](./content/tecnico/banco-dados/cloudsql_integracao.md)** - Configuração de BD
- **[Deploy](./content/tecnico/deploy/deploy-checklist.md)** - Processo de deployment

## 📚 Como Navegar

1. **Para usuários finais**: Comece pelos [Manuais de Usuário](./content/usuario/)
2. **Para desenvolvedores**: Veja os [Guias Técnicos](./content/tecnico/)
3. **Para administradores**: Consulte a [Documentação de Deploy](./content/tecnico/deploy/)
4. **Para análise**: Veja os [Relatórios](./relatorios/) e [Análises](./analises/)
5. **Para procedimentos**: Consulte os [Manuais](./manuais/)

## 🏗️ Gerando Documentação

Para gerar a documentação Sphinx:

```bash
make docs-build
```

Para servir localmente:

```bash
make docs-serve
```

## 📝 Contribuindo

Ao adicionar nova documentação:

1. Coloque arquivos técnicos em `content/tecnico/`
2. Coloque relatórios em `relatorios/`
3. Coloque análises em `analises/`
4. Coloque manuais de usuário em `manuais/`
5. Atualize este README com novos links importantes

## 🔄 Reorganização Realizada

Esta estrutura foi reorganizada para:
- ✅ **Centralizar documentos dispersos** - Movidos do diretório raiz
- ✅ **Eliminar duplicação** - Consolidação de docs/content/ e docs/documentos/
- ✅ **Padronizar estrutura** - Diretórios específicos por tipo
- ✅ **Facilitar navegação** - Organização lógica e intuitiva

---

> 🎯 **Objetivo**: Manter toda documentação centralizada, organizada e facilmente navegável para todos os stakeholders do projeto.