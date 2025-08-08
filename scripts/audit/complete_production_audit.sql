-- =====================================================================
-- AUDITORIA360 - SCRIPT CONSOLIDADO DE VALIDAÇÃO DE PRODUÇÃO
-- =====================================================================
-- [VALIDAÇÃO] Auditoria Completa da Configuração de Produção
--
-- Objetivo: Validar de forma sistemática a estrutura da base de dados, 
-- a implementação da segurança multi-tenant (RLS) e a integridade dos dados, 
-- garantindo que a plataforma auditoria360 está corretamente configurada 
-- conforme o planeado.
-- =====================================================================

-- INSTRUÇÕES DE USO:
-- Execute cada seção deste script no seu Editor SQL da Supabase.
-- Analise os resultados de cada um conforme a descrição para diagnosticar 
-- a saúde do seu sistema.

-- =====================================================================
-- PARTE 1: VERIFICAÇÃO DO SCHEMA DA BASE DE DADOS
-- =====================================================================
-- Estes scripts verificam se a "planta" da sua base de dados está correta.

-- 1.1. 📜 Script para verificar se todas as tabelas principais existem:
SELECT
    '1.1 - Verificação de Tabelas Principais' AS teste,
    table_name,
    EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = T.table_name
    ) AS tabela_existe
FROM (VALUES
    ('Contabilidades'),
    ('Empresas'),
    ('ControlesMensais'),
    ('Documentos'),
    ('TarefasControle'),
    ('profiles')
) AS T(table_name);

-- 1.2. 🔗 Script para verificar as colunas e relações chave (Multi-Tenant):
SELECT
    '1.2 - Verificação de Colunas Multi-Tenant' AS teste,
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE
    (table_name = 'Empresas' AND column_name = 'contabilidade_id') OR
    (table_name = 'profiles' AND column_name = 'contabilidade_id') OR
    (table_name = 'profiles' AND column_name = 'id' AND data_type = 'uuid');

-- =====================================================================
-- PARTE 2: AUDITORIA DA SEGURANÇA MULTI-TENANT (RLS)
-- =====================================================================
-- Esta é a auditoria mais importante. Vamos verificar se as "paredes" 
-- de segurança entre os seus clientes estão de pé.

-- 2.1. 🔒 Script para verificar se a RLS está ATIVA nas tabelas:
SELECT
    '2.1 - Status da Row Level Security (RLS)' AS teste,
    c.relname AS table_name,
    c.relrowsecurity AS rls_ativada
FROM pg_catalog.pg_class c
JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
AND c.relname IN ('Empresas', 'ControlesMensais', 'Documentos', 'TarefasControle');

-- 2.2. 🛡️ Script para listar as políticas de segurança aplicadas:
SELECT
    '2.2 - Políticas de Segurança Ativas' AS teste,
    schemaname,
    tablename,
    policyname,
    cmd AS tipo_comando, -- SELECT, INSERT, UPDATE, DELETE, ALL
    qual AS regra_aplicada -- A condição da política
FROM pg_policies
WHERE tablename IN ('Empresas', 'ControlesMensais', 'Documentos', 'TarefasControle');

-- =====================================================================
-- PARTE 3: VERIFICAÇÃO DA INTEGRIDADE DOS DADOS
-- =====================================================================
-- Agora, vamos inspecionar os dados em si para garantir que estão 
-- corretamente ligados.

-- 3.1. 🏢 Script para verificar se as contabilidades foram inseridas:
SELECT
    '3.1 - Contabilidades Registadas' AS teste,
    id, 
    nome_contabilidade, 
    cnpj 
FROM public."Contabilidades";

-- 3.2. 🤝 Script para verificar a ligação entre Utilizadores e Contabilidades:
SELECT
    '3.2 - Relação Utilizadores-Contabilidades' AS teste,
    u.id AS user_id,
    u.email,
    p.contabilidade_id,
    c.nome_contabilidade
FROM auth.users u
LEFT JOIN public.profiles p ON u.id = p.id
LEFT JOIN public."Contabilidades" c ON p.contabilidade_id = c.id
ORDER BY u.created_at;

-- 3.3. 📈 Script para verificar a ligação entre Empresas e Contabilidades:
SELECT
    '3.3a - Empresas por Contabilidade' AS teste,
    c.nome_contabilidade,
    COUNT(e.id) AS numero_de_empresas_associadas
FROM public."Contabilidades" c
LEFT JOIN public."Empresas" e ON c.id = e.contabilidade_id
GROUP BY c.nome_contabilidade;

-- Verificação de empresas "órfãs" (não ligadas a nenhuma contabilidade)
SELECT
    '3.3b - Empresas Órfãs (SEM contabilidade)' AS teste,
    id, 
    nome 
FROM public."Empresas" 
WHERE contabilidade_id IS NULL;

-- =====================================================================
-- RESUMO DA VALIDAÇÃO
-- =====================================================================
-- Se todos os scripts executarem e os resultados forem os esperados, 
-- especialmente os da Parte 2 (Auditoria de Segurança) e o 3.2 
-- (Ligação Utilizador-Contabilidade), pode ter uma excelente confiança 
-- de que a sua plataforma está corretamente configurada para operar 
-- de forma segura e multi-tenant.
--
-- Qualquer resultado inesperado é um ponto de atenção que deve ser 
-- corrigido antes de avançar.
-- =====================================================================