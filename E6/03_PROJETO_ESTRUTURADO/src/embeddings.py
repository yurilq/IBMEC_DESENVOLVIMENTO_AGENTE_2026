"""
EMBEDDINGS.PY - Embeddings com Sentence-BERT ou TF-IDF

Tenta usar Sentence-BERT primeiro (melhor qualidade),
com fallback para TF-IDF (compatibilidade).
"""

import numpy as np
from typing import List, Optional

_embedding_model = None
_model_type = None

def carregar_modelo_embedding(nome_modelo: str = 'auto'):
    """
    Carrega modelo de embeddings automaticamente.
    
    Tenta:
    1. Sentence-BERT (melhor qualidade semântica)
    2. TF-IDF (fallback rápido)
    """
    global _embedding_model, _model_type
    
    if _embedding_model is not None:
        return _embedding_model
    
    # Tentar Sentence-BERT primeiro
    try:
        from sentence_transformers import SentenceTransformer
        print("[INFO] Usando Sentence-BERT (embeddings semânticos)")
        _embedding_model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
        _model_type = 'sentence-bert'
        return _embedding_model
    except ImportError:
        print("[INFO] Sentence-BERT não instalado")
    except Exception as e:
        print("[AVISO] Erro ao carregar Sentence-BERT: {}".format(str(e)[:50]))
    
    # Fallback: TF-IDF
    print("[INFO] Usando TF-IDF (sem Sentence-BERT)")
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    _embedding_model = TfidfVectorizer(max_features=384, stop_words='english')
    _model_type = 'tfidf'
    return _embedding_model


def gerar_embeddings(textos: List[str], modelo=None):
    """
    Gera embeddings com o modelo disponível.
    
    Args:
        textos: Lista de textos
        modelo: Modelo carregado (ou None para carregar automaticamente)
    
    Returns:
        Array NumPy com embeddings (N x D)
    """
    global _model_type
    
    if modelo is None:
        modelo = carregar_modelo_embedding()
    
    # Sentence-BERT
    if _model_type == 'sentence-bert' or hasattr(modelo, 'encode'):
        embeddings = modelo.encode(textos, convert_to_numpy=True)
        return embeddings.astype(np.float32)
    
    # TF-IDF
    else:
        embeddings = modelo.fit_transform(textos).toarray()
        return embeddings.astype(np.float32)


def gerar_embedding_pergunta(pergunta: str, modelo=None):
    """
    Gera embedding para uma pergunta.
    
    Args:
        pergunta: Texto da pergunta
        modelo: Modelo carregado (ou None para carregar automaticamente)
    
    Returns:
        Array NumPy com embedding (1 x D)
    """
    global _model_type
    
    if modelo is None:
        modelo = carregar_modelo_embedding()
    
    # Sentence-BERT
    if _model_type == 'sentence-bert' or hasattr(modelo, 'encode'):
        embedding = modelo.encode([pergunta], convert_to_numpy=True)
        return embedding.astype(np.float32)
    
    # TF-IDF
    else:
        embedding = modelo.transform([pergunta]).toarray()
        return embedding.astype(np.float32)


def validar_embeddings(embeddings: np.ndarray):
    """Valida embeddings"""
    if embeddings is None or len(embeddings) == 0:
        raise ValueError("Embeddings vazios")
    
    if embeddings.dtype != np.float32:
        raise ValueError(f"Tipo incorreto: {embeddings.dtype}")
    
    return True


def salvar_embeddings(embeddings: np.ndarray, caminho: str):
    """Salva embeddings"""
    np.save(caminho, embeddings)


def carregar_embeddings(caminho: str):
    """Carrega embeddings"""
    return np.load(caminho)


def limpar_cache():
    """Limpa cache"""
    global _embedding_model, _model_type
    _embedding_model = None
    _model_type = None


def get_model_info():
    """Retorna informações sobre o modelo carregado"""
    global _model_type
    if _model_type == 'sentence-bert':
        return "Sentence-BERT (512D, semântico, melhor qualidade)"
    else:
        return "TF-IDF (384D, rápido, qualidade básica)"

