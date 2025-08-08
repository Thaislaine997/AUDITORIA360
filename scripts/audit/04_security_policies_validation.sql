-- =====================================================================
-- AUDITORIA360 - VALIDAÇÃO DE POLÍTICAS DE SEGURANÇA
-- =====================================================================
-- PARTE 2.2: Verificação das políticas de segurança aplicadas
-- =====================================================================

-- 2.2. 🛡️ Script para listar as políticas de segurança aplicadas:

-- Lista todas as políticas de segurança ativas na base de dados
SELECT
    schemaname,
    tablename,
    policyname,
    cmd AS tipo_comando, -- SELECT, INSERT, UPDATE, DELETE, ALL
    qual AS regra_aplicada -- A condição da política
FROM pg_policies
WHERE tablename IN ('Empresas', 'ControlesMensais', 'Documentos', 'TarefasControle');

-- Resultado Esperado: Deve ver a lista das políticas que criámos, como 
-- "Acesso total para administradores de empresas". Verifique a coluna 
-- regra_aplicada para garantir que a lógica auth.get_contabilidade_id() = contabilidade_id 
-- está presente. Isto mostra que as regras corretas estão em vigor.