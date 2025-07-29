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

## 6. Checklist Inteligente de Fechamento da Folha (NOVO)

- O backend expõe endpoints REST para:
  - Listar folhas processadas disponíveis para checklist (`/clientes/{id_cliente}/folhas-processadas/disponiveis-para-checklist`)
  - CRUD de itens do checklist, geração dinâmica, dicas de IA (Gemini) e fechamento da folha
- O frontend (Streamlit) consome esses endpoints e exibe:
  - Login, seleção de cliente/folha, checklist dinâmico, status/notas, dicas de IA, alerta de bloqueadores e fechamento
- O checklist é salvo no BigQuery conforme schema em `docs/bigquery_schema.sql`
- Veja exemplos de integração em `src/checklist_page.py`, `src/controllers/checklist_folha_controller.py` e `src/routes/checklist_folha_routes.py`
- Para adicionar novos itens dinâmicos ou regras de checklist, edite o controller e o schema correspondente
- O fluxo completo está documentado no manual do usuário

## 7. Exemplos de Payloads e Respostas de API do Checklist

### Listar folhas processadas disponíveis para checklist

**GET** `/api/v1/clientes/{id_cliente}/folhas-processadas/disponiveis-para-checklist`

**Resposta:**

```json
[
  {
    "id_folha_processada": "folha2025-05-01",
    "descricao": "Folha Maio/2025",
    "status": "EM_ABERTO"
  },
  {
    "id_folha_processada": "folha2025-04-01",
    "descricao": "Folha Abril/2025",
    "status": "EM_ABERTO"
  }
]
```

### Buscar checklist de uma folha

**GET** `/api/v1/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist`

**Resposta:**

```json
[
  {
    "id_item_checklist": "item1",
    "descricao": "Conferir INSS",
    "categoria": "Tributos",
    "status": "PENDENTE",
    "criticidade": "BLOQUEADOR",
    "notas": "",
    "responsavel": "Maria"
  },
  {
    "id_item_checklist": "item2",
    "descricao": "Validar FGTS",
    "categoria": "Tributos",
    "status": "CONCLUIDO",
    "criticidade": "ALTA",
    "notas": "OK",
    "responsavel": "João"
  }
]
```

### Atualizar item do checklist

**PUT** `/api/v1/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist/{id_item_checklist}`

**Payload:**

```json
{
  "status": "CONCLUIDO",
  "notas": "Conferido e validado."
}
```

**Resposta:**

```json
{
  "id_item_checklist": "item1",
  "descricao": "Conferir INSS",
  "categoria": "Tributos",
  "status": "CONCLUIDO",
  "criticidade": "BLOQUEADOR",
  "notas": "Conferido e validado.",
  "responsavel": "Maria"
}
```

### Obter dica de IA para um item

**GET** `/api/v1/clientes/{id_cliente}/folhas/{id_folha_processada}/checklist/dica-ia?id_item_checklist=item1&descricao_item=Conferir%20INSS`

**Resposta:**

```json
{
  "dica": "Verifique se o valor do INSS está compatível com a tabela vigente e se não há descontos duplicados."
}
```

### Marcar folha como fechada

**POST** `/api/v1/clientes/{id_cliente}/folhas/{id_folha_processada}/marcar-fechada`

**Resposta:**

```json
{
  "status_folha": "FECHADA_CLIENTE",
  "message": "Folha marcada como fechada com sucesso."
}
```

---

## 7. Padrões de Scripts

- Todos os scripts Shell (.sh) e PowerShell (.ps1) devem seguir os padrões definidos no [Guia de Padronização de Scripts](script-standardization-guide.md).
- Use os templates disponíveis em `templates/scripts/` para novos scripts.
- Scripts devem incluir:
  - Tratamento adequado de erros
  - Funções de logging padronizadas
  - Validação de pré-requisitos
  - Documentação completa (--help)
  - Modo dry-run quando aplicável

```bash
# Exemplo de uso dos scripts padronizados
./scripts/git_update_all.sh --help
./scripts/deploy_vercel.sh --production --verbose
./deploy/cloudrun_deploy.sh --project-id my-project --dry-run
```

---

> Consulte também os arquivos `script-standardization-guide.md`, `onboarding_white_label.md`, `qa_checklist.md` e `deploy_checklist.md` para garantir qualidade e segurança no ciclo de vida do projeto.
