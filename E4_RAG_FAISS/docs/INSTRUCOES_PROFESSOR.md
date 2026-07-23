# EXECUÇÃO AUTOMÁTICA - INSTRUÇÕES PARA O ROTEIRO DA AULA

## 📋 VISÃO GERAL

Para facilitar a execução na aula, criamos **2 scripts automáticos** que fazem TUDO:
- ✅ Criar ambiente virtual (venv)
- ✅ Instalar dependências (requirements.txt)
- ✅ Verificar ambiente (Python, bibliotecas, Ollama)
- ✅ Executar pipeline RAG completo (4 scripts)

## 🚀 SCRIPTS DISPONÍVEIS

### 1. `executar_completo.bat` (Windows - CMD)
```batch
executar_completo.bat
```

### 2. `executar_completo.ps1` (Windows - PowerShell)
```powershell
.\executar_completo.ps1
```

**Recomendação:** Use `.bat` (CMD) por ser mais compatível com todos os Windows.

---

## 📝 O QUE O SCRIPT FAZ (PASSO A PASSO)

### PASSO 1: Verificar Python
- Checa se Python 3.11+ está instalado
- Exibe versão encontrada

### PASSO 2: Criar Ambiente Virtual (venv)
```
python -m venv venv
```
- Se `venv` já existe, pergunta se quer recriar
- Cria pasta `venv/` no diretório atual

### PASSO 3: Ativar Ambiente Virtual
```
venv\Scripts\activate.bat
```
- Prompt muda para: `(venv) E:\...\03_CODIGOS_PRONTOS>`

### PASSO 4: Atualizar pip
```
python -m pip install --upgrade pip
```

### PASSO 5: Instalar Dependências
```
pip install -r requirements.txt
```
- ⏱️ **Tempo:** 5-10 minutos (primeira vez)
- Instala: numpy, pandas, torch, sentence-transformers, faiss-cpu, langchain, etc.

### PASSO 6: Verificar Ambiente
```
python verificar_ambiente.py
```
- Valida Python 3.11+
- Verifica bibliotecas instaladas
- Testa Ollama 0.3.2.1
- Confirma modelo llama3

### PASSO 7: Verificar Dados SINARM
- Checa se existe: `DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026.csv`
- Se não existir, oferece executar `copiar_dados_sinarm.bat`

### PASSO 8: Limpar Outputs Anteriores (OPCIONAL)
- Pergunta se quer remover pasta `03_outputs/`
- Útil para demonstrar pipeline do zero

### PASSO 9: Executar Pipeline RAG (4 scripts)

#### 9.1 - Script 1: Preparar Documentos
```
python 01_preparar_documentos.py
```
- ⏱️ **Tempo:** ~4 segundos
- **Output:** `03_outputs/documentos.json`, `03_outputs/metadados.json`
- **Resultado:** 1.000 documentos textuais criados

#### 9.2 - Script 2: Gerar Embeddings
```
python 02_gerar_embeddings.py
```
- ⏱️ **Tempo:** ~8 segundos (primeira vez: +download modelo ~90 MB)
- **Output:** `03_outputs/embeddings.npy`
- **Resultado:** 1.000 vetores de 384 dimensões

#### 9.3 - Script 3: Criar Índice FAISS
```
python 03_criar_indice_faiss.py
```
- ⏱️ **Tempo:** ~1 segundo
- **Output:** `03_outputs/faiss_index.bin`, `03_outputs/index_config.json`
- **Resultado:** Índice FAISS com 1.000 vetores indexados

#### 9.4 - Script 4: Testar Retrieval
```
python 04_testar_retrieval.py
```
- ⏱️ **Tempo:** ~2 segundos
- **Output:** Exibe no console (top-3 documentos relevantes)
- **Resultado:** Testa busca semântica com query de exemplo

---

## 🎯 INTEGRAÇÃO NO ROTEIRO DA AULA

### OPÇÃO A: Execução Automática (Recomendado para aula)
**Tempo total:** ~10-15 minutos

```
PROFESSOR [digita no terminal]:
> executar_completo.bat

[Script executa tudo automaticamente]
[Professor explica cada etapa enquanto roda]
```

**Vantagens:**
- ✅ Rápido e sem erro
- ✅ Alunos veem output correto
- ✅ Garante ambiente padronizado
- ✅ Sobra mais tempo para explicar conceitos

**Quando usar:**
- Início da aula (setup)
- Ambiente novo (primeira vez)
- Alunos com dificuldade técnica

---

### OPÇÃO B: Execução Manual Line-by-Line (Live Coding)
**Tempo total:** ~40-50 minutos

```
PROFESSOR [digita cada comando]:
> python -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt
> python 01_preparar_documentos.py
> python 02_gerar_embeddings.py
> python 03_criar_indice_faiss.py
> python 04_testar_retrieval.py
```

**Vantagens:**
- ✅ Alunos aprendem cada comando
- ✅ Professor pode pausar e explicar
- ✅ Debugging ao vivo (se houver erro)

**Quando usar:**
- Aula com foco em infraestrutura
- Turma avançada
- Segunda execução (review)

---

### OPÇÃO C: Híbrido (MELHOR ESTRATÉGIA!)
**Tempo total:** ~20-25 minutos

**Setup automático + Explicação detalhada**

1. **Executar script automático** (10 min)
   ```
   > executar_completo.bat
   ```

2. **Professor explica durante execução:**
   - Enquanto instala dependências → explica o que é venv
   - Enquanto gera embeddings → explica sentence-transformers
   - Enquanto cria FAISS → explica índice vetorial

3. **Após conclusão, revisar outputs:**
   ```
   > dir 03_outputs
   ```
   - Abrir `documentos.json` (mostrar estrutura)
   - Explicar `embeddings.npy` (numpy array)
   - Mostrar `faiss_index.bin` (índice binário)

4. **Re-executar 1 script manualmente** (live coding)
   ```
   > python 04_testar_retrieval.py
   ```
   - Modificar query de teste no código
   - Rodar novamente
   - Mostrar diferentes resultados

**Vantagens:**
- ✅ Melhor custo-benefício (tempo vs. aprendizado)
- ✅ Setup rápido + exploração hands-on
- ✅ Alunos veem automação + entendimento profundo

---

## 📂 ESTRUTURA DE OUTPUTS PADRONIZADA

Todos os outputs ficam em **`03_outputs/`**:

```
03_CODIGOS_PRONTOS/
├── 03_outputs/                    ← PASTA DE OUTPUTS (criada automaticamente)
│   ├── documentos.json            ← Script 1: Lista de 1.000 documentos textuais
│   ├── metadados.json             ← Script 1: Metadados (IDs, timestamps)
│   ├── embeddings.npy             ← Script 2: 1.000 vetores × 384 dim (NumPy array)
│   ├── faiss_index.bin            ← Script 3: Índice FAISS (busca vetorial)
│   └── index_config.json          ← Script 3: Configuração do índice
│
├── DADOS_SINARM/                  ← DADOS DE ENTRADA (não são outputs)
│   └── OCORRENCIAS/
│       └── OCORRENCIAS_2026.csv   ← CSV original (74.758 registros)
│
├── executar_completo.bat          ← Script automático (CMD)
├── executar_completo.ps1          ← Script automático (PowerShell)
├── requirements.txt               ← Dependências
├── 01_preparar_documentos.py      ← Pipeline passo 1
├── 02_gerar_embeddings.py         ← Pipeline passo 2
├── 03_criar_indice_faiss.py       ← Pipeline passo 3
├── 04_testar_retrieval.py         ← Pipeline passo 4
└── ...
```

### ✅ Benefícios da Padronização

1. **Organização clara:**
   - Inputs: `DADOS_SINARM/`
   - Outputs: `03_outputs/`

2. **Fácil limpeza:**
   ```
   rmdir /S /Q 03_outputs
   ```
   Remove todos os outputs sem afetar código/dados

3. **Gitignore simples:**
   ```
   03_outputs/
   venv/
   ```

4. **Consistência entre scripts:**
   - Todos os scripts leem/escrevem na mesma pasta
   - Não há outputs espalhados pelo diretório

---

## 🎬 ROTEIRO SUGERIDO PARA AULA

### TIMING: 5 HORAS (300 minutos)

#### PARTE 1: TEORIA + SETUP (90 min)
- **[0-40 min]** Slides teóricos (RAG, embeddings, FAISS)
- **[40-50 min]** Mostrar estrutura do projeto
- **[50-70 min]** Executar `executar_completo.bat` (COM EXPLICAÇÕES)
- **[70-90 min]** Explorar outputs gerados

#### PARTE 2: LIVE CODING PIPELINE (90 min)
- **[90-110 min]** Re-executar Script 1 (linha por linha)
- **[110-130 min]** Re-executar Script 2 (modificar parâmetros)
- **[130-150 min]** Re-executar Script 3 (testar diferentes índices)
- **[150-180 min]** Re-executar Script 4 (queries personalizadas)

#### PARTE 3: INTEGRAÇÃO AGENTE (90 min)
- **[180-210 min]** Executar agente v4.5 com RAG
- **[210-240 min]** Comparar v4.0 vs v4.5 (alucinação)
- **[240-270 min]** Modificar tool RAG (top_k, threshold)

#### PARTE 4: PRÁTICA LIVRE + Q&A (40 min)
- **[270-290 min]** Alunos experimentam livremente
- **[290-300 min]** Dúvidas e encerramento

---

## 🐛 TROUBLESHOOTING

### Problema 1: Script não encontra Python
```
[ERRO] Python nao encontrado!
```
**Solução:**
- Instalar Python 3.11+ de: https://www.python.org/downloads/
- Marcar opção "Add Python to PATH" no instalador
- Reiniciar terminal

### Problema 2: Erro ao instalar dependências
```
[ERRO] Falha ao instalar dependencias!
```
**Solução:**
- Verificar conexão com internet
- Atualizar pip: `python -m pip install --upgrade pip`
- Instalar manualmente: `pip install numpy pandas torch`

### Problema 3: Dados SINARM não encontrados
```
[ERRO] Dados SINARM nao encontrados!
```
**Solução:**
- Verificar estrutura: `DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026.csv`
- Executar: `copiar_dados_sinarm.bat`
- Ou copiar manualmente da pasta raiz E4_RAG_FAISS

### Problema 4: Ollama não encontrado
```
[ERRO] Ollama nao encontrado!
```
**Solução:**
- Instalar Ollama 0.3.2.1
- Baixar modelo: `ollama pull llama3`
- Verificar: `ollama list`

---

## 📌 CHECKLIST PRÉ-AULA (PROFESSOR)

### 1 dia antes da aula:
- [ ] Testar script completo em máquina limpa
- [ ] Verificar tempo real de execução
- [ ] Confirmar outputs gerados corretamente
- [ ] Preparar queries de exemplo alternativas

### 1 hora antes da aula:
- [ ] Abrir terminal em `03_CODIGOS_PRONTOS/`
- [ ] Verificar conexão internet (download modelo)
- [ ] Testar projetor (fonte grande: Ctrl + +)
- [ ] Ter backup: USB com requirements.txt offline

### Durante a aula:
- [ ] Executar script automático primeiro
- [ ] Explicar cada etapa durante execução
- [ ] Mostrar outputs em tempo real
- [ ] Pausar após cada script (checkpoint)

---

## 🎓 OBJETIVOS DE APRENDIZADO

Após execução automática + explicação, alunos devem:

1. ✅ Entender conceito de ambiente virtual (venv)
2. ✅ Saber instalar dependências (requirements.txt)
3. ✅ Compreender pipeline RAG (4 etapas)
4. ✅ Identificar inputs (CSV) vs outputs (03_outputs/)
5. ✅ Reconhecer estrutura de documentos/embeddings/índice
6. ✅ Conseguir re-executar pipeline sozinhos

---

## 📚 PRÓXIMOS PASSOS (APÓS EXECUÇÃO)

1. **Explorar outputs:**
   ```
   python
   >>> import json
   >>> with open('03_outputs/documentos.json') as f:
   ...     docs = json.load(f)
   >>> docs[0]
   ```

2. **Testar retrieval interativo:**
   - Modificar query em `04_testar_retrieval.py`
   - Rodar novamente
   - Comparar resultados

3. **Integrar com agente:**
   ```
   python agente_v4_5_rag.py
   ```

4. **Experimentos:**
   - Mudar `NUM_DOCS = 1000` para `5000`
   - Testar diferentes modelos de embedding
   - Comparar índices FAISS (Flat vs IVF)

---

## ✅ CONCLUSÃO

**Script automático = ferramenta pedagógica poderosa!**

- ✅ Garante setup correto (todos começam igual)
- ✅ Economiza tempo (foca em conceitos, não troubleshooting)
- ✅ Outputs padronizados (facilita suporte)
- ✅ Alunos podem replicar em casa

**Recomendação final:**
Use **OPÇÃO C (Híbrido)** no roteiro da aula:
1. Script automático (setup rápido)
2. Explicação conceitual (durante execução)
3. Re-execução manual (1-2 scripts para fixar)

---

**Criado para:** E4 - RAG + FAISS  
**Última atualização:** 2026-07-22  
**Testado em:** Windows 11, Python 3.11.9, Ollama 0.3.2.1
