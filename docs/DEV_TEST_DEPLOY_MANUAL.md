# AUDITORIA360 - Manual de Desenvolvimento, Testes e Deploy

## Fluxo de Desenvolvimento

### Estrutura de Branches

```
main
├── develop
│   ├── feature/[ticket-id]-feature-name
│   ├── bugfix/[ticket-id]-bug-description
│   ├── hotfix/[ticket-id]-critical-fix
│   └── release/v[x.y.z]
```

### Processo de Feature Development

#### 1. Criação da Branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/AUD-123-new-audit-engine
```

#### 2. Desenvolvimento
- Seguir padrões de código estabelecidos
- Escrever testes unitários
- Documentar mudanças significativas
- Commits frequentes com mensagens descritivas

#### 3. Commit Guidelines
```bash
# Formato: tipo(escopo): descrição breve
feat(auditoria): adiciona novo motor de auditoria
fix(dashboard): corrige erro de carregamento dos gráficos
docs(api): atualiza documentação dos endpoints
test(simulador): adiciona testes unitários para simulações
```

#### 4. Pull Request
- Título: `[AUD-123] Nova funcionalidade de auditoria`
- Descrição usando template
- Labels apropriadas
- Reviewers obrigatórios

### Template de Pull Request

```markdown
## Descrição
[Breve descrição das mudanças]

## Ticket/Issue
Closes #[número] ou Link: [URL do ticket]

## Tipo de Mudança
- [ ] Bug fix (mudança que não quebra compatibilidade e corrige um problema)
- [ ] Feature (mudança que não quebra compatibilidade e adiciona funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentation update (documentação)

## Como Testar
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Screenshots (se UI)
[Adicionar screenshots das mudanças]

## Checklist
- [ ] Meu código segue o padrão de estilo do projeto
- [ ] Revisei meu próprio código
- [ ] Comentei o código em partes difíceis de entender
- [ ] Fiz mudanças correspondentes na documentação
- [ ] Minhas mudanças não geram novos warnings
- [ ] Adicionei testes que provam que minha correção/feature funciona
- [ ] Testes novos e existentes passam localmente
- [ ] Mudanças dependentes foram mergeadas e publicadas

## Impacto
- [ ] Performance
- [ ] Segurança  
- [ ] Compatibilidade
- [ ] Configuração
- [ ] Database migrations

## Reviewers
@[teammate1] @[teammate2]
```

## Ambiente Local - Setup

### Pré-requisitos
```bash
# Python 3.11+
python --version

# Node.js 18+
node --version

# Docker & Docker Compose
docker --version
docker-compose --version

# Git
git --version
```

### Setup do Backend
```bash
# Clone do repositório
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Environment variables
cp .env.template .env
# Editar .env com configurações locais

# Database setup (se local)
python setup_database.py

# Start API
uvicorn src.main:app --reload --port 8001
```

### Setup do Frontend
```bash
cd src/frontend
npm install

# Development server
npm run dev

# Build para produção
npm run build
```

### Docker Setup (Alternativo)
```bash
# Build e start todos os serviços
docker-compose up -d

# Logs
docker-compose logs -f [service]

# Stop
docker-compose down
```

## Testes

### Estrutura de Testes
```
tests/
├── unit/
│   ├── api/
│   ├── services/
│   └── utils/
├── integration/
│   ├── api/
│   └── database/
├── e2e/
│   └── playwright/
└── load/
    └── locust/
```

### Executando Testes

#### Testes Unitários
```bash
# Todos os testes
python -m pytest

# Com coverage
python -m pytest --cov=src --cov-report=html

# Testes específicos
python -m pytest tests/unit/api/test_health.py

# Watch mode
ptw src tests
```

#### Testes de Integração
```bash
# Setup test database
export DATABASE_URL=postgresql://test:test@localhost:5433/test_db

# Run integration tests
python -m pytest tests/integration -v
```

#### Testes E2E
```bash
# Install playwright
playwright install

# Run E2E tests
python -m pytest tests/e2e --headed

# Specific browser
python -m pytest tests/e2e --browser chromium
```

#### Testes de Carga
```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/load/api_load_test.py --host=http://localhost:8001
```

### Coverage Requirements
- **Unitários:** >90%
- **Integração:** >80%
- **E2E:** Critical paths obrigatórios

## Deploy

### Ambientes

#### Development
- **Branch:** develop
- **Deploy:** Automático via CI/CD
- **URL:** https://dev.auditoria360.com
- **Database:** Dev database
- **Monitoring:** Basic

#### Staging
- **Branch:** release/v*
- **Deploy:** Automático após testes
- **URL:** https://staging.auditoria360.com
- **Database:** Staging database (copy of prod)
- **Monitoring:** Full monitoring

#### Production
- **Branch:** main
- **Deploy:** Manual approval required
- **URL:** https://app.auditoria360.com
- **Database:** Production database
- **Monitoring:** Full monitoring + alerts

### Deploy Process

#### Staging Deploy
```bash
# Create release branch
git checkout develop
git pull origin develop
git checkout -b release/v1.2.3

# Update version
./scripts/bump_version.sh 1.2.3

# Commit and push
git add .
git commit -m "release: v1.2.3"
git push origin release/v1.2.3

# Create PR to main
# CI/CD will deploy to staging automatically
```

#### Production Deploy
```bash
# After staging approval
git checkout main
git merge release/v1.2.3
git tag v1.2.3
git push origin main --tags

# Manual approval in GitHub Actions required
```

### Deploy Checklist

#### Pre-Deploy
- [ ] All tests passing
- [ ] Code review approved
- [ ] Database migrations tested
- [ ] Performance tests passed
- [ ] Security scan clean
- [ ] Documentation updated
- [ ] Changelog updated

#### Durante Deploy
- [ ] Health checks monitored
- [ ] Error rates monitored
- [ ] Performance metrics monitored
- [ ] User feedback monitored

#### Post-Deploy
- [ ] Smoke tests executed
- [ ] Health dashboard green
- [ ] User acceptance testing
- [ ] Rollback plan ready
- [ ] Team notified

### Rollback Process

#### Automatic Rollback Triggers
- Health check failures > 2 minutes
- Error rate > 5%
- Response time > 3x baseline

#### Manual Rollback
```bash
# Rollback to previous version
kubectl rollout undo deployment/auditoria360-api

# Or specific version
kubectl rollout undo deployment/auditoria360-api --to-revision=2

# Verify rollback
kubectl rollout status deployment/auditoria360-api
```

## Database Migrations

### Alembic Setup
```bash
# Create migration
alembic revision --autogenerate -m "add user preferences table"

# Review migration file
# Edit if necessary

# Test migration locally
alembic upgrade head

# Test rollback
alembic downgrade -1
```

### Migration Checklist
- [ ] Migration é backward compatible
- [ ] Inclui rollback script
- [ ] Testado localmente
- [ ] Testado em staging
- [ ] Dados sensíveis protegidos
- [ ] Performance impact avaliado

## Monitoramento Local

### Health Checks
```bash
# API health
curl http://localhost:8001/api/health/

# Individual modules
curl http://localhost:8001/api/health/dashboard

# Status dashboard
python automation/update_status.py
```

### Logs
```bash
# API logs
tail -f logs/api.log

# Docker logs
docker-compose logs -f api

# Structured logging
tail -f logs/audit.jsonl | jq '.'
```

### Metrics
```bash
# Start Prometheus + Grafana
docker-compose -f docker-compose.monitoring.yml up -d

# Access dashboards
open http://localhost:3000  # Grafana
open http://localhost:9090  # Prometheus
```

## Debugging

### Common Issues

#### Connection Errors
```bash
# Check ports
netstat -tlnp | grep 8001

# Check environment
printenv | grep AUDITORIA360

# Check database
psql $DATABASE_URL -c "SELECT 1"
```

#### Performance Issues
```bash
# Profile API
python -m cProfile -o profile.stats src/main.py
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('time').print_stats(20)"

# Memory usage
python -m memory_profiler src/main.py
```

#### Frontend Issues  
```bash
# Build analysis
npm run analyze

# Debug mode
npm run dev -- --debug

# Clear cache
rm -rf node_modules/.cache
npm run dev
```

## Recursos

### Links Úteis
- [Repositório](https://github.com/Thaislaine997/AUDITORIA360)
- [Documentação API](https://api.auditoria360.com/docs)
- [Status Dashboard](https://status.auditoria360.com)
- [Grafana](https://monitoring.auditoria360.com)

### Comandos Úteis
```bash
# Makefile shortcuts
make setup        # Setup local environment
make test         # Run all tests
make lint         # Run linters
make build        # Build application
make deploy-dev   # Deploy to dev
make clean        # Clean build artifacts
```

---

**Última Atualização:** 2025-08-11  
**Mantido por:** DevOps Team