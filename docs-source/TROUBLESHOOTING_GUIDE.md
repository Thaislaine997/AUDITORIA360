# 🔧 TROUBLESHOOTING GUIDE v1.0.0 - AUDITORIA360

## 📋 Visão Geral

Este guia fornece procedimentos de diagnóstico e resolução de problemas para o AUDITORIA360 v1.0.0, incluindo cenários pós-deploy e operação contínua.

---

## 🚨 PROBLEMAS CRÍTICOS E RESOLUÇÃO IMEDIATA

### 1. Sistema Indisponível (HTTP 5xx)

#### Sintomas
- Página não carrega
- Erro 500/502/503/504
- Timeout de conexão

#### Diagnóstico Rápido
```bash
# Verificar status dos pods
kubectl get pods -n production

# Verificar logs de aplicação
kubectl logs -l app=auditoria360 --tail=100

# Verificar health check
curl -f https://app.auditoria360.com.br/health

# Verificar load balancer
kubectl get services -n production
```

#### Resolução Imediata
```bash
# 1. Restart da aplicação
kubectl rollout restart deployment/auditoria360

# 2. Se persistir, escalar pods
kubectl scale deployment/auditoria360 --replicas=5

# 3. Verificar recursos
kubectl top pods -n production

# 4. Em último caso, rollback
./scripts/emergency-rollback.sh
```

#### Escalação
- **Tempo limite**: 5 minutos
- **Contato**: Tech Lead + DevOps
- **Decisão rollback**: CTO

---

### 2. Performance Degradada (Lentidão)

#### Sintomas
- Response time > 500ms
- Aplicação lenta
- Timeouts ocasionais

#### Diagnóstico
```bash
# Verificar métricas de performance
curl -s http://prometheus:9090/api/v1/query?query=http_request_duration_seconds

# Verificar uso de CPU/Memory
kubectl top pods -n production

# Verificar conexões de banco
psql "$DATABASE_URL" -c "SELECT * FROM pg_stat_activity;"

# Verificar cache Redis
redis-cli info stats
```

#### Resolução
```bash
# 1. Verificar cache hit rate
redis-cli info stats | grep hit_rate

# 2. Limpar cache se necessário
redis-cli FLUSHDB

# 3. Reiniciar cache
kubectl restart deployment/redis

# 4. Verificar queries lentas
psql "$DATABASE_URL" -c "SELECT query, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"

# 5. Escalar aplicação
kubectl scale deployment/auditoria360 --replicas=8
```

---

### 3. Erro de Autenticação (401/403)

#### Sintomas
- Usuários não conseguem fazer login
- Tokens expirados constantemente
- Erro "Unauthorized"

#### Diagnóstico
```bash
# Verificar serviço de auth
kubectl logs -l app=auditoria360 | grep -i auth

# Verificar JWT
echo "$JWT_TOKEN" | jwt decode -

# Verificar OAuth2 provider
curl -f https://auth.auditoria360.com/.well-known/openid_configuration

# Verificar banco de usuários
psql "$DATABASE_URL" -c "SELECT count(*) FROM users WHERE status = 'active';"
```

#### Resolução
```bash
# 1. Verificar configuração OAuth2
kubectl get configmap auth-config -o yaml

# 2. Renovar certificados JWT (se expirados)
./scripts/renew-jwt-certificates.sh

# 3. Verificar MFA settings
kubectl logs -l app=auditoria360 | grep -i mfa

# 4. Reset user sessions (emergência)
redis-cli FLUSHDB 1
```

---

## 📊 MONITORAMENTO E MÉTRICAS

### Dashboard Principal - Grafana

#### Métricas Críticas a Monitorar

**Application Metrics:**
```
# Response Time (p95)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error Rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) * 100

# Throughput
rate(http_requests_total[5m])

# Active Users
increase(user_login_total[1h])
```

**Infrastructure Metrics:**
```
# CPU Usage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory Usage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Disk Usage
100 - ((node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100)

# Network I/O
rate(node_network_receive_bytes_total[5m])
```

#### Alertas Configurados

**Critical Alerts (PagerDuty):**
- Response time > 1000ms por 5 minutos
- Error rate > 5% por 2 minutos
- Availability < 99% por 1 minuto
- Disk usage > 90%

**Warning Alerts (Slack):**
- Response time > 500ms por 10 minutos
- Error rate > 2% por 5 minutos
- CPU usage > 80% por 15 minutos
- Memory usage > 85% por 10 minutos

---

## 🔍 DIAGNÓSTICOS ESPECÍFICOS

### Problemas de Banco de Dados

#### Conexões Esgotadas
```bash
# Verificar conexões ativas
psql "$DATABASE_URL" -c "
SELECT count(*) as active_connections, 
       max_conn, 
       max_conn - count(*) as available
FROM pg_stat_activity, 
     (SELECT setting::int as max_conn FROM pg_settings WHERE name='max_connections') mc;
"

# Matar conexões idle (se necessário)
psql "$DATABASE_URL" -c "
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE state = 'idle' AND state_change < now() - interval '5 minutes';
"
```

#### Queries Lentas
```bash
# Identificar queries problemáticas
psql "$DATABASE_URL" -c "
SELECT query, calls, mean_time, total_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
"

# Reset estatísticas (se necessário)
psql "$DATABASE_URL" -c "SELECT pg_stat_statements_reset();"
```

#### Lock de Tabelas
```bash
# Verificar locks
psql "$DATABASE_URL" -c "
SELECT t.relname, l.locktype, page, virtualtransaction, pid, mode, granted 
FROM pg_locks l, pg_stat_all_tables t 
WHERE l.relation = t.relid 
ORDER BY relation ASC;
"
```

### Problemas de Cache (Redis)

#### Cache Miss Rate Alto
```bash
# Verificar estatísticas
redis-cli info stats

# Verificar configuração
redis-cli config get "*"

# Verificar memória
redis-cli info memory

# Warm up cache (se necessário)
python scripts/cache-warmup.py
```

#### Redis Indisponível
```bash
# Verificar conectividade
redis-cli ping

# Restart Redis
kubectl restart deployment/redis

# Verificar logs
kubectl logs -l app=redis --tail=100

# Backup/Restore (se necessário)
redis-cli --rdb /backup/dump.rdb
```

### Problemas de Storage (Cloudflare R2)

#### Upload de Arquivos Falhando
```bash
# Testar conectividade R2
aws s3 ls s3://auditoria360-bucket --endpoint-url=https://r2.cloudflarestorage.com

# Verificar credenciais
aws configure list

# Verificar logs de upload
kubectl logs -l app=auditoria360 | grep -i "upload\|storage"

# Testar upload manual
aws s3 cp test.txt s3://auditoria360-bucket/test/ --endpoint-url=https://r2.cloudflarestorage.com
```

---

## 🔧 FERRAMENTAS DE DIAGNÓSTICO

### Scripts de Diagnóstico Automático

#### Health Check Completo
```bash
#!/bin/bash
# scripts/health-check-complete.sh

echo "🏥 AUDITORIA360 - Health Check Completo"
echo "=================================="

# 1. API Health
echo "📡 Verificando API..."
if curl -f -s https://app.auditoria360.com.br/health > /dev/null; then
    echo "✅ API Online"
else
    echo "❌ API Offline"
fi

# 2. Database Health
echo "🗄️ Verificando Banco de Dados..."
if psql "$DATABASE_URL" -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Banco Online"
else
    echo "❌ Banco Offline"
fi

# 3. Redis Health
echo "🔄 Verificando Cache..."
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Cache Online"
else
    echo "❌ Cache Offline"
fi

# 4. Storage Health
echo "📁 Verificando Storage..."
if aws s3 ls s3://auditoria360-bucket --endpoint-url=https://r2.cloudflarestorage.com > /dev/null 2>&1; then
    echo "✅ Storage Online"
else
    echo "❌ Storage Offline"
fi

# 5. Performance Check
echo "⚡ Verificando Performance..."
RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' https://app.auditoria360.com.br/health)
if (( $(echo "$RESPONSE_TIME < 1.0" | bc -l) )); then
    echo "✅ Performance OK (${RESPONSE_TIME}s)"
else
    echo "⚠️ Performance Lenta (${RESPONSE_TIME}s)"
fi

echo "=================================="
echo "Health Check Concluído: $(date)"
```

#### Performance Monitor
```bash
#!/bin/bash
# scripts/performance-monitor.sh

echo "📊 AUDITORIA360 - Monitor de Performance"
echo "======================================"

# Métricas de Sistema
echo "💻 Uso de Recursos:"
kubectl top pods -n production

# Métricas de Aplicação
echo "🚀 Métricas de Aplicação:"
curl -s http://prometheus:9090/api/v1/query?query=rate\(http_requests_total\[5m\]\) | jq '.data.result[0].value[1]'

# Conexões de Banco
echo "🗄️ Conexões de Banco:"
psql "$DATABASE_URL" -c "SELECT count(*) as connections FROM pg_stat_activity;"

# Cache Stats
echo "🔄 Estatísticas de Cache:"
redis-cli info stats | grep -E "(hit_rate|ops_per_sec)"

echo "======================================"
```

### Log Analysis

#### Análise de Erros
```bash
#!/bin/bash
# scripts/error-analysis.sh

echo "🔍 Análise de Erros - Últimas 24h"
echo "================================"

# Errors por hora
kubectl logs -l app=auditoria360 --since=24h | grep -i error | awk '{print $1" "$2}' | cut -d: -f1-2 | sort | uniq -c

# Top 10 erros
kubectl logs -l app=auditoria360 --since=24h | grep -i error | sort | uniq -c | sort -nr | head -10

# Erros críticos
kubectl logs -l app=auditoria360 --since=24h | grep -E "(CRITICAL|FATAL)"

echo "================================"
```

---

## 📋 PROCEDIMENTOS DE EMERGÊNCIA

### 1. Rollback de Emergência

```bash
#!/bin/bash
# scripts/emergency-rollback.sh

echo "🚨 ROLLBACK DE EMERGÊNCIA"
echo "========================"

# 1. Capturar estado atual
kubectl get deployment auditoria360 -o yaml > rollback-$(date +%Y%m%d-%H%M%S).yaml

# 2. Rollback para versão anterior
kubectl rollout undo deployment/auditoria360

# 3. Verificar rollback
kubectl rollout status deployment/auditoria360

# 4. Health check pós-rollback
./scripts/health-check-complete.sh

# 5. Notificar equipes
./scripts/notify-emergency.sh "Rollback executado"

echo "Rollback concluído: $(date)"
```

### 2. Disaster Recovery

```bash
#!/bin/bash
# scripts/disaster-recovery.sh

echo "🆘 PROCEDIMENTO DE DISASTER RECOVERY"
echo "===================================="

# 1. Backup de emergência
pg_dump "$DATABASE_URL" > emergency-backup-$(date +%Y%m%d-%H%M%S).sql

# 2. Recrear cluster (se necessário)
kubectl apply -f k8s/disaster-recovery/

# 3. Restaurar dados
psql "$RECOVERY_DATABASE_URL" < latest-backup.sql

# 4. Validar integridade
./scripts/validate-data-integrity.sh

# 5. Redirecionar tráfego
./scripts/update-dns.sh disaster-recovery

echo "Disaster Recovery ativado: $(date)"
```

---

## 📞 CONTATOS E ESCALAÇÃO

### Níveis de Escalação

**Nível 1 - Support Team (0-15min)**
- Problemas gerais
- Dúvidas de usuários
- Issues não críticos

**Nível 2 - Technical Team (15-30min)**
- Problemas de performance
- Erros de aplicação
- Issues de integração

**Nível 3 - Senior Team (30-60min)**
- Problemas críticos
- Falhas de infraestrutura
- Decisões de rollback

**Nível 4 - Management (60min+)**
- Indisponibilidade prolongada
- Problemas de segurança
- Decisões de negócio

### Contatos de Emergência

**24/7 Emergency Response**
- **Hotline**: +55 11 XXXX-XXXX
- **Slack**: #emergency-response
- **Email**: emergency@auditoria360.com

**Technical Leads**
- **DevOps Lead**: [Nome] - [Telefone]
- **Backend Lead**: [Nome] - [Telefone]
- **Frontend Lead**: [Nome] - [Telefone]

**Management**
- **CTO**: [Nome] - [Telefone]
- **Engineering Manager**: [Nome] - [Telefone]

---

## 📚 KNOWLEDGE BASE

### Problemas Conhecidos e Soluções

#### 1. "Database connection timeout"
**Causa**: Pool de conexões esgotado  
**Solução**: Restart da aplicação ou aumento do pool  
**Prevenção**: Monitorar conexões ativas

#### 2. "Redis connection refused"
**Causa**: Redis indisponível ou sobregregado  
**Solução**: Restart do Redis ou fallback para cache local  
**Prevenção**: Monitorar memória Redis

#### 3. "JWT token expired"
**Causa**: Certificados expirados ou clock skew  
**Solução**: Renovar certificados ou sincronizar clock  
**Prevenção**: Monitoramento de expiração

#### 4. "Upload failed to R2"
**Causa**: Credenciais inválidas ou rate limiting  
**Solução**: Renovar credenciais ou retry com backoff  
**Prevenção**: Monitorar quotas R2

### Runbooks Específicos

- **[Database Maintenance](runbooks/database-maintenance.md)**
- **[Cache Management](runbooks/cache-management.md)**
- **[Security Incident Response](runbooks/security-incident.md)**
- **[Performance Tuning](runbooks/performance-tuning.md)**

---

> **🔧 Troubleshooting v1.0.0**: Guia completo para diagnóstico e resolução de problemas no AUDITORIA360.

**Última atualização**: 30 de Julho de 2025  
**Próxima revisão**: Mensal ou após incidentes maiores