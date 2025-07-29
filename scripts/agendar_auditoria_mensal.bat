@echo off
setlocal EnableDelayedExpansion

REM ================================================================
REM Script: agendar_auditoria_mensal.bat
REM Descrição: Agendamento de auditoria mensal automática do AUDITORIA360
REM Uso: agendar_auditoria_mensal.bat [opcoes]
REM Autor: AUDITORIA360 Team
REM Data: 2024-07-29
REM Versão: 2.0.0
REM ================================================================

REM Configurações
set SCRIPT_NAME=%~n0
set SCRIPT_DIR=%~dp0
set LOG_FILE=%TEMP%\%SCRIPT_NAME%.log
set TASK_NAME=Auditoria_Mensal_AUDITORIA360
set PYTHON_SCRIPT=%SCRIPT_DIR%exportar_auditorias_csv.py
set PYTHON_CMD=python
set SCHEDULE_TIME=03:00
set SCHEDULE_DAY=1
set RUN_LEVEL=HIGHEST

REM Função de logging (usando goto)
goto :main

:log_info
echo [INFO] %~1
echo [%date% %time%] [INFO] %~1 >> "%LOG_FILE%"
goto :eof

:log_success
echo [SUCCESS] %~1
echo [%date% %time%] [SUCCESS] %~1 >> "%LOG_FILE%"
goto :eof

:log_warning
echo [WARNING] %~1
echo [%date% %time%] [WARNING] %~1 >> "%LOG_FILE%"
goto :eof

:log_error
echo [ERROR] %~1
echo [%date% %time%] [ERROR] %~1 >> "%LOG_FILE%"
goto :eof

:check_prerequisites
call :log_info "Verificando pré-requisitos..."

REM Verificar se está executando como administrador
net session >nul 2>&1
if errorlevel 1 (
    call :log_error "Este script precisa ser executado como Administrador"
    call :log_info "Clique com o botão direito e selecione 'Executar como administrador'"
    pause
    exit /b 1
)

REM Verificar se schtasks está disponível
schtasks /? >nul 2>&1
if errorlevel 1 (
    call :log_error "Comando schtasks não está disponível"
    exit /b 1
)

REM Verificar se Python está instalado
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    call :log_warning "Python não encontrado. Tentando 'py'..."
    set PYTHON_CMD=py
    py --version >nul 2>&1
    if errorlevel 1 (
        call :log_error "Python não está instalado ou não está no PATH"
        call :log_info "Instale Python em: https://python.org/downloads"
        exit /b 1
    )
)

REM Verificar se o script Python existe
if not exist "%PYTHON_SCRIPT%" (
    call :log_error "Script Python não encontrado: %PYTHON_SCRIPT%"
    exit /b 1
)

call :log_success "Pré-requisitos verificados"
goto :eof

:remove_existing_task
call :log_info "Removendo tarefa agendada existente (se houver)..."

schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if not errorlevel 1 (
    call :log_info "Tarefa existente encontrada. Removendo..."
    schtasks /Delete /TN "%TASK_NAME%" /F >nul 2>&1
    if errorlevel 1 (
        call :log_warning "Falha ao remover tarefa existente"
    ) else (
        call :log_success "Tarefa existente removida"
    )
) else (
    call :log_info "Nenhuma tarefa existente encontrada"
)

goto :eof

:create_task
call :log_info "Criando nova tarefa agendada..."

REM Criar comando completo para a tarefa
set TASK_COMMAND="%PYTHON_CMD%" "%PYTHON_SCRIPT%"

call :log_info "Configurações da tarefa:"
call :log_info "  Nome: %TASK_NAME%"
call :log_info "  Comando: %TASK_COMMAND%"
call :log_info "  Agendamento: Todo mês no dia %SCHEDULE_DAY% às %SCHEDULE_TIME%"
call :log_info "  Nível de execução: %RUN_LEVEL%"

REM Criar tarefa agendada com configurações avançadas
schtasks /Create ^
    /SC MONTHLY ^
    /D %SCHEDULE_DAY% ^
    /TN "%TASK_NAME%" ^
    /TR "%TASK_COMMAND%" ^
    /ST %SCHEDULE_TIME% ^
    /RL %RUN_LEVEL% ^
    /RU SYSTEM ^
    /F

if errorlevel 1 (
    call :log_error "Falha ao criar tarefa agendada"
    exit /b 1
) else (
    call :log_success "Tarefa agendada criada com sucesso"
)

goto :eof

:verify_task
call :log_info "Verificando tarefa criada..."

schtasks /Query /TN "%TASK_NAME%" /FO LIST >nul 2>&1
if errorlevel 1 (
    call :log_error "Tarefa não foi criada corretamente"
    exit /b 1
) else (
    call :log_success "Tarefa verificada e funcionando"
    
    call :log_info "Detalhes da tarefa:"
    schtasks /Query /TN "%TASK_NAME%" /FO LIST | findstr /C:"TaskName" /C:"Next Run Time" /C:"Status" /C:"Schedule"
)

goto :eof

:test_script
call :log_info "Testando script Python..."

REM Verificar se o script Python pode ser importado/executado
%PYTHON_CMD% -c "import sys; print('Python OK')" >nul 2>&1
if errorlevel 1 (
    call :log_warning "Erro ao testar Python"
) else (
    call :log_success "Python funcionando corretamente"
)

REM Teste básico do script (verificação de sintaxe)
%PYTHON_CMD% -m py_compile "%PYTHON_SCRIPT%" >nul 2>&1
if errorlevel 1 (
    call :log_warning "Script Python pode ter problemas de sintaxe"
) else (
    call :log_success "Script Python compilado com sucesso"
)

goto :eof

:run_now_option
call :log_info "Executando tarefa imediatamente para teste..."

schtasks /Run /TN "%TASK_NAME%"
if errorlevel 1 (
    call :log_warning "Falha ao executar tarefa imediatamente"
) else (
    call :log_success "Tarefa iniciada. Verifique os logs para confirmar execução."
)

goto :eof

:show_help
echo Uso: %SCRIPT_NAME% [OPCOES]
echo.
echo DESCRICAO:
echo     Configura agendamento automático de auditoria mensal do AUDITORIA360
echo     A tarefa será executada todo dia 1 do mês às 03:00
echo.
echo OPCOES:
echo     /h, /help        Mostra esta ajuda
echo     /remove          Remove agendamento existente
echo     /test            Testa o script Python
echo     /run             Executa a tarefa imediatamente após criar
echo     /status          Mostra status da tarefa atual
echo.
echo EXEMPLOS:
echo     %SCRIPT_NAME%                - Cria agendamento padrão
echo     %SCRIPT_NAME% /remove        - Remove agendamento
echo     %SCRIPT_NAME% /test          - Testa configuração
echo.
echo NOTAS:
echo     - Deve ser executado como Administrador
echo     - Python deve estar instalado e no PATH
echo     - Script exportar_auditorias_csv.py deve existir
echo.
goto :eof

:show_status
call :log_info "Status da tarefa agendada:"

schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if errorlevel 1 (
    call :log_warning "Tarefa '%TASK_NAME%' não está agendada"
) else (
    call :log_success "Tarefa '%TASK_NAME%' está ativa"
    echo.
    echo Detalhes:
    schtasks /Query /TN "%TASK_NAME%" /FO LIST
)

goto :eof

:remove_task_only
call :log_info "Removendo tarefa agendada..."

schtasks /Query /TN "%TASK_NAME%" >nul 2>&1
if errorlevel 1 (
    call :log_warning "Tarefa '%TASK_NAME%' não existe"
) else (
    schtasks /Delete /TN "%TASK_NAME%" /F
    if errorlevel 1 (
        call :log_error "Falha ao remover tarefa"
        exit /b 1
    ) else (
        call :log_success "Tarefa removida com sucesso"
    )
)

goto :eof

:cleanup
call :log_info "Executando limpeza..."
REM Limpeza de arquivos temporários se necessário
goto :eof

:main
call :log_info "=== AUDITORIA360 - AGENDADOR DE AUDITORIA MENSAL ==="
call :log_info "Iniciando %SCRIPT_NAME%..."

set RUN_NOW=false
set TEST_ONLY=false

REM Processar argumentos
:parse_args
if "%~1"=="" goto :start_execution
if /i "%~1"=="/h" goto :show_help
if /i "%~1"=="/help" goto :show_help
if /i "%~1"=="/remove" goto :remove_task_only
if /i "%~1"=="/test" (
    set TEST_ONLY=true
    shift
    goto :parse_args
)
if /i "%~1"=="/run" (
    set RUN_NOW=true
    shift
    goto :parse_args
)
if /i "%~1"=="/status" goto :show_status

call :log_error "Opção desconhecida: %~1"
goto :show_help

:start_execution
REM Verificar pré-requisitos
call :check_prerequisites
if errorlevel 1 exit /b 1

REM Se for apenas teste, executar teste e sair
if "%TEST_ONLY%"=="true" (
    call :test_script
    goto :end_success
)

REM Remover tarefa existente
call :remove_existing_task

REM Criar nova tarefa
call :create_task
if errorlevel 1 exit /b 1

REM Verificar tarefa criada
call :verify_task
if errorlevel 1 exit /b 1

REM Testar script Python
call :test_script

REM Executar tarefa agora se solicitado
if "%RUN_NOW%"=="true" (
    call :run_now_option
)

:end_success
REM Limpeza
call :cleanup

call :log_success "=== CONFIGURAÇÃO CONCLUÍDA COM SUCESSO ==="
echo.
call :log_info "RESUMO:"
call :log_info "  ✓ Tarefa '%TASK_NAME%' configurada"
call :log_info "  ✓ Agendamento: Todo dia %SCHEDULE_DAY% do mês às %SCHEDULE_TIME%"
call :log_info "  ✓ Script: %PYTHON_SCRIPT%"
call :log_info "  ✓ Log: %LOG_FILE%"
echo.
call :log_info "Para verificar o status: schtasks /Query /TN \"%TASK_NAME%\""
call :log_info "Para executar manualmente: schtasks /Run /TN \"%TASK_NAME%\""
echo.
pause
exit /b 0
