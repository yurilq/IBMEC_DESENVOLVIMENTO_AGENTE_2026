"""
ATIVIDADE 1A: MEDIR BASELINE (Zero-Shot)
Encontro 2 - Conceito: Few-Shot Learning
Duração: 20 minutos

OBJETIVO:
Medir a performance ATUAL do agente v1.8 (Zero-Shot) para estabelecer
baseline de comparação antes de adicionar Few-Shot.

O QUE VOCÊ VAI FAZER:
1. Executar 5 queries teste no agente v1.8
2. Avaliar qualidade das respostas (accuracy)
3. Medir tempo de resposta (latência)
4. Preencher tabela de resultados

POR QUE ISSO É IMPORTANTE:
- Estabelecer linha de base (baseline) para comparação
- Identificar queries que agente Zero-Shot erra ou demora
- Justificar necessidade de Few-Shot com DADOS

CONCEITO: Zero-Shot vs Few-Shot
- Zero-Shot: LLM responde SEM exemplos prévios (só instruções genéricas)
- Few-Shot: LLM recebe 2-5 exemplos ANTES de responder
- Expectativa: Few-Shot melhora accuracy em 15-30%
"""

import sys
from pathlib import Path

# Ajustar path para importar utils
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from utils.tools_sinarm import buscar_ocorrencias, buscar_portes, buscar_registros, buscar_requerimentos
import time
import json

# ========== QUERIES DE TESTE ==========

QUERIES_TESTE = [
    {
        "id": 1,
        "query": "Quantas ocorrências de furto de armas Taurus aconteceram no DF?",
        "resposta_esperada": "Número específico de ocorrências",
        "dataset_correto": "ocorrencias",
        "campos_necessarios": ["marca:Taurus", "tipo:Furto", "uf:DF"]
    },
    {
        "id": 2,
        "query": "Quais marcas de arma têm mais portes válidos atualmente?",
        "resposta_esperada": "Lista de marcas com contagem",
        "dataset_correto": "portes",
        "campos_necessarios": ["status:Válido"]
    },
    {
        "id": 3,
        "query": "Quantos registros de pistola calibre 9mm existem?",
        "resposta_esperada": "Número específico",
        "dataset_correto": "registros",
        "campos_necessarios": ["especie:Pistola", "calibre:9mm"]
    },
    {
        "id": 4,
        "query": "Qual a taxa de aprovação de requerimentos de porte no DF?",
        "resposta_esperada": "Percentual (aprovados / total)",
        "dataset_correto": "requerimentos",
        "campos_necessarios": ["decisao:Aprovado", "uf:DF"]
    },
    {
        "id": 5,
        "query": "Quais municípios do DF tiveram mais recuperações de armas em 2026?",
        "resposta_esperada": "Ranking de municípios",
        "dataset_correto": "ocorrencias",
        "campos_necessarios": ["tipo:Recuperação", "uf:DF", "ano:2026"]
    }
]

# ========== FUNÇÃO DE TESTE ==========

def testar_query_baseline(query_info):
    """
    Testa uma query no modo Zero-Shot (sem Few-Shot).
    
    Avalia:
    - Tempo de resposta
    - Acerto/erro
    - Qualidade da resposta
    """
    
    print(f"\n{'='*60}")
    print(f"TESTE {query_info['id']}: {query_info['query']}")
    print(f"{'='*60}")
    
    print(f"\n🎯 Resposta esperada: {query_info['resposta_esperada']}")
    print(f"📊 Dataset correto: {query_info['dataset_correto']}")
    print(f"🔍 Campos necessários: {', '.join(query_info['campos_necessarios'])}")
    
    # Simular chamada ao agente v1.8 (por enquanto manual)
    print("\n⏳ Executando query no agente v1.8 (Zero-Shot)...")
    print("   [SIMULAÇÃO - Na aula real, você rodaria o agente v1.8 aqui]")
    
    inicio = time.time()
    
    # TODO: Integrar com agente v1.8 real
    # Por enquanto, instrução manual para o aluno
    
    tempo = time.time() - inicio
    
    print(f"\n⏱️  Tempo: {tempo:.2f}s")
    print("\n📝 PREENCHA MANUALMENTE:")
    print("   1. O agente escolheu o dataset correto? (S/N)")
    print("   2. O agente usou os campos corretos? (S/N)")
    print("   3. A resposta foi precisa? (1-5)")
    print("   4. Houve erros? Quais?")
    
    return {
        "query_id": query_info['id'],
        "tempo": tempo,
        "dataset_correto": None,  # Aluno preenche
        "campos_corretos": None,  # Aluno preenche
        "qualidade": None,        # Aluno preenche (1-5)
        "erros": None             # Aluno preenche
    }

# ========== TABELA DE RESULTADOS ==========

def gerar_tabela_resultados():
    """Gerar tabela para aluno preencher manualmente."""
    
    print("\n" + "="*80)
    print("TABELA DE RESULTADOS - BASELINE ZERO-SHOT (v1.8)")
    print("="*80)
    print(f"{'ID':<4} {'Query':<50} {'Dataset OK':<12} {'Campos OK':<12} {'Qualidade':<12} {'Tempo (s)':<10}")
    print("-"*80)
    
    for q in QUERIES_TESTE:
        print(f"{q['id']:<4} {q['query'][:47]:<50} {'[ ]':<12} {'[ ]':<12} {'[   /5]':<12} {'[    ]':<10}")
    
    print("-"*80)
    print("\nLEGENDA:")
    print("  Dataset OK: [X] = escolheu dataset correto, [ ] = errou")
    print("  Campos OK:  [X] = usou campos necessários, [ ] = faltou/errou")
    print("  Qualidade:  1 (péssimo) a 5 (excelente)")
    print("  Tempo:      Latência em segundos")
    print("\n")
    print("MÉTRICAS CALCULADAS:")
    print("  Accuracy:    ___% (queries corretas / total)")
    print("  Tempo médio: ___s")
    print("  Taxa erro:   ___% (queries com erro / total)")
    print("="*80)

# ========== MAIN ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  ATIVIDADE 1A: MEDIR BASELINE (Zero-Shot)                    ║
║  Encontro 2 - Few-Shot Learning                              ║
╚═══════════════════════════════════════════════════════════════╝

INSTRUÇÕES:
1. Execute este script para ver as 5 queries de teste
2. Para CADA query, rode o agente v1.8 manualmente
3. Avalie a resposta usando os critérios fornecidos
4. Preencha a tabela de resultados
5. Calcule as métricas finais

CRITÉRIOS DE AVALIAÇÃO:
- Dataset OK: Agente escolheu o dataset correto?
- Campos OK: Agente usou todos os campos necessários?
- Qualidade: Resposta foi precisa, completa, útil? (1-5)
- Tempo: Quanto tempo levou? (medir manualmente)

DICA: Anote os erros! Você vai comparar com Few-Shot na Atividade 1D.
""")
    
    input("Pressione ENTER para ver as queries de teste...")
    
    # Mostrar queries
    print("\n" + "="*80)
    print("QUERIES DE TESTE")
    print("="*80)
    for q in QUERIES_TESTE:
        print(f"\n{q['id']}. {q['query']}")
        print(f"   📊 Dataset: {q['dataset_correto']}")
        print(f"   🔍 Campos: {', '.join(q['campos_necessarios'])}")
        print(f"   🎯 Esperado: {q['resposta_esperada']}")
    
    input("\n\nPressione ENTER para gerar tabela de resultados...")
    
    # Gerar tabela
    gerar_tabela_resultados()
    
    print("\n✅ PRÓXIMO PASSO: ATIVIDADE 1B - Criar Exemplos Few-Shot")
    print("   Você vai criar 3 exemplos de alta qualidade para melhorar o agente.\n")
