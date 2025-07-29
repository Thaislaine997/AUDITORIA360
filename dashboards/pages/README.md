# dashboards/pages/

Este diretório contém todas as páginas visuais do sistema, implementadas em Streamlit.

## Estrutura Recomendada

- Cada arquivo representa uma página/tela do sistema.
- Use nomes claros e temáticos: `home.py`, `checklist.py`, `comunicados.py`, `demandas.py`, etc.
- Centralize apenas a lógica de exibição e interação do usuário.
- Para componentes reutilizáveis, crie a pasta `dashboards/components/`.
- Para consumir APIs backend, utilize `dashboards/api_client.py`.

## Exemplo de página

```python
# dashboards/pages/demandas.py
import streamlit as st
from dashboards.api_client import get_tickets

st.title("Portal de Demandas")
tickets = get_tickets()
st.table(tickets)
```
