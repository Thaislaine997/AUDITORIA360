# AUDITORIA360 - Observabilidade e Monitoramento (Fase 4)

## Visão Geral

Esta implementação da Fase 4 do plano estratégico adiciona capacidades avançadas de observabilidade e monitoramento ao AUDITORIA360, proporcionando visibilidade total sobre a saúde e comportamento da aplicação em produção.

## Funcionalidades Implementadas

### 1. 📊 Métricas Prometheus + Grafana

#### Endpoint de Métricas
- **URL**: `http://localhost:8000/metrics`
- **Formato**: Prometheus
- **Atualização**: Tempo real

#### Métricas Disponíveis

**Métricas Técnicas:**
- `http_requests_total` - Total de requisições HTTP
- `http_request_duration_seconds` - Duração das requisições
- `system_cpu_usage_percent` - Uso de CPU
- `system_memory_usage_percent` - Uso de memória
- `database_connections_active` - Conexões ativas do banco

**Métricas de Negócio:**
- `auditorias_processadas_total` - Total de auditorias processadas
- `usuarios_ativos_total` - Usuários ativos por tipo
- `relatorios_gerados_total` - Relatórios gerados por tipo
- `compliance_checks_total` - Verificações de compliance

### 2. 📝 Logging Estruturado

#### Configuração
O sistema utiliza logging estruturado em formato JSON para facilitar análise centralizada:

```python
from src.monitoring.structured_logging import get_business_logger

business_logger = get_business_logger()
business_logger.log_audit_start("audit_001", "compliance", "user_123")
```

#### Tipos de Logs
- **Business Events**: Eventos de negócio (auditorias, relatórios)
- **Security Events**: Eventos de segurança (logins, acessos negados)
- **Performance Events**: Eventos de performance (queries lentas, APIs lentas)

### 3. 🔍 Rastreamento Distribuído

#### Implementação
Sistema de tracing simples com correlation IDs para rastrear requisições:

```python
from src.monitoring.tracing import trace_function

@trace_function("audit_processing")
def process_audit(audit_data):
    # Função instrumentada automaticamente
    return result
```

#### Visualização
- **Endpoint**: `/api/v1/monitoring/traces`
- **Formato**: JSON com spans e timing

### 4. 📈 Dashboards de Negócio

#### Dashboards Grafana
Localizados em `/monitoring/dashboards/`:

1. **Business Overview** (`business_overview.json`)
   - Auditorias processadas
   - Tempo médio de processamento
   - Taxa de sucesso
   - Usuários ativos

2. **Technical Performance** (`technical_performance.json`)
   - CPU e memória
   - Latência de API
   - Taxa de erro
   - Conexões de banco

## Como Usar

### 1. Executar a Aplicação

```bash
# Iniciar API
cd /home/runner/work/AUDITORIA360/AUDITORIA360
python -m uvicorn api.index:app --host 0.0.0.0 --port 8000
```

### 2. Configurar Stack de Monitoramento

```bash
# Iniciar Prometheus + Grafana
docker-compose -f docker-compose.monitoring.yml up -d
```

**Serviços disponíveis:**
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/auditoria360)
- **Jaeger**: http://localhost:16686 (opcional)

### 3. Importar Dashboards

1. Acesse Grafana: http://localhost:3001
2. Login: admin/auditoria360
3. Import dashboards de `/monitoring/dashboards/`

### 4. Verificar Métricas

```bash
# Métricas Prometheus
curl http://localhost:8000/metrics

# Métricas de negócio
curl http://localhost:8000/api/v1/monitoring/business-metrics

# Dashboard de monitoramento
curl http://localhost:8000/api/v1/monitoring/dashboard
```

## Endpoints de Monitoramento

### Métricas
- `GET /metrics` - Métricas Prometheus
- `GET /api/v1/monitoring/business-metrics` - KPIs de negócio
- `GET /api/v1/monitoring/dashboard` - Dashboard consolidado

### Eventos
- `POST /api/v1/monitoring/business-events` - Registrar evento de negócio
- `GET /api/v1/monitoring/traces` - Visualizar traces recentes

### Sistema
- `GET /health` - Health check detalhado
- `GET /api/v1/system/status` - Status do sistema

## Validação da Implementação

### 1. Validação do Monitoramento
```bash
# Verificar se métricas estão sendo expostas
curl http://localhost:8000/metrics | grep auditoria360

# Verificar Grafana
curl http://localhost:3001/api/health
```

### 2. Validação de Logs
```bash
# Gerar atividade e verificar logs
curl http://localhost:8000/api/v1/monitoring/business-events \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"type": "audit_completed", "data": {"audit_id": "test_001"}}'
```

### 3. Validação do Rastreamento
```bash
# Fazer requisição complexa e verificar trace
curl http://localhost:8000/api/v1/monitoring/traces
```

## Checklist de Qualidade

- [x] A integração com Prometheus e Grafana está funcional
- [x] Os logs estão sendo gerados em formato estruturado
- [x] O rastreamento distribuído está implementado nos fluxos principais
- [x] Os painéis de métricas de negócio foram criados e validados

## Arquivos de Configuração

### Prometheus (`monitoring/prometheus.yml`)
```yaml
scrape_configs:
  - job_name: 'auditoria360-api'
    static_configs:
      - targets: ['host.docker.internal:8000']
    metrics_path: '/metrics'
```

### Grafana Datasources (`monitoring/grafana/datasources/`)
- Prometheus configurado automaticamente
- Loki para logs (opcional)

### Docker Compose (`docker-compose.monitoring.yml`)
- Prometheus
- Grafana
- Jaeger (tracing)
- Loki (logs)

## Próximos Passos

1. **Produção**: Configurar Grafana Cloud ou instância dedicada
2. **Alertas**: Configurar alertas no Grafana baseados nas métricas
3. **Logs Centralizados**: Implementar ELK Stack ou Grafana Loki
4. **Métricas Customizadas**: Adicionar métricas específicas por módulo

## Troubleshooting

### Problema: Métricas não aparecem no Grafana
**Solução**: Verificar se a URL do Prometheus está correta em `host.docker.internal:8000`

### Problema: Logs não estruturados
**Solução**: Verificar se o `setup_structured_logging()` está sendo chamado

### Problema: Traces não aparecem
**Solução**: Verificar se o middleware de tracing está ativo nas rotas

## Benefícios Implementados

1. **Visibilidade Total**: Métricas técnicas e de negócio em tempo real
2. **Debugging Eficiente**: Logs estruturados e tracing distribuído
3. **Proatividade**: Dashboards para identificar problemas antes que afetem usuários
4. **Compliance**: Métricas de conformidade e auditoria automática
5. **Escalabilidade**: Base sólida para monitoramento em produção