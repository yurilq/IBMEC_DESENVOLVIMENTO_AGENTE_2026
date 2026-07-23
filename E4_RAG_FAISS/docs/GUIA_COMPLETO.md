# 📚 GUIA COMPLETO - E4 RAG + FAISS

## 📑 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Requisitos e Ambiente Padronizado](#requisitos-e-ambiente-padronizado)
4. [Instalação e Configuração](#instalação-e-configuração)
5. [Execução do Pipeline](#execução-do-pipeline)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 VISÃO GERAL

Este projeto implementa um sistema completo de **RAG (Retrieval-Augmented Generation)** com **FAISS** para:
- Transformar dados SINARM em documentos pesquisáveis
- Gerar embeddings semânticos (vetores de 384 dimensões)
- Criar índice vetorial FAISS para busca rápida
- Integrar retrieval com agente conversacional

**Tempo estimado (setup completo):** 15-20 minutos

---

## 📂 ESTRUTURA DO PROJETO

```
03_CODIGOS_PRONTOS/
│
├── 📄 README.md                          ← Início rápido
├── 📄 requirements.txt                   ← Dependências Python
├── 🚀 executar_completo.bat              ← Script automático (RECOMENDADO!)
│
├── 📂 scripts_pipeline/                  ← Pipeline RAG (4 scripts)
│   ├── 01_preparar_documentos.py         ← CSV → documentos textuais
│   ├── 02_gerar_embeddings.py            ← Documentos → vetores (384 dim)
│   ├── 03_criar_indice_faiss.py          ← Vetores → índice FAISS
│   └── 04_testar_retrieval.py            ← Testar busca semântica
│
├── 📂 scripts_agente/                    ← Agente v4.5 com RAG
│   ├── agente_v4_5_rag.py                ← Agente principal
│   ├── tool_rag_conceitual.py            ← Tool de retrieval
│   └── tools_basicas_v2.py               ← Tools SQL (contagens)
│
├── 📂 utilitarios/                       ← Scripts auxiliares
│   ├── verificar_ambiente.py             ← Valida Python, bibliotecas, Ollama
│   ├── executar_completo.ps1             ← Script automático (PowerShell)
│   └── copiar_dados_sinarm.bat           ← Copia dados SINARM
│
├── 📂 docs/                              ← Documentação extra
│   ├── SETUP_RAPIDO.md                   ← Guia rápido (5 min)
│   └── INSTRUCOES_PROFESSOR.md           ← Roteiro para aula
│
├── 📂 DADOS_SINARM/                      ← Dados de entrada
│   └── OCORRENCIAS/
│       └── OCORRENCIAS_2026.csv          ← 74.758 registros, 7.8 MB
│
└── 📂 03_outputs/                        ← Gerado automaticamente
    ├── documentos.json                   ← 1.000 documentos textuais
    ├── metadados.json                    ← IDs e metadados
    ├── embeddings.npy                    ← 1.000 × 384 vetores
    ├── faiss_index.bin                   ← Índice FAISS
    └── index_config.json                 ← Configuração do índice
```

---

## 🔧 REQUISITOS E AMBIENTE PADRONIZADO

### 🐍 Python 3.11+

**Verificar versão:**
```bash
python --version
```

**Resultado esperado:**
```
Python 3.11.x ou 3.12.x
```

**Se versão < 3.11:**
- Baixar: https://www.python.org/downloads/
- Instalar Python 3.11+
- Marcar opção: "Add Python to PATH"

---

### 📚 Bibliotecas Python (Versões Fixas)

**Arquivo:** `requirements.txt`

```
numpy==2.4.2
pandas==2.2.2
torch==2.13.0
sentence-transformers==3.1.1
faiss-cpu==1.14.3
langchain==1.3.13
langchain-community==0.4.2
langchain-core==1.4.9
langchain-ollama==1.3.0
```

**Por que versões fixas?**
- ✅ Evita erros de incompatibilidade
- ✅ Todos os alunos têm mesmo ambiente
- ✅ Facilita troubleshooting

---

### 🦙 Ollama 0.3.2.1

**Verificar versão:**
```bash
ollama --version
```

**Resultado esperado:**
```
ollama version is 0.3.2.1
```

**Instalar:**
- Download: https://ollama.ai/download
- Versão específica: 0.3.2.1

---

### 🤖 Modelo llama3

**Verificar modelo:**
```bash
ollama list
```

**Resultado esperado:**
```
NAME            ID              SIZE
llama3:latest   365c0bd3c000    4.7 GB
```

**Baixar modelo:**
```bash
ollama pull llama3
```

---

## 🚀 INSTALAÇÃO E CONFIGURAÇÃO

### OPÇÃO A: Execução Automática (RECOMENDADO!)

**Tempo:** ~10-15 minutos

```bash
# Executar script automático
executar_completo.bat
```

**O script faz TUDO:**
1. ✅ Cria ambiente virtual (venv)
2. ✅ Instala dependências (requirements.txt)
3. ✅ Verifica ambiente (Python, bibliotecas, Ollama)
4. ✅ Executa pipeline RAG completo (4 scripts)

**Vantagens:**
- Rápido e sem erro
- Garante ambiente padronizado
- Ideal para aula (economiza tempo)

---

### OPÇÃO B: Instalação Manual (Passo a Passo)

**Tempo:** ~20-30 minutos

#### 1. Criar Ambiente Virtual

```bash
python -m venv venv
```

#### 2. Ativar Ambiente Virtual

**Windows (CMD/PowerShell):**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Confirmação:** Prompt muda para `(venv) ...`

#### 3. Atualizar pip

```bash
python -m pip install --upgrade pip
```

#### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Tempo:** 5-10 minutos (download + instalação)

#### 5. Verificar Ambiente

```bash
python utilitarios/verificar_ambiente.py
```

**Output esperado:**
```
✅ Python 3.11+ detectado
✅ Bibliotecas instaladas corretamente
✅ Ollama 0.3.2.1 detectado
✅ Modelo llama3 encontrado
```

#### 6. Verificar Dados SINARM

```bash
dir DADOS_SINARM\OCORRENCIAS\OCORRENCIAS_2026.csv
```

**Se não existir:**
```bash
utilitarios\copiar_dados_sinarm.bat
```

---

## 🔄 EXECUÇÃO DO PIPELINE

### Pipeline RAG (4 Scripts)

Execute na ordem:

#### 1️⃣ Preparar Documentos

```bash
python scripts_pipeline/01_preparar_documentos.py
```

**Função:** CSV → documentos textuais  
**Tempo:** ~4 segundos  
**Output:**
- `03_outputs/documentos.json` (1.000 documentos)
- `03_outputs/metadados.json` (IDs, timestamps)

**Exemplo de documento gerado:**
```
Boletim de Ocorrência nº BO-42735:
- Município: SÃO PAULO
- Delegacia: 12ª DP PINHEIROS
- Tipo de Ocorrência: Furto
- Arma: PISTOLA
- Marca: TAURUS
- Calibre: .380
- Data: 2026-03-15
```

---

#### 2️⃣ Gerar Embeddings

```bash
python scripts_pipeline/02_gerar_embeddings.py
```

**Função:** Documentos → vetores semânticos  
**Tempo:** ~8 segundos (primeira vez: +download modelo ~90 MB)  
**Output:**
- `03_outputs/embeddings.npy` (1.000 vetores × 384 dimensões)

**Modelo usado:** `sentence-transformers/all-MiniLM-L6-v2`
- Dimensões: 384
- Tamanho: ~90 MB
- Velocidade: rápido (CPU)

---

#### 3️⃣ Criar Índice FAISS

```bash
python scripts_pipeline/03_criar_indice_faiss.py
```

**Função:** Vetores → índice de busca rápida  
**Tempo:** ~1 segundo  
**Output:**
- `03_outputs/faiss_index.bin` (índice binário)
- `03_outputs/index_config.json` (configuração)

**Tipo de índice:** IndexFlatL2 (busca exata por distância euclidiana)

---

#### 4️⃣ Testar Retrieval

```bash
python scripts_pipeline/04_testar_retrieval.py
```

**Função:** Testar busca semântica  
**Tempo:** ~2 segundos  
**Output:** Exibe top-3 documentos relevantes no console

**Query de teste padrão:**
```
"O que são armas apreendidas em São Paulo?"
```

**Output esperado:**
```
TOP 3 DOCUMENTOS RELEVANTES:

[1] Score: 0.65
Boletim de Ocorrência nº BO-12345:
- Município: SÃO PAULO
- Tipo de Ocorrência: Apreensão
...

[2] Score: 0.58
...
```

---

### Testar Agente v4.5 com RAG

```bash
python scripts_agente/agente_v4_5_rag.py
```

**Função:** Agente conversacional + RAG  
**Capacidades:**
- Perguntas conceituais → usa RAG (busca em documentos)
- Perguntas quantitativas → usa SQL tools (contagens)

**Exemplos de perguntas:**

```
[Conceitual - usa RAG]
"O que é BO de furto?"
"Explique o que são armas apreendidas"

[Quantitativa - usa SQL]
"Quantas armas Taurus?"
"Há mais Glock ou Taurus roubadas?"
```

---

## 🐛 TROUBLESHOOTING

### Problema 1: Python não encontrado

**Erro:**
```
'python' is not recognized as an internal or external command
```

**Solução:**
1. Instalar Python 3.11+ de: https://www.python.org/downloads/
2. **Importante:** Marcar "Add Python to PATH" no instalador
3. Reiniciar terminal
4. Verificar: `python --version`

---

### Problema 2: Erro ao instalar dependências

**Erro:**
```
ERROR: Could not install packages due to an OSError
```

**Soluções:**

**2.1 - Atualizar pip:**
```bash
python -m pip install --upgrade pip
```

**2.2 - Instalar com permissões:**
```bash
pip install -r requirements.txt --user
```

**2.3 - Verificar conexão internet:**
- Algumas bibliotecas são grandes (torch ~2 GB)
- Tentar em rede estável

**2.4 - Instalar manualmente (uma por vez):**
```bash
pip install numpy==2.4.2
pip install pandas==2.2.2
pip install torch==2.13.0
...
```

---

### Problema 3: Dados SINARM não encontrados

**Erro:**
```
FileNotFoundError: Pasta DADOS_SINARM não encontrada
```

**Solução:**

**3.1 - Verificar estrutura:**
```bash
dir DADOS_SINARM\OCORRENCIAS
```

Deve mostrar: `OCORRENCIAS_2026.csv`

**3.2 - Copiar dados:**
```bash
# Se estiver em 03_CODIGOS_PRONTOS:
utilitarios\copiar_dados_sinarm.bat

# Ou copiar manualmente:
# DE: E:\...\DISCIPLINA_1_DESENVOLVIMENTO_AGENTE\DADOS_SINARM
# PARA: E:\...\E4_RAG_FAISS\03_CODIGOS_PRONTOS\DADOS_SINARM
```

---

### Problema 4: Ollama não encontrado

**Erro:**
```
Connection refused: Ollama not running
```

**Solução:**

**4.1 - Verificar Ollama instalado:**
```bash
ollama --version
```

**4.2 - Iniciar Ollama:**

**Windows:**
- Ollama inicia automaticamente (serviço)
- Verificar: ícone Ollama na bandeja do sistema

**Linux/Mac:**
```bash
ollama serve
```

**4.3 - Testar conexão:**
```bash
ollama list
```

**4.4 - Baixar modelo llama3:**
```bash
ollama pull llama3
```

---

### Problema 5: Erro ao gerar embeddings (primeira vez)

**Erro:**
```
OSError: [E050] Can't find model 'sentence-transformers/all-MiniLM-L6-v2'
```

**Causa:** Primeira execução precisa baixar modelo (~90 MB)

**Solução:**
- Aguardar download completar (1-2 minutos)
- Verificar conexão internet
- Se falhar, executar novamente

**Cache do modelo:**
- Windows: `C:\Users\<seu_usuario>\.cache\torch\sentence_transformers\`
- Linux/Mac: `~/.cache/torch/sentence_transformers/`

---

### Problema 6: Scripts muito lentos

**Causa:** Processando muitos documentos (default: 1.000)

**Solução (reduzir para teste rápido):**

Editar `scripts_pipeline/01_preparar_documentos.py`:

```python
# Linha ~40
NUM_DOCS = 100  # Processar só 100 (muito rápido - ~1 segundo)
```

Para processar todos (~75k documentos):
```python
NUM_DOCS = len(df_ocorrencias)  # Processar todos (demora ~2-3 minutos)
```

**Comparação de tempo:**
| NUM_DOCS | Tempo Script 1 | Tempo Script 2 | Tempo Total |
|----------|----------------|----------------|-------------|
| 100      | ~1s            | ~2s            | ~5s         |
| 1.000    | ~4s            | ~8s            | ~15s        |
| 10.000   | ~40s           | ~80s           | ~2min       |
| 75.000   | ~5min          | ~10min         | ~20min      |

---

### Problema 7: Importação de módulos falha

**Erro:**
```
ModuleNotFoundError: No module named 'sentence_transformers'
```

**Causa:** Ambiente virtual não ativado OU dependências não instaladas

**Solução:**

**7.1 - Verificar venv ativo:**
- Prompt deve mostrar: `(venv) ...`
- Se não mostrar, ativar: `venv\Scripts\activate`

**7.2 - Verificar instalação:**
```bash
pip list | findstr sentence-transformers
```

**7.3 - Reinstalar:**
```bash
pip install sentence-transformers==3.1.1
```

---

## ✅ CHECKLIST DE VALIDAÇÃO

Antes de executar os scripts, verificar:

### Ambiente Python:
- [ ] Python 3.11+ instalado (`python --version`)
- [ ] Ambiente virtual criado (`venv/` existe)
- [ ] Ambiente virtual ativado (prompt mostra `(venv)`)
- [ ] pip atualizado (`python -m pip install --upgrade pip`)
- [ ] Dependências instaladas (`pip list`)

### Ollama:
- [ ] Ollama 0.3.2.1 instalado (`ollama --version`)
- [ ] Ollama rodando (ícone na bandeja do sistema)
- [ ] Modelo llama3 baixado (`ollama list`)

### Dados:
- [ ] Pasta `DADOS_SINARM/` existe
- [ ] Arquivo `DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026.csv` existe
- [ ] CSV tem ~7.8 MB (74.758 registros)

### Scripts:
- [ ] Pasta `scripts_pipeline/` com 4 scripts
- [ ] Pasta `scripts_agente/` com 3 scripts
- [ ] Script de validação executado: `python utilitarios/verificar_ambiente.py`

---

## 📊 TAMANHO DOS ARQUIVOS

### Dados de entrada:
- `OCORRENCIAS_2026.csv`: 7.8 MB (74.758 registros)

### Outputs (com NUM_DOCS=1000):
- `documentos.json`: ~250 KB
- `metadados.json`: ~90 KB
- `embeddings.npy`: ~1.5 MB
- `faiss_index.bin`: ~1.5 MB
- **Total:** ~3.5 MB

### Modelo sentence-transformers:
- `all-MiniLM-L6-v2`: ~90 MB (download único)

### Modelo Ollama:
- `llama3:latest`: ~4.7 GB

---

## 🎯 DICAS PARA AULA

### Para Professores:

1. **Executar setup automático no início:**
   ```bash
   executar_completo.bat
   ```
   - Economiza tempo
   - Garante que todos começam iguais

2. **Explicar durante execução:**
   - Enquanto instala → explicar venv
   - Enquanto gera embeddings → explicar sentence-transformers
   - Enquanto cria FAISS → explicar índice vetorial

3. **Checkpoints frequentes:**
   - Pausar após cada script
   - Mostrar outputs gerados
   - Perguntar se todos conseguiram

4. **Explorar outputs:**
   ```python
   import json
   with open('03_outputs/documentos.json') as f:
       docs = json.load(f)
   print(docs[0])  # Mostrar primeiro documento
   ```

### Para Alunos:

1. **Primeiro: ler README.md** (1 min)
2. **Depois: executar script automático** (10 min)
3. **Explorar outputs gerados** (5 min)
4. **Re-executar scripts manualmente** (10 min)
5. **Testar agente v4.5** (5 min)

---

## 📞 SUPORTE

**Problemas com setup?**
1. Executar: `python utilitarios/verificar_ambiente.py`
2. Consultar seção [Troubleshooting](#troubleshooting) acima
3. Verificar documentação: `docs/SETUP_RAPIDO.md`
4. Consultar professor/monitor

---

**Última atualização:** 22/07/2026  
**Versão:** 2.0 (estrutura reorganizada)  
**Testado em:** Windows 11, Python 3.11.9, Ollama 0.3.2.1
