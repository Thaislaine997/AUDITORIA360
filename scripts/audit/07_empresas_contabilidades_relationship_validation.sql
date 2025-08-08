-- =====================================================================
-- AUDITORIA360 - VALIDAÇÃO DA RELAÇÃO EMPRESAS-CONTABILIDADES
-- =====================================================================
-- PARTE 3.3: Verificação da ligação entre Empresas e Contabilidades
-- =====================================================================

-- 3.3. 📈 Script para verificar a ligação entre Empresas e Contabilidades:

-- Conta quantas empresas (clientes) estão associadas a cada contabilidade
SELECT
    c.nome_contabilidade,
    COUNT(e.id) AS numero_de_empresas_associadas
FROM public."Contabilidades" c
LEFT JOIN public."Empresas" e ON c.id = e.contabilidade_id
GROUP BY c.nome_contabilidade;

-- E verifica se existem empresas "órfãs" (não ligadas a nenhuma contabilidade)
SELECT id, nome FROM public."Empresas" WHERE contabilidade_id IS NULL;

-- Resultado Esperado:
-- 
-- O primeiro SELECT deve mostrar uma contagem de empresas para cada contabilidade. 
-- Isto é útil após a migração dos dados.
--
-- O segundo SELECT deve retornar 0 linhas. Se alguma empresa aparecer aqui, 
-- significa que ela foi inserida sem ser associada a uma contabilidade, 
-- o que é um erro de dados.