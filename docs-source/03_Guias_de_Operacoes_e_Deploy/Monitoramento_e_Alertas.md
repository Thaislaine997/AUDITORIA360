# 🔧 Monitoramento e Alertas - AUDITORIA360

## 🎯 Objetivo

Este documento descreve a estratégia completa de observabilidade da AUDITORIA360, incluindo monitoramento de aplicação, infraestrutura, alertas e dashboards operacionais.

## 📊 Stack de Observabilidade

### Componentes Principais
- **📈 Prometheus**: Coleta de métricas
- **📊 Grafana**: Visualização e dashboards
- **📝 Loki**: Agregação de logs
- **🔍 Jaeger**: Distributed tracing
- **⚠️ AlertManager**: Gestão de alertas

### Integração com Cloud
- **☁️ Cloudflare Analytics**: Métricas de CDN
- **🗄️ PostgreSQL Monitoring**: Métricas de banco
- **🔴 Redis Monitoring**: Performance de cache
- **🐳 Docker Stats**: Métricas de containers

## 📈 Métricas Principais

### Métricas de Aplicação

#### Performance HTTP
```prometheus
# Tempo de resposta por endpoint
http_request_duration_seconds{method="GET", endpoint="/api/funcionarios"}

# Taxa de requests por segundo
rate(http_requests_total[5m])

# Taxa de erro 5xx
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])
```

#### Métricas de Negócio
```prometheus
# Auditorias realizadas por hora
auditoria360_auditorias_total

# Irregularidades detectadas
auditoria360_irregularidades_total

# Usuários ativos
auditoria360_usuarios_ativos

# Uploads processados
auditoria360_uploads_processados_total

# Relatórios gerados
auditoria360_relatorios_gerados_total
```

#### Métricas de Sistema
```prometheus
# CPU usage
cpu_usage_percent

# Memory usage
memory_usage_percent

# Disk usage
disk_usage_percent

# Network I/O
network_bytes_total
```

### Métricas de Banco de Dados

```sql
-- Conexões ativas
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

-- Queries lentas
SELECT query, mean_exec_time 
FROM pg_stat_statements 
WHERE mean_exec_time > 1000 
ORDER BY mean_exec_time DESC;

-- Tamanho das tabelas
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## 🚨 Alertas Críticos

### Alertas de Infraestrutura

#### CPU Alto
```yaml
alert: HighCPUUsage
expr: cpu_usage_percent > 80
for: 5m
labels:
  severity: warning
annotations:
  summary: "CPU usage alto no servidor {{ $labels.instance }}"
  description: "CPU em {{ $value }}% por mais de 5 minutos"
```

#### Memória Esgotada
```yaml
alert: HighMemoryUsage
expr: memory_usage_percent > 90
for: 2m
labels:
  severity: critical
annotations:
  summary: "Memória crítica no servidor {{ $labels.instance }}"
  description: "Uso de memória em {{ $value }}%"
```

#### Disco Cheio
```yaml
alert: DiskSpaceRunningOut
expr: disk_usage_percent > 85
for: 5m
labels:
  severity: warning
annotations:
  summary: "Espaço em disco baixo"
  description: "Apenas {{ $value }}% de espaço livre"
```

### Alertas de Aplicação

#### Taxa de Erro Alta
```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
for: 2m
labels:
  severity: critical
annotations:
  summary: "Taxa de erro HTTP alta"
  description: "{{ $value }} erros por segundo"
```

#### Latência Alta
```yaml
alert: HighLatency
expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
for: 5m
labels:
  severity: warning
annotations:
  summary: "Latência alta detectada"
  description: "P95 latência: {{ $value }}s"
```

#### Banco Indisponível
```yaml
alert: DatabaseDown
expr: up{job="postgresql"} == 0
for: 1m
labels:
  severity: critical
annotations:
  summary: "Banco de dados indisponível"
  description: "PostgreSQL não está respondendo"
```

## 📊 Dashboards Operacionais

### Dashboard Principal - AUDITORIA360

#### Seção 1: Overview Geral
- **🔄 Status da Aplicação**: Up/Down status
- **📊 Requests/sec**: Taxa de requisições
- **⏱️ Response Time**: Tempo médio de resposta
- **❌ Error Rate**: Taxa de erros 5xx
- **👥 Usuários Ativos**: Usuários logados atualmente

#### Seção 2: Performance
- **📈 CPU Usage**: Uso de CPU por servidor
- **💾 Memory Usage**: Consumo de memória
- **💿 Disk I/O**: Operações de disco
- **🌐 Network**: Tráfego de rede

#### Seção 3: Métricas de Negócio
- **🔍 Auditorias por Hora**: Volume de auditorias
- **⚠️ Irregularidades**: Detecções por período
- **📄 Relatórios Gerados**: Relatórios por tipo
- **📤 Uploads**: Volume de arquivos processados

### Dashboard de Banco de Dados

#### PostgreSQL Metrics
- **🔌 Conexões**: Ativas/Máximo
- **📊 QPS**: Queries por segundo
- **⏱️ Query Time**: Tempo médio de queries
- **🔒 Locks**: Locks ativos
- **💾 Cache Hit Ratio**: Taxa de acerto do cache

### Dashboard de Infrastructure

#### Docker Containers
- **📦 Container Status**: Up/Down por container
- **💾 Resource Usage**: CPU/Memory por container
- **📊 Container Logs**: Logs em tempo real
- **🔄 Restart Count**: Contagem de restarts

## 🔔 Configuração de Notificações

### Canais de Alertas

#### Slack Integration
```yaml
slack_configs:
  - api_url: 'https://hooks.slack.com/services/...'
    channel: '#ops-alerts'
    title: 'AUDITORIA360 Alert'
    text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
```

#### Email Alerts
```yaml
email_configs:
  - to: 'ops-team@auditoria360.com.br'
    from: 'alerts@auditoria360.com.br'
    subject: 'AUDITORIA360 Alert: {{ .GroupLabels.alertname }}'
    body: |
      {{ range .Alerts }}
      Alert: {{ .Annotations.summary }}
      Description: {{ .Annotations.description }}
      {{ end }}
```

#### WhatsApp Business (via Twilio)
```python
# Integração para alertas críticos
def send_whatsapp_alert(message, severity):
    if severity == 'critical':
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"🚨 AUDITORIA360 CRÍTICO: {message}",
            from_='whatsapp:+14155238886',
            to='whatsapp:+5511999999999'
        )
```

### Escalação de Alertas

#### Nível 1: Avisos (Warning)
- **Canais**: Slack #dev-alerts
- **Horário**: 8h às 18h
- **Frequência**: A cada 30 minutos

#### Nível 2: Crítico (Critical)
- **Canais**: Slack #ops-alerts + Email + SMS
- **Horário**: 24/7
- **Frequência**: Imediato + a cada 15 minutos

#### Nível 3: Emergência (Emergency)
- **Canais**: Todos + WhatsApp + Ligação
- **Horário**: 24/7
- **Frequência**: Imediato + a cada 5 minutos

## 📝 Logging Strategy

### Estrutura de Logs

#### Formato JSON Estruturado
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "logger": "auditoria360.api",
  "message": "Auditoria iniciada",
  "request_id": "req_abc123",
  "user_id": 456,
  "client_id": "empresa_123",
  "endpoint": "/api/auditorias",
  "method": "POST",
  "response_time": 234,
  "status_code": 201
}
```

#### Níveis de Log
- **DEBUG**: Informações detalhadas para desenvolvimento
- **INFO**: Operações normais da aplicação
- **WARNING**: Situações que requerem atenção
- **ERROR**: Erros que não interrompem a aplicação
- **CRITICAL**: Erros que podem interromper o serviço

### Agregação com Loki

```yaml
# promtail.yml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
- job_name: auditoria360
  static_configs:
  - targets:
      - localhost
    labels:
      job: auditoria360
      __path__: /var/log/auditoria360/*.log
```

## 🔍 Tracing com Jaeger

### Instrumentação de Código

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configuração do tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=14268,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrumentação de funções
@tracer.start_as_current_span("processo_auditoria")
def processar_auditoria(funcionario_id):
    with tracer.start_as_current_span("validar_dados") as span:
        span.set_attribute("funcionario.id", funcionario_id)
        # lógica de validação
        
    with tracer.start_as_current_span("calcular_valores"):
        # cálculos da auditoria
        pass
```

## 📱 Health Checks

### Endpoints de Status

```python
@app.get("/health")
async def health_check():
    """Health check básico."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/ready")
async def readiness_check():
    """Verifica se aplicação está pronta."""
    checks = await run_readiness_checks()
    
    if all(check["healthy"] for check in checks.values()):
        return {"status": "ready", "checks": checks}
    else:
        raise HTTPException(
            status_code=503,
            detail={"status": "not_ready", "checks": checks}
        )

@app.get("/metrics")
async def metrics():
    """Métricas para Prometheus."""
    return Response(
        generate_latest(REGISTRY),
        media_type="text/plain"
    )
```

### Monitoramento Externo

```bash
#!/bin/bash
# Script de monitoramento externo

ENDPOINT="https://auditoria360.com.br/health"
EXPECTED_STATUS="healthy"

response=$(curl -s "$ENDPOINT" | jq -r '.status')

if [ "$response" != "$EXPECTED_STATUS" ]; then
    echo "CRITICAL: Health check failed - Status: $response"
    # Enviar alerta
    exit 2
else
    echo "OK: Application healthy"
    exit 0
fi
```

## 🚀 Deployment Monitoring

### Blue-Green Deployment Monitoring

```yaml
# Monitor durante deploy
deployment_monitor:
  pre_deploy:
    - check_database_connectivity
    - verify_migrations
    - validate_config
  
  during_deploy:
    - monitor_error_rates
    - track_response_times
    - watch_resource_usage
  
  post_deploy:
    - run_smoke_tests
    - verify_all_endpoints
    - check_business_metrics
```

## 📋 Runbooks

### Incident Response

#### High CPU Usage
1. **Identificar causa**: Verificar top processes
2. **Avaliar impacto**: Checar métricas de resposta
3. **Ação imediata**: Scale horizontal se necessário
4. **Investigação**: Analisar logs para processos anômalos
5. **Resolução**: Otimizar queries ou adicionar recursos

#### Database Connection Issues
1. **Verificar conectividade**: `pg_isready`
2. **Checar pool de conexões**: Monitorar conexões ativas
3. **Restart se necessário**: Reiniciar aplicação
4. **Escalação**: Contatar DBA se problema persistir

---

💡 **Lembre-se**: Observabilidade é fundamental para manter a AUDITORIA360 funcionando com excelência 24/7.

🚨 **Em caso de dúvidas**: Consulte o [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) ou escalonate para a equipe de SRE.