"""
Métricas de Avaliação

Funções para avaliar qualidade de busca:
- Precision@K
- Mean Reciprocal Rank (MRR)
- NDCG@K
"""

import numpy as np
from typing import List, Tuple, Dict


def precision_at_k(
    resultados: List[Tuple[Dict, float]],
    relevantes_ids: List[str],
    k: int = 5
) -> float:
    """
    Calcula Precision@K.
    
    Precision@K = (# documentos relevantes nos top-K) / K
    
    Args:
        resultados: Resultados da busca [(chunk, score), ...]
        relevantes_ids: IDs dos documentos relevantes
        k: Número de top resultados
    
    Returns:
        float: Precision@K (0-1)
    
    Example:
        >>> p5 = precision_at_k(resultados, ['doc1', 'doc2'], k=5)
        >>> print(f"Precision@5: {p5:.2%}")
    """
    top_k = resultados[:k]
    
    relevantes_encontrados = 0
    for chunk, _ in top_k:
        if chunk.get('arquivo') in relevantes_ids:
            relevantes_encontrados += 1
    
    return relevantes_encontrados / k if k > 0 else 0.0


def mean_reciprocal_rank(
    resultados: List[Tuple[Dict, float]],
    relevantes_ids: List[str]
) -> float:
    """
    Calcula Mean Reciprocal Rank (MRR).
    
    MRR = 1 / (posição do primeiro documento relevante)
    
    Args:
        resultados: Resultados da busca
        relevantes_ids: IDs dos documentos relevantes
    
    Returns:
        float: MRR (0-1)
    
    Example:
        >>> mrr = mean_reciprocal_rank(resultados, ['doc1', 'doc2'])
        >>> print(f"MRR: {mrr:.3f}")
    """
    for i, (chunk, _) in enumerate(resultados, 1):
        if chunk.get('arquivo') in relevantes_ids:
            return 1.0 / i
    
    return 0.0


def ndcg_at_k(
    resultados: List[Tuple[Dict, float]],
    relevantes_scores: Dict[str, float],
    k: int = 5
) -> float:
    """
    Calcula NDCG@K (Normalized Discounted Cumulative Gain).
    
    Leva em conta a posição e o grau de relevância.
    
    Args:
        resultados: Resultados da busca
        relevantes_scores: {arquivo: score_relevancia}
        k: Número de top resultados
    
    Returns:
        float: NDCG@K (0-1)
    
    Example:
        >>> relevantes = {'doc1': 1.0, 'doc2': 0.8}
        >>> ndcg = ndcg_at_k(resultados, relevantes, k=5)
        >>> print(f"NDCG@5: {ndcg:.3f}")
    """
    # Calcular DCG
    dcg = 0.0
    for i, (chunk, _) in enumerate(resultados[:k], 1):
        arquivo = chunk.get('arquivo')
        relevancia = relevantes_scores.get(arquivo, 0.0)
        dcg += relevancia / np.log2(i + 1)
    
    # Calcular IDCG (ideal DCG)
    relevancia_ideal = sorted(relevantes_scores.values(), reverse=True)[:k]
    idcg = 0.0
    for i, relevancia in enumerate(relevancia_ideal, 1):
        idcg += relevancia / np.log2(i + 1)
    
    # NDCG = DCG / IDCG
    return dcg / idcg if idcg > 0 else 0.0


def recall_at_k(
    resultados: List[Tuple[Dict, float]],
    relevantes_ids: List[str],
    k: int = 5
) -> float:
    """
    Calcula Recall@K.
    
    Recall@K = (# documentos relevantes nos top-K) / (total de relevantes)
    
    Args:
        resultados: Resultados da busca
        relevantes_ids: IDs dos documentos relevantes
        k: Número de top resultados
    
    Returns:
        float: Recall@K (0-1)
    
    Example:
        >>> r5 = recall_at_k(resultados, ['doc1', 'doc2'], k=5)
        >>> print(f"Recall@5: {r5:.2%}")
    """
    top_k = resultados[:k]
    
    relevantes_encontrados = 0
    for chunk, _ in top_k:
        if chunk.get('arquivo') in relevantes_ids:
            relevantes_encontrados += 1
    
    total_relevantes = len(relevantes_ids)
    return relevantes_encontrados / total_relevantes if total_relevantes > 0 else 0.0


def f1_score_at_k(
    resultados: List[Tuple[Dict, float]],
    relevantes_ids: List[str],
    k: int = 5
) -> float:
    """
    Calcula F1-Score@K.
    
    F1 = 2 * (Precision * Recall) / (Precision + Recall)
    
    Args:
        resultados: Resultados da busca
        relevantes_ids: IDs dos documentos relevantes
        k: Número de top resultados
    
    Returns:
        float: F1-Score@K (0-1)
    
    Example:
        >>> f1 = f1_score_at_k(resultados, ['doc1', 'doc2'], k=5)
        >>> print(f"F1@5: {f1:.3f}")
    """
    precision = precision_at_k(resultados, relevantes_ids, k)
    recall = recall_at_k(resultados, relevantes_ids, k)
    
    if precision + recall == 0:
        return 0.0
    
    return 2 * (precision * recall) / (precision + recall)


def avaliar_completo(
    resultados: List[Tuple[Dict, float]],
    relevantes_ids: List[str],
    relevantes_scores: Dict[str, float] = None,
    k: int = 5
) -> Dict[str, float]:
    """
    Avaliação completa com múltiplas métricas.
    
    Args:
        resultados: Resultados da busca
        relevantes_ids: IDs dos documentos relevantes
        relevantes_scores: Scores de relevância (opcional)
        k: Número de top resultados
    
    Returns:
        dict: Todas as métricas
    
    Example:
        >>> metricas = avaliar_completo(resultados, ['doc1', 'doc2'])
        >>> for metrica, valor in metricas.items():
        ...     print(f"{metrica}: {valor:.3f}")
    """
    if relevantes_scores is None:
        relevantes_scores = {doc_id: 1.0 for doc_id in relevantes_ids}
    
    return {
        'precision_at_k': precision_at_k(resultados, relevantes_ids, k),
        'recall_at_k': recall_at_k(resultados, relevantes_ids, k),
        'f1_score_at_k': f1_score_at_k(resultados, relevantes_ids, k),
        'mrr': mean_reciprocal_rank(resultados, relevantes_ids),
        'ndcg_at_k': ndcg_at_k(resultados, relevantes_scores, k),
    }
