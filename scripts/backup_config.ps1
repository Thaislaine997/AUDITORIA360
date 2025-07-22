# Script PowerShell para backup dos arquivos críticos do AUDITORIA360
# Salva um zip com data/hora dos diretórios de configuração e autenticação

$Data = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupDir = "backups"
$BackupFile = "AUDITORIA360_backup_$Data.zip"

# Cria pasta de backup se não existir
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
}

# Lista os arquivos e pastas a serem incluídos
$Itens = @(
    "configs/client_configs",
    "auth/login.yaml"
)

# Cria o zip
Compress-Archive -Path $Itens -DestinationPath "$BackupDir/$BackupFile"

Write-Host "Backup criado em $BackupDir/$BackupFile"
