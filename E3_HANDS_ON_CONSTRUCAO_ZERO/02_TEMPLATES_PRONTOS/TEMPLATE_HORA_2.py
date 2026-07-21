# TEMPLATE_HORA_2.py
# Código de referência para Parte 2: Primeira Tool (SEM decorator)
# Use se ficar travado na Parte 2

from langchain_ollama import OllamaLLM
from langchain.agents import Tool, initialize_agent, AgentType
import pandas as pd

# ============================================================
# FUNÇÃO PYTHON SIMPLES
# ============================================================

def contar_armas_marca(marca: str):
    """Conta quantas armas de uma marca específica"""
    
    print(f"🔍 Buscando armas da marca: {marca}")
    
    # Carregar CSV
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", 
                     sep=";", 
                     encoding="latin1")
    
    # Filtrar por marca
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    
    # Contar
    total = len(resultado)
    
    return f"Encontrei {total} armas da marca {marca}"


# ============================================================
# TESTAR FUNÇÃO ISOLADA
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("TESTANDO FUNÇÃO")
    print("="*60)
    
    resultado = contar_armas_marca("Taurus")
    print(f"✅ {resultado}")
    
    resultado = contar_armas_marca("Glock")
    print(f"✅ {resultado}")
    
    print("="*60)
    
    # ============================================================
    # CRIAR AGENTE COM TOOL MANUAL
    # ============================================================
    
    print("\n" + "="*60)
    print("CRIANDO AGENTE COM TOOL")
    print("="*60)
    
    # LLM
    llm = OllamaLLM(model="llama3", temperature=0)
    
    # Tool MANUAL (jeito chato)
    tool_contar = Tool(
        name="ContarArmas",
        func=contar_armas_marca,
        description="""Conta quantas armas de uma marca específica estão registradas no SINARM.
        
Input: Nome da marca (string) - ex: 'Taurus', 'Glock', 'Rossi'
Output: Total de armas encontradas

Use esta ferramenta quando usuário perguntar sobre QUANTIDADE de armas de uma MARCA específica."""
    )
    
    # Agente
    agente = initialize_agent(
        tools=[tool_contar],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    # Testar
    print("\n" + "="*60)
    print("TESTANDO AGENTE")
    print("="*60 + "\n")
    
    pergunta = "Quantas armas Taurus existem?"
    print(f"❓ PERGUNTA: {pergunta}\n")
    
    resposta = agente.invoke({"input": pergunta})
    
    print(f"\n✅ RESPOSTA FINAL: {resposta['output']}\n")
    print("="*60)
