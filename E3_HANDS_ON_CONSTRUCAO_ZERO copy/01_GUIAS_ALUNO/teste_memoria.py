# teste_memoria.py
# Teste com modelo menor para economizar RAM

from langchain_ollama import OllamaLLM

print("="*60)
print("TESTE COM MODELO MENOR (llama3.2:1b)")
print("="*60)

# Usar modelo menor
llm = OllamaLLM(model="llama3.2:1b", temperature=0)
print("[OK] LLM criado com modelo menor\n")

# Teste simples
print("Testando LLM...")
resposta = llm.invoke("Olá! Responda apenas: OK")
print(f"Resposta: {resposta}")

print("\n" + "="*60)
print("SUCESSO! Modelo menor funciona")
print("="*60)
