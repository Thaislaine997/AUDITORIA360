-- =====================================================================
-- AUDITORIA360 - VALIDAÇÃO DE CONTABILIDADES
-- =====================================================================
-- PARTE 3: Verificação da Integridade dos Dados
-- Agora, vamos inspecionar os dados em si para garantir que estão 
-- corretamente ligados.
-- =====================================================================

-- 3.1. 🏢 Script para verificar se as contabilidades foram inseridas:

-- Mostra todas as contabilidades registadas
SELECT id, nome_contabilidade, cnpj FROM public."Contabilidades";

-- Resultado Esperado: Deve ver as quatro empresas de contabilidade que inserimos, 
-- cada uma com o seu id, nome e cnpj.