# 🔌 Endpoints Principais - API AUDITORIA360

## 🎯 Visão Geral

A API AUDITORIA360 oferece endpoints RESTful para integração completa com nossa plataforma de auditoria. Esta documentação cobre os principais endpoints utilizados para operações essenciais.

### Base URL
```
Produção: https://api.auditoria360.com.br/v1
Desenvolvimento: http://localhost:8000/v1
```

### Autenticação
Todos os endpoints (exceto `/auth/login`) requerem autenticação via JWT token no header:
```
Authorization: Bearer <token>
```

## 🔐 Autenticação

### POST /auth/login
Realiza login e retorna token de acesso.

**Request:**
```json
{
  "email": "usuario@empresa.com.br",
  "password": "senha123",
  "client_id": "empresa_123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "email": "usuario@empresa.com.br",
    "name": "João Silva",
    "role": "admin",
    "client_id": "empresa_123"
  }
}
```

### POST /auth/refresh
Renova token de acesso.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### POST /auth/logout
Invalida token atual.

**Response:**
```json
{
  "message": "Logout realizado com sucesso"
}
```

## 👥 Funcionários

### GET /funcionarios
Lista funcionários com paginação e filtros.

**Query Parameters:**
- `page`: Página (padrão: 1)
- `limit`: Itens por página (padrão: 50, máximo: 100)
- `search`: Busca por nome ou CPF
- `departamento`: Filtro por departamento
- `ativo`: Filtro por status (true/false)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "nome": "João Silva",
      "cpf": "123.456.789-00",
      "cargo": "Analista de Sistemas",
      "departamento": "TI",
      "salario": 5000.00,
      "data_admissao": "2023-01-15",
      "ativo": true,
      "created_at": "2023-01-15T10:00:00Z",
      "updated_at": "2023-01-15T10:00:00Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 250,
    "items_per_page": 50,
    "has_next": true,
    "has_prev": false
  }
}
```

### GET /funcionarios/{id}
Obtém detalhes de um funcionário específico.

**Response:**
```json
{
  "id": 1,
  "nome": "João Silva",
  "cpf": "123.456.789-00",
  "rg": "12.345.678-9",
  "cargo": "Analista de Sistemas",
  "departamento": "TI",
  "centro_custo": "TI001",
  "salario": 5000.00,
  "data_admissao": "2023-01-15",
  "data_nascimento": "1990-05-20",
  "estado_civil": "Solteiro",
  "escolaridade": "Superior Completo",
  "endereco": {
    "logradouro": "Rua das Flores, 123",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "uf": "SP",
    "cep": "01234-567"
  },
  "dependentes": [
    {
      "nome": "Maria Silva",
      "data_nascimento": "2020-03-10",
      "parentesco": "Filha"
    }
  ],
  "ativo": true,
  "created_at": "2023-01-15T10:00:00Z",
  "updated_at": "2023-01-15T10:00:00Z"
}
```

### POST /funcionarios
Cria novo funcionário.

**Request:**
```json
{
  "nome": "Maria Santos",
  "cpf": "987.654.321-00",
  "cargo": "Desenvolvedora",
  "departamento": "TI",
  "salario": 6000.00,
  "data_admissao": "2024-01-15",
  "endereco": {
    "logradouro": "Av. Paulista, 456",
    "bairro": "Bela Vista",
    "cidade": "São Paulo",
    "uf": "SP",
    "cep": "01310-100"
  }
}
```

### PUT /funcionarios/{id}
Atualiza funcionário existente.

### DELETE /funcionarios/{id}
Remove funcionário (soft delete).

## 📊 Auditorias

### GET /auditorias
Lista auditorias realizadas.

**Query Parameters:**
- `page`: Página
- `limit`: Itens por página
- `data_inicio`: Data início (YYYY-MM-DD)
- `data_fim`: Data fim (YYYY-MM-DD)
- `status`: Status da auditoria (pendente, em_progresso, concluida, erro)
- `tipo`: Tipo de auditoria (folha, cct, compliance)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "tipo": "folha",
      "periodo_referencia": "2024-01",
      "status": "concluida",
      "total_funcionarios": 250,
      "irregularidades_encontradas": 15,
      "valor_total_auditado": 1250000.00,
      "economia_identificada": 25000.00,
      "data_execucao": "2024-01-05T14:30:00Z",
      "tempo_execucao": 1800,
      "created_by": {
        "id": 1,
        "name": "João Silva"
      }
    }
  ],
  "pagination": {...}
}
```

### POST /auditorias
Inicia nova auditoria.

**Request:**
```json
{
  "tipo": "folha",
  "periodo_referencia": "2024-01",
  "parametros": {
    "verificar_horas_extras": true,
    "verificar_descontos": true,
    "aplicar_regras_cct": true,
    "departamentos": ["TI", "Vendas"],
    "funcionarios_especificos": [1, 2, 3]
  },
  "configuracoes": {
    "gerar_relatorio": true,
    "enviar_notificacao": true,
    "salvar_historico": true
  }
}
```

**Response:**
```json
{
  "id": 123,
  "status": "iniciada",
  "data_inicio": "2024-01-15T10:00:00Z",
  "previsao_conclusao": "2024-01-15T11:30:00Z",
  "job_id": "audit_job_abc123"
}
```

### GET /auditorias/{id}
Obtém detalhes de auditoria específica.

### GET /auditorias/{id}/resultados
Obtém resultados detalhados da auditoria.

**Response:**
```json
{
  "auditoria_id": 123,
  "resumo": {
    "funcionarios_auditados": 250,
    "irregularidades_total": 15,
    "valor_economia": 25000.00,
    "score_conformidade": 94.5
  },
  "irregularidades": [
    {
      "id": 1,
      "funcionario_id": 45,
      "funcionario_nome": "Carlos Oliveira",
      "tipo": "horas_extras_incorretas",
      "descricao": "Horas extras calculadas incorretamente - valor menor que o devido",
      "valor_erro": 250.00,
      "valor_correto": 320.00,
      "diferenca": 70.00,
      "severidade": "media",
      "status": "pendente",
      "recomendacao": "Revisar cálculo de horas extras para janeiro/2024"
    }
  ],
  "metricas_departamento": [
    {
      "departamento": "TI",
      "funcionarios": 50,
      "irregularidades": 2,
      "conformidade": 96.0
    }
  ]
}
```

## 📋 Relatórios

### GET /relatorios
Lista relatórios disponíveis.

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "nome": "Relatório de Auditoria - Janeiro 2024",
      "tipo": "auditoria",
      "formato": "pdf",
      "tamanho_mb": 2.5,
      "data_geracao": "2024-01-15T16:00:00Z",
      "valido_ate": "2024-04-15T16:00:00Z",
      "download_url": "https://api.auditoria360.com.br/v1/relatorios/1/download"
    }
  ]
}
```

### POST /relatorios
Gera novo relatório.

**Request:**
```json
{
  "tipo": "auditoria",
  "periodo": "2024-01",
  "formato": "pdf",
  "incluir_graficos": true,
  "incluir_detalhes": true,
  "filtros": {
    "departamentos": ["TI", "Vendas"],
    "apenas_irregularidades": false
  },
  "template": "executivo"
}
```

### GET /relatorios/{id}/download
Faz download do relatório.

## 📈 Dashboard e Métricas

### GET /dashboard/overview
Obtém métricas gerais do dashboard.

**Response:**
```json
{
  "periodo": "2024-01",
  "resumo": {
    "total_funcionarios": 250,
    "folha_total": 1250000.00,
    "economia_mes": 15000.00,
    "compliance_score": 95.2,
    "auditorias_realizadas": 12
  },
  "tendencias": {
    "funcionarios": "+5.2%",
    "folha_total": "+2.8%",
    "economia": "+15.5%",
    "compliance": "+1.2%"
  },
  "alertas": [
    {
      "tipo": "warning",
      "titulo": "CCT vencendo",
      "descricao": "Convenção do Sindicato ABC vence em 15 dias",
      "data_vencimento": "2024-02-01"
    }
  ]
}
```

### GET /dashboard/metricas
Obtém métricas detalhadas por período.

**Query Parameters:**
- `periodo`: Período (mes, trimestre, ano)
- `data_inicio`: Data início
- `data_fim`: Data fim
- `departamento`: Filtro por departamento

## 🔧 Configurações

### GET /configuracoes
Obtém configurações da empresa.

### PUT /configuracoes
Atualiza configurações.

### GET /configuracoes/regras-auditoria
Obtém regras de auditoria personalizadas.

### POST /configuracoes/regras-auditoria
Cria nova regra de auditoria.

## 📤 Upload e Importação

### POST /upload/folha
Faz upload de arquivo de folha de pagamento.

**Content-Type:** multipart/form-data

**Form Data:**
- `file`: Arquivo (Excel ou CSV)
- `periodo`: Período de referência (YYYY-MM)
- `mapeamento`: JSON com mapeamento de colunas

**Response:**
```json
{
  "upload_id": "upload_abc123",
  "status": "processando",
  "arquivo": "folha_janeiro_2024.xlsx",
  "linhas_detectadas": 250,
  "preview": [
    {
      "linha": 1,
      "nome": "João Silva",
      "cpf": "123.456.789-00",
      "salario": 5000.00
    }
  ]
}
```

### GET /upload/{id}/status
Verifica status do upload.

## ❌ Códigos de Erro

### Códigos HTTP
- `200`: Sucesso
- `201`: Criado com sucesso
- `400`: Requisição inválida
- `401`: Não autenticado
- `403`: Não autorizado
- `404`: Não encontrado
- `422`: Erro de validação
- `429`: Muitas requisições
- `500`: Erro interno do servidor

### Formato de Erro
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos",
    "details": [
      {
        "field": "cpf",
        "message": "CPF inválido"
      }
    ]
  }
}
```

## 🔄 Rate Limiting

- **Limite Geral**: 1000 requisições por hora por usuário
- **Limite de Upload**: 10 uploads por hora
- **Limite de Relatórios**: 50 gerações por hora

Headers de resposta:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## 📝 Webhooks

### Configuração
```json
{
  "url": "https://sua-api.com/webhooks/auditoria360",
  "eventos": ["auditoria.concluida", "irregularidade.detectada"],
  "secret": "webhook_secret_123"
}
```

### Eventos Disponíveis
- `auditoria.iniciada`
- `auditoria.concluida`
- `auditoria.erro`
- `irregularidade.detectada`
- `relatorio.gerado`
- `upload.concluido`

---

📚 **Documentação Completa**: Para mais detalhes, consulte nossa [documentação interativa](https://api.auditoria360.com.br/docs) com Swagger UI.

🔧 **SDKs Disponíveis**: Python, JavaScript, PHP - consulte nosso [GitHub](https://github.com/auditoria360/sdks).