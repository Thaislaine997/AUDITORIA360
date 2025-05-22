# Script PowerShell para agendar backup diário automático do AUDITORIA360
# Cria uma tarefa agendada no Windows para rodar o backup_config.ps1 todo dia às 2h da manhã

$ScriptPath = (Resolve-Path "scripts/backup_config.ps1").Path
$TaskName = "Backup_AUDITORIA360_Diario"
$Hora = "02:00"

# Remove tarefa antiga se existir
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Cria nova tarefa agendada
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File `"$ScriptPath`""
$Trigger = New-ScheduledTaskTrigger -Daily -At $Hora
Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName $TaskName -Description "Backup diário automático do AUDITORIA360" -User "$env:USERNAME" -RunLevel Highest

Write-Host "Tarefa agendada '$TaskName' criada para rodar diariamente às $Hora."
