# 🔧 TROUBLESHOOTING - Soluções para Problemas Comuns

**Última atualização:** 16/07/2026

---

## 📋 ÍNDICE RÁPIDO

1. [Problemas de Instalação](#1-problemas-de-instalação)
2. [Problemas de Ambiente Virtual](#2-problemas-de-ambiente-virtual)
3. [Problemas de Imports](#3-problemas-de-imports)
4. [Problemas com Ollama](#4-problemas-com-ollama)
5. [Problemas com Dados](#5-problemas-com-dados)
6. [Problemas de Path](#6-problemas-de-path)
7. [Problemas de Encoding](#7-problemas-de-encoding)
8. [Problemas de Performance](#8-problemas-de-performance)

---

## 1. PROBLEMAS DE INSTALAÇÃO

### ❌ Erro: "python não é reconhecido como comando"

**Windows:**
```bash
# Solução 1: Usar py (Python Launcher)
py --version
py -m venv venv

# Solução 2: Adicionar ao PATH
# 1. Procurar "Variáveis de Ambiente" no Windows
# 2. Editar PATH
# 3. Adicionar: C:\Users\[SEU_USUARIO]\AppData\Local\Programs\Python\Python310\
# 4. Reiniciar terminal
```

**Linux/macOS:**
```bash
# Usar python3
python3 --version
python3 -m venv venv
```

---

### ❌ Erro: "pip não encontrado"

```bash
# Windows
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# Linux
sudo apt install python3-pip

# macOS
python3 -m ensurepip --upgrade
```

---

### ❌ Erro: "SSL: CERTIFICATE_VERIFY_FAILED"

**Causa:** Proxy corporativo ou firewall bloqueando

**Solução:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

### ❌ Erro: "Permission denied" ao instalar

**Linux/macOS:**
```bash
# NÃO usar sudo com pip
# Criar venv primeiro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 2. PROBLEMAS DE AMBIENTE VIRTUAL

### ❌ Erro: "No module 'venv'"

**Linux/Ubuntu:**
```bash
sudo apt update
sudo apt install python3.10-venv
```

**Verificar depois:**
```bash
python3 -m venv venv
```

---

### ❌ Ambiente virtual não ativa (Windows)

**Erro:**
```
venv\Scripts\activate : File cannot be loaded because running scripts is disabled
```

**Solução:**
```powershell
# Abrir PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Tentar novamente
venv\Scripts\activate
```

**Alternativa (CMD):**
```bash
venv\Scripts\activate.bat
```

---

### ❌ (venv) não aparece no prompt

**Verificar se está ativado:**
```bash
# Windows
where python
# Deve mostrar: ...\venv\Scripts\python.exe

# Linux/macOS
which python
# Deve mostrar: .../venv/bin/python
```

**Se não estiver:**
```bash
# Ativar novamente
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

---

## 3. PROBLEMAS DE IMPORTS

### ❌ Erro: "No module named 'langchain'"

**Causa 1:** Ambiente virtual não ativado

**Solução:**
```bash
# Verificar se (venv) aparece no prompt
# Se não:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

**Causa 2:** Dependências não instaladas

**Solução:**
```bash
pip install -r requirements.txt
```

**Causa 3:** Ambiente virtual corrompido

**Solução:**
```bash
# Deletar venv
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Recriar
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### ❌ Erro: "No module named 'utils'"

**Causa:** Script não está configurando PATH corretamente

**Solução:**
```python
# No script, adicionar/corrigir:
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Ajustar número
sys.path.insert(0, str(PROJECT_ROOT))

# Agora importar
from utils.tools_sinarm import buscar_ocorrencias
```

**Verificar estrutura:**
```
03_CODIGOS_PRONTOS/           ← PROJECT_ROOT
├── utils/
│   └── tools_sinarm.py
└── E2_QUALIDADE_E_MEMORIA/
    └── solucao_final/
        └── agente_v2.0.py    ← Seu script (2 níveis acima de PROJECT_ROOT)
```

---

### ❌ Erro: "cannot import name 'OllamaLLM'"

**Causa:** Versão errada de langchain-ollama

**Solução:**
```bash
pip uninstall langchain-ollama
pip install langchain-ollama>=0.1.0
```

---

## 4. PROBLEMAS COM OLLAMA

### ❌ Erro: "Ollama connection refused"

**Causa:** Ollama não está rodando

**Solução:**
```bash
# Terminal separado
ollama serve
```

**Verificar se está rodando:**
```bash
curl http://localhost:11434
# Deve retornar: Ollama is running
```

---

### ❌ Erro: "Model llama3 not found"

**Causa:** Modelo não foi baixado

**Solução:**
```bash
ollama pull llama3
```

⏱️ Atenção: Download de ~4GB, pode demorar 10-30 min

**Verificar modelos instalados:**
```bash
ollama list
```

---

### ❌ Ollama muito lento

**Causa 1:** Hardware limitado (RAM < 8GB)

**Solução:** Usar modelo menor
```bash
ollama pull llama3:8b  # Mais leve
# Ou
ollama pull phi  # Muito leve (~2GB)
```

**Causa 2:** GPU não detectada

**Solução:**
```bash
# Verificar GPU
nvidia-smi  # Linux
# Se não tiver GPU, Ollama usa CPU (mais lento, mas funciona)
```

---

### ❌ Erro: "Ollama timeout"

**Causa:** Query muito complexa ou modelo sobrecarregado

**Solução no código:**
```python
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3",
    temperature=0,
    timeout=120  # Aumentar timeout (padrão: 60s)
)
```

---

## 5. PROBLEMAS COM DADOS

### ❌ Erro: "FileNotFoundError: DADOS_SINARM/"

**Causa:** Pasta de dados não está no local correto

**Solução:**
```bash
# Verificar estrutura
ls DADOS_SINARM  # Linux/macOS
dir DADOS_SINARM  # Windows

# Deve mostrar:
# OCORRENCIAS/
# PORTES/
# REGISTROS/
# REQUERIMENTOS/
```

**Se não existir:**
1. Baixar ZIP dos dados (instrutor fornece)
2. Extrair na raiz de `03_CODIGOS_PRONTOS/`

---

### ❌ Erro: "EmptyDataError" ao ler CSV

**Causa 1:** Arquivo CSV corrompido ou vazio

**Solução:**
```bash
# Verificar tamanho
ls -lh DADOS_SINARM/REGISTROS/*.csv  # Linux/macOS
dir DADOS_SINARM\REGISTROS\*.csv  # Windows

# Se 0 bytes: redownload dados
```

**Causa 2:** Encoding errado

**Solução no código:**
```python
df = pd.read_csv(
    arquivo,
    sep=';',
    encoding='latin1',  # Tentar: latin1, utf-8, cp1252
    on_bad_lines='skip'  # Pular linhas problemáticas
)
```

---

### ❌ Erro: "UnicodeDecodeError"

**Solução:**
```python
import pandas as pd

df = pd.read_csv(
    arquivo,
    sep=';',
    encoding='latin1',  # Encoding correto para SINARM
    low_memory=False
)
```

---

## 6. PROBLEMAS DE PATH

### ❌ Erro: "No such file or directory"

**Causa:** Path relativo errado

**Solução:**
```python
from pathlib import Path

# ERRADO (não use string hardcoded)
path = "E:\documentos\..."

# CERTO (use Path relativo)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
path = PROJECT_ROOT / "DADOS_SINARM" / "REGISTROS" / "arquivo.csv"
```

---

### ❌ Path com espaços não funciona

**Solução:**
```python
# Path com espaços
path = Path("C:/Users/João Silva/projeto")  # OK
# Ou
path = Path(r"C:\Users\João Silva\projeto")  # OK (raw string)
```

---

## 7. PROBLEMAS DE ENCODING

### ❌ Caracteres estranhos no output (�, ?, etc.)

**Causa:** Encoding errado no Windows

**Solução no script:**
```python
import sys
import io
import os

# Fix encoding Windows (adicionar no início)
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.version_info >= (3, 7):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

---

### ❌ Erro ao imprimir acentos

**Solução:**
```python
# Forçar encoding UTF-8
print("São Paulo")  # Deve funcionar após fix acima
```

---

## 8. PROBLEMAS DE PERFORMANCE

### ❌ Script muito lento (> 60s)

**Causa 1:** Carregamento repetido de CSVs grandes

**Solução:**
```python
# Usar cache
from functools import lru_cache

@lru_cache(maxsize=1)
def carregar_registros():
    return pd.read_csv(...)

# Chamar uma vez
df = carregar_registros()
```

**Causa 2:** Query LLM muito complexa

**Solução:**
```python
# Simplificar prompt
# Reduzir exemplos Few-Shot de 10 para 3-5
# Usar modelo menor (phi em vez de llama3)
```

---

### ❌ Consumo alto de memória

**Causa:** DataFrames grandes não liberados

**Solução:**
```python
# Carregar apenas colunas necessárias
df = pd.read_csv(
    arquivo,
    usecols=['ESPECIE_ARMA', 'MARCA_ARMA', 'TOTAL']  # Apenas necessárias
)

# Liberar memória após uso
del df
import gc
gc.collect()
```

---

## 🆘 PROBLEMAS NÃO LISTADOS?

### 1. Verificar logs

```bash
cat logs/agente_v2.0.log  # Linux/macOS
type logs\agente_v2.0.log  # Windows
```

### 2. Verificar versões

```bash
python --version
pip list | grep langchain
ollama --version
```

### 3. Testar ambiente limpo

```bash
# Criar novo venv
python -m venv venv_teste
venv_teste\Scripts\activate
pip install -r requirements.txt
python verify_setup.py
```

### 4. Buscar erro específico

```bash
# Copiar mensagem de erro exata
# Buscar no Google: "[mensagem de erro] python langchain"
```

### 5. Contatar suporte

**Informações a fornecer:**
- Sistema operacional (Windows 10/11, Ubuntu 22.04, macOS 13, etc.)
- Python version (`python --version`)
- Mensagem de erro completa
- Comando executado
- Arquivo `logs/` mais recente

---

## ✅ CHECKLIST DE DIAGNÓSTICO

Quando algo não funcionar, verificar nesta ordem:

1. [ ] Ambiente virtual ativado? (`(venv)` no prompt)
2. [ ] Python 3.10 ou 3.11? (`python --version`)
3. [ ] Dependências instaladas? (`pip list | grep langchain`)
4. [ ] DADOS_SINARM/ existe? (`ls DADOS_SINARM`)
5. [ ] Ollama rodando? (se usar LLM) (`curl localhost:11434`)
6. [ ] Modelo baixado? (se usar LLM) (`ollama list`)
7. [ ] Path correto no script? (verificar `PROJECT_ROOT`)
8. [ ] Logs sem erros? (`cat logs/*.log`)

---

**Última atualização:** 16/07/2026  
**Contribuições:** Adicionar novos problemas e soluções conforme surgem
