# 🧠 Assistente de Desenvolvimento IA - AUDITORIA360

## Visão Geral

O **Assistente de Desenvolvimento IA** é uma funcionalidade revolucionária que implementa uma "IA para ajudar a construir a IA" no projeto AUDITORIA360. Este assistente é treinado especificamente no código-fonte do projeto e pode responder perguntas, sugerir implementações e ajudar com debugging.

## 🏗️ Arquitetura

```
ia_desenvolvimento/
├── __init__.py
├── cerebro.py              # Cérebro da IA (LangChain + OpenAI)
└── README.md              # Esta documentação

src/api/routers/
└── dev_assistant.py       # API endpoints

src/frontend/src/pages/
└── DevAssistantPage.tsx   # Interface React
```

## 🚀 Funcionalidades

### Backend (Python)
- **Cérebro IA**: Classe `CerebroAuditoria360` que usa LangChain + OpenAI
- **Treinamento Automático**: Lê o arquivo `lista_arquivos.txt` e treina nos arquivos do projeto
- **Base Vetorial**: Usa ChromaDB para busca semântica no código
- **API RESTful**: Endpoints para query, status e retreinamento

### Frontend (React + TypeScript)
- **Interface Chat**: Conversa natural com a IA
- **Status em Tempo Real**: Mostra status da IA e arquivos processados
- **Fontes Citadas**: Exibe quais arquivos foram consultados para cada resposta
- **Retreinamento**: Botão para retreinar a IA com código atualizado

## 📡 Endpoints da API

### `GET /api/v1/dev-assistant/status`
Retorna o status atual do assistente:
```json
{
  "database_exists": true,
  "retrieval_ready": true,
  "files_processed": 127,
  "last_training": 1684567890,
  "message": "✅ Assistente ativo com 127 arquivos processados"
}
```

### `POST /api/v1/dev-assistant/query`
Faz uma pergunta para o assistente:
```json
// Request
{
  "pergunta": "Como funciona a autenticação em auth.py?"
}

// Response
{
  "resposta": "O sistema de autenticação usa JWT tokens...",
  "status": "success",
  "timestamp": 1684567890,
  "sources": [
    {"file": "src/api/routers/auth.py", "type": ".py"}
  ]
}
```

### `POST /api/v1/dev-assistant/retrain`
Retreina a IA com os arquivos atuais:
```json
{
  "message": "✅ Retreinamento concluído com sucesso!",
  "files_processed": 127,
  "retrieval_ready": true
}
```

### `GET /api/v1/dev-assistant/health`
Health check básico:
```json
{
  "status": "healthy",
  "service": "AI Development Assistant",
  "version": "1.0.0"
}
```

## ⚙️ Configuração

### 1. Configurar OpenAI API Key
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 2. Instalar Dependências
As dependências necessárias já estão no `requirements.txt`:
- `langchain`
- `langchain-openai`
- `langchain-community`
- `openai`
- `chromadb` (instalado automaticamente)

### 3. Inicializar o Sistema
O sistema inicializa automaticamente quando chamado pela primeira vez. Ele:
1. Lê o arquivo `lista_arquivos.txt`
2. Processa todos os arquivos de código
3. Cria uma base de dados vetorial
4. Fica pronto para responder perguntas

## 🎯 Como Usar

### Via API (cURL)
```bash
# Verificar status
curl -X GET "http://localhost:8000/api/v1/dev-assistant/status"

# Fazer pergunta
curl -X POST "http://localhost:8000/api/v1/dev-assistant/query" \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Como funciona a estrutura de routers?"}'

# Retreinar
curl -X POST "http://localhost:8000/api/v1/dev-assistant/retrain"
```

### Via Interface Web
1. Acesse a página `DevAssistantPage.tsx` no frontend
2. Veja o status do sistema no painel lateral
3. Digite perguntas na área de chat
4. Veja as respostas com fontes citadas

### Exemplos de Perguntas
- "Como funciona a autenticação em auth.py?"
- "Que APIs existem para relatórios?"
- "Como está organizada a estrutura de routers?"
- "Como resolver erros de CORS no frontend?"
- "Explique o sistema de notificações"
- "Como implementar um novo endpoint?"

## 🧪 Demo

Execute o script de demonstração:
```bash
python demo_dev_assistant.py
```

## 🔧 Desenvolvimento

### Arquivos Importantes
- `ia_desenvolvimento/cerebro.py` - Lógica principal da IA
- `src/api/routers/dev_assistant.py` - Endpoints da API
- `src/frontend/src/pages/DevAssistantPage.tsx` - Interface React
- `lista_arquivos.txt` - Lista de arquivos para treinamento

### Customização
- **Prompt**: Edite o `prompt_template` em `cerebro.py`
- **Filtros**: Modifique `_should_skip_file()` para filtrar tipos de arquivo
- **Modelo**: Altere o modelo OpenAI em `ChatOpenAI(model="...")`

## 🚨 Troubleshooting

### Problema: "404 Not Found" nos endpoints
- **Solução**: Verifique se o router foi importado corretamente no `api/index.py`

### Problema: Resposta "fallback" 
- **Causa**: OpenAI API key não configurada
- **Solução**: Configure `OPENAI_API_KEY`

### Problema: "Base de conhecimento não encontrada"
- **Causa**: Primeira execução ou pasta `db_ia_dev` não existe
- **Solução**: Normal, o sistema treina automaticamente

### Problema: Muitos arquivos sendo ignorados
- **Causa**: Filtros muito restritivos
- **Solução**: Ajuste `_should_skip_file()` conforme necessário

## 🎉 Resultado Final

Você agora tem seu próprio "meta-cérebro" - uma IA que conhece todo o seu código e pode:
- Responder perguntas específicas sobre implementação
- Sugerir boas práticas baseadas no código existente  
- Ajudar com debugging e troubleshooting
- Acelerar o desenvolvimento mantendo consistência
- Atuar como documentação viva do projeto

**É literalmente uma IA para ajudar a construir a IA!** 🤖✨