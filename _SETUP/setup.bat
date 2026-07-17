@echo off
REM ============================================================
REM SCRIPT DE CONFIGURACAO AUTOMATICA - WINDOWS
REM Agente Investigador SINARM E1
REM ============================================================

echo.
echo ============================================================
echo   CONFIGURACAO AUTOMATICA DO AMBIENTE
echo   Agente Investigador SINARM E1
echo ============================================================
echo.

REM Verificar se Python esta instalado
echo [1/6] Verificando instalacao do Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo Durante a instalacao, marque a opcao:
    echo [X] Add Python to PATH
    echo.
    pause
    exit /b 1
)

REM Mostrar versao do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python encontrado: %PYTHON_VERSION%

REM Verificar versao minima (Python 3.8+)
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo.
    echo [ERRO] Versao do Python muito antiga!
    echo Versao atual: %PYTHON_VERSION%
    echo Versao minima: 3.8
    echo.
    echo Baixe a versao mais recente em:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

if %MAJOR% EQU 3 if %MINOR% LSS 8 (
    echo.
    echo [AVISO] Versao do Python pode ser muito antiga!
    echo Versao atual: %PYTHON_VERSION%
    echo Versao recomendada: 3.10+
    echo.
    echo Recomendamos atualizar para Python 3.10 ou superior.
    echo Continuar mesmo assim? (S/N)
    set /p CONTINUE=
    if /i not "%CONTINUE%"=="S" (
        exit /b 1
    )
)

echo [OK] Versao do Python compativel: %PYTHON_VERSION%
echo.

REM Verificar se ja existe venv
echo [2/6] Verificando ambiente virtual...
if exist "venv\" (
    echo.
    echo [AVISO] Ambiente virtual ja existe!
    echo Deseja recria-lo? (S/N)
    echo (Recomendado se houver problemas)
    set /p RECREATE=
    if /i "%RECREATE%"=="S" (
        echo.
        echo Removendo ambiente virtual antigo...
        rmdir /s /q venv
        echo [OK] Ambiente virtual removido
    ) else (
        echo.
        echo Pulando criacao do ambiente virtual...
        goto :activate_venv
    )
)

echo Criando ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao criar ambiente virtual!
    echo.
    echo Tente instalar o pacote venv:
    echo pip install virtualenv
    echo.
    pause
    exit /b 1
)
echo [OK] Ambiente virtual criado
echo.

:activate_venv
REM Ativar ambiente virtual
echo [3/6] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao ativar ambiente virtual!
    echo.
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado
echo.

REM Atualizar pip
echo [4/6] Atualizando pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [AVISO] Falha ao atualizar pip, continuando...
) else (
    echo [OK] pip atualizado
)
echo.

REM Instalar dependencias
echo [5/6] Instalando dependencias do projeto...
echo Isso pode levar alguns minutos...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar dependencias!
    echo.
    echo Tente manualmente:
    echo 1. venv\Scripts\activate
    echo 2. pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
echo.
echo [OK] Dependencias instaladas
echo.

REM Verificar instalacao
echo [6/6] Verificando instalacao...
python verify_setup.py
if errorlevel 1 (
    echo.
    echo [AVISO] Alguns componentes podem nao estar funcionando corretamente.
    echo Verifique os erros acima.
    echo.
) else (
    echo.
    echo [OK] Instalacao verificada com sucesso!
)
echo.

REM Verificar Ollama
echo ============================================================
echo   VERIFICANDO OLLAMA
echo ============================================================
echo.
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Ollama nao encontrado!
    echo.
    echo O agente precisa do Ollama para funcionar.
    echo.
    echo 1. Baixe em: https://ollama.ai
    echo 2. Instale o Ollama
    echo 3. Execute: ollama pull llama3
    echo.
) else (
    echo [OK] Ollama instalado
    echo.
    echo Verificando modelo llama3...
    ollama list | findstr llama3 >nul 2>&1
    if errorlevel 1 (
        echo [AVISO] Modelo llama3 nao encontrado!
        echo.
        echo Execute: ollama pull llama3
        echo.
    ) else (
        echo [OK] Modelo llama3 disponivel
    )
)
echo.

REM Finalizar
echo ============================================================
echo   CONFIGURACAO CONCLUIDA!
echo ============================================================
echo.
echo Ambiente virtual criado e ativado com sucesso!
echo.
echo PROXIMOS PASSOS:
echo.
echo 1. Para ATIVAR o ambiente virtual (sempre que abrir novo terminal):
echo    venv\Scripts\activate
echo.
echo 2. Para TESTAR o agente:
echo    python E1_agente_react_v3.py
echo.
echo 3. Para executar os TESTES:
echo    python TESTES_COMPLETOS.py
echo.
echo 4. Para DESATIVAR o ambiente virtual:
echo    deactivate
echo.
echo ============================================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
