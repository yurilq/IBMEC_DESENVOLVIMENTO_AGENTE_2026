# 🧹 MÓDULO EXTRA: TRATAMENTO DE DADOS

**Tempo:** 15-20 minutos (pode ser inserido na Parte 2 ou 4)  
**Objetivo:** Ensinar tratamento de dados reais com pandas  
**Nível:** Intermediário

---

## 🎯 O PROBLEMA REAL

Você criou a função `contar_armas_marca("Taurus")` mas retorna **0 resultados**.

Por quê? Vamos investigar!

---

## 🔍 INVESTIGAÇÃO: Entendendo os Dados

### PASSO 1: Criar Script de Análise (5 min)

Crie arquivo: `analisar_dados.py`

```python
import pandas as pd
import os

# Carregar CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "DADOS_SINARM", "OCORRENCIAS_2026.csv")

df = pd.read_csv(csv_path, sep=";", encoding="latin1", nrows=100)

print("="*60)
print("ANÁLISE DE DADOS")
print("="*60)

# Ver primeiras linhas
print("\n1. PRIMEIRAS 3 LINHAS:")
print(df.head(3))

# Ver marcas únicas
print("\n2. MARCAS ÚNICAS (primeiras 10):")
marcas = df["MARCA_ARMA"].unique()[:10]
for i, marca in enumerate(marcas, 1):
    print(f"{i}. '{marca}' (comprimento: {len(marca)} caracteres)")

# Buscar Taurus
print("\n3. BUSCANDO 'TAURUS':")
# Método 1: Comparação exata
exato = df[df["MARCA_ARMA"] == "TAURUS"]
print(f"   Comparação exata '==' : {len(exato)} resultados")

# Método 2: Comparação com upper()
upper = df[df["MARCA_ARMA"] == "TAURUS".upper()]
print(f"   Com .upper(): {len(upper)} resultados")

# Método 3: Busca parcial (contains)
contains = df[df["MARCA_ARMA"].str.contains("TAURUS", case=False, na=False)]
print(f"   Com .contains(): {len(contains)} resultados")

if len(contains) > 0:
    print(f"\n   Exemplo encontrado: '{contains.iloc[0]['MARCA_ARMA']}'")
```

**Execute:**
```bash
python analisar_dados.py
```

---

## 💡 DESCOBERTAS

Você vai ver algo assim:

```
2. MARCAS ÚNICAS (primeiras 10):
1. 'BOITO (E.R. AMANTINO & CIA)                                           ' (comprimento: 70 caracteres)
2. 'CBC (COMPANHIA BRASILEIRA DE CARTUCHOS)                               ' (comprimento: 70 caracteres)
3. 'TAURUS ARMAS S.A.                                                     ' (comprimento: 70 caracteres)
```

### 🔍 Problemas Identificados:

1. **Espaços extras**: Todas marcas têm 70 caracteres (padding com espaços)
2. **Nome completo**: `'TAURUS ARMAS S.A.'` (não apenas "TAURUS")
3. **Busca exata falha**: `df["MARCA_ARMA"] == "TAURUS"` retorna 0

---

## ✅ SOLUÇÃO: Técnicas de Tratamento de Dados

### Técnica 1: `.str.strip()` - Remover Espaços

```python
# ANTES (com espaços)
marca_suja = "TAURUS ARMAS S.A.                           "
print(len(marca_suja))  # 70 caracteres

# DEPOIS (limpa)
marca_limpa = marca_suja.strip()
print(len(marca_limpa))  # 17 caracteres
print(f"'{marca_limpa}'")  # 'TAURUS ARMAS S.A.'
```

---

### Técnica 2: `.str.contains()` - Busca Parcial

```python
# PROBLEMA: Comparação exata não funciona
df[df["MARCA_ARMA"] == "TAURUS"]  # ❌ Retorna 0 (não existe "TAURUS" exato)

# SOLUÇÃO: Busca parcial
df[df["MARCA_ARMA"].str.contains("TAURUS", case=False)]  # ✅ Encontra "TAURUS ARMAS S.A."
```

**Parâmetros importantes:**
- `case=False` → Ignora maiúsculas/minúsculas
- `na=False` → Ignora valores nulos (não quebra)

---

### Técnica 3: Combinar `.strip()` + `.contains()`

```python
# MELHOR SOLUÇÃO: Combinar técnicas
df[
    df["MARCA_ARMA"]
    .str.strip()          # 1. Remove espaços
    .str.contains("TAURUS", case=False, na=False)  # 2. Busca parcial
]
```

---

## 🔧 REFATORAR: Aplicar no Código

### ANTES (não funciona):

```python
def contar_armas_marca(marca: str):
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", 
                     sep=";", encoding="latin1")
    
    # ❌ Comparação exata - não funciona com espaços
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    
    total = len(resultado)
    return f"Encontrei {total} armas {marca}"
```

**Problema:** Retorna sempre 0!

---

### DEPOIS (funciona):

```python
def contar_armas_marca(marca: str):
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", 
                     sep=";", encoding="latin1")
    
    # ✅ Busca parcial com tratamento
    resultado = df[
        df["MARCA_ARMA"]
        .str.strip()                           # Remove espaços
        .str.contains(marca, case=False, na=False)  # Busca parcial
    ]
    
    total = len(resultado)
    
    # Bonus: Mostrar nome completo encontrado
    if total > 0:
        marca_completa = resultado.iloc[0]["MARCA_ARMA"].strip()
        return f"Encontrei {total} armas da marca '{marca_completa}'"
    else:
        return f"Nenhuma arma encontrada para '{marca}'"
```

**Melhoria:** Funciona e mostra nome completo!

---

## 🎓 CONCEITOS APRENDIDOS

### Pandas String Methods

```python
# Métodos úteis para strings em pandas:

# 1. Remover espaços
df["coluna"].str.strip()        # Remove início e fim
df["coluna"].str.lstrip()       # Remove só início
df["coluna"].str.rstrip()       # Remove só fim

# 2. Busca
df["coluna"].str.contains("texto")     # Busca parcial
df["coluna"].str.startswith("texto")   # Começa com
df["coluna"].str.endswith("texto")     # Termina com

# 3. Transformação
df["coluna"].str.upper()        # Maiúsculas
df["coluna"].str.lower()        # Minúsculas
df["coluna"].str.replace("A", "B")  # Substituir

# 4. Informação
df["coluna"].str.len()          # Comprimento
```

---

## 🧪 EXERCÍCIO PRÁTICO

### Desafio 1: Analisar Outras Colunas

```python
# Verificar se outras colunas também têm espaços extras
print("Análise de CALIBRE_ARMA:")
calibres = df["CALIBRE_ARMA"].unique()[:10]
for calibre in calibres:
    print(f"'{calibre}' (len={len(calibre)})")
```

### Desafio 2: Função de Limpeza Genérica

```python
def limpar_coluna(df, coluna):
    """Remove espaços extras de uma coluna"""
    df[coluna] = df[coluna].str.strip()
    return df

# Usar
df = limpar_coluna(df, "MARCA_ARMA")
df = limpar_coluna(df, "CALIBRE_ARMA")
df = limpar_coluna(df, "TIPO_OCORRENCIA")
```

### Desafio 3: Preprocessamento no Carregamento

```python
def carregar_csv_limpo():
    """Carrega CSV e já limpa todas colunas de texto"""
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    
    # Limpar todas colunas de texto (object)
    colunas_texto = df.select_dtypes(include=['object']).columns
    for coluna in colunas_texto:
        df[coluna] = df[coluna].str.strip()
    
    return df
```

---

## 📊 COMPARAÇÃO: ANTES vs DEPOIS

### Busca "Taurus"

| Método | Código | Resultado |
|--------|--------|-----------|
| ❌ Exato | `df["MARCA_ARMA"] == "TAURUS"` | 0 armas |
| ❌ Upper | `df["MARCA_ARMA"] == "TAURUS".upper()` | 0 armas |
| ✅ Contains | `df["MARCA_ARMA"].str.contains("TAURUS")` | 42 armas |
| ✅ Strip + Contains | `.str.strip().str.contains("TAURUS")` | 42 armas |

---

## 🐛 ERROS COMUNS

### Erro 1: Esquecer `na=False`

```python
# ❌ ERRO: Quebra se tiver valores nulos
df[df["MARCA_ARMA"].str.contains("TAURUS")]

# ✅ CORRETO: Ignora nulos
df[df["MARCA_ARMA"].str.contains("TAURUS", na=False)]
```

### Erro 2: Esquecer `case=False`

```python
# ❌ Não encontra "taurus" (minúsculo)
df[df["MARCA_ARMA"].str.contains("TAURUS")]

# ✅ Encontra independente de maiúscula
df[df["MARCA_ARMA"].str.contains("TAURUS", case=False)]
```

---

## 📚 LEITURA ADICIONAL

### Por que CSVs têm espaços extras?

**Resposta:** Formatação de largura fixa.

Alguns sistemas exportam CSVs com **colunas de largura fixa**:
- Facilita leitura visual (alinhamento)
- Compatibilidade com sistemas antigos
- Padrão de alguns bancos de dados

**Exemplo:**
```
MARCA_ARMA                                                    | CALIBRE
TAURUS ARMAS S.A.                                             | .38 TPC
GLOCK GMBH (ÁUSTRIA)                                          | 9mm
```

**Solução:** Sempre usar `.str.strip()` ao processar!

---

## 🎯 QUANDO INSERIR NA AULA

### Opção 1: Durante Parte 2 (14:20-14:40)

**Momento:** Após criar função `contar_armas_marca`

**Roteiro:**
1. Aluno cria função básica
2. Testa: `contar_armas_marca("Taurus")`
3. **Resultado: 0 armas** ❌
4. Professor: "Por que não funciona? Vamos investigar!"
5. Criar `analisar_dados.py` juntos
6. Descobrir espaços extras
7. Refatorar com `.str.strip()` e `.str.contains()`
8. Testar novamente: **Funciona!** ✅

**Vantagem:** Aprendizado orgânico (problema → investigação → solução)

---

### Opção 2: Como Módulo Extra (Opcional após Parte 4)

**Momento:** Após ter 4 tools funcionando (17:15)

**Roteiro:**
1. Professor: "Vocês notaram espaços no CSV?"
2. Explicar problema de dados reais
3. Mostrar técnicas de limpeza
4. Refatorar todas as 4 tools
5. Bonus: Criar função `carregar_csv_limpo()`

**Vantagem:** Revisão e melhoria de código existente

---

## ✅ RESUMO

### Lição Principal:
**Dados reais são sujos!** Sempre inspecione antes de processar.

### Técnicas Essenciais:
1. `.str.strip()` → Remove espaços
2. `.str.contains()` → Busca parcial
3. `case=False` → Ignora maiúsculas
4. `na=False` → Ignora nulos

### Para Código Profissional:
- Sempre limpe dados na entrada
- Use `.str.contains()` para buscas flexíveis
- Documente comportamentos inesperados
- Teste com dados reais (não só exemplos perfeitos)

---

**Módulo:** TRATAMENTO_DE_DADOS_E3.md  
**Localização:** 04_MATERIAL_APOIO/  
**Tempo:** 15-20 minutos  
**Status:** ✅ Pronto para inserir na aula

**Transforme bugs em oportunidades de aprendizado! 🐛→🎓**
