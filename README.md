# AUDITORIA360 🔍 - Era Kairós

> **Plataforma Integrada de Auditoria, Gestão da Folha e Compliance - Pós-Gênesis**

[![Status](https://img.shields.io/badge/status-Era%20Kairós-success.svg)]()
[![Gênesis](https://img.shields.io/badge/Projeto%20Gênesis-✅%20Concluído-brightgreen)]()
[![Wiki](https://img.shields.io/badge/docs-Wiki%20Oficial-blue.svg)](https://github.com/Thaislaine997/AUDITORIA360/wiki)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()

## 🚀 Início Rápido

### Pré-requisitos
- Node.js 18+ | Python 3.12+ | Docker (opcional)

### Configuração Básica
```bash
# 1. Clone do repositório
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# 2. Backend (FastAPI)
pip install -r requirements.txt
cp .env.template .env  # Configure suas variáveis
python test_api_server.py

# 3. Frontend (React)
cd src/frontend
npm install && npm run dev
```

### Acesso
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8001  
- **Docs API**: http://localhost:8001/docs

**Usuários de teste:**
- Admin: `admin` / `admin123`
- Contabilidade: `contabilidade` / `conta123`

## 📚 Documentação Completa

📖 **IMPORTANTE: Toda a documentação foi centralizada na [Wiki Oficial](https://github.com/Thaislaine997/AUDITORIA360/wiki)**

### 🗂️ Navegação Rápida
- 🎯 **[Visão e Estratégia](https://github.com/Thaislaine997/AUDITORIA360/wiki/Vision-and-Strategy)** - Roadmap, decisões de arquitetura, status do projeto
- 👨‍💻 **[Guias de Desenvolvedor](https://github.com/Thaislaine997/AUDITORIA360/wiki/Developer-Guides)** - Setup completo, padrões, arquitetura, contribuição
- 🚀 **[Operações e Deploy](https://github.com/Thaislaine997/AUDITORIA360/wiki/Operations-Deploy)** - Deploy, troubleshooting, monitoramento, migração
- 👤 **[Manuais de Usuário](https://github.com/Thaislaine997/AUDITORIA360/wiki/User-Manuals)** - Primeiros passos, guia completo, FAQ
- 🔌 **[Referência da API](https://github.com/Thaislaine997/AUDITORIA360/wiki/API-Reference)** - Autenticação, endpoints, modelos de dados

## 🏆 Status do Projeto - Era Kairós

### ✅ **PROJETO GÊNESIS OFICIALMENTE CONCLUÍDO** (Julho 2025)
- **PR #108-111**: Refatoração abrangente, auditoria, certificação e execução ✅ **CONCLUÍDAS**

### 🌟 **ERA KAIRÓS ATIVA** (Agosto 2025)
- ⚡ **Arquitetura Unificada**: Backend Python + SPA React exclusivamente
- 🔒 **Segurança Robusta**: Multi-tenant + RBAC implementados  
- 🗑️ **Legado Eliminado**: Streamlit removido, código simplificado
- 📊 **Modelo Simplificado**: Funcionários com 7 campos essenciais
- 🎯 **Interface Corporativa**: UI profissional focada em eficiência
- 📈 **Performance Otimizada**: < 100ms (p95)

## 🛠️ Stack Tecnológica

### Frontend
**React 18** + TypeScript + Material-UI + Zustand + Vite

### Backend  
**Python 3.12** + FastAPI + SQLAlchemy + PostgreSQL + DuckDB + Redis

### Infraestrutura
**Docker** + GitHub Actions + Cloudflare + Prometheus + Grafana

## 🧪 Comandos Úteis

```bash
# Testes
make test                 # Executar todos os testes
make test-coverage        # Testes com cobertura
make lint                 # Linting do código

# Deploy
make build               # Build da aplicação
make deploy              # Deploy completo
make checklist           # Validação do Master Checklist
```

## 🤝 Contribuição

1. Consulte o **[Guia de Contribuição](https://github.com/Thaislaine997/AUDITORIA360/wiki/Developer-Guides/Contributing)** na Wiki
2. Faça fork do projeto
3. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
4. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
5. Push para a branch (`git push origin feature/AmazingFeature`)
6. Abra um Pull Request

## 📞 Suporte

- **📖 Wiki**: [Documentação Completa](https://github.com/Thaislaine997/AUDITORIA360/wiki)
- **💬 Issues**: [GitHub Issues](https://github.com/Thaislaine997/AUDITORIA360/issues)
- **📧 Email**: suporte@auditoria360.com
- **🔧 Troubleshooting**: [Guia na Wiki](https://github.com/Thaislaine997/AUDITORIA360/wiki/Operations-Deploy/Troubleshooting)

---

**📝 Nota**: Esta documentação README foi simplificada como parte do **Projeto Alexandria** - migração da documentação para a Wiki. Para informações detalhadas, consulte sempre a **[Wiki Oficial](https://github.com/Thaislaine997/AUDITORIA360/wiki)**.

**Desenvolvido com ❤️ pela equipe AUDITORIA360** | *"Transformando a auditoria trabalhista através da tecnologia"*