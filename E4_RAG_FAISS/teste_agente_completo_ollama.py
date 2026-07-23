"""
TESTE COMPLETO DO AGENTE v4.5 COM OLLAMA
Executa o agente end-to-end com perguntas reais
"""

import sys
import os

# Adicionar path dos scripts
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts_agente'))

from agente_v4_5_rag import agente_v4_5_rag

print("="*70)
print("TESTE END-TO-END - AGENTE v4.5 COM OLLAMA")
print("="*70)
print()

# Lista de perguntas de teste
testes = [
    {
        "numero": 1,
        "pergunta": "Quantas armas calibre .38?",
        "tipo_esperado": "calibre",
        "descricao": "Pergunta simples - busca SQL por calibre"
    },
    {
        "numero": 2,
        "pergunta": "O que eh calibre de arma?",
        "tipo_esperado": "conceitual",
        "descricao": "Pergunta conceitual - usa RAG TF-IDF"
    },
]

resultados = []

for teste in testes:
    print(f"\n{'='*70}")
    print(f"TESTE {teste['numero']}: {teste['pergunta']}")
    print(f"Tipo esperado: {teste['tipo_esperado']}")
    print(f"Descricao: {teste['descricao']}")
    print(f"{'='*70}\n")
    
    try:
        resposta = agente_v4_5_rag(teste['pergunta'])
        
        print(f"\n{'─'*70}")
        print(f"[RESPOSTA FINAL DO AGENTE]")
        print(f"{'─'*70}")
        print(resposta)
        print(f"{'─'*70}")
        
        resultados.append({
            "teste": teste['numero'],
            "status": "SUCESSO",
            "pergunta": teste['pergunta'],
            "resposta": resposta
        })
        
    except Exception as e:
        print(f"\n[ERRO] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        
        resultados.append({
            "teste": teste['numero'],
            "status": "ERRO",
            "pergunta": teste['pergunta'],
            "erro": str(e)
        })
    
    print("\n")

# =============================================================================
# RESUMO FINAL
# =============================================================================

print("\n" + "="*70)
print("RESUMO DOS TESTES")
print("="*70)

for resultado in resultados:
    status_icon = "[OK]" if resultado['status'] == "SUCESSO" else "[X]"
    print(f"\n{status_icon} TESTE {resultado['teste']}: {resultado['pergunta']}")
    if resultado['status'] == "SUCESSO":
        print(f"    Resposta obtida com sucesso")
    else:
        print(f"    Erro: {resultado['erro']}")

print("\n" + "="*70)
print(f"TOTAL: {len([r for r in resultados if r['status'] == 'SUCESSO'])}/{len(resultados)} testes bem-sucedidos")
print("="*70)
