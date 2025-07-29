# Testes - AUDITORIA360

Este diretório contém todos os testes do projeto AUDITORIA360, organizados por categoria para facilitar manutenção e execução.

## Estrutura de Diretórios

```
tests/
├── unit/           # Testes unitários - componentes isolados
│   ├── ingestion/  # Testes de ingestão, hash, validação, carga
│   └── ml/         # Testes de componentes ML, explainability, LLMOps
├── integration/    # Testes de integração - múltiplos componentes
├── e2e/           # Testes end-to-end - simulação de usuário
├── performance/   # Testes de performance - carga e latência
├── conftest.py    # Configurações globais do pytest
└── pytest.ini    # Configuração do pytest
```

## Execução de Testes

**Todos os testes:**

```bash
pytest tests/
# ou
make test
```

**Por categoria:**

```bash
pytest tests/unit/          # Testes unitários
pytest tests/integration/   # Testes de integração
pytest tests/e2e/          # Testes end-to-end
pytest tests/performance/  # Testes de performance
```

## Documentação Completa

Para documentação detalhada sobre a organização de testes, consulte:
`docs/tecnico/desenvolvimento/organizacao-testes.md`
