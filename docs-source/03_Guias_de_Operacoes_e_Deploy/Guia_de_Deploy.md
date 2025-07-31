# 🚀 Guia de Deploy - AUDITORIA360

## 🎯 Objetivo

Este documento fornece instruções completas para deploy da AUDITORIA360 em diferentes ambientes, desde desenvolvimento até produção.

## 📋 Checklist Pré-Deploy

### ✅ Verificações Obrigatórias

Antes de qualquer deploy em produção, execute este checklist:

#### 🌐 Domínios e DNS
- [ ] **auditoria360.com.br** - IP correto configurado
  - Ferramenta: [WhatsMyDNS.net](https://www.whatsmydns.net/)
  - Status: 🔴 Pendente / 🟡 Propagando / 🟢 OK

- [ ] **api.auditoria360.com.br** - CNAME/A record configurado
  - Verificar propagação DNS global
  - Status: 🔴 Pendente / 🟡 Propagando / 🟢 OK

- [ ] **Servidor de E-mail** - MX records configurados
  - dpeixerassessoria.com.br apontando para servidor correto
  - Status: 🔴 Pendente / 🟡 Propagando / 🟢 OK

#### 🔐 Certificados SSL
- [ ] **Certificado Principal** - auditoria360.com.br
  - Ferramenta: [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
  - Nota mínima: A ou A+
  - Validade: > 30 dias

- [ ] **Certificado da API** - api.auditoria360.com.br
  - Verificar cadeia de certificados
  - Protocolos suportados: TLS 1.2+

#### ⚙️ Infraestrutura
- [ ] **Servidor de Aplicação**
  - CPU: < 80% uso médio
  - RAM: < 80% uso médio
  - Disco: > 20% espaço livre
  - Uptime: > 99.5%

- [ ] **Banco de Dados**
  - Conexões disponíveis: > 20%
  - Backup recente: < 24h
  - Replicação funcionando (se aplicável)

- [ ] **Cache/Redis**
  - Memória disponível: > 30%
  - Conexão estável
  - Persistência configurada

#### 🔧 Aplicação
- [ ] **Testes**
  - Cobertura: > 90%
  - Todos os testes passando
  - Testes de integração executados

- [ ] **Build**
  - Build de produção bem-sucedido
  - Assets otimizados
  - Bundle size aceitável

- [ ] **Configuração**
  - Variáveis de ambiente configuradas
  - Secrets atualizados
  - Feature flags revisadas

## 🐳 Deploy com Docker

### Ambiente de Desenvolvimento

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
cp .env.template .env
# Editar .env com suas configurações

# 3. Iniciar API
python test_api_server.py
# ou usando o Makefile
make run

# 4. Iniciar frontend (em outro terminal)
cd src/frontend
npm install
npm run dev

# 5. Verificar saúde da API
curl http://localhost:8001/health
```

### Ambiente de Produção

```bash
# 1. Configurar variáveis de ambiente
cp .env.template .env.production
nano .env.production

# 2. Instalar dependências de produção
pip install -r requirements.txt

# 3. Iniciar com uvicorn (produção)
uvicorn api.index:app --host 0.0.0.0 --port 8001 --workers 4

# 4. Verificação
curl -f http://localhost:8001/health || exit 1
```

### Monitoramento com Docker Compose

Para monitoramento, use o arquivo docker-compose.monitoring.yml:

```bash
# Iniciar stack de monitoramento
docker-compose -f docker-compose.monitoring.yml up -d

# Acessar dashboards
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001
```

### Configuração de Produção

Para deploy em produção, configure adequadamente:

```bash
# Variáveis de ambiente essenciais
export SECRET_KEY="sua_chave_secreta_32_caracteres_minimo"
export DATABASE_URL="postgresql://user:pass@host:port/dbname"
export OPENAI_API_KEY="sua_chave_openai"
export ENVIRONMENT="production"

# Deploy com uvicorn
uvicorn api.index:app --host 0.0.0.0 --port 8001 --workers 4 --access-log
```

## ☁️ Deploy em Cloud (AWS/GCP/Azure)

### AWS ECS com Fargate

```bash
# 1. Configurar CLI
aws configure

# 2. Criar cluster
aws ecs create-cluster --cluster-name auditoria360-prod

# 3. Build e push da imagem
docker build -t auditoria360 .
docker tag auditoria360:latest your-account.dkr.ecr.region.amazonaws.com/auditoria360:latest
docker push your-account.dkr.ecr.region.amazonaws.com/auditoria360:latest

# 4. Deploy via task definition
aws ecs run-task --cluster auditoria360-prod --task-definition auditoria360-task
```

### Kubernetes

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auditoria360-app
  labels:
    app: auditoria360
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auditoria360
  template:
    metadata:
      labels:
        app: auditoria360
    spec:
      containers:
      - name: app
        image: auditoria360:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: auditoria360-secrets
              key: database-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: auditoria360-service
spec:
  selector:
    app: auditoria360
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

## 🔄 CI/CD com GitHub Actions

### Workflow de Deploy

```yaml
# .github/workflows/deploy.yml
name: 🚀 Deploy to Production

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ghcr.io/${{ github.repository }}:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
    - name: Deploy to production
      run: |
        echo "🚀 Deploying to production..."
        # SSH para servidor ou kubectl apply
```

## 📊 Monitoramento Pós-Deploy

### Health Checks

```python
# src/health.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
import redis
import httpx

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check básico da aplicação."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.get("/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Verifica se aplicação está pronta para receber tráfego."""
    checks = {}
    
    # Verificar banco de dados
    try:
        db.execute("SELECT 1")
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
    
    # Verificar Redis
    try:
        r = redis.Redis.from_url(settings.REDIS_URL)
        r.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"
    
    # Verificar APIs externas
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.externa.com/health")
            checks["external_api"] = "healthy" if response.status_code == 200 else "degraded"
    except Exception as e:
        checks["external_api"] = f"unhealthy: {str(e)}"
    
    # Determinar status geral
    unhealthy_services = [k for k, v in checks.items() if "unhealthy" in v]
    
    if unhealthy_services:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "checks": checks,
                "unhealthy_services": unhealthy_services
            }
        )
    
    return {
        "status": "ready",
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Scripts de Validação

```bash
#!/bin/bash
# scripts/validate_deploy.sh

echo "🔍 Validando deploy..."

# Verificar se aplicação está respondendo
if curl -f http://localhost/health; then
    echo "✅ Health check OK"
else
    echo "❌ Health check falhou"
    exit 1
fi

# Verificar readiness
if curl -f http://localhost/ready; then
    echo "✅ Readiness check OK"
else
    echo "❌ Readiness check falhou"
    exit 1
fi

# Verificar principais endpoints
endpoints=("/api/auth/me" "/api/dashboard" "/api/health")

for endpoint in "${endpoints[@]}"; do
    if curl -f "http://localhost${endpoint}"; then
        echo "✅ Endpoint ${endpoint} OK"
    else
        echo "❌ Endpoint ${endpoint} falhou"
        exit 1
    fi
done

echo "🎉 Deploy validado com sucesso!"
```

## 🔧 Troubleshooting

### Problemas Comuns

#### Container não inicia
```bash
# Verificar logs
docker logs container-name

# Verificar recursos
docker stats

# Entrar no container
docker exec -it container-name /bin/bash
```

#### Banco de dados não conecta
```bash
# Verificar conectividade
pg_isready -h hostname -p 5432

# Testar conexão
psql -h hostname -U username -d database_name

# Verificar logs do PostgreSQL
docker logs postgres-container
```

#### Performance degradada
```bash
# Verificar métricas
curl http://localhost/metrics

# Analisar logs
tail -f logs/app.log | grep ERROR

# Profiling
py-spy top --pid $(pgrep python)
```

### Rollback

```bash
# Para ambiente simples com uvicorn
# 1. Parar processo atual
pkill -f "uvicorn api.index:app"

# 2. Reverter código
git checkout previous-commit

# 3. Reinstalar dependências se necessário
pip install -r requirements.txt

# 4. Reiniciar aplicação
uvicorn api.index:app --host 0.0.0.0 --port 8001 --workers 4

# Para Kubernetes (se aplicável)
kubectl rollout undo deployment/auditoria360-app

# Para monitoramento
docker-compose -f docker-compose.monitoring.yml restart
```

## 📚 Recursos Adicionais

- [Documentação de Monitoramento](../monitoring/README.md)
- [Guia de Troubleshooting](Troubleshooting.md)
- [Scripts de Automação](../../scripts/README.md)
- [Configuração de Alerts](../monitoring/alerting.md)

---

⚠️ **Importante**: Sempre teste o processo de deploy em ambiente de staging antes de aplicar em produção.

🚨 **Emergência**: Em caso de problemas críticos, execute imediatamente o rollback e documente o incidente.