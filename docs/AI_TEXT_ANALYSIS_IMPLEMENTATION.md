# AI-Powered Text Analysis Implementation

## Overview
This implementation adds AI-powered text analysis capabilities to AUDITORIA360, specifically for extracting legal parameters from documents. The system creates a processing pipeline that:

1. **PDF Processing**: Extracts text from uploaded PDF documents
2. **AI Analysis**: Uses Google Gemini to extract structured legal parameters
3. **Data Storage**: Stores extracted parameters in a structured database format

## Files Created/Modified

### Database Migrations
- `migrations/004_criar_tabela_documentos.sql` - Creates the Documentos table for storing document metadata and extracted text
- `migrations/003_criar_tabela_parametros_legais.sql` - Creates the ParametrosLegais table for storing structured legal parameters

### Supabase Edge Functions
- `supabase/functions/processar-pdf/index.ts` - Processes PDF files and extracts text
- `supabase/functions/analisar-texto-com-ia/index.ts` - Analyzes extracted text with AI and stores parameters

### Configuration & Documentation
- `supabase/config.toml` - Basic Supabase configuration
- `supabase/README.md` - Setup and deployment instructions
- `scripts/deploy-functions.sh` - Automated deployment script
- `tests/test-ai-analysis.js` - Testing utilities
- `.env.example` - Updated with required environment variables

## Setup Instructions

### 1. Database Setup
Execute these migrations in your Supabase SQL Editor in order:
```sql
-- First run: migrations/004_criar_tabela_documentos.sql
-- Then run: migrations/003_criar_tabela_parametros_legais.sql
```

### 2. Environment Variables
Set the following in your Supabase project:
```bash
# Get Gemini API key from https://aistudio.google.com/app/apikey
npx supabase secrets set GEMINI_API_KEY=your_api_key_here
```

### 3. Deploy Functions
```bash
chmod +x scripts/deploy-functions.sh
./scripts/deploy-functions.sh
```

Or manually:
```bash
npx supabase functions deploy processar-pdf --no-verify-jwt
npx supabase functions deploy analisar-texto-com-ia --no-verify-jwt
```

## API Usage

### Upload and Process PDF
```bash
curl -X POST \
  'https://your-project.supabase.co/functions/v1/processar-pdf' \
  -H 'Authorization: Bearer YOUR_SUPABASE_ANON_KEY' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@document.pdf'
```

### Response
```json
{
  "message": "Documento document.pdf processado e enviado para análise de IA.",
  "documentoId": 123,
  "textoExtraido": "PORTARIA Nº 123/2024..."
}
```

## Data Flow

1. **Upload**: Client uploads PDF via `processar-pdf` function
2. **Extract**: Function extracts text and saves to `Documentos` table
3. **Analyze**: Function calls `analisar-texto-com-ia` with extracted text
4. **AI Processing**: Gemini AI analyzes text and extracts legal parameters
5. **Store**: Parameters are saved to `ParametrosLegais` table with references

## Database Schema

### Documentos
- `id`: Primary key
- `nome`: Original filename
- `texto_extraido`: Extracted text content
- `status`: Processing status (PROCESSANDO, CONCLUIDO, ERRO)

### ParametrosLegais
- `id`: Primary key
- `documento_id`: Foreign key to Documentos
- `nome_parametro`: Parameter name (e.g., "aliquota_inss_faixa_1")
- `valor_parametro`: Parameter value (e.g., "7.5")
- `tipo_valor`: Value type (percentual, moeda, inteiro)
- `contexto_original`: Original text context
- `data_inicio_vigencia`: Effective start date
- `data_fim_vigencia`: Effective end date

## Example Extracted Parameters

```json
{
  "parametros": [
    {
      "nome_parametro": "valor_salario_minimo_nacional",
      "valor_parametro": "1550.00",
      "tipo_valor": "moeda",
      "contexto_original": "Fica estabelecido o salário mínimo de R$ 1.550,00"
    },
    {
      "nome_parametro": "aliquota_inss_faixa_1",
      "valor_parametro": "7.5",
      "tipo_valor": "percentual",
      "contexto_original": "7,5% para salários de até R$ 1.412,00"
    }
  ]
}
```

## Testing

Run the test script:
```bash
node tests/test-ai-analysis.js
```

## Notes

- The PDF processing currently uses example text for demonstration
- In production, implement proper PDF text extraction using libraries like pdf-parse
- The AI analysis is currently optimized for Brazilian legal documents
- All functions include CORS headers for web browser compatibility