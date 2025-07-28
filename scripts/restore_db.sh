#!/bin/bash
# Script para restaurar o banco Neon a partir de um backup.sql

if [ -z "$DATABASE_URL" ]; then
  echo "Defina a variável de ambiente DATABASE_URL antes de rodar este script."
  exit 1
fi

if [ ! -f backup.sql ]; then
  echo "Arquivo backup.sql não encontrado."
  exit 1
fi

PGPASSWORD=$(echo $DATABASE_URL | sed -E 's/.*:(.*)@.*/\1/') \
psql "$DATABASE_URL" < backup.sql

echo "Restauração concluída."
