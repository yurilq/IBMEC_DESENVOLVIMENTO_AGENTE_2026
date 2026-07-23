"""
RAG (Retrieval-Augmented Generation) 100% LOCAL
Usa TF-IDF + Similaridade Coseno (SEM PyTorch, SEM APIs)

Autor: Professor IBMEC
Data: 23/07/2026
Versão: 1.0 - TF-IDF Local
"""

import json
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RAGLocal:
    """
    RAG usando TF-IDF para busca semântica local
    
    Vantagens:
    - 100% local (sem APIs, sem custos)
    - Sem PyTorch (sem erros de DLL)
    - Apenas scikit-learn (já instalado)
    - Rápido para bases pequenas (<10k docs)
    
    Limitações:
    - Menos preciso que embeddings neurais
    - Não captura sinônimos complexos
    - Sensível a vocabulário exato
    """
    
    def __init__(self, docs_path: str):
        """
        Inicializa RAG carregando documentos e criando índice TF-IDF
        
        Args:
            docs_path: Caminho para arquivo JSON com documentos
        """
        print(f"[RAG-LOCAL] Inicializando RAG com TF-IDF...")
        
        # Carregar documentos
        with open(docs_path, 'r', encoding='utf-8') as f:
            self.documentos = json.load(f)
        
        print(f"[RAG-LOCAL] {len(self.documentos)} documentos carregados")
        
        # Extrair textos
        self.textos = [doc['texto'] for doc in self.documentos]
        
        # Criar vetorizador TF-IDF
        # max_features: limitar vocabulário (reduz memória)
        # ngram_range: uni-gramas e bi-gramas (captura "calibre arma", não só "calibre")
        # min_df: ignorar palavras muito raras (aparecem em <2 docs)
        # stop_words: remover palavras vazias do português
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            min_df=1,
            stop_words=self._stopwords_pt()
        )
        
        # Criar índice TF-IDF
        print(f"[RAG-LOCAL] Criando índice TF-IDF...")
        self.doc_vectors = self.vectorizer.fit_transform(self.textos)
        
        print(f"[RAG-LOCAL] Índice criado: {self.doc_vectors.shape[0]} docs, "
              f"{self.doc_vectors.shape[1]} features")
        print(f"[RAG-LOCAL] [INFO] RAG pronto para uso!")
    
    def _stopwords_pt(self):
        """Stopwords básicas do português"""
        return [
            'a', 'o', 'e', 'de', 'da', 'do', 'em', 'um', 'uma', 'os', 'as',
            'dos', 'das', 'ao', 'aos', 'à', 'às', 'pelo', 'pela', 'pelos',
            'pelas', 'no', 'na', 'nos', 'nas', 'por', 'para', 'com', 'sem',
            'sob', 'sobre', 'é', 'são', 'foi', 'será', 'ou', 'mas', 'se'
        ]
    
    def buscar(self, query: str, top_k: int = 3, threshold: float = 0.1):
        """
        Busca documentos similares à query usando TF-IDF + Cosine Similarity
        
        Args:
            query: Pergunta do usuário
            top_k: Número máximo de documentos a retornar
            threshold: Similaridade mínima (0.0 a 1.0)
        
        Returns:
            Lista de dicts com {id, categoria, texto, score}
        """
        # Vetorizar query
        query_vector = self.vectorizer.transform([query])
        
        # Calcular similaridade coseno com todos documentos
        similaridades = cosine_similarity(query_vector, self.doc_vectors)[0]
        
        # Criar lista de resultados
        resultados = []
        for idx, score in enumerate(similaridades):
            if score >= threshold:  # Filtrar por threshold
                resultados.append({
                    'id': self.documentos[idx]['id'],
                    'categoria': self.documentos[idx]['categoria'],
                    'texto': self.documentos[idx]['texto'],
                    'score': float(score)
                })
        
        # Ordenar por score (maior primeiro)
        resultados.sort(key=lambda x: x['score'], reverse=True)
        
        # Retornar top K
        return resultados[:top_k]
    
    def get_context(self, query: str, top_k: int = 3, threshold: float = 0.1):
        """
        Retorna contexto formatado para o LLM
        
        Args:
            query: Pergunta do usuário
            top_k: Número de documentos a recuperar
            threshold: Similaridade mínima
        
        Returns:
            String formatada com contexto ou mensagem de erro
        """
        resultados = self.buscar(query, top_k=top_k, threshold=threshold)
        
        # Se não encontrou nada relevante
        if not resultados:
            return "[INFO] Nenhum documento relevante encontrado (threshold não atingido)"
        
        # Formatar contexto para o LLM
        contexto = "DOCUMENTOS SINARM RELEVANTES:\n\n"
        
        for i, doc in enumerate(resultados, 1):
            contexto += f"[Documento {doc['id']}] (Relevância: {doc['score']:.2f})\n"
            contexto += f"Categoria: {doc['categoria']}\n"
            contexto += f"{doc['texto']}\n\n"
            contexto += "-" * 80 + "\n\n"
        
        return contexto
    
    def diagnostico(self, query: str, top_k: int = 5):
        """
        Modo diagnóstico: mostra detalhes da busca
        
        Args:
            query: Pergunta do usuário
            top_k: Quantos resultados mostrar
        """
        print(f"\n{'='*80}")
        print(f"DIAGNÓSTICO RAG - Query: '{query}'")
        print(f"{'='*80}\n")
        
        # Vetorizar query
        query_vector = self.vectorizer.transform([query])
        
        # Mostrar tokens da query
        feature_names = self.vectorizer.get_feature_names_out()
        query_tokens = query_vector.toarray()[0]
        tokens_ativos = [(feature_names[i], query_tokens[i]) 
                         for i in range(len(query_tokens)) if query_tokens[i] > 0]
        
        print(f"Tokens extraídos da query ({len(tokens_ativos)}):")
        for token, peso in sorted(tokens_ativos, key=lambda x: x[1], reverse=True)[:10]:
            print(f"  - '{token}': {peso:.3f}")
        
        # Calcular similaridades
        similaridades = cosine_similarity(query_vector, self.doc_vectors)[0]
        
        # Mostrar top K
        top_indices = np.argsort(similaridades)[-top_k:][::-1]
        
        print(f"\nTop {top_k} documentos mais similares:")
        for rank, idx in enumerate(top_indices, 1):
            doc = self.documentos[idx]
            score = similaridades[idx]
            print(f"\n{rank}. [Doc {doc['id']}] Score: {score:.3f}")
            print(f"   Categoria: {doc['categoria']}")
            print(f"   Texto: {doc['texto'][:100]}...")
        
        print(f"\n{'='*80}\n")


# ============================================================================
# INTERFACE COMPATÍVEL COM v4.5 (buscar_conhecimento_sinarm)
# ============================================================================

# Instância global (singleton)
_rag_instance = None


def buscar_conhecimento_sinarm(query: str) -> str:
    """
    Interface compatível com agente_v4_5_rag.py
    
    Esta função é chamada pelo agente quando precisa de conhecimento conceitual.
    Retorna contexto formatado para o LLM responder.
    
    Args:
        query: Pergunta do usuário
    
    Returns:
        Contexto formatado ou mensagem de erro
    """
    global _rag_instance
    
    # Lazy loading: criar instância apenas na primeira chamada
    if _rag_instance is None:
        # Path para documentos (subir um nível da pasta scripts_agente)
        docs_path = Path(__file__).parent.parent / "DADOS_SINARM" / "documentos_conceituais.json"
        
        try:
            _rag_instance = RAGLocal(str(docs_path))
        except FileNotFoundError:
            return "[INFO] ERRO: Arquivo documentos_conceituais.json não encontrado"
        except Exception as e:
            return f"[INFO] ERRO ao inicializar RAG: {str(e)}"
    
    # Buscar contexto
    try:
        contexto = _rag_instance.get_context(
            query=query,
            top_k=3,  # Top 3 documentos
            threshold=0.1  # Aceitar similaridade >= 10%
        )
        return contexto
    
    except Exception as e:
        return f"[INFO] ERRO ao buscar documentos: {str(e)}"


# ============================================================================
# TESTE RÁPIDO (executar: python tool_rag_tfidf.py)
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("TESTE RAG LOCAL (TF-IDF)")
    print("="*80 + "\n")
    
    # Caminho para documentos
    docs_path = Path(__file__).parent / "DADOS_SINARM" / "documentos_conceituais.json"
    
    # Criar RAG
    rag = RAGLocal(str(docs_path))
    
    # Testes
    perguntas = [
        "O que é arma apreendida?",
        "Explique o que é calibre",
        "Qual a diferença entre furto e roubo?",
        "Quais marcas de arma existem?",
        "O que é BO?"
    ]
    
    for pergunta in perguntas:
        print("\n" + "="*80)
        print(f"PERGUNTA: {pergunta}")
        print("="*80)
        
        # Buscar contexto
        contexto = rag.get_context(pergunta, top_k=2, threshold=0.1)
        
        print(contexto)
        print("\n")
    
    # Diagnóstico de uma pergunta
    rag.diagnostico("O que é calibre de arma?", top_k=5)
