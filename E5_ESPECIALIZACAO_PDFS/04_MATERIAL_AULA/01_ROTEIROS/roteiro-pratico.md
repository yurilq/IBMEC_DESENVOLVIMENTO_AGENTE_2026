# 📖 Roteiro Prático - E5: RAG Especializado com PDFs

**Tempo Total:** 5 horas (terça/quinta 13h-18h)

---

## ⏰ CRONOGRAMA

### **13:00-14:15 (1h15min) - BLOCO 1: Fundamentos**

#### Teoria (30min)
- Recap E4 (TF-IDF, 9 tools)
- Limitações do E4
- Solução do E5 (Sentence-BERT + Reranking)
- Comparação E4 vs E5

#### Prática (45min)
- **ATIVIDADE 1:** Carregamento de Dados
  - Executar `exemplo_01_basico.py`
  - Explorar estrutura de dados
  - Validar carregamento

**Checkpoint 1:** CSV + .txt + PDFs carregados? ✅

---

### **14:15-14:30 (15min) - INTERVALO 1**

---

### **14:30-15:30 (1h) - BLOCO 2: Processamento**

#### Prática (60min)
- **ATIVIDADE 2:** Processamento de Chunks
  - Entender chunking híbrido
  - Testar diferentes tamanhos
  - Comparar semântico vs fixo
  - Validar qualidade

**Checkpoint 2:** 915 chunks preparados? ✅

---

### **15:30-16:15 (45min) - BLOCO 3: Embeddings**

#### Teoria (15min)
- Sentence-BERT vs TF-IDF
- 384 dimensões
- Multilíngue
- Comparação de resultados

#### Prática (30min)
- **ATIVIDADE 3:** Geração de Embeddings
  - Carregar modelo Sentence-BERT
  - Gerar embeddings (915 x 384)
  - Salvar índices
  - Carregar índices

**Checkpoint 3:** Embeddings gerados e salvos? ✅

---

### **16:15-16:30 (15min) - INTERVALO 2**

---

### **16:30-17:50 (1h20min) - BLOCO 4: Busca e Reranking**

#### Teoria (20min)
- Busca com NumPy (por que não FAISS?)
- Pipeline 2-estágios
- CrossEncoder
- Métricas de avaliação

#### Prática (60min)
- **ATIVIDADE 4:** Busca e Reranking
  - Executar `exemplo_03_avancado.py`
  - Comparar busca simples vs reranking
  - Calcular métricas
  - Gerar relatório

**Checkpoint 4:** Reranking melhora resultados? ✅

---

### **17:50-18:00 (10min) - ENCERRAMENTO**

- Resumo do aprendizado
- Próximos passos (E6)
- Dúvidas e discussão

---

## 📋 ATIVIDADES DETALHADAS

### **ATIVIDADE 1: Carregamento de Dados (30min)**

**Objetivo:** Carregar e explorar dados

**Passos:**

1. **Abrir terminal e navegar para projeto:**
   ```bash
   cd E5_ESPECIALIZACAO_PDFS/03_PROJETO_ESTRUTURADO
   ```

2. **Ativar ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar exemplo básico:**
   ```bash
   python ../04_MATERIAL_AULA/02_EXEMPLOS/exemplo_01_basico.py
   ```

5. **Explorar dados:**
   - Quantos registros no CSV?
   - Quantos documentos .txt?
   - Quantos PDFs?
   - Qual o tamanho total?

**Validação:**
- [ ] CSV carregado (74.758 registros)?
- [ ] Documentos .txt carregados (6 arquivos)?
- [ ] PDFs carregados (5 arquivos)?
- [ ] Sem erros de encoding?

---

### **ATIVIDADE 2: Processamento de Chunks (40min)**

**Objetivo:** Entender chunking e preparar dados

**Passos:**

1. **Abrir notebook ou script:**
   ```python
   from src.chunker import chunk_text_hibrido, preparar_todos_chunks
   from src.loader import carregar_documentos_txt, carregar_pdfs
   
   docs_txt = carregar_documentos_txt()
   pdfs = carregar_pdfs()
   
   # Testar diferentes tamanhos
   chunks_pequeno = chunk_text_hibrido(docs_txt[0]['conteudo'], chunk_size=300)
   chunks_medio = chunk_text_hibrido(docs_txt[0]['conteudo'], chunk_size=500)
   chunks_grande = chunk_text_hibrido(docs_txt[0]['conteudo'], chunk_size=1000)
   
   print(f"Pequeno: {len(chunks_pequeno)} chunks")
   print(f"Médio: {len(chunks_medio)} chunks")
   print(f"Grande: {len(chunks_grande)} chunks")
   ```

2. **Comparar qualidade:**
   - Qual tamanho preserva melhor o contexto?
   - Qual tem menos overlap?
   - Qual é mais eficiente?

3. **Preparar todos os chunks:**
   ```python
   todos_chunks = preparar_todos_chunks(docs_txt, pdfs)
   print(f"Total: {len(todos_chunks)} chunks")
   ```

**Validação:**
- [ ] Chunks criados (>50)?
- [ ] Tamanho médio ~500-700 caracteres?
- [ ] Sem chunks vazios?
- [ ] Overlap funcionando?

---

### **ATIVIDADE 3: Geração de Embeddings (50min)**

**Objetivo:** Gerar e salvar embeddings

**Passos:**

1. **Carregar modelo:**
   ```python
   from src.embeddings import carregar_modelo_embedding, gerar_embeddings
   
   modelo = carregar_modelo_embedding()
   print(f"Dimensões: {modelo.get_embedding_dimension()}")
   ```

2. **Gerar embeddings:**
   ```python
   textos = [chunk['texto'] for chunk in todos_chunks]
   embeddings = gerar_embeddings(textos, modelo)
   print(f"Shape: {embeddings.shape}")  # Deve ser (915, 384)
   ```

3. **Salvar índices:**
   ```python
   from src.embeddings import salvar_embeddings
   import numpy as np
   
   salvar_embeddings(embeddings, "./data/indices/embeddings.npy")
   np.save("./data/indices/chunks_metadata.npy", todos_chunks)
   ```

4. **Carregar e validar:**
   ```python
   from src.embeddings import carregar_embeddings
   
   embeddings_carregados = carregar_embeddings("./data/indices/embeddings.npy")
   print(f"Carregados: {embeddings_carregados.shape}")
   ```

**Validação:**
- [ ] Modelo carregado (384 dimensões)?
- [ ] Embeddings gerados (915 x 384)?
- [ ] Arquivo salvo (~1.34 MB)?
- [ ] Carregamento funciona?

---

### **ATIVIDADE 4: Busca e Reranking (60min)**

**Objetivo:** Testar busca e reranking

**Passos:**

1. **Executar exemplo avançado:**
   ```bash
   python ../04_MATERIAL_AULA/02_EXEMPLOS/exemplo_03_avancado.py
   ```

2. **Analisar resultados:**
   - Busca simples retorna bons resultados?
   - Reranking melhora os resultados?
   - Qual é a melhoria percentual?

3. **Testar múltiplas perguntas:**
   ```python
   from src.search import buscar_numpy
   from src.reranker import buscar_com_reranking
   
   perguntas = [
       "O que é calibre?",
       "Diferença entre pistola e revolver?",
       "Como funciona o SINARM?"
   ]
   
   for pergunta in perguntas:
       print(f"\n❓ {pergunta}")
       
       # Busca simples
       simples = buscar_numpy(pergunta, embeddings, todos_chunks, modelo, k=3)
       print("Simples:")
       for chunk, score in simples:
           print(f"  - {chunk['arquivo']}: {score:.3f}")
       
       # Com reranking
       reranking = buscar_com_reranking(pergunta, embeddings, todos_chunks, modelo, reranker, k_final=3)
       print("Reranking:")
       for chunk, score in reranking:
           print(f"  - {chunk['arquivo']}: {score:.3f}")
   ```

4. **Calcular métricas:**
   ```python
   from tools.metrics import avaliar_completo
   
   # Definir documentos relevantes
   relevantes = ['calibres_armas.txt', 'cartilha-de-armamento-e-tiro.pdf']
   
   metricas = avaliar_completo(resultados_reranking, relevantes, k=5)
   
   for metrica, valor in metricas.items():
       print(f"{metrica}: {valor:.3f}")
   ```

**Validação:**
- [ ] Busca funciona?
- [ ] Reranking melhora resultados?
- [ ] Métricas calculadas?
- [ ] Relatório gerado?

---

## 🎯 Checkpoints

### Checkpoint 1: Carregamento ✅
```
[CACHE] Carregando CSV com encoding=latin-1, sep=';'
[OK] 74758 registros, 10 colunas carregadas!
📚 6 documentos .txt carregados
✅ 5 PDFs carregados com sucesso!
```

### Checkpoint 2: Chunks ✅
```
📚 Processando documentos .txt...
✅ 131 chunks de .txt

📄 Processando PDFs...
✅ 784 chunks de PDFs

🎉 Total: 915 chunks preparados!
```

### Checkpoint 3: Embeddings ✅
```
📥 Carregando Sentence-BERT...
✅ Modelo carregado!
   Dimensões: 384

🔄 Gerando embeddings para 915 textos...
✅ Embeddings gerados!
   Forma: (915, 384)
```

### Checkpoint 4: Busca ✅
```
❓ Pergunta: O que é calibre?

📊 Busca Simples (NumPy):
  1. calibres_armas.txt (score: 0.519)
  2. cartilha-de-armamento-e-tiro.pdf (score: 0.506)
  3. procedimento_operacional_padrao-pericia_criminal.pdf (score: 0.501)

📊 Busca com Reranking:
  1. calibres_armas.txt (score: 8.514)
  2. cartilha-de-armamento-e-tiro.pdf (score: 6.706)
  3. cartilha-de-armamento-e-tiro.pdf (score: 5.510)

📈 Melhoria: +200%
```

---

## 💡 Dicas Importantes

1. **Primeira execução é lenta:**
   - Modelo Sentence-BERT: ~1 minuto para baixar
   - Geração de embeddings: ~1-2 minutos
   - Reranking: ~30 segundos para carregar

2. **Reutilizar embeddings:**
   - Salve embeddings após gerar
   - Carregue em próximas execuções
   - Economiza tempo

3. **Ajustar parâmetros:**
   - `k_inicial`: Aumentar para mais candidatos
   - `k_final`: Aumentar para mais resultados
   - `threshold`: Aumentar para filtro mais rigoroso

4. **Troubleshooting:**
   - Erro de arquivo? Verificar `.env`
   - Erro de memória? Reduzir batch_size
   - PDF não extraído? Aumentar chunk_size

---

**Bom aprendizado! 🚀**
