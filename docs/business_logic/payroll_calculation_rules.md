# Regras de Cálculo da Folha de Pagamento

## Visão Geral
Este documento detalha as regras de negócio implementadas no `payroll_service.py` para os cálculos da folha de pagamento no AUDITORIA360.

## Regras Principais

### 1. Validação de Funcionários
- ID do funcionário deve ser único no sistema
- Funcionário deve estar ativo para participar dos cálculos
- Departamento deve estar cadastrado e aprovado

### 2. Competências de Folha
- Cada competência é única por ano/mês/tipo
- Status deve ser validado antes dos cálculos
- Período deve estar dentro do ano fiscal válido

### 3. Cálculos de Salário

#### 3.1 Salário Bruto
- Base salarial conforme contrato individual
- Adicionais conforme CCT (Convenção Coletiva de Trabalho)
- Horas extras calculadas com percentuais legais

#### 3.2 Deduções Obrigatórias
- **INSS**: Calculado por faixas progressivas conforme tabela oficial
- **IRRF**: Aplicado conforme faixas de renda e dependentes
- **FGTS**: 8% sobre salário base (depositado pelo empregador)

#### 3.3 Benefícios
- Vale-transporte: Limitado a 6% do salário base
- Vale-alimentação: Conforme acordo coletivo
- Plano de saúde: Desconto conforme percentual contratado

### 4. Regras de Férias
- Cálculo baseado em 30 dias para período aquisitivo completo
- 1/3 constitucional sobre o valor das férias
- Validação de períodos disponíveis para gozo

⚠️ **ATENÇÃO**: A função `calculate_vacation_days` atualmente possui uma violação semântica intencional para teste do sistema IAI-C, permitindo valores negativos de dias de férias.

### 5. Processamento em Lotes
- Funcionários processados em lotes de 50 para otimização
- Processamento assíncrono para competências com mais de 100 funcionários
- Cache de resultados por 10 minutos para estatísticas

### 6. Validações de Conformidade
- Verificação de divergências automática
- Validação contra regras da CCT
- Controle de aprovação por supervisor

## Arquitetura de Performance

### Cache Strategy
- Consultas de funcionários: cache de 5 minutos
- Detalhes de competência: cache de 10 minutos
- Estatísticas de folha: cache de 10 minutos

### Otimizações de Banco
- Uso de `joinedload` para evitar problema N+1
- Queries SQL otimizadas para agregações
- Índices otimizados em campos de busca frequente

## Referências Legais
- CLT (Consolidação das Leis do Trabalho)
- CCT específica do setor/região
- Instruções Normativas do MTE
- Regulamentação do eSocial