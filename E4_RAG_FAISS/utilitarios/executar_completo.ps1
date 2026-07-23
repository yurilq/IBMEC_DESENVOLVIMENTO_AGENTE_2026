# ========================================================================
# EXECUCAO AUTOMATICA COMPLETA - E4 RAG + FAISS (PowerShell)
# Cria venv, instala dependencias e executa pipeline completo
# ========================================================================

Write-Host ""
Write-Host "========================================================================"
Write-Host "  E4 RAG + FAISS - EXECUCAO AUTOMATICA COMPLETA"
Write-Host "========================================================================"
Write-Host ""

# Funcao para pause
function Pause-Script {
    Write-Host ""
    Write-Host "Pressione qualquer tecla para continuar..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Cyan

try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Python nao encontrado!" -ForegroundColor Red
    Write-Host "Instale Python 3.11+ de: https://www.python.org/downloads/"
    Pause-Script
    exit 1
}

Write-Host ""

# ========================================================================
# PASSO 1: CRIAR AMBIENTE VIRTUAL
# ========================================================================

Write-Host "========================================================================"
Write-Host "PASSO 1: CRIANDO AMBIENTE VIRTUAL (venv)"
Write-Host "========================================================================"
Write-Host ""

if (Test-Path "venv") {
    Write-Host "[AVISO] Pasta venv ja existe!" -ForegroundColor Yellow
    $resposta = Read-Host "Deseja recriar o ambiente virtual? (S/N)"
    
    if ($resposta -eq "S" -or $resposta -eq "s") {
        Write-Host "Removendo venv antigo..." -ForegroundColor Yellow
        Remove-Item -Path "venv" -Recurse -Force
    } else {
        Write-Host "Usando venv existente..." -ForegroundColor Cyan
        goto ativar_venv
    }
}

Write-Host "Criando ambiente virtual..." -ForegroundColor Cyan
python -m venv venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao criar venv!" -ForegroundColor Red
    Pause-Script
    exit 1
}

Write-Host "[OK] Ambiente virtual criado!" -ForegroundColor Green
Write-Host ""

# ========================================================================
# PASSO 2: ATIVAR AMBIENTE VIRTUAL
# ========================================================================

:ativar_venv

Write-Host "========================================================================"
Write-Host "PASSO 2: ATIVANDO AMBIENTE VIRTUAL"
Write-Host "========================================================================"
Write-Host ""

& "venv\Scripts\Activate.ps1"

Write-Host "[OK] Ambiente virtual ativado!" -ForegroundColor Green
Write-Host "Prompt deve mostrar: (venv)" -ForegroundColor Cyan
Write-Host ""

# ========================================================================
# PASSO 3: ATUALIZAR PIP
# ========================================================================

Write-Host "========================================================================"
Write-Host "PASSO 3: ATUALIZANDO PIP"
Write-Host "========================================================================"
Write-Host ""

python -m pip install --upgrade pip --quiet

Write-Host "[OK] pip atualizado!" -ForegroundColor Green
Write-Host ""

# ========================================================================
# PASSO 4: INSTALAR DEPENDENCIAS
# ========================================================================

Write-Host "========================================================================"
Write-Host "PASSO 4: INSTALANDO DEPENDENCIAS (requirements.txt)"
Write-Host "========================================================================"
Write-Host ""
Write-Host "Isso pode demorar 5-10 minutos na primeira vez..." -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path "requirements.txt")) {
    Write-Host "[ERRO] Arquivo requirements.txt nao encontrado!" -ForegroundColor Red
    Pause-Script
    exit 1
}

pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao instalar dependencias!" -ForegroundColor Red
    Pause-Script
    exit 1
}

Write-Host ""
Write-Host "[OK] Todas as dependencias instaladas!" -ForegroundColor Green
Write-Host ""

# ========================================================================
# PASSO 5: VERIFICAR AMBIENTE
# ========================================================================

Write-Host "========================================================================"
Write-Host "PASSO 5: VERIFICANDO AMBIENTE"
Write-Host "========================================================================"
Write-Host ""

if (Test-Path "verificar_ambiente.py") {
    python verificar_ambiente.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[AVISO] Ambiente com problemas!" -ForegroundColor Yellow
        Write-Host "Verifique os erros acima antes de continuar." -ForegroundColor Yellow
        Write-Host ""
        $resposta = Read-Host "Deseja continuar mesmo assim? (S/N)"
        if ($resposta -ne "S" -and $resposta -ne "s") {
            exit 1
        }
    }
} else {
    Write-Host "[AVISO] Script verificar_ambiente.py nao encontrado. Pulando..." -ForegroundColor Yellow
}

Write-Host ""

# ========================================================================
# PASSO 6: VERIFICAR DADOS SINARM
# ========================================================================

Write-Host "========================================================================"
Write-Host "PASSO 6: VERIFICANDO DADOS SINARM"
Write-Host "========================================================================"
Write-Host ""

if (-not (Test-Path "DADOS_SINARM\OCORRENCIAS\OCORRENCIAS_2026.csv")) {
    Write-Host "[ERRO] Dados SINARM nao encontrados!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Esperado: DADOS_SINARM\OCORRENCIAS\OCORRENCIAS_2026.csv"
    Write-Host ""
    
    if (Test-Path "copiar_dados_sinarm.bat") {
        $resposta = Read-Host "Deseja executar copiar_dados_sinarm.bat? (S/N)"
        if ($resposta -eq "S" -or $resposta -eq "s") {
            & ".\copiar_dados_sinarm.bat"
        } else {
            Write-Host "Copie a pasta DADOS_SINARM para este diretorio e execute novamente."
            Pause-Script
            exit 1
        }
    } else {
        Write-Host "Copie a pasta DADOS_SINARM para este diretorio e execute novamente."
        Pause-Script
        exit 1
    }
}

Write-Host "[OK] Dados SINARM encontrados!" -ForegroundColor Green
Write-Host ""

# ========================================================================
# PASSO 7: LIMPAR OUTPUTS ANTERIORES
# ========================================================================

Write-Host "========================================================================"
Write-Host "PASSO 7: LIMPEZA DE OUTPUTS ANTERIORES"
Write-Host "========================================================================"
Write-Host ""

if (Test-Path "03_outputs") {
    Write-Host "Pasta 03_outputs ja existe." -ForegroundColor Yellow
    $resposta = Read-Host "Deseja limpar outputs anteriores? (S/N)"
    
    if ($resposta -eq "S" -or $resposta -eq "s") {
        Write-Host "Removendo 03_outputs..." -ForegroundColor Yellow
        Remove-Item -Path "03_outputs" -Recurse -Force
        Write-Host "[OK] Outputs anteriores removidos!" -ForegroundColor Green
    }
}

Write-Host ""

# ========================================================================
# PASSO 8: EXECUTAR PIPELINE RAG
# ========================================================================

Write-Host "========================================================================"
Write-Host "PASSO 8: EXECUTANDO PIPELINE RAG COMPLETO"
Write-Host "========================================================================"
Write-Host ""
Write-Host "Serao executados 4 scripts na sequencia:" -ForegroundColor Cyan
Write-Host "  1. 01_preparar_documentos.py"
Write-Host "  2. 02_gerar_embeddings.py"
Write-Host "  3. 03_criar_indice_faiss.py"
Write-Host "  4. 04_testar_retrieval.py"
Write-Host ""
Write-Host "Tempo estimado: ~30 segundos (primeira vez: ~1 minuto)" -ForegroundColor Yellow
Write-Host ""
Pause-Script

# Lista de scripts
$scripts = @(
    @{Numero=1; Nome="01_preparar_documentos.py"; Descricao="Preparar Documentos"},
    @{Numero=2; Nome="02_gerar_embeddings.py"; Descricao="Gerar Embeddings"},
    @{Numero=3; Nome="03_criar_indice_faiss.py"; Descricao="Criar Indice FAISS"},
    @{Numero=4; Nome="04_testar_retrieval.py"; Descricao="Testar Retrieval"}
)

foreach ($script in $scripts) {
    Write-Host ""
    Write-Host "------------------------------------------------------------------------" -ForegroundColor Cyan
    Write-Host "[$($script.Numero)/4] EXECUTANDO: $($script.Nome)" -ForegroundColor Cyan
    Write-Host "------------------------------------------------------------------------" -ForegroundColor Cyan
    Write-Host ""
    
    if ($script.Numero -eq 2) {
        Write-Host "ATENCAO: Primeira execucao faz download do modelo (~90 MB)" -ForegroundColor Yellow
        Write-Host "         Pode demorar 1-2 minutos..." -ForegroundColor Yellow
        Write-Host ""
    }
    
    $startTime = Get-Date
    python $script.Nome
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[ERRO] Script $($script.Numero) falhou!" -ForegroundColor Red
        Write-Host "Verifique o erro acima." -ForegroundColor Red
        Pause-Script
        exit 1
    }
    
    Write-Host ""
    Write-Host "[OK] Script $($script.Numero) concluido! (Tempo: $([math]::Round($duration, 2))s)" -ForegroundColor Green
    Write-Host ""
    Pause-Script
}

# ========================================================================
# CONCLUSAO
# ========================================================================

Write-Host ""
Write-Host "========================================================================"
Write-Host "  PIPELINE RAG COMPLETO EXECUTADO COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================================================"
Write-Host ""
Write-Host "Arquivos gerados em: 03_outputs\" -ForegroundColor Cyan
Write-Host "  - documentos.json"
Write-Host "  - metadados.json"
Write-Host "  - embeddings.npy"
Write-Host "  - faiss_index.bin"
Write-Host "  - index_config.json"
Write-Host ""
Write-Host "========================================================================"
Write-Host "  PROXIMO PASSO: Testar agente v4.5" -ForegroundColor Yellow
Write-Host "========================================================================"
Write-Host ""
Write-Host "Para testar o agente com RAG:" -ForegroundColor Cyan
Write-Host "  python agente_v4_5_rag.py"
Write-Host ""
Write-Host "Para desativar o ambiente virtual:" -ForegroundColor Cyan
Write-Host "  deactivate"
Write-Host ""
Write-Host "========================================================================"

Pause-Script
