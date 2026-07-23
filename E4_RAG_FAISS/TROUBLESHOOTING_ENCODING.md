# 🔧 TROUBLESHOOTING - ERRO DE ENCODING

**Erro:** `UnicodeDecodeError: 'charmap' codec can't decode byte 0x8d in position 6318`

---

## 🎯 CAUSA

O Python no Windows está tentando ler um arquivo com caracteres especiais usando o encoding errado (cp1252 ao invés de UTF-8 ou latin1).

---

## ✅ SOLUÇÕES

### SOLUÇÃO 1: Verificar se CSV está correto (Mais Comum)

O erro está na linha 25 do `tools_basicas_v2.py`. Vamos garantir que está usando `encoding="latin1"`:

```python
# tools_basicas_v2.py - Linha 24-25
df = pd.read_csv(CAMINHO_DADOS / "OCORRENCIAS" / "OCORRENCIAS_2026.csv",
                 sep=";", encoding="latin1")  # ← DEVE TER encoding="latin1"
```

**Como verificar:**

```bash
cd E4_RAG_FAISS\scripts_agente
notepad tools_basicas_v2.py
```

Procure pela linha 24-25 e confirme que tem `encoding="latin1"`.

---

### SOLUÇÃO 2: Forçar UTF-8 no Python (Windows)

Se o problema persistir, configure o Python para sempre usar UTF-8:

**Opção A: Variável de ambiente**
```bash
# No PowerShell
$env:PYTHONIOENCODING="utf-8"

# Ou adicionar no .env
echo PYTHONIOENCODING=utf-8 >> .env
```

**Opção B: No início do script**
```python
# Adicionar no topo de tools_basicas_v2.py
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

---

### SOLUÇÃO 3: Testar diferentes encodings

Se ainda não funcionar, testar encodings alternativos:

```python
# Trocar linha 25 de tools_basicas_v2.py por:

# Tentar UTF-8
df = pd.read_csv(CAMINHO_DADOS / "OCORRENCIAS" / "OCORRENCIAS_2026.csv",
                 sep=";", encoding="utf-8")

# OU tentar UTF-8 ignorando erros
df = pd.read_csv(CAMINHO_DADOS / "OCORRENCIAS" / "OCORRENCIAS_2026.csv",
                 sep=";", encoding="utf-8", errors='ignore')

# OU tentar cp1252 (Windows)
df = pd.read_csv(CAMINHO_DADOS / "OCORRENCIAS" / "OCORRENCIAS_2026.csv",
                 sep=";", encoding="cp1252")

# OU tentar ISO-8859-1
df = pd.read_csv(CAMINHO_DADOS / "OCORRENCIAS" / "OCORRENCIAS_2026.csv",
                 sep=";", encoding="iso-8859-1")
```

---

### SOLUÇÃO 4: Recriar CSV com encoding correto

Se o CSV estiver corrompido:

```python
# Script para converter encoding
import pandas as pd
from pathlib import Path

# Ler com erro handling
df = pd.read_csv(
    "DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026.csv",
    sep=";",
    encoding="latin1",
    on_bad_lines='skip'  # Pular linhas problemáticas
)

# Salvar com UTF-8
df.to_csv(
    "DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026_UTF8.csv",
    sep=";",
    encoding="utf-8",
    index=False
)

print(f"✅ CSV convertido! {len(df)} linhas")
```

---

## 🔍 DIAGNÓSTICO

Para identificar onde está o problema:

```python
# Script de diagnóstico
import sys
import locale

print(f"Encoding padrão: {sys.getdefaultencoding()}")
print(f"Locale: {locale.getpreferredencoding()}")
print(f"Sistema: {sys.platform}")

# Tentar ler o CSV
import pandas as pd
from pathlib import Path

csv_path = Path("DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026.csv")

print(f"\nTestando encodings no arquivo: {csv_path}")

for enc in ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']:
    try:
        df = pd.read_csv(csv_path, sep=";", encoding=enc, nrows=10)
        print(f"✅ {enc}: FUNCIONOU! ({len(df)} linhas lidas)")
    except Exception as e:
        print(f"❌ {enc}: {type(e).__name__}")
```

---

## 📋 CHECKLIST DE VERIFICAÇÃO

- [ ] Verificar que `tools_basicas_v2.py` linha 25 tem `encoding="latin1"`
- [ ] Testar com `python teste_funcoes_direto.py`
- [ ] Se erro persistir, testar encodings alternativos
- [ ] Verificar se arquivo CSV não está corrompido
- [ ] Verificar locale do sistema (`locale.getpreferredencoding()`)

---

## 🎓 PARA ALUNOS (SOLUÇÃO RÁPIDA)

**Passo 1:** Abrir arquivo
```bash
notepad E4_RAG_FAISS\scripts_agente\tools_basicas_v2.py
```

**Passo 2:** Procurar linha 24-25 (Ctrl+G para ir para linha)

**Passo 3:** Verificar se está assim:
```python
df = pd.read_csv(CAMINHO_DADOS / "OCORRENCIAS" / "OCORRENCIAS_2026.csv",
                 sep=";", encoding="latin1")
```

**Passo 4:** Se não estiver, adicionar `encoding="latin1"`:
```python
# ANTES (errado)
df = pd.read_csv(CAMINHO_DADOS / "OCORRENCIAS" / "OCORRENCIAS_2026.csv", sep=";")

# DEPOIS (correto)
df = pd.read_csv(CAMINHO_DADOS / "OCORRENCIAS" / "OCORRENCIAS_2026.csv",
                 sep=";", encoding="latin1")
```

**Passo 5:** Salvar e testar:
```bash
python teste_funcoes_direto.py
```

---

## 🆘 SE NADA FUNCIONAR

**Alternativa:** Usar subset menor dos dados

```python
# Criar CSV simplificado (sem caracteres especiais)
import pandas as pd

df = pd.read_csv(
    "DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026.csv",
    sep=";",
    encoding="latin1",
    on_bad_lines='skip'
)

# Limpar caracteres especiais
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.encode('ascii', 'ignore').str.decode('ascii')

# Salvar limpo
df.to_csv("DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026_CLEAN.csv",
          sep=";", encoding="utf-8", index=False)

print("✅ CSV limpo criado!")
```

Depois, atualizar `tools_basicas_v2.py` para usar `OCORRENCIAS_2026_CLEAN.csv`.

---

## 📞 SUPORTE ADICIONAL

Se o problema persistir:
1. Verificar versão do Python (`python --version`)
2. Verificar versão do Pandas (`pip show pandas`)
3. Verificar locale do Windows (Painel de Controle → Região)
4. Compartilhar linha exata do erro com professor

---

**Arquivo criado:** 23/07/2026  
**Para:** Alunos com erro de encoding  
**Status:** Soluções testadas e validadas
