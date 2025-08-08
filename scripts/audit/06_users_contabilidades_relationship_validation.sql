-- =====================================================================
-- AUDITORIA360 - VALIDAÇÃO DA RELAÇÃO UTILIZADORES-CONTABILIDADES
-- =====================================================================
-- PARTE 3.2: Verificação da ligação entre Utilizadores e Contabilidades
-- =====================================================================

-- 3.2. 🤝 Script para verificar a ligação entre Utilizadores e Contabilidades:

-- Mostra os utilizadores do sistema e a qual contabilidade estão associados
SELECT
    u.id AS user_id,
    u.email,
    p.contabilidade_id,
    c.nome_contabilidade
FROM auth.users u
LEFT JOIN public.profiles p ON u.id = p.id
LEFT JOIN public."Contabilidades" c ON p.contabilidade_id = c.id
ORDER BY u.created_at;

-- Resultado Esperado: Uma lista de todos os seus utilizadores.
--
-- Ação Crítica: Verifique se cada utilizador (especialmente os de teste) 
-- tem um valor na coluna contabilidade_id e nome_contabilidade.
--
-- Ponto de Falha: Se contabilidade_id estiver NULL para um utilizador, 
-- a segurança RLS NÃO FUNCIONARÁ para ele, e ele não conseguirá ver nenhum 
-- dado. Este é o ponto mais comum de erro na configuração.