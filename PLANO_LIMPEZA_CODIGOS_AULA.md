# PLANO DE LIMPEZA - CODIGOS_AULA

**Data:** 26/07/2026  
**Objetivo:** Remover arquivos antigos/desatualizados e organizar para docente

---

## 1. ANÁLISE ATUAL

### Estrutura de Pastas
```
CODIGOS_AULA/
├── __pycache__/              ❌ DELETAR (cache Python)
├── logs/                     ❌ DELETAR (logs temporários)
├── utils/                    ⚠️ AVALIAR
├── E1_ANATOMIA_DO_AGENTE/    ✅ MANTER
├── E2_QUALIDADE_E_MEMORIA/   ✅ MANTER
├── E3_HANDS_ON_CONSTRUCAO_ZERO/ ✅ MANTER (limpo)
├── E4_RAG_FAISS/             ✅ MANTER (limpo)
├── _DOCUMENTACAO/            ⚠️ AVALIAR
├── _SETUP/                   ⚠️ AVALIAR
├── _INTERNO/                 ⚠️ AVALIAR
├── _PROFESSORES/             ✅ MANTER (docente)
└── DADOS_SINARM/             ⚠️ AVALIAR (duplicado?)
```

### Arquivos por Tipo
- `.py`: 106 (muitos podem ser duplicados/antigos)
- `.md`: 97 (documentação)
- `.csv`: 53 (dados)
- `.pyc`: 30 ❌ DELETAR (cache Python)
- `.txt`: 20
- `.log`: 4 ❌ DELETAR
- `.ipynb`: 2 (notebooks)

---

## 2. AÇÕES DE LIMPEZA

### 2.1. Deletar Cache e Temporários

**Pastas:**
- `__pycache__/` (todos)
- `logs/`
- `.pytest_cache/`
- `.ipynb_checkpoints/`
- `venv/` ou `.venv/` (se existir na raiz)

**Arquivos:**
- `*.pyc`
- `*.pyo`
- `*.log`
- `*.tmp`
- `.DS_Store`
- `Thumbs.db`

### 2.2. Avaliar Pastas Especiais

**`utils/`**
- Verificar se é usado
- Se não, deletar
- Se sim, mover para `_INTERNO/`

**`_DOCUMENTACAO/`**
- Consolidar em README.md principal
- Deletar se redundante

**`_SETUP/`**
- Verificar se é necessário
- Consolidar em requirements.txt

**`_INTERNO/`**
- Verificar conteúdo
- Manter apenas se necessário para docente

**`DADOS_SINARM/`**
- Verificar se é duplicado de E3/E4
- Se sim, deletar
- Se não, mover para `_DADOS_COMPARTILHADOS/`

### 2.3. Organizar para Docente

**Criar estrutura:**
```
CODIGOS_AULA/
├── E1_ANATOMIA_DO_AGENTE/
├── E2_QUALIDADE_E_MEMORIA/
├── E3_HANDS_ON_CONSTRUCAO_ZERO/
├── E4_RAG_FAISS/
├── _PROFESSORES/
│   ├── GUIA_DOCENTE.md
│   ├── PLANOS_AULA/
│   ├── GABARITOS/
│   └── RECURSOS/
└── _DADOS_COMPARTILHADOS/ (se necessário)
```

---

## 3. GITIGNORE

### Criar `.gitignore` na raiz de CODIGOS_AULA

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual Environment
venv/
.venv/
env/
ENV/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/
*.tmp

# OS
.DS_Store
Thumbs.db
desktop.ini

# Dados sensíveis (se houver)
*.csv
*.xlsx
*.db
*.sqlite

# Documentos do professor (não compartilhar com alunos)
_PROFESSORES/
_INTERNO/
_GABARITOS/

# Backups
*.bak
*.backup
*_old/
*_antigo/
```

---

## 4. ESTRUTURA FINAL PROPOSTA

```
CODIGOS_AULA/
│
├── .gitignore                    ✅ CRIAR
├── README.md                     ✅ ATUALIZAR
├── requirements.txt              ✅ CONSOLIDAR
│
├── E1_ANATOMIA_DO_AGENTE/        ✅ MANTER
│   ├── README.md
│   ├── 01_MATERIAL_TEORICO/
│   ├── 02_MATERIAL_PRATICA/
│   └── 03_CODIGOS_PRONTOS/
│
├── E2_QUALIDADE_E_MEMORIA/       ✅ MANTER
│   ├── README.md
│   ├── 01_MATERIAL_TEORICO/
│   ├── 02_MATERIAL_PRATICA/
│   └── 03_CODIGOS_PRONTOS/
│
├── E3_HANDS_ON_CONSTRUCAO_ZERO/  ✅ LIMPO
│   ├── README.md
│   ├── 01_GUIAS_ALUNO/
│   ├── 02_NOTEBOOK_PASSO_A_PASSO/
│   ├── 03_AGENTE_CONSOLIDADO/
│   └── 04_MATERIAL_APOIO/
│
├── E4_RAG_FAISS/                 ✅ LIMPO
│   ├── README.md
│   ├── 01_DADOS/
│   ├── 02_NOTEBOOK_PASSO_A_PASSO/
│   ├── 03_AGENTE_CONSOLIDADO/
│   └── 04_MATERIAL_APOIO/
│
└── _PROFESSORES/                 🔒 GITIGNORE
    ├── GUIA_DOCENTE.md
    ├── PLANOS_AULA/
    │   ├── E1_plano_aula.md
    │   ├── E2_plano_aula.md
    │   ├── E3_plano_aula.md
    │   └── E4_plano_aula.md
    ├── GABARITOS/
    │   ├── E1_gabarito.md
    │   ├── E2_gabarito.md
    │   ├── E3_gabarito.md
    │   └── E4_gabarito.md
    └── RECURSOS/
        ├── slides/
        ├── videos/
        └── referencias/
```

---

## 5. CHECKLIST DE EXECUÇÃO

### Fase 1: Análise
- [ ] Listar todos os arquivos `.pyc`
- [ ] Listar todos os `__pycache__`
- [ ] Listar todos os `.log`
- [ ] Verificar conteúdo de `utils/`
- [ ] Verificar conteúdo de `_DOCUMENTACAO/`
- [ ] Verificar conteúdo de `_SETUP/`
- [ ] Verificar conteúdo de `_INTERNO/`
- [ ] Verificar conteúdo de `DADOS_SINARM/`

### Fase 2: Limpeza
- [ ] Deletar `__pycache__/` (todos)
- [ ] Deletar `*.pyc` (todos)
- [ ] Deletar `*.log` (todos)
- [ ] Deletar `logs/`
- [ ] Deletar pastas vazias
- [ ] Deletar arquivos duplicados

### Fase 3: Organização
- [ ] Criar `.gitignore`
- [ ] Criar `_PROFESSORES/` (se não existir)
- [ ] Mover materiais docente para `_PROFESSORES/`
- [ ] Consolidar `requirements.txt`
- [ ] Atualizar `README.md` principal

### Fase 4: Validação
- [ ] Verificar E3 funciona
- [ ] Verificar E4 funciona
- [ ] Verificar notebooks funcionam
- [ ] Verificar documentação está completa
- [ ] Testar git ignore

---

## 6. COMANDOS DE LIMPEZA

### PowerShell

```powershell
# Ir para pasta
cd "E:\documentos\ibmec\CODIGOS_AULA"

# Deletar __pycache__
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Deletar .pyc
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force

# Deletar .log
Get-ChildItem -Path . -Recurse -Filter "*.log" | Remove-Item -Force

# Deletar logs/
if (Test-Path "logs") { Remove-Item -Path "logs" -Recurse -Force }

# Deletar .ipynb_checkpoints
Get-ChildItem -Path . -Recurse -Directory -Filter ".ipynb_checkpoints" | Remove-Item -Recurse -Force
```

---

## 7. ESTIMATIVAS

### Espaço a Liberar
- `__pycache__/`: ~5-10 MB
- `*.pyc`: ~1-2 MB
- `logs/`: ~1-5 MB
- Duplicados: ~50-100 MB (estimativa)
- **Total:** ~60-120 MB

### Arquivos a Remover
- `__pycache__/`: ~30 pastas
- `*.pyc`: ~30 arquivos
- `*.log`: ~4 arquivos
- Duplicados: ~50-100 arquivos (estimativa)
- **Total:** ~120-170 arquivos

---

## 8. PRÓXIMOS PASSOS

1. ✅ Aprovar plano
2. ⏳ Executar limpeza
3. ⏳ Criar `.gitignore`
4. ⏳ Organizar `_PROFESSORES/`
5. ⏳ Validar funcionamento
6. ⏳ Commit no git

---

**Status:** ⏳ AGUARDANDO APROVAÇÃO PARA EXECUTAR
