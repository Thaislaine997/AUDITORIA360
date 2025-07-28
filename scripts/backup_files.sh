#!/bin/bash
# Script para backup dos arquivos do diretório data/input e data/raw

BACKUP_DIR=backups/backup_$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"
cp -r data/input "$BACKUP_DIR"/
cp -r data/raw "$BACKUP_DIR"/
echo "Backup dos arquivos realizado em $BACKUP_DIR"
