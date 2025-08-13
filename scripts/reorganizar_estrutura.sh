#!/bin/bash

# Script de Reorganização da Estrutura do Repositório AUDITORIA360
# Criado para facilitar a manutenção e reorganização seguindo as melhores práticas

set -e

echo "=== AUDITORIA360 - Script de Reorganização ==="
echo "Iniciando reorganização da estrutura do repositório..."

# Função para criar diretórios se não existirem
create_dir_if_not_exists() {
    if [ ! -d "$1" ]; then
        echo "Criando diretório: $1"
        mkdir -p "$1"
    else
        echo "Diretório já existe: $1"
    fi
}

# Criar estrutura de diretórios necessária
echo -e "\n1. Criando estrutura de diretórios..."
create_dir_if_not_exists "docs/historico"
create_dir_if_not_exists "demos"
create_dir_if_not_exists "demos/reports"
create_dir_if_not_exists "web"
create_dir_if_not_exists "conf"
create_dir_if_not_exists "tests"
create_dir_if_not_exists "scripts"

# Função para mover arquivos se existirem
move_if_exists() {
    local source="$1"
    local dest="$2"
    if [ -f "$source" ] || [ -d "$source" ]; then
        echo "Movendo: $source -> $dest"
        mv "$source" "$dest"
    else
        echo "Arquivo não encontrado (ok): $source"
    fi
}

# Mover arquivos de demo
echo -e "\n2. Reorganizando arquivos de demo..."
for file in demo_*.py; do
    if [ -f "$file" ]; then
        move_if_exists "$file" "demos/"
    fi
done

# Mover scripts de validação e seed
echo -e "\n3. Reorganizando scripts..."
move_if_exists "validate_*.py" "scripts/"
move_if_exists "seed_blueprint_data.py" "scripts/"

# Mover arquivos de teste da raiz para tests/
echo -e "\n4. Reorganizando testes..."
for file in test_*.py; do
    if [ -f "$file" ]; then
        move_if_exists "$file" "tests/"
    fi
done

# Mover arquivos HTML para web/
echo -e "\n5. Reorganizando arquivos web..."
for file in *.html; do
    if [ -f "$file" ]; then
        move_if_exists "$file" "web/"
    fi
done

# Mover configurações de webserver
echo -e "\n6. Reorganizando configurações..."
move_if_exists ".htaccess" "conf/"
move_if_exists "nginx.conf.example" "conf/"

# Mover relatórios de demo
echo -e "\n7. Reorganizando relatórios..."
if [ -d "demo_reports" ]; then
    mv demo_reports/* demos/reports/ 2>/dev/null || true
    rmdir demo_reports 2>/dev/null || true
fi

# Limpar arquivos temporários e de build
echo -e "\n8. Limpando arquivos temporários..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
rm -f .coverage 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true
find . -name "temp_*" -delete 2>/dev/null || true

echo -e "\n9. Verificando estrutura final..."
echo "Estrutura de diretórios criada:"
ls -la | grep ^d

# 10. Sugerir reorganização de arquivos soltos na raiz
echo -e "\n10. Sugerindo reorganização de arquivos soltos na raiz..."

# Lista de extensões e destinos sugeridos
declare -A EXT_DIR_MAP=(
    ["py"]="scripts/"
    ["sh"]="scripts/"
    ["sql"]="migrations/"
    ["md"]="docs/"
    ["json"]="conf/"
    ["html"]="web/"
    ["txt"]="docs/"
)

# Identifica arquivos soltos na raiz (exceto README.md, Makefile, arquivos ocultos)
for file in $(find . -maxdepth 1 -type f ! -name "README.md" ! -name "Makefile" ! -name ".*" ! -name "*.lock" ! -name "*.toml" ! -name "*.yml" ! -name "*.yaml"); do
    ext="${file##*.}"
    dest="${EXT_DIR_MAP[$ext]}"
    if [ -n "$dest" ] && [ ! -d "$dest" ]; then
        mkdir -p "$dest"
    fi
    if [ -n "$dest" ] && [ "$file" != "./${dest}"* ]; then
        echo "Movendo $file para $dest"
        mv "$file" "$dest"
    fi
done

# 11. Listar arquivos órfãos (não organizados)
echo -e "\n11. Arquivos órfãos (não organizados):"
find . -maxdepth 1 -type f ! -name "README.md" ! -name "Makefile" ! -name ".*" ! -name "*.lock" ! -name "*.toml" ! -name "*.yml" ! -name "*.yaml"

echo -e "\n=== Reorganização concluída! ==="
echo "Próximos passos:"
echo "1. Verifique se todos os arquivos foram movidos corretamente"
echo "2. Atualize o README.md"
echo "3. Teste a aplicação para garantir que não há referências quebradas"
echo "4. Commit das mudanças: git add . && git commit -m 'Reorganização da estrutura do repositório'"

echo -e "\nPara reverter mudanças (se necessário): git checkout ."