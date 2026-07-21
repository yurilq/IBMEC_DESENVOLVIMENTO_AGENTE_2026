# 🔍 EXPLICAÇÃO DETALHADA: Como .str.contains() Funciona

## 📚 Entendendo Busca Parcial vs Busca Exata

### Problema: Busca Exata com `==`

```python
# O que temos no CSV:
marca_no_csv = "TAURUS ARMAS S.A.                                                     "
# ↑ String de 70 caracteres

# O que o usuário digita:
marca_usuario = "Taurus"
# ↑ String de 6 caracteres

# Tentativa de comparação EXATA:
if marca_no_csv == marca_usuario.upper():
    print("Encontrou!")
else:
    print("NÃO encontrou!")

# Resultado: NÃO encontrou!
# Por quê? Porque compara caractere por caractere:
# "TAURUS ARMAS S.A.        ..." (70 chars) ≠ "TAURUS" (6 chars)
```

**Comparação exata (`==`) exige que TUDO seja IGUAL:**
- Mesmo comprimento
- Mesmos caracteres
- Mesma posição

---

### Solução: Busca Parcial com `.contains()`

```python
# O que temos no CSV:
marca_no_csv = "TAURUS ARMAS S.A.                                                     "

# O que o usuário digita:
marca_usuario = "Taurus"

# Busca PARCIAL:
if "TAURUS" in marca_no_csv:  # ← Verifica se "TAURUS" está DENTRO
    print("Encontrou!")
else:
    print("NÃO encontrou!")

# Resultado: Encontrou! ✅
# Por quê? Porque "TAURUS" existe DENTRO de "TAURUS ARMAS S.A. ..."
```

---

## 🎯 Como `.str.contains()` Funciona (Passo a Passo)

### Exemplo Simples:

```python
import pandas as pd

# Criar DataFrame de exemplo
marcas = [
    "TAURUS ARMAS S.A.                                                     ",
    "GLOCK GMBH (ÁUSTRIA)                                                  ",
    "ROSSI (AMADEO ROSSI S.A.)                                             ",
    "BOITO (E.R. AMANTINO & CIA)                                           "
]

df = pd.DataFrame({"MARCA_ARMA": marcas})

print("="*60)
print("DADOS ORIGINAIS:")
print("="*60)
for i, marca in enumerate(df["MARCA_ARMA"], 1):
    print(f"{i}. '{marca}'")

# Buscar "TAURUS"
print("\n" + "="*60)
print("BUSCANDO 'TAURUS' com .contains()")
print("="*60)

resultado = df[df["MARCA_ARMA"].str.contains("TAURUS", case=False)]
print(f"Encontrou {len(resultado)} linha(s):")
print(resultado)
```

**Saída:**
```
============================================================
DADOS ORIGINAIS:
============================================================
1. 'TAURUS ARMAS S.A.                                                     '
2. 'GLOCK GMBH (ÁUSTRIA)                                                  '
3. 'ROSSI (AMADEO ROSSI S.A.)                                             '
4. 'BOITO (E.R. AMANTINO & CIA)                                           '

============================================================
BUSCANDO 'TAURUS' com .contains()
============================================================
Encontrou 1 linha(s):
                                          MARCA_ARMA
0  TAURUS ARMAS S.A.                      ...
```

---

## 🔬 O Que `.str.contains()` Faz Internamente

### Passo a Passo:

```python
# String grande do CSV:
texto_grande = "TAURUS ARMAS S.A.                    "

# String pequena que buscamos:
texto_pequeno = "TAURUS"

# .contains() verifica:
# "TAURUS" está em "TAURUS ARMAS S.A. ..."?

# Processo:
# Posição 0: T A U R U S   A R M A S   S . A .
#            ↑ ↑ ↑ ↑ ↑ ↑
#            T A U R U S
# ✅ MATCH! Encontrou nos primeiros 6 caracteres
```

**Analogia:**
- É como procurar a palavra "casa" dentro da frase "A casa é azul"
- Não importa que a frase seja maior
- Se "casa" existe EM QUALQUER LUGAR, encontra!

---

## 💡 Comparação Visual

### Exemplo 1: Buscar "TAURUS"

```
String no CSV: "TAURUS ARMAS S.A.                    "
                ^^^^^^
                  ↑
            ENCONTROU AQUI!

Busca: "TAURUS"
Resultado: ✅ ENCONTRADO (posição 0-5)
```

### Exemplo 2: Buscar "ARMAS"

```
String no CSV: "TAURUS ARMAS S.A.                    "
                       ^^^^^
                         ↑
                 ENCONTROU AQUI!

Busca: "ARMAS"
Resultado: ✅ ENCONTRADO (posição 7-11)
```

### Exemplo 3: Buscar "GLOCK"

```
String no CSV: "TAURUS ARMAS S.A.                    "
                ❌ Não tem "GLOCK"

Busca: "GLOCK"
Resultado: ❌ NÃO ENCONTRADO
```

---

## 🧪 Experimento Prático

Crie arquivo: `experimento_contains.py`

```python
import pandas as pd

# Exemplo com strings grandes (70 caracteres)
marcas = [
    "TAURUS ARMAS S.A.                                                     ",
    "GLOCK GMBH (ÁUSTRIA)                                                  ",
    "ROSSI (AMADEO ROSSI S.A.)                                             ",
]

df = pd.DataFrame({"MARCA": marcas})

print("="*60)
print("EXPERIMENTO: Busca Parcial")
print("="*60)

# Teste 1: Buscar "TAURUS"
print("\n1. Buscando 'TAURUS':")
resultado = df[df["MARCA"].str.contains("TAURUS", case=False)]
print(f"   Encontrou: {len(resultado)} linha(s)")
if len(resultado) > 0:
    print(f"   Linha encontrada: '{resultado.iloc[0]['MARCA'].strip()}'")

# Teste 2: Buscar "GLOCK"
print("\n2. Buscando 'GLOCK':")
resultado = df[df["MARCA"].str.contains("GLOCK", case=False)]
print(f"   Encontrou: {len(resultado)} linha(s)")
if len(resultado) > 0:
    print(f"   Linha encontrada: '{resultado.iloc[0]['MARCA'].strip()}'")

# Teste 3: Buscar "ARMAS" (palavra que aparece em TAURUS)
print("\n3. Buscando 'ARMAS':")
resultado = df[df["MARCA"].str.contains("ARMAS", case=False)]
print(f"   Encontrou: {len(resultado)} linha(s)")
if len(resultado) > 0:
    print(f"   Linha encontrada: '{resultado.iloc[0]['MARCA'].strip()}'")

# Teste 4: Buscar "ROSSI"
print("\n4. Buscando 'ROSSI':")
resultado = df[df["MARCA"].str.contains("ROSSI", case=False)]
print(f"   Encontrou: {len(resultado)} linha(s)")
if len(resultado) > 0:
    print(f"   Linha encontrada: '{resultado.iloc[0]['MARCA'].strip()}'")

# Teste 5: Buscar algo que NÃO existe
print("\n5. Buscando 'BERETTA' (não existe):")
resultado = df[df["MARCA"].str.contains("BERETTA", case=False)]
print(f"   Encontrou: {len(resultado)} linha(s)")

print("\n" + "="*60)
```

**Execute:**
```bash
python experimento_contains.py
```

**Saída esperada:**
```
============================================================
EXPERIMENTO: Busca Parcial
============================================================

1. Buscando 'TAURUS':
   Encontrou: 1 linha(s)
   Linha encontrada: 'TAURUS ARMAS S.A.'

2. Buscando 'GLOCK':
   Encontrou: 1 linha(s)
   Linha encontrada: 'GLOCK GMBH (ÁUSTRIA)'

3. Buscando 'ARMAS':
   Encontrou: 1 linha(s)
   Linha encontrada: 'TAURUS ARMAS S.A.'

4. Buscando 'ROSSI':
   Encontrou: 1 linha(s)
   Linha encontrada: 'ROSSI (AMADEO ROSSI S.A.)'

5. Buscando 'BERETTA' (não existe):
   Encontrou: 0 linha(s)

============================================================
```

---

## 📊 Comparação: `==` vs `in` vs `.contains()`

```python
texto_grande = "TAURUS ARMAS S.A.                    "
texto_pequeno = "TAURUS"

# MÉTODO 1: == (comparação EXATA)
if texto_grande == texto_pequeno:
    print("Método 1: Encontrou")
else:
    print("Método 1: NÃO encontrou")  # ← Resultado
# Por quê? Tamanhos diferentes (70 ≠ 6)

# MÉTODO 2: in (busca PARCIAL em string)
if texto_pequeno in texto_grande:
    print("Método 2: Encontrou")  # ← Resultado
else:
    print("Método 2: NÃO encontrou")
# Por quê? "TAURUS" existe DENTRO de "TAURUS ARMAS..."

# MÉTODO 3: .contains() (busca PARCIAL em DataFrame)
# (funciona igual ao 'in', mas para pandas Series/DataFrame)
if df["MARCA_ARMA"].str.contains(texto_pequeno).any():
    print("Método 3: Encontrou")  # ← Resultado
else:
    print("Método 3: NÃO encontrou")
```

---

## 🎓 Conceitos Importantes

### 1. **Substring (Sub-string)**

```
String grande: "TAURUS ARMAS S.A."
Substrings possíveis:
- "TAURUS"       ✅ Existe
- "ARMAS"        ✅ Existe
- "S.A."         ✅ Existe
- "TAURUS ARMAS" ✅ Existe
- "GLOCK"        ❌ NÃO existe
```

**Substring** = pedaço de texto que está contido em um texto maior

---

### 2. **Case Sensitivity (Sensibilidade a Maiúsculas)**

```python
texto = "TAURUS ARMAS S.A."

# SEM case=False (diferencia maiúsculas)
"taurus" in texto  # ❌ False (procura "taurus" minúsculo)
"TAURUS" in texto  # ✅ True (procura "TAURUS" maiúsculo)

# COM case=False (ignora maiúsculas)
texto_lower = texto.lower()  # "taurus armas s.a."
"taurus" in texto_lower      # ✅ True
"TAURUS" in texto_lower      # ❌ False (agora texto está minúsculo)

# MELHOR: usar .contains() com case=False
df["MARCA"].str.contains("taurus", case=False)  # ✅ Encontra "TAURUS"
```

---

### 3. **Parâmetro `na=False`**

```python
# Dataset com valores nulos
marcas_com_nulos = [
    "TAURUS ARMAS S.A.",
    None,  # ← Valor nulo
    "GLOCK GMBH",
    ""     # ← String vazia
]

df = pd.DataFrame({"MARCA": marcas_com_nulos})

# SEM na=False (ERRO!)
try:
    resultado = df[df["MARCA"].str.contains("TAURUS")]
except Exception as e:
    print(f"Erro: {e}")  # Erro ao processar None

# COM na=False (FUNCIONA!)
resultado = df[df["MARCA"].str.contains("TAURUS", na=False)]
print(f"Encontrou: {len(resultado)} linha(s)")
# ↑ Ignora linhas com None e continua buscando
```

---

## 🚀 Resumo Final

### Como `.str.contains()` funciona:

1. **Pega cada linha** do DataFrame
2. **Verifica se o texto buscado existe EM QUALQUER LUGAR** da string
3. **Retorna True/False** para cada linha
4. **Filtra** só as linhas True

### Por que funciona com nomes parciais:

```
CSV:     "TAURUS ARMAS S.A.                    " (70 chars)
Busca:   "TAURUS"                                (6 chars)

Pergunta: "TAURUS" está dentro de "TAURUS ARMAS S.A. ..."?
Resposta: SIM! (nos primeiros 6 caracteres)
Resultado: ✅ MATCH!
```

### Analogia do dia a dia:

- **`==`** é como perguntar: "Você é exatamente João Silva Santos?"
  - Só responde sim se o nome for EXATO
  
- **`.contains()`** é como perguntar: "Seu nome tem 'João'?"
  - Responde sim para "João Silva", "Maria João", "João Pedro", etc.

---

**Arquivo:** EXPLICACAO_CONTAINS.md  
**Localização:** 04_MATERIAL_APOIO/  
**Criado:** 20/07/2026  
**Status:** ✅ Explicação detalhada de busca parcial
