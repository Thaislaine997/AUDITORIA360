# 🧪 EXEMPLOS - CÓDIGO DE DEMONSTRAÇÃO APENAS

> ⚠️  **AVISO: ESTES SÃO ARQUIVOS DE EXEMPLO PARA FINS DE DEMONSTRAÇÃO APENAS**
> 
> ⚠️  **NÃO USAR EM AMBIENTES DE PRODUÇÃO**
> 
> ⚠️  **Para deployment em produção, use a aplicação principal em `src/`**

# Exemplos de Uso da Stack AUDITORIA360

Esta pasta contém exemplos práticos e abrangentes demonstrando como usar todos os principais módulos do sistema AUDITORIA360.

## 📚 Índice de Exemplos

### 🔐 Autenticação e Segurança

- **[api_authentication_example.py](api_authentication_example.py)** - Autenticação, gestão de usuários e permissões
  - Login e logout de usuários
  - Criação e gestão de usuários
  - Sistema de permissões granulares
  - Proteção de rotas com JWT
  - Tratamento de erros de autenticação

### 💼 Folha de Pagamento

- **[api_payroll_example.py](api_payroll_example.py)** - Gestão completa de folha de pagamento
  - Gestão de funcionários (CRUD)
  - Cálculos de folha automatizados
  - Geração de relatórios sintéticos e analíticos
  - Importação de dados via CSV/Excel
  - Validação de folha de pagamento

### 📁 Gestão de Documentos

- **[api_documents_example.py](api_documents_example.py)** - Gestão completa de documentos
  - Upload para Cloudflare R2
  - Listagem e busca avançada
  - Download de documentos
  - Processamento OCR automático
  - Versionamento de documentos

### 🤖 Inteligência Artificial e Chatbot

- **[ai_chatbot_example.py](ai_chatbot_example.py)** - IA e assistente virtual
  - Conversa com chatbot especializado
  - Busca na base de conhecimento
  - Recomendações personalizadas
  - Análise de documentos com IA
  - Treinamento e feedback do chatbot

### 📊 Analytics e Relatórios

- **[duckdb_example.py](duckdb_example.py)** - Analytics avançados com DuckDB
  - Análise departamental de custos
  - Tendências salariais com gráficos
  - Verificações de compliance fiscal
  - Análise detalhada de custos
  - Relatórios executivos
  - Testes de performance de queries

### 🔍 Processamento OCR

- **[ocr_paddle_example.py](ocr_paddle_example.py)** - OCR avançado com PaddleOCR
  - Processamento de imagens e PDFs
  - Pré-processamento para melhor precisão
  - Extração de dados estruturados
  - Suporte a múltiplos idiomas
  - Comparação de performance

### ☁️ Armazenamento em Nuvem

- **[r2_upload_download_example.py](r2_upload_download_example.py)** - Integração com Cloudflare R2
  - Upload e download de arquivos
  - Gestão de buckets
  - Controle de permissões
  - Backup e sincronização

### 🔄 Workflows Completos

- **[complete_workflow_example.py](complete_workflow_example.py)** - Fluxos de trabalho integrados
  - Auditoria completa de folha de pagamento
  - Verificação de compliance com CCT
  - Monitoramento em tempo real
  - Workflows integrados entre módulos

## 🚀 Como Executar os Exemplos

### Pré-requisitos

1. **Instalar dependências:**

```bash
pip install -r requirements.txt
```

2. **Configurar variáveis de ambiente:**

```bash
cp .env.example .env
# Editar .env com suas credenciais
```

3. **Iniciar a API:**

```bash
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

### Execução Individual

Cada exemplo pode ser executado independentemente:

```bash
# Exemplo de autenticação
python examples/api_authentication_example.py

# Exemplo de folha de pagamento
python examples/api_payroll_example.py

# Exemplo de documentos
python examples/api_documents_example.py

# Exemplo de IA/Chatbot
python examples/ai_chatbot_example.py

# Exemplo de analytics
python examples/duckdb_example.py

# Exemplo de OCR (com arquivo específico)
python examples/ocr_paddle_example.py caminho/para/imagem.png

# Exemplo de storage
python examples/r2_upload_download_example.py

# Workflow completo
python examples/complete_workflow_example.py
```

### Execução em Lote

Para executar todos os exemplos sequencialmente:

```bash
# Executar todos os exemplos
for script in examples/*.py; do
    echo "Executando $script..."
    python "$script"
    echo "---"
done
```

## 📋 Cenários de Uso por Perfil

### 👤 **Usuário Final (RH/Contador)**

1. **[api_authentication_example.py](api_authentication_example.py)** - Login e acesso ao sistema
2. **[api_payroll_example.py](api_payroll_example.py)** - Processamento de folha
3. **[api_documents_example.py](api_documents_example.py)** - Gestão de documentos

### 👨‍💻 **Desenvolvedor**

1. **[complete_workflow_example.py](complete_workflow_example.py)** - Entendimento do fluxo completo
2. **[duckdb_example.py](duckdb_example.py)** - Implementação de analytics
3. **[ai_chatbot_example.py](ai_chatbot_example.py)** - Integração com IA

### 🔍 **Auditor**

1. **[complete_workflow_example.py](complete_workflow_example.py)** - Processo de auditoria
2. **[api_documents_example.py](api_documents_example.py)** - Análise de documentos
3. **[duckdb_example.py](duckdb_example.py)** - Relatórios de compliance

### 👔 **Gestor/Administrador**

1. **[api_authentication_example.py](api_authentication_example.py)** - Gestão de usuários
2. **[duckdb_example.py](duckdb_example.py)** - Relatórios executivos
3. **[complete_workflow_example.py](complete_workflow_example.py)** - Visão geral do sistema

## 🛠️ Configuração Avançada

### Configuração de Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Executar testes
pytest tests/ -v

# Executar com cobertura
pytest --cov=src --cov-report=html
```

### Configuração de Produção

```bash
# Configurar variáveis de ambiente de produção
export DATABASE_URL="postgresql://..."
export R2_ENDPOINT_URL="https://..."
export OPENAI_API_KEY="sk-..."

# Executar em modo produção
uvicorn api.index:app --host 0.0.0.0 --port 8000
```

## 📊 Métricas de Performance

Os exemplos incluem medições de performance para ajudar na otimização:

- **OCR**: Tempo de processamento por página
- **Analytics**: Tempo de execução de queries complexas
- **APIs**: Tempo de resposta de endpoints
- **Upload**: Velocidade de transferência de arquivos

## 🔧 Solução de Problemas

### Problemas Comuns

1. **Erro de autenticação:**
   - Verificar se a API está rodando
   - Confirmar credenciais no .env

2. **Dependências não encontradas:**
   - Executar `pip install -r requirements.txt`
   - Verificar versão do Python (3.12+)

3. **Erro de conexão com banco:**
   - Verificar DATABASE_URL no .env
   - Confirmar se o banco está acessível

4. **Erro de OCR:**
   - Instalar `paddleocr paddlepaddle`
   - Verificar se a imagem existe

### Logs e Debug

Para ativar logs detalhados:

```bash
export LOG_LEVEL=DEBUG
python examples/nome_do_exemplo.py
```

## 📚 Documentação Relacionada

- **[Documentação Principal](../docs/00-INDICE_PRINCIPAL.md)** - Índice completo
- **[Início Rápido](../docs/01-INICIO_RAPIDO.md)** - Guia para começar
- **[APIs](../docs/tecnico/apis/)** - Documentação das APIs
- **[Módulos](../docs/tecnico/modulos-principais.md)** - Descrição dos módulos

## 🤝 Contribuição

Para adicionar novos exemplos:

1. Criar arquivo no padrão `nome_modulo_example.py`
2. Incluir docstring completa com funcionalidades
3. Adicionar tratamento de erros abrangente
4. Atualizar este README
5. Adicionar testes se aplicável

## ⚡ Próximos Passos

Após executar os exemplos:

1. **Explorar a API interativa:** http://localhost:8000/docs
2. **Consultar documentação completa:** [docs/](../docs/)
3. **Implementar casos de uso específicos** baseados nos exemplos
4. **Contribuir com melhorias** via Pull Requests

---

**AUDITORIA360** - Transformando a gestão de folha de pagamento com exemplos práticos e código de qualidade.
