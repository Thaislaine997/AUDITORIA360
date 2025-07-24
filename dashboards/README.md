# dashboards/

Aplicação Streamlit para visualização de dados, filtros, gráficos e exportação.

## Estrutura
- `app.py`: inicialização do dashboard
- `pages/`: páginas/telas do sistema
- `components/`: componentes visuais reutilizáveis
- `api_client.py`: cliente para consumir APIs backend
- `assets/`: imagens, CSS, etc

## Recomendações
- Centralize lógica visual nas páginas
- Use componentes para evitar duplicação
- Consuma APIs backend via `api_client.py`
