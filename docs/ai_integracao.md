# Integração e Evolução de Modelos de IA (Vertex AI e Gemini)

## Centralização das Chamadas de IA

As chamadas para classificação de cláusulas trabalhistas agora são centralizadas no módulo `src/ai_utils.py`.

### Como Usar

```python
from src.ai_utils import classificar_clausula

texto = "Cláusula exemplo ..."
resultado = classificar_clausula(texto)  # Usa o provedor padrão (config ou env)
resultado_vertex = classificar_clausula(texto, provider="vertex")
resultado_gemini = classificar_clausula(texto, provider="gemini")
```

- O provedor padrão é definido pela variável de ambiente `AI_PROVIDER` ("vertex" ou "gemini").
- Para forçar um provedor, passe o parâmetro `provider`.

### Como Adicionar/Trocar Modelos

1. Implemente a função de chamada do novo modelo (ex: `prever_com_novo_modelo`).
2. Importe e adicione um novo bloco `elif` em `classificar_clausula`.
3. Atualize a documentação e testes.

### Exemplo de Configuração

No `.env` ou nas variáveis de ambiente do deploy:

```env
AI_PROVIDER=gemini
```

---

Para detalhes de cada provedor, consulte:

- `src/vertex_utils.py` para Vertex AI
- `src/gemini_utils.py` para Gemini
- `src/ai_utils.py` para centralização
