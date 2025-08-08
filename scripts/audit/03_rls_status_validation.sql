-- =====================================================================
-- AUDITORIA360 - VALIDAÇÃO DO STATUS DA ROW LEVEL SECURITY (RLS)
-- =====================================================================
-- PARTE 2: Auditoria da Segurança Multi-Tenant (RLS)
-- Esta é a auditoria mais importante. Vamos verificar se as "paredes" 
-- de segurança entre os seus clientes estão de pé.
-- =====================================================================

-- 2.1. 🔒 Script para verificar se a RLS está ATIVA nas tabelas:

-- Verifica o estado da Row Level Security (RLS) para cada tabela sensível
SELECT
    c.relname AS table_name,
    c.relrowsecurity AS rls_ativada
FROM pg_catalog.pg_class c
JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
AND c.relname IN ('Empresas', 'ControlesMensais', 'Documentos', 'TarefasControle');

-- Resultado Esperado: Uma lista das suas tabelas. A coluna rls_ativada 
-- deve ser true para todas elas. Se alguma estiver false, a segurança 
-- a nível de linha não está habilitada para essa tabela.