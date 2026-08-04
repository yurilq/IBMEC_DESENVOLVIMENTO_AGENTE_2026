"""
Módulo de Busca Vetorial

Responsável por busca com NumPy (SEM FAISS):
- Busca com cosine similarity
- Top-K configurável
- Rápido para datasets pequenos/médios (<100K docs)

Por que NumPy em vez de FAISS?
- FAISS: Extremamente rápido (milhões de vetores)
  Requer PyTorch (problema de DLL no Windows)
- NumPy: Rápido para datasets pequenos/médios
  Funciona 100% no Windows (sem PyTorch)
  Mesma precisão que FAISS
  Mais simples de entender
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from sklearn.metrics.pairwise import cosine_similarity


def buscar_numpy(
    query_embedding: np.ndarray,
    embeddings: np.ndarray,
    chunks: Optional[List[Dict[str, any]]] = None,
    modelo_embedding = None,
    k: int = 5
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Busca documentos similares usando NumPy + cosine similarity.
    
    Compatível com TF-IDF (sem PyTorch).
    
    Args:
        query_embedding: Array com embedding da pergunta (1 x D)
        embeddings: Array de embeddings (N x D)
        chunks: (Opcional) Lista de chunks para retornar também
        modelo_embedding: (Não usado, para compatibilidade)
        k: Número de documentos a retornar
    
    Returns:
        tuple: (indices, scores) - Arrays NumPy
        ou list: [(chunk, score), ...] se chunks for fornecido
    
    Example:
        >>> indices, scores = buscar_numpy(query_embedding, embeddings, k=5)
        >>> for idx, score in zip(indices, scores):
        ...     print(f"Índice {idx}: {score:.3f}")
    """
    # Calcular similaridade com todos os documentos
    similaridades = cosine_similarity(query_embedding, embeddings)[0]
    
    # Pegar top-K (indices com maior similaridade)
    top_indices = np.argsort(similaridades)[-k:][::-1]
    top_scores = similaridades[top_indices]
    
    # Se chunks foi fornecido, retornar tuplas (chunk, score)
    if chunks is not None:
        resultados = []
        for idx in top_indices:
            if idx < len(chunks):
                chunk = chunks[idx]
                score = float(similaridades[idx])
                resultados.append((chunk, score))
        return resultados
    
    # Caso contrário, retornar (indices, scores)
    return np.array([top_indices]), np.array(top_scores)


def buscar_com_filtro(
    pergunta: str,
    embeddings: np.ndarray,
    chunks: List[Dict[str, any]],
    modelo_embedding,
    k: int = 5,
    threshold: float = 0.0,
    tipo_filtro: Optional[str] = None
) -> List[Tuple[Dict[str, any], float]]:
    """
    Busca com filtros adicionais.
    
    Args:
        pergunta: Pergunta do usuário
        embeddings: Array de embeddings
        chunks: Lista de chunks
        modelo_embedding: Modelo Sentence-BERT
        k: Número de documentos a retornar
        threshold: Score mínimo
        tipo_filtro: Filtrar por tipo ('txt' ou 'pdf')
    
    Returns:
        list: [(chunk, score), ...]
    
    Example:
        >>> resultados = buscar_com_filtro(
        ...     "O que é calibre?",
        ...     embeddings,
        ...     chunks,
        ...     modelo,
        ...     k=5,
        ...     tipo_filtro='pdf'
        ... )
    """
    # Gerar embedding da pergunta
    query_embedding = modelo_embedding.encode([pergunta])
    
    # Calcular similaridade
    similaridades = cosine_similarity(query_embedding, embeddings)[0]
    
    # Aplicar filtro de tipo se fornecido
    if tipo_filtro:
        indices_filtrados = [
            i for i, chunk in enumerate(chunks)
            if chunk['tipo'] == tipo_filtro
        ]
        similaridades_filtradas = similaridades[indices_filtrados]
        indices_ordenados = np.argsort(similaridades_filtradas)[::-1]
        top_indices = [indices_filtrados[i] for i in indices_ordenados[:k]]
    else:
        top_indices = similaridades.argsort()[-k:][::-1]
    
    # Retornar resultados com threshold
    resultados = []
    for idx in top_indices:
        if idx < len(chunks):
            score = float(similaridades[idx])
            
            # Aplicar threshold
            if score < threshold:
                continue
            
            chunk = chunks[idx]
            resultados.append((chunk, score))
            
            if len(resultados) >= k:
                break
    
    return resultados


def buscar_multiplas_perguntas(
    perguntas: List[str],
    embeddings: np.ndarray,
    chunks: List[Dict[str, any]],
    modelo_embedding,
    k: int = 5
) -> Dict[str, List[Tuple[Dict[str, any], float]]]:
    """
    Busca para múltiplas perguntas.
    
    Args:
        perguntas: Lista de perguntas
        embeddings: Array de embeddings
        chunks: Lista de chunks
        modelo_embedding: Modelo Sentence-BERT
        k: Número de documentos por pergunta
    
    Returns:
        dict: {pergunta: [(chunk, score), ...]}
    
    Example:
        >>> perguntas = ["O que é calibre?", "Diferença entre pistola e revolver?"]
        >>> resultados = buscar_multiplas_perguntas(
        ...     perguntas,
        ...     embeddings,
        ...     chunks,
        ...     modelo,
        ...     k=5
        ... )
    """
    resultados = {}
    
    for pergunta in perguntas:
        resultados[pergunta] = buscar_numpy(
            pergunta,
            embeddings,
            chunks,
            modelo_embedding,
            k=k
        )
    
    return resultados


def validar_busca(
    resultados: List[Tuple[Dict[str, any], float]],
    threshold_minimo: float = 0.3
) -> Dict[str, any]:
    """
    Valida qualidade dos resultados de busca.
    
    Args:
        resultados: Resultados da busca
        threshold_minimo: Score mínimo esperado
    
    Returns:
        dict: Estatísticas de validação
    
    Example:
        >>> stats = validar_busca(resultados)
        >>> print(f"Score médio: {stats['score_medio']:.3f}")
    """
    if not resultados:
        return {
            'total': 0,
            'score_medio': 0,
            'score_minimo': 0,
            'score_maximo': 0,
            'abaixo_threshold': 0
        }
    
    scores = [score for _, score in resultados]
    
    return {
        'total': len(resultados),
        'score_medio': np.mean(scores),
        'score_minimo': min(scores),
        'score_maximo': max(scores),
        'abaixo_threshold': sum(1 for s in scores if s < threshold_minimo)
    }
