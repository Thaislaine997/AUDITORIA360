# 🚀 AUDITORIA360 v1.0 - Deployment & Usage Guide

## 📋 Overview

This implementation delivers the core functionality specified in the problem statement:

- **Funcionalidade 4:** Base de Conhecimento Inteligente ("Biblioteca Viva")
- **Funcionalidade 2:** Motor de Auditoria da Folha de Pagamento ("Robô Auditor")

## 🛠 Installation & Setup

### 1. Install Dependencies

```bash
cd /home/runner/work/AUDITORIA360/AUDITORIA360

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install core dependencies
pip install fastapi uvicorn sqlalchemy python-multipart python-dotenv psycopg2-binary
```

### 2. Database Setup

```bash
# Run the database migration script
psql -U your_user -d your_database -f data_base/migrations/001_create_v1_0_tables.sql

# Or if using SQLite for development:
sqlite3 auditoria360.db < data_base/migrations/001_create_v1_0_tables.sql
```

### 3. Start the Backend API

```bash
cd portal_demandas
python api.py

# Or using uvicorn directly:
uvicorn api:app --host 0.0.0.0 --port 8001 --reload
```

The API will be available at: `http://localhost:8001`

### 4. Start the Frontend

```bash
cd src/frontend
npm install
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## 🧪 API Usage Examples

### 1. CCT PDF Extraction (Funcionalidade 4)

```bash
# Upload and process a CCT PDF with AI
curl -X POST "http://localhost:8001/v1/legislacao/extrair-pdf" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "arquivo_pdf=@cct_comerciarios.pdf"

# Response includes structured data extracted by AI:
{
  "documento_id": 123,
  "dados_extraidos": {
    "tipo_documento": "cct",
    "piso_salarial": 1985.00,
    "beneficios": [
      {"nome": "Vale Refeição", "valor": 25.00},
      {"nome": "Auxílio Creche", "valor": 150.00}
    ],
    "vigencia_inicio": "2024-01-01",
    "vigencia_fim": "2024-12-31"
  },
  "confidence_score": 0.92,
  "sugestoes_validacao": [
    "Verificar se o piso salarial está atualizado",
    "Confirmar vigência"
  ]
}
```

### 2. Official Sources Monitoring (Funcionalidade 4)

```bash
# Run the monitoring robot to check for new CCTs
curl -X POST "http://localhost:8001/v1/jobs/monitorar-mediador" \
  -H "accept: application/json"

# Response shows monitoring results:
{
  "status": "Monitorização concluída com sucesso",
  "estatisticas": {
    "sindicatos_verificados": 3,
    "novas_ccts_encontradas": 1
  },
  "novidades": ["Sindicato dos Comerciários de São Paulo"],
  "detalhes_ccts": [
    {
      "sindicato_nome": "Sindicato dos Comerciários de São Paulo",
      "numero_registro": "MTE-456789",
      "link_documento": "https://mediador.mte.gov.br/documento/cct/456789.pdf"
    }
  ]
}
```

### 3. Payroll Auditing (Funcionalidade 2)

```bash
# Upload payroll PDF for intelligent auditing
curl -X POST "http://localhost:8001/v1/folha/auditar?empresa_id=1&mes=11&ano=2024" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "arquivo_pdf=@folha_pagamento_nov_2024.pdf"

# Response includes comprehensive audit results:
{
  "id": 456,
  "empresa_id": 1,
  "total_funcionarios": 25,
  "total_divergencias": 3,
  "status_processamento": "CONCLUIDO",
  "divergencias": [
    {
      "nome_funcionario": "João Silva",
      "tipo_divergencia": "ALERTA",
      "descricao_divergencia": "Salário base (R$ 1,800.00) está abaixo do piso da CCT",
      "valor_encontrado": "R$ 1,800.00",
      "valor_esperado": "R$ 1,985.00",
      "campo_afetado": "salario_base"
    }
  ]
}
```

### 4. CCT Management

```bash
# List all CCTs with intelligent filtering
curl "http://localhost:8001/v1/cct?vigente=true&search_text=comerciários"

# Response includes statistics and search results:
{
  "ccts": [...],
  "total": 15,
  "ativas": 12,
  "expiradas": 3,
  "expirando_30_dias": 2
}
```

## 🎨 Frontend Usage

### CCT Management Page (`/cct`)

1. **Smart Search & Filtering:**
   - Search by syndicate name, MTE registry number
   - Filter by validity status (Active, Expired, Expiring Soon)
   - Filter by specific syndicate

2. **AI-Powered Upload:**
   - Drag & drop PDF files
   - Automatic processing with Document AI
   - Validation form with extracted data
   - Confidence scoring and suggestions

3. **Digital Library:**
   - Visual status indicators
   - Detailed CCT information
   - Link to official documents

### Payroll Audit Page (`/payroll`)

1. **Context Configuration:**
   - Select company and period (month/year)
   - Automatic CCT rule loading

2. **Intelligent Processing:**
   - Drag & drop payroll PDFs
   - Real-time processing progress
   - AI extraction with structured data

3. **Comprehensive Results:**
   - Employee-by-employee audit
   - Divergence classification (Alert, Warning, Info)
   - Interactive results table
   - Actionable recommendations

## 🏗 Architecture

### Database Schema

- **Sindicatos:** Labor unions with CNPJ for monitoring
- **ConvencoesColetivas:** CCTs with JSONB data for AI-extracted rules
- **ProcessamentosFolha:** Payroll audit results with divergences
- **DocumentosLegislacao:** General legislation management
- **NotificacoesValidacao:** Monitoring alerts system

### AI Services

- **DocumentAIClient:** Processes PDFs and extracts structured data
- **MediadorScraper:** Monitors official sources for new documents

### API Endpoints

- `/v1/legislacao/extrair-pdf`: AI-powered PDF processing
- `/v1/jobs/monitorar-mediador`: Automated monitoring robot
- `/v1/folha/auditar`: Comprehensive payroll auditing
- `/v1/cct/*`: Full CCT management suite

## 📊 Key Features Implemented

✅ **"Robô Bibliotecário"** - Intelligent PDF processing with AI  
✅ **"Robô Vigia"** - Automated monitoring of official sources  
✅ **"Motor de Auditoria"** - Comprehensive payroll vs CCT validation  
✅ **Digital Knowledge Base** - Searchable CCT library  
✅ **React Frontend** - Modern, responsive UI components  
✅ **Comprehensive Testing** - Validation scripts and examples  

## 🔧 Production Considerations

1. **AI Integration:** Replace mock services with real AI providers (Google Document AI, OpenAI, etc.)
2. **Database:** Configure PostgreSQL with proper indexing and backup
3. **Security:** Add authentication, authorization, and data validation
4. **Monitoring:** Set up logging, metrics, and alerting
5. **Deployment:** Use Docker containers with orchestration (Kubernetes)

## 📞 Support

For technical support or questions about the implementation, refer to the comprehensive code documentation and test files included in the repository.