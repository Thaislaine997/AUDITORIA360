@echo off
schtasks /create /tn "AuditoriaRH360" /tr "python C:\AUDITORIA360\src\auditoria_agendada.py" /sc monthly /mo 1 /d 5 /st 09:00 /ru SYSTEM
pause
