#!/bin/bash

# AUDITORIA360 Legacy System Inventory Script
# Generates a comprehensive inventory of the legacy system before migration

echo "# INVENTÁRIO COMPLETO DO SISTEMA LEGADO - AUDITORIA360"
echo "Gerado em: $(date)"
echo ""

# Legacy Frontend Analysis
echo "## FRONTEND LEGADO (src/frontend/)"
echo ""
echo "### Estatísticas Gerais"
echo "- Total de arquivos TypeScript/React: $(find ./src/frontend -name '*.tsx' -o -name '*.ts' | wc -l)"
echo "- Total de páginas: $(find ./src/frontend/src/pages -name '*.tsx' | wc -l)"
echo "- Total de componentes: $(find ./src/frontend/src/components -name '*.tsx' | wc -l 2>/dev/null || echo '0')"
echo ""

echo "### Páginas Legacy Identificadas"
find ./src/frontend/src/pages -name "*.tsx" | sort | while read file; do
    echo "- \`$(basename "$file" .tsx)\` - $file"
done
echo ""

echo "### Componentes Legacy"
if [ -d "./src/frontend/src/components" ]; then
    find ./src/frontend/src/components -name "*.tsx" | head -20 | while read file; do
        echo "- $file"
    done
    echo "- ... (total: $(find ./src/frontend/src/components -name '*.tsx' | wc -l) componentes)"
else
    echo "- Diretório de componentes não encontrado"
fi
echo ""

# API Backend Analysis
echo "## BACKEND LEGADO (src/api/)"
echo ""
if [ -d "./src/api" ]; then
    echo "### APIs Python"
    find ./src/api -name "*.py" | head -10 | while read file; do
        echo "- $file"
    done
    echo "- ... (total: $(find ./src/api -name '*.py' | wc -l) arquivos Python)"
else
    echo "- Diretório src/api não encontrado"
fi
echo ""

# Other Legacy Systems
echo "## OUTROS SISTEMAS LEGADOS"
echo ""

echo "### Portal de Demandas"
if [ -d "./portal_demandas" ]; then
    echo "- Diretório: ./portal_demandas/"
    echo "- Arquivos: $(find ./portal_demandas -type f | wc -l)"
else
    echo "- Não encontrado"
fi
echo ""

echo "### Supabase Functions"
if [ -d "./supabase" ]; then
    echo "- Diretório: ./supabase/"
    echo "- Functions: $(find ./supabase/functions -name "*.ts" 2>/dev/null | wc -l || echo '0')"
else
    echo "- Não encontrado"
fi
echo ""

echo "## ARQUIVOS DE CONFIGURAÇÃO"
echo ""
echo "### Configurações Principais"
config_files=("package.json" "tsconfig.json" "next.config.js" "tailwind.config.js" ".env.example")
for config in "${config_files[@]}"; do
    if [ -f "./$config" ]; then
        echo "- ✅ $config"
    else
        echo "- ❌ $config (ausente)"
    fi
done
echo ""

echo "### Configurações de Desenvolvimento"
dev_config_files=(".eslintrc.json" ".prettierrc" ".gitignore" "jest.config.js")
for config in "${dev_config_files[@]}"; do
    if [ -f "./$config" ]; then
        echo "- ✅ $config"
    else
        echo "- ❌ $config (ausente)"
    fi
done
echo ""

echo "## ARQUIVOS DUPLICADOS E OBSOLETOS"
echo ""
echo "### Possíveis Duplicações"
echo "- README files: $(find . -name "README*.md" | wc -l)"
find . -name "README*.md" | while read file; do
    echo "  - $file"
done
echo ""

echo "### Arquivos de Backup/Temporários"
backup_count=$(find . -name "*.bkp" -o -name "*.old" -o -name "*.tmp" -o -name "*~" | wc -l)
echo "- Total de arquivos backup/temporários: $backup_count"
if [ $backup_count -gt 0 ]; then
    find . -name "*.bkp" -o -name "*.old" -o -name "*.tmp" -o -name "*~" | head -10 | while read file; do
        echo "  - $file"
    done
fi
echo ""

echo "## RECOMENDAÇÕES DE MIGRAÇÃO"
echo ""
echo "### Prioridade Alta (Core Funcionalidades)"
echo "- Dashboard principal"
echo "- Sistema de autenticação"
echo "- Gestão de clientes"
echo "- Auditorias"
echo ""

echo "### Prioridade Média (Funcionalidades Específicas)"
echo "- Relatórios"
echo "- Upload de documentos"
echo "- Portal de demandas"
echo ""

echo "### Prioridade Baixa (Funcionalidades Auxiliares)"
echo "- Páginas de detalhe específicas"
echo "- Componentes de UI avançados"
echo "- Integrações secundárias"
echo ""

echo "---"
echo "**Inventário gerado automaticamente pelo script de migração AUDITORIA360**"