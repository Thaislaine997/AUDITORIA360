# A Arquitetura Alvo do Ecossistema Kairós

Este documento é a constituição e a fonte única da verdade para a arquitetura do projeto AUDITORIA360 na sua Era Kairós. Ele serve como o "histórico base" para auditoria e desenvolvimento futuro.

### Princípios Fundamentais
1.  **Unificação Total:** Uma única SPA Frontend, uma única API Backend. Nenhuma tecnologia ou estrutura legada ativa.
2.  **Profissionalismo Corporativo:** A UI/UX é clara, eficiente, densa em informação e estritamente profissional.
3.  **Segurança "Zero-Trust":** Arquitetura multi-tenant com isolamento de dados rigoroso em todas as camadas.
4.  **Testabilidade Comprovada:** Cobertura de testes mínima de 85% para todo o código novo.
5.  **Documentação Viva:** A Wiki do GitHub, sincronizada via "Docs-as-Code", é a única fonte de documentação.

### Estrutura de Diretórios Final
/
├── .github/                 # Workflows de CI/CD e governança
├── backend/                 # Aplicação unificada em Python (FastAPI/Poetry)
│   └── src/
│       ├── modules/         # Módulos de negócio (clientes, auth, payroll, etc.)
│       └── ...
├── frontend/                # SPA em React (Vite/TypeScript)
│   └── src/
│       ├── components/      # Componentes UI (baseados em um Design System)
│       └── ...
├── infra/                   # Configurações de infraestrutura (Docker, Nginx, etc.)
├── docs-source/             # Fonte da verdade para a Wiki
├── legacy_dashboards/       # Aplicação Streamlit legada, marcada para depreciação
├── scripts/                 # Scripts de utilidade e deploy
└── tests/                   # Suíte de testes completa

### Stack Tecnológica Canônica
* **Backend:** Python 3.11+, FastAPI, Poetry, SQLAlchemy, Pytest.
* **Frontend:** TypeScript, React 18+, Vite, Zustand, React Testing Library, Material-UI.
* **Banco de Dados:** PostgreSQL.
* **Cache:** Redis.
* **Infraestrutura:** Docker.

### Módulos de Negócio Essenciais (Pós-Simplificação)
* **Dashboard Corporativo:** KPIs, Data Grids de alta performance, gráficos.
* **Controle de Folha de Pagamento:** Módulo central baseado na planilha, com o fluxo de trabalho mensal.
* **Gestão de Empresas:** CRUD de empresas.
* **Gestão de Funcionários (Simplificado):** CRUD com os 7 campos essenciais.
* **Serviços Extras:** Registro de serviços adicionais.
* **Auditoria e LGPD:** Logs de alteração.

### Processos de DevOps Mandatórios
* **CI/CD:** Pipeline automatizado no GitHub Actions para lint, teste, build e deploy.
* **Pre-commit Hooks:** Formatação e linting automáticos antes de cada commit.
* **"Docs-as-Code":** Sincronização automática da pasta `/docs-source` com a Wiki.