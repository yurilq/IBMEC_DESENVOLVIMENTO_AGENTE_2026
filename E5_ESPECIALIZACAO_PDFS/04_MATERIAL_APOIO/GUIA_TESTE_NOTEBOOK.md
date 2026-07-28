# GUIA: COMO TESTAR O NOTEBOOK E5

## ⚠️ PROBLEMA IDENTIFICADO

O teste automatizado falhou devido a:
1. **Imports não executados** (células marcadas como comentário)
2. **Encoding de emojis** no Windows (PowerShell não suporta UTF-8 completo)
3. **Dependências entre células** (cada célula depende das anteriores)

## ✅ SOLUÇÃO: TESTAR NO JUPYTER

### Opção 1: Jupyter Notebook (RECOMENDADO)

```bash
# 1. Navegar até a pasta
cd E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\02_NOTEBOOK_PASSO_A_PASSO

# 2. Abrir Jupyter
jupyter notebook E5_ESPECIALIZACAO_PDFS.ipynb

# 3. Executar células sequencialmente
#    - Kernel > Restart & Run All
#    - Ou executar célula por célula (Shift+Enter)
```

### Opção 2: JupyterLab

```bash
# 1. Navegar até a pasta
cd E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\02_NOTEBOOK_PASSO_A_PASSO

# 2. Abrir JupyterLab
jupyter lab E5_ESPECIALIZACAO_PDFS.ipynb

# 3. Executar células sequencialmente
```

### Opção 3: VS Code

```bash
# 1. Abrir VS Code
code E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\02_NOTEBOOK_PASSO_A_PASSO\E5_ESPECIALIZACAO_PDFS.ipynb

# 2. Instalar extensão Jupyter (se não tiver)
# 3. Executar células sequencialmente
```

## 📋 CHECKLIST DE TESTE

### Pré-requisitos

- [ ] Python 3.8+ instalado
- [ ] Jupyter instalado (`pip install jupyter`)
- [ ] Dependências instaladas (executar célula 3 do notebook)

### Teste Sequencial

Execute as células **NA ORDEM** e valide cada checkpoint:

#### ✅ CHECKPOINT 1 (após célula ~10)
- [ ] CSV carregado (74.758 registros)?
- [ ] Documentos .txt carregados (5-6 arquivos)?
- [ ] Imports funcionando?

#### ✅ CHECKPOINT 2 (após célula ~18)
- [ ] PDFs carregados (4 arquivos)?
- [ ] Chunks criados (>50 chunks)?
- [ ] Tamanho médio ~500 caracteres?

#### ✅ CHECKPOINT 3 (após célula ~26)
- [ ] Sentence-BERT carregado?
- [ ] Embeddings gerados (384 dimensões)?
- [ ] Busca funciona?
- [ ] Sentence-BERT retorna resultados mais relevantes?

#### ✅ CHECKPOINT 4 (após célula ~34)
- [ ] Índice FAISS criado?
- [ ] Busca funciona?
- [ ] Índice salvo em disco?
- [ ] Carregamento funciona?

#### ✅ CHECKPOINT 5 (após célula ~42)
- [ ] CrossEncoder carregado?
- [ ] Pipeline de reranking funciona?
- [ ] Resultados com reranking são melhores?
- [ ] Tempo de busca aceitável (<100ms)?

#### ✅ CHECKPOINT 6 (após célula ~52)
- [ ] Dataset de teste criado?
- [ ] Métricas implementadas?
- [ ] Avaliação executada?
- [ ] Reranking melhora métricas?

#### ✅ CHECKPOINT FINAL (após célula ~62)
- [ ] Tool RAG especializado funciona?
- [ ] Roteador funciona?
- [ ] Sistema completo integrado?

## 🐛 PROBLEMAS COMUNS

### 1. ModuleNotFoundError: No module named 'sentence_transformers'

**Solução:**
```bash
pip install sentence-transformers
# OU
pip install --upgrade sentence-transformers
```

### 2. ModuleNotFoundError: No module named 'faiss'

**Solução:**
```bash
pip install faiss-cpu
# OU (se tiver GPU)
pip install faiss-gpu
```

### 3. Erro ao carregar PDFs

**Solução:**
```bash
pip install PyPDF2
```

### 4. Kernel morreu / Out of Memory

**Solução:**
- Reduzir número de chunks
- Processar PDFs em lotes
- Reiniciar kernel

### 5. Encoding error (caracteres estranhos nos PDFs)

**Solução:**
- Normal! PyPDF2 pode ter problemas com encoding
- Não afeta a busca semântica
- Sentence-BERT captura o significado mesmo com erros

## 📊 RESULTADOS ESPERADOS

### Métricas Finais (Checkpoint 6)

| Métrica | Objetivo | Descrição |
|---------|----------|-----------|
| **Precision@5** | > 0.80 | 80%+ dos top-5 são relevantes |
| **MRR** | > 0.70 | Primeiro relevante nas primeiras posições |
| **Recall@5** | > 0.75 | 75%+ dos relevantes são recuperados |

### Exemplo de Saída (Checkpoint Final)

```
❓ Pergunta: O que é o SINARM?
------------------------------------------------------------

1. 📄 LEI-10.826-03-SINARM.pdf (score: 0.850)
   Art. 1o O Sistema Nacional de Armas – Sinarm, instituído no Ministério da Justiça...

2. 📝 sistema_sinarm.txt (score: 0.720)
   # Sistema SINARM - Sistema Nacional de Armas...

3. 📄 estatuto_desarmamento.pdf (score: 0.650)
   ...
```

## ⏱️ TEMPO ESTIMADO

- **Execução completa:** 15-20 minutos
- **Primeira execução:** 25-30 minutos (download de modelos)
- **Execuções seguintes:** 10-15 minutos (modelos em cache)

## 🚀 PRÓXIMOS PASSOS

Após validar o notebook:

1. ✅ Notebook funciona completamente
2. ⏳ Criar agente consolidado (.py)
3. ⏳ Testar agente em modo interativo
4. ⏳ Deploy em produção

## 📝 REPORTAR PROBLEMAS

Se encontrar erros, documente:

1. **Célula que falhou:** Número da célula
2. **Erro completo:** Copiar mensagem de erro
3. **Ambiente:** Python version, OS, Jupyter version
4. **Dados:** PDFs carregados? Quantos chunks?

---

**Última atualização:** 26/07/2026  
**Versão:** 1.0  
**Status:** ✅ Pronto para teste manual
