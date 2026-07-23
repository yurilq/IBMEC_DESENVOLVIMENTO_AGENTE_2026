@echo off
REM Script para copiar pasta DADOS_SINARM para local correto
REM Execute este script na pasta 03_CODIGOS_PRONTOS

echo ====================================================================
echo COPIAR DADOS SINARM - E4 RAG + FAISS
echo ====================================================================
echo.

REM Verificar se já existe
if exist "DADOS_SINARM" (
    echo [AVISO] Pasta DADOS_SINARM ja existe!
    echo.
    choice /C SN /M "Deseja substituir? (S=Sim, N=Nao)"
    if errorlevel 2 goto :fim
    if errorlevel 1 goto :copiar
) else (
    goto :copiar
)

:copiar
echo.
echo Copiando pasta DADOS_SINARM...
echo.
echo DE: ..\..\DADOS_SINARM
echo PARA: %CD%\DADOS_SINARM
echo.

REM Copiar pasta (robocopy é mais rápido)
robocopy "..\..\DADOS_SINARM" "DADOS_SINARM" /E /NFL /NDL /NJH /NJS /nc /ns /np

if errorlevel 8 (
    echo.
    echo [ERRO] Falha ao copiar arquivos!
    echo Verifique se a pasta origem existe: ..\..\DADOS_SINARM
    pause
    exit /b 1
)

echo.
echo ====================================================================
echo OK! DADOS_SINARM copiados com sucesso!
echo ====================================================================
echo.

REM Verificar tamanho
echo Verificando arquivos copiados...
echo.

if exist "DADOS_SINARM\OCORRENCIAS\OCORRENCIAS_2026.csv" (
    echo [OK] OCORRENCIAS_2026.csv encontrado
    for %%A in ("DADOS_SINARM\OCORRENCIAS\OCORRENCIAS_2026.csv") do (
        set size=%%~zA
        set /A sizeMB=%%~zA / 1048576
    )
    echo      Tamanho: ~%sizeMB% MB
) else (
    echo [AVISO] OCORRENCIAS_2026.csv nao encontrado!
)

echo.
echo Proximos passos:
echo 1. Execute: python validar_configuracao.py
echo 2. Se OK, execute: python 01_preparar_documentos.py
echo.

:fim
pause
