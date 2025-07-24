# Portal Demandas

CRUD de tickets para gestão de demandas, etapas e prazos.

## Estrutura Inicial
- `models.py`: definição do modelo Ticket
- `api.py`: endpoints FastAPI para CRUD
- `db.py`: integração com Postgres
- `tests/`: testes unitários e integração

## Status
❌ Ausente — precisa ser implementado conforme especificação do plano.

# portal_demandas/

Microserviço FastAPI para gestão de tickets/demandas.

## Estrutura
- `models.py`: modelos Pydantic para tickets
- `db.py`: integração com banco Postgres
- `api.py`: endpoints CRUD
- `tests/`: testes automatizados

## Recomendações
- Consuma via HTTP no dashboard
- Centralize regras de negócio no backend
