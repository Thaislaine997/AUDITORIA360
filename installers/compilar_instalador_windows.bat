@echo off
setlocal EnableDelayedExpansion

REM ================================================================
REM Script: compilar_instalador_windows.bat
REM Descrição: Script para compilar o instalador do AUDITORIA360 no Windows
REM Uso: compilar_instalador_windows.bat [opcoes]
REM Autor: AUDITORIA360 Team
REM Data: 2024-07-29
REM Versão: 2.0.0
REM ================================================================

REM Configurações
set SCRIPT_NAME=%~n0
set SCRIPT_DIR=%~dp0
set LOG_FILE=%TEMP%\%SCRIPT_NAME%.log
set INSTALLER_NAME=AUDITORIA360_Installer
set BUILD_DIR=%SCRIPT_DIR%build
set DIST_DIR=%SCRIPT_DIR%dist

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
call :log_info "Verificando pré-requisitos para compilação..."

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Python não está instalado ou não está no PATH"
    exit /b 1
)

REM Verificar se PyInstaller está instalado
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    call :log_warning "PyInstaller não encontrado. Instalando..."
    pip install pyinstaller
    if errorlevel 1 (
        call :log_error "Falha ao instalar PyInstaller"
        exit /b 1
    )
)

REM Verificar se Inno Setup está instalado (opcional)
where iscc >nul 2>&1
if errorlevel 1 (
    call :log_warning "Inno Setup não encontrado. Instalador avançado não será criado."
    set INNO_AVAILABLE=false
) else (
    set INNO_AVAILABLE=true
)

call :log_success "Pré-requisitos verificados"
goto :eof

:create_directories
call :log_info "Criando diretórios de build..."

if not exist "%BUILD_DIR%" (
    mkdir "%BUILD_DIR%"
    call :log_info "Diretório build criado: %BUILD_DIR%"
)

if not exist "%DIST_DIR%" (
    mkdir "%DIST_DIR%"
    call :log_info "Diretório dist criado: %DIST_DIR%"
)

goto :eof

:cleanup_previous_build
call :log_info "Limpando builds anteriores..."

if exist "%BUILD_DIR%" (
    rmdir /s /q "%BUILD_DIR%"
    call :log_info "Build anterior removido"
)

if exist "%DIST_DIR%" (
    rmdir /s /q "%DIST_DIR%"
    call :log_info "Distribuição anterior removida"
)

goto :eof

:build_executable
call :log_info "Compilando aplicação principal com PyInstaller..."

REM Verificar se existe arquivo spec personalizado
if exist "%SCRIPT_DIR%auditoria360.spec" (
    call :log_info "Usando arquivo .spec personalizado"
    pyinstaller "%SCRIPT_DIR%auditoria360.spec" --distpath "%DIST_DIR%" --workpath "%BUILD_DIR%"
) else (
    REM Compilação padrão
    call :log_info "Usando configuração padrão do PyInstaller"
    pyinstaller --onefile --windowed ^
        --name "%INSTALLER_NAME%" ^
        --distpath "%DIST_DIR%" ^
        --workpath "%BUILD_DIR%" ^
        --add-data "configs;configs" ^
        --add-data "assets;assets" ^
        --icon="%SCRIPT_DIR%assets\icon.ico" ^
        "%SCRIPT_DIR%..\src\main.py"
)

if errorlevel 1 (
    call :log_error "Falha na compilação com PyInstaller"
    exit /b 1
)

call :log_success "Executável compilado com sucesso"
goto :eof

:create_installer_script
call :log_info "Criando script do Inno Setup..."

set INNO_SCRIPT=%SCRIPT_DIR%installer_script.iss

echo [Setup] > "%INNO_SCRIPT%"
echo AppName=AUDITORIA360 >> "%INNO_SCRIPT%"
echo AppVersion=1.0.0 >> "%INNO_SCRIPT%"
echo AppPublisher=AUDITORIA360 Team >> "%INNO_SCRIPT%"
echo DefaultDirName={pf}\AUDITORIA360 >> "%INNO_SCRIPT%"
echo DefaultGroupName=AUDITORIA360 >> "%INNO_SCRIPT%"
echo OutputDir=%DIST_DIR% >> "%INNO_SCRIPT%"
echo OutputBaseFilename=AUDITORIA360_Setup >> "%INNO_SCRIPT%"
echo Compression=lzma >> "%INNO_SCRIPT%"
echo SolidCompression=yes >> "%INNO_SCRIPT%"
echo >> "%INNO_SCRIPT%"
echo [Files] >> "%INNO_SCRIPT%"
echo Source: "%DIST_DIR%\%INSTALLER_NAME%.exe"; DestDir: "{app}"; Flags: ignoreversion >> "%INNO_SCRIPT%"
echo >> "%INNO_SCRIPT%"
echo [Icons] >> "%INNO_SCRIPT%"
echo Name: "{group}\AUDITORIA360"; Filename: "{app}\%INSTALLER_NAME%.exe" >> "%INNO_SCRIPT%"
echo Name: "{commondesktop}\AUDITORIA360"; Filename: "{app}\%INSTALLER_NAME%.exe"; Tasks: desktopicon >> "%INNO_SCRIPT%"
echo >> "%INNO_SCRIPT%"
echo [Tasks] >> "%INNO_SCRIPT%"
echo Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked >> "%INNO_SCRIPT%"

call :log_success "Script do Inno Setup criado"
goto :eof

:build_installer
if "%INNO_AVAILABLE%"=="false" (
    call :log_warning "Inno Setup não disponível. Pulando criação do instalador."
    goto :eof
)

call :log_info "Criando instalador com Inno Setup..."

call :create_installer_script

iscc "%SCRIPT_DIR%installer_script.iss"
if errorlevel 1 (
    call :log_error "Falha na criação do instalador"
    exit /b 1
)

REM Limpar arquivo temporário
del "%SCRIPT_DIR%installer_script.iss"

call :log_success "Instalador criado com sucesso"
goto :eof

:show_results
call :log_info "=== RESULTADOS DA COMPILAÇÃO ==="

if exist "%DIST_DIR%\%INSTALLER_NAME%.exe" (
    call :log_success "Executável: %DIST_DIR%\%INSTALLER_NAME%.exe"
    for %%I in ("%DIST_DIR%\%INSTALLER_NAME%.exe") do (
        call :log_info "Tamanho: %%~zI bytes"
    )
)

if exist "%DIST_DIR%\AUDITORIA360_Setup.exe" (
    call :log_success "Instalador: %DIST_DIR%\AUDITORIA360_Setup.exe"
    for %%I in ("%DIST_DIR%\AUDITORIA360_Setup.exe") do (
        call :log_info "Tamanho: %%~zI bytes"
    )
)

call :log_info "Log completo: %LOG_FILE%"
call :log_info "================================"
goto :eof

:cleanup
call :log_info "Executando limpeza..."
REM Remover arquivos temporários se necessário
goto :eof

:show_help
echo Uso: %SCRIPT_NAME% [OPCOES]
echo.
echo DESCRICAO:
echo     Compila o aplicativo AUDITORIA360 para Windows usando PyInstaller
echo     e opcionalmente cria um instalador usando Inno Setup
echo.
echo OPCOES:
echo     /h, /help     Mostra esta ajuda
echo     /clean        Limpa builds anteriores antes de compilar
echo     /noinstaller  Não cria instalador (apenas executável)
echo.
echo EXEMPLOS:
echo     %SCRIPT_NAME%                   - Compilação padrão
echo     %SCRIPT_NAME% /clean            - Limpa e compila
echo     %SCRIPT_NAME% /noinstaller      - Apenas executável
echo.
goto :eof

:main
call :log_info "=== AUDITORIA360 - COMPILADOR DE INSTALADOR WINDOWS ==="
call :log_info "Iniciando %SCRIPT_NAME%..."

set CLEAN_BUILD=false
set CREATE_INSTALLER=true

REM Processar argumentos
:parse_args
if "%~1"=="" goto :start_compilation
if /i "%~1"=="/h" goto :show_help
if /i "%~1"=="/help" goto :show_help
if /i "%~1"=="/clean" (
    set CLEAN_BUILD=true
    shift
    goto :parse_args
)
if /i "%~1"=="/noinstaller" (
    set CREATE_INSTALLER=false
    shift
    goto :parse_args
)

call :log_error "Opção desconhecida: %~1"
goto :show_help

:start_compilation
REM Verificar pré-requisitos
call :check_prerequisites
if errorlevel 1 exit /b 1

REM Limpar builds anteriores se solicitado
if "%CLEAN_BUILD%"=="true" (
    call :cleanup_previous_build
)

REM Criar diretórios necessários
call :create_directories

REM Compilar executável
call :build_executable
if errorlevel 1 exit /b 1

REM Criar instalador se solicitado
if "%CREATE_INSTALLER%"=="true" (
    call :build_installer
    if errorlevel 1 exit /b 1
)

REM Mostrar resultados
call :show_results

REM Limpeza final
call :cleanup

call :log_success "=== COMPILAÇÃO CONCLUÍDA COM SUCESSO ==="
exit /b 0