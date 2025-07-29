# Organização de Testes - AUDITORIA360

## Visão Geral

Este documento descreve a nova estrutura organizacional dos testes do projeto AUDITORIA360, implementada para centralizar e organizar todos os testes em um diretório dedicado com separação clara entre tipos de teste.

## Estrutura de Diretórios

A estrutura de testes foi reorganizada da seguinte forma:

```
tests/
├── __init__.py                 # Pacote principal de testes
├── conftest.py                 # Configurações globais do pytest
├── pytest.ini                 # Configuração do pytest
├── README.md                   # Documentação dos testes
├── unit/                       # Testes unitários
│   ├── __init__.py
│   ├── ingestion/             # Testes de ingestão de dados
│   ├── ml/                    # Testes de componentes ML
│   └── test_*.py              # Testes unitários diversos
├── integration/               # Testes de integração
│   ├── __init__.py
│   ├── portal_demandas/       # Testes do Portal de Demandas
│   │   ├── __init__.py
│   │   ├── test_api.py        # Testes da API do portal
│   │   └── test_api_integration.py
│   ├── mcp/                   # Testes de integração MCP
│   │   ├── __init__.py
│   │   └── test_mcp_integration_simple.py
│   ├── test_api_*.py          # Testes de APIs principais
│   ├── test_automation_*.py   # Testes de automação
│   └── test_*_integration.py  # Outros testes de integração
├── e2e/                       # Testes end-to-end
│   ├── __init__.py
│   ├── e2e_config.py          # Configurações para testes E2E
│   ├── playwright-page-*.html # Páginas de teste Playwright
│   └── test_e2e_*.py          # Testes E2E com Playwright
└── performance/               # Testes de performance
    ├── __init__.py
    └── test_performance.py    # Testes de performance
```

## Categorização dos Testes

### Testes Unitários (`tests/unit/`)

Testes que verificam o comportamento de componentes individuais de forma isolada:

- **Schemas e Modelos**: Validação de estruturas de dados
- **Utilitários**: Funções auxiliares e helpers
- **Componentes ML**: Modelos de machine learning isolados
- **Serviços**: Lógica de negócio sem dependências externas

**Exemplos:**
- `test_auth_service.py` - Testes de autenticação
- `test_gemini_utils.py` - Utilitários do Gemini
- `test_ml_components_*.py` - Componentes de ML
- `test_*_schemas.py` - Validação de schemas

### Testes de Integração (`tests/integration/`)

Testes que verificam a interação entre múltiplos componentes:

- **APIs**: Endpoints e rotas da aplicação principal
- **Portal de Demandas**: Testes específicos do portal (`portal_demandas/`)
- **Integração MCP**: Testes de Model Context Protocol (`mcp/`)
- **Automação**: Processos automatizados completos
- **Integrações Externas**: Serviços externos como BigQuery, GCP
- **Fluxos Completos**: Processos de negócio end-to-end

**Exemplos:**
- `test_api_*.py` - Testes de APIs REST principais
- `portal_demandas/test_api.py` - API do Portal de Demandas
- `mcp/test_mcp_integration_simple.py` - Integração MCP
- `test_automation_*.py` - Automação e RPA
- `test_*_integration.py` - Integrações específicas

### Testes E2E (`tests/e2e/`)

Testes que simulam o comportamento do usuário final:

- **Playwright**: Testes de interface web
- **Fluxos de Usuário**: Cenários completos de uso
- **Validação de Interface**: Componentes visuais

### Testes de Performance (`tests/performance/`)

Testes que verificam o desempenho da aplicação:

- **Carga**: Testes de volume e stress
- **Latência**: Medição de tempos de resposta
- **Recursos**: Uso de CPU, memória, etc.

## Configuração e Execução

### Pytest Configuration

O arquivo `pytest.ini` foi atualizado para trabalhar com a nova estrutura:

```ini
[pytest]
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
testpaths = unit integration e2e performance
```

**Suporte a Async/Await:**
- Testes assíncronos suportados via `pytest-asyncio`
- Use o decorador `@pytest.mark.asyncio` para testes async
- Configuração automática para testes MCP e componentes assíncronos

### Comandos de Execução

**Executar todos os testes:**
```bash
pytest tests/
```

**Executar por categoria:**
```bash
# Apenas testes unitários
pytest tests/unit/

# Apenas testes de integração
pytest tests/integration/

# Portal de Demandas especificamente
pytest tests/integration/portal_demandas/

# Integração MCP especificamente
pytest tests/integration/mcp/

# Apenas testes E2E
pytest tests/e2e/

# Apenas testes de performance
pytest tests/performance/
```

**Executar com coverage:**
```bash
pytest tests/ --cov=src --cov-report=html
```

### Makefile

O comando `make test` continua funcionando e executa todos os testes:

```bash
make test
```

## Migração Realizada

### Movimentações de Arquivos

1. **De `portal_demandas/tests/` para `tests/integration/portal_demandas/`:**
   - `test_api.py` - Testes da API do Portal de Demandas
   - `test_api_integration.py` - Testes de integração do Portal

2. **De `scripts/python/` para `tests/integration/mcp/`:**
   - `test_mcp_simple.py` → `test_mcp_integration_simple.py` (convertido para pytest)

3. **Organização dentro de `tests/`:**
   - Separação entre `unit/` e `integration/` baseada na análise do conteúdo
   - Manutenção das subpastas `ingestion/` e `ml/` em `unit/`
   - Criação de subpastas organizacionais em `integration/`:
     - `portal_demandas/` - Para testes específicos do portal
     - `mcp/` - Para testes de integração MCP

### Atualizações de Configuração

- **conftest.py**: Mantém configurações globais e mocks
- **pytest.ini**: Configurado com `testpaths` para as categorias de teste
- **__init__.py**: Criados em todas as subpastas para organização modular
- **Conversão para pytest**: Testes convertidos para usar decoradores `@pytest.mark.asyncio`

### Padronização de Scripts

- Scripts originais atualizados para referenciar a nova localização dos testes
- Mantidos links para compatibilidade com workflows existentes

## Benefícios da Reorganização

1. **Clareza**: Separação clara entre tipos de teste
2. **Manutenibilidade**: Estrutura organizada facilita manutenção
3. **Escalabilidade**: Fácil adição de novos testes por categoria
4. **CI/CD**: Possibilidade de executar categorias específicas
5. **Performance**: Execução seletiva de testes conforme necessidade

## Próximos Passos

1. **CI/CD**: Configurar pipeline para executar categorias específicas
2. **Coverage**: Implementar relatórios de cobertura por categoria
3. **Parallelização**: Otimizar execução paralela por tipo de teste
4. **Documentação**: Manter este documento atualizado com novas adições

## Padrões de Nomenclatura

- **Testes unitários**: `test_<componente>.py`
- **Testes de integração**: 
  - `test_<funcionalidade>_integration.py` 
  - `test_api_<endpoint>.py` (para APIs)
  - Organizados em subpastas por módulo (`portal_demandas/`, `mcp/`)
- **Testes E2E**: `test_e2e_<cenario>.py`
- **Testes de performance**: `test_performance_<aspecto>.py`
- **Testes assíncronos**: Usar `@pytest.mark.asyncio` para métodos async

## Contribuição

Ao adicionar novos testes:

1. Identifique o tipo correto (unit/integration/e2e/performance)
2. Coloque no diretório apropriado
3. Siga os padrões de nomenclatura
4. Atualize a documentação se necessário