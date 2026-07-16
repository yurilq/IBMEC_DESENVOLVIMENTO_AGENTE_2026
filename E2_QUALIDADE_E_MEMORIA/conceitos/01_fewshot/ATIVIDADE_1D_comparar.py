"""
ATIVIDADE 1D: COMPARAR v1.8 vs v2.0 (MEDIR IMPACTO FEW-SHOT)
Encontro 2 - Conceito: Few-Shot Learning
Duração: 15 minutos

OBJETIVO:
Comparar objetivamente a performance do agente v1.8 (Zero-Shot) vs v2.0 (Few-Shot)
usando as mesmas 5 queries da Atividade 1A.

O QUE VOCÊ VAI FAZER:
1. Executar as 5 queries teste no agente v2.0 (Few-Shot)
2. Comparar com resultados do v1.8 (baseline da Atividade 1A)
3. Calcular métricas: Δ accuracy, Δ latência, Δ erros
4. Analisar: Few-Shot valeu a pena?

POR QUE ISSO É IMPORTANTE:
- Decisões técnicas precisam ser baseadas em DADOS, não intuição
- Medir impacto é essencial para justificar mudanças
- Trade-off: Few-Shot aumenta latência (prompt maior) mas melhora accuracy
- Baseline + Experimento + Comparação = método científico em engenharia

CONCEITO: A/B Testing para Agentes
┌──────────────────────────────────────────────────────────────┐
│ BASELINE (v1.8 Zero-Shot)                                    │
│ ✓ Accuracy:     60% (3/5 queries corretas)                   │
│ ✓ Latência:     2.3s média                                   │
│ ✓ Taxa erro:    40%                                          │
├──────────────────────────────────────────────────────────────┤
│ EXPERIMENTO (v2.0 Few-Shot)                                  │
│ ✓ Accuracy:     80% (4/5 queries corretas)                   │
│ ✓ Latência:     2.8s média (+21% por causa do prompt maior) │
│ ✓ Taxa erro:    20%                                          │
├──────────────────────────────────────────────────────────────┤
│ ANÁLISE                                                      │
│ ✅ Accuracy melhorou +20pp (60% → 80%)                       │
│ ⚠️  Latência aumentou +21% (2.3s → 2.8s)                     │
│ ✅ Erros reduziram 50% (40% → 20%)                           │
│                                                              │
│ CONCLUSÃO: Few-Shot vale a pena!                            │
│ Trade-off favorável: +20% accuracy por +0.5s latência       │
└──────────────────────────────────────────────────────────────┘

MÉTRICAS:
- Accuracy: % queries respondidas corretamente
- Latência: Tempo médio de resposta (segundos)
- Taxa erro: % queries com erro/falha
- Δ (Delta): Diferença entre v2.0 e v1.8
"""

import sys
from pathlib import Path
import json
import time

# Ajustar path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

# Importar atividades anteriores
from ATIVIDADE_1A_baseline import QUERIES_TESTE
from ATIVIDADE_1C_implementar import criar_agente_v2_fewshot, carregar_exemplos

# ========== EXECUTAR QUERIES v2.0 ==========

def executar_queries_v2(agente):
    """
    Executa as 5 queries teste no agente v2.0.
    
    Retorna: lista de resultados
    """
    
    resultados = []
    
    print("\n" + "="*70)
    print("EXECUTANDO QUERIES NO AGENTE v2.0 (FEW-SHOT)")
    print("="*70)
    
    for q in QUERIES_TESTE:
        print(f"\n📝 Query {q['id']}: {q['query']}")
        print(f"   Dataset esperado: {q['dataset_correto']}")
        
        inicio = time.time()
        
        try:
            resposta = agente.invoke({"input": q['query']})
            tempo = time.time() - inicio
            
            print(f"   ⏱️  Tempo: {tempo:.2f}s")
            print(f"   ✅ Resposta: {resposta['output'][:80]}...")
            
            # Avaliar manualmente (aluno preenche)
            print("\n   📊 AVALIAR:")
            dataset_ok = input("      Dataset correto? (S/N): ").strip().upper() == "S"
            campos_ok = input("      Campos corretos? (S/N): ").strip().upper() == "S"
            qualidade = int(input("      Qualidade (1-5): ").strip())
            
            resultados.append({
                "query_id": q['id'],
                "tempo": tempo,
                "dataset_correto": dataset_ok,
                "campos_corretos": campos_ok,
                "qualidade": qualidade,
                "sucesso": dataset_ok and campos_ok and qualidade >= 3
            })
            
        except Exception as e:
            tempo = time.time() - inicio
            print(f"   ❌ Erro: {str(e)}")
            
            resultados.append({
                "query_id": q['id'],
                "tempo": tempo,
                "dataset_correto": False,
                "campos_corretos": False,
                "qualidade": 0,
                "sucesso": False,
                "erro": str(e)
            })
    
    return resultados

# ========== CARREGAR RESULTADOS v1.8 ==========

def carregar_resultados_v1():
    """
    Carrega resultados do v1.8 (Atividade 1A).
    
    Se não existir arquivo, pede para o aluno preencher manualmente.
    """
    
    caminho = Path(__file__).parent / "resultados_v1.8_baseline.json"
    
    if caminho.exists():
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Não existe - preencher manualmente
    print("\n⚠️  Arquivo resultados_v1.8_baseline.json não encontrado.")
    print("   Digite os resultados da ATIVIDADE_1A manualmente:\n")
    
    resultados_v1 = []
    
    for q in QUERIES_TESTE:
        print(f"\nQuery {q['id']}: {q['query']}")
        dataset_ok = input("  Dataset correto? (S/N): ").strip().upper() == "S"
        campos_ok = input("  Campos corretos? (S/N): ").strip().upper() == "S"
        qualidade = int(input("  Qualidade (1-5): ").strip())
        tempo = float(input("  Tempo (segundos): ").strip())
        
        resultados_v1.append({
            "query_id": q['id'],
            "tempo": tempo,
            "dataset_correto": dataset_ok,
            "campos_corretos": campos_ok,
            "qualidade": qualidade,
            "sucesso": dataset_ok and campos_ok and qualidade >= 3
        })
    
    # Salvar para não pedir novamente
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultados_v1, f, ensure_ascii=False, indent=2)
    
    return resultados_v1

# ========== CALCULAR MÉTRICAS ==========

def calcular_metricas(resultados):
    """Calcula accuracy, latência média, taxa de erro."""
    
    total = len(resultados)
    sucessos = sum(1 for r in resultados if r['sucesso'])
    erros = total - sucessos
    tempo_medio = sum(r['tempo'] for r in resultados) / total
    
    return {
        "accuracy": (sucessos / total) * 100,
        "latencia_media": tempo_medio,
        "taxa_erro": (erros / total) * 100,
        "total_queries": total,
        "sucessos": sucessos,
        "erros": erros
    }

# ========== COMPARAR v1.8 vs v2.0 ==========

def comparar_versoes(resultados_v1, resultados_v2):
    """Compara métricas v1.8 vs v2.0 e calcula Δ."""
    
    metricas_v1 = calcular_metricas(resultados_v1)
    metricas_v2 = calcular_metricas(resultados_v2)
    
    delta_accuracy = metricas_v2['accuracy'] - metricas_v1['accuracy']
    delta_latencia = metricas_v2['latencia_media'] - metricas_v1['latencia_media']
    delta_latencia_pct = (delta_latencia / metricas_v1['latencia_media']) * 100
    delta_erro = metricas_v2['taxa_erro'] - metricas_v1['taxa_erro']
    
    print("\n" + "="*70)
    print("COMPARAÇÃO: v1.8 (Zero-Shot) vs v2.0 (Few-Shot)")
    print("="*70)
    
    print(f"\n{'Métrica':<20} {'v1.8 (Baseline)':<20} {'v2.0 (Few-Shot)':<20} {'Δ':<15}")
    print("-"*70)
    
    print(f"{'Accuracy':<20} {metricas_v1['accuracy']:.1f}%{'':<14} {metricas_v2['accuracy']:.1f}%{'':<14} {delta_accuracy:+.1f}pp")
    print(f"{'Latência média':<20} {metricas_v1['latencia_media']:.2f}s{'':<14} {metricas_v2['latencia_media']:.2f}s{'':<14} {delta_latencia:+.2f}s ({delta_latencia_pct:+.0f}%)")
    print(f"{'Taxa erro':<20} {metricas_v1['taxa_erro']:.1f}%{'':<14} {metricas_v2['taxa_erro']:.1f}%{'':<14} {delta_erro:+.1f}pp")
    print(f"{'Sucessos':<20} {metricas_v1['sucessos']}/{metricas_v1['total_queries']}{'':<14} {metricas_v2['sucessos']}/{metricas_v2['total_queries']}{'':<14}")
    
    print("\n" + "="*70)
    print("ANÁLISE")
    print("="*70)
    
    if delta_accuracy > 10:
        print(f"✅ Accuracy melhorou significativamente ({delta_accuracy:+.1f}pp)")
    elif delta_accuracy > 0:
        print(f"✅ Accuracy melhorou levemente ({delta_accuracy:+.1f}pp)")
    else:
        print(f"❌ Accuracy piorou ({delta_accuracy:+.1f}pp)")
    
    if abs(delta_latencia_pct) < 10:
        print(f"✅ Latência manteve-se estável ({delta_latencia_pct:+.0f}%)")
    elif delta_latencia_pct > 0:
        print(f"⚠️  Latência aumentou ({delta_latencia_pct:+.0f}%) - prompt maior")
    else:
        print(f"✅ Latência diminuiu ({delta_latencia_pct:+.0f}%)")
    
    if delta_erro < 0:
        reducao_pct = abs((delta_erro / metricas_v1['taxa_erro']) * 100)
        print(f"✅ Erros reduziram {reducao_pct:.0f}%")
    elif delta_erro > 0:
        print(f"❌ Erros aumentaram ({delta_erro:+.1f}pp)")
    else:
        print(f"➖ Taxa de erro manteve-se igual")
    
    # Conclusão
    print("\n" + "="*70)
    print("CONCLUSÃO")
    print("="*70)
    
    if delta_accuracy > 10 and abs(delta_latencia_pct) < 30:
        print("✅ Few-Shot VALE A PENA!")
        print("   Trade-off favorável: melhoria significativa em accuracy")
        print("   com aumento aceitável de latência.")
    elif delta_accuracy > 5:
        print("✅ Few-Shot é BENÉFICO, mas com ressalvas.")
        print("   Melhoria moderada. Avalie se latência extra é aceitável.")
    else:
        print("⚠️  Few-Shot teve impacto LIMITADO.")
        print("   Considere: mais exemplos? Exemplos de melhor qualidade?")
    
    print("="*70)
    
    return {
        "v1": metricas_v1,
        "v2": metricas_v2,
        "delta": {
            "accuracy": delta_accuracy,
            "latencia": delta_latencia,
            "latencia_pct": delta_latencia_pct,
            "erro": delta_erro
        }
    }

# ========== MAIN ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  ATIVIDADE 1D: COMPARAR v1.8 vs v2.0 (MEDIR IMPACTO)        ║
║  Encontro 2 - Few-Shot Learning                              ║
╚═══════════════════════════════════════════════════════════════╝

INSTRUÇÕES:
1. Certifique-se que tem os resultados da ATIVIDADE_1A (v1.8 baseline)
2. Execute as 5 queries teste no agente v2.0
3. Compare as métricas: Δ accuracy, Δ latência, Δ erros
4. Analise: Few-Shot valeu a pena?

MÉTRICAS:
- Accuracy: % queries corretas
- Latência: Tempo médio de resposta
- Taxa erro: % queries com erro/falha
- Δ (Delta): Diferença v2.0 - v1.8
""")
    
    input("Pressione ENTER para começar...")
    
    # 1. Carregar exemplos e criar agente v2.0
    print("\n🔧 Criando agente v2.0 (Few-Shot)...")
    exemplos = carregar_exemplos()
    agente_v2 = criar_agente_v2_fewshot(exemplos)
    print("✅ Agente v2.0 pronto!")
    
    # 2. Executar queries v2.0
    resultados_v2 = executar_queries_v2(agente_v2)
    
    # 3. Carregar resultados v1.8
    print("\n📂 Carregando resultados v1.8 (baseline)...")
    resultados_v1 = carregar_resultados_v1()
    
    # 4. Comparar
    comparacao = comparar_versoes(resultados_v1, resultados_v2)
    
    # 5. Salvar comparação
    caminho_comparacao = Path(__file__).parent / "comparacao_v1_v2.json"
    with open(caminho_comparacao, "w", encoding="utf-8") as f:
        json.dump(comparacao, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Comparação salva em: {caminho_comparacao}")
    
    print("\n" + "="*70)
    print("✅ ATIVIDADE 1 (FEW-SHOT) CONCLUÍDA!")
    print("="*70)
    print("\nVocê aprendeu:")
    print("  ✓ Medir baseline (Zero-Shot)")
    print("  ✓ Criar exemplos Few-Shot de qualidade")
    print("  ✓ Implementar Few-Shot no agente")
    print("  ✓ Comparar versões com métricas objetivas")
    print("\n🎯 PRÓXIMO: ATIVIDADE 2 - Chain-of-Thought (CoT)")
    print("   Vamos adicionar raciocínio explícito para queries complexas!\n")
