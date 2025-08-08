# Guia de Implementação Multi-Tenant para AUDITORIA360

Este documento descreve como implementar a segurança multi-tenant no AUDITORIA360, corrigindo os problemas de RLS (Row Level Security) e preparando o sistema para produção.

## Problema Resolvido

O erro `a relação "public.profiles" não existe` foi corrigido. O problema ocorreu porque a lógica de segurança (RLS) foi criada antes da tabela que identifica os utilizadores, tornando-a inválida.

## Solução Implementada

### 1. Script SQL Unificado

**Localização:** `/migrations/006_unified_multi_tenant_security.sql`

Este script único deve ser executado no **Editor SQL da Supabase** e contém:

1. **Criação da estrutura de dados:**
   - Tabela `Contabilidades` (empresas de contabilidade - tenants)
   - Tabela `profiles` (ligação de utilizadores a contabilidades)
   - Alteração da tabela `Empresas` para suporte multi-tenant
   - Tabela `TarefasControle` (que faltava anteriormente)

2. **Inserção de dados iniciais:**
   - 4 contabilidades pré-configuradas
   - Dados de exemplo para teste

3. **Configuração de segurança:**
   - Habilitação de RLS em todas as tabelas sensíveis
   - Criação de políticas de segurança corrigidas
   - Função auxiliar `auth.get_contabilidade_id()`

### 2. Script de Migração de Dados

**Localização:** `/scripts/migracao.py`

Script Python para importar dados de PDFs para o Supabase com:
- Extração automática de dados de PDFs
- Inserção segura na base de dados
- Associação automática a contabilidades
- Tratamento de erros robusto

**Dependências:** `/scripts/requirements-migration.txt`

## Instruções de Implementação

### Passo 1: Executar o Script SQL

1. Acesse o **Editor SQL** da sua Supabase
2. Copie e cole todo o conteúdo do arquivo `/migrations/006_unified_multi_tenant_security.sql`
3. Execute o script (deve executar sem erros)

### Passo 2: Configurar Utilizadores

1. Crie utilizadores no sistema (em *Authentication -> Users*)
2. Para cada utilizador, acesse *Table Editor -> profiles*
3. Preencha a coluna `contabilidade_id` com o ID correto da contabilidade
   - Use a tabela `Contabilidades` para consultar os IDs disponíveis

### Passo 3: Migração de Dados (Opcional)

Se você tem dados em PDFs para importar:

1. Instale as dependências:
   ```bash
   pip install -r scripts/requirements-migration.txt
   ```

2. Configure as variáveis de ambiente:
   ```bash
   export SUPABASE_URL="https://seu-projeto.supabase.co"
   export SUPABASE_SERVICE_KEY="sua-service-key"
   ```

3. Ajuste os caminhos dos PDFs no script `migracao.py`

4. Execute a migração:
   ```bash
   python scripts/migracao.py
   ```

## Estrutura Multi-Tenant

### Tabelas Principais

- **`Contabilidades`**: Empresas de contabilidade (tenants)
- **`profiles`**: Ligação de utilizadores autenticados a contabilidades
- **`Empresas`**: Empresas clientes (com `contabilidade_id`)
- **`ControlesMensais`**: Controles mensais das empresas
- **`TarefasControle`**: Tarefas específicas de cada controle

### Segurança Implementada

1. **Row Level Security (RLS)** habilitado em todas as tabelas sensíveis
2. **Políticas de acesso** que garantem isolamento de dados por contabilidade
3. **Função auxiliar** `auth.get_contabilidade_id()` para simplificar políticas
4. **Isolamento completo** - cada contabilidade só vê seus próprios dados

## Validação da Implementação

### Teste de Segurança

1. Faça login com um utilizador da "CKONT"
2. Verifique se ele só vê dados ligados à CKONT
3. Faça login com um utilizador da "Elaine Contabilidade"  
4. Confirme que só vê os dados da sua contabilidade

### Verificação de Dados

Execute estas consultas no Editor SQL para validar:

```sql
-- Verificar contabilidades criadas
SELECT * FROM public."Contabilidades";

-- Verificar estrutura da tabela Empresas
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'Empresas' AND table_schema = 'public';

-- Testar função de segurança (como utilizador autenticado)
SELECT auth.get_contabilidade_id();
```

## Contabilidades Pré-Configuradas

1. **Elaine Cristina da Silva Contabilidade**
   - CNPJ: 21.391.377/0001-99

2. **CONTROLLER SOLUCOES LTDA**
   - CNPJ: 21.719.740/0001-52

3. **CKONT ASSESSORIA EMPRESARIAL LTDA**
   - CNPJ: 50.215.504/0001-05

4. **VENDEDOR CONTABIL CONTABILIDADE E CONSULTORIA EMPRESARIAL LTDA**
   - CNPJ: 47.229.784/0001-98

## Solução de Problemas

### Erro: "relation does not exist"
- Confirme que executou o script SQL completo
- Verifique se todas as tabelas foram criadas corretamente

### Erro: "permission denied"
- Verifique se o RLS está configurado corretamente
- Confirme que o utilizador tem um `contabilidade_id` na tabela `profiles`

### Dados não aparecem
- Verifique se o utilizador está associado à contabilidade correta
- Confirme se as empresas têm `contabilidade_id` preenchido

## Próximos Passos

Após a implementação:

1. **Teste exaustivamente** o isolamento de dados
2. **Configure backup** automático dos dados
3. **Monitore performance** das consultas com RLS
4. **Documente** procedimentos operacionais
5. **Treine utilizadores** no novo sistema

## Suporte

Para problemas ou dúvidas:
1. Verifique os logs do Supabase
2. Execute queries de diagnóstico fornecidas
3. Consulte a documentação oficial do Supabase sobre RLS