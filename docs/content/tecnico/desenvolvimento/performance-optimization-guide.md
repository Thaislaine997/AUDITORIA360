# 🚀 Performance Optimization Guide - AUDITORIA360

## Visão Geral

Este guia fornece estratégias abrangentes para otimização de desempenho do sistema AUDITORIA360, incluindo análise de gargalos, otimização de consultas e implementação de cache.

---

## 📊 Análise de Gargalos

### 1. Profiling de Funções

Use o sistema de profiling integrado para identificar funções lentas:

```python
from src.utils.performance import profile, profiler

# Decorator para profiling automático
@profile(include_params=True)
def minha_funcao_lenta(dados):
    # Sua lógica aqui
    return processo_dados(dados)

# Verificar gargalos
bottlenecks = profiler.get_bottlenecks(hours=24)
for bottleneck in bottlenecks:
    print(f"Função: {bottleneck['function_name']}")
    print(f"Severidade: {bottleneck['severity']}/100")
    print(f"Recomendações: {bottleneck['recommendations']}")
```

### 2. Monitoramento de Sistema

```python
from src.utils.monitoring import MonitoringSystem

monitoring = MonitoringSystem()
monitoring.start()

# Métricas disponíveis automaticamente:
# - CPU usage
# - Memory usage
# - Disk usage
# - Network I/O
```

---

## 🗄️ Otimização de Banco de Dados

### PostgreSQL (Neon) - Melhores Práticas

#### 1. Otimização de Queries

```python
from src.utils.performance import DatabaseOptimizer

optimizer = DatabaseOptimizer()

# Analisar query
query = "SELECT * FROM auditorias WHERE empresa_id = %s"
optimizations = optimizer.optimize_postgresql_query(query)

print("Sugestões:")
for suggestion in optimizations['suggestions']:
    print(f"- {suggestion}")
```

#### 2. Índices Recomendados

```sql
-- Para consultas frequentes de auditoria
CREATE INDEX CONCURRENTLY idx_auditorias_empresa_data
ON auditorias(empresa_id, data_auditoria);

-- Para filtros por status
CREATE INDEX CONCURRENTLY idx_auditorias_status
ON auditorias(status) WHERE status IN ('pendente', 'em_andamento');

-- Para pesquisas de texto
CREATE INDEX CONCURRENTLY idx_cct_texto_busca
ON cct USING gin(to_tsvector('portuguese', texto_cct));
```

#### 3. Query Profiling

```python
@profile_database_query("buscar_auditorias_empresa")
def buscar_auditorias_empresa(empresa_id):
    with optimizer.profile_query("auditorias_por_empresa"):
        # Sua query aqui
        return db.execute(query, empresa_id)
```

### DuckDB - Otimização para Analytics

#### 1. Formato de Dados Otimizado

```python
# Converter CSV para Parquet para melhor performance
import duckdb

conn = duckdb.connect()

# Exportar para Parquet
conn.execute("""
    COPY (SELECT * FROM read_csv('dados.csv'))
    TO 'dados_otimizados.parquet' (FORMAT PARQUET)
""")

# Usar Parquet nas consultas
conn.execute("SELECT * FROM read_parquet('dados_otimizados.parquet')")
```

#### 2. Otimização de Queries Analytics

```python
# Projeção de colunas
query_otimizada = """
SELECT
    empresa_id,
    SUM(valor_auditoria) as total,
    COUNT(*) as quantidade
FROM read_parquet('auditorias.parquet')
WHERE data_auditoria >= '2024-01-01'
GROUP BY empresa_id
"""

# Análise da query
optimizations = optimizer.optimize_duckdb_query(query_otimizada)
```

---

## 🚀 Sistema de Cache

### 1. Cache de Função

```python
from src.utils.performance import cached

# Cache com TTL de 1 hora
@cached(ttl_seconds=3600)
def buscar_parametros_legais(ano):
    # Operação custosa
    return consultar_base_legal(ano)

# Cache customizado por chave
@cached(ttl_seconds=1800, key_func=lambda empresa_id, tipo: f"cct_{empresa_id}_{tipo}")
def buscar_cct_empresa(empresa_id, tipo):
    return consultar_cct(empresa_id, tipo)
```

### 2. Cache Manager

```python
from src.utils.performance import cache

# Uso manual do cache
def processo_complexo(parametros):
    cache_key = f"resultado_{hash(str(parametros))}"

    resultado = cache.get(cache_key)
    if resultado is not None:
        return resultado

    # Processar dados
    resultado = realizar_calculo_complexo(parametros)

    # Cachear resultado
    cache.set(cache_key, resultado)
    return resultado

# Estatísticas do cache
stats = cache.stats()
print(f"Cache hit rate: {stats['hit_rate']:.2%}")
print(f"Memory usage: {stats['memory_usage_mb']:.2f}MB")
```

---

## ⚡ Otimizações Específicas do AUDITORIA360

### 1. Processamento de OCR

```python
@profile(include_params=True)
def processar_documento_ocr(documento_path):
    # Cache de resultados OCR por hash do arquivo
    file_hash = calcular_hash_arquivo(documento_path)

    @cached(ttl_seconds=86400, key_func=lambda _: f"ocr_{file_hash}")
    def extrair_texto_cached():
        return paddleocr_extrair_texto(documento_path)

    return extrair_texto_cached()
```

### 2. Cálculos de Folha de Pagamento

```python
@profile
@cached(ttl_seconds=3600)
def calcular_folha_pagamento(empresa_id, mes_ano):
    # Cache por empresa e período
    with optimizer.profile_query("folha_calculo"):
        funcionarios = buscar_funcionarios(empresa_id)
        parametros = buscar_parametros_legais(mes_ano)

        resultados = []
        for funcionario in funcionarios:
            calculo = processar_calculo_funcionario(funcionario, parametros)
            resultados.append(calculo)

        return resultados
```

### 3. Análise de CCT

```python
@profile
def comparar_cct_empresas(empresa_ids):
    # Paralelizar comparações
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for empresa_id in empresa_ids:
            future = executor.submit(buscar_cct_empresa, empresa_id)
            futures.append((empresa_id, future))

        resultados = {}
        for empresa_id, future in futures:
            resultados[empresa_id] = future.result()

    return analisar_diferencas_cct(resultados)
```

---

## 📈 Monitoramento de Performance

### 1. Métricas Automáticas

O sistema coleta automaticamente:

- **Tempo de execução** de funções críticas
- **Uso de memória** por operação
- **Queries lentas** (> 1 segundo)
- **Operações com alto uso de CPU**

### 2. Alertas de Performance

```python
# Configurar alertas automáticos
monitoring.alert_manager.add_alert_rule(
    metric_name="function_execution_time",
    threshold=5.0,  # 5 segundos
    condition="gt",
    severity=AlertSeverity.HIGH,
    title="Função Lenta Detectada",
    description="Função executando acima de 5 segundos"
)
```

### 3. Dashboard de Performance

Acesse `/api/v1/monitoring/dashboard` para visualizar:

- Gráficos de tempo de resposta
- Top 10 funções mais lentas
- Uso de recursos do sistema
- Status de cache

---

## 🛠️ Ferramentas de Profiling

### 1. Profiling Manual

```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()

    # Sua função aqui
    resultado = funcao_para_profile()

    profiler.disable()

    # Analisar resultados
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 funções

    return resultado
```

### 2. Memory Profiling

```python
from memory_profiler import profile

@profile
def funcao_memory_intensive():
    # Sua lógica aqui
    dados = carregar_dados_grandes()
    resultado = processar_dados(dados)
    return resultado
```

---

## 📋 Checklist de Otimização

### ✅ Banco de Dados

- [ ] Queries com índices apropriados
- [ ] Evitar SELECT \* desnecessário
- [ ] Paginação implementada
- [ ] Connection pooling configurado
- [ ] Queries parametrizadas (evitar SQL injection)

### ✅ Cache

- [ ] Cache implementado para operações custosas
- [ ] TTL apropriado configurado
- [ ] Cache invalidation strategy definida
- [ ] Monitoring de hit rate

### ✅ Código

- [ ] Profiling em funções críticas
- [ ] Algoritmos otimizados
- [ ] Evitar loops desnecessários
- [ ] Lazy loading implementado
- [ ] Processamento assíncrono onde apropriado

### ✅ Infraestrutura

- [ ] Monitoramento de recursos ativo
- [ ] Alertas configurados
- [ ] Logs de performance coletados
- [ ] Métricas sendo acompanhadas

---

## 🎯 Metas de Performance

| Métrica              | Meta    | Atual | Status |
| -------------------- | ------- | ----- | ------ |
| Tempo resposta API   | < 200ms | -     | ⏳     |
| Query DB tempo médio | < 100ms | -     | ⏳     |
| Cache hit rate       | > 80%   | -     | ⏳     |
| Uso CPU              | < 70%   | -     | ⏳     |
| Uso memória          | < 80%   | -     | ⏳     |

---

## 📞 Suporte

Para dúvidas sobre otimização de performance:

1. Verifique os logs de monitoring
2. Analise os bottlenecks reportados
3. Consulte a documentação técnica
4. Entre em contato com a equipe técnica

---

_Última atualização: 2025-01-28_
_Versão: 1.0.0_
