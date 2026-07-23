@echo off
REM ========================================================================
REM EXECUCAO AUTOMATICA COMPLETA - E4 RAG + FAISS
REM Cria venv, instala dependencias e executa pipeline completo
REM ========================================================================

echo.
echo ========================================================================
echo   E4 RAG + FAISS - EXECUCAO AUTOMATICA COMPLETA
echo ========================================================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Instale Python 3.11+ de: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version
echo.

REM ========================================================================
REM PASSO 1: CRIAR AMBIENTE VIRTUAL
REM ========================================================================

echo ========================================================================
echo PASSO 1: CRIANDO AMBIENTE VIRTUAL (venv)
echo ========================================================================
echo.

if exist "venv" (
    echo [AVISO] Pasta venv ja existe!
    choice /C SN /M "Deseja recriar o ambiente virtual? (S=Sim, N=Nao)"
    if errorlevel 2 goto ativar_venv
    if errorlevel 1 (
        echo Removendo venv antigo...
        rmdir /S /Q venv
    )
)

echo Criando ambiente virtual...
python -m venv venv

if errorlevel 1 (
    echo [ERRO] Falha ao criar venv!
    pause
    exit /b 1
)

echo [OK] Ambiente virtual criado!
echo.

REM ========================================================================
REM PASSO 2: ATIVAR AMBIENTE VIRTUAL
REM ========================================================================

:ativar_venv

echo ========================================================================
echo PASSO 2: ATIVANDO AMBIENTE VIRTUAL
echo ========================================================================
echo.

call venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERRO] Falha ao ativar venv!
    pause
    exit /b 1
)

echo [OK] Ambiente virtual ativado!
echo Prompt deve mostrar: (venv)
echo.

REM ========================================================================
REM PASSO 3: ATUALIZAR PIP
REM ========================================================================

echo ========================================================================
echo PASSO 3: ATUALIZANDO PIP
echo ========================================================================
echo.

python -m pip install --upgrade pip --quiet

echo [OK] pip atualizado!
echo.

REM ========================================================================
REM PASSO 4: INSTALAR DEPENDENCIAS
REM ========================================================================

echo ========================================================================
echo PASSO 4: INSTALANDO DEPENDENCIAS (requirements.txt)
echo ========================================================================
echo.
echo Isso pode demorar 5-10 minutos na primeira vez...
echo.

if not exist "requirements.txt" (
    echo [ERRO] Arquivo requirements.txt nao encontrado!
    pause
    exit /b 1
)

pip install -r requirements.txt

if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo [OK] Todas as dependencias instaladas!
echo.

REM ========================================================================
REM PASSO 5: VERIFICAR AMBIENTE
REM ========================================================================

echo ========================================================================
echo PASSO 5: VERIFICANDO AMBIENTE
echo ========================================================================
echo.

if exist "utilitarios\verificar_ambiente.py" (
    python utilitarios\verificar_ambiente.py
    
    if errorlevel 1 (
        echo.
        echo [AVISO] Ambiente com problemas!
        echo Verifique os erros acima antes de continuar.
        echo.
        choice /C SN /M "Deseja continuar mesmo assim? (S=Sim, N=Nao)"
        if errorlevel 2 exit /b 1
    )
) else (
    echo [AVISO] Script verificar_ambiente.py nao encontrado. Pulando verificacao.
)

echo.

REM ========================================================================
REM PASSO 6: VERIFICAR DADOS SINARM
REM ========================================================================

echo ========================================================================
echo PASSO 6: VERIFICANDO DADOS SINARM
echo ========================================================================
echo.

if not exist "DADOS_SINARM\OCORRENCIAS\OCORRENCIAS_2026.csv" (
    echo [ERRO] Dados SINARM nao encontrados!
    echo.
    echo Esperado: DADOS_SINARM\OCORRENCIAS\OCORRENCIAS_2026.csv
    echo.
    
    if exist "utilitarios\copiar_dados_sinarm.bat" (
        choice /C SN /M "Deseja executar copiar_dados_sinarm.bat agora? (S=Sim, N=Nao)"
        if errorlevel 2 exit /b 1
        if errorlevel 1 (
            call utilitarios\copiar_dados_sinarm.bat
        )
    ) else (
        echo Copie a pasta DADOS_SINARM para este diretorio e execute novamente.
        pause
        exit /b 1
    )
)

echo [OK] Dados SINARM encontrados!
echo.

REM ========================================================================
REM PASSO 7: LIMPAR OUTPUTS ANTERIORES (OPCIONAL)
REM ========================================================================

echo ========================================================================
echo PASSO 7: LIMPEZA DE OUTPUTS ANTERIORES
echo ========================================================================
echo.

if exist "03_outputs" (
    echo Pasta 03_outputs ja existe.
    choice /C SN /M "Deseja limpar outputs anteriores? (S=Sim, N=Nao)"
    if errorlevel 1 (
        echo Removendo 03_outputs...
        rmdir /S /Q 03_outputs
        echo [OK] Outputs anteriores removidos!
    )
)

echo.

REM ========================================================================
REM PASSO 8: EXECUTAR PIPELINE RAG (4 SCRIPTS)
REM ========================================================================

echo ========================================================================
echo PASSO 8: EXECUTANDO PIPELINE RAG COMPLETO
echo ========================================================================
echo.
echo Serao executados 4 scripts na sequencia:
echo   1. scripts_pipeline\01_preparar_documentos.py
echo   2. scripts_pipeline\02_gerar_embeddings.py
echo   3. scripts_pipeline\03_criar_indice_faiss.py
echo   4. scripts_pipeline\04_testar_retrieval.py
echo.
echo Tempo estimado: ~30 segundos (primeira vez: ~1 minuto)
echo.
pause

REM --- Script 1: Preparar Documentos ---

echo.
echo ------------------------------------------------------------------------
echo [1/4] EXECUTANDO: scripts_pipeline\01_preparar_documentos.py
echo ------------------------------------------------------------------------
echo.

python scripts_pipeline\01_preparar_documentos.py

if errorlevel 1 (
    echo.
    echo [ERRO] Script 1 falhou! Verifique o erro acima.
    pause
    exit /b 1
)

echo.
echo [OK] Script 1 concluido!
echo.
pause

REM --- Script 2: Gerar Embeddings ---

echo.
echo ------------------------------------------------------------------------
echo [2/4] EXECUTANDO: scripts_pipeline\02_gerar_embeddings.py
echo ------------------------------------------------------------------------
echo.
echo ATENCAO: Primeira execucao faz download do modelo (~90 MB)
echo          Pode demorar 1-2 minutos...
echo.

python scripts_pipeline\02_gerar_embeddings.py

if errorlevel 1 (
    echo.
    echo [ERRO] Script 2 falhou! Verifique o erro acima.
    pause
    exit /b 1
)

echo.
echo [OK] Script 2 concluido!
echo.
pause

REM --- Script 3: Criar Indice FAISS ---

echo.
echo ------------------------------------------------------------------------
echo [3/4] EXECUTANDO: scripts_pipeline\03_criar_indice_faiss.py
echo ------------------------------------------------------------------------
echo.

python scripts_pipeline\03_criar_indice_faiss.py

if errorlevel 1 (
    echo.
    echo [ERRO] Script 3 falhou! Verifique o erro acima.
    pause
    exit /b 1
)

echo.
echo [OK] Script 3 concluido!
echo.
pause

REM --- Script 4: Testar Retrieval ---

echo.
echo ------------------------------------------------------------------------
echo [4/4] EXECUTANDO: scripts_pipeline\04_testar_retrieval.py
echo ------------------------------------------------------------------------
echo.

python scripts_pipeline\04_testar_retrieval.py

if errorlevel 1 (
    echo.
    echo [ERRO] Script 4 falhou! Verifique o erro acima.
    pause
    exit /b 1
)

echo.
echo [OK] Script 4 concluido!
echo.

REM ========================================================================
REM CONCLUSAO
REM ========================================================================

echo.
echo ========================================================================
echo   PIPELINE RAG COMPLETO EXECUTADO COM SUCESSO!
echo ========================================================================
echo.
echo Arquivos gerados em: 03_outputs\
echo   - documentos.json
echo   - metadados.json
echo   - embeddings.npy
echo   - faiss_index.bin
echo   - index_config.json
echo.
echo ========================================================================
echo   PROXIMO PASSO: Testar agente v4.5
echo ========================================================================
echo.
echo Para testar o agente com RAG:
echo   python scripts_agente\agente_v4_5_rag.py
echo.
echo Para desativar o ambiente virtual:
echo   deactivate
echo.
echo ========================================================================

pause
