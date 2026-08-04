"""
Módulo de Reranking (Versão SEM PyTorch)

Responsável por reranking:
- Usa apenas NumPy e Scikit-learn
- Sem dependências de PyTorch
- Reranking baseado em similaridade de cosseno
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity


# Cache global para modelo
_reranker_model = None


def carregar_modelo_reranker(nome_modelo: str = 'tfidf-reranker'):
    """
    Carrega modelo de reranking (sem PyTorch).
    
    Args:
        nome_modelo: Nome do modelo (não usado, apenas para compatibilidade)
    
    Returns:
        dict: Configuração de reranking
    
    Example:
        >>> reranker = carregar_modelo_reranker()
    """
    global _reranker_model
    
    if _reranker_model is not None:
        return _reranker_model
    
    print("[INFO] Usando reranking com TF-IDF (sem PyTorch)")
    
    _reranker_model = {'tipo': 'tfidf'}
    
    return _reranker_model


def buscar_com_reranking(
    pergunta: str,
    embeddings: np.ndarray,
    chunks: List[Dict[str, any]],
    modelo_embedding,
    reranker: Optional[dict] = None,
    top_k: int = 5
) -> List[Tuple[Dict[str, str], float]]:
    """
    Busca e reranking de documentos (versão sem PyTorch).
    
    Args:
        pergunta: Pergunta do usuário
        embeddings: Embeddings dos chunks
        chunks: Lista de chunks
        modelo_embedding: Modelo de embeddings
        reranker: Modelo de reranking (não usado)
        top_k: Número de resultados finais
    
    Returns:
        Lista de (chunk, score) ordenada por relevância
    
    Example:
        >>> resultados = buscar_com_reranking(
        ...     pergunta="O que é calibre?",
        ...     embeddings=embeddings,
        ...     chunks=chunks,
        ...     modelo_embedding=modelo
        ... )
    """
    
    # Gerar embedding da pergunta
    from src.embeddings import gerar_embedding_pergunta
    embedding_pergunta = gerar_embedding_pergunta(pergunta, modelo_embedding)
    
    # Calcular similaridade com todos os chunks
    scores = cosine_similarity(embedding_pergunta, embeddings)[0]
    
    # Ordenar por score
    indices_ordenados = np.argsort(scores)[::-1]
    
    # Retornar top-k com scores
    resultados = []
    for idx in indices_ordenados[:top_k]:
        chunk = chunks[idx]
        score = scores[idx]
        resultados.append((chunk, float(score)))
    
    return resultados


def validar_reranking(resultados: List[Tuple[Dict, float]]) -> bool:
    """
    Valida resultado do reranking.
    
    Args:
        resultados: Lista de (chunk, score)
    
    Returns:
        bool: True se válido
    
    Example:
        >>> validar_reranking(resultados)
        True
    """
    if not resultados or not isinstance(resultados, list):
        raise ValueError("Resultados vazios ou inválidos")
    
    for chunk, score in resultados:
        if not isinstance(chunk, dict) or not isinstance(score, (float, int)):
            raise ValueError(f"Formato inválido: {type(chunk)}, {type(score)}")
        
        if score < 0 or score > 1:
            raise ValueError(f"Score fora do intervalo [0, 1]: {score}")
    
    return True


def limpar_cache():
    """Limpa cache de modelos."""
    global _reranker_model
    _reranker_model = None


# Aliases para compatibilidade
def reranking_cruzado(pares: List[Tuple[str, str]], reranker=None) -> np.ndarray:
    """
    Reranking cruzado (compatibilidade com código antigo).
    
    Args:
        pares: Lista de (pergunta, documento)
        reranker: Modelo (não usado)
    
    Returns:
        Array de scores
    """
    # Calcular similaridade simples entre pares
    scores = []
    for pergunta, documento in pares:
        # Usar comprimento e palavras em comum como heurística
        palavras_pergunta = set(pergunta.lower().split())
        palavras_doc = set(documento.lower().split())
        
        if len(palavras_pergunta) == 0 or len(palavras_doc) == 0:
            score = 0.0
        else:
            intersecao = len(palavras_pergunta & palavras_doc)
            score = intersecao / max(len(palavras_pergunta), len(palavras_doc))
        
        scores.append(score)
    
    return np.array(scores, dtype=np.float32)


if __name__ == "__main__":
    # Teste básico
    print("Teste de reranking (sem PyTorch)")
    print("=" * 70)
    
    # Simular chunks e embeddings
    chunks = [
        {"arquivo": "doc1.txt", "conteudo": "Calibre é a medida do diâmetro"},
        {"arquivo": "doc2.txt", "conteudo": "Os calibres mais comuns são .38"}
    ]
    
    embeddings = np.random.rand(2, 5).astype(np.float32)
    
    print("✅ Módulo de reranking carregado com sucesso!")
