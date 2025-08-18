#!/bin/bash

# AUDITORIA360 Development Setup Script
# Configures the development environment with all necessary tools

set -e

echo "🚀 AUDITORIA360 - Configuração do Ambiente de Desenvolvimento"
echo "============================================================"
echo ""

# Check Node.js version
echo "🔍 Verificando Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js detectado: $NODE_VERSION"
    
    # Check if version is 18 or higher
    NODE_MAJOR_VERSION=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [ "$NODE_MAJOR_VERSION" -lt "18" ]; then
        echo "⚠️  AVISO: Node.js versão 18+ recomendada para melhor compatibilidade"
    fi
else
    echo "❌ Node.js não encontrado. Por favor, instale Node.js 18+ antes de continuar."
    exit 1
fi
echo ""

# Install dependencies
echo "📦 Instalando dependências..."
npm install
echo "✅ Dependências instaladas"
echo ""

# Setup environment variables
echo "🔧 Configurando variáveis de ambiente..."
if [ ! -f ".env.local" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env.local
        echo "✅ Arquivo .env.local criado a partir do .env.example"
        echo "⚠️  Configure as variáveis de ambiente em .env.local antes de executar"
    else
        echo "❌ Arquivo .env.example não encontrado"
    fi
else
    echo "✅ Arquivo .env.local já existe"
fi
echo ""

# Run linting
echo "🧹 Executando linting..."
if npm run lint --silent; then
    echo "✅ Linting passou sem erros"
else
    echo "⚠️  Alguns problemas de linting encontrados. Execute 'npm run lint' para detalhes."
fi
echo ""

# Run format check
echo "🎨 Verificando formatação..."
if npm run format:check --silent; then
    echo "✅ Formatação está correta"
else
    echo "⚠️  Formatação precisa de ajustes. Execute 'npm run format' para corrigir."
fi
echo ""

# Build test
echo "🏗️  Testando build..."
if npm run build --silent; then
    echo "✅ Build executado com sucesso"
else
    echo "❌ Build falhou. Verifique os erros acima."
    exit 1
fi
echo ""

# Success message
echo "🎉 Configuração concluída com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure as variáveis de ambiente em .env.local"
echo "2. Execute 'npm run dev' para iniciar o desenvolvimento"
echo "3. Acesse http://localhost:3000 para visualizar a aplicação"
echo ""
echo "🛠️  Comandos úteis:"
echo "- npm run dev        # Iniciar servidor de desenvolvimento"
echo "- npm run build      # Build para produção"
echo "- npm run lint       # Executar linting"
echo "- npm run format     # Formatar código"
echo "- npm run test       # Executar testes (quando disponível)"
echo ""
echo "📚 Documentação: ./README.md"
echo "🐛 Problemas: https://github.com/Thaislaine997/AUDITORIA360/issues"