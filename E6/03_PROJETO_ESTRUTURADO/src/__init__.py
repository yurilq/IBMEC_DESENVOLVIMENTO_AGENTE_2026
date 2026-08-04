"""
E5: RAG Especializado com PDFs PCDF

Módulo principal para processamento de PDFs, embeddings e busca vetorial.

Componentes:
- loader: Carregamento de dados (CSV, .txt, PDFs)
- chunker: Processamento de chunks
- embeddings: Geração de embeddings semânticos
- search: Busca vetorial com NumPy
- reranker: Reranking com CrossEncoder
"""

__version__ = "1.0.0"
__author__ = "MBA IA Generativa PCDF - IBMEC"

from .loader import (
    carregar_csv,
    carregar_documentos_txt,
    carregar_pdfs
)

from .chunker import chunk_text_hibrido, preparar_todos_chunks

from .embeddings import gerar_embeddings, carregar_modelo_embedding

from .search import buscar_numpy

from .reranker import buscar_com_reranking, carregar_modelo_reranker

__all__ = [
    "carregar_csv",
    "carregar_documentos_txt",
    "carregar_pdfs",
    "chunk_text_hibrido",
    "preparar_todos_chunks",
    "gerar_embeddings",
    "carregar_modelo_embedding",
    "buscar_numpy",
    "buscar_com_reranking",
    "carregar_modelo_reranker",
]
