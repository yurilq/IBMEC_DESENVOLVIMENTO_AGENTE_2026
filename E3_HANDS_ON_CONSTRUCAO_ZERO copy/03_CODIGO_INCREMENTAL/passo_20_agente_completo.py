# passo_20_agente_completo.py
# PASSO 20: AGENTE V2.0 COMPLETO
# Igual ao TEMPLATE_HORA_5.py - versão final

import pandas as pd
from functools import lru_cache
from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType

# Validação
def validar_input(texto: str):
    if len(texto) > 500:
        raise ValueError("Query muito longa")
    if len(texto) < 3:
        raise ValueError("Query muito curta")
    perigosos = [";", "--", "DROP", "DELETE"]
    for char in perigosos:
        if char in texto.upper():
            raise ValueError(f"Caractere perigoso: {char}")
    return True

def perguntar_seguro(pergunta: str):
    try:
        validar_input(pergunta)
        resposta = agente.invoke({"input": pergunta})
        return resposta["output"]
    except ValueError as e:
        return f"❌ ERRO: {e}"

# Cache
@lru_cache(maxsize=1)
def carregar_csv():
    print("🔄 Carregando CSV...")
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    return df

# Tools
@tool
def contar_armas_marca(marca: str) -> str:
    """Conta armas por marca"""
    df = carregar_csv()
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    return f"Encontrei {len(resultado)} armas {marca}"

@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta armas por calibre"""
    df = carregar_csv()
    resultado = df[df["CALIBRE"] == calibre]
    return f"Encontrei {len(resultado)} armas calibre {calibre}"

@tool
def contar_armas_tipo(tipo: str) -> str:
    """Conta por tipo de ocorrência"""
    df = carregar_csv()
    resultado = df[df["TIPO_OCORRENCIA"] == tipo.upper()]
    return f"Encontrei {len(resultado)} ocorrências {tipo}"

@tool
def contar_armas_combinado(marca: str, tipo: str) -> str:
    """Conta por marca E tipo"""
    df = carregar_csv()
    resultado = df[(df["MARCA_ARMA"] == marca.upper()) & 
                   (df["TIPO_OCORRENCIA"] == tipo.upper())]
    return f"Encontrei {len(resultado)} armas {marca} tipo {tipo}"

# Agente
llm = OllamaLLM(model="llama3", temperature=0)

system_message = """
Você é investigador PCDF especialista em SINARM.

=== FEW-SHOT ===
Pergunta: "O que é BO furto?"
Resposta: "BO furto é tipo=FURTO no SINARM."

=== CHAIN-OF-THOUGHT ===
PASSO 1 - ANÁLISE: Tipo pergunta?
PASSO 2 - BUSCA: Tool e params
PASSO 3 - RESULTADO: Valores
PASSO 4 - RESPOSTA: Conclusão + Fonte SINARM
"""

agente = initialize_agent(
    tools=[contar_armas_marca, contar_armas_calibre,
           contar_armas_tipo, contar_armas_combinado],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"system_message": system_message}
)

if __name__ == "__main__":
    print("🤖 AGENTE SINARM v2.0 COMPLETO\n")
    while True:
        p = input("❓ Pergunta (ou 'sair'): ")
        if p.lower() == 'sair': break
        print(f"\n💬 {perguntar_seguro(p)}\n")
