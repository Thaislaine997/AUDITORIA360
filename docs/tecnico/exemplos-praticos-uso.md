# Exemplos Práticos de Uso - AUDITORIA360

Este documento consolida todos os exemplos práticos disponíveis no sistema AUDITORIA360, fornecendo guias detalhados para cada módulo principal.

## 📖 Visão Geral

Os exemplos foram organizados por módulo e complexidade, permitindo que usuários de diferentes níveis técnicos encontrem rapidamente o que precisam:

- **Básicos**: Funcionalidades essenciais de cada módulo
- **Intermediários**: Integração entre módulos
- **Avançados**: Workflows completos e otimizações

## 🎯 Exemplos por Categoria

### 1. 🔐 Autenticação e Segurança

#### Exemplo Básico: Login e Gestão de Usuários

```python
from examples.api_authentication_example import AuditAPI

# Inicializar cliente
api = AuditAPI()

# Fazer login
api.login("usuario@empresa.com", "senha123")

# Obter perfil do usuário
profile = api.get_user_profile()
print(f"Usuário: {profile['name']} - Role: {profile['role']}")
```

**Funcionalidades Demonstradas:**

- ✅ Autenticação via JWT
- ✅ Gestão de perfis de usuário
- ✅ Sistema de permissões granulares
- ✅ Proteção de rotas
- ✅ Tratamento de erros de autenticação

**Arquivo:** `examples/api_authentication_example.py`

---

### 2. 💼 Folha de Pagamento

#### Exemplo Básico: Gestão de Funcionários

```python
from examples.api_payroll_example import PayrollAPI

# Inicializar API com token
api = PayrollAPI(token="seu_token_jwt")

# Criar funcionário
employee_data = {
    "name": "João Silva",
    "cpf": "123.456.789-00",
    "salary": 4500.00,
    "department": "TI"
}
result = api.create_employee(employee_data)
```

#### Exemplo Intermediário: Cálculo de Folha

```python
# Configurar cálculo de folha
calculation_data = {
    "competency": "2024-01",
    "employees": [{
        "employee_id": 1,
        "salary": 4500.00,
        "overtime_hours": 10
    }]
}

# Executar cálculo
result = api.calculate_payroll(calculation_data)
print(f"Total líquido: R$ {result['total_net']}")
```

**Funcionalidades Demonstradas:**

- ✅ CRUD completo de funcionários
- ✅ Cálculos automáticos (INSS, IRRF, FGTS)
- ✅ Geração de relatórios
- ✅ Importação de dados via CSV/Excel
- ✅ Validação de conformidade

**Arquivo:** `examples/api_payroll_example.py`

---

### 3. 📁 Gestão de Documentos

#### Exemplo Básico: Upload e Download

```python
from examples.api_documents_example import DocumentsAPI

api = DocumentsAPI(token="seu_token")

# Upload de documento
result = api.upload_document(
    file_path="/path/to/contract.pdf",
    category="contracts",
    process_ocr=True
)

# Download de documento
api.download_document(document_id=1, download_path="/tmp/downloaded.pdf")
```

#### Exemplo Avançado: Versionamento

```python
# Criar nova versão de documento
api.create_document_version(
    document_id=1,
    new_file_path="/path/to/contract_v2.pdf",
    version_notes="Atualização salarial"
)

# Listar histórico de versões
versions = api.list_document_versions(document_id=1)
```

**Funcionalidades Demonstradas:**

- ✅ Upload para Cloudflare R2
- ✅ Processamento OCR automático
- ✅ Busca avançada por conteúdo
- ✅ Versionamento completo
- ✅ Controle de permissões

**Arquivo:** `examples/api_documents_example.py`

---

### 4. 🤖 Inteligência Artificial e Chatbot

#### Exemplo Básico: Conversa com Chatbot

```python
from examples.ai_chatbot_example import ChatbotAPI

api = ChatbotAPI(token="seu_token")

# Fazer pergunta ao chatbot
response = api.chat("Como calcular férias?")
print(f"Resposta: {response['response']}")
```

#### Exemplo Intermediário: Análise de Documentos

```python
# Analisar documento com IA
analysis = api.analyze_document(
    document_id=1,
    analysis_type="payroll_compliance"
)

print(f"Score de conformidade: {analysis['compliance_score']}")
```

#### Exemplo Avançado: Recomendações Personalizadas

```python
# Obter recomendações baseadas no contexto
context = {
    "user_role": "hr_manager",
    "company_size": "medium",
    "current_issues": ["high_turnover", "payroll_errors"]
}

recommendations = api.get_recommendations(context)
```

**Funcionalidades Demonstradas:**

- ✅ Chatbot especializado em RH/Contabilidade
- ✅ Busca inteligente na base de conhecimento
- ✅ Análise automatizada de documentos
- ✅ Recomendações personalizadas
- ✅ Aprendizado contínuo

**Arquivo:** `examples/ai_chatbot_example.py`

---

### 5. 📊 Analytics e Relatórios

#### Exemplo Básico: Análise Departamental

```python
from examples.duckdb_example import PayrollAnalytics

# Inicializar analytics
analytics = PayrollAnalytics()

# Análise por departamento
resultado = analytics.analise_departamental()
print(resultado)
```

#### Exemplo Intermediário: Tendências Salariais

```python
# Gerar gráfico de tendências
tendencias = analytics.tendencia_salarial()

# Análise de compliance fiscal
compliance = analytics.analise_compliance()
```

#### Exemplo Avançado: Relatório Executivo

```python
# Gerar relatório executivo completo
relatorio = analytics.relatorio_executivo()
print(f"Funcionários ativos: {relatorio['metricas']['total_funcionarios_ativos']}")
```

**Funcionalidades Demonstradas:**

- ✅ Queries SQL otimizadas com DuckDB
- ✅ Visualizações com matplotlib/seaborn
- ✅ Análises de compliance automáticas
- ✅ Relatórios executivos
- ✅ Testes de performance

**Arquivo:** `examples/duckdb_example.py`

---

### 6. 🔍 Processamento OCR

#### Exemplo Básico: OCR de Imagem

```python
from examples.ocr_paddle_example import DocumentOCR

# Inicializar OCR
ocr = DocumentOCR(lang="pt")

# Processar imagem
result = ocr.extract_text_from_image("/path/to/image.png")
print(f"Texto extraído: {result['text']}")
```

#### Exemplo Intermediário: OCR de PDF

```python
# Processar PDF completo
pdf_result = ocr.extract_text_from_pdf("/path/to/document.pdf")
print(f"Páginas processadas: {pdf_result['pages_processed']}")
```

#### Exemplo Avançado: Extração Estruturada

```python
# Extrair dados específicos de demonstrativo
structured_data = ocr.extract_structured_data(
    text=result['text'],
    document_type="payroll"
)
print(f"Nome: {structured_data.get('nome')}")
print(f"Salário: {structured_data.get('salario_base')}")
```

**Funcionalidades Demonstradas:**

- ✅ OCR multi-idioma com PaddleOCR
- ✅ Pré-processamento de imagens
- ✅ Processamento de PDFs
- ✅ Extração de dados estruturados
- ✅ Otimização de performance

**Arquivo:** `examples/ocr_paddle_example.py`

---

### 7. 🔄 Workflows Completos

#### Exemplo: Auditoria Completa de Folha

```python
from examples.complete_workflow_example import AuditoriaFlowManager

# Inicializar workflow
manager = AuditoriaFlowManager()

# 1. Autenticar
manager.authenticate("auditor@empresa.com", "senha")

# 2. Configurar auditoria
audit_config = {
    "audit_type": "payroll_compliance",
    "scope": "full_organization",
    "period": {"start_date": "2024-01-01", "end_date": "2024-03-31"}
}

# 3. Executar workflow completo
audit_id = manager.start_audit_process(audit_config)
findings = manager.generate_audit_findings(audit_id)
```

**Funcionalidades Demonstradas:**

- ✅ Workflow end-to-end de auditoria
- ✅ Verificação de compliance com CCT
- ✅ Monitoramento em tempo real
- ✅ Integração entre todos os módulos
- ✅ Geração de relatórios automáticos

**Arquivo:** `examples/complete_workflow_example.py`

---

## 🚀 Guia de Execução

### Pré-requisitos

1. **Ambiente Python configurado:**

```bash
python --version  # 3.12+
pip install -r requirements.txt
```

2. **API rodando:**

```bash
uvicorn api.index:app --reload --port 8000
```

3. **Variáveis de ambiente configuradas:**

```bash
# .env
DATABASE_URL=postgresql://...
R2_ACCESS_KEY_ID=...
OPENAI_API_KEY=...
```

### Execução dos Exemplos

#### Execução Individual

```bash
# Executar exemplo específico
python examples/api_authentication_example.py

# OCR com arquivo específico
python examples/ocr_paddle_example.py /path/to/image.png
```

#### Execução em Lote

```bash
# Executar todos os exemplos
for script in examples/*.py; do
    echo "Executando $script..."
    python "$script"
done
```

#### Execução com Debug

```bash
# Ativar logs detalhados
export LOG_LEVEL=DEBUG
python examples/nome_do_exemplo.py
```

---

## 📋 Casos de Uso por Perfil

### 👤 **Usuário Final (RH/Contador)**

**Cenário:** Processamento mensal de folha de pagamento

1. **Login no sistema**

   ```bash
   python examples/api_authentication_example.py
   ```

2. **Importar dados de funcionários**

   ```bash
   python examples/api_payroll_example.py
   # Foco: example_data_import()
   ```

3. **Calcular folha e gerar relatórios**

   ```bash
   python examples/api_payroll_example.py
   # Foco: example_payroll_calculation()
   ```

4. **Upload de documentos necessários**
   ```bash
   python examples/api_documents_example.py
   # Foco: example_document_upload()
   ```

### 👨‍💻 **Desenvolvedor**

**Cenário:** Implementação de nova funcionalidade

1. **Entender arquitetura completa**

   ```bash
   python examples/complete_workflow_example.py
   ```

2. **Estudar integração com analytics**

   ```bash
   python examples/duckdb_example.py
   ```

3. **Implementar recursos de IA**
   ```bash
   python examples/ai_chatbot_example.py
   ```

### 🔍 **Auditor**

**Cenário:** Auditoria trimestral de compliance

1. **Executar workflow de auditoria completo**

   ```bash
   python examples/complete_workflow_example.py
   # Foco: example_complete_payroll_audit()
   ```

2. **Analisar documentos submetidos**

   ```bash
   python examples/api_documents_example.py
   # Foco: example_document_processing()
   ```

3. **Gerar relatórios de conformidade**
   ```bash
   python examples/duckdb_example.py
   # Foco: analise_compliance()
   ```

### 👔 **Gestor/Administrador**

**Cenário:** Visão estratégica e gestão de usuários

1. **Gerenciar usuários e permissões**

   ```bash
   python examples/api_authentication_example.py
   # Foco: example_user_management()
   ```

2. **Acompanhar métricas executivas**

   ```bash
   python examples/duckdb_example.py
   # Foco: relatorio_executivo()
   ```

3. **Monitorar sistema em tempo real**
   ```bash
   python examples/complete_workflow_example.py
   # Foco: example_realtime_monitoring()
   ```

---

## 🛠️ Personalização e Extensão

### Criando Novos Exemplos

1. **Estrutura básica:**

```python
"""
Exemplo de [MÓDULO] do AUDITORIA360.

Este exemplo demonstra:
- Funcionalidade 1
- Funcionalidade 2
- Funcionalidade 3

Requer: dependencia1, dependencia2
"""

def example_basic_functionality():
    """Exemplo básico da funcionalidade."""
    pass

def main():
    """Função principal com todos os exemplos."""
    print("EXEMPLOS DE USO - [MÓDULO] AUDITORIA360")
    print("=" * 50)

    try:
        example_basic_functionality()
        print("\n✅ Todos os exemplos executados com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")

if __name__ == "__main__":
    main()
```

2. **Padrões a seguir:**
   - Docstrings detalhadas
   - Tratamento de erros robusto
   - Logs informativos com emojis
   - Validação de pré-requisitos
   - Comentários explicativos

3. **Testes incluídos:**

```python
def test_example_functionality():
    """Teste da funcionalidade do exemplo."""
    # Implementar testes básicos
    assert True
```

### Configuração Avançada

#### Performance Tuning

```python
# Configurações para produção
import os
os.environ["DUCKDB_THREADS"] = "4"
os.environ["OCR_BATCH_SIZE"] = "10"
```

#### Monitoramento

```python
# Ativar métricas detalhadas
import time
start_time = time.time()
# ... código do exemplo ...
execution_time = time.time() - start_time
print(f"Tempo de execução: {execution_time:.2f}s")
```

---

## 📊 Métricas e Performance

### Benchmarks dos Exemplos

| Exemplo           | Tempo Médio | Memória | Dependências               |
| ----------------- | ----------- | ------- | -------------------------- |
| Authentication    | 0.5s        | 15MB    | requests                   |
| Payroll           | 2.1s        | 45MB    | requests, pandas           |
| Documents         | 1.8s        | 35MB    | requests                   |
| AI/Chatbot        | 3.2s        | 120MB   | requests, openai           |
| Analytics         | 4.5s        | 85MB    | duckdb, pandas, matplotlib |
| OCR               | 8.3s        | 200MB   | paddleocr, opencv          |
| Complete Workflow | 15.2s       | 250MB   | todas                      |

### Otimizações Implementadas

- **Cache de resultados** para queries frequentes
- **Processamento paralelo** para uploads múltiplos
- **Lazy loading** para dependências pesadas
- **Connection pooling** para APIs
- **Compressão** para transferência de dados

---

## 🤝 Contribuição

### Como Contribuir

1. **Fork** do repositório
2. **Criar branch** para nova funcionalidade
3. **Implementar** exemplo seguindo padrões
4. **Adicionar testes** se aplicável
5. **Atualizar documentação**
6. **Submeter Pull Request**

### Checklist para Novos Exemplos

- [ ] Docstring completa com funcionalidades
- [ ] Tratamento de erros robusto
- [ ] Logs informativos
- [ ] Validação de pré-requisitos
- [ ] Exemplos básicos e avançados
- [ ] Documentação atualizada
- [ ] Testes básicos incluídos

---

## 📚 Recursos Adicionais

### Documentação Relacionada

- **[Índice Principal](00-INDICE_PRINCIPAL.md)** - Navegação completa
- **[Início Rápido](01-INICIO_RAPIDO.md)** - Guia para começar
- **[APIs](tecnico/apis/)** - Documentação das APIs
- **[Módulos](tecnico/modulos-principais.md)** - Descrição dos módulos

### Links Úteis

- **API Interativa:** http://localhost:8000/docs
- **Código Fonte:** [GitHub Repository](https://github.com/empresa/auditoria360)
- **Issues:** [GitHub Issues](https://github.com/empresa/auditoria360/issues)

### Suporte

- **Email:** suporte@auditoria360.com
- **Chat:** Canal #suporte no Slack
- **Documentação:** Portal de ajuda online

---

**AUDITORIA360** - Exemplos práticos para transformar a gestão de folha de pagamento com tecnologia avançada.
