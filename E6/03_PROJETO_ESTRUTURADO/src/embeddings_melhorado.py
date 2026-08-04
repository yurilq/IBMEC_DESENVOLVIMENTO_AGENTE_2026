"""
EMBEDDINGS_MELHORADO.PY - Sentence-BERT sem PyTorch

Usa ONNX Runtime em vez de PyTorch para executar Sentence-BERT.
Melhor qualidade de embeddings que TF-IDF.
"""

import numpy as np
from typing import List, Optional
import os

_embedding_model = None
_use_onnx = False

def carregar_modelo_embedding(nome_modelo: str = 'sentence-transformers'):
    """
    Carrega modelo de embeddings.
    
    Tenta:
    1. ONNX Runtime (melhor, sem PyTorch)
    2. Sentence-BERT com PyTorch (fallback)
    3. TF-IDF (fallback final)
    """
    global _embedding_model, _use_onnx
    
    if _embedding_model is not None:
        return _embedding_model
    
    # Tentar ONNX Runtime primeiro
    try:
        import onnxruntime as ort
        print("[INFO] Tentando usar ONNX Runtime (melhor qualidade, sem PyTorch)")
        
        # Modelo ONNX pré-treinado em português
        model_name = "sentence-transformers/distiluse-base-multilingual-cased-v2"
        
        try:
            from huggingface_hub import hf_hub_download
            
            # Download do modelo ONNX
            print("[INFO] Baixando modelo ONNX (primeira vez, ~100MB)...")
            model_path = hf_hub_download(
                repo_id="onnx-community/distiluse-base-multilingual-cased-v2",
                filename="model.onnx"
            )
            
            session = ort.InferenceSession(model_path)
            _embedding_model = {
                'type': 'onnx',
                'session': session,
                'dimension': 512
            }
            _use_onnx = True
            print("[INFO] ONNX carregado com sucesso!")
            return _embedding_model
            
        except:
            print("[INFO] ONNX não disponível, tentando Sentence-BERT...")
    
    except ImportError:
        print("[INFO] ONNX Runtime não instalado")
    
    # Fallback: Sentence-BERT
    try:
        print("[INFO] Tentando usar Sentence-BERT")
        from sentence_transformers import SentenceTransformer
        
        # Modelo multilíngue compacto
        model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
        
        _embedding_model = {
            'type': 'sentence-bert',
            'model': model,
            'dimension': 512
        }
        print("[INFO] Sentence-BERT carregado com sucesso!")
        return _embedding_model
        
    except ImportError:
        print("[AVISO] Sentence-BERT não instalado")
    
    # Fallback final: TF-IDF
    print("[INFO] Usando TF-IDF (fallback - qualidade menor)")
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    _embedding_model = {
        'type': 'tfidf',
        'model': TfidfVectorizer(max_features=384, stop_words='english'),
        'dimension': 384
    }
    
    return _embedding_model


def gerar_embeddings(textos: List[str], modelo=None):
    """Gera embeddings com qualidade automática"""
    if modelo is None:
        modelo = carregar_modelo_embedding()
    
    tipo = modelo.get('type')
    
    if tipo == 'onnx':
        # ONNX Runtime
        embeddings = []
        for texto in textos:
            # Tokenizar e processar
            inputs = _tokenize_for_onnx(texto, modelo)
            outputs = modelo['session'].run(None, inputs)
            embeddings.append(outputs[0][0])  # Pooled output
        embeddings = np.array(embeddings, dtype=np.float32)
    
    elif tipo == 'sentence-bert':
        # Sentence-BERT
        embeddings = modelo['model'].encode(textos, convert_to_numpy=True)
        embeddings = embeddings.astype(np.float32)
    
    else:
        # TF-IDF
        embeddings = modelo['model'].fit_transform(textos).toarray()
        embeddings = embeddings.astype(np.float32)
    
    return embeddings


def gerar_embedding_pergunta(pergunta: str, modelo=None):
    """Gera embedding para pergunta"""
    if modelo is None:
        modelo = carregar_modelo_embedding()
    
    tipo = modelo.get('type')
    
    if tipo == 'onnx':
        inputs = _tokenize_for_onnx(pergunta, modelo)
        outputs = modelo['session'].run(None, inputs)
        embedding = outputs[0][0:1]
    
    elif tipo == 'sentence-bert':
        embedding = modelo['model'].encode([pergunta], convert_to_numpy=True)
    
    else:
        embedding = modelo['model'].transform([pergunta]).toarray()
    
    return embedding.astype(np.float32)


def _tokenize_for_onnx(texto: str, modelo):
    """Tokeniza texto para ONNX Runtime"""
    try:
        from transformers import AutoTokenizer
        
        tokenizer = AutoTokenizer.from_pretrained(
            "distiluse-base-multilingual-cased-v2"
        )
        
        encoded = tokenizer(
            texto,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='np'
        )
        
        return {
            'input_ids': encoded['input_ids'],
            'attention_mask': encoded['attention_mask'],
            'token_type_ids': encoded.get('token_type_ids', 
                                         np.zeros_like(encoded['input_ids']))
        }
    except:
        # Fallback manual se tokenizer não disponível
        return {}


def get_modelo_info(modelo):
    """Retorna informações sobre o modelo"""
    tipo = modelo.get('type')
    dim = modelo.get('dimension', 0)
    
    if tipo == 'onnx':
        return f"ONNX Runtime ({dim}D) - Melhor qualidade"
    elif tipo == 'sentence-bert':
        return f"Sentence-BERT ({dim}D) - Boa qualidade"
    else:
        return f"TF-IDF ({dim}D) - Qualidade básica"


# Manter compatibilidade com versão anterior
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
    global _embedding_model
    _embedding_model = None
