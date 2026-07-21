# teste_llm.py
# Primeiro contato com LLM

# LINHA 1: Importar LangChain
from langchain_ollama import OllamaLLM

# LINHA 2: Criar conexão com Ollama
llm = OllamaLLM(model="llama3")

"""
# LINHA 3: Enviar pergunta
resposta = llm.invoke("Olá, tudo bem?")

# LINHA 4: Mostrar resposta
print(resposta)

"""

perguntas = [
    "Quantas armas existem no Brasil?",
    "O que é o sistema SINARM?",
    "Qual a diferença entre calibre .38 e 9mm?"
]

for pergunta in perguntas:
    print(f"\n❓ PERGUNTA: {pergunta}")
    resposta = llm.invoke(pergunta)
    print(f"💬 RESPOSTA: {resposta}\n")
    print("-" * 60)