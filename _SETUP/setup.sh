#!/bin/bash
# ============================================================
# SCRIPT DE CONFIGURACAO AUTOMATICA - LINUX/MAC
# Agente Investigador SINARM E1
# ============================================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "============================================================"
echo "  CONFIGURACAO AUTOMATICA DO AMBIENTE"
echo "  Agente Investigador SINARM E1"
echo "============================================================"
echo ""

# Funcao para mensagens de erro
error_exit() {
    echo -e "${RED}[ERRO]${NC} $1"
    exit 1
}

# Funcao para avisos
warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

# Funcao para sucesso
success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

# Funcao para info
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# [1/6] Verificar se Python esta instalado
echo "[1/6] Verificando instalacao do Python..."

if ! command -v python3 &> /dev/null; then
    error_exit "Python3 nao encontrado!

Por favor, instale Python 3.8 ou superior:

Ubuntu/Debian:
  sudo apt update
  sudo apt install python3 python3-pip python3-venv

macOS (usando Homebrew):
  brew install python3

Fedora/RHEL:
  sudo dnf install python3 python3-pip
"
fi

# Verificar versao do Python
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

info "Python encontrado: $PYTHON_VERSION"

# Verificar versao minima (Python 3.8+)
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    error_exit "Versao do Python muito antiga!
Versao atual: $PYTHON_VERSION
Versao minima: 3.8

Por favor, atualize o Python."
fi

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]; then
    warning "Versao do Python pode ser antiga!"
    warning "Versao atual: $PYTHON_VERSION"
    warning "Versao recomendada: 3.10+"
    echo ""
    read -p "Continuar mesmo assim? (s/N): " CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Ss]$ ]]; then
        exit 0
    fi
fi

success "Versao do Python compativel: $PYTHON_VERSION"
echo ""

# [2/6] Verificar se ja existe venv
echo "[2/6] Verificando ambiente virtual..."

if [ -d "venv" ]; then
    warning "Ambiente virtual ja existe!"
    echo ""
    read -p "Deseja recria-lo? (s/N) [Recomendado se houver problemas]: " RECREATE
    if [[ "$RECREATE" =~ ^[Ss]$ ]]; then
        echo ""
        info "Removendo ambiente virtual antigo..."
        rm -rf venv
        success "Ambiente virtual removido"
    else
        echo ""
        info "Pulando criacao do ambiente virtual..."
        # Verificar se o venv esta funcional
        if [ ! -f "venv/bin/activate" ]; then
            error_exit "Ambiente virtual existente esta corrompido. Delete a pasta venv e execute novamente."
        fi
    fi
fi

# Criar ambiente virtual se nao existir
if [ ! -d "venv" ]; then
    info "Criando ambiente virtual..."
    
    # Verificar se python3-venv esta instalado
    if ! python3 -m venv --help &> /dev/null; then
        error_exit "Modulo venv nao encontrado!

Ubuntu/Debian:
  sudo apt install python3-venv

Fedora/RHEL:
  sudo dnf install python3-virtualenv
"
    fi
    
    python3 -m venv venv || error_exit "Falha ao criar ambiente virtual!"
    success "Ambiente virtual criado"
fi
echo ""

# [3/6] Ativar ambiente virtual
echo "[3/6] Ativando ambiente virtual..."
source venv/bin/activate || error_exit "Falha ao ativar ambiente virtual!"
success "Ambiente virtual ativado"
echo ""

# [4/6] Atualizar pip
echo "[4/6] Atualizando pip..."
python -m pip install --upgrade pip --quiet
if [ $? -eq 0 ]; then
    success "pip atualizado"
else
    warning "Falha ao atualizar pip, continuando..."
fi
echo ""

# [5/6] Instalar dependencias
echo "[5/6] Instalando dependencias do projeto..."
echo "Isso pode levar alguns minutos..."
echo ""

pip install -r requirements.txt
if [ $? -ne 0 ]; then
    error_exit "Falha ao instalar dependencias!

Tente manualmente:
  1. source venv/bin/activate
  2. pip install -r requirements.txt
"
fi

echo ""
success "Dependencias instaladas"
echo ""

# [6/6] Verificar instalacao
echo "[6/6] Verificando instalacao..."
python verify_setup.py
if [ $? -ne 0 ]; then
    warning "Alguns componentes podem nao estar funcionando corretamente."
    warning "Verifique os erros acima."
    echo ""
else
    echo ""
    success "Instalacao verificada com sucesso!"
fi
echo ""

# Verificar Ollama
echo "============================================================"
echo "  VERIFICANDO OLLAMA"
echo "============================================================"
echo ""

if ! command -v ollama &> /dev/null; then
    warning "Ollama nao encontrado!"
    echo ""
    echo "O agente precisa do Ollama para funcionar."
    echo ""
    echo "1. Baixe em: https://ollama.ai"
    echo ""
    echo "Linux:"
    echo "  curl -fsSL https://ollama.ai/install.sh | sh"
    echo ""
    echo "macOS:"
    echo "  brew install ollama"
    echo "  ou baixe o instalador em https://ollama.ai"
    echo ""
    echo "2. Execute: ollama pull llama3"
    echo ""
else
    success "Ollama instalado"
    echo ""
    
    info "Verificando modelo llama3..."
    if ollama list | grep -q llama3; then
        success "Modelo llama3 disponivel"
    else
        warning "Modelo llama3 nao encontrado!"
        echo ""
        echo "Execute: ollama pull llama3"
        echo ""
    fi
fi
echo ""

# Finalizar
echo "============================================================"
echo "  CONFIGURACAO CONCLUIDA!"
echo "============================================================"
echo ""
echo -e "${GREEN}Ambiente virtual criado e ativado com sucesso!${NC}"
echo ""
echo "PROXIMOS PASSOS:"
echo ""
echo "1. Para ATIVAR o ambiente virtual (sempre que abrir novo terminal):"
echo -e "   ${BLUE}source venv/bin/activate${NC}"
echo ""
echo "2. Para TESTAR o agente:"
echo -e "   ${BLUE}python E1_agente_react_v3.py${NC}"
echo ""
echo "3. Para executar os TESTES:"
echo -e "   ${BLUE}python TESTES_COMPLETOS.py${NC}"
echo ""
echo "4. Para DESATIVAR o ambiente virtual:"
echo -e "   ${BLUE}deactivate${NC}"
echo ""
echo "============================================================"
echo ""
