# Guia de Onboarding - AUDITORIA360

## 🌟 Bem-vindo ao Ecossistema AUDITORIA360

Este guia foi projetado para acelerar seu onboarding e transformar você em um contribuidor produtivo no menor tempo possível. Nossa abordagem prioriza a **compreensão holística** antes do mergulho nos detalhes técnicos.

## 🎯 Filosofia do Onboarding

> "Compreender o todo antes das partes permite decisões mais sábias e contribuições mais efetivas."

Seguimos uma abordagem **top-down** que prioriza:
1. **Visão Sistêmica** - Como os componentes se relacionam
2. **Context First** - Por que as decisões foram tomadas
3. **Hands-on Gradual** - Prática progressiva com complexidade crescente

## 📋 Checklist de Onboarding

### Dia 1: Consciência Holística 🧠
- [ ] **PRIORIDADE #1**: Explorar o [Diagrama de Vitalidade Sistêmica](#diagrama-de-vitalidade)
- [ ] Ler o [README.md](../README.md) do projeto
- [ ] Assistir apresentação executiva (30min)
- [ ] Setup do ambiente de desenvolvimento
- [ ] Primeiro commit: adicionar seu nome ao `CONTRIBUTORS.md`

### Dia 2-3: Arquitetura e Decisões 🏗️
- [ ] Estudar [Architecture Decision Records (ADRs)](adr/README.md)
- [ ] Compreender a [arquitetura de dados](adr/001-escolha-da-arquitetura-de-dados-descentralizada-com-duckdb.md)
- [ ] Explorar o [sistema MCP](adr/002-implementacao-sistema-mcp-multi-agente.md)
- [ ] Revisar a [estratégia API-as-a-Product](adr/003-estrategia-api-as-a-product.md)
- [ ] Reunião 1:1 com mentor técnico (45min)

### Semana 1: Exploração Guiada 🗺️
- [ ] Executar suite de testes completa
- [ ] Navegar pelo código com foco na [documentação de negócio](business_logic/README.md)
- [ ] Configurar ferramentas de desenvolvimento
- [ ] Participar da reunião de retrospectiva da equipe
- [ ] Completar primeira tarefa: correção de bug simples

### Semana 2: Contribuição Ativa 🚀
- [ ] Implementar nova funcionalidade pequena/média
- [ ] Realizar primeiro code review
- [ ] Apresentar sua primeira contribuição para a equipe
- [ ] Definir área de especialização/interesse

### Semana 3-4: Autonomia 🎓
- [ ] Liderar implementação de funcionalidade complexa
- [ ] Mentorear próximo novo membro (se aplicável)
- [ ] Contribuir para melhorias de processo/tooling
- [ ] Feedback completo do período de onboarding

## 🌊 Diagrama de Vitalidade Sistêmica

### Por que começar aqui?

O **Diagrama de Vitalidade** é sua porta de entrada para compreender o AUDITORIA360 de forma holística. Criado pelo ACH (Agente de Consciência Holística), ele oferece:

- **Visão em Tempo Real**: Estado atual de todos os componentes
- **Relações Visuais**: Como os módulos se comunicam e dependem uns dos outros
- **Métricas de Saúde**: Quais partes do sistema precisam de atenção
- **Histórico de Evolução**: Como o sistema cresceu e evoluiu

### Como acessar

1. **Localmente**: Execute `python scripts/python/run_holistic_consciousness_agent.py`
2. **Online**: [https://thaislaine997.github.io/AUDITORIA360/ach-reports/](https://thaislaine997.github.io/AUDITORIA360/ach-reports/)
3. **Via Dashboard**: Menu "Admin" → "System Health" → "Vitality Diagram"

### O que observar

```bash
# Execute e explore interativamente
$ python scripts/python/run_holistic_consciousness_agent.py

# Observe as seguintes seções no relatório:
# 1. System Overview - Saúde geral
# 2. Component Health - Estado de cada módulo
# 3. Integration Flow - Fluxo de dados
# 4. Critical Issues - Problemas que requerem atenção
# 5. Recommendations - Próximos passos sugeridos
```

### Exercício Prático

Após explorar o diagrama, responda:
1. Qual é o componente com melhor "saúde" atualmente?
2. Identifique 3 integrações críticas do sistema
3. Quais são os 2 principais riscos apontados?
4. Que padrões você observa na evolução do sistema?

## 🏗️ Estrutura do Projeto

### Visão de Alto Nível

```
AUDITORIA360/
├── 🧠 src/mcp/              # Multi-Agent System (Cerebro)
├── 🎨 src/frontend/         # Interface React/TypeScript  
├── 🔧 src/services/         # Business Logic Core
├── 🗄️ src/api/             # REST API Layer
├── 📊 src/models/          # Data Models
├── 🔒 src/auth/            # Authentication & Security
├── ⚡ src/serverless/      # Serverless Functions
├── 📝 docs/                # Documentation
├── 🧪 tests/               # Test Suite
└── 📈 monitoring/          # Observability
```

### Fluxo de Dados Simplificado

```
Frontend (React) 
    ↓ HTTP/WebSocket
API Layer (FastAPI)
    ↓ Business Logic
Services Layer
    ↓ Database Queries
Models & Schemas
    ↓ Storage
PostgreSQL + DuckDB
```

## 🛠️ Configuração do Ambiente

### Pré-requisitos

```bash
# Python 3.12+ 
python --version  # >= 3.12

# Node.js 20+
node --version    # >= 20.0.0

# Git
git --version     # >= 2.30
```

### Setup Rápido

```bash
# 1. Clone e setup inicial
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# 2. Ambiente Python
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Ambiente Frontend
cd src/frontend
npm install
cd ../..

# 4. Configuração
cp .env.example .env
# Edite .env com suas configurações

# 5. Teste da instalação
python -m pytest tests/ --maxfail=3
npm test --prefix src/frontend
```

### Verificação da Instalação

```bash
# Execute o diagrama de vitalidade como teste final
python scripts/python/run_holistic_consciousness_agent.py

# Se tudo estiver correto, você verá:
# ✅ Genomic census completed
# ✅ Vital pulse analysis completed  
# ✅ Systemic vitality diagram generated
```

## 📚 Recursos de Aprendizado

### Documentação Essencial (Order de Prioridade)

1. **[Diagrama de Vitalidade](#diagrama-de-vitalidade)** - Comece aqui SEMPRE
2. **[ADRs](adr/README.md)** - Decisões arquiteturais e contexto
3. **[Business Logic Docs](business_logic/README.md)** - Regras de negócio
4. **[API Documentation](../api/README.md)** - Contratos e endpoints
5. **[Frontend Guide](../src/frontend/README.md)** - Interface e UX

### Codebase Navigation Tips

```bash
# Encontrar componentes por funcionalidade
find . -name "*payroll*" -type f
find . -name "*audit*" -type f
find . -name "*user*" -type f

# Explorar dependências
grep -r "import.*services" src/
grep -r "from.*models" src/

# Entender fluxos críticos
grep -r "def.*calculate" src/services/
grep -r "async def.*process" src/
```

### Ferramentas de Desenvolvimento

```bash
# Formatação de código
black . && isort .

# Linting
flake8 .

# Testes com coverage
pytest --cov=src tests/

# Análise de qualidade
python scripts/python/semantic_intent_validator.py src/services/*.py
```

## 🎯 Primeiras Contribuições

### Tarefas Ideais para Novos Membros

1. **Documentação**: Melhorar documentação de APIs
2. **Testes**: Adicionar testes para código legado
3. **Bugs Simples**: Issues marcadas como "good-first-issue"
4. **Melhorias de UX**: Pequenos ajustes na interface
5. **Validações**: Adicionar validações em formulários

### Processo de Contribuição

```bash
# 1. Criar branch para sua funcionalidade
git checkout -b feature/sua-funcionalidade

# 2. Implementar mudanças
# ... código ...

# 3. Executar testes
pytest tests/
npm test --prefix src/frontend

# 4. Commit seguindo convenção
git commit -m "feat: adiciona validação de CPF em formulário"

# 5. Push e criar PR
git push origin feature/sua-funcionalidade
# Criar Pull Request no GitHub
```

## 🤝 Cultura e Práticas

### Nossos Valores

- **Excellence Through Simplicity**: Soluções elegantes e simples
- **Context-Driven Decisions**: Decisões baseadas em contexto e dados
- **Continuous Learning**: Aprendizado e evolução constantes
- **Human-Centric Technology**: Tecnologia que serve às pessoas

### Reuniões e Rituais

- **Daily Standups**: 9h, 15min máximo
- **Sprint Planning**: Quinzenal, 2h
- **Retrospectives**: Quinzenal, 1h
- **Architecture Reviews**: Mensal, 2h
- **Demo Sessions**: Mensal, 1h

### Comunicação

- **Slack**: Comunicação rápida e informal
- **GitHub Issues**: Tracking de bugs e features
- **Documentation**: Decisões importantes sempre documentadas
- **Code Reviews**: Toda mudança passa por review

## 🆘 Suporte e Ajuda

### Canais de Suporte

1. **Mentor Técnico**: Seu mentor atribuído (primeira semana)
2. **Slack #onboarding**: Canal dedicado para novos membros
3. **Slack #architecture**: Dúvidas sobre arquitetura e decisões
4. **Slack #general**: Dúvidas gerais e discussões

### FAQ Rápido

**Q: Como entender um erro estranho no sistema?**
A: Consulte primeiro o Diagrama de Vitalidade, depois os logs do componente específico.

**Q: Preciso entender todo o código antes de contribuir?**
A: Não! Comece pelo Diagrama de Vitalidade e focalize no componente que você está modificando.

**Q: Como sei se minha mudança pode quebrar algo?**
A: Execute os testes e verifique no Diagrama de Vitalidade se há degradação de saúde.

**Q: Devo perguntar ou tentar descobrir sozinho?**
A: Tente por 30min, depois pergunte. Valorizamos autonomia E colaboração.

## 🎓 Conclusão

Este onboarding foi projetado para te transformar em um contribuidor efetivo rapidamente, priorizando **compreensão** sobre **memorização**. 

Lembre-se: o **Diagrama de Vitalidade** é sua bússola - sempre que se sentir perdido, volte a ele para reorientar sua compreensão do sistema.

**Próximo passo**: Explore o Diagrama de Vitalidade agora mesmo!

---

*Última atualização: 2025-01-20*  
*Feedback: Slack #onboarding ou abra uma issue*