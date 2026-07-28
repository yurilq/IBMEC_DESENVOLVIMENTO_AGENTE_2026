# 🔄 Como Atualizar o Notebook E4

**Problema:** Você está executando código antigo no Jupyter  
**Solução:** Recarregar o notebook atualizado

---

## ✅ SOLUÇÃO RÁPIDA

### Opção 1: Recarregar Notebook (RECOMENDADO)

1. **Fechar o notebook atual:**
   - No Jupyter: `File` → `Close and Halt`
   - Ou feche a aba do navegador

2. **Reabrir o notebook:**
   ```bash
   cd E:\documentos\ibmec\CODIGOS_AULA\E4_RAG_FAISS\02_NOTEBOOK_PASSO_A_PASSO
   jupyter notebook E4_RAG_FAISS.ipynb
   ```

3. **Executar célula corrigida:**
   - Procure a célula "PASSO 2: Carregar Dados E3"
   - Execute (Shift + Enter)
   - Deve mostrar: `[CACHE] Carregando CSV com encoding latin-1...`

---

### Opção 2: Atualizar Célula Manualmente

Se não quiser recarregar, copie e cole este código na célula:

```python
# Cache para carregar dados apenas uma vez
@lru_cache(maxsize=1)
def carregar_csv():
    """
    Carrega dados SINARM do CSV.
    Cache garante que carrega apenas UMA VEZ.
    """
    # Tentar diferentes caminhos
    caminhos_possiveis = [
        "../01_DADOS/DADOS_SINARM/OCORRENCIAS_2026.csv",
        "../01_DADOS/DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026.csv",
        "../../E3_HANDS_ON_CONSTRUCAO_ZERO/01_GUIAS_ALUNO/meu_agente_sinarm/DADOS_SINARM/OCORRENCIAS_2026.csv"
    ]
    
    caminho = None
    for c in caminhos_possiveis:
        if os.path.exists(c):
            caminho = c
            break
    
    if not caminho:
        raise FileNotFoundError(f"Arquivo não encontrado em nenhum dos caminhos: {caminhos_possiveis}")
    
    # Tentar diferentes encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(caminho, encoding=encoding)
            print(f"[CACHE] Carregando CSV com encoding {encoding}...")
            print(f"[OK] {len(df)} registros carregados!")
            return df
        except UnicodeDecodeError:
            continue
    
    raise UnicodeDecodeError(f"Não foi possível ler o arquivo com nenhum encoding testado: {encodings}")

# Testar carregamento
df = carregar_csv()
print(f"\n📊 Primeiros registros:")
df.head()
```

**Passos:**
1. Selecione TODO o código da célula antiga
2. Delete (Ctrl + A, Delete)
3. Cole o código acima (Ctrl + V)
4. Execute (Shift + Enter)

---

## 🎯 Resultado Esperado

### ✅ Sucesso
```
[CACHE] Carregando CSV com encoding latin-1...
[OK] 120 registros carregados!

📊 Primeiros registros:
   MARCA_ARMA  CALIBRE_ARMA  TIPO_ARMA  ...
0  TAURUS      .38           REVOLVER   ...
1  GLOCK       9MM           PISTOLA    ...
...
```

### ❌ Erro (se ainda aparecer)
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc2...
```

**Significa:** Você ainda está executando código antigo

---

## 🔍 Como Verificar se Está Correto

### Código ANTIGO (errado):
```python
df = pd.read_csv(caminho)  # ❌ SEM encoding
```

### Código NOVO (correto):
```python
for encoding in encodings:  # ✅ COM loop de encodings
    try:
        df = pd.read_csv(caminho, encoding=encoding)
```

---

## 🚨 Se Ainda Não Funcionar

### 1. Limpar Cache do Notebook
```python
# Executar em uma célula nova:
%reset -f
```

### 2. Reiniciar Kernel
- No Jupyter: `Kernel` → `Restart & Clear Output`
- Executar todas as células novamente

### 3. Verificar Arquivo
```python
# Executar em uma célula nova:
import os
caminho = "../01_DADOS/DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026.csv"
print(f"Arquivo existe? {os.path.exists(caminho)}")
print(f"Caminho absoluto: {os.path.abspath(caminho)}")
```

---

## 📝 Checklist

- [ ] Fechei o notebook antigo
- [ ] Reabri o notebook atualizado
- [ ] Executei célula de imports
- [ ] Executei célula de carregamento
- [ ] Vi mensagem `[CACHE] Carregando CSV com encoding latin-1...`
- [ ] DataFrame carregou com sucesso

---

## 🎓 Por Que Isso Aconteceu?

1. **Notebook em memória:** Jupyter mantém código em memória
2. **Arquivo atualizado:** Eu atualizei o arquivo .ipynb no disco
3. **Dessincronia:** Seu Jupyter ainda tinha versão antiga em memória

**Solução:** Sempre recarregar notebook após edições externas!

---

## ✅ Próximos Passos

Depois que carregar com sucesso:

1. ✅ Executar células das 8 tools E3
2. ✅ Executar células de RAG
3. ✅ Testar perguntas
4. ✅ Validar funcionamento completo

---

**Status:** ✅ Correção aplicada no arquivo, aguardando reload no Jupyter
