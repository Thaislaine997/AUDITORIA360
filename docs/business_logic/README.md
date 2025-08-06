# Business Logic Documentation

Esta pasta contém a documentação das regras de negócio críticas do AUDITORIA360, mantida sincronizada com o código fonte.

## Estrutura

- `payroll_calculation_rules.md` - Regras de cálculo da folha de pagamento
- `audit_compliance_rules.md` - Regras de conformidade e auditoria
- `data_validation_rules.md` - Regras de validação de dados

## Filosofia da Documentação como Código

Toda alteração em arquivos críticos de serviços (`src/services/*.py`) deve ser acompanhada pela atualização da documentação correspondente nesta pasta. Esta prática garante que:

1. O conhecimento de negócio seja explícito e versionado
2. A documentação esteja sempre sincronizada com o código
3. Novos membros da equipe tenham acesso ao contexto de negócio

## Validação Automática

O pipeline de CI/CD verifica automaticamente se alterações em serviços críticos são acompanhadas por atualizações na documentação.