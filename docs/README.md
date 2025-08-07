# 📚 AUDITORIA360 - Documentação Central

Bem-vindo ao centro de documentação do projeto AUDITORIA360. Este índice organiza toda a documentação disponível para facilitar a navegação e onboarding de novos membros da equipe.

## 🚀 Início Rápido

### Para Novos Desenvolvedores:
1. **[Guia de Onboarding](onboarding_guide.md)** - Primeiros passos no projeto
2. **[README Principal](../README.md)** - Visão geral e instalação
3. **[Guia de Contribuição](../CONTRIBUTING.md)** - Como contribuir para o projeto

### Para Deploy e Produção:
1. **[Guia de Deploy](../deploy/)** - Arquivos e processos de deployment
2. **[Monitoramento](../monitoring/)** - Dashboards e métricas
3. **[Scripts de Automação](../scripts/)** - Ferramentas de automação

## 📖 Documentação Técnica

### Arquitetura e Decisões:
- **[ADRs (Architecture Decision Records)](adr/)** - Decisões arquiteturais documentadas
- **[Análise de Tecnologias](TECHNOLOGY_STACK_ANALYSIS.md)** - Análise detalhada das stacks utilizadas
- **[Lógica de Negócio](business_logic/)** - Documentação das regras de negócio

### Relatórios e Análises:
- **[Histórico do Projeto](historico/)** - Evolução e marcos históricos
- **[Relatórios Gerados](generated/)** - Documentação auto-gerada
- **[Metamorfose Final](../METAMORFOSE_RELATORIO_FINAL.md)** - Relatório de transformação do projeto

## 🛠️ Guias Técnicos

### Backend (Python/FastAPI):
- **[API Documentation](../api/)** - Estrutura e endpoints da API
- **[Migrações de Banco](../migrations/)** - Scripts de migração de dados
- **[Configuração](../config/)** - Arquivos de configuração

### Frontend (React/TypeScript):
- **[Frontend](../src/frontend/)** - Aplicação React
- **[Componentes](../frontend/)** - Estrutura de componentes
- **[Assets](../assets/)** - Recursos estáticos

### DevOps:
- **[Docker](../Dockerfile)** - Configuração de containers
- **[Kubernetes](../deploy/kubernetes/)** - Configuração de orquestração
- **[CI/CD](../.github/workflows/)** - Pipelines de integração contínua

## 🧪 Testes e Qualidade

### Estrutura de Testes:
- **[Testes Unitários](../tests/unit/)** - Testes de unidade
- **[Testes de Integração](../tests/integration/)** - Testes de integração
- **[Testes E2E](../tests/e2e/)** - Testes end-to-end
- **[Testes de Performance](../tests/performance/)** - Testes de performance
- **[Testes de Segurança](../tests/security/)** - Validações de segurança

### Qualidade de Código:
- **[Makefile](../Makefile)** - Comandos de automação e qualidade
- **[Pre-commit](../.pre-commit-config.yaml)** - Hooks de qualidade
- **[Configuração Flake8](../.flake8)** - Linting Python

## 💡 Exemplos e Demos

### Exemplos de Uso:
- **[Exemplos de API](../examples/)** - Como usar as APIs do sistema (com README detalhado)
- **[Demos](../demos/)** - Demonstrações completas e avançadas (com README detalhado)
- **[Notebooks](../notebooks/)** - Análises e explorações de dados

### Estrutura Organizada:
- **Examples**: Foco em APIs específicas, código didático, para desenvolvedores
- **Demos**: Showcases completos, múltiplas integrações, para stakeholders e apresentações

### Scripts Utilitários:
- **[Scripts Python](../scripts/python/)** - Utilitários em Python
- **[Scripts Shell](../scripts/shell/)** - Automação em Shell
- **[Scripts PowerShell](../scripts/powershell/)** - Automação Windows

## 🔧 Ferramentas e Utilitários

### Scripts de Automação:
- **[Master Checklist](../scripts/master_execution_checklist.py)** - Validação completa do sistema
- **[Quick Checklist](../scripts/quick_checklist.py)** - Validação rápida
- **[Gerador de Docs](../scripts/genesis_docs_generator.py)** - Geração automática de documentação

### Validação e Relatórios:
- **[Validação de Produção](../scripts/validate_production_deploy.py)** - Testes de produção
- **[Análise de Repositório](../scripts/repository_analysis.py)** - Análise estrutural
- **[Validação de CI](../scripts/validate_ci.py)** - Validação de pipelines

## 📊 Monitoramento e Observabilidade

### Dashboards:
- **[Grafana Dashboards](../monitoring/)** - Métricas e alertas
- **[Prometheus Config](../docker-compose.monitoring.yml)** - Configuração de métricas

### Performance:
- **[Otimização](PERFORMANCE_OPTIMIZATION_STRATEGY.md)** - Estratégias de performance
- **[Validação Quantum](QUANTUM_VALIDATION.md)** - Validações avançadas
- **[Inteligência de Enxame](SWARM_INTELLIGENCE.md)** - Algoritmos distribuídos

## 🔄 Versionamento e Releases

### Estratégia de Versionamento:
- **Semântico**: Major.Minor.Patch (ex: 1.0.0)
- **Tags Git**: Para marcar releases
- **CHANGELOG**: Documentação de mudanças

### Processo de Release:
1. Atualizar versão em `pyproject.toml` e `package.json`
2. Executar testes completos
3. Criar tag Git
4. Deploy automático via GitHub Actions

## 🆘 Suporte e Troubleshooting

### Problemas Comuns:
- **Falhas de Build**: Verificar dependências e versões
- **Testes Falhando**: Executar `make test` e verificar logs
- **Deploy Issues**: Consultar logs do CI/CD

### Contato:
- **Email**: dev@auditoria360.com.br
- **Issues**: GitHub Issues do repositório
- **Documentação**: Este diretório docs/

---

## 📝 Como Contribuir para a Documentação

1. **Atualize** este índice ao adicionar novos documentos
2. **Mantenha** links atualizados e funcionais
3. **Documente** novas funcionalidades e decisões
4. **Siga** os padrões de nomenclatura estabelecidos

### Estrutura de Documentos:
```
docs/
├── README.md (este arquivo - índice central)
├── TECHNOLOGY_STACK_ANALYSIS.md (análise técnica)
├── onboarding_guide.md (guia para novos membros)
├── adr/ (decisões arquiteturais)
├── business_logic/ (regras de negócio)
├── generated/ (docs auto-geradas)
└── historico/ (evolução do projeto)
```

---

**Última atualização**: $(date)
**Versão**: 1.0.0
**Mantido por**: AUDITORIA360 Team