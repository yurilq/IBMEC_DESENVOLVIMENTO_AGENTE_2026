# agente_v0_1.py
# Agente manual - LangChain 1.3+

from langchain_ollama import OllamaLLM
from langchain_core.tools import Tool  # ← Import mudou!
from tools_basicas import contar_armas_marca
import re

print("="*60)
print("CRIANDO AGENTE MANUAL - LangChain 1.3+")
print("="*60)

# PARTE 1: Criar LLM
print("\n[1/3] Criando LLM...")
llm = OllamaLLM(model="llama3.2:1b", temperature=0)
print("      [OK] LLM criado")

# PARTE 2: Criar Tool
print("\n[2/3] Criando Tool...")
tool_contar = Tool(
    name="contar_armas_marca",
    func=contar_armas_marca,
    description="Conta quantas armas de uma marca específica. Input: nome da marca"
)
print("      [OK] Tool criada")

# PARTE 3: Criar função agente (implementa ReAct manualmente)
print("\n[3/3] Criando agente...")

def agente_simples(pergunta_usuario):
    """
    Implementa ciclo ReAct manualmente:
    THOUGHT → ACTION → OBSERVATION → THOUGHT → ANSWER
    """
    
    # THOUGHT: Analisar pergunta
    print(f"\n[THOUGHT] Processando: '{pergunta_usuario}'")
    
    # Detectar marca na pergunta
    marcas = ["taurus", "glock", "rossi", "beretta", "smith"]
    marca_encontrada = None
    
    for marca in marcas:
        if marca in pergunta_usuario.lower():
            marca_encontrada = marca.capitalize()
            break
    
    if not marca_encontrada:
        return "Não identifiquei a marca. Tente: Taurus, Glock, Rossi..."
    
    # ACTION: Chamar tool
    print(f"[ACTION] Chamando: {tool_contar.name}('{marca_encontrada}')")
    resultado_tool = tool_contar.func(marca_encontrada)
    
    # OBSERVATION: Ver resultado
    print(f"[OBSERVATION] {resultado_tool}")
    
    # THOUGHT + ANSWER: Formatar com LLM
    print(f"[THOUGHT] Formatando resposta...")
    
    # Extrair número do resultado
    numeros = re.findall(r'\d+', resultado_tool)
    total = numeros[0] if numeros else "?"
    
    prompt = f"""Dados do SINARM: {resultado_tool}

Responda APENAS o número e a marca de forma direta.
Exemplo: "Existem 17.760 armas Taurus."

Resposta:"""
    
    resposta_final = llm.invoke(prompt)
    
    return resposta_final

print("      [OK] Agente pronto")

# PARTE 4: Testar
print("\n" + "="*60)
print("TESTANDO AGENTE")
print("="*60)

pergunta = "Quantas armas Taurus existem?"
print(f"\nPERGUNTA: {pergunta}")
print("-"*60)

resposta = agente_simples(pergunta)

print("-"*60)
print(f"\nRESPOSTA FINAL: {resposta}\n")
print("="*60)