# AUDITORIA360 - Examples Directory

Este diretório contém exemplos práticos de uso das APIs e funcionalidades do sistema AUDITORIA360.

## 📋 Exemplos Disponíveis

### 🤖 Inteligência Artificial
- **[ai_chatbot_example.py](ai_chatbot_example.py)** - Exemplo de integração com chatbot de IA

### 🔐 Autenticação e Segurança
- **[api_authentication_example.py](api_authentication_example.py)** - Como implementar autenticação nas APIs

### 📄 Processamento de Documentos
- **[api_documents_example.py](api_documents_example.py)** - Processamento e análise de documentos
- **[ocr_paddle_example.py](ocr_paddle_example.py)** - OCR usando PaddleOCR

### 💼 Folha de Pagamento
- **[api_payroll_example.py](api_payroll_example.py)** - Gestão de folha de pagamento via API

### 🗄️ Banco de Dados
- **[duckdb_example.py](duckdb_example.py)** - Análise de dados com DuckDB

### ☁️ Armazenamento em Nuvem
- **[r2_upload_download_example.py](r2_upload_download_example.py)** - Upload/download com Cloudflare R2

### 🔄 Workflow Completo
- **[complete_workflow_example.py](complete_workflow_example.py)** - Exemplo de workflow completo do sistema

## 🚀 Como Usar

### Pré-requisitos:
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações
```

### Executar Exemplos:
```bash
# Exemplo básico de autenticação
python examples/api_authentication_example.py

# Exemplo de processamento de documentos
python examples/api_documents_example.py

# Workflow completo
python examples/complete_workflow_example.py
```

## 📖 Diferença entre Examples e Demos

### 📁 Examples (este diretório):
- Exemplos específicos de uso de APIs
- Foco em funcionalidades individuais
- Código simples e didático
- Para desenvolvedores iniciantes

### 🎭 Demos (../demos/):
- Demonstrações completas do sistema
- Integração de múltiplas funcionalidades
- Cenários mais complexos
- Para demonstrações técnicas e vendas

## 🔗 Links Relacionados

- **[Demos](../demos/)** - Demonstrações completas do sistema
- **[Documentação](../docs/)** - Documentação técnica completa
- **[API Documentation](../api/)** - Endpoints e estrutura da API
- **[Tests](../tests/)** - Testes automatizados do sistema

## 🆘 Precisa de Ajuda?

1. Consulte a **[documentação central](../docs/README.md)**
2. Execute os **[testes](../tests/)** para verificar configuração
3. Verifique os **[logs do sistema](../logs/)**
4. Contate a equipe: dev@auditoria360.com.br

---

**Mantido por**: AUDITORIA360 Team  
**Última atualização**: $(date)