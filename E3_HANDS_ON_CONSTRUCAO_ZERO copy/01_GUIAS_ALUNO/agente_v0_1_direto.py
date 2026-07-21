# agente_v0_1_direto.py
# Versão MAIS SIMPLES - teste direto do LLM com tool

from langchain_ollama import OllamaLLM
from tools_basicas import contar_armas_marca

print("="*60)
print("TESTE SIMPLES: LLM + TOOL")
print("="*60)

# Criar LLM
llm = OllamaLLM(model="llama3", temperature=0)
print("[OK] LLM criado\n")

# TESTE 1: LLM responde sozinho
print("TESTE 1: Pergunta simples ao LLM")
print("-" * 60)
resposta = llm.invoke("Olá, você está funcionando?")
print(f"Resposta: {resposta}\n")

# TESTE 2: Chamar tool diretamente
print("TESTE 2: Chamar tool diretamente")
print("-" * 60)
resultado_tool = contar_armas_marca("Taurus")
print(f"Resultado da tool: {resultado_tool}\n")

# TESTE 3: LLM com contexto da tool
print("TESTE 3: LLM usando resultado da tool")
print("-" * 60)
pergunta_usuario = "Quantas armas Taurus existem?"
resultado_tool = contar_armas_marca("Taurus")

prompt_com_contexto = f"""O usuário perguntou: "{pergunta_usuario}"

Eu consultei o banco de dados e obtive: {resultado_tool}

Responda ao usuário de forma clara:"""

resposta_final = llm.invoke(prompt_com_contexto)
print(f"Resposta final: {resposta_final}\n")

print("="*60)
print("TODOS OS TESTES CONCLUÍDOS!")
print("="*60)
