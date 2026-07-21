# 📂 ESTRUTURA DE PASTAS - E3

**IMPORTANTE:** Entenda a diferença entre **Pasta do Material** e **Pasta de Trabalho**

---

## 🎯 DUAS PASTAS DIFERENTES

### 1️⃣ PASTA DO MATERIAL (Não mexer!)

Localização: `E3_HANDS_ON_CONSTRUCAO_ZERO/`

```
E3_HANDS_ON_CONSTRUCAO_ZERO/
├── 00_COMECE_AQUI_E3.md              ← Leia aqui
├── INDEX_E3.md                       ← Navegação
├── 01_GUIAS_ALUNO/                   ← Guias passo a passo
├── 02_TEMPLATES_PRONTOS/             ← Código de referência
├── 03_CODIGO_INCREMENTAL/            ← Exemplos progressivos
└── 04_MATERIAL_APOIO/                ← FAQ, conceitos, etc.
```

**USO:** Consultar, ler, copiar código de referência  
**NÃO:** Executar código aqui, criar arquivos aqui

---

### 2️⃣ PASTA DE TRABALHO (Você vai criar!)

Localização: **Onde você quiser** (ex: `Desktop/meu_agente_sinarm/`)

```
meu_agente_sinarm/                    ← SUA PASTA DE TRABALHO
│
├── DADOS_SINARM/                     ← Você cria esta pasta
│   └── OCORRENCIAS_2026.csv          ← Você coloca o CSV aqui
│
├── teste_llm.py                      ← Você cria (Parte 1)
├── tools_basicas.py                  ← Você cria (Parte 2)
├── agente_v0_1.py                    ← Você cria (Parte 2)
├── decorator_exemplo.py              ← Você cria (Parte 3)
└── agente_v2_0.py                    ← Você cria (Parte 5)
```

**USO:** Aqui você trabalha, cria arquivos, executa código  
**IMPORTANTE:** Todos os paths nos guias assumem que você está DENTRO desta pasta

---

## 📋 SETUP CORRETO (Passo a Passo)

### PASSO 1: Criar Pasta de Trabalho

Crie uma pasta FORA de E3_HANDS_ON_CONSTRUCAO_ZERO:

```bash
# Windows (PowerShell)
cd Desktop
mkdir meu_agente_sinarm
cd meu_agente_sinarm

# Mac/Linux
cd ~/Desktop
mkdir meu_agente_sinarm
cd meu_agente_sinarm
```

---

### PASSO 2: Criar Subpasta DADOS_SINARM

Dentro da sua pasta de trabalho:

```bash
mkdir DADOS_SINARM
```

---

### PASSO 3: Copiar CSV

Copie o arquivo CSV para sua pasta de trabalho:

**Opção A: Se você tem o CSV**
```bash
# Windows
copy C:\path\para\OCORRENCIAS_2026.csv DADOS_SINARM\

# Mac/Linux
cp /path/para/OCORRENCIAS_2026.csv DADOS_SINARM/
```

**Opção B: Se está na pasta do material**
```bash
# Copiar do material para sua pasta
copy ..\E3_HANDS_ON_CONSTRUCAO_ZERO\01_GUIAS_ALUNO\DADOS_SINARM\OCORRENCIAS_2026.csv DADOS_SINARM\
```

---

### PASSO 4: Verificar Estrutura

Dentro de `meu_agente_sinarm/`, execute:

```bash
# Windows
dir /s

# Mac/Linux
ls -R
```

**Resultado esperado:**
```
meu_agente_sinarm/
└── DADOS_SINARM/
    └── OCORRENCIAS_2026.csv
```

✅ **PRONTO!** Agora você pode seguir os guias.

---

## 🚨 PROBLEMAS COMUNS

### ❌ FileNotFoundError: DADOS_SINARM/OCORRENCIAS_2026.csv

**Causa:** Você está executando de lugar errado ou CSV não está na subpasta.

**Solução:**
```bash
# 1. Ver onde você está
pwd  # Mac/Linux
cd   # Windows

# 2. Ver se DADOS_SINARM existe
ls DADOS_SINARM/  # Mac/Linux
dir DADOS_SINARM\ # Windows

# 3. Se não existir, criar e copiar CSV (ver PASSO 2 e 3)
```

---

### ❌ Executei código dentro de E3_HANDS_ON_CONSTRUCAO_ZERO/

**Problema:** Não deve trabalhar dentro da pasta do material!

**Solução:** 
1. Crie pasta separada (ver PASSO 1)
2. Copie CSV (ver PASSO 3)
3. Trabalhe na nova pasta

---

## 📊 COMPARAÇÃO

| Aspecto | Pasta Material | Pasta Trabalho |
|---------|----------------|----------------|
| **Localização** | `E3_HANDS_ON_CONSTRUCAO_ZERO/` | `Desktop/meu_agente_sinarm/` |
| **Conteúdo** | Guias, templates, exemplos | Seus arquivos .py + CSV |
| **Você cria arquivos?** | ❌ NÃO | ✅ SIM |
| **Você executa .py?** | ❌ NÃO | ✅ SIM |
| **CSV fica aqui?** | ❌ NÃO (só referência) | ✅ SIM |

---

## 🎯 FLUXO DE TRABALHO

```
1. ABRIR GUIA
   └─ E3_HANDS_ON_CONSTRUCAO_ZERO/01_GUIAS_ALUNO/PARTE_1_SETUP.md

2. LER INSTRUÇÕES
   └─ Guia explica o que fazer

3. CRIAR ARQUIVO (na sua pasta de trabalho!)
   └─ Desktop/meu_agente_sinarm/teste_llm.py

4. EXECUTAR (da sua pasta de trabalho!)
   └─ cd Desktop/meu_agente_sinarm
   └─ python teste_llm.py

5. SE TRAVAR: Consultar template
   └─ E3_HANDS_ON_CONSTRUCAO_ZERO/02_TEMPLATES_PRONTOS/TEMPLATE_HORA_1.py
   └─ Copiar referência para seu arquivo
```

---

## 📌 RESUMO

### ✅ CERTO:
```
Desktop/
├── E3_HANDS_ON_CONSTRUCAO_ZERO/      ← Material (só consultar)
└── meu_agente_sinarm/                ← Trabalho (você trabalha aqui)
    ├── DADOS_SINARM/
    │   └── OCORRENCIAS_2026.csv
    ├── teste_llm.py
    └── tools_basicas.py
```

### ❌ ERRADO:
```
E3_HANDS_ON_CONSTRUCAO_ZERO/
├── 01_GUIAS_ALUNO/
│   ├── teste_llm.py              ← NÃO criar aqui!
│   └── tools_basicas.py          ← NÃO criar aqui!
└── DADOS_SINARM/                 ← NÃO colocar CSV aqui!
```

---

## 🔄 PATHS RELATIVOS NOS GUIAS

Todos os paths nos guias assumem que você está na **pasta de trabalho**:

```python
# ✅ CERTO (você está em meu_agente_sinarm/)
df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", ...)

# ❌ ERRADO (path absoluto - não use!)
df = pd.read_csv("C:/Users/.../E3_HANDS_ON_CONSTRUCAO_ZERO/01_GUIAS_ALUNO/DADOS_SINARM/OCORRENCIAS_2026.csv", ...)

# ❌ ERRADO (você está em lugar errado)
df = pd.read_csv("../DADOS_SINARM/OCORRENCIAS_2026.csv", ...)
```

---

**Arquivo:** ESTRUTURA_PASTAS_E3.md  
**Localização:** E3_HANDS_ON_CONSTRUCAO_ZERO/  
**Criado:** 20/07/2026  
**Status:** ✅ Explicação completa de estrutura

**Leia antes de começar a aula!**
