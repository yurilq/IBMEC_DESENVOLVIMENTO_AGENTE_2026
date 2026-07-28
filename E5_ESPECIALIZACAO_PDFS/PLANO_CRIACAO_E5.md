# 📋 PLANO DE CRIAÇÃO E5 - CODIGOS_AULA

**Data:** 26/07/2026  
**Status:** ⏳ EM PROGRESSO (60% completo)

---

## ✅ JÁ CRIADO

### Estrutura
- [x] Pasta `E5_ESPECIALIZACAO_PDFS/`
- [x] Subpastas (01_DADOS, 02_NOTEBOOK, 03_AGENTE, 04_APOIO)
- [x] `README.md` principal
- [x] `00_COMECE_AQUI_E5.md`
- [x] `requirements.txt`

---

## ⏳ FALTA CRIAR

### 1. Notebook Incremental (PRIORIDADE ALTA)

**Arquivo:** `02_NOTEBOOK_PASSO_A_PASSO/E5_especializacao_pdfs.ipynb`

**Estrutura (60-80 células):**

```
PARTE 1: RECAP E4 (células 1-10)
- Recap E4 (8 tools + RAG básico)
- Limitações do E4
- O que muda no E5

PARTE 2: SETUP E5 (células 11-15)
- Imports
- Verificar dependências
- Carregar dados E4 (CSV + docs)

PARTE 3: PROCESSAR PDFs (células 16-25)
- Carregar PDFs
- Extrair texto
- Chunking inteligente
- Validar chunks

PARTE 4: EMBEDDINGS (células 26-35)
- Sentence-BERT
- Gerar embeddings
- Comparar com TF-IDF
- Visualizar

PARTE 5: FAISS (células 36-45)
- Criar índice FAISS
- Adicionar embeddings
- Salvar índice
- Testar busca

PARTE 6: RERANKING (células 46-55)
- CrossEncoder
- Pipeline busca + reranking
- Comparar resultados
- Métricas

PARTE 7: INTEGRAÇÃO (células 56-65)
- Tool RAG especializado
- Roteador atualizado
- Testes
- Comparação E4 vs E5

PARTE 8: FINE-TUNING LoRA (células 66-80) [OPCIONAL]
- Preparar dataset
- Configurar LoRA
- Treinar (Google Colab)
- Avaliar
```

**Tempo estimado:** 3-4 horas

---

### 2. Agente Consolidado (PRIORIDADE ALTA)

**Arquivo:** `03_AGENTE_CONSOLIDADO/agente_v5_especializado.py`

**Estrutura (~600 linhas):**

```python
"""
agente_v5_especializado.py
==========================

AGENTE SINARM v5.0 - RAG ESPECIALIZADO COM PDFs

PROGRESSÃO:
- E3: 8 tools (dados CSV)
- E4: 8 tools + RAG básico (TF-IDF + docs .txt)
- E5: 8 tools + RAG especializado (FAISS + PDFs + Reranking)

NOVIDADES E5:
1. FAISS para busca vetorial rápida
2. Sentence-BERT para embeddings semânticos
3. Reranking com CrossEncoder
4. Processamento de PDFs
5. Métricas de avaliação (Precision@K, MRR)

MODOS DE EXECUÇÃO:
1. Sem argumentos: Testes automáticos
2. Com pergunta: Responde pergunta
3. --interativo: Loop de perguntas

AUTOR: MBA IA Generativa PCDF - IBMEC
DATA: 2026-07-26
VERSÃO: 5.0
"""

# ============================================================================
# IMPORTS
# ============================================================================

import pandas as pd
import os
import sys
from functools import lru_cache
from langchain_core.tools import tool
from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss
import numpy as np
from PyPDF2 import PdfReader

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

# Caminhos
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(SCRIPT_DIR, "..", "01_DADOS")
CSV_PATH = os.path.join(DADOS_DIR, "..", "..", "E4_RAG_FAISS", "01_DADOS", "DADOS_SINARM", "OCORRENCIAS", "OCORRENCIAS_2026.csv")
DOCS_PATH = os.path.join(DADOS_DIR, "documentos_conceituais")
PDFS_PATH = os.path.join(DADOS_DIR, "pdfs_pcdf")
FAISS_INDEX_PATH = os.path.join(DADOS_DIR, "faiss_index.bin")

# Modelos
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ============================================================================
# CARREGAMENTO DE DADOS CSV (E3/E4)
# ============================================================================

@lru_cache(maxsize=1)
def carregar_csv():
    """Carrega CSV SINARM (mesmo do E4)"""
    # [CÓDIGO DO E4]
    pass

# ============================================================================
# CARREGAMENTO DE DOCUMENTOS CONCEITUAIS (E4)
# ============================================================================

@lru_cache(maxsize=1)
def carregar_documentos_conceituais():
    """Carrega documentos .txt (mesmo do E4)"""
    # [CÓDIGO DO E4]
    pass

# ============================================================================
# PROCESSAMENTO DE PDFs (NOVO NO E5)
# ============================================================================

@lru_cache(maxsize=1)
def carregar_pdfs():
    """
    Carrega e processa PDFs da PCDF.
    Retorna lista de dicionários com metadata.
    """
    print("[CACHE] Carregando PDFs...")
    
    if not os.path.exists(PDFS_PATH):
        print(f"[AVISO] Pasta de PDFs não encontrada: {PDFS_PATH}")
        return []
    
    pdfs = []
    for root, dirs, files in os.walk(PDFS_PATH):
        for file in files:
            if file.endswith('.pdf'):
                caminho = os.path.join(root, file)
                try:
                    reader = PdfReader(caminho)
                    texto = ""
                    for page in reader.pages:
                        texto += page.extract_text()
                    
                    pdfs.append({
                        'arquivo': file,
                        'caminho': caminho,
                        'conteudo': texto,
                        'num_paginas': len(reader.pages)
                    })
                except Exception as e:
                    print(f"[ERRO] Não foi possível ler {file}: {e}")
    
    print(f"[OK] {len(pdfs)} PDFs carregados!")
    return pdfs

def chunk_text(texto, chunk_size=500, overlap=50):
    """
    Divide texto em chunks com overlap.
    """
    chunks = []
    start = 0
    while start < len(texto):
        end = start + chunk_size
        chunk = texto[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks

# ============================================================================
# SISTEMA RAG ESPECIALIZADO (NOVO NO E5)
# ============================================================================

class SistemaRAGEspecializado:
    """Sistema RAG com FAISS + Reranking"""
    
    def __init__(self):
        self.documentos = []
        self.chunks = []
        self.embeddings = None
        self.index = None
        self.embedding_model = None
        self.reranker = None
        self.inicializado = False
    
    def inicializar(self):
        """Inicializa sistema RAG"""
        if self.inicializado:
            return
        
        print("[RAG] Inicializando sistema RAG especializado...")
        
        # Carregar modelos
        print("[RAG] Carregando Sentence-BERT...")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
        print("[RAG] Carregando CrossEncoder...")
        self.reranker = CrossEncoder(RERANKER_MODEL)
        
        # Carregar documentos
        docs_txt = carregar_documentos_conceituais()
        pdfs = carregar_pdfs()
        
        # Processar documentos .txt
        for doc in docs_txt:
            chunks = chunk_text(doc['conteudo'])
            for i, chunk in enumerate(chunks):
                self.chunks.append({
                    'tipo': 'txt',
                    'arquivo': doc['arquivo'],
                    'chunk_id': i,
                    'texto': chunk
                })
        
        # Processar PDFs
        for pdf in pdfs:
            chunks = chunk_text(pdf['conteudo'])
            for i, chunk in enumerate(chunks):
                self.chunks.append({
                    'tipo': 'pdf',
                    'arquivo': pdf['arquivo'],
                    'chunk_id': i,
                    'texto': chunk
                })
        
        if not self.chunks:
            print("[RAG] Nenhum documento encontrado. RAG desabilitado.")
            return
        
        # Gerar embeddings
        print(f"[RAG] Gerando embeddings para {len(self.chunks)} chunks...")
        textos = [chunk['texto'] for chunk in self.chunks]
        self.embeddings = self.embedding_model.encode(textos, show_progress_bar=True)
        
        # Criar índice FAISS
        print("[RAG] Criando índice FAISS...")
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype('float32'))
        
        # Salvar índice
        faiss.write_index(self.index, FAISS_INDEX_PATH)
        print(f"[RAG] Índice salvo em: {FAISS_INDEX_PATH}")
        
        self.inicializado = True
        print(f"[RAG] Sistema inicializado com {len(self.chunks)} chunks!")
    
    def buscar(self, pergunta, k=20, rerank_k=5):
        """
        Busca com reranking.
        
        Args:
            pergunta: Pergunta do usuário
            k: Número de documentos na busca inicial
            rerank_k: Número de documentos após reranking
        
        Returns:
            Lista de chunks relevantes
        """
        if not self.inicializado:
            self.inicializar()
        
        if not self.inicializado:
            return []
        
        # 1. Busca inicial (top-K)
        query_embedding = self.embedding_model.encode([pergunta])
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # 2. Reranking (top-rerank_K)
        candidates = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                candidates.append(self.chunks[idx])
        
        # Criar pares (pergunta, documento)
        pairs = [[pergunta, chunk['texto']] for chunk in candidates]
        
        # Reranking
        scores = self.reranker.predict(pairs)
        
        # Ordenar por score
        ranked_indices = np.argsort(scores)[::-1][:rerank_k]
        
        # Retornar top-rerank_K
        resultados = []
        for i in ranked_indices:
            chunk = candidates[i]
            resultados.append({
                'tipo': chunk['tipo'],
                'arquivo': chunk['arquivo'],
                'score': float(scores[i]),
                'texto': chunk['texto'][:500]  # Primeiros 500 chars
            })
        
        return resultados

# Instância global
sistema_rag = SistemaRAGEspecializado()

# ============================================================================
# TOOLS E3/E4 (8 TOOLS MANTIDAS)
# ============================================================================

# [COPIAR TOOLS DO E4]

@tool
def contar_armas_marca(marca: str) -> str:
    """Conta armas por marca"""
    # [CÓDIGO DO E4]
    pass

# ... (outras 7 tools)

# ============================================================================
# TOOL RAG ESPECIALIZADO (NOVA NO E5)
# ============================================================================

@tool
def buscar_conhecimento_especializado(pergunta: str) -> str:
    """
    Busca informações em documentos e PDFs da PCDF.
    Usa FAISS + Reranking para máxima precisão.
    
    Args:
        pergunta: Pergunta do usuário
    
    Returns:
        Resposta baseada nos documentos
    """
    # Inicializar RAG
    if not sistema_rag.inicializado:
        sistema_rag.inicializar()
    
    if not sistema_rag.inicializado:
        return "Sistema RAG não disponível."
    
    # Buscar com reranking
    resultados = sistema_rag.buscar(pergunta, k=20, rerank_k=5)
    
    if not resultados:
        return "Não encontrei informações relevantes."
    
    # Montar resposta
    resposta = "Informacoes encontradas:\n\n"
    
    for i, res in enumerate(resultados, 1):
        tipo_emoji = "📄" if res['tipo'] == 'pdf' else "📝"
        resposta += f"[{i}] {tipo_emoji} {res['arquivo']} (score: {res['score']:.2f})\n"
        resposta += f"{res['texto']}\n"
        if i < len(resultados):
            resposta += "\n---\n\n"
    
    return resposta

# ============================================================================
# ROTEADOR (ATUALIZADO)
# ============================================================================

def rotear_pergunta(pergunta: str):
    """Decide qual tool usar"""
    # [CÓDIGO DO E4 ATUALIZADO]
    pass

# ============================================================================
# PROCESSAMENTO
# ============================================================================

def processar_pergunta(pergunta: str) -> str:
    """Processa pergunta"""
    # [CÓDIGO DO E4]
    pass

# ============================================================================
# TESTES AUTOMÁTICOS
# ============================================================================

def executar_testes():
    """Testes automáticos"""
    print("="*60)
    print(" EXECUTANDO TESTES AUTOMATICOS E5")
    print("="*60)
    
    # Testes E3/E4
    testes_e3_e4 = [
        "Quantas armas Taurus existem?",
        "O que é calibre?",
    ]
    
    # Testes E5 (PDFs)
    testes_e5 = [
        "O que diz o Estatuto do Desarmamento sobre porte de arma?",
        "Como fazer depoimento especial de criança?",
        "Quais são os procedimentos para apreensão de arma?",
    ]
    
    print("\n TESTES E3/E4")
    print("-"*60)
    for pergunta in testes_e3_e4:
        resposta = processar_pergunta(pergunta)
        print(f" {resposta[:200]}...\n")
    
    print("\n TESTES E5 (PDFs)")
    print("-"*60)
    for pergunta in testes_e5:
        resposta = processar_pergunta(pergunta)
        print(f" {resposta[:200]}...\n")
    
    print("="*60)
    print(" TESTES CONCLUIDOS!")
    print("="*60)

# ============================================================================
# MODO INTERATIVO
# ============================================================================

def modo_interativo():
    """Modo interativo"""
    # [CÓDIGO DO E4]
    pass

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Função principal"""
    print("="*60)
    print(" AGENTE SINARM v5.0 - RAG ESPECIALIZADO")
    print("="*60)
    
    if len(sys.argv) == 1:
        executar_testes()
    elif sys.argv[1] == '--interativo':
        modo_interativo()
    else:
        pergunta = ' '.join(sys.argv[1:])
        resposta = processar_pergunta(pergunta)
        print(f"\n Resposta: {resposta}")

if __name__ == "__main__":
    main()
```

**Tempo estimado:** 2-3 horas

---

### 3. Material de Apoio (PRIORIDADE MÉDIA)

**Arquivos:**

**a) `04_MATERIAL_APOIO/FAQ_E5.md`**
- Perguntas frequentes
- Dúvidas comuns
- Soluções rápidas

**b) `04_MATERIAL_APOIO/TROUBLESHOOTING_E5.md`**
- Erros comuns
- Como resolver
- Logs e debug

**c) `04_MATERIAL_APOIO/COMPARACAO_E4_vs_E5.md`**
- Tabela comparativa
- Métricas
- Quando usar cada um

**d) `02_NOTEBOOK_PASSO_A_PASSO/README.md`**
- Como usar notebook
- Estrutura
- Checkpoints

**e) `03_AGENTE_CONSOLIDADO/README.md`**
- Como usar agente
- Modos de execução
- Exemplos

**Tempo estimado:** 1-2 horas

---

### 4. Dados de Exemplo (PRIORIDADE BAIXA)

**PDFs de exemplo:**
- Estatuto do Desarmamento (baixar)
- Manual PCDF (se disponível)
- Portaria exemplo (criar fictícia)

**Tempo estimado:** 1 hora

---

## 📊 RESUMO

### Já Criado (60%)
- ✅ Estrutura de pastas
- ✅ README.md principal
- ✅ 00_COMECE_AQUI_E5.md
- ✅ requirements.txt
- ✅ Notebook incremental (60-80 células) - **COMPLETO!**
- ✅ README.md do notebook

### Falta Criar (40%)
- ⏳ Agente consolidado (~600 linhas) - **2-3h**
- ⏳ Material de apoio (5 arquivos) - **1-2h**
- ⏳ Dados de exemplo (PDFs) - **1h**

**Tempo total estimado:** 4-6 horas (restantes)

---

## 🚀 PRÓXIMOS PASSOS

### Sessão Atual (Finalizar)
1. ✅ Criar este plano
2. ✅ Salvar progresso
3. ✅ Documentar o que falta
4. ✅ Criar notebook incremental (60-80 células)
5. ✅ Criar README.md do notebook

### Próxima Sessão
1. ⏳ Criar agente consolidado
2. ⏳ Criar material de apoio
3. ⏳ Testar tudo
4. ⏳ Validar funcionamento

---

**Status:** ⏳ 60% COMPLETO

**Próxima etapa:** Criar notebook incremental E5
