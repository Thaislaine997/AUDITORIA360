# ✅ POST-DEPLOYMENT VALIDATION GUIDE v1.0.0

## 📋 Visão Geral

Este guia define os procedimentos de validação que devem ser executados após o deploy do Release Candidate v1.0.0 do AUDITORIA360, garantindo que todas as funcionalidades estão operando corretamente em produção.

---

## 🎯 VALIDAÇÃO IMEDIATA (T+0 a T+30min)

### 1. Health Checks Básicos

#### 1.1 Verificação de Disponibilidade
```bash
# API Health Check
curl -f https://app.auditoria360.com.br/health
# Esperado: HTTP 200 + JSON com status: "healthy"

# Frontend Load
curl -f https://auditoria360.com.br/
# Esperado: HTTP 200 + HTML válido

# API Documentation
curl -f https://app.auditoria360.com.br/docs
# Esperado: HTTP 200 + Swagger UI
```

#### 1.2 Verificação de Serviços Críticos
```bash
# Database Connection
curl -f https://app.auditoria360.com.br/api/v1/status/database
# Esperado: {"status": "connected", "pool_status": "healthy"}

# Cache Status
curl -f https://app.auditoria360.com.br/api/v1/status/cache
# Esperado: {"status": "connected", "hit_rate": ">80%"}

# Storage Connectivity
curl -f https://app.auditoria360.com.br/api/v1/status/storage
# Esperado: {"status": "connected", "write_test": "ok"}
```

### 2. Autenticação e Autorização

#### 2.1 Login Administrativo
```bash
# Test admin login
curl -X POST https://app.auditoria360.com.br/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "ADMIN_PASSWORD"}'
# Esperado: HTTP 200 + access_token
```

#### 2.2 Verificação MFA
```bash
# Test MFA requirement for admin
# (Deve ser testado via interface web)
```

#### 2.3 Teste de Permissões
```bash
# Test role-based access
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  https://app.auditoria360.com.br/api/v1/admin/users
# Esperado: HTTP 200 + lista de usuários
```

### 3. Funcionalidades Core

#### 3.1 Upload de Documentos
```bash
# Test document upload
curl -X POST https://app.auditoria360.com.br/api/v1/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test-document.pdf"
# Esperado: HTTP 201 + document_id
```

#### 3.2 OCR Processing
```bash
# Test OCR processing
curl -X POST https://app.auditoria360.com.br/api/v1/documents/{id}/ocr \
  -H "Authorization: Bearer $TOKEN"
# Esperado: HTTP 202 + processing_id
```

#### 3.3 IA Assistant
```bash
# Test AI chat
curl -X POST https://app.auditoria360.com.br/api/v1/ai/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "Como calcular adicional noturno?"}'
# Esperado: HTTP 200 + resposta contextual
```

---

## 📊 VALIDAÇÃO DE PERFORMANCE (T+30min a T+2h)

### 1. Métricas de Response Time

#### 1.1 Endpoints Críticos
```bash
# Medir response time de endpoints principais
for endpoint in "health" "api/v1/status" "api/v1/payroll" "api/v1/documents"; do
  echo "Testing $endpoint:"
  curl -o /dev/null -s -w "%{time_total}" https://app.auditoria360.com.br/$endpoint
  echo " seconds"
done
# Target: <200ms para 95% das requisições
```

#### 1.2 Load Testing Básico
```bash
# Apache Bench test
ab -n 1000 -c 10 https://app.auditoria360.com.br/api/v1/health
# Target: >1000 req/s, 0% failed requests
```

### 2. Verificação de Cache

#### 2.1 Cache Hit Rate
```bash
# Verificar hit rate do Redis
redis-cli info stats | grep keyspace_hits
# Target: >80% hit rate
```

#### 2.2 Cache Warming
```bash
# Executar cache warming
python scripts/cache-warmup.py
# Verificar melhoria na performance
```

### 3. Database Performance

#### 3.1 Query Performance
```bash
# Verificar queries mais lentas
psql "$DATABASE_URL" -c "
SELECT query, mean_time, calls 
FROM pg_stat_statements 
WHERE mean_time > 100 
ORDER BY mean_time DESC 
LIMIT 5;
"
# Target: Nenhuma query >1000ms
```

---

## 🔐 VALIDAÇÃO DE SEGURANÇA (T+2h a T+4h)

### 1. Verificação de Headers de Segurança

#### 1.1 Security Headers
```bash
# Verificar headers de segurança
curl -I https://auditoria360.com.br/
# Verificar presença de:
# - Content-Security-Policy
# - X-Frame-Options: DENY
# - X-Content-Type-Options: nosniff
# - Strict-Transport-Security
```

#### 1.2 TLS Configuration
```bash
# Test TLS configuration
nmap --script ssl-enum-ciphers -p 443 auditoria360.com.br
# Verificar: TLS 1.2+, sem ciphers fracos
```

### 2. Teste de Input Validation

#### 2.1 SQL Injection Protection
```bash
# Test SQL injection attempts
curl -X POST https://app.auditoria360.com.br/api/v1/auth/login \
  -d "username=admin' OR '1'='1&password=test"
# Esperado: HTTP 400 ou 422 (input validation error)
```

#### 2.2 XSS Protection
```bash
# Test XSS attempts
curl -X POST https://app.auditoria360.com.br/api/v1/documents/upload \
  -F "filename=<script>alert('xss')</script>"
# Esperado: Input sanitizado ou rejeitado
```

### 3. Rate Limiting

#### 3.1 API Rate Limits
```bash
# Test rate limiting
for i in {1..20}; do
  curl -s -o /dev/null -w "%{http_code}" \
    https://app.auditoria360.com.br/api/v1/auth/login
done
# Esperado: HTTP 429 após limite atingido
```

---

## 💼 VALIDAÇÃO FUNCIONAL (T+4h a T+8h)

### 1. Fluxos de Usuário Principais

#### 1.1 Gestão de Funcionários
```bash
# Criar funcionário
curl -X POST https://app.auditoria360.com.br/api/v1/employees \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Test",
    "cpf": "12345678901",
    "email": "joao.test@example.com",
    "role": "employee"
  }'
# Esperado: HTTP 201 + employee_id

# Buscar funcionário
curl -H "Authorization: Bearer $TOKEN" \
  https://app.auditoria360.com.br/api/v1/employees/{id}
# Esperado: HTTP 200 + dados do funcionário
```

#### 1.2 Processamento de Folha
```bash
# Upload de planilha de folha
curl -X POST https://app.auditoria360.com.br/api/v1/payroll/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@folha-test.xlsx"
# Esperado: HTTP 201 + processing_id

# Verificar processamento
curl -H "Authorization: Bearer $TOKEN" \
  https://app.auditoria360.com.br/api/v1/payroll/processing/{id}/status
# Esperado: HTTP 200 + status: "completed"
```

#### 1.3 Geração de Relatórios
```bash
# Gerar relatório de auditoria
curl -X POST https://app.auditoria360.com.br/api/v1/reports/audit \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "period": "2025-07",
    "type": "compliance"
  }'
# Esperado: HTTP 201 + report_id
```

### 2. Integração com Serviços Externos

#### 2.1 Verificação eSocial (Simulado)
```bash
# Test eSocial integration
curl -X POST https://app.auditoria360.com.br/api/v1/esocial/validate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"employee_id": "123", "period": "2025-07"}'
# Esperado: HTTP 200 + validation results
```

#### 2.2 Integração Receita Federal (Simulado)
```bash
# Test CPF validation
curl -X POST https://app.auditoria360.com.br/api/v1/validation/cpf \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cpf": "12345678901"}'
# Esperado: HTTP 200 + validation status
```

---

## 🔍 VALIDAÇÃO DE COMPLIANCE (T+8h a T+12h)

### 1. LGPD Compliance

#### 1.1 Exportação de Dados
```bash
# Test data export (LGPD Article 15)
curl -X POST https://app.auditoria360.com.br/api/v1/gdpr/export \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-user", "format": "json"}'
# Esperado: HTTP 202 + export_id
```

#### 1.2 Anonimização de Dados
```bash
# Test data anonymization
curl -X POST https://app.auditoria360.com.br/api/v1/gdpr/anonymize \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-user", "reason": "user_request"}'
# Esperado: HTTP 202 + anonymization_id
```

#### 1.3 Verificação de Auditoria
```bash
# Verificar logs de auditoria
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  "https://app.auditoria360.com.br/api/v1/audit/logs?since=2025-07-31T00:00:00Z"
# Esperado: HTTP 200 + logs de deploy e validação
```

### 2. Isolamento Multi-Tenant

#### 2.1 Teste de Isolamento
```bash
# Login como tenant A
TOKEN_A=$(curl -X POST https://app.auditoria360.com.br/api/v1/auth/login \
  -d '{"username": "user_a", "password": "pass"}' | jq -r '.access_token')

# Login como tenant B  
TOKEN_B=$(curl -X POST https://app.auditoria360.com.br/api/v1/auth/login \
  -d '{"username": "user_b", "password": "pass"}' | jq -r '.access_token')

# Verificar que tenant A não vê dados de tenant B
curl -H "Authorization: Bearer $TOKEN_A" \
  https://app.auditoria360.com.br/api/v1/employees
# Deve retornar apenas funcionários do tenant A
```

---

## 📱 VALIDAÇÃO DE INTERFACE (T+12h a T+16h)

### 1. Testes de Frontend

#### 1.1 Carregamento de Páginas
```bash
# Verificar páginas principais
PAGES=("/" "/login" "/dashboard" "/employees" "/payroll" "/reports")
for page in "${PAGES[@]}"; do
  echo "Testing $page:"
  curl -s -o /dev/null -w "%{http_code} %{time_total}s" \
    "https://auditoria360.com.br$page"
  echo
done
# Target: HTTP 200, <2s load time
```

#### 1.2 JavaScript/CSS Resources
```bash
# Verificar assets principais
curl -f https://auditoria360.com.br/static/js/main.js
curl -f https://auditoria360.com.br/static/css/main.css
# Esperado: HTTP 200 para todos os assets
```

### 2. Responsividade e Compatibilidade

#### 2.1 Mobile Testing (via User-Agent)
```bash
# Test mobile view
curl -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)" \
  https://auditoria360.com.br/
# Verificar viewport meta tag e responsive design
```

---

## 📈 VALIDAÇÃO DE MONITORAMENTO (T+16h a T+24h)

### 1. Verificação de Métricas

#### 1.1 Prometheus Metrics
```bash
# Verificar coleta de métricas
curl -s http://prometheus:9090/api/v1/query?query=up{job="auditoria360"}
# Esperado: Todos os targets "up"

# Verificar métricas de aplicação
curl -s http://prometheus:9090/api/v1/query?query=http_requests_total
# Esperado: Métricas sendo coletadas
```

#### 1.2 Grafana Dashboards
```bash
# Verificar dashboards
curl -f http://grafana:3000/api/dashboards/uid/auditoria360-main
# Esperado: Dashboard carregando corretamente
```

### 2. Alertas e Notificações

#### 2.1 Test Alert Manager
```bash
# Simular alerta de teste
curl -X POST http://alertmanager:9093/api/v1/alerts \
  -H "Content-Type: application/json" \
  -d '[{
    "labels": {"alertname": "TestAlert", "severity": "warning"},
    "annotations": {"summary": "Test alert for validation"}
  }]'
# Verificar se alerta é recebido nos canais configurados
```

---

## 📋 CHECKLIST DE VALIDAÇÃO FINAL

### ✅ Validação Imediata (T+30min)
- [ ] API Health checks passando
- [ ] Frontend carregando corretamente
- [ ] Database conectado e responsivo
- [ ] Cache funcionando
- [ ] Storage acessível
- [ ] Autenticação funcionando
- [ ] MFA ativo para admins

### ✅ Validação de Performance (T+2h)
- [ ] Response time <200ms (95% req)
- [ ] Throughput >1000 req/s
- [ ] Cache hit rate >80%
- [ ] Zero queries >1000ms
- [ ] Load test aprovado

### ✅ Validação de Segurança (T+4h)
- [ ] Headers de segurança presentes
- [ ] TLS 1.2+ configurado
- [ ] Input validation funcionando
- [ ] Rate limiting ativo
- [ ] XSS/SQL injection bloqueados

### ✅ Validação Funcional (T+8h)
- [ ] CRUD de funcionários funcionando
- [ ] Upload e processamento de folha
- [ ] Geração de relatórios
- [ ] IA Assistant respondendo
- [ ] OCR processando documentos
- [ ] Integrações externas funcionais

### ✅ Validação de Compliance (T+12h)
- [ ] Exportação LGPD funcionando
- [ ] Anonimização implementada
- [ ] Logs de auditoria gerados
- [ ] Isolamento multi-tenant validado
- [ ] Trilha de auditoria completa

### ✅ Validação de Interface (T+16h)
- [ ] Todas as páginas carregando
- [ ] Assets estáticos disponíveis
- [ ] Mobile responsivo
- [ ] JavaScript funcionando
- [ ] UX sem regressões

### ✅ Validação de Monitoramento (T+24h)
- [ ] Métricas sendo coletadas
- [ ] Dashboards funcionando
- [ ] Alertas configurados
- [ ] Logs centralizados
- [ ] Observabilidade completa

---

## 📊 RELATÓRIO DE VALIDAÇÃO

### Template de Relatório

```markdown
# Relatório de Validação Pós-Deploy v1.0.0

**Data**: 31 de Julho de 2025
**Responsável**: [Nome]
**Duração**: [XX] horas

## Resumo Executivo
- ✅ Deploy bem-sucedido
- ✅ Todas as validações aprovadas
- ✅ Sistema estável e operacional

## Métricas Alcançadas
- **Availability**: 100%
- **Response Time**: XXXms (Target: <200ms)
- **Error Rate**: 0.0X% (Target: <1%)
- **Throughput**: XXXX req/s (Target: >1000)

## Funcionalidades Validadas
- [x] Autenticação e autorização
- [x] Gestão de funcionários
- [x] Processamento de folha
- [x] Relatórios e dashboards
- [x] IA e OCR
- [x] Compliance LGPD

## Issues Identificados
- Nenhum issue crítico
- [Lista de issues menores, se houver]

## Recomendações
- Continuar monitoramento por 48h
- [Outras recomendações]

## Conclusão
Sistema v1.0.0 validado e pronto para operação completa.
```

---

> **✅ Post-Deployment Validation v1.0.0**: Procedimentos completos para garantir que o sistema está operando perfeitamente após o deploy.

**Última atualização**: 30 de Julho de 2025  
**Responsável**: QA Team + DevOps Team