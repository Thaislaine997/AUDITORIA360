# Supabase Edge Functions Configuration

## Required Environment Variables

To deploy and run the Edge Functions, you need to set the following environment variables in your Supabase project:

### 1. GEMINI_API_KEY
- Get your API key from Google AI Studio: https://aistudio.google.com/app/apikey
- Set in Supabase: `npx supabase secrets set GEMINI_API_KEY=your_api_key_here`

### 2. SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY
- These are automatically available in Edge Functions
- Found in your Supabase project settings

## Deployment Commands

```bash
# Deploy the AI text analysis function
npx supabase functions deploy analisar-texto-com-ia --no-verify-jwt

# Deploy the PDF processing function  
npx supabase functions deploy processar-pdf --no-verify-jwt
```

## Database Setup

Execute the following migrations in order in your Supabase SQL Editor:

1. `migrations/004_criar_tabela_documentos.sql` - Creates the Documentos table
2. `migrations/003_criar_tabela_parametros_legais.sql` - Creates the ParametrosLegais table

## Testing

After deployment, you can test the PDF processing by sending a POST request to:
`https://your-project.supabase.co/functions/v1/processar-pdf`

With a multipart/form-data body containing a PDF file.

## Function Flow

1. **processar-pdf**: Receives PDF file → Extracts text → Saves to Documentos table → Calls AI analysis
2. **analisar-texto-com-ia**: Receives document record → Calls AI API → Extracts parameters → Saves to ParametrosLegais table