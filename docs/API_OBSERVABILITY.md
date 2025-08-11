# AUDITORIA360 - API Pública e Observabilidade

## Documentação da API

### Endpoints Públicos

#### Status do Sistema
```http
GET /api/health/public
```

**Resposta:**
```json
{
  "system": "AUDITORIA360",
  "status": "operational",
  "version": "1.0.0",
  "services": {
    "api": "operational",
    "database": "operational",
    "ai_integration": "operational"
  },
  "timestamp": "2025-08-11T20:30:00Z"
}
```

#### Health Check Geral
```http
GET /api/health/status
```

**Resposta:**
```json
{
  "status": "healthy",
  "health_percentage": 95.5,
  "healthy_modules": 14,
  "total_modules": 15,
  "modules": [
    {
      "name": "Dashboard Estratégico",
      "status": "ok",
      "response_time": 0.045,
      "details": "All dependencies healthy",
      "timestamp": "2025-08-11T20:30:00Z"
    }
  ],
  "response_time": 0.123,
  "timestamp": "2025-08-11T20:30:00Z"
}
```

#### Métricas Agregadas
```http
GET /api/metrics/summary
```

**Resposta:**
```json
{
  "system_metrics": {
    "uptime": "99.9%",
    "total_requests": 150420,
    "avg_response_time": 0.089,
    "error_rate": 0.1
  },
  "business_metrics": {
    "total_audits": 5420,
    "active_clients": 89,
    "reports_generated": 1203,
    "ai_requests": 8940
  },
  "timestamp": "2025-08-11T20:30:00Z"
}
```

### Autenticação

#### API Keys
Para endpoints protegidos, use API key no header:
```http
Authorization: Bearer YOUR_API_KEY
```

#### Rate Limiting
- **Público**: 100 requests/minuto
- **Autenticado**: 1000 requests/minuto

## Observabilidade

### Estrutura de Logs

#### Formato Estruturado (JSON)
```json
{
  "timestamp": "2025-08-11T20:30:00.123Z",
  "level": "INFO",
  "service": "auditoria360-api",
  "module": "dashboard",
  "user_id": "user-123",
  "client_id": "client-456",
  "request_id": "req-789",
  "message": "Dashboard data loaded successfully",
  "duration_ms": 45,
  "metadata": {
    "endpoint": "/api/dashboard/data",
    "method": "GET",
    "status_code": 200,
    "user_agent": "Mozilla/5.0..."
  }
}
```

#### Níveis de Log
- **ERROR**: Erros que requerem atenção imediata
- **WARN**: Situações anômalas que não são erros
- **INFO**: Eventos importantes do sistema
- **DEBUG**: Informações detalhadas para debugging

### Métricas de Sistema

#### Application Metrics
```prometheus
# Requests por segundo
auditoria360_requests_total{method="GET",endpoint="/api/dashboard"} 1543

# Tempo de resposta
auditoria360_request_duration_seconds{method="GET",endpoint="/api/dashboard"} 0.045

# Erros por tipo
auditoria360_errors_total{type="validation_error"} 23

# Usuários ativos
auditoria360_active_users 89

# Auditorias em execução
auditoria360_audits_running 12
```

#### Business Metrics
```prometheus
# Auditorias completadas
auditoria360_audits_completed_total 5420

# Relatórios gerados
auditoria360_reports_generated_total 1203

# Uso de IA
auditoria360_ai_requests_total{model="audit-analyzer"} 8940

# Score médio de auditoria
auditoria360_audit_score_avg 8.7
```

#### Infrastructure Metrics
```prometheus
# CPU usage
auditoria360_cpu_usage_percent 45.2

# Memory usage
auditoria360_memory_usage_bytes 2147483648

# Database connections
auditoria360_db_connections_active 12

# Cache hit rate
auditoria360_cache_hit_rate 0.89
```

### Distributed Tracing

#### Trace Context
Cada request recebe um trace ID único:
```http
X-Trace-ID: trace-abc-123-def
```

#### Span Structure
```json
{
  "trace_id": "trace-abc-123-def",
  "span_id": "span-456",
  "parent_span_id": "span-123",
  "operation_name": "dashboard.load_data",
  "start_time": "2025-08-11T20:30:00.000Z",
  "end_time": "2025-08-11T20:30:00.045Z",
  "duration_ms": 45,
  "tags": {
    "user_id": "user-123",
    "client_id": "client-456",
    "component": "dashboard-service"
  },
  "logs": [
    {
      "timestamp": "2025-08-11T20:30:00.010Z",
      "message": "Querying database for KPIs"
    },
    {
      "timestamp": "2025-08-11T20:30:00.040Z", 
      "message": "Data transformation completed"
    }
  ]
}
```

### Dashboards de Monitoramento

#### System Overview Dashboard
- **Uptime**: 99.9%
- **Request Rate**: 150 req/min
- **Error Rate**: 0.1%
- **Response Time P95**: 120ms
- **Active Users**: 89
- **Health Score**: 95.5%

#### Business Metrics Dashboard
- **Daily Audits**: 45
- **Reports Generated**: 23
- **AI Usage**: 234 requests
- **Client Growth**: +3 this month
- **Feature Adoption**: Dashboard (100%), Reports (89%), Simulator (45%)

#### Infrastructure Dashboard
- **CPU**: 45% avg
- **Memory**: 2.1GB used
- **Database**: 12 active connections
- **Cache**: 89% hit rate
- **Storage**: 75% used

### Alerting

#### Alert Rules

```yaml
groups:
  - name: auditoria360.critical
    rules:
      - alert: SystemDown
        expr: up{job="auditoria360"} == 0
        for: 1m
        annotations:
          summary: "AUDITORIA360 sistema indisponível"
          
      - alert: HighErrorRate
        expr: rate(auditoria360_errors_total[5m]) > 0.05
        for: 2m
        annotations:
          summary: "Alta taxa de erro: {{ $value }}%"
          
      - alert: SlowResponse
        expr: histogram_quantile(0.95, auditoria360_request_duration_seconds) > 1
        for: 2m
        annotations:
          summary: "Tempo de resposta alto: {{ $value }}s"
          
      - alert: LowHealthScore
        expr: auditoria360_health_score < 80
        for: 5m
        annotations:
          summary: "Score de saúde baixo: {{ $value }}%"
```

#### Notification Channels
- **Slack**: #auditoria360-alerts
- **Email**: tech@auditoria360.com
- **PagerDuty**: Critical alerts only
- **Teams**: General alerts

### Debugging

#### Request Tracing
Para debug de requests específicos:
```bash
# Buscar por trace ID
grep "trace-abc-123-def" /var/log/auditoria360/*.log

# Ou via API
curl -H "Authorization: Bearer API_KEY" \
  "https://api.auditoria360.com/api/debug/trace/trace-abc-123-def"
```

#### Performance Analysis
```bash
# Top endpoints por latência
curl -H "Authorization: Bearer API_KEY" \
  "https://api.auditoria360.com/api/metrics/slow-endpoints"

# Análise de errors
curl -H "Authorization: Bearer API_KEY" \
  "https://api.auditoria360.com/api/metrics/errors?hours=24"
```

### Health Check Endpoints

#### Liveness Probe
```http
GET /api/health/live
```
Retorna 200 se o serviço está rodando.

#### Readiness Probe  
```http
GET /api/health/ready
```
Retorna 200 se o serviço está pronto para receber tráfego.

#### Startup Probe
```http
GET /api/health/startup
```
Retorna 200 se o serviço completou a inicialização.

### Configuration

#### Environment Variables
```bash
# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Metrics
METRICS_ENABLED=true
METRICS_PORT=9090

# Tracing  
TRACING_ENABLED=true
JAEGER_ENDPOINT=http://jaeger:14268/api/traces

# Health Checks
HEALTH_CHECK_INTERVAL=30s
HEALTH_CHECK_TIMEOUT=5s
```

#### Prometheus Configuration
```yaml
scrape_configs:
  - job_name: 'auditoria360'
    static_configs:
      - targets: ['api:9090']
    scrape_interval: 15s
    metrics_path: /metrics
```

### SLA e SLO

#### Service Level Objectives (SLO)
- **Uptime**: 99.9% (43 minutos downtime/mês)
- **Response Time**: P95 < 500ms
- **Error Rate**: < 0.1%
- **Health Score**: > 95%

#### Service Level Indicators (SLI)
- **Availability**: successful requests / total requests
- **Latency**: request duration P95
- **Quality**: (total requests - errors) / total requests
- **Throughput**: requests per second

#### Service Level Agreements (SLA)
- **Uptime Garantido**: 99.5%
- **Suporte Resposta**: < 2 horas (business hours)
- **Incident Resolution**: < 4 horas (crítico)
- **Data Backup**: RPO < 1 hora, RTO < 4 horas

---

## Integrações

### Exportação de Dados

#### Logs para ELK Stack
```yaml
filebeat:
  inputs:
    - type: log
      paths: ["/var/log/auditoria360/*.jsonl"]
      fields:
        service: auditoria360
```

#### Métricas para Prometheus
```python
from prometheus_client import Counter, Histogram, Gauge

request_count = Counter('auditoria360_requests_total', 'Total requests')
request_duration = Histogram('auditoria360_request_duration_seconds', 'Request duration')
active_users = Gauge('auditoria360_active_users', 'Active users')
```

#### Traces para Jaeger
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

tracer = trace.get_tracer(__name__)
exporter = JaegerExporter(agent_host_name="jaeger", agent_port=6831)
```

---

**Última Atualização:** 2025-08-11  
**Responsável:** DevOps & Platform Team