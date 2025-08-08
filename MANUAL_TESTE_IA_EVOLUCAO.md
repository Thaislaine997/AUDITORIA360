# Manual de Teste - Sistema de Aprendizagem Contínua da IA

## 📋 Resumo das Implementações

Este documento descreve como testar manualmente o novo sistema de aprendizagem contínua e RAG implementado no AUDITORIA360.

## 🗄️ PARTE 1: Configuração da Base de Dados

### 1.1 Executar a Migração SQL
Execute o script no Editor SQL da Supabase:

```sql
-- Cole o conteúdo do arquivo: /migrations/005_evoluir_schema_ia.sql
```

**Resultado Esperado:**
- ✅ Tabela `ParametrosLegais` renomeada para `RegrasValidadas`
- ✅ Nova tabela `ExtracoesIA` criada
- ✅ Enum `status_processamento` criado
- ✅ Todas as colunas e índices adicionados

### 1.2 Verificar Estrutura das Tabelas
```sql
-- Verificar estrutura da nova tabela de extrações
\d "ExtracoesIA"

-- Verificar estrutura da tabela de regras validadas
\d "RegrasValidadas"

-- Verificar se os índices foram criados
\di
```

## 🤖 PARTE 2: Testar Função Edge Atualizada

### 2.1 Verificar Deploy da Função
```bash
# No diretório do projeto
supabase functions deploy analisar-texto-com-ia
```

### 2.2 Teste Manual via Supabase Dashboard

1. **Acesse Functions no Dashboard**
2. **Execute com payload de teste:**
```json
{
  "record": {
    "id": 1,
    "texto_extraido": "O salário mínimo nacional fica estabelecido em R$ 1.412,00 a partir de janeiro de 2024. A alíquota do INSS para a primeira faixa salarial é de 7,5% até R$ 1.412,00."
  }
}
```

**Resultado Esperado:**
- ✅ Função executa sem erros
- ✅ Dados inseridos na tabela `ExtracoesIA` com status `PENDENTE`
- ✅ RAG: Usa contexto de regras validadas (se existirem)
- ✅ Campos de auditoria preenchidos (modelo, confidence score, raw_response)

### 2.3 Verificar Dados na Base de Dados
```sql
-- Verificar extrações inseridas
SELECT * FROM "ExtracoesIA" ORDER BY criado_em DESC LIMIT 5;

-- Verificar se RAG está funcionando (deve mostrar consultas à tabela RegrasValidadas)
-- Check nos logs da função Edge
```

## 🖥️ PARTE 3: Testar Interface Frontend

### 3.1 Executar Frontend Localmente
```bash
cd src/frontend
npm install
npm run dev
```

### 3.2 Acessar Nova Página de Validação

1. **Login no Sistema**
2. **Navegar para: Operação → Validação de IA**
3. **URL esperada:** `http://localhost:5173/validacao-ia`

**Resultado Esperado:**
- ✅ Página carrega sem erros
- ✅ Interface mostra abas (Pendentes, Concluídas, etc.)
- ✅ Estatísticas exibidas corretamente
- ✅ Lista de extrações pendentes aparece (se houver dados)

### 3.3 Testar Componente ValidacaoIARow

Para cada extração pendente, verificar:

1. **Visualização dos Dados:**
   - ✅ Nome do parâmetro exibido
   - ✅ Valor extraído mostrado
   - ✅ Tipo de valor (chip colorido)
   - ✅ Score de confiança (% com cor baseada no valor)
   - ✅ Contexto original do documento
   - ✅ Informações do modelo e timestamp

2. **Funcionalidade dos Botões:**
   - ✅ Botão "Aprovar" - move dados para `RegrasValidadas`
   - ✅ Botão "Editar" - abre modal de edição
   - ✅ States de carregamento funcionam

### 3.4 Testar Workflow de Aprovação

1. **Clicar em "Aprovar" em uma extração**

**Resultado Esperado:**
- ✅ Dados movidos de `ExtracoesIA` para `RegrasValidadas`
- ✅ Status atualizado para `CONCLUIDO`
- ✅ Campos de validação preenchidos
- ✅ Interface atualizada automaticamente
- ✅ Extração sai da aba "Pendentes" e vai para "Concluídas"

2. **Clicar em "Editar" em uma extração**

**Resultado Esperado:**
- ✅ Modal de edição abre
- ✅ Campos preenchidos com dados atuais
- ✅ Possível editar todos os campos principais
- ✅ "Salvar e Aprovar" funciona corretamente
- ✅ Dados editados são salvos na `RegrasValidadas`

## 🔄 PARTE 4: Testar Ciclo Completo RAG

### 4.1 Estabelecer Dados Base
1. **Processar alguns documentos e aprovar extrações**
2. **Verificar tabela `RegrasValidadas`:**
```sql
SELECT nome_parametro, valor_parametro, validado_por_humano 
FROM "RegrasValidadas" 
WHERE validado_por_humano = true;
```

### 4.2 Testar RAG em Nova Extração
1. **Processar novo documento com parâmetros similares**
2. **Verificar logs da função Edge Function**
3. **Confirmar que RAG está usando contexto das regras validadas**

**Resultado Esperado:**
- ✅ IA usa contexto de regras já validadas
- ✅ Extrações mais precisas para parâmetros similares
- ✅ Maior confidence score em extrações que batem com dados conhecidos

## 🧪 PARTE 5: Testes de Integração

### 5.1 Fluxo Completo
1. **Upload PDF → Extração de Texto → Análise IA → Validação Humana → Regra Final**

**Checkpoints:**
- ✅ PDF processado corretamente
- ✅ Texto extraído salvo em `Documentos`
- ✅ IA chamada automaticamente
- ✅ Dados salvos em `ExtracoesIA` com status PENDENTE
- ✅ Interface mostra extrações para validação
- ✅ Validação humana move dados para `RegrasValidadas`
- ✅ Próximas extrações usam dados validados como contexto

### 5.2 Testes de Performance
```sql
-- Verificar índices estão sendo usados
EXPLAIN ANALYZE SELECT * FROM "ExtracoesIA" WHERE status_validacao = 'PENDENTE';

-- Verificar performance de RAG
EXPLAIN ANALYZE SELECT * FROM "RegrasValidadas" WHERE validado_por_humano = true LIMIT 20;
```

## 🐛 Troubleshooting

### Problemas Comuns:

1. **Função Edge não encontra tabela RegrasValidadas**
   - Verificar se migração foi executada
   - Verificar nome da tabela (case-sensitive)

2. **Frontend não carrega extrações**
   - Verificar conexão Supabase
   - Verificar RLS (Row Level Security) policies
   - Verificar console do browser para erros JS

3. **RAG não está funcionando**
   - Verificar logs da função Edge
   - Confirmar que existem dados em `RegrasValidadas` com `validado_por_humano = true`

4. **Aprovação não funciona**
   - Verificar se usuário tem permissões de escrita
   - Verificar se foreign keys estão corretas
   - Verificar console do browser para erros de rede

## 📊 Métricas de Sucesso

Após testes completos, você deve observar:

- ✅ **Precisão Crescente**: IA fica mais precisa conforme mais dados são validados
- ✅ **Confidence Scores Maiores**: Parâmetros similares aos já conhecidos têm scores altos
- ✅ **Menos Correções**: Necessidade de edição diminui com o tempo
- ✅ **Contexto Relevante**: RAG usa dados históricos para melhorar extrações
- ✅ **Auditoria Completa**: Todas as respostas da IA ficam guardadas para análise

---

**🎯 Objetivo Alcançado:** Sistema transformado de ferramenta de "extração única" para plataforma de "aprendizagem contínua" com feedback humano e contextualização via RAG.