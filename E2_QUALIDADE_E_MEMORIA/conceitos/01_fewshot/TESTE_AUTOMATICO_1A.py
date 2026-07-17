"""
SCRIPT DE TESTE - ATIVIDADE 1A
Executa as 5 queries no agente v1.8 automaticamente
"""

import sys
from pathlib import Path

# Ajustar path para importar agente v1.8
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "E1_ANATOMIA_DO_AGENTE" / "solucao_final"))

try:
    # Importar agente v1.8
    from E1_agente_react_v3 import AgenteInvestigador
except ImportError as e:
    print(f"❌ Erro ao importar agente v1.8: {e}")
    print("\nVerifique se o arquivo existe:")
    print("  E1_ANATOMIA_DO_AGENTE/solucao_final/E1_agente_react_v3.py")
    sys.exit(1)

# Queries da ATIVIDADE 1A
QUERIES = [
    "Quantas ocorrências de furto de armas Taurus aconteceram no DF?",
    "Quais marcas de arma têm mais portes válidos atualmente?",
    "Quantos registros de pistola calibre 9mm existem?",
    "Qual a taxa de aprovação de requerimentos de porte no DF?",
    "Quais municípios do DF tiveram mais recuperações de armas em 2026?"
]

def testar_query(agente, query_num, query):
    """Testa uma query e permite avaliação manual"""
    
    print(f"\n{'='*80}")
    print(f"QUERY {query_num}/5")
    print(f"{'='*80}")
    print(f"\n📝 Pergunta: {query}\n")
    
    import time
    inicio = time.time()
    
    try:
        # Executar query no agente
        resposta = agente.executar(query)
        
        tempo = time.time() - inicio
        
        print(f"\n🤖 Resposta do Agente:")
        print(f"{'-'*80}")
        print(resposta)
        print(f"{'-'*80}")
        print(f"\n⏱️  Tempo: {tempo:.2f}s")
        
        # Avaliação manual
        print(f"\n📊 AVALIAÇÃO (preencha manualmente):")
        dataset_ok = input("   Dataset correto? (S/N): ").strip().upper()
        campos_ok = input("   Campos corretos? (S/N): ").strip().upper()
        qualidade = input("   Qualidade (1-5): ").strip()
        
        return {
            'query': query,
            'resposta': resposta,
            'tempo': tempo,
            'dataset_ok': dataset_ok == 'S',
            'campos_ok': campos_ok == 'S',
            'qualidade': int(qualidade) if qualidade.isdigit() else 3
        }
        
    except Exception as e:
        print(f"\n❌ Erro ao executar query: {e}")
        return {
            'query': query,
            'resposta': f"ERRO: {e}",
            'tempo': time.time() - inicio,
            'dataset_ok': False,
            'campos_ok': False,
            'qualidade': 1
        }

def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  TESTE AUTOMÁTICO - ATIVIDADE 1A                             ║
║  Executa 5 queries no agente v1.8 e coleta avaliações        ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar agente v1.8
    print("🔧 Inicializando agente v1.8...")
    try:
        agente = AgenteInvestigador(verbose=True)
        print("✅ Agente v1.8 carregado!\n")
    except Exception as e:
        print(f"❌ Erro ao inicializar agente: {e}")
        return
    
    # Testar cada query
    resultados = []
    
    for i, query in enumerate(QUERIES, 1):
        resultado = testar_query(agente, i, query)
        resultados.append(resultado)
        
        if i < len(QUERIES):
            input(f"\n{'─'*80}\nPressione ENTER para próxima query...\n{'─'*80}\n")
    
    # Relatório final
    print(f"\n{'='*80}")
    print("📊 RELATÓRIO FINAL - BASELINE v1.8")
    print(f"{'='*80}\n")
    
    print(f"{'ID':<4} {'Dataset OK':<12} {'Campos OK':<12} {'Qualidade':<12} {'Tempo (s)':<10}")
    print(f"{'-'*80}")
    
    for i, r in enumerate(resultados, 1):
        dataset_icon = "[X]" if r['dataset_ok'] else "[ ]"
        campos_icon = "[X]" if r['campos_ok'] else "[ ]"
        print(f"{i:<4} {dataset_icon:<12} {campos_icon:<12} {r['qualidade']:<12} {r['tempo']:.2f}s")
    
    # Métricas
    corretas = sum(1 for r in resultados if r['dataset_ok'] and r['campos_ok'])
    accuracy = (corretas / len(resultados)) * 100
    tempo_medio = sum(r['tempo'] for r in resultados) / len(resultados)
    erros = len(resultados) - corretas
    taxa_erro = (erros / len(resultados)) * 100
    
    print(f"\n{'─'*80}")
    print(f"📈 MÉTRICAS:")
    print(f"   Accuracy:    {accuracy:.0f}% ({corretas}/{len(resultados)} corretas)")
    print(f"   Tempo médio: {tempo_medio:.2f}s")
    print(f"   Taxa erro:   {taxa_erro:.0f}% ({erros}/{len(resultados)} erros)")
    print(f"{'='*80}\n")
    
    print("✅ ATIVIDADE 1A CONCLUÍDA!")
    print("📝 Anote esses resultados - você vai comparar na ATIVIDADE 1D\n")

if __name__ == "__main__":
    main()
