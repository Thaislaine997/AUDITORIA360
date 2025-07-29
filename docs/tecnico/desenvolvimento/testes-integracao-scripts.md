# Testes de Integração para Scripts Auxiliares

Este documento descreve os testes de integração implementados para validar os scripts auxiliares do sistema AUDITORIA360.

## Visão Geral

Os testes de integração foram criados para garantir que todos os scripts auxiliares funcionem corretamente dentro do contexto do sistema, validando suas integrações com APIs, bancos de dados, sistemas de monitoramento e outras dependências.

## Scripts Testados

### 1. Health Check (`health_check.py`)
**Arquivo de teste**: `tests/integration/test_health_check_script.py`

**Funcionalidades testadas**:
- Inicialização do HealthChecker
- Verificação de saúde da API, banco de dados e storage
- Execução de todas as verificações de saúde
- Medição de tempos de resposta
- Tratamento de erros
- Execução concorrente de verificações
- Integração com o sistema

**Cobertura**: 11 testes implementados

### 2. ETL/ELT (`etl_elt.py`)
**Arquivo de teste**: `tests/integration/test_etl_script.py`

**Funcionalidades testadas**:
- Configuração do cliente BigQuery
- Extração de dados da folha de pagamento
- Transformação e engenharia de features
- Anonimização de dados sensíveis
- Carregamento do dataset de treinamento
- Tratamento de variáveis de ambiente
- Workflow completo de ETL/ELT
- Configurações flexíveis de projeto/dataset

**Cobertura**: 15 testes implementados

### 3. Monitoramento (`monitoramento.py`)
**Arquivo de teste**: `tests/integration/test_monitoring_script.py`

**Funcionalidades testadas**:
- Verificação de serviços HTTP
- Monitoramento de banco de dados e storage
- Verificação de métricas de performance
- Sistema de alertas
- Execução da função principal de monitoramento
- Configuração de serviços
- Medição de tempos de resposta
- Resiliência a erros
- Execução concorrente
- Compatibilidade com CLI

**Cobertura**: 16 testes implementados

### 4. Scripts Auxiliares Diversos
**Arquivo de teste**: `tests/integration/test_auxiliary_scripts.py`

**Scripts cobertos**:
- `deploy_production.py` - Deploy em produção
- `validate_config.py` - Validação de configurações
- `api_healthcheck.py` - Verificação de saúde da API
- `onboarding_cliente.py` - Onboarding de clientes
- `setup_monitoring.py` - Configuração de monitoramento
- `setup_advanced_monitoring.py` - Monitoramento avançado
- Scripts de geração de hash
- Scripts de backup e restore
- Scripts de exportação CSV

**Verificações realizadas**:
- Disponibilidade e estrutura dos scripts
- Sintaxe válida de Python
- Documentação adequada
- Tratamento de erros
- Integração com CI/CD
- Compatibilidade com diferentes ambientes

**Cobertura**: 17 testes implementados

## Execução dos Testes

### Executar todos os testes de integração de scripts auxiliares:
```bash
python -m pytest tests/integration/test_health_check_script.py tests/integration/test_etl_script.py tests/integration/test_monitoring_script.py tests/integration/test_auxiliary_scripts.py -v
```

### Executar testes específicos:
```bash
# Apenas testes de health check
python -m pytest tests/integration/test_health_check_script.py -v

# Apenas testes de ETL
python -m pytest tests/integration/test_etl_script.py -v

# Apenas testes de monitoramento
python -m pytest tests/integration/test_monitoring_script.py -v

# Apenas testes de scripts auxiliares
python -m pytest tests/integration/test_auxiliary_scripts.py -v
```

### Executar com cobertura:
```bash
python -m pytest tests/integration/test_*_script*.py --cov=scripts --cov-report=html
```

## Integração com CI/CD

Os testes de integração estão integrados ao pipeline de CI/CD através do GitHub Actions:

1. **Workflow principal**: `.github/workflows/ci-cd.yml`
   - Executa testes de integração de scripts auxiliares
   - Inclui cobertura de código para o diretório `scripts`
   - Verifica compatibilidade com diferentes versões do Python

2. **Etapas do CI/CD**:
   - Instalação de dependências
   - Execução de linting
   - Execução de testes unitários
   - **Execução de testes de integração de scripts auxiliares** (novo)
   - Relatórios de cobertura
   - Deploy automático

## Estrutura dos Testes

### Padrão de organização:
```
tests/integration/
├── test_health_check_script.py     # Testes do health check
├── test_etl_script.py              # Testes do ETL/ELT
├── test_monitoring_script.py       # Testes do monitoramento
└── test_auxiliary_scripts.py       # Testes dos scripts auxiliares
```

### Convenções:
- Classes de teste organizadas por funcionalidade
- Uso de mocks para dependências externas
- Testes parametrizados para diferentes cenários
- Verificação de tratamento de erros
- Validação de integração com o sistema

## Mocks e Dependências

### Dependências mockadas:
- **BigQuery**: Cliente e operações de query/load
- **HTTP requests**: Respostas de APIs e serviços
- **Sistema de arquivos**: Leitura/escrita de arquivos
- **Variáveis de ambiente**: Configurações de teste
- **Funções assíncronas**: Simulação de operações I/O

### Bibliotecas utilizadas:
- `pytest` - Framework de testes
- `pytest-asyncio` - Suporte a testes assíncronos
- `unittest.mock` - Sistema de mocks
- `aiohttp` - Cliente HTTP assíncrono
- `requests` - Cliente HTTP síncrono

## Métricas e Cobertura

### Estatísticas atuais:
- **Total de testes**: 59 testes de integração para scripts auxiliares
- **Scripts cobertos**: 15+ scripts auxiliares
- **Cobertura funcional**: 
  - Health checking: 100%
  - ETL/ELT: 85% (algumas funcionalidades específicas do BigQuery)
  - Monitoramento: 90%
  - Scripts auxiliares: 80%

### Relatórios:
- Cobertura HTML gerada automaticamente
- Relatórios XML para integração com ferramentas externas
- Logs detalhados de execução no CI/CD

## Validação Contínua

### Verificações automáticas:
1. **Sintaxe**: Todos os scripts Python têm sintaxe válida
2. **Estrutura**: Scripts seguem padrões de organização
3. **Documentação**: Presença de docstrings e comentários
4. **Tratamento de erros**: Verificação de exception handling
5. **Configuração**: Scripts respeitam variáveis de ambiente
6. **Integração**: Compatibilidade com sistema principal

### Execução em paralelo:
- Testes podem ser executados simultaneamente com outros PRs
- Não há dependências diretas entre diferentes conjuntos de testes
- Execução isolada garante não interferência

## Resolução de Problemas

### Problemas comuns:

1. **Dependências faltando**:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov pytest-asyncio
   ```

2. **Erro de importação de scripts**:
   - Verificar se o diretório `scripts/python` está no PATH
   - Scripts são importados dinamicamente nos testes

3. **Testes de conectividade falhando**:
   - Normal em ambiente de teste sem serviços rodando
   - Testes verificam o comportamento de falha

4. **Timeout em testes assíncronos**:
   - Ajustar timeouts conforme necessário
   - Verificar configuração do event loop

### Debug:
```bash
# Executar com saída detalhada
python -m pytest tests/integration/test_health_check_script.py -v -s

# Executar teste específico
python -m pytest tests/integration/test_health_check_script.py::TestHealthCheckIntegration::test_run_all_checks -v -s
```

## Próximos Passos

### Melhorias planejadas:
1. **Cobertura adicional**: Incluir mais scripts auxiliares conforme são criados
2. **Testes de performance**: Adicionar benchmarks para scripts críticos
3. **Testes de integração real**: Incluir testes com serviços reais em ambiente de staging
4. **Monitoramento de qualidade**: Alertas automáticos para degradação de testes

### Expansão:
- Adicionar testes para novos scripts conforme são desenvolvidos
- Integrar com ferramentas de qualidade de código
- Implementar testes de regressão automatizados