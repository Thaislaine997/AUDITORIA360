# 📡 AUDITORIA360 - Referência Completa da API

*Documentação completa dos endpoints, payloads e integrações*

---

## 🚀 Visão Geral da API

### Informações Base
- **Base URL**: `https://api.auditoria360.com`
- **Versão**: `v1`
- **Protocolo**: HTTPS/TLS 1.3
- **Formato**: JSON
- **Autenticação**: JWT Bearer Token
- **Rate Limiting**: 100 requests/minute por IP

### Arquitetura Multi-Tenant
- **Isolamento**: Row Level Security (RLS) por `contabilidade_id`
- **Contexto**: Definido automaticamente via token JWT
- **Segurança**: Acesso apenas aos dados da própria contabilidade

---

## 🔐 Autenticação e Autorização

### POST `/api/auth/login`
Realiza login do usuário e retorna tokens de acesso.

**Request:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "contab1@exemplo.com",
  "password": "senha123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "contab1@exemplo.com",
    "nome": "João Silva",
    "perfil": "operador",
    "contabilidade": {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "nome": "Contabilidade ABC"
    }
  }
}
```

**Errors:**
```json
// 401 Unauthorized
{
  "detail": "Credenciais inválidas",
  "code": "INVALID_CREDENTIALS"
}

// 429 Too Many Requests
{
  "detail": "Muitas tentativas de login. Tente novamente em 15 minutos.",
  "code": "RATE_LIMIT_EXCEEDED"
}
```

### POST `/api/auth/refresh`
Renova o token de acesso usando o refresh token.

**Request:**
```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer", 
  "expires_in": 3600
}
```

### POST `/api/auth/logout`
Invalida os tokens do usuário.

**Request:**
```http
POST /api/auth/logout
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
  "message": "Logout realizado com sucesso"
}
```

### GET `/api/auth/profile`
Retorna informações do perfil do usuário logado.

**Request:**
```http
GET /api/auth/profile
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "contab1@exemplo.com",
  "nome": "João Silva",
  "perfil": "operador",
  "created_at": "2025-08-01T10:00:00Z",
  "last_login": "2025-08-11T14:30:00Z",
  "contabilidade": {
    "id": "123e4567-e89b-12d3-a456-426655440000",
    "nome": "Contabilidade ABC",
    "cnpj": "12345678000100"
  },
  "permissoes": [
    "clientes:read",
    "clientes:write", 
    "auditorias:create",
    "relatorios:read"
  ]
}
```

---

## 👥 Gestão de Clientes Finais

### GET `/api/contabilidade/clientes`
Lista todos os clientes da contabilidade autenticada.

**Request:**
```http
GET /api/contabilidade/clientes?page=1&limit=20&search=empresa
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Query Parameters:**
- `page` (opcional): Número da página (default: 1)
- `limit` (opcional): Itens por página (default: 20, max: 100)
- `search` (opcional): Busca por nome/CNPJ
- `ativo` (opcional): Filtrar por status ativo (true/false)

**Response (200 OK):**
```json
{
  "clientes": [
    {
      "id": "789e0123-f45g-67h8-i901-234567890123",
      "nome": "Empresa XPTO Ltda",
      "cnpj": "12345678000199",
      "email_contato": "rh@xpto.com.br",
      "telefone": "(11) 99999-9999",
      "endereco": {
        "logradouro": "Rua das Empresas, 123",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01234-567"
      },
      "ativo": true,
      "created_at": "2025-07-15T09:00:00Z",
      "updated_at": "2025-08-10T16:30:00Z",
      "ultima_auditoria": "2025-08-01T10:00:00Z",
      "total_funcionarios": 25,
      "score_risco_atual": 75
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1,
    "total_pages": 1
  }
}
```

### POST `/api/contabilidade/clientes`
Cria um novo cliente final.

**Request:**
```http
POST /api/contabilidade/clientes
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "nome": "Nova Empresa Ltda",
  "cnpj": "98765432000188",
  "email_contato": "contato@novaempresa.com.br",
  "telefone": "(11) 88888-8888",
  "endereco": {
    "logradouro": "Av. Principal, 456",
    "cidade": "Rio de Janeiro", 
    "estado": "RJ",
    "cep": "22222-333"
  },
  "responsavel_rh": {
    "nome": "Maria Santos",
    "email": "maria@novaempresa.com.br",
    "telefone": "(11) 77777-7777"
  }
}
```

**Response (201 Created):**
```json
{
  "id": "456e7890-f12g-34h5-i678-901234567890",
  "nome": "Nova Empresa Ltda",
  "cnpj": "98765432000188",
  "email_contato": "contato@novaempresa.com.br",
  "telefone": "(11) 88888-8888",
  "endereco": {
    "logradouro": "Av. Principal, 456",
    "cidade": "Rio de Janeiro",
    "estado": "RJ", 
    "cep": "22222-333"
  },
  "responsavel_rh": {
    "nome": "Maria Santos",
    "email": "maria@novaempresa.com.br",
    "telefone": "(11) 77777-7777"
  },
  "ativo": true,
  "created_at": "2025-08-11T19:30:00Z",
  "updated_at": "2025-08-11T19:30:00Z",
  "total_funcionarios": 0,
  "score_risco_atual": null
}
```

**Validation Errors (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "cnpj"],
      "msg": "CNPJ inválido",
      "type": "value_error"
    },
    {
      "loc": ["body", "email_contato"],
      "msg": "Email inválido",
      "type": "value_error"
    }
  ]
}
```

### GET `/api/contabilidade/clientes/{cliente_id}`
Obtém detalhes de um cliente específico.

**Request:**
```http
GET /api/contabilidade/clientes/789e0123-f45g-67h8-i901-234567890123
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
  "id": "789e0123-f45g-67h8-i901-234567890123",
  "nome": "Empresa XPTO Ltda",
  "cnpj": "12345678000199",
  "email_contato": "rh@xpto.com.br",
  "telefone": "(11) 99999-9999",
  "endereco": {
    "logradouro": "Rua das Empresas, 123",
    "cidade": "São Paulo",
    "estado": "SP",
    "cep": "01234-567"
  },
  "responsavel_rh": {
    "nome": "João Silva",
    "email": "joao@xpto.com.br",
    "telefone": "(11) 99999-9998"
  },
  "ativo": true,
  "created_at": "2025-07-15T09:00:00Z",
  "updated_at": "2025-08-10T16:30:00Z",
  "total_funcionarios": 25,
  "score_risco_atual": 75,
  "historico_auditorias": [
    {
      "id": "AUD-2025-08-001",
      "data": "2025-08-01T10:00:00Z",
      "score_risco": 75,
      "status": "concluida"
    }
  ],
  "configuracoes": {
    "auditoria_automatica": true,
    "dia_auditoria": 5,
    "notificacoes_email": true
  }
}
```

### PUT `/api/contabilidade/clientes/{cliente_id}`
Atualiza dados de um cliente.

**Request:**
```http
PUT /api/contabilidade/clientes/789e0123-f45g-67h8-i901-234567890123
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "email_contato": "novo.email@xpto.com.br",
  "telefone": "(11) 88888-8888",
  "responsavel_rh": {
    "nome": "Maria Silva",
    "email": "maria@xpto.com.br",
    "telefone": "(11) 88888-8899"
  }
}
```

**Response (200 OK):**
```json
{
  "id": "789e0123-f45g-67h8-i901-234567890123",
  "nome": "Empresa XPTO Ltda",
  "cnpj": "12345678000199",
  "email_contato": "novo.email@xpto.com.br",
  "telefone": "(11) 88888-8888",
  "responsavel_rh": {
    "nome": "Maria Silva",
    "email": "maria@xpto.com.br",
    "telefone": "(11) 88888-8899"
  },
  "updated_at": "2025-08-11T20:00:00Z"
}
```

### DELETE `/api/contabilidade/clientes/{cliente_id}`
Desativa um cliente (soft delete).

**Request:**
```http
DELETE /api/contabilidade/clientes/789e0123-f45g-67h8-i901-234567890123
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
  "message": "Cliente desativado com sucesso",
  "cliente_id": "789e0123-f45g-67h8-i901-234567890123",
  "desativado_em": "2025-08-11T20:15:00Z"
}
```

---

## 🔍 Sistema de Auditorias

### GET `/api/contabilidade/auditorias`
Lista auditorias da contabilidade.

**Request:**
```http
GET /api/contabilidade/auditorias?cliente_id=789e0123-f45g-67h8-i901-234567890123&status=concluida&mes=2025-08
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Query Parameters:**
- `cliente_id` (opcional): Filtrar por cliente
- `status` (opcional): processando, concluida, erro
- `mes` (opcional): Filtrar por mês (YYYY-MM)
- `page` (opcional): Paginação
- `limit` (opcional): Itens por página

**Response (200 OK):**
```json
{
  "auditorias": [
    {
      "id": "AUD-2025-08-001",
      "cliente": {
        "id": "789e0123-f45g-67h8-i901-234567890123",
        "nome": "Empresa XPTO Ltda"
      },
      "mes_referencia": "2025-08",
      "tipo": "mensal",
      "status": "concluida",
      "score_risco": 75,
      "created_at": "2025-08-01T10:00:00Z",
      "completed_at": "2025-08-01T10:05:00Z",
      "total_divergencias": 3,
      "divergencias_criticas": 1,
      "relatorio_url": "https://storage.auditoria360.com/relatorios/AUD-2025-08-001.pdf"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1,
    "total_pages": 1
  },
  "resumo": {
    "total_auditorias": 15,
    "concluidas": 12,
    "processando": 2,
    "com_erro": 1,
    "score_medio": 78.5
  }
}
```

### POST `/api/contabilidade/auditorias`
Dispara uma nova auditoria.

**Request:**
```http
POST /api/contabilidade/auditorias
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "cliente_id": "789e0123-f45g-67h8-i901-234567890123",
  "mes_referencia": "2025-08",
  "tipo": "mensal",
  "opcoes": {
    "incluir_historico": true,
    "verificar_esocial": true,
    "analise_detalhada": true,
    "gerar_relatorio_pdf": true
  }
}
```

**Response (201 Created):**
```json
{
  "id": "AUD-2025-08-002",
  "cliente": {
    "id": "789e0123-f45g-67h8-i901-234567890123",
    "nome": "Empresa XPTO Ltda"
  },
  "mes_referencia": "2025-08",
  "tipo": "mensal",
  "status": "processando",
  "created_at": "2025-08-11T20:30:00Z",
  "estimated_completion": "2025-08-11T20:35:00Z",
  "opcoes": {
    "incluir_historico": true,
    "verificar_esocial": true,
    "analise_detalhada": true,
    "gerar_relatorio_pdf": true
  }
}
```

### GET `/api/contabilidade/auditorias/{auditoria_id}`
Obtém detalhes de uma auditoria específica.

**Request:**
```http
GET /api/contabilidade/auditorias/AUD-2025-08-001
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
  "id": "AUD-2025-08-001",
  "cliente": {
    "id": "789e0123-f45g-67h8-i901-234567890123",
    "nome": "Empresa XPTO Ltda",
    "cnpj": "12345678000199"
  },
  "mes_referencia": "2025-08",
  "tipo": "mensal",
  "status": "concluida",
  "score_risco": 75,
  "created_at": "2025-08-01T10:00:00Z",
  "completed_at": "2025-08-01T10:05:00Z",
  "tempo_processamento": "00:05:23",
  "resumo_execucao": {
    "funcionarios_analisados": 25,
    "calculos_verificados": 475,
    "regras_aplicadas": 15,
    "divergencias_encontradas": 3
  },
  "divergencias": [
    {
      "tipo": "critica",
      "categoria": "INSS",
      "descricao": "Base de cálculo INSS incorreta para funcionário João Silva",
      "funcionario": "João Silva",
      "valor_esperado": 1200.00,
      "valor_encontrado": 1150.00,
      "diferenca": 50.00,
      "recomendacao": "Revisar base de cálculo do INSS considerando adicional noturno"
    },
    {
      "tipo": "media",
      "categoria": "FGTS",
      "descricao": "Depósito FGTS com atraso de 2 dias",
      "valor_multa_estimada": 25.50,
      "recomendacao": "Configurar lembretes automáticos para depósitos FGTS"
    },
    {
      "tipo": "baixa", 
      "categoria": "Documentação",
      "descricao": "Falta assinatura digital em 3 holerites",
      "quantidade_afetada": 3,
      "recomendacao": "Implementar assinatura digital automática"
    }
  ],
  "relatorio_url": "https://storage.auditoria360.com/relatorios/AUD-2025-08-001.pdf",
  "arquivos_analisados": [
    {
      "nome": "folha_agosto_2025.xlsx",
      "tamanho": 245760,
      "uploaded_at": "2025-08-01T09:55:00Z"
    }
  ]
}
```

### GET `/api/contabilidade/auditorias/{auditoria_id}/score_risco`
Obtém o score de risco detalhado de uma auditoria.

**Request:**
```http
GET /api/contabilidade/auditorias/AUD-2025-08-001/score_risco
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
  "score_risco": 75,
  "classificacao": "MEDIO",
  "tendencia": "estavel",
  "historico_scores": [
    {"mes": "2025-06", "score": 70},
    {"mes": "2025-07", "score": 73},
    {"mes": "2025-08", "score": 75}
  ],
  "componentes_score": {
    "calculos_tributarios": {
      "score": 80,
      "peso": 0.4,
      "contribuicao": 32.0,
      "status": "bom"
    },
    "obrigacoes_acessorias": {
      "score": 65,
      "peso": 0.3,
      "contribuicao": 19.5,
      "status": "atencao"
    },
    "documentacao": {
      "score": 85,
      "peso": 0.2,
      "contribuicao": 17.0,
      "status": "excelente"
    },
    "prazos_legais": {
      "score": 60,
      "peso": 0.1,
      "contribuicao": 6.0,
      "status": "critico"
    }
  },
  "recomendacoes": [
    {
      "prioridade": "alta",
      "categoria": "prazos_legais",
      "descricao": "Implementar sistema de lembretes para obrigações",
      "impacto_estimado": "+10 pontos"
    },
    {
      "prioridade": "media",
      "categoria": "obrigacoes_acessorias", 
      "descricao": "Revisar processo de entrega do eSocial",
      "impacto_estimado": "+5 pontos"
    }
  ]
}
```

### GET `/api/contabilidade/auditorias/{auditoria_id}/relatorio`
Faz download do relatório PDF da auditoria.

**Request:**
```http
GET /api/contabilidade/auditorias/AUD-2025-08-001/relatorio
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```http
Content-Type: application/pdf
Content-Disposition: attachment; filename="auditoria_AUD-2025-08-001.pdf"
Content-Length: 524288

%PDF-1.4
[binary PDF content]
```

---

## 🧠 Integração com IA

### POST `/api/ai/analyze-payroll`
Envia dados da folha para análise inteligente.

**Request:**
```http
POST /api/ai/analyze-payroll
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "cliente_id": "789e0123-f45g-67h8-i901-234567890123",
  "mes_referencia": "2025-08",
  "dados_folha": {
    "funcionarios": [
      {
        "nome": "João Silva",
        "cargo": "Analista",
        "salario_base": 5000.00,
        "adicionais": {
          "horas_extras": 300.00,
          "adicional_noturno": 200.00
        },
        "descontos": {
          "inss": 550.00,
          "irrf": 427.00,
          "vale_transporte": 132.00
        }
      }
    ],
    "totalizadores": {
      "total_bruto": 125000.00,
      "total_inss": 13750.00,
      "total_irrf": 10675.00,
      "total_fgts": 10000.00
    }
  },
  "regras_aplicaveis": [
    "inss_2025",
    "irrf_2025", 
    "fgts_padrao",
    "convenção_metalurgicos_sp"
  ],
  "opcoes_analise": {
    "verificar_calculos": true,
    "comparar_historico": true,
    "sugerir_otimizacoes": true,
    "detectar_anomalias": true
  }
}
```

**Response (200 OK):**
```json
{
  "resultado": "analise_concluida",
  "tempo_processamento": "00:02:15",
  "score_risco_calculado": 75,
  "divergencias_encontradas": [
    {
      "funcionario": "João Silva",
      "categoria": "INSS",
      "tipo": "erro_calculo",
      "descricao": "Base de cálculo INSS não considerou adicional noturno",
      "valor_correto": 550.00,
      "valor_informado": 500.00,
      "diferenca": 50.00,
      "explicacao_ia": "O adicional noturno de R$ 200,00 deve integrar a base de cálculo do INSS. A alíquota de 11% aplicada sobre R$ 5.200,00 resultaria em R$ 572,00.",
      "referencias_legais": ["Lei 8.213/91, Art. 28"]
    }
  ],
  "anomalias_detectadas": [
    {
      "tipo": "padrao_incomum",
      "descricao": "Aumento de 15% nas horas extras em relação ao mês anterior",
      "funcionarios_afetados": 8,
      "recomendacao": "Verificar se houve evento específico que justifique o aumento"
    }
  ],
  "otimizacoes_sugeridas": [
    {
      "categoria": "tributaria",
      "descricao": "Possível economia com vale-alimentação",
      "economia_estimada": 1250.00,
      "explicacao": "Substituir parte do salário por vale-alimentação (limite R$ 2.112,00) pode reduzir encargos em até R$ 1.250,00/mês"
    }
  ],
  "comparacao_historica": {
    "mes_anterior": {
      "score_risco": 73,
      "total_divergencias": 2,
      "principais_melhorias": ["Correção cálculo FGTS"]
    },
    "tendencia": "leve_piora",
    "principais_indicadores": {
      "pontualidade_pagamentos": "estavel",
      "conformidade_calculos": "piora_leve",
      "documentacao": "melhoria"
    }
  }
}
```

### POST `/api/ai/chat`
Interface de chat com IA para suporte e dúvidas.

**Request:**
```http
POST /api/ai/chat
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "message": "Como calcular corretamente o adicional noturno para um funcionário que trabalha das 22h às 6h?",
  "context": {
    "cliente_id": "789e0123-f45g-67h8-i901-234567890123",
    "conversation_id": "chat_2025_08_11_001"
  }
}
```

**Response (200 OK):**
```json
{
  "response": "Para calcular o adicional noturno corretamente:\n\n1. **Horário noturno**: 22h às 5h (CLT, Art. 73)\n2. **Percentual**: 20% sobre a hora normal\n3. **Hora reduzida**: Cada hora noturna = 52min30s\n\n**Exemplo prático:**\n- Funcionário das 22h às 6h = 8h trabalhadas\n- Período noturno: 22h às 5h = 7h normais\n- Com hora reduzida: 7h ÷ 52,5min = 8h (considerar 8 horas noturnas)\n- Adicional: Valor da hora × 20% × 8h\n\n**Base de cálculo**: O adicional noturno integra salário para INSS, IRRF e FGTS.\n\n**Referência legal**: CLT Art. 73, IN RFB 971/2009",
  "conversation_id": "chat_2025_08_11_001",
  "message_id": "msg_001", 
  "references": [
    {
      "type": "lei",
      "title": "CLT - Art. 73",
      "url": "http://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm"
    },
    {
      "type": "instrucao_normativa",
      "title": "IN RFB 971/2009",
      "url": "http://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=15055"
    }
  ],
  "related_topics": [
    "Cálculo de horas extras",
    "Integração de adicionais à base de cálculo",
    "Jornada de trabalho noturno"
  ]
}
```

### GET `/api/ai/models/status`
Verifica status dos modelos de IA.

**Request:**
```http
GET /api/ai/models/status
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
  "models": {
    "payroll_analyzer": {
      "status": "active",
      "version": "2.1.0",
      "last_update": "2025-08-01T10:00:00Z",
      "accuracy": 94.5,
      "avg_response_time": "2.3s"
    },
    "risk_calculator": {
      "status": "active",
      "version": "1.8.0",
      "last_update": "2025-07-15T14:30:00Z",
      "accuracy": 91.2,
      "avg_response_time": "1.1s"
    },
    "chatbot": {
      "status": "active",
      "version": "3.0.1",
      "last_update": "2025-08-10T09:15:00Z",
      "accuracy": 89.7,
      "avg_response_time": "0.8s"
    }
  },
  "overall_status": "healthy",
  "last_maintenance": "2025-08-10T02:00:00Z"
}
```

---

## 📊 Relatórios e Dashboard

### GET `/api/reports/dashboard`
Dados para o dashboard principal.

**Request:**
```http
GET /api/reports/dashboard?periodo=30d
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Query Parameters:**
- `periodo`: 7d, 30d, 90d, 1y (default: 30d)

**Response (200 OK):**
```json
{
  "resumo": {
    "total_clientes": 15,
    "clientes_ativos": 12,
    "auditorias_mes": 28,
    "score_medio": 78.5,
    "alertas_pendentes": 3
  },
  "metricas_periodo": {
    "auditorias_realizadas": 85,
    "divergencias_encontradas": 127,
    "divergencias_resolvidas": 98,
    "economia_identificada": 15780.50,
    "tempo_medio_auditoria": "00:03:45"
  },
  "distribuicao_scores": {
    "excelente": {"range": "90-100", "count": 2},
    "bom": {"range": "80-89", "count": 5},
    "medio": {"range": "60-79", "count": 4},
    "ruim": {"range": "40-59", "count": 1},
    "critico": {"range": "0-39", "count": 0}
  },
  "tendencias": {
    "scores": [
      {"periodo": "2025-07", "score_medio": 76.2},
      {"periodo": "2025-08", "score_medio": 78.5}
    ],
    "auditorias": [
      {"periodo": "2025-07", "total": 82},
      {"periodo": "2025-08", "total": 85}
    ]
  },
  "top_divergencias": [
    {
      "categoria": "INSS",
      "occorrencias": 15,
      "impacto_financeiro": 2340.00
    },
    {
      "categoria": "IRRF", 
      "occorrencias": 12,
      "impacto_financeiro": 1890.50
    }
  ],
  "alertas": [
    {
      "id": "ALT-001",
      "tipo": "prazo",
      "titulo": "eSocial vencendo em 2 dias",
      "cliente": "Empresa ABC",
      "prioridade": "alta",
      "created_at": "2025-08-09T10:00:00Z"
    }
  ]
}
```

### POST `/api/reports/generate`
Gera relatório customizado.

**Request:**
```http
POST /api/reports/generate
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "tipo": "executivo",
  "periodo": {
    "inicio": "2025-07-01",
    "fim": "2025-08-31"
  },
  "filtros": {
    "clientes": ["789e0123-f45g-67h8-i901-234567890123"],
    "categorias": ["INSS", "IRRF", "FGTS"],
    "score_minimo": 60
  },
  "formato": "pdf",
  "opcoes": {
    "incluir_graficos": true,
    "incluir_recomendacoes": true,
    "incluir_comparativo": true,
    "enviar_email": true,
    "emails_destinatarios": ["gestor@contabilidade.com"]
  }
}
```

**Response (202 Accepted):**
```json
{
  "job_id": "RPT-2025-08-11-001",
  "status": "processando",
  "estimated_completion": "2025-08-11T21:05:00Z",
  "status_url": "/api/reports/jobs/RPT-2025-08-11-001"
}
```

### GET `/api/reports/jobs/{job_id}`
Status da geração de relatório.

**Request:**
```http
GET /api/reports/jobs/RPT-2025-08-11-001
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
  "job_id": "RPT-2025-08-11-001",
  "status": "concluido",
  "created_at": "2025-08-11T21:00:00Z",
  "completed_at": "2025-08-11T21:04:32Z",
  "resultado": {
    "download_url": "https://storage.auditoria360.com/reports/RPT-2025-08-11-001.pdf",
    "expires_at": "2025-08-18T21:04:32Z",
    "file_size": 1048576,
    "email_enviado": true
  }
}
```

---

## ⚙️ Sistema de Configurações

### GET `/api/contabilidade/configuracoes`
Obtém configurações da contabilidade.

**Request:**
```http
GET /api/contabilidade/configuracoes
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
  "auditoria": {
    "automatica": true,
    "dia_mes": 5,
    "incluir_analise_ia": true,
    "gerar_relatorio_automatico": true
  },
  "notificacoes": {
    "email_auditoria_concluida": true,
    "email_divergencias_criticas": true,
    "slack_webhook": "https://hooks.slack.com/...",
    "whatsapp_enabled": false
  },
  "integracao": {
    "esocial_automatico": true,
    "backup_r2": true,
    "sync_folha": false
  },
  "personalização": {
    "logo_url": "https://storage.auditoria360.com/logos/contab123.png",
    "cores_tema": {
      "primary": "#007bff",
      "secondary": "#6c757d"
    }
  }
}
```

### PUT `/api/contabilidade/configuracoes`
Atualiza configurações da contabilidade.

**Request:**
```http
PUT /api/contabilidade/configuracoes
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "auditoria": {
    "automatica": true,
    "dia_mes": 10
  },
  "notificacoes": {
    "email_divergencias_criticas": true,
    "slack_webhook": "https://hooks.slack.com/new-webhook"
  }
}
```

**Response (200 OK):**
```json
{
  "message": "Configurações atualizadas com sucesso",
  "updated_at": "2025-08-11T21:15:00Z"
}
```

---

## 🔧 Utilitários e Sistema

### GET `/api/health`
Health check do sistema.

**Request:**
```http
GET /api/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-11T21:20:00Z",
  "version": "1.0.0",
  "environment": "production",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "openai": "healthy",
    "storage": "healthy"
  },
  "metrics": {
    "active_connections": 25,
    "response_time_p95": 234,
    "memory_usage": "68%",
    "cpu_usage": "42%"
  }
}
```

### GET `/api/status`
Status detalhado do sistema.

**Request:**
```http
GET /api/status
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Response (200 OK):**
```json
{
  "system": {
    "uptime": "15d 4h 23m",
    "last_deployment": "2025-08-01T10:00:00Z",
    "version": "1.0.0",
    "environment": "production"
  },
  "statistics": {
    "total_users": 125,
    "active_sessions": 23,
    "auditorias_today": 15,
    "requests_per_minute": 45.2
  },
  "performance": {
    "avg_response_time": "245ms",
    "p95_response_time": "780ms",
    "error_rate": "0.12%",
    "uptime_percentage": 99.97
  }
}
```

---

## ⚠️ Códigos de Erro

### Códigos HTTP Padrão
- **200 OK**: Requisição bem-sucedida
- **201 Created**: Recurso criado com sucesso
- **400 Bad Request**: Dados inválidos na requisição
- **401 Unauthorized**: Token inválido ou ausente
- **403 Forbidden**: Sem permissão para o recurso
- **404 Not Found**: Recurso não encontrado
- **422 Unprocessable Entity**: Erro de validação
- **429 Too Many Requests**: Rate limit excedido
- **500 Internal Server Error**: Erro interno do servidor

### Códigos de Erro Customizados
```json
{
  "detail": "Mensagem de erro legível",
  "code": "CODIGO_ERRO_INTERNO",
  "timestamp": "2025-08-11T21:25:00Z",
  "path": "/api/endpoint",
  "trace_id": "abc123-def456-ghi789"
}
```

#### Códigos Específicos
- `INVALID_CREDENTIALS`: Credenciais de login inválidas
- `TOKEN_EXPIRED`: Token JWT expirado
- `RATE_LIMIT_EXCEEDED`: Muitas requisições
- `INSUFFICIENT_PERMISSIONS`: Sem permissão
- `RESOURCE_NOT_FOUND`: Recurso não encontrado
- `VALIDATION_ERROR`: Erro de validação de dados
- `EXTERNAL_SERVICE_ERROR`: Erro em serviço externo (IA, storage)
- `MULTI_TENANT_VIOLATION`: Tentativa de acesso cross-tenant

---

## 📋 Rate Limiting

### Limites por Endpoint
| Endpoint | Limite | Janela |
|----------|--------|--------|
| `/api/auth/login` | 5 requests | 5 minutos |
| `/api/auth/refresh` | 10 requests | 1 minuto |  
| `/api/contabilidade/*` | 100 requests | 1 minuto |
| `/api/ai/*` | 20 requests | 1 minuto |
| `/api/reports/*` | 50 requests | 1 minuto |
| Outros endpoints | 200 requests | 1 minuto |

### Headers de Rate Limiting
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1691784900
Retry-After: 60
```

---

**Esta documentação da API é atualizada automaticamente e reflete o estado atual do sistema AUDITORIA360.**