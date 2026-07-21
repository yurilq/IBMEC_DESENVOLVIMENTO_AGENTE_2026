# passo_01_hello_world.py
# PASSO 1: Primeiro contato com LLM

from langchain_ollama import OllamaLLM

# Criar LLM
llm = OllamaLLM(model="llama3")

# Primeira pergunta
resposta = llm.invoke("Olá, tudo bem?")

# Mostrar
print(resposta)
