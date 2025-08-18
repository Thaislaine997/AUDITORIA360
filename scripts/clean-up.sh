#!/bin/bash

# AUDITORIA360 Clean-up Script
# Removes obsolete, duplicate, and temporary files as part of the modernization plan

set -e

echo "🧹 AUDITORIA360 - Script de Limpeza e Otimização"
echo "==============================================="
echo ""

# Backup current state before cleanup
echo "💾 Criando backup de segurança..."
BACKUP_DIR="/tmp/auditoria360-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "Backup criado em: $BACKUP_DIR"
echo ""

# List files to be removed (dry run first)
echo "🔍 Analisando arquivos para limpeza..."
echo ""

echo "### Arquivos de backup/temporários encontrados:"
backup_files=$(find . -name "*.bkp" -o -name "*.old" -o -name "*.tmp" -o -name "*~" 2>/dev/null || true)
if [ -n "$backup_files" ]; then
    echo "$backup_files" | while read file; do
        echo "  - $file"
    done
else
    echo "  ✅ Nenhum arquivo de backup/temporário encontrado"
fi
echo ""

echo "### Arquivos de build/cache que podem ser limpos:"
cache_dirs=(
    "./node_modules/.cache"
    "./.next"
    "./out"
    "./dist"
    "./src/frontend/dist"
    "./src/frontend/node_modules"
)

for dir in "${cache_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  - $dir ($(du -sh "$dir" 2>/dev/null | cut -f1))"
    fi
done
echo ""

# Ask for confirmation
echo "⚠️  ATENÇÃO: Esta operação removerá arquivos permanentemente."
echo "Deseja continuar? (y/N)"
read -r response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "❌ Operação cancelada pelo usuário"
    exit 0
fi

echo ""
echo "🚀 Iniciando limpeza..."

# Remove backup/temporary files
echo "1. Removendo arquivos de backup e temporários..."
if [ -n "$backup_files" ]; then
    echo "$backup_files" | while read file; do
        if [ -f "$file" ]; then
            echo "  Removendo: $file"
            rm -f "$file"
        fi
    done
else
    echo "  ✅ Nenhum arquivo para remover"
fi

# Clean build artifacts
echo "2. Limpeza de artefatos de build..."
for dir in "${cache_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  Removendo: $dir"
        rm -rf "$dir"
    fi
done

# Clean npm cache if requested
echo "3. Limpeza de cache npm..."
echo "Deseja limpar o cache do npm? (y/N)"
read -r npm_response
if [[ "$npm_response" =~ ^[Yy]$ ]]; then
    npm cache clean --force
    echo "  ✅ Cache npm limpo"
else
    echo "  ⏭️  Cache npm mantido"
fi

echo ""
echo "🎯 Executando reinstalação limpa..."
npm install

echo ""
echo "🧪 Testando integridade após limpeza..."
if npm run build --silent; then
    echo "✅ Build teste bem-sucedido"
else
    echo "❌ Problema detectado no build. Verifique os logs."
    exit 1
fi

echo ""
echo "📊 Estatísticas finais:"
echo "- Diretório atual: $(du -sh . 2>/dev/null | cut -f1)"
echo "- Arquivos TypeScript: $(find . -name "*.ts" -o -name "*.tsx" | wc -l)"
echo "- Páginas Next.js: $(find ./pages -name "*.tsx" | wc -l)"
echo "- Componentes: $(find ./components -name "*.tsx" | wc -l)"

echo ""
echo "✅ Limpeza concluída com sucesso!"
echo ""
echo "📋 Próximos passos recomendados:"
echo "1. Executar: npm run validate"
echo "2. Testar aplicação: npm run dev"
echo "3. Verificar funcionalidades críticas"
echo "4. Fazer commit das alterações"

echo ""
echo "---"
echo "Backup disponível em: $BACKUP_DIR"
echo "Script executado em: $(date)"