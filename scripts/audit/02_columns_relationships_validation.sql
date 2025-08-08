-- =====================================================================
-- AUDITORIA360 - VALIDAÇÃO DE COLUNAS E RELAÇÕES MULTI-TENANT
-- =====================================================================
-- PARTE 1.2: Verificação das colunas e relações chave (Multi-Tenant)
-- =====================================================================

-- 1.2. 🔗 Script para verificar as colunas e relações chave (Multi-Tenant):

-- Verifica se as colunas essenciais para o multi-tenant foram criadas
SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE
    (table_name = 'Empresas' AND column_name = 'contabilidade_id') OR
    (table_name = 'profiles' AND column_name = 'contabilidade_id') OR
    (table_name = 'profiles' AND column_name = 'id' AND data_type = 'uuid');

-- Resultado Esperado: Deve ver três linhas:
-- Empresas, contabilidade_id, bigint
-- profiles, contabilidade_id, bigint
-- profiles, id, uuid
-- Isto confirma que a ligação entre empresas, perfis e contabilidades existe.