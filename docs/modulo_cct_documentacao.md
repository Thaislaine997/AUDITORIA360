# Módulo de Gestão de Convenções Coletivas (CCTs) e Sindicatos

Este módulo implementa a funcionalidade para cadastrar e gerenciar Sindicatos e Convenções Coletivas de Trabalho (CCTs) no sistema AUDITORIA360.

## Visão Geral

O módulo CCT transforma o sistema de uma ferramenta de auditoria passiva para um assistente de compliance ativo, permitindo:

- Cadastro e gestão de sindicatos laborais
- Gestão completa de Convenções Coletivas de Trabalho (CCTs)
- Associação de empresas aos seus sindicatos correspondentes
- Armazenamento flexível de dados extraídos das CCTs
- Segurança multi-tenant com Row Level Security (RLS)

## Estrutura da Base de Dados

### Tabelas Criadas

1. **`Sindicatos`** - Armazena os sindicatos laborais
   - `id` - Chave primária
   - `nome_sindicato` - Nome do sindicato
   - `cnpj` - CNPJ do sindicato (único)
   - `base_territorial` - Área de abrangência geográfica
   - `categoria_representada` - Categoria profissional representada
   - `criado_em` - Data/hora de criação

2. **`ConvencoesColetivas`** - Armazena as CCTs
   - `id` - Chave primária
   - `sindicato_id` - Referência ao sindicato (FK)
   - `numero_registro_mte` - Código único do Sistema Mediador do Governo
   - `vigencia_inicio` - Data de início da vigência
   - `vigencia_fim` - Data de fim da vigência
   - `link_documento_oficial` - URL para o PDF oficial
   - `dados_cct` - Campo JSONB flexível para dados extraídos
   - `criado_em` - Data/hora de criação

3. **Alteração na tabela `Empresas`**
   - `sindicato_id` - Nova coluna para associar empresa ao sindicato (FK)

### Estrutura de Dados JSON (dados_cct)

Exemplo de como os dados são armazenados no campo `dados_cct`:

```json
{
  "resumo_executivo": "Aumento de 8% nos salários, novo piso de R$ 1.850,00 e vale-refeição de R$ 25,00/dia.",
  "pisos_salariais": [
    { "cargo": "Auxiliar Administrativo", "valor": 1850.00 },
    { "cargo": "Técnico", "valor": 2500.00 }
  ],
  "beneficios": {
    "vale_refeicao_dia": 25.00,
    "cesta_basica_mes": 150.00
  },
  "clausulas_importantes": [
    "Cláusula 3ª - Reajuste Salarial",
    "Cláusula 15ª - Benefício Social Familiar"
  ]
}
```

## API Endpoints

### Sindicatos

- **POST** `/cct/sindicatos` - Criar novo sindicato
- **GET** `/cct/sindicatos` - Listar sindicatos
- **GET** `/cct/sindicatos/{id}` - Obter sindicato por ID
- **PUT** `/cct/sindicatos/{id}` - Atualizar sindicato
- **GET** `/cct/sindicatos/{id}/empresas` - Listar empresas do sindicato

### Convenções Coletivas

- **POST** `/cct/` - Criar nova CCT
- **GET** `/cct/` - Listar CCTs
- **GET** `/cct/{id}` - Obter CCT por ID
- **PUT** `/cct/{id}` - Atualizar CCT

### Associações

- **POST** `/cct/empresas/{empresa_id}/sindicato/{sindicato_id}` - Associar empresa ao sindicato

## Exemplos de Uso

### Criar um Sindicato

```json
POST /cct/sindicatos
{
  "nome_sindicato": "Sindicato dos Trabalhadores no Comércio",
  "cnpj": "12.345.678/0001-99",
  "base_territorial": "São Paulo - SP",
  "categoria_representada": "Trabalhadores no Comércio de Bens, Serviços e Turismo"
}
```

### Criar uma CCT

```json
POST /cct/
{
  "sindicato_id": 1,
  "numero_registro_mte": "SP000123/2024",
  "vigencia_inicio": "2024-01-01",
  "vigencia_fim": "2024-12-31",
  "link_documento_oficial": "https://www.gov.br/trabalho/ccts/SP000123-2024.pdf",
  "dados_cct": {
    "resumo_executivo": "Reajuste salarial de 8% e novos benefícios",
    "pisos_salariais": [
      {"cargo": "Vendedor", "valor": 1800.00}
    ]
  }
}
```

### Associar Empresa ao Sindicato

```json
POST /cct/empresas/1/sindicato/1
```

## Segurança

O módulo implementa Row Level Security (RLS) garantindo que:

- Cada contabilidade só pode ver/gerenciar sindicatos associados às suas empresas clientes
- CCTs só são visíveis para contabilidades que têm empresas associadas ao sindicato correspondente
- Isolamento completo de dados entre diferentes contabilidades

## Fluxo de Trabalho Recomendado

1. **Cadastrar Sindicato**: Criar o sindicato relevante para os clientes
2. **Associar Empresas**: Conectar as empresas clientes ao sindicato apropriado
3. **Cadastrar CCT**: Buscar no Sistema Mediador do MTE e cadastrar a CCT
4. **Extrair Dados**: Processar o PDF oficial e extrair informações importantes
5. **Manter Atualizado**: Monitorar vigências e atualizar CCTs conforme necessário

## Instalação e Configuração

1. Execute a migração da base de dados:
   ```bash
   # No editor SQL da Supabase, execute:
   # migrations/007_modulo_cct_sindicatos.sql
   ```

2. Certifique-se de que as variáveis de ambiente estão configuradas:
   ```bash
   SUPABASE_URL=your_supabase_url
   SUPABASE_SERVICE_KEY=your_service_key
   ```

## Testes

Execute os testes do módulo:

```bash
python -m pytest tests/test_cct_module.py -v
```

## Próximos Passos

- Implementar funcionalidade de comparação entre CCTs
- Adicionar notificações automáticas de vencimento
- Integração com APIs governamentais para busca automática
- Dashboard de compliance baseado nas CCTs cadastradas