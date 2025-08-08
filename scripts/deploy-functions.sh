#!/bin/bash

# Deploy script for AUDITORIA360 Supabase functions
# This script helps deploy the AI text analysis functionality

echo "🚀 Deploying AUDITORIA360 AI Text Analysis Functions"
echo "================================================="

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI not found. Please install it first:"
    echo "   npm install -g @supabase/supabase"
    exit 1
fi

# Check if we're in a Supabase project
if [ ! -f "supabase/config.toml" ]; then
    echo "⚠️  supabase/config.toml not found. Initializing Supabase project..."
    echo "   Please run: supabase init"
    echo "   Then update supabase/config.toml with your project details"
    exit 1
fi

echo "📦 Deploying Edge Functions..."

# Deploy the PDF processing function
echo "   → Deploying processar-pdf function..."
npx supabase functions deploy processar-pdf --no-verify-jwt

if [ $? -eq 0 ]; then
    echo "   ✅ processar-pdf deployed successfully"
else
    echo "   ❌ Failed to deploy processar-pdf"
    exit 1
fi

# Deploy the AI analysis function
echo "   → Deploying analisar-texto-com-ia function..."
npx supabase functions deploy analisar-texto-com-ia --no-verify-jwt

if [ $? -eq 0 ]; then
    echo "   ✅ analisar-texto-com-ia deployed successfully"
else
    echo "   ❌ Failed to deploy analisar-texto-com-ia"
    exit 1
fi

echo ""
echo "🎉 All functions deployed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Set your GEMINI_API_KEY secret:"
echo "   npx supabase secrets set GEMINI_API_KEY=your_api_key_here"
echo ""
echo "2. Run the database migrations in your Supabase SQL Editor:"
echo "   - migrations/004_criar_tabela_documentos.sql"
echo "   - migrations/003_criar_tabela_parametros_legais.sql"
echo ""
echo "3. Test your functions:"
echo "   Send a PDF to: https://your-project.supabase.co/functions/v1/processar-pdf"
echo ""
echo "📚 See supabase/README.md for detailed setup instructions"