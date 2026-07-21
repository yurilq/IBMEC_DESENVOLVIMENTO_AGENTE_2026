# GUIA RAPIDO: ERROS COMUNS - PARTE 4

## ✅ vs ❌ COMPARACAO VISUAL

### 1. IMPORT DO @tool

#### ❌ ERRADO (falta import)
```python
import pandas as pd

@tool  # <- ERRO: 'tool' nao definido!
def contar_armas_calibre(calibre: str) -> str:
    pass
```

#### ✅ CERTO
```python
import pandas as pd
from langchain_core.tools import tool  # <- ADICIONAR!

@tool  # <- Agora funciona
def contar_armas_calibre(calibre: str) -> str:
    pass
```

---

### 2. INDENTACAO

#### ❌ ERRADO (progressiva)
```python
def contar_armas_calibre(calibre: str) -> str:
    """Docstring"""
        df = pd.read_csv(...)     # <- 8 espacos
            resultado = ...        # <- 12 espacos
                return resultado   # <- 16 espacos
```

#### ✅ CERTO (4 espacos consistentes)
```python
def contar_armas_calibre(calibre: str) -> str:
    """Docstring"""
    df = pd.read_csv(...)     # <- 4 espacos
    resultado = ...            # <- 4 espacos
    return resultado           # <- 4 espacos
```

---

### 3. NOME DA COLUNA

#### ❌ ERRADO (coluna nao existe)
```python
resultado = df[df["CALIBRE"] == calibre]  # KeyError!
```

#### ✅ CERTO
```python
# Verificar primeiro
print(df.columns)
# ['MARCA_ARMA', 'CALIBRE_ARMA', ...]  <- Nome correto!

# Usar nome correto
resultado = df[df["CALIBRE_ARMA"].str.contains(calibre, case=False, na=False)]
```

---

### 4. BUSCA COM ESPACOS

#### ❌ ERRADO (busca exata - falha com espacos)
```python
resultado = df[df["CALIBRE_ARMA"] == ".38"]
# Retorna 0 (CSV tem espacos!)
```

#### ✅ CERTO (busca com contains)
```python
# Limpar espacos
df["CALIBRE_ARMA"] = df["CALIBRE_ARMA"].str.strip()

# Buscar com contains (mais robusto)
resultado = df[df["CALIBRE_ARMA"].str.contains(".38", case=False, na=False)]
# Retorna 17564!
```

---

### 5. CACHE

#### ❌ ERRADO (sem @lru_cache)
```python
def carregar_csv():  # <- Sem decorator
    df = pd.read_csv(...)
    return df
```
**Resultado:** Carrega CSV multiplas vezes (LENTO!)

#### ✅ CERTO (com @lru_cache)
```python
from functools import lru_cache

@lru_cache(maxsize=1)  # <- Decorator ESSENCIAL!
def carregar_csv():
    df = pd.read_csv(...)
    return df
```
**Resultado:** Carrega CSV SO 1 VEZ (RAPIDO!)

---

### 6. DOCSTRING

#### ❌ ERRADO (indentacao inconsistente)
```python
def contar_armas_calibre(calibre: str) -> str:
    """Conta armas.
        
            Args:
                    calibre: ...
                        
                            Returns:
                                    Total...
                                        """
```

#### ✅ CERTO (indentacao consistente)
```python
def contar_armas_calibre(calibre: str) -> str:
    """Conta armas.
    
    Args:
        calibre: Calibre da arma
    
    Returns:
        Total de armas
    """
```

---

### 7. ESTRUTURA COMPLETA

#### ✅ CODIGO COMPLETO CORRETO

```python
# tools_basicas_v2.py
import pandas as pd
from functools import lru_cache
from langchain_core.tools import tool

@lru_cache(maxsize=1)
def carregar_csv():
    """Carrega CSV UMA VEZ"""
    print("[CACHE] Carregando CSV...")
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    
    # Limpar espacos
    df["CALIBRE_ARMA"] = df["CALIBRE_ARMA"].str.strip()
    
    print(f"[OK] CSV carregado! {len(df)} linhas")
    return df

@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta armas por calibre.
    
    Args:
        calibre: Calibre da arma
    
    Returns:
        Total de armas
    """
    df = carregar_csv()  # Usa cache!
    resultado = df[df["CALIBRE_ARMA"].str.contains(calibre, case=False, na=False)]
    total = len(resultado)
    
    if total > 0:
        calibre_real = resultado["CALIBRE_ARMA"].iloc[0]
        return f"Encontrei {total} armas calibre '{calibre_real}'"
    else:
        return f"Nao encontrei armas calibre '{calibre}'"
```

---

## 🧪 COMO TESTAR

### Teste 1: Verificar imports
```python
python -c "from tools_basicas_v2 import contar_armas_calibre; print('OK!')"
```

### Teste 2: Executar funcao
```python
python -c "from tools_basicas_v2 import contar_armas_calibre; print(contar_armas_calibre.func('.38'))"
```
**Esperado:** "Encontrei 17564 armas..."

### Teste 3: Executar arquivo completo
```bash
python tools_basicas_v2.py
```
**Esperado:** "[CACHE] Carregando CSV..." aparece SO 1 VEZ!

---

## 📋 CHECKLIST DE VERIFICACAO

Antes de executar, verifique:

- [ ] ✅ Import correto: `from langchain_core.tools import tool`
- [ ] ✅ Import cache: `from functools import lru_cache`
- [ ] ✅ Decorator @lru_cache na funcao carregar_csv
- [ ] ✅ Decorator @tool em todas as tools
- [ ] ✅ Indentacao: 4 espacos consistentes
- [ ] ✅ Coluna correta: `CALIBRE_ARMA` (nao `CALIBRE`)
- [ ] ✅ Usa .str.strip() e .str.contains()
- [ ] ✅ Docstring bem formatada (4 espacos)

---

## 🆘 RESOLVER PROBLEMAS

### Se der erro de import:
```bash
pip install langchain-core langchain-ollama
```

### Se der erro de indentacao:
1. Selecione todo o codigo
2. VS Code: Shift+Alt+F (formatar)
3. PyCharm: Ctrl+Alt+L (formatar)

### Se retornar 0 resultados:
```python
# Debugar passo a passo
df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", sep=";", encoding="latin1")
print(df.columns)  # Ver colunas
print(df["CALIBRE_ARMA"].unique()[:5])  # Ver valores
print(df["CALIBRE_ARMA"].str.len().max())  # Ver tamanho (espacos?)
```

---

## 💡 DICAS

1. **Sempre copie codigo SEM formatar no Word/Google Docs**
   - Use editor de texto puro (VS Code, Notepad++)
   
2. **Configure seu editor:**
   - Tab size: 4
   - Insert spaces: true
   - Trim trailing whitespace: true

3. **Use verificacao de sintaxe:**
   ```bash
   python -m py_compile tools_basicas_v2.py
   ```

4. **Teste funcoes isoladamente antes de integrar no agente**

---

**LEMBRE-SE:** Indentacao em Python NAO eh opcional - ela define a estrutura do codigo!
