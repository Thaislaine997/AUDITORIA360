# Guia Técnico para Desenvolvedores - AUDITORIA360 White-Label

## 1. Endpoints protegidos por client_id

- Sempre utilize o parâmetro/filtro `client_id` em todas as queries e endpoints que retornam dados sensíveis.
- Exemplo FastAPI:

```python
@app.get("/api/v1/auditorias/")
def listar_auditorias(client_id: str = Depends(get_client_id_from_request)):
    # Use client_id para filtrar dados no BigQuery
    ...
```

- Nunca retorne dados de outro cliente, mesmo que o usuário tente manipular parâmetros.

## 2. Evolução do fluxo de autenticação

- O login padrão usa `streamlit_authenticator` e reCAPTCHA customizado.
- Para SSO/OAuth, centralize a lógica em um módulo (ex: `auth_utils.py`) e injete o usuário autenticado no contexto do painel/backend.
- Sempre vincule o usuário ao seu `client_id`.

## 3. Integração com IA (Vertex AI, Gemini, etc)

- Centralize as chamadas de IA em um utilitário (ex: `ai_utils.py`).
- Use a configuração dinâmica do cliente para escolher o provedor/modelo:

```python
if config["AI_PROVIDER"] == "vertex":
    ... # Chamada Vertex
elif config["AI_PROVIDER"] == "gemini":
    ... # Chamada Gemini
```

- Documente como adicionar novos modelos.

## 4. Testes automatizados

- Todos os novos endpoints e fluxos devem ter testes pytest.
- Use mocks para dependências externas (BigQuery, IA, e-mail, etc).
- Exemplo de teste para isolamento multi-cliente:

```python
def test_listar_empresas_isolamento(...):
    ...
```

## 5. Boas práticas

- Nunca exponha chaves ou segredos em logs ou respostas de API.
- Use variáveis de ambiente para segredos sensíveis.
- Sempre revise o checklist de QA e deploy antes de liberar para produção.

---

> Consulte também os arquivos `onboarding_white_label.md`, `qa_checklist.md` e `deploy_checklist.md` para garantir qualidade e segurança no ciclo de vida do projeto.
