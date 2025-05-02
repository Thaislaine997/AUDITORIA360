@echo off
schtasks /create /tn "AuditoriaRH360" /tr "python C:\AUDITORIA_RH_360\auditoria_agendada.py" /sc monthly /mo 1 /d 5 /st 09:00 /ru SYSTEM
echo Auditoria agendada para todo dia 5 às 09:00.
pause
