# Architecture Decision Records (ADRs)

Este diretório contém os Registros de Decisões de Arquitetura (ADRs) do projeto AUDITORIA360.

## O que são ADRs?

Architecture Decision Records (ADRs) são documentos que capturam as decisões importantes de arquitetura tomadas durante o desenvolvimento do projeto, incluindo o contexto, a decisão e suas consequências.

## Formato

Cada ADR segue o template:

1. **Contexto**: A situação que levou à necessidade da decisão
2. **Decisão**: A mudança que estamos propondo ou fizemos
3. **Consequências**: O que se torna mais fácil ou mais difícil com esta decisão

## Lista de ADRs

| Número | Título | Status |
|--------|--------|--------|
| [001](001-escolha-da-arquitetura-de-dados-descentralizada-com-duckdb.md) | Escolha da Arquitetura de Dados Descentralizada com DuckDB | Aceito |
| [002](002-implementacao-sistema-mcp-multi-agente.md) | Implementação do Sistema MCP Multi-Agente | Aceito |
| [003](003-estrategia-api-as-a-product.md) | Estratégia API-as-a-Product para Ecossistema de Parcerias | Proposto |

## Status dos ADRs

- **Proposto**: A decisão está sendo considerada
- **Aceito**: A decisão foi aceita e implementada
- **Rejeitado**: A decisão foi rejeitada
- **Superseded**: A decisão foi substituída por uma nova decisão
- **Deprecated**: A decisão não é mais relevante

## Criando um novo ADR

1. Crie um novo arquivo seguindo o padrão: `XXX-titulo-da-decisao.md`
2. Use o próximo número sequencial
3. Siga o template estabelecido
4. Adicione à tabela acima

## Princípios

- As decisões são documentadas assim que são tomadas
- O contexto é tão importante quanto a decisão
- As consequências incluem tanto benefícios quanto limitações
- ADRs são imutáveis - novas decisões criam novos ADRs