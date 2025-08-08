-- =====================================================================
-- AUDITORIA360 - VALIDAÇÃO DO SCHEMA DA BASE DE DADOS
-- =====================================================================
-- PARTE 1: Verificação do Schema da Base de Dados
-- Estes scripts verificam se a "planta" da sua base de dados está correta.
-- =====================================================================

-- 1.1. 📜 Script para verificar se todas as tabelas principais existem:

-- Verifica a existência das tabelas no schema 'public'
SELECT
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

-- Resultado Esperado: Uma tabela com duas colunas. A coluna tabela_existe 
-- deve mostrar true para todas as seis tabelas. Se alguma mostrar false, 
-- significa que a tabela não foi criada.