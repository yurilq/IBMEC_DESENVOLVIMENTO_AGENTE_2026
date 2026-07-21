# teste_rapido.py
# Teste rápido do agente v3.0

from agente_v3_0 import agente_v3_fewshot_cot

print("\n" + "="*70)
print("TESTE RÁPIDO - Agente v3.0")
print("="*70)

# Teste simples
pergunta = "Quantas armas Taurus?"
print(f"\nPergunta: {pergunta}\n")

resposta = agente_v3_fewshot_cot(pergunta)

print("\n" + "="*70)
print("RESPOSTA:")
print("="*70)
print(resposta)
