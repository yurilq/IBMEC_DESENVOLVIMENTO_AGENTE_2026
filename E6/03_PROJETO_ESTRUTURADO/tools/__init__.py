"""
Ferramentas Reutilizáveis

Módulos auxiliares para:
- Processamento de PDFs
- Cálculo de métricas
- Funções utilitárias
"""

from .metrics import precision_at_k, mean_reciprocal_rank, ndcg_at_k
from .utils import formatar_resultado, salvar_resultados, carregar_resultados

__all__ = [
    "precision_at_k",
    "mean_reciprocal_rank",
    "ndcg_at_k",
    "formatar_resultado",
    "salvar_resultados",
    "carregar_resultados",
]
