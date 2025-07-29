# 📚 Notebooks de Análise e Prototipagem - AUDITORIA360

## 📋 Visão Geral

Esta seção contém os notebooks Jupyter utilizados para análise de dados, prototipagem de modelos e demonstração das funcionalidades do sistema AUDITORIA360.

## 📖 Notebooks Disponíveis

### 1. [Exploração e Prototipagem](../../../notebooks/exploracao_e_prototipagem.ipynb)

**Objetivo**: Análise exploratória de dados de folha de pagamento e prototipagem de modelos de machine learning.

**Funcionalidades**:
- ✅ Análise exploratória de dados
- ✅ Detecção de anomalias usando Isolation Forest
- ✅ Segmentação de funcionários com K-Means
- ✅ Visualizações interativas
- ✅ Relatório automático de auditoria

**Pré-requisitos**:
- Python 3.8+
- pandas, numpy, matplotlib, seaborn, scikit-learn
- Dados de folha de pagamento (exemplo incluído)

**Como usar**:
1. Execute as células sequencialmente
2. Ajuste parâmetros conforme necessário
3. Analise os resultados e visualizações

### 2. [Módulo 2: Folha Inteligente](../../../notebooks/modulo_2_folha_inteligente.ipynb)

**Objetivo**: Demonstração completa do processamento de PDFs de folha de pagamento.

**Funcionalidades**:
- ✅ Upload e processamento de PDFs
- ✅ Monitoramento de jobs assíncronos
- ✅ Validação e mapeamento de dados
- ✅ Armazenamento no banco de dados
- ✅ Visualização de resultados

**Pré-requisitos**:
- Python 3.8+
- requests, pandas, streamlit, matplotlib
- API AUDITORIA360 em execução
- Arquivos PDF de folha de pagamento

**Como usar**:
1. Configure as variáveis de ambiente
2. Execute as células sequencialmente
3. Faça upload do arquivo PDF
4. Monitore o processamento
5. Visualize os resultados

## 🛠️ Configuração do Ambiente

### Instalação das Dependências

```bash
# Instalar dependências básicas
pip install -r requirements.txt

# Dependências específicas para notebooks
pip install jupyter notebook ipywidgets
```

### Configuração do Jupyter

```bash
# Iniciar Jupyter Notebook
jupyter notebook

# Ou usar Jupyter Lab
jupyter lab
```

### Variáveis de Ambiente

```bash
# Configurar no arquivo .env
API_BASE_URL=http://localhost:8000
CLIENT_ID=12345
```

## 📊 Estrutura dos Dados

### Dados de Entrada (Folha de Pagamento)

```json
{
  "funcionarios": [
    {
      "nome": "João Silva Santos",
      "cpf": "123.456.789-00",
      "cargo": "Analista",
      "salario_base": 5000.00,
      "horas_extras": 300.00,
      "descontos": 850.00,
      "salario_liquido": 4450.00
    }
  ]
}
```

### Saída de Análise

```json
{
  "validation_summary": {
    "total_records": 100,
    "valid_records": 95,
    "invalid_records": 5,
    "warnings_count": 8
  },
  "anomalies_detected": 10,
  "clusters_identified": 4
}
```

## 🎯 Casos de Uso

### 1. Auditoria Mensal
- Carregar dados da folha do mês
- Executar análise exploratória
- Identificar anomalias e inconsistências
- Gerar relatório de auditoria

### 2. Análise de Tendências
- Comparar dados de múltiplos meses
- Identificar padrões sazonais
- Detectar mudanças estruturais

### 3. Detecção de Fraudes
- Aplicar modelos de machine learning
- Identificar comportamentos suspeitos
- Validar com regras de negócio

### 4. Processamento de PDFs
- Upload automático de extratos
- Extração e validação de dados
- Integração com sistemas existentes

## 📈 Métricas e KPIs

### Métricas de Qualidade
- **Taxa de Validação**: % de registros válidos
- **Taxa de Anomalias**: % de anomalias detectadas
- **Cobertura de Dados**: % de campos preenchidos

### Métricas de Performance
- **Tempo de Processamento**: Tempo médio por arquivo
- **Throughput**: Arquivos processados por hora
- **Taxa de Erro**: % de falhas no processamento

## 🔧 Troubleshooting

### Problemas Comuns

**Erro de Dependências**:
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

**Erro de Conexão com API**:
- Verificar se a API está rodando
- Conferir variáveis de ambiente
- Testar conectividade de rede

**Dados Não Carregando**:
- Verificar formato dos dados
- Conferir permissões de arquivo
- Usar dados de exemplo incluídos

### Logs de Debug

```python
# Habilitar logs detalhados
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Contribuição

### Adicionando Novos Notebooks

1. Criar notebook na pasta `notebooks/`
2. Seguir padrão de nomenclatura: `modulo_X_nome_descritivo.ipynb`
3. Incluir documentação completa
4. Adicionar ao índice desta documentação
5. Testar com dados de exemplo

### Padrões de Código

- **Células de Markdown**: Documentar cada seção
- **Docstrings**: Documentar todas as funções
- **Comentários**: Explicar lógica complexa
- **Visualizações**: Incluir títulos e legendas
- **Tratamento de Erros**: Capturar e explicar erros

## 🔗 Links Relacionados

- [Documentação da API](../apis/api-documentation.md)
- [Guia de Desenvolvimento](../desenvolvimento/dev-guide.md)
- [Arquitetura do Sistema](../arquitetura/visao-geral.md)
- [Schemas de Dados](../banco-dados/schema-bigquery.md)

---

**📅 Última atualização**: Janeiro 2025  
**👨‍💻 Mantido por**: Equipe AUDITORIA360  
**📧 Suporte**: Consulte a documentação técnica