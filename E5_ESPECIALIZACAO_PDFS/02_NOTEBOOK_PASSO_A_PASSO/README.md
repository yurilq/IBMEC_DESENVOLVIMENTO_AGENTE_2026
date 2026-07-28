# 📓 NOTEBOOK E5 - PASSO A PASSO

**Arquivo:** `E5_ESPECIALIZACAO_PDFS.ipynb`

---

## 🎯 OBJETIVO

Notebook didático incremental que estende o E4 com:
- Processamento de PDFs
- FAISS para busca vetorial
- Reranking com CrossEncoder
- Métricas de avaliação

---

## 📋 ESTRUTURA (21 PASSOS)

### PARTE 1: RECAP E4 (Passos 1-3)
- Recap do que foi construído no E4
- Limitações do E4
- Solução do E5

### PARTE 2: PROCESSAR PDFs (Passos 4-6)
- Carregar PDFs
- Chunking inteligente (fixo vs semântico)
- Preparar todos os chunks

### PARTE 3: EMBEDDINGS SEMÂNTICOS (Passos 7-9)
- Carregar Sentence-BERT
- Gerar embeddings
- Comparar TF-IDF vs Sentence-BERT

### PARTE 4: FAISS (Passos 10-12)
- Criar índice FAISS
- Testar busca
- Salvar e carregar índice

### PARTE 5: RERANKING (Passos 13-15)
- Carregar CrossEncoder
- Implementar pipeline com reranking
- Comparar SEM vs COM reranking

### PARTE 6: MÉTRICAS (Passos 16-19)
- Criar dataset de teste
- Implementar métricas (Precision@K, MRR, Recall@K)
- Avaliar sistema
- Comparar resultados

### PARTE 7: INTEGRAÇÃO (Passos 20-21)
- Tool RAG especializado
- Roteador inteligente

---

## ⏱️ TEMPO ESTIMADO

**Total:** 5 horas

- PARTE 1: 30 min
- PARTE 2: 1h
- PARTE 3: 1h
- PARTE 4: 45 min
- PARTE 5: 45 min
- PARTE 6: 1h
- PARTE 7: 30 min

---

## 🚀 COMO USAR

### 1. Instalar Dependências

```bash
pip install pandas langchain-core scikit-learn faiss-cpu sentence-transformers PyPDF2
```

### 2. Abrir Notebook

```bash
jupyter notebook E5_ESPECIALIZACAO_PDFS.ipynb
```

### 3. Executar Células

Execute as células **na ordem**, uma por vez.

**⚠️ IMPORTANTE:**
- Não pule células
- Aguarde cada célula terminar antes de executar a próxima
- Preste atenção nos checkpoints

---

## ✅ CHECKPOINTS

O notebook tem **6 checkpoints** para validar o progresso:

### Checkpoint 1 (após Passo 3)
- [ ] CSV carregado (74.758 registros)?
- [ ] Documentos .txt carregados (5-6 arquivos)?
- [ ] Imports funcionando?

### Checkpoint 2 (após Passo 6)
- [ ] PDFs carregados (ou aviso se não houver)?
- [ ] Chunks criados (>50 chunks esperados)?
- [ ] Tamanho médio ~500 caracteres?

### Checkpoint 3 (após Passo 9)
- [ ] Sentence-BERT carregado?
- [ ] Embeddings gerados (384 dimensões)?
- [ ] Busca funciona?
- [ ] Sentence-BERT retorna resultados mais relevantes?

### Checkpoint 4 (após Passo 12)
- [ ] Índice FAISS criado?
- [ ] Busca funciona?
- [ ] Índice salvo em disco?
- [ ] Carregamento funciona?

### Checkpoint 5 (após Passo 15)
- [ ] CrossEncoder carregado?
- [ ] Pipeline de reranking funciona?
- [ ] Resultados com reranking são melhores?
- [ ] Tempo de busca aceitável (<100ms)?

### Checkpoint 6 (após Passo 19)
- [ ] Dataset de teste criado?
- [ ] Métricas implementadas?
- [ ] Avaliação executada?
- [ ] Reranking melhora métricas?

---

## 📊 RESULTADOS ESPERADOS

### Métricas Finais

| Métrica | E4 (TF-IDF) | E5 (FAISS + Reranking) | Melhoria |
|---------|-------------|------------------------|----------|
| **Precision@5** | ~0.40 | ~0.86 | +115% |
| **MRR** | ~0.55 | ~0.91 | +65% |
| **Recall@5** | ~0.50 | ~0.90 | +80% |

### Tempo de Busca

- **SEM Reranking:** ~5ms
- **COM Reranking:** ~50ms (+10x, mas muito mais preciso)

---

## 🛠️ TROUBLESHOOTING

### Erro: "FAISS não instala"

```bash
# Tentar CPU version
pip install faiss-cpu

# Ou GPU version (se tiver CUDA)
pip install faiss-gpu
```

### Erro: "Sentence-BERT demora muito"

**Normal!** Primeira vez baixa o modelo (~120 MB).

Próximas execuções são rápidas (modelo fica em cache).

### Erro: "PDF não carrega"

Verifique se a pasta `../01_DADOS/pdfs_pcdf/` existe.

Se não houver PDFs, o notebook continua funcionando (só com .txt).

### Erro: "Memória insuficiente"

Reduza o número de chunks:

```python
# Em vez de processar todos
todos_chunks = todos_chunks[:100]  # Processar apenas 100
```

---

## 📁 ARQUIVOS GERADOS

Após executar o notebook, serão criados:

```
01_DADOS/
└── indices/
    ├── faiss_index.bin          # Índice FAISS (pode ser grande)
    └── chunks_metadata.npy      # Metadata dos chunks
```

**💡 Dica:** Esses arquivos podem ser reutilizados no agente consolidado!

---

## 🎓 CONCEITOS APRENDIDOS

### Técnicos
- Processamento de PDFs com PyPDF2
- Chunking semântico vs fixo
- Embeddings com Sentence-BERT
- Busca vetorial com FAISS
- Reranking com CrossEncoder
- Métricas de avaliação (Precision@K, MRR, Recall@K)

### Práticos
- Trade-off velocidade vs precisão
- Quando usar reranking
- Como avaliar sistemas RAG
- Comparação de métodos

---

## 📚 RECURSOS ADICIONAIS

### Documentação
- **FAISS:** https://github.com/facebookresearch/faiss
- **Sentence-Transformers:** https://www.sbert.net/
- **PyPDF2:** https://pypdf2.readthedocs.io/

### Tutoriais
- **RAG com FAISS:** https://www.sbert.net/examples/applications/retrieve_rerank/README.html
- **Reranking:** https://www.sbert.net/examples/applications/cross-encoder/README.html

---

## 🔄 PRÓXIMOS PASSOS

Após completar o notebook:

1. ✅ Entender cada conceito
2. ✅ Experimentar com diferentes hiperparâmetros
3. ✅ Adicionar mais PDFs
4. ✅ Criar agente consolidado (.py)
5. ✅ Testar em produção

---

## 💡 DICAS

### Para Alunos
- Execute célula por célula
- Leia os comentários
- Teste com suas próprias perguntas
- Compare resultados E4 vs E5

### Para Professores
- Demonstre ao vivo a diferença TF-IDF vs Sentence-BERT
- Mostre impacto do reranking nas métricas
- Explique trade-off velocidade vs precisão
- Conecte com casos reais PCDF

---

**Última atualização:** 26/07/2026  
**Versão:** 1.0  
**Status:** ✅ Pronto para uso
