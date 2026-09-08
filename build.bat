@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ==========================================================
REM SCRIPTCASE MONITOR - BUILD
REM ==========================================================

cd /d "%~dp0"

echo.
echo ==========================================
echo     ScriptCase Monitor - Build
echo ==========================================
echo.
echo Diretorio do projeto:
echo %CD%
echo.

REM ==========================================================
REM VERIFICAR PYTHON / VENV
REM ==========================================================

if not exist ".venv\Scripts\python.exe" (
    echo [ERRO] Ambiente virtual nao encontrado:
    echo .venv\Scripts\python.exe
    echo.
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"

REM ==========================================================
REM VERIFICAR ARQUIVOS PRINCIPAIS
REM ==========================================================

if not exist "interface\app.py" (
    echo [ERRO] interface\app.py nao encontrado.
    pause
    exit /b 1
)

if not exist "main.py" (
    echo [ERRO] main.py nao encontrado.
    pause
    exit /b 1
)

if not exist "logo.png" (
    echo [ERRO] logo.png nao encontrado.
    pause
    exit /b 1
)

if not exist "logo.ico" (
    echo [ERRO] logo.ico nao encontrado.
    pause
    exit /b 1
)

if not exist "config" (
    echo [ERRO] Pasta config nao encontrada.
    pause
    exit /b 1
)

REM ==========================================================
REM 1 - PYINSTALLER
REM ==========================================================

echo.
echo [1/7] Instalando PyInstaller...

python -m pip install --upgrade pyinstaller

if errorlevel 1 goto erro

REM ==========================================================
REM 2 - PLAYWRIGHT
REM ==========================================================

echo.
echo [2/7] Verificando Playwright...

python -m pip install --upgrade playwright

if errorlevel 1 goto erro

REM ==========================================================
REM 3 - INSTALAR CHROMIUM
REM ==========================================================

echo.
echo [3/7] Instalando Chromium do Playwright...

set PLAYWRIGHT_BROWSERS_PATH=0

python -m playwright install chromium

if errorlevel 1 goto erro

REM ==========================================================
REM 4 - LIMPAR BUILD ANTERIOR
REM ==========================================================

echo.
echo [4/7] Limpando compilacoes anteriores...

if exist "build" (
    rmdir /S /Q "build"
)

if exist "dist" (
    rmdir /S /Q "dist"
)

if exist "ScriptCaseMonitor.spec" (
    del /F /Q "ScriptCaseMonitor.spec"
)

REM ==========================================================
REM 5 - COMPILAR
REM ==========================================================

echo.
echo [5/7] Compilando executavel...

pyinstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --onedir ^
    --name "ScriptCaseMonitor" ^
    --icon "%CD%\logo.ico" ^
    --add-data "%CD%\logo.png;." ^
    --add-data "%CD%\logo.ico;." ^
    --add-data "%CD%\config;config" ^
    --hidden-import main ^
    --hidden-import services.login ^
    --hidden-import services.checker ^
    --hidden-import services.logger ^
    --hidden-import services.report ^
    --hidden-import services.scanner ^
    --hidden-import services.context_manager ^
    --hidden-import validators.page_validator ^
    --hidden-import config.config ^
    --hidden-import config.monitor_config ^
    --hidden-import config.context_config ^
    "interface\app.py"

if errorlevel 1 goto erro

REM ==========================================================
REM 6 - COPIAR ARQUIVOS EXTERNOS
REM ==========================================================

echo.
echo [6/7] Copiando arquivos para dist...

if not exist "dist\ScriptCaseMonitor\config" (
    mkdir "dist\ScriptCaseMonitor\config"
)

echo.
echo Copiando logo.png...
copy /Y "%CD%\logo.png" ^
"%CD%\dist\ScriptCaseMonitor\logo.png"

if errorlevel 1 goto erro

echo.
echo Copiando logo.ico...
copy /Y "%CD%\logo.ico" ^
"%CD%\dist\ScriptCaseMonitor\logo.ico"

if errorlevel 1 goto erro

echo.
echo Copiando configuracoes...

copy /Y "%CD%\config\config.ini" ^
"%CD%\dist\ScriptCaseMonitor\config\config.ini"

copy /Y "%CD%\config\monitor.ini" ^
"%CD%\dist\ScriptCaseMonitor\config\monitor.ini"

copy /Y "%CD%\config\context.ini" ^
"%CD%\dist\ScriptCaseMonitor\config\context.ini"

REM ==========================================================
REM COPIAR CHROMIUM
REM ==========================================================

echo.
echo Copiando Chromium do Playwright...

if not exist ".venv\Lib\site-packages\playwright\driver\package\.local-browsers" (

    echo.
    echo [ERRO] .local-browsers nao encontrado.
    echo.
    echo Caminho esperado:
    echo .venv\Lib\site-packages\playwright\driver\package\.local-browsers
    goto erro
)

if not exist "dist\ScriptCaseMonitor\_internal\playwright\driver\package" (
    mkdir "dist\ScriptCaseMonitor\_internal\playwright\driver\package"
)

xcopy ^
    ".venv\Lib\site-packages\playwright\driver\package\.local-browsers" ^
    "dist\ScriptCaseMonitor\_internal\playwright\driver\package\.local-browsers" ^
    /E ^
    /I ^
    /Y

if errorlevel 1 goto erro

REM ==========================================================
REM 7 - VALIDACAO FINAL
REM ==========================================================

echo.
echo [7/7] Validando pacote final...

if not exist "dist\ScriptCaseMonitor\ScriptCaseMonitor.exe" (
    echo [ERRO] Executavel nao encontrado.
    goto erro
)

if not exist "dist\ScriptCaseMonitor\logo.png" (
    echo [ERRO] logo.png nao foi copiado.
    goto erro
)

if not exist "dist\ScriptCaseMonitor\logo.ico" (
    echo [ERRO] logo.ico nao foi copiado.
    goto erro
)

if not exist "dist\ScriptCaseMonitor\config\config.ini" (
    echo [ERRO] config.ini nao foi copiado.
    goto erro
)

if not exist "dist\ScriptCaseMonitor\config\monitor.ini" (
    echo [ERRO] monitor.ini nao foi copiado.
    goto erro
)

if not exist "dist\ScriptCaseMonitor\config\context.ini" (
    echo [ERRO] context.ini nao foi copiado.
    goto erro
)

if not exist "dist\ScriptCaseMonitor\_internal\playwright\driver\package\.local-browsers" (
    echo [ERRO] Chromium nao foi copiado.
    goto erro
)

REM ==========================================================
REM SUCESSO
REM ==========================================================

echo.
echo ==========================================
echo     BUILD CONCLUIDO COM SUCESSO
echo ==========================================
echo.
echo Pacote final:
echo.
echo %CD%\dist\ScriptCaseMonitor\
echo.
echo Executavel:
echo.
echo %CD%\dist\ScriptCaseMonitor\ScriptCaseMonitor.exe
echo.
echo Arquivos:
echo   [OK] ScriptCaseMonitor.exe
echo   [OK] logo.png
echo   [OK] logo.ico
echo   [OK] config\
echo   [OK] Chromium / Playwright
echo.
pause
exit /b 0

REM ==========================================================
REM ERRO
REM ==========================================================

:erro

echo.
echo ==========================================
echo     ERRO DURANTE A COMPILACAO
echo ==========================================
echo.
echo Verifique a mensagem acima.
echo.
pause
exit /b 1