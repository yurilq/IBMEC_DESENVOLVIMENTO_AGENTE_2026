# 📄 DOCUMENTOS CONCEITUAIS (REUTILIZADOS DO E4)

**Origem:** E4_RAG_FAISS/01_DADOS/documentos_conceituais/  
**Uso no E5:** Comparação TF-IDF (E4) vs Sentence-BERT (E5)

---

## 📚 ARQUIVOS DISPONÍVEIS

### 1. **calibres_armas.txt** (5.4 KB)
- Explicação sobre calibres de armas de fogo
- Diferenças entre calibres comuns (.38, 9mm, .45, etc.)
- Curiosidades e comparações

### 2. **marcas_armas.txt** (8.3 KB)
- Principais fabricantes de armas
- Modelos mais comuns no Brasil
- Características de cada marca

### 3. **sistema_sinarm.txt** (8.6 KB)
- O que é o SINARM
- Como funciona o registro de armas
- Procedimentos e legislação

### 4. **tipos_armas.txt** (9.2 KB)
- Classificação de armas de fogo
- Diferenças entre pistola, revólver, rifle, etc.
- Características técnicas

### 5. **rag_conceitos.txt** (11.1 KB)
- Conceitos de RAG (Retrieval-Augmented Generation)
- Como funciona o retrieval
- Diferenças entre TF-IDF e embeddings

### 6. **boletim_ocorrencia.txt** (9.1 KB)
- Como fazer BO de arma
- Procedimentos PCDF
- Informações obrigatórias

---

## 🎯 USO NO E5

Esses arquivos são usados para **comparar** duas técnicas de busca:

### **TF-IDF (E4) - Busca por palavras-chave**
```python
vectorizer_tfidf = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
embeddings_tfidf = vectorizer_tfidf.fit_transform(textos_chunks)
```

### **Sentence-BERT (E5) - Busca por significado**
```python
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedding_model.encode(textos_chunks)
```

---

## 📊 EXEMPLO DE COMPARAÇÃO

**Pergunta:** "O que é calibre de arma?"

**TF-IDF (E4):**
- Busca por palavras-chave: "calibre", "arma"
- Pode retornar documentos com essas palavras, mas em contexto diferente
- Exemplo: "boletim_ocorrencia.txt" (menciona "arma" mas não explica calibre)

**Sentence-BERT (E5):**
- Busca por significado semântico
- Entende que a pergunta é sobre **conceito de calibre**
- Retorna: "calibres_armas.txt" (explica o que é calibre)

---

## 🔄 ATUALIZAÇÃO

Esses arquivos foram **copiados do E4** para o E5 em 28/07/2026.

Se precisar atualizar, copie novamente do E4:
```bash
Copy-Item -Path "E:\documentos\ibmec\CODIGOS_AULA\E4_RAG_FAISS\01_DADOS\documentos_conceituais\*.txt" -Destination "E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\01_DADOS\documentos_conceituais\" -Force
```

---

**Total:** 6 arquivos | 51.7 KB  
**Formato:** UTF-8 (texto puro)  
**Uso:** Comparação TF-IDF vs Sentence-BERT
