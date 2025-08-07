# AUDITORIA360 - Demos Directory

Este diretório contém demonstrações completas e avançadas do sistema AUDITORIA360, incluindo integrações complexas e showcases técnicos.

## 🎭 Demos Disponíveis

### 🚀 Demonstrações Principais

#### **[demo_first_stage.py](demo_first_stage.py)**
- **Propósito**: Demonstração da primeira fase de implementação
- **Funcionalidades**: Integração inicial de módulos
- **Público**: Técnico e stakeholders
- **Duração**: ~15 minutos

#### **[demo_modular_backend.py](demo_modular_backend.py)**  
- **Propósito**: Showcase da arquitetura modular do backend
- **Funcionalidades**: Demonstra como módulos trabalham juntos
- **Público**: Desenvolvedores e arquitetos
- **Duração**: ~20 minutos

#### **[demo_quantum_validation.py](demo_quantum_validation.py)**
- **Propósito**: Sistema Nervoso Descentralizado e Validação Quantum
- **Funcionalidades**: Algoritmos avançados de validação
- **Público**: Técnico especializado
- **Duração**: ~30 minutos

#### **[demo_swarm_intelligence.py](demo_swarm_intelligence.py)**
- **Propósito**: Demonstração de Inteligência de Enxame (Swarm Intelligence)
- **Funcionalidades**: Algoritmos distribuídos e coletivos
- **Público**: Pesquisadores e arquitetos de sistemas
- **Duração**: ~25 minutos

## 🎯 Cenários de Uso

### 📊 Para Apresentações Comerciais:
```bash
# Demo básico para clientes
python demos/demo_first_stage.py

# Demo técnico avançado
python demos/demo_modular_backend.py
```

### 🔬 Para Validação Técnica:
```bash
# Validação quantum (algoritmos avançados)
python demos/demo_quantum_validation.py

# Inteligência distribuída
python demos/demo_swarm_intelligence.py
```

### 📈 Para Análise de Performance:
```bash
# Executar todos os demos com relatórios
python demos/demo_first_stage.py --report
python demos/demo_modular_backend.py --benchmark
```

## 🛠️ Configuração e Setup

### Pré-requisitos:
```bash
# Dependências avançadas
pip install -r requirements-ml.txt

# Configurar ambiente de desenvolvimento
cp .env.template .env
# Configurar credenciais específicas para demos

# Verificar configuração
python scripts/validate_config.py
```

### Variáveis de Ambiente:
```bash
# Configurações específicas para demos
DEMO_MODE=true
QUANTUM_VALIDATION_ENABLED=true
SWARM_INTELLIGENCE_NODES=5
PERFORMANCE_MONITORING=true
```

## 📁 Estrutura de Arquivos

### Relatórios Gerados:
Os relatórios de execução são salvos em `artifacts/reports/`:
- `daily_YYYYMMDD_YYYYMMDD.json`
- `weekly_YYYYMMDD_YYYYMMDD.json`  
- `monthly_YYYYMMDD_YYYYMMDD.json`

### Logs e Métricas:
- Logs detalhados em `/logs/demos/`
- Métricas de performance coletadas automaticamente
- Dashboards disponíveis no Grafana (se configurado)

## 🔍 Diferença entre Demos e Examples

### 🎭 Demos (este diretório):
- **Complexidade**: Alta - demonstrações completas
- **Duração**: 15-30 minutos cada
- **Público**: Stakeholders, clientes, arquitetos
- **Funcionalidades**: Múltiplas integrações e casos de uso
- **Relatórios**: Geração automática de métricas

### 📁 Examples (../examples/):
- **Complexidade**: Baixa - exemplos específicos
- **Duração**: 2-5 minutos cada
- **Público**: Desenvolvedores aprendendo as APIs
- **Funcionalidades**: Uma funcionalidade por exemplo
- **Relatórios**: Mínimos ou nenhum

## 📊 Monitoramento e Métricas

### Métricas Coletadas:
- **Performance**: Tempo de execução, uso de memória
- **Validação**: Taxa de sucesso, erros encontrados
- **Inteligência**: Eficiência dos algoritmos, convergência
- **Sistema**: Load, throughput, latência

### Dashboards Disponíveis:
```bash
# Iniciar monitoramento
docker-compose -f docker-compose.monitoring.yml up -d

# Acessar dashboards
# Grafana: http://localhost:3000
# Prometheus: http://localhost:9090
```

## 🚀 Execução Avançada

### Modo Batch:
```bash
# Executar todos os demos sequencialmente
python scripts/run_all_demos.py

# Com relatório consolidado
python scripts/run_all_demos.py --generate-report
```

### Modo CI/CD:
```bash
# Validação automática (usado em pipelines)
python demos/demo_quantum_validation.py --ci-mode
```

### Modo Debug:
```bash
# Com logs detalhados
python demos/demo_swarm_intelligence.py --verbose --debug
```

## 📋 Checklist de Execução

Antes de executar demos importantes:

- [ ] Verificar configuração do ambiente
- [ ] Confirmar dependências instaladas
- [ ] Validar conectividade com serviços externos
- [ ] Verificar espaço em disco para relatórios
- [ ] Configurar monitoramento (se necessário)

```bash
# Checklist automático
python scripts/validate_demo_environment.py
```

## 🆘 Troubleshooting

### Problemas Comuns:

**Demo não inicia:**
```bash
# Verificar dependências
pip install -r requirements-ml.txt

# Validar configuração
python scripts/validate_config.py
```

**Performance baixa:**
```bash
# Verificar recursos do sistema
python scripts/system_health_check.py

# Otimizar configuração
python scripts/optimize_demo_config.py
```

**Erros de validação:**
```bash
# Logs detalhados
tail -f logs/demos/quantum_validation.log

# Executar diagnóstico
python scripts/diagnose_quantum_validation.py
```

## 🔗 Links Relacionados

- **[Examples](../examples/)** - Exemplos simples de APIs
- **[Tests](../tests/)** - Testes automatizados 
- **[Scripts](../scripts/)** - Utilitários e automação
- **[Monitoring](../monitoring/)** - Dashboards e métricas
- **[Documentation](../docs/)** - Documentação completa

---

**Mantido por**: AUDITORIA360 Team  
**Última atualização**: $(date)  
**Versão**: 1.0.0