# ADR-002: Implementação de Observabilidade com ACR e ACH

## Status
Aceito

## Data
2024-02-07

## Contexto
O AUDITORIA360 está a evoluir para uma plataforma complexa com múltiplos componentes (Frontend React, Backend Python, APIs, Base de Dados). Para garantir confiabilidade, performance e capacidade de diagnóstico, necessitamos de um sistema de observabilidade abrangente.

## Problema
1. **Falta de Visibilidade**: Dificuldade em diagnosticar problemas em produção
2. **Performance Unknowns**: Sem métricas de performance de ponta-a-ponta  
3. **Debug Complexo**: Fluxos distribuídos difíceis de rastrear
4. **Saúde do Sistema**: Ausência de monitorização holística da saúde da aplicação

## Decisão
Implementaremos um sistema duplo de observabilidade:

### ACR - Agente de Rastreamento Cinético
**Propósito**: Rastreamento de fluxo de execução e tracing distribuído

**Componentes**:
- OpenTelemetry no Frontend (React) e Backend (Python)
- Jaeger como sistema de tracing distribuído
- Instrumentação automática de HTTP requests, componentes React, e APIs
- Geração automática de diagramas de fluxo usando Graphviz

**Capacidades**:
- Rastreamento de user journeys completos
- Identificação de gargalos de performance
- Visualização de fluxos de execução
- Correlação entre Frontend e Backend

### ACH - Agente de Consciência Holística  
**Propósito**: Análise holística de saúde do sistema e censo genómico

**Componentes**:
- Censo Genómico: Classificação e análise de todos os ficheiros do repositório
- Testes de Pulso Vital: Verificações de saúde por componente
- Simulação com Alma: Testes com dados realistas
- Diagrama de Vitalidade Sistémica: Dashboard interativo de saúde

**Capacidades**:
- Análise automatizada de saúde do código
- Detecção precoce de problemas arquiteturais
- Relatórios de vitalidade do sistema
- Monitorização de métricas de qualidade

## Arquitectura

### Stack Tecnológico
- **Tracing**: OpenTelemetry + Jaeger
- **Metrics**: Prometheus + Grafana (já existente)
- **Logs**: Loki + Promtail (já existente)
- **Análise**: Python scripts para ACH
- **Visualização**: D3.js para diagramas interativos

### Integração CI/CD
- ACR executa durante testes E2E para capturar traces
- ACH executa diariamente (3:00 AM) para análise de saúde
- Artefactos gerados disponibilizados no portal de desenvolvimento
- Alertas automáticos para degradação de métricas

### Estrutura de Dados
```
artifacts/
├── acr/                    # Artefactos do ACR
│   ├── traces_*.json      # Traces capturados  
│   ├── *_flow.dot         # Diagramas em DOT
│   └── *_flow.svg         # Diagramas visuais
└── ach/                    # Artefactos do ACH
    ├── census_data.json   # Dados do censo genómico
    ├── vitality_report.json # Relatório de vitalidade
    └── vitality_diagram.html # Dashboard interativo
```

## Consequências

### Positivas
- **Visibilidade Total**: Capacidade de observar toda a stack
- **Debug Eficiente**: Traces facilitam identificação de problemas
- **Performance Insights**: Métricas detalhadas de performance
- **Qualidade Proactiva**: Detecção precoce de problemas
- **Cultura DevOps**: Observabilidade como cidadão de primeira classe

### Negativas  
- **Overhead de Performance**: Instrumentação adiciona latência mínima
- **Complexidade**: Sistema mais complexo para manter
- **Armazenamento**: Traces e métricas requerem espaço de armazenamento
- **Curva de Aprendizagem**: Equipa precisa aprender ferramentas de observabilidade

### Riscos e Mitigações
- **Overhead Excessivo**: Sampling configurável para reduzir impacto
- **Dados Sensíveis**: Sanitização automática de dados pessoais nos traces
- **Vendor Lock-in**: OpenTelemetry garante portabilidade
- **Custos**: Implementação in-house minimiza custos externos

## Métricas de Sucesso
- **MTTR** (Mean Time To Resolution): Redução de 50% em 3 meses
- **Performance Visibility**: 95% dos endpoints com traces
- **System Health**: Score de vitalidade > 8.0/10
- **Error Detection**: 90% dos erros detectados antes dos utilizadores

## Implementação Faseada

### Fase 1: Fundação (Semana 1-2)
- Setup do Jaeger no docker-compose
- Instrumentação básica do Frontend e Backend  
- Scripts ACR e ACH funcionais

### Fase 2: Integração (Semana 3-4)
- Integração com CI/CD
- Dashboards básicos no Grafana
- Testes E2E com tracing

### Fase 3: Optimização (Semana 5-6)
- Fine-tuning de sampling rates
- Alertas automatizados
- Documentação completa

## Decisões Técnicas

### Sampling Strategy
- **Production**: 10% sampling para reduzir overhead
- **Development**: 100% sampling para debug completo
- **E2E Tests**: 100% sampling para análise de fluxos

### Retenção de Dados
- **Traces**: 7 dias (Jaeger)
- **Metrics**: 30 dias (Prometheus)
- **Health Reports**: Indefinido (arquivos estáticos)

### Segurança
- Sanitização automática de PII nos traces
- API keys mascaradas nos logs
- Access control via Grafana RBAC

## Revisão
- **Revisão Mensal**: Métricas de performance e utilização
- **Revisão Trimestral**: ROI da observabilidade
- **Revisão Anual**: Evolução tecnológica e necessidades