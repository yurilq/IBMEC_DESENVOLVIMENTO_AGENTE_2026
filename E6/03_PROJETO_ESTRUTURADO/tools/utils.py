"""
Funções Utilitárias

Funções auxiliares para:
- Formatação de resultados
- Salvamento/carregamento de dados
- Logging
"""

import json
import os
from typing import List, Tuple, Dict, Any
from datetime import datetime


def formatar_resultado(
    chunk: Dict[str, Any],
    score: float,
    max_chars: int = 200
) -> str:
    """
    Formata um resultado de busca para exibição.
    
    Args:
        chunk: Chunk do documento
        score: Score de relevância
        max_chars: Máximo de caracteres do preview
    
    Returns:
        str: Resultado formatado
    
    Example:
        >>> resultado = formatar_resultado(chunk, 0.85)
        >>> print(resultado)
    """
    tipo_emoji = "📄" if chunk['tipo'] == "pdf" else "📝"
    score_emoji = "✅" if score > 0.5 else ("⚠️" if score > 0.3 else "❌")
    
    preview = chunk['texto'][:max_chars].replace('\n', ' ')
    
    return f"{tipo_emoji} {chunk['arquivo']} (score: {score:.3f}) {score_emoji}\n   {preview}..."


def salvar_resultados(
    resultados: List[Tuple[Dict[str, Any], float]],
    caminho: str,
    pergunta: str = "",
    metadados: Dict[str, Any] = None
) -> None:
    """
    Salva resultados de busca em arquivo JSON.
    
    Args:
        resultados: Resultados da busca
        caminho: Caminho do arquivo
        pergunta: Pergunta original
        metadados: Metadados adicionais
    
    Example:
        >>> salvar_resultados(resultados, "resultados.json", "O que é calibre?")
    """
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    
    dados = {
        'timestamp': datetime.now().isoformat(),
        'pergunta': pergunta,
        'total_resultados': len(resultados),
        'resultados': [
            {
                'arquivo': chunk['arquivo'],
                'tipo': chunk['tipo'],
                'score': float(score),
                'preview': chunk['texto'][:200]
            }
            for chunk, score in resultados
        ],
        'metadados': metadados or {}
    }
    
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Resultados salvos em: {caminho}")


def carregar_resultados(caminho: str) -> Dict[str, Any]:
    """
    Carrega resultados de busca de arquivo JSON.
    
    Args:
        caminho: Caminho do arquivo
    
    Returns:
        dict: Dados carregados
    
    Example:
        >>> dados = carregar_resultados("resultados.json")
        >>> print(f"Pergunta: {dados['pergunta']}")
    """
    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print(f"✅ Resultados carregados: {dados['total_resultados']} itens")
    return dados


def exibir_resultados(
    resultados: List[Tuple[Dict[str, Any], float]],
    titulo: str = "Resultados da Busca",
    max_resultados: int = 5
) -> None:
    """
    Exibe resultados de forma formatada.
    
    Args:
        resultados: Resultados da busca
        titulo: Título da exibição
        max_resultados: Máximo de resultados a exibir
    
    Example:
        >>> exibir_resultados(resultados, "Busca: O que é calibre?")
    """
    print(f"\n{titulo}")
    print("=" * 60)
    
    if not resultados:
        print("⚠️ Nenhum resultado encontrado")
        return
    
    for i, (chunk, score) in enumerate(resultados[:max_resultados], 1):
        print(f"\n{i}. {formatar_resultado(chunk, score)}")
    
    print("\n" + "=" * 60)


def comparar_resultados(
    resultados1: List[Tuple[Dict[str, Any], float]],
    resultados2: List[Tuple[Dict[str, Any], float]],
    titulo1: str = "Método 1",
    titulo2: str = "Método 2"
) -> None:
    """
    Compara dois conjuntos de resultados lado a lado.
    
    Args:
        resultados1: Primeiro conjunto de resultados
        resultados2: Segundo conjunto de resultados
        titulo1: Título do primeiro método
        titulo2: Título do segundo método
    
    Example:
        >>> comparar_resultados(busca_simples, busca_reranking, "Simples", "Reranking")
    """
    print(f"\n{'COMPARAÇÃO DE RESULTADOS':^60}")
    print("=" * 60)
    
    max_len = max(len(resultados1), len(resultados2))
    
    for i in range(max_len):
        print(f"\n--- Posição {i+1} ---")
        
        if i < len(resultados1):
            chunk1, score1 = resultados1[i]
            print(f"{titulo1}: {chunk1['arquivo']} ({score1:.3f})")
        else:
            print(f"{titulo1}: N/A")
        
        if i < len(resultados2):
            chunk2, score2 = resultados2[i]
            print(f"{titulo2}: {chunk2['arquivo']} ({score2:.3f})")
        else:
            print(f"{titulo2}: N/A")
    
    print("\n" + "=" * 60)


def gerar_relatorio(
    pergunta: str,
    resultados: List[Tuple[Dict[str, Any], float]],
    metricas: Dict[str, float] = None,
    caminho_saida: str = None
) -> str:
    """
    Gera relatório completo de busca.
    
    Args:
        pergunta: Pergunta original
        resultados: Resultados da busca
        metricas: Métricas de avaliação
        caminho_saida: Caminho para salvar relatório
    
    Returns:
        str: Relatório formatado
    
    Example:
        >>> relatorio = gerar_relatorio(pergunta, resultados, metricas)
        >>> print(relatorio)
    """
    relatorio = f"""
{'='*60}
RELATÓRIO DE BUSCA
{'='*60}

Pergunta: {pergunta}
Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total de Resultados: {len(resultados)}

{'RESULTADOS':^60}
{'-'*60}
"""
    
    for i, (chunk, score) in enumerate(resultados, 1):
        relatorio += f"\n{i}. {chunk['arquivo']} (score: {score:.3f})\n"
        relatorio += f"   Tipo: {chunk['tipo']}\n"
        relatorio += f"   Preview: {chunk['texto'][:100]}...\n"
    
    if metricas:
        relatorio += f"\n{'MÉTRICAS':^60}\n"
        relatorio += f"{'-'*60}\n"
        for metrica, valor in metricas.items():
            relatorio += f"{metrica}: {valor:.3f}\n"
    
    relatorio += f"\n{'='*60}\n"
    
    if caminho_saida:
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            f.write(relatorio)
        print(f"✅ Relatório salvo em: {caminho_saida}")
    
    return relatorio
