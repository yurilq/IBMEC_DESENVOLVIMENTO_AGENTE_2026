# 🧹 PLANO DE LIMPEZA - E4_RAG_FAISS

## 🎯 OBJETIVO
Aplicar o padrão IBMEC criado no E3 para limpar e organizar o E4

---

## 📊 SITUAÇÃO ATUAL

### Números
- **Total de pastas:** 1.045 (incluindo venv)
- **Total de arquivos:** 9.290
- **Tamanho estimado:** ~200 MB

### Estrutura Atual
```
E4_RAG_FAISS/
├── DADOS_SINARM/
├── docs/ (18 arquivos)
├── scripts_agente/ (8 arquivos)
├── scripts_pipeline/ (4 arquivos)
├── utilitarios/ (3 arquivos)
├── venv/ ❌ DELETAR
└── 24 arquivos raiz
```

---

## 🗑️ ARQUIVOS PARA DELETAR

### 1. Ambiente Virtual
```
❌ venv/
```
**Motivo:** ~200 MB, não deve estar no Git

### 2. Cache Python
```
❌ **/__pycache__/
```

### 3. Arquivos de Ambiente
```
❌ .env (contém API keys)
```
**Manter:** .env.example

---

## 🔄 REORGANIZAÇÃO PARA PADRÃO IBMEC

### Estrutura Atual → Nova Estrutura

```
ATUAL:                          NOVO PADRÃO IBMEC:
├── docs/                       ├── 01_MATERIAL_TEORICO/
├── scripts_pipeline/           ├── 02_NOTEBOOK_PASSO_A_PASSO/
├── scripts_agente/             ├── 03_AGENTE_CONSOLIDADO/
├── utilitarios/                ├── 04_MATERIAL_APOIO/
├── DADOS_SINARM/               ├── DADOS_SINARM/
└── 24 arquivos raiz            └── Arquivos raiz essenciais
```

---

## 📁 NOVA ESTRUTURA DETALHADA

### 01_MATERIAL_TEORICO/
```
├── README.md (criar)
├── CONCEITOS_RAG.md (criar)
├── CONCEITOS_FAISS.md (criar)
├── CONCEITOS_EMBEDDINGS.md (criar)
└── COMPARACAO_LLMS_2026.md (mover de docs/)
```

### 02_NOTEBOOK_PASSO_A_PASSO/
```
├── E4_rag_faiss_pipeline.ipynb (criar)
├── E4_rag_faiss_agente.ipynb (criar)
└── README.md (criar)
```

### 03_AGENTE_CONSOLIDADO/
```
├── agente_v4_7_rag_fewshot_cot.py (mover)
├── tool_rag_tfidf.py (mover)
├── tools_basicas_v2.py (mover)
├── config_llm.py (mover)
├── requirements.txt (mover)
└── README.md (criar)
```

### 04_MATERIAL_APOIO/
```
├── FAQ_E4.md (criar)
├── TROUBLESHOOTING_E4.md (consolidar)
├── GUIA_ESCOLHA_LLM.md (mover de docs/)
├── IMPLEMENTACAO_MULTI_LLM.md (mover de docs/)
└── verificar_ambiente.py (mover de utilitarios/)
```

### DADOS_SINARM/
```
└── (manter como está)
```

---

## 🔒 ARQUIVOS PARA .GITIGNORE

### Material do Docente (não compartilhar)
```
# Documentação interna
ANALISE_*.md
JUSTIFICATIVA_*.md
ROTEIRO_*.md
RESUMO_EXECUTIVO_*.md
ATUALIZACAO_*.md
CORRECAO_*.md
SOLUCAO_*.md
COMUNICADO_*.md
GUIA_RAPIDO_DIA_DA_AULA.md

# Scripts de teste do docente
teste_*.py
testar_*.py

# Arquivos batch/scripts auxiliares
executar_completo.bat
executar_completo.ps1
copiar_dados_sinarm.bat

# Documentos internos (docs/)
docs/INSTRUCOES_PROFESSOR.md
docs/ANALISE_*.md
docs/EVOLUCAO_*.md
docs/RESUMO_*.md
docs/RELATORIO_*.md
docs/LICAO_*.md
docs/RESULTADOS_*.md
docs/RAG_*.md

# Versões antigas/deprecated
*_DEPRECATED.py
agente_v4_5_*.py
agente_v4_6_*.py
tool_rag_conceitual.py

# Ambiente
.env
venv/
__pycache__/
```

---

## ✅ ARQUIVOS PARA MANTER

### Arquivos Raiz Essenciais
```
✅ README.md (atualizar)
✅ requirements.txt
✅ .env.example
✅ .gitignore (atualizar)
✅ INDEX_E4.md (criar)
✅ 00_COMECE_AQUI_E4.md (criar)
```

### Scripts Pipeline (mover para 02_NOTEBOOK)
```
✅ 01_preparar_documentos.py
✅ 02_gerar_embeddings.py
✅ 03_criar_indice_faiss.py
✅ 04_testar_retrieval.py
```

### Scripts Agente (mover para 03_AGENTE)
```
✅ agente_v4_7_rag_fewshot_cot.py (versão final)
✅ tool_rag_tfidf.py
✅ tools_basicas_v2.py
✅ config_llm.py
```

---

## 🚀 PLANO DE EXECUÇÃO

### FASE 1: BACKUP
```powershell
# Criar backup completo
Copy-Item -Recurse "E4_RAG_FAISS" "E4_RAG_FAISS_BACKUP_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
```

### FASE 2: DELETAR
```powershell
# 1. Deletar venv
Remove-Item -Recurse -Force "venv"

# 2. Deletar cache
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# 3. Deletar .env
Remove-Item ".env" -ErrorAction SilentlyContinue
```

### FASE 3: CRIAR ESTRUTURA
```powershell
# Criar pastas padrão IBMEC
New-Item -ItemType Directory -Path "01_MATERIAL_TEORICO"
New-Item -ItemType Directory -Path "02_NOTEBOOK_PASSO_A_PASSO"
New-Item -ItemType Directory -Path "03_AGENTE_CONSOLIDADO"
New-Item -ItemType Directory -Path "04_MATERIAL_APOIO"
```

### FASE 4: MOVER ARQUIVOS
```powershell
# Mover scripts agente
Move-Item "scripts_agente/agente_v4_7_rag_fewshot_cot.py" "03_AGENTE_CONSOLIDADO/"
Move-Item "scripts_agente/tool_rag_tfidf.py" "03_AGENTE_CONSOLIDADO/"
Move-Item "scripts_agente/tools_basicas_v2.py" "03_AGENTE_CONSOLIDADO/"
Move-Item "scripts_agente/config_llm.py" "03_AGENTE_CONSOLIDADO/"

# Mover scripts pipeline
Move-Item "scripts_pipeline/*" "02_NOTEBOOK_PASSO_A_PASSO/"

# Mover documentação selecionada
Move-Item "docs/COMPARACAO_LLMS_2026.md" "01_MATERIAL_TEORICO/"
Move-Item "docs/GUIA_ESCOLHA_LLM.md" "04_MATERIAL_APOIO/"
Move-Item "docs/IMPLEMENTACAO_MULTI_LLM.md" "04_MATERIAL_APOIO/"

# Mover utilitários
Move-Item "utilitarios/verificar_ambiente.py" "04_MATERIAL_APOIO/"
```

### FASE 5: DELETAR PASTAS VAZIAS
```powershell
Remove-Item "scripts_agente" -Recurse -Force
Remove-Item "scripts_pipeline" -Recurse -Force
Remove-Item "utilitarios" -Recurse -Force
Remove-Item "docs" -Recurse -Force
```

### FASE 6: ATUALIZAR .GITIGNORE
```powershell
# Adicionar padrões do material docente
```

---

## 📝 ARQUIVOS PARA CRIAR

### 1. INDEX_E4.md
```markdown
# E4 - RAG com FAISS

## Navegação Rápida
- [Começar aqui](00_COMECE_AQUI_E4.md)
- [Material Teórico](01_MATERIAL_TEORICO/)
- [Notebooks](02_NOTEBOOK_PASSO_A_PASSO/)
- [Agente Consolidado](03_AGENTE_CONSOLIDADO/)
- [Material de Apoio](04_MATERIAL_APOIO/)
```

### 2. 00_COMECE_AQUI_E4.md
```markdown
# 🚀 Comece Aqui - E4 RAG FAISS

## Passo 1: Ambiente
1. Criar venv
2. Instalar dependências
3. Configurar .env

## Passo 2: Pipeline RAG
1. Preparar documentos
2. Gerar embeddings
3. Criar índice FAISS
4. Testar retrieval

## Passo 3: Agente
1. Testar agente completo
2. Modo interativo
```

### 3. READMEs em cada pasta
- 01_MATERIAL_TEORICO/README.md
- 02_NOTEBOOK_PASSO_A_PASSO/README.md
- 03_AGENTE_CONSOLIDADO/README.md
- 04_MATERIAL_APOIO/README.md

---

## 📊 RESULTADO ESPERADO

### Antes
- **Arquivos:** 9.290
- **Pastas:** 1.045
- **Tamanho:** ~200 MB

### Depois
- **Arquivos:** ~50
- **Pastas:** ~8
- **Tamanho:** ~5 MB

### Redução
- **99% menos arquivos**
- **99% menos pastas**
- **97% menos espaço**

---

## 🎯 ESTRUTURA FINAL

```
E4_RAG_FAISS/
├── 01_MATERIAL_TEORICO/
│   ├── README.md
│   ├── CONCEITOS_RAG.md
│   ├── CONCEITOS_FAISS.md
│   ├── CONCEITOS_EMBEDDINGS.md
│   └── COMPARACAO_LLMS_2026.md
│
├── 02_NOTEBOOK_PASSO_A_PASSO/
│   ├── README.md
│   ├── 01_preparar_documentos.py
│   ├── 02_gerar_embeddings.py
│   ├── 03_criar_indice_faiss.py
│   ├── 04_testar_retrieval.py
│   ├── E4_rag_faiss_pipeline.ipynb
│   └── E4_rag_faiss_agente.ipynb
│
├── 03_AGENTE_CONSOLIDADO/
│   ├── README.md
│   ├── agente_v4_7_rag_fewshot_cot.py
│   ├── tool_rag_tfidf.py
│   ├── tools_basicas_v2.py
│   ├── config_llm.py
│   └── requirements.txt
│
├── 04_MATERIAL_APOIO/
│   ├── README.md
│   ├── FAQ_E4.md
│   ├── TROUBLESHOOTING_E4.md
│   ├── GUIA_ESCOLHA_LLM.md
│   ├── IMPLEMENTACAO_MULTI_LLM.md
│   └── verificar_ambiente.py
│
├── DADOS_SINARM/
│   └── (arquivos de dados)
│
├── README.md
├── INDEX_E4.md
├── 00_COMECE_AQUI_E4.md
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## ✅ CHECKLIST DE VALIDAÇÃO

- [ ] Backup criado
- [ ] venv deletado
- [ ] Cache deletado
- [ ] .env deletado
- [ ] Estrutura IBMEC criada
- [ ] Arquivos movidos
- [ ] Pastas antigas deletadas
- [ ] .gitignore atualizado
- [ ] READMEs criados
- [ ] Documentação atualizada
- [ ] Testes funcionais

---

**IMPORTANTE:** Executar backup antes de iniciar!
