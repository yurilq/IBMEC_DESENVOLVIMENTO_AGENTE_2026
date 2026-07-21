# TEMPLATE_HORA_3.py
# Código de referência para Parte 3: Decorators + @tool
# Use se ficar travado na Parte 3

import pandas as pd
from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType

# ============================================================
# EXEMPLO 1: DECORATOR SIMPLES
# ============================================================

def mostrar_log(funcao):
    """Decorator que adiciona log"""
    
    def funcao_embrulhada(a, b):
        print(f"Chamando {funcao.__name__}({a}, {b})...")
        resultado = funcao(a, b)
        print(f"Resultado: {resultado}")
        return resultado
    
    return funcao_embrulhada

@mostrar_log
def somar(a, b):
    return a + b

@mostrar_log
def multiplicar(a, b):
    return a * b

# Testar
print("="*40)
print("EXEMPLO: DECORATOR SIMPLES")
print("="*40)
somar(2, 3)
print("="*40)
multiplicar(4, 5)
print("="*40)

# ============================================================
# EXEMPLO 2: TOOL COM @tool DECORATOR
# ============================================================

@tool
def contar_armas_marca(marca: str) -> str:
    """Conta quantas armas de uma marca específica estão registradas.
    
    Args:
        marca: Nome da marca (ex: Taurus, Glock, Rossi)
    
    Returns:
        String com total de armas encontradas
    """
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    total = len(resultado)
    return f"Encontrei {total} armas da marca {marca}"

# ============================================================
# AGENTE COM @tool (SIMPLIFICADO)
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("AGENTE COM @tool DECORATOR")
    print("="*60)
    
    llm = OllamaLLM(model="llama3", temperature=0)
    
    # ANTES (Hora 2 - SEM @tool): 15 linhas
    # Tool manual com name, func, description...
    
    # DEPOIS (Hora 3 - COM @tool): 1 linha!
    agente = initialize_agent(
        tools=[contar_armas_marca],  # ← Direto! Mais simples!
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    # Testar
    pergunta = "Quantas armas Taurus?"
    print(f"\n❓ PERGUNTA: {pergunta}\n")
    
    resposta = agente.invoke({"input": pergunta})
    print(f"\n✅ RESPOSTA: {resposta['output']}\n")
    print("="*60)
