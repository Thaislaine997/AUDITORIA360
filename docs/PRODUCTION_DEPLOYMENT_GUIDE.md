# 🚀 AUDITORIA360 - Guia de Deploy para Produção

*Procedimentos completos para deploy seguro e confiável em produção*

---

## 🎯 Visão Geral do Deploy

### Arquitetura de Produção
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cloudflare    │    │     Vercel       │    │   Supabase      │
│   (CDN + WAF)   │──▶ │   (Frontend)     │──▶ │  (Database)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ Cloudflare       │    │  Cloudflare R2  │
                       │ Workers (API)    │──▶ │   (Storage)     │
                       └──────────────────┘    └─────────────────┘
```

### Componentes de Deploy
- **Frontend**: React SPA na Vercel
- **Backend**: FastAPI em Cloudflare Workers  
- **Database**: Supabase (PostgreSQL)
- **Storage**: Cloudflare R2
- **CDN**: Cloudflare
- **Monitoring**: OpenTelemetry + Custom ACR

---

## 🔧 Configuração de Ambientes

### 1️⃣ Ambiente de Staging

#### Características
- **URL**: `https://staging-auditoria360.vercel.app`
- **Database**: Supabase staging instance
- **Purpose**: Testes finais antes da produção
- **Data**: Dados sintéticos/anonimizados

#### Setup Staging
```bash
# 1. Criar branch de staging
git checkout -b staging
git push origin staging

# 2. Configurar Vercel para staging
vercel --prod --env staging
vercel env add NEXT_PUBLIC_API_URL
# Valor: https://staging-api.auditoria360.com

# 3. Deploy automático via GitHub Actions
# (Pipeline configurado em .github/workflows/staging.yml)
```

### 2️⃣ Ambiente de Produção

#### Características
- **URL**: `https://auditoria360.com`
- **Database**: Supabase production
- **Purpose**: Sistema ativo para clientes
- **Data**: Dados reais com backup automatizado

---

## 📋 Checklist Pré-Deploy

### Backend (API)
- [ ] **Testes**: 100% dos testes críticos passando
- [ ] **Dependencies**: Requirements.txt atualizado
- [ ] **Environment Variables**: Todas as vars configuradas
- [ ] **Database Migrations**: Migrations testadas em staging
- [ ] **Rate Limiting**: Configurado para produção
- [ ] **Error Handling**: Logs estruturados implementados
- [ ] **Health Checks**: Endpoints /health implementados
- [ ] **Security**: HTTPS, CORS, CSP configurados

### Frontend
- [ ] **Build**: Build de produção sem warnings
- [ ] **Bundle Size**: Análise de bundle otimizada
- [ ] **Environment**: Variáveis de produção configuradas
- [ ] **CDN**: Assets configurados para CDN
- [ ] **SEO**: Meta tags e analytics configurados
- [ ] **Performance**: Lighthouse score > 90
- [ ] **Responsive**: Testado em diferentes dispositivos
- [ ] **Accessibility**: WCAG compliance verificado

### Infraestrutura
- [ ] **DNS**: Domínio configurado e propagado
- [ ] **SSL**: Certificados válidos (TLS 1.3)
- [ ] **Backup**: Estratégia de backup implementada
- [ ] **Monitoring**: Alertas configurados
- [ ] **Rollback**: Plano de rollback documentado
- [ ] **Capacity Planning**: Recursos dimensionados
- [ ] **Security**: WAF e proteções ativas

---

## 🔄 Pipeline CI/CD

### GitHub Actions Workflow

```yaml
# .github/workflows/production.yml
name: Production Deploy
on:
  push:
    branches: [main]
  
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      - name: Run tests
        run: pytest tests/
        
  build-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install and build
        run: |
          cd src/frontend
          npm ci
          npm run build
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
          
  deploy-backend:
    needs: test
    runs-on: ubuntu-latest  
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Cloudflare Workers
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: publish
          
  smoke-tests:
    needs: [build-frontend, deploy-backend]
    runs-on: ubuntu-latest
    steps:
      - name: Run smoke tests
        run: |
          curl -f https://auditoria360.com/health
          curl -f https://api.auditoria360.com/health
```

---

## 🗄️ Database Migrations

### Processo de Migration
```bash
# 1. Backup antes da migration
pg_dump $SUPABASE_DATABASE_URL > backup_pre_migration.sql

# 2. Execute migration em staging primeiro
python migrations/run_migrations.py --env staging

# 3. Validar em staging
pytest tests/integration/test_database.py

# 4. Execute migration em produção
python migrations/run_migrations.py --env production

# 5. Validar em produção
python scripts/validate_migration.py
```

### Script de Migration Exemplo
```python
# migrations/20250801_add_audit_table.py
from supabase import create_client
import os

def up_migration():
    """Adiciona tabela de auditoria"""
    supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_ANON_KEY")
    )
    
    sql = """
    CREATE TABLE IF NOT EXISTS audit_logs (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID REFERENCES auth.users(id),
        contabilidade_id UUID REFERENCES contabilidades(id),
        action VARCHAR(100) NOT NULL,
        resource_id UUID,
        details JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- RLS Policy
    ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
    
    CREATE POLICY "audit_logs_policy" ON audit_logs
        USING (contabilidade_id = current_setting('app.current_contabilidade_id')::uuid);
    """
    
    supabase.rpc('execute_sql', {'sql': sql})
    
def down_migration():
    """Rollback da migration"""
    supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_ANON_KEY")
    )
    
    sql = "DROP TABLE IF EXISTS audit_logs CASCADE;"
    supabase.rpc('execute_sql', {'sql': sql})
```

---

## 📊 Monitoramento Pós-Deploy

### Health Checks
```python
# api/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check completo"""
    checks = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT"),
        "checks": {}
    }
    
    try:
        # Test database connection
        db.execute("SELECT 1")
        checks["checks"]["database"] = "healthy"
    except Exception as e:
        checks["checks"]["database"] = f"unhealthy: {str(e)}"
        checks["status"] = "degraded"
    
    try:
        # Test Redis connection (if used)
        redis_client.ping()
        checks["checks"]["redis"] = "healthy"
    except:
        checks["checks"]["redis"] = "unavailable"
    
    try:
        # Test external APIs
        openai_response = test_openai_connection()
        checks["checks"]["openai"] = "healthy"
    except:
        checks["checks"]["openai"] = "unavailable"
    
    return checks

@router.get("/ready")
async def readiness_check():
    """Readiness probe para Kubernetes/Docker"""
    return {"status": "ready"}

@router.get("/live")  
async def liveness_check():
    """Liveness probe para Kubernetes/Docker"""
    return {"status": "alive"}
```

### Métricas de Produção
```python
# monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Contadores
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Histogramas
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency'
)

# Gauges
ACTIVE_USERS = Gauge(
    'active_users_total',
    'Number of active users'
)

DATABASE_CONNECTIONS = Gauge(
    'database_connections_active',
    'Active database connections'
)
```

---

## 🚨 Plano de Rollback

### Estratégias de Rollback

#### 1. Rollback Automático
```yaml
# Configuração no Vercel
{
  "deploymentProtection": {
    "automaticRollback": true,
    "healthCheck": "https://auditoria360.com/health",
    "checkInterval": 30,
    "failureThreshold": 3
  }
}
```

#### 2. Rollback Manual
```bash
# Rollback do frontend (Vercel)
vercel rollback --token=$VERCEL_TOKEN

# Rollback do backend (Cloudflare Workers)  
wrangler rollback --name=auditoria360-api

# Rollback da database (se necessário)
pg_restore -d $DATABASE_URL backup_pre_migration.sql
```

#### 3. Rollback de Emergency
```bash
# Script de emergency rollback
#!/bin/bash
set -e

echo "🚨 EMERGENCY ROLLBACK INITIATED"

# 1. Rollback frontend
echo "Rolling back frontend..."
vercel rollback --token=$VERCEL_TOKEN --yes

# 2. Rollback backend
echo "Rolling back backend..."
wrangler rollback --name=auditoria360-api

# 3. Switch to maintenance mode
echo "Enabling maintenance mode..."
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/maintenance_mode" \
     -H "Authorization: Bearer $CF_API_TOKEN" \
     -H "Content-Type: application/json" \
     --data '{"value":"on"}'

# 4. Notify team
echo "Sending notifications..."
curl -X POST $SLACK_WEBHOOK_URL \
     -H 'Content-type: application/json' \
     --data '{"text":"🚨 EMERGENCY ROLLBACK EXECUTED"}'

echo "✅ Emergency rollback completed"
```

---

## 📈 Performance e Scaling

### Configurações de Performance

#### Cloudflare Workers
```javascript
// wrangler.toml
[env.production]
name = "auditoria360-api"
compatibility_date = "2023-05-18"

[env.production.vars]
ENVIRONMENT = "production"

[env.production.limits]
cpu_ms = 30000

[env.production.placement]
mode = "smart"
```

#### Database Optimization
```sql
-- Índices para performance
CREATE INDEX CONCURRENTLY idx_auditorias_cliente_id 
    ON auditorias(cliente_id);

CREATE INDEX CONCURRENTLY idx_auditorias_data_criacao 
    ON auditorias(created_at DESC);

CREATE INDEX CONCURRENTLY idx_usuarios_contabilidade_id 
    ON usuarios(contabilidade_id);

-- Configurações de connection pool
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
```

### Auto-scaling Configuration
```yaml
# Auto-scaling baseado em métricas
scaling:
  frontend:
    provider: vercel
    auto_scale: true
    regions: ["iad1", "sfo1", "fra1"]
    
  backend:
    provider: cloudflare_workers
    auto_scale: true
    min_instances: 0
    max_instances: 1000
    
  database:
    provider: supabase
    auto_scale: true
    max_connections: 200
```

---

## 🔒 Configurações de Segurança em Produção

### Environment Variables (Produção)
```bash
# API Configuration
API_BASE_URL=https://api.auditoria360.com
JWT_SECRET_KEY=${SECRETS_MANAGER_JWT_KEY}
ENCRYPTION_KEY=${SECRETS_MANAGER_ENCRYPTION_KEY}

# Database
SUPABASE_URL=${SECRETS_MANAGER_SUPABASE_URL}
SUPABASE_ANON_KEY=${SECRETS_MANAGER_SUPABASE_ANON_KEY}

# External Services
OPENAI_API_KEY=${SECRETS_MANAGER_OPENAI_KEY}
CLOUDFLARE_R2_ACCESS_KEY=${SECRETS_MANAGER_R2_ACCESS_KEY}

# Security
CORS_ORIGINS=["https://auditoria360.com"]
HTTPS_ONLY=true
SECURE_COOKIES=true
RATE_LIMIT_ENABLED=true
```

### WAF Rules (Cloudflare)
```javascript
// Cloudflare WAF Rules
[
  {
    "action": "block",
    "expression": "(http.request.method eq \"POST\" and http.request.uri.path contains \"/api/auth/login\" and rate(5m) > 10)"
  },
  {
    "action": "challenge", 
    "expression": "(cf.threat_score > 10)"
  },
  {
    "action": "block",
    "expression": "(ip.src in $blocked_ips)"
  }
]
```

---

## 📋 Checklist Final de Deploy

### Pré-Deploy
- [ ] Todos os testes passando
- [ ] Staging validado pela equipe
- [ ] Backup da produção atual realizado
- [ ] Variáveis de ambiente configuradas
- [ ] SSL certificates válidos
- [ ] DNS configurado e propagado

### Durante o Deploy  
- [ ] Pipeline CI/CD executado com sucesso
- [ ] Health checks passando
- [ ] Smoke tests executados
- [ ] Métricas de performance dentro do esperado
- [ ] Logs sem erros críticos

### Pós-Deploy
- [ ] Monitoring dashboards verificados
- [ ] Alertas configurados e testados
- [ ] Performance baseline estabelecida
- [ ] Documentação atualizada
- [ ] Equipe notificada do deploy
- [ ] Rollback plan validado e documentado

### Follow-up (24h após deploy)
- [ ] Métricas de uso analisadas
- [ ] Feedback dos usuários coletado
- [ ] Logs de erro analisados
- [ ] Performance comparada com baseline
- [ ] Relatório pós-deploy documentado

---

## 📞 Contatos de Emergency

### Escalation Matrix
| Severidade | Tempo Resposta | Contatos |
|------------|----------------|----------|
| **P0** (Sistema down) | 15 min | DevOps Lead, CTO |
| **P1** (Funcionalidade crítica) | 1 hora | Tech Lead, Product |
| **P2** (Degradação performance) | 4 horas | Dev Team |
| **P3** (Issue menor) | 24 horas | Dev Team |

### Emergency Procedures
- **Slack Channel**: `#auditoria360-alerts`
- **PagerDuty**: Configurado para P0/P1
- **Runbook**: `/docs/emergency_runbook.md`
- **War Room**: Google Meet room pré-configurado

---

**Este guia deve ser revisado a cada deploy major e atualizado conforme mudanças na infraestrutura.**