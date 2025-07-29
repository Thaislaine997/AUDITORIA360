@echo off
REM Script para agendar auditoria mensal automática do AUDITORIA360
REM Executa o exportar_auditorias_csv.py todo mês no dia 1 às 03:00

set TASKNAME=Auditoria_Mensal_AUDITORIA360
set SCRIPT="%~dp0exportar_auditorias_csv.py"
set PYTHON=python

REM Remove tarefa antiga se existir
schtasks /Delete /TN %TASKNAME% /F >nul 2>&1

REM Cria nova tarefa agendada
schtasks /Create /SC MONTHLY /D 1 /TN %TASKNAME% /TR "%PYTHON% %SCRIPT%" /ST 03:00 /RL HIGHEST

echo Tarefa agendada '%TASKNAME%' criada para rodar todo mês no dia 1 às 03:00.
pause
