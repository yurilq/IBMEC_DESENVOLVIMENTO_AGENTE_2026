# passo_10_debug.py
# PASSO 10: Debugar problemas comuns com agente

from langchain_ollama import OllamaLLM
from langchain.agents import Tool, initialize_agent, AgentType
import pandas as pd

def contar_armas_marca(marca: str):
    """Conta armas por marca"""
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    return f"Encontrei {len(resultado)} armas {marca}"

llm = OllamaLLM(model="llama3", temperature=0)

tool = Tool(
    name="ContarArmas",
    func=contar_armas_marca,
    description="Conta armas por marca. Use quando usuário perguntar quantidade de uma marca específica."
)

agente = initialize_agent(
    tools=[tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  # Ver raciocínio
    max_iterations=5  # Evitar loop infinito
)

# Teste
pergunta = "Quantas Taurus?"
print(f"❓ {pergunta}\n")
resposta = agente.invoke({"input": pergunta})
print(f"\n✅ {resposta['output']}")
