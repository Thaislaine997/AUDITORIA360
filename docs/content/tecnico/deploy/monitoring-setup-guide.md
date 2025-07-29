# 📊 Monitoring Setup Guide - AUDITORIA360

## Visão Geral

Este guia completo aborda a implementação e configuração do sistema de monitoramento avançado do AUDITORIA360, incluindo métricas, alertas e dashboards.

---

## 🚀 Configuração Inicial

### 1. Instalação de Dependências

```bash
# Instalar dependências de monitoramento
pip install prometheus-client psutil requests

# Para alertas por email
pip install smtplib

# Para integração com Slack
pip install slack-sdk
```

### 2. Configuração Básica

```python
from src.utils.monitoring import MonitoringSystem

# Inicializar sistema de monitoramento
monitoring = MonitoringSystem()

# Iniciar coleta de métricas
monitoring.start()
```

---

## 📈 Sistema de Métricas

### 1. Tipos de Métricas

#### Counter (Contador)

```python
# Incrementar contador de requests
monitoring.metrics.increment_counter("api_requests_total",
                                    labels={"endpoint": "/api/v1/auditorias"})

# Incrementar contador de erros
monitoring.metrics.increment_counter("api_errors_total",
                                    labels={"endpoint": "/api/v1/auditorias", "status": "500"})
```

#### Gauge (Medidor)

```python
# Métricas de sistema (coletadas automaticamente)
monitoring.metrics.set_gauge("system_cpu_percent", 45.2)
monitoring.metrics.set_gauge("system_memory_percent", 67.8)

# Métricas customizadas
monitoring.metrics.set_gauge("active_users", 125)
monitoring.metrics.set_gauge("pending_audits", 23)
```

#### Histogram (Histograma)

```python
# Tempo de resposta
monitoring.metrics.record_histogram("api_response_time_ms", 250.5,
                                   labels={"endpoint": "/api/v1/auditorias"})

# Tamanho de uploads
monitoring.metrics.record_histogram("upload_size_bytes", 1024000,
                                   labels={"type": "document"})
```

### 2. Métricas Automáticas do Sistema

O sistema coleta automaticamente:

| Métrica                     | Descrição             | Labels                  |
| --------------------------- | --------------------- | ----------------------- |
| `system_cpu_percent`        | Uso de CPU do sistema | `type: overall`         |
| `system_memory_percent`     | Uso de memória        | `type: virtual`         |
| `system_disk_percent`       | Uso de disco          | `mountpoint: /`         |
| `system_network_bytes_sent` | Bytes enviados        | `direction: sent`       |
| `system_network_bytes_recv` | Bytes recebidos       | `direction: received`   |
| `process_memory_percent`    | Memória do processo   | `type: current_process` |
| `process_cpu_percent`       | CPU do processo       | `type: current_process` |

### 3. Métricas Específicas do AUDITORIA360

```python
# Métricas de auditoria
monitoring.metrics.increment_counter("auditorias_processadas_total")
monitoring.metrics.set_gauge("auditorias_pendentes", 15)
monitoring.metrics.record_histogram("auditoria_processing_time_ms", 2500)

# Métricas de OCR
monitoring.metrics.increment_counter("ocr_documents_processed_total")
monitoring.metrics.record_histogram("ocr_processing_time_ms", 1800)

# Métricas de folha de pagamento
monitoring.metrics.increment_counter("folha_calculations_total")
monitoring.metrics.set_gauge("funcionarios_ativos", 1500)

# Métricas de CCT
monitoring.metrics.increment_counter("cct_comparisons_total")
monitoring.metrics.set_gauge("cct_documents_count", 250)
```

---

## 🚨 Sistema de Alertas

### 1. Configuração de Alertas

```python
from src.utils.monitoring import AlertSeverity

# Alerta de alto uso de CPU
monitoring.alert_manager.add_alert_rule(
    metric_name="system_cpu_percent",
    threshold=80,
    condition="gt",  # greater than
    severity=AlertSeverity.HIGH,
    title="Alto Uso de CPU",
    description="Uso de CPU acima de 80% detectado"
)

# Alerta de muitas auditorias pendentes
monitoring.alert_manager.add_alert_rule(
    metric_name="auditorias_pendentes",
    threshold=50,
    condition="gt",
    severity=AlertSeverity.MEDIUM,
    title="Muitas Auditorias Pendentes",
    description="Mais de 50 auditorias aguardando processamento"
)

# Alerta de erro rate alto
monitoring.alert_manager.add_alert_rule(
    metric_name="api_error_rate",
    threshold=5.0,  # 5%
    condition="gt",
    severity=AlertSeverity.HIGH,
    title="Taxa de Erro Alta",
    description="Taxa de erro da API acima de 5%"
)
```

### 2. Canais de Notificação

#### Email

```python
email_config = {
    'from_email': 'alerts@auditoria360.com',
    'to_emails': ['admin@empresa.com', 'dev@empresa.com'],
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'username': 'alerts@auditoria360.com',
    'password': 'sua_senha_app'
}

monitoring.alert_manager.add_notification_channel('email', email_config)
```

#### Slack

```python
slack_config = {
    'webhook_url': 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
}

monitoring.alert_manager.add_notification_channel('slack', slack_config)
```

#### Webhook Customizado

```python
webhook_config = {
    'url': 'https://api.empresa.com/alerts',
    'headers': {
        'Authorization': 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    }
}

monitoring.alert_manager.add_notification_channel('webhook', webhook_config)
```

### 3. Gerenciamento de Alertas

```python
# Listar alertas ativos
active_alerts = monitoring.alert_manager.get_active_alerts()
for alert in active_alerts:
    print(f"[{alert.severity.value}] {alert.title}")
    print(f"Métrica: {alert.metric_name} = {alert.current_value}")

# Resolver alerta manualmente
monitoring.alert_manager.resolve_alert("alert_id_123")
```

---

## 🏥 Health Checks

### 1. Health Checks Básicos

```python
# Check de banco de dados
async def check_database():
    try:
        # Testar conexão com Neon
        async with get_database_connection() as conn:
            await conn.execute("SELECT 1")
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# Check de armazenamento R2
async def check_storage():
    try:
        # Testar conexão com Cloudflare R2
        s3_client = get_s3_client()
        s3_client.list_objects_v2(Bucket='auditoria360-bucket', MaxKeys=1)
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# Adicionar health checks
monitoring.health_checker.add_health_check("database", check_database, interval=60)
monitoring.health_checker.add_health_check("storage", check_storage, interval=120)
```

### 2. Health Checks Customizados

```python
# Check de API externa
async def check_external_api():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.externa.com/health", timeout=5)
            if response.status_code == 200:
                return {"status": "healthy", "details": {"response_time": response.elapsed.total_seconds()}}
            else:
                return {"status": "degraded", "details": {"status_code": response.status_code}}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# Check de fila de processamento
async def check_processing_queue():
    try:
        queue_size = get_queue_size()  # Implementar conforme sua fila
        if queue_size < 100:
            return {"status": "healthy", "details": {"queue_size": queue_size}}
        elif queue_size < 500:
            return {"status": "degraded", "details": {"queue_size": queue_size}}
        else:
            return {"status": "unhealthy", "details": {"queue_size": queue_size, "error": "Queue too large"}}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

---

## 📊 Dashboard e Visualização

### 1. Endpoint de Dashboard

```python
from fastapi import FastAPI
from src.utils.monitoring import get_monitoring_system

app = FastAPI()

@app.get("/api/v1/monitoring/dashboard")
async def get_monitoring_dashboard():
    monitoring = get_monitoring_system()
    return monitoring.get_dashboard_data()

@app.get("/api/v1/monitoring/metrics")
async def get_metrics(hours: int = 1):
    monitoring = get_monitoring_system()
    return monitoring.metrics.get_metrics_summary(hours=hours)

@app.get("/api/v1/monitoring/alerts")
async def get_active_alerts():
    monitoring = get_monitoring_system()
    return [asdict(alert) for alert in monitoring.alert_manager.get_active_alerts()]

@app.get("/api/v1/monitoring/health")
async def get_health_status():
    monitoring = get_monitoring_system()
    results = await monitoring.health_checker.run_all_checks()
    return [asdict(result) for result in results]
```

### 2. Dashboard Frontend (Streamlit)

```python
import streamlit as st
import plotly.graph_objects as go
import requests

def create_monitoring_dashboard():
    st.set_page_config(page_title="AUDITORIA360 Monitoring", layout="wide")

    st.title("🔧 AUDITORIA360 - Sistema de Monitoramento")

    # Carregar dados
    dashboard_data = requests.get("http://localhost:8000/api/v1/monitoring/dashboard").json()

    # Status geral
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Status do Sistema", dashboard_data['system_status'].upper())

    with col2:
        active_alerts = len(dashboard_data['active_alerts'])
        st.metric("Alertas Ativos", active_alerts)

    with col3:
        healthy_checks = len([h for h in dashboard_data['health_checks'] if h['status'] == 'healthy'])
        total_checks = len(dashboard_data['health_checks'])
        st.metric("Health Checks", f"{healthy_checks}/{total_checks}")

    with col4:
        cpu_usage = dashboard_data['metrics_summary'].get('system_cpu_percent', {}).get('latest', 0)
        st.metric("CPU Usage", f"{cpu_usage:.1f}%")

    # Gráficos de métricas
    st.subheader("📈 Métricas do Sistema")

    # Implementar gráficos com Plotly
    # ... código dos gráficos ...

if __name__ == "__main__":
    create_monitoring_dashboard()
```

---

## 🛠️ Configuração Avançada

### 1. Configuração via Variáveis de Ambiente

```bash
# .env
MONITORING_ENABLED=true
MONITORING_INTERVAL=30
ALERT_EMAIL_ENABLED=true
ALERT_SLACK_ENABLED=true
METRICS_RETENTION_HOURS=48
HEALTH_CHECK_INTERVAL=60

# Email configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=alerts@auditoria360.com
SMTP_PASSWORD=sua_senha

# Slack configuration
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
```

### 2. Configuração Programática

```python
import os
from src.utils.monitoring import MonitoringSystem

def setup_monitoring():
    monitoring = MonitoringSystem()

    # Configurar intervalos
    monitoring.system_monitor.interval = int(os.getenv('MONITORING_INTERVAL', 30))
    monitoring.alert_manager.evaluation_interval = int(os.getenv('ALERT_INTERVAL', 60))

    # Configurar retenção
    monitoring.metrics.retention_hours = int(os.getenv('METRICS_RETENTION_HOURS', 24))

    # Configurar notificações se habilitadas
    if os.getenv('ALERT_EMAIL_ENABLED', 'false').lower() == 'true':
        email_config = {
            'from_email': os.getenv('SMTP_USERNAME'),
            'to_emails': os.getenv('ALERT_EMAIL_RECIPIENTS', '').split(','),
            'smtp_server': os.getenv('SMTP_SERVER'),
            'smtp_port': int(os.getenv('SMTP_PORT', 587)),
            'username': os.getenv('SMTP_USERNAME'),
            'password': os.getenv('SMTP_PASSWORD')
        }
        monitoring.alert_manager.add_notification_channel('email', email_config)

    if os.getenv('ALERT_SLACK_ENABLED', 'false').lower() == 'true':
        slack_config = {
            'webhook_url': os.getenv('SLACK_WEBHOOK_URL')
        }
        monitoring.alert_manager.add_notification_channel('slack', slack_config)

    return monitoring
```

---

## 🔧 Integração com API

### 1. Middleware de Métricas

```python
from fastapi import Request, Response
import time

@app.middleware("http")
async def monitoring_middleware(request: Request, call_next):
    start_time = time.time()

    # Incrementar contador de requests
    monitoring.metrics.increment_counter("api_requests_total",
                                        labels={"method": request.method,
                                               "endpoint": request.url.path})

    # Processar request
    response = await call_next(request)

    # Calcular tempo de resposta
    process_time = (time.time() - start_time) * 1000

    # Registrar métricas
    monitoring.metrics.record_histogram("api_response_time_ms", process_time,
                                      labels={"method": request.method,
                                             "endpoint": request.url.path,
                                             "status": str(response.status_code)})

    # Incrementar contador de respostas por status
    monitoring.metrics.increment_counter("api_responses_total",
                                        labels={"status": str(response.status_code)})

    # Adicionar header com tempo de resposta
    response.headers["X-Process-Time"] = str(process_time)

    return response
```

### 2. Decorador para Endpoints

```python
from functools import wraps

def monitor_endpoint(endpoint_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                result = await func(*args, **kwargs)

                # Registrar sucesso
                monitoring.metrics.increment_counter("endpoint_success_total",
                                                   labels={"endpoint": endpoint_name})
                return result

            except Exception as e:
                # Registrar erro
                monitoring.metrics.increment_counter("endpoint_error_total",
                                                   labels={"endpoint": endpoint_name,
                                                          "error_type": type(e).__name__})
                raise

            finally:
                # Registrar tempo de execução
                execution_time = (time.time() - start_time) * 1000
                monitoring.metrics.record_histogram("endpoint_execution_time_ms",
                                                   execution_time,
                                                   labels={"endpoint": endpoint_name})

        return wrapper
    return decorator

# Uso
@app.post("/api/v1/auditorias")
@monitor_endpoint("create_auditoria")
async def create_auditoria(auditoria_data: AuditoriaCreate):
    # Sua lógica aqui
    pass
```

---

## 📋 Checklist de Monitoramento

### ✅ Configuração Inicial

- [ ] Sistema de monitoramento inicializado
- [ ] Métricas de sistema coletadas
- [ ] Health checks configurados
- [ ] Alertas básicos criados

### ✅ Métricas

- [ ] Métricas de API (tempo resposta, erros)
- [ ] Métricas de negócio (auditorias, OCR, folha)
- [ ] Métricas de sistema (CPU, memória, disco)
- [ ] Métricas customizadas por módulo

### ✅ Alertas

- [ ] Alertas de infraestrutura configurados
- [ ] Alertas de aplicação configurados
- [ ] Canais de notificação testados
- [ ] Thresholds apropriados definidos

### ✅ Health Checks

- [ ] Database connectivity
- [ ] Storage connectivity
- [ ] External APIs
- [ ] Background jobs

### ✅ Dashboard

- [ ] Endpoint de métricas exposto
- [ ] Dashboard frontend criado
- [ ] Gráficos de tendência implementados
- [ ] Status overview disponível

---

## 🎯 Métricas Importantes para Acompanhar

### Infraestrutura

- CPU, memória, disco, rede
- Tempo de resposta da aplicação
- Rate de erros HTTP
- Tempo de conexão com banco

### Negócio

- Número de auditorias processadas
- Tempo médio de processamento OCR
- Quantidade de usuários ativos
- Documentos CCT processados

### Performance

- Tempo de resposta da API
- Queries mais lentas
- Cache hit rate
- Uso de memória por função

---

## 📞 Troubleshooting

### Problemas Comuns

1. **Alertas não funcionando**
   - Verificar configuração SMTP/Slack
   - Checar logs de erro
   - Validar thresholds

2. **Métricas não coletadas**
   - Verificar se monitoramento foi iniciado
   - Checar permissões de sistema
   - Validar decoradores

3. **Dashboard não carrega**
   - Verificar endpoint de métricas
   - Checar conectividade frontend/backend
   - Validar dados retornados

---

_Última atualização: 2025-01-28_
_Versão: 1.0.0_
