# TEMPLATE_HORA_1.py
# Código de referência para Parte 1: Setup + Hello World
# Use se ficar travado na Parte 1

from langchain_ollama import OllamaLLM

# Criar conexão com LLM
llm = OllamaLLM(model="llama3")

# Enviar pergunta
resposta = llm.invoke("Olá, tudo bem?")

# Mostrar resposta
print(resposta)

# ============================================================
# EXERCÍCIO: Fazer 3 perguntas
# ============================================================

perguntas = [
    "Quantas armas existem no Brasil?",
    "O que é o sistema SINARM?",
    "Qual a diferença entre calibre .38 e 9mm?"
]

print("\n" + "="*60)
print("TESTANDO MÚLTIPLAS PERGUNTAS")
print("="*60 + "\n")

for pergunta in perguntas:
    print(f"❓ PERGUNTA: {pergunta}")
    resposta = llm.invoke(pergunta)
    print(f"💬 RESPOSTA: {resposta}\n")
    print("-" * 60)
