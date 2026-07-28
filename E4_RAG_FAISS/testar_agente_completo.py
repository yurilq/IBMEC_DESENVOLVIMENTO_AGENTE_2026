"""
TESTE COMPLETO DO AGENTE v4.5 COM OLLAMA
Executa o agente com diferentes tipos de perguntas
"""

import sys
import os

# Adicionar path dos scripts
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts_agente'))

from agente_v4_5_rag import agente_v4_5_rag

print("="*70)
print("TESTE DO AGENTE v4.5 - EXECUCAO REAL COM OLLAMA")
print("="*70)
print()

# Lista de perguntas de teste
perguntas_teste = [
    "Quantas armas Taurus?",
    "O que eh calibre de arma?",
    "Quantas armas calibre .38?",
]

for i, pergunta in enumerate(perguntas_teste, 1):
    print(f"\n{'='*70}")
    print(f"TESTE {i}/3: {pergunta}")
    print(f"{'='*70}")
    
    try:
        resposta = agente_v4_5_rag(pergunta)
        print(f"\n[RESPOSTA FINAL]")
        print(resposta)
    except Exception as e:
        print(f"\n[ERRO] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "-"*70)
    input("Pressione ENTER para continuar...")

print("\n" + "="*70)
print("TESTES CONCLUIDOS!")
print("="*70)
