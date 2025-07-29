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
│   ├── test_api_*.py          # Testes de APIs
│   ├── test_automation_*.py   # Testes de automação
│   └── test_*_integration.py  # Outros testes de integração
├── e2e/                       # Testes end-to-end
│   ├── __init__.py
│   ├── e2e_config.py          # Configurações para testes E2E
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

- **APIs**: Endpoints e rotas da aplicação
- **Automação**: Processos automatizados completos
- **Integrações Externas**: Serviços externos como BigQuery, GCP
- **Fluxos Completos**: Processos de negócio end-to-end

**Exemplos:**
- `test_api_*.py` - Testes de APIs REST
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

1. **De `e2e_tests/` para `tests/e2e/`:**
   - `test_e2e_playwright.py`
   - `e2e_config.py`
   - Arquivos HTML de teste

2. **De `/automation/` para `tests/integration/`:**
   - `test_robot_esocial.py`

3. **Da raiz para `tests/performance/`:**
   - `test_performance.py`

4. **Organização dentro de `tests/`:**
   - Separação entre `unit/` e `integration/` baseada na análise do conteúdo
   - Manutenção das subpastas `ingestion/` e `ml/` em `unit/`

### Atualizações de Configuração

- **conftest.py**: Ajustado import do `e2e_config`
- **pytest.ini**: Adicionado `testpaths` para as novas pastas
- **__init__.py**: Criados em todas as subpastas

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
- **Testes de integração**: `test_<funcionalidade>_integration.py` ou `test_api_<endpoint>.py`
- **Testes E2E**: `test_e2e_<cenario>.py`
- **Testes de performance**: `test_performance_<aspecto>.py`

## Contribuição

Ao adicionar novos testes:

1. Identifique o tipo correto (unit/integration/e2e/performance)
2. Coloque no diretório apropriado
3. Siga os padrões de nomenclatura
4. Atualize a documentação se necessário