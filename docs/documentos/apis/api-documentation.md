# Documentação de APIs - AUDITORIA360

> **Redirecionamento para documentação técnica principal**

Este documento foi movido para manter a organização da estrutura de documentos.

📍 **Localização atual:** [`../../tecnico/apis/`](../../tecnico/apis/)

## Acesso Direto

Para acessar a documentação completa de APIs, navegue para:
- 🔗 **API Documentation**: [`../../tecnico/apis/api-documentation.md`](../../tecnico/apis/api-documentation.md)
- 💡 **Exemplos Práticos**: [`../../tecnico/apis/exemplos-praticos.md`](../../tecnico/apis/exemplos-praticos.md)

## Endpoints Principais

### 🔐 Autenticação
- `POST /api/v1/auth/login` - Login de usuário
- `GET /api/v1/auth/me` - Dados do usuário atual
- `POST /api/v1/auth/users` - Criar usuário (admin)

### 💼 Folha de Pagamento
- `GET /api/v1/payroll/employees` - Listar funcionários
- `POST /api/v1/payroll/employees` - Criar funcionário
- `GET /api/v1/payroll/competencies` - Listar competências
- `POST /api/v1/payroll/calculate` - Calcular folha

### 📄 Documentos
- `POST /api/v1/documents/upload` - Upload de documento
- `GET /api/v1/documents/` - Listar documentos
- `GET /api/v1/documents/{id}` - Obter documento

### 📝 CCT
- `GET /api/v1/cct/` - Listar CCTs
- `POST /api/v1/cct/` - Criar CCT
- `POST /api/v1/cct/{id}/compare/{other_id}` - Comparar CCTs

### 🤖 IA e Chatbot
- `POST /api/v1/ai/chat` - Conversar com chatbot
- `GET /api/v1/ai/recommendations` - Obter recomendações
- `GET /api/v1/ai/knowledge-base/search` - Buscar na base

## Documentação Interativa

**API Docs**: `http://localhost:8000/docs` (quando rodando localmente)
**Health Check**: `http://localhost:8000/health`

---

**Mantido sincronizado com a estrutura principal de documentação**