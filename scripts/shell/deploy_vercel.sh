#!/bin/bash
# Script para deploy automatizado na Vercel

# Checa se o Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "Vercel CLI não encontrado. Instalando..."
    npm install -g vercel
fi

echo "Iniciando deploy na Vercel..."
vercel --prod --confirm
