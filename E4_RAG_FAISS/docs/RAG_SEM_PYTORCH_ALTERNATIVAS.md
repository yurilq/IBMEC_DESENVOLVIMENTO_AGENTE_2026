# 🔧 RAG SEM PyTorch - ALTERNATIVAS

**Data:** 23/07/2026 01:45  
**Objetivo:** Implementar RAG sem depender de PyTorch/sentence-transformers

---

## ✅ OPÇÕES DISPONÍVEIS

### **OPÇÃO 1: Usar API de Embeddings (RECOMENDADO para E4)** ⭐

**Vantagens:**
- ✅ Sem PyTorch
- ✅ Sem FAISS local
- ✅ Funciona 100% via API
- ✅ Mais simples para aula

**Providers disponíveis:**
1. **OpenAI Embeddings API** (já temos OpenRouter configurado)
2. **Cohere Embeddings API** (gratuito até 1M chamadas/mês)
3. **Voyage AI** (especializado em embeddings)

**Implementação:**
```python
# Usar OpenAI API para embeddings
from openai import OpenAI
import numpy as np

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."
)

def criar_embedding(texto):
    """Cria embedding via API (sem PyTorch local)"""
    response = client.embeddings.create(
        model="text-embedding-3-small",  # OpenAI
        input=texto
    )
    return response.data[0].embedding

def buscar_similar(query, documentos):
    """Busca documentos similares usando embeddings via API"""
    query_emb = criar_embedding(query)
    
    resultados = []
    for doc in documentos:
        doc_emb = doc['embedding']
        # Similaridade coseno (numpy puro, sem PyTorch)
        similaridade = np.dot(query_emb, doc_emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
        )
        resultados.append({
            'texto': doc['texto'],
            'similaridade': similaridade
        })
    
    # Retornar top 3
    return sorted(resultados, key=lambda x: x['similaridade'], reverse=True)[:3]
```

**Custo:**
- OpenAI embedding-3-small: $0.00002 / 1K tokens
- 100 perguntas × 500 tokens = **$0.001 (R$0.005)** ← Muito barato!

---

### **OPÇÃO 2: TF-IDF + Similaridade Coseno (SEM LLM/Embeddings)**

**Vantagens:**
- ✅ 100% local
- ✅ Zero custo
- ✅ Sem APIs externas
- ✅ Apenas scikit-learn (já instalado)

**Desvantagens:**
- ⚠️ Menos preciso que embeddings
- ⚠️ Não captura semântica profunda

**Implementação:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RAGSimples:
    def __init__(self, documentos):
        """
        documentos: lista de dicts [{'id': 1, 'texto': '...'}]
        """
        self.documentos = documentos
        self.textos = [doc['texto'] for doc in documentos]
        
        # Criar TF-IDF
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.doc_vectors = self.vectorizer.fit_transform(self.textos)
    
    def buscar(self, query, top_k=3):
        """Busca documentos similares via TF-IDF"""
        # Vetorizar query
        query_vector = self.vectorizer.transform([query])
        
        # Calcular similaridade coseno
        similaridades = cosine_similarity(query_vector, self.doc_vectors)[0]
        
        # Top K resultados
        top_indices = np.argsort(similaridades)[-top_k:][::-1]
        
        resultados = []
        for idx in top_indices:
            resultados.append({
                'id': self.documentos[idx]['id'],
                'texto': self.documentos[idx]['texto'],
                'similaridade': float(similaridades[idx])
            })
        
        return resultados

# Uso:
documentos = [
    {'id': 1, 'texto': 'BO é Boletim de Ocorrência policial'},
    {'id': 2, 'texto': 'Furto é crime sem violência'},
    {'id': 3, 'texto': 'Roubo é crime com violência'},
]

rag = RAGSimples(documentos)
resultados = rag.buscar("O que é BO?")
print(resultados[0]['texto'])  # "BO é Boletim de Ocorrência policial"
```

**Dependências:**
- ✅ scikit-learn (já instalado)
- ✅ numpy (já instalado)

---

### **OPÇÃO 3: BM25 (Melhor que TF-IDF)**

**Vantagens:**
- ✅ Mais preciso que TF-IDF
- ✅ 100% local
- ✅ Biblioteca: `rank-bm25` (leve)

**Implementação:**
```python
from rank_bm25 import BM25Okapi
import nltk

class RAGBM25:
    def __init__(self, documentos):
        self.documentos = documentos
        self.textos = [doc['texto'] for doc in documentos]
        
        # Tokenizar
        self.tokenized = [texto.lower().split() for texto in self.textos]
        
        # Criar índice BM25
        self.bm25 = BM25Okapi(self.tokenized)
    
    def buscar(self, query, top_k=3):
        """Busca via BM25"""
        query_tokens = query.lower().split()
        scores = self.bm25.get_scores(query_tokens)
        
        # Top K
        top_indices = np.argsort(scores)[-top_k:][::-1]
        
        resultados = []
        for idx in top_indices:
            resultados.append({
                'id': self.documentos[idx]['id'],
                'texto': self.documentos[idx]['texto'],
                'score': float(scores[idx])
            })
        
        return resultados

# Instalar: pip install rank-bm25
```

---

### **OPÇÃO 4: Híbrido - BM25 + API Embeddings**

**Melhor dos dois mundos:**
- ✅ BM25 para busca inicial rápida (local)
- ✅ API Embeddings para re-rankar top 10
- ✅ Mais preciso e eficiente

**Implementação:**
```python
class RAGHibrido:
    def __init__(self, documentos):
        self.documentos = documentos
        self.bm25 = RAGBM25(documentos)
    
    def buscar(self, query, top_k=3):
        # 1. BM25: buscar top 10 rápido
        candidatos = self.bm25.buscar(query, top_k=10)
        
        # 2. Embeddings: re-rankar top 10
        query_emb = criar_embedding(query)
        
        for cand in candidatos:
            doc_emb = cand['embedding']  # Pre-computado
            cand['similaridade'] = cosine_similarity(query_emb, doc_emb)
        
        # 3. Retornar top K final
        candidatos.sort(key=lambda x: x['similaridade'], reverse=True)
        return candidatos[:top_k]
```

---

## 🎯 RECOMENDAÇÃO PARA E4

### **Melhor opção: OPÇÃO 1 (API Embeddings)** ⭐

**Por quê?**
1. ✅ Funciona 100% (sem erro PyTorch)
2. ✅ Simples de implementar (30 linhas)
3. ✅ Custo muito baixo (R$0.005 para 100 testes)
4. ✅ Didático: alunos veem RAG funcionando
5. ✅ Usa mesma infraestrutura (OpenRouter) já configurada

**Tempo implementação:** 30-45 minutos

**Complexidade:** Baixa (apenas trocar backend de embeddings)

---

## 📋 IMPLEMENTAÇÃO RÁPIDA (OPÇÃO 1)

Vou criar um arquivo `tool_rag_api.py` que substitui `tool_rag_conceitual.py`:

```python
# tool_rag_api.py
# RAG usando API de Embeddings (SEM PyTorch!)

import json
import numpy as np
from pathlib import Path
from openai import OpenAI
from config_llm import OPENROUTER_API_KEY

# Cliente OpenAI apontando para OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

class RAGSimples:
    """RAG usando embeddings via API (sem PyTorch)"""
    
    def __init__(self, docs_path: str):
        # Carregar documentos
        with open(docs_path, 'r', encoding='utf-8') as f:
            self.documentos = json.load(f)
        
        print(f"[RAG] {len(self.documentos)} documentos carregados")
    
    def criar_embedding(self, texto: str):
        """Cria embedding via API"""
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texto[:8000]  # Limitar tokens
        )
        return np.array(response.data[0].embedding)
    
    def buscar(self, query: str, top_k: int = 3):
        """Busca documentos similares"""
        # Embedding da query
        query_emb = self.criar_embedding(query)
        
        # Calcular similaridade com todos documentos
        resultados = []
        for doc in self.documentos:
            # Embedding do documento (pre-computado ou on-the-fly)
            if 'embedding' in doc:
                doc_emb = np.array(doc['embedding'])
            else:
                doc_emb = self.criar_embedding(doc['texto'])
            
            # Similaridade coseno
            sim = np.dot(query_emb, doc_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
            )
            
            resultados.append({
                'texto': doc['texto'],
                'similaridade': float(sim)
            })
        
        # Top K
        resultados.sort(key=lambda x: x['similaridade'], reverse=True)
        return resultados[:top_k]
    
    def get_context(self, query: str, k: int = 3, threshold: float = 0.5):
        """Retorna contexto formatado"""
        resultados = self.buscar(query, top_k=k)
        
        # Filtrar por threshold
        resultados = [r for r in resultados if r['similaridade'] >= threshold]
        
        if not resultados:
            return "[INFO] Nenhum documento relevante encontrado"
        
        # Formatar contexto
        contexto = "DOCUMENTOS RELEVANTES:\n\n"
        for i, r in enumerate(resultados, 1):
            contexto += f"[Doc {i}] (Similaridade: {r['similaridade']:.2f})\n"
            contexto += f"{r['texto']}\n\n"
        
        return contexto


# Criar instância global
rag = None

def buscar_conhecimento_sinarm(query: str) -> str:
    """Interface compatível com v4.5"""
    global rag
    
    if rag is None:
        docs_path = Path(__file__).parent / "DADOS_SINARM" / "documentos.json"
        rag = RAGSimples(str(docs_path))
    
    contexto = rag.get_context(query, k=3, threshold=0.5)
    return contexto
```

**Usar no agente:**
```python
# Trocar linha 13 do agente_v4_5_rag.py:
# from tool_rag_conceitual import buscar_conhecimento_sinarm  # ANTIGO (PyTorch)
from tool_rag_api import buscar_conhecimento_sinarm  # NOVO (API)
```

---

## ⚖️ COMPARAÇÃO DE OPÇÕES

| Opção | Precisão | Velocidade | Custo | Complexidade | PyTorch? |
|-------|----------|------------|-------|--------------|----------|
| **1. API Embeddings** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | $0.001 | ⭐⭐ | ❌ |
| **2. TF-IDF** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $0 | ⭐ | ❌ |
| **3. BM25** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $0 | ⭐⭐ | ❌ |
| **4. Híbrido** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | $0.001 | ⭐⭐⭐ | ❌ |
| **PyTorch+FAISS** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $0 | ⭐⭐⭐⭐⭐ | ✅ (erro!) |

---

## 🚀 PRÓXIMOS PASSOS

### **Para implementar AGORA (30 min):**

1. ✅ Criar `tool_rag_api.py` (código acima)
2. ✅ Preparar `documentos.json` (5-10 documentos conceituais)
3. ✅ Modificar `agente_v4_5_rag.py` linha 13 (trocar import)
4. ✅ Testar com perguntas conceituais
5. ✅ Rodar suite de 100 testes

### **Para implementar DEPOIS (caso queira otimizar):**

1. ⏳ Pre-computar embeddings de todos documentos
2. ⏳ Salvar embeddings em arquivo (cache)
3. ⏳ Implementar BM25 + API híbrido
4. ⏳ Adicionar re-ranking

---

## ✅ CONCLUSÃO

**SIM, é totalmente possível implementar RAG sem PyTorch!**

**Melhor opção para E4:**
- **API Embeddings (OpenAI via OpenRouter)**
- Custo: R$0.005 para 100 testes
- Tempo implementação: 30 minutos
- Funciona 100% (sem erro)

**Quer que eu implemente agora?** 🚀

---

**Data:** 23/07/2026 01:45  
**Status:** ✅ Análise completa de alternativas  
**Recomendação:** OPÇÃO 1 (API Embeddings) - Simples, funciona, barato
