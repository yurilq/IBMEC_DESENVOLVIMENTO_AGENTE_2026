# TEMPLATE_HORA_4.py
# Código de referência para Parte 4: 4 Tools + Cache
# Use se ficar travado na Parte 4

import pandas as pd
from functools import lru_cache
from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType

# ============================================================
# CACHE: Carregar CSV UMA VEZ
# ============================================================

@lru_cache(maxsize=1)
def carregar_csv():
    """Carrega CSV UMA VEZ e guarda em cache"""
    print("🔄 Carregando CSV...")
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    print(f"✅ CSV carregado! {len(df)} linhas")
    return df

# ============================================================
# 4 TOOLS COM @tool
# ============================================================

@tool
def contar_armas_marca(marca: str) -> str:
    """Conta quantas armas de uma marca específica.
    
    Args:
        marca: Nome da marca (ex: Taurus, Glock, Rossi)
    """
    df = carregar_csv()  # Usa cache!
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    return f"Encontrei {len(resultado)} armas {marca}"

@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta quantas armas de um calibre específico.
    
    Args:
        calibre: Calibre da arma (ex: .38 TPC, 9mm, .40 S&W)
    """
    df = carregar_csv()  # Usa cache!
    resultado = df[df["CALIBRE"] == calibre]
    return f"Encontrei {len(resultado)} armas calibre {calibre}"

@tool
def contar_armas_tipo(tipo: str) -> str:
    """Conta armas por tipo de ocorrência.
    
    Args:
        tipo: Tipo (ex: Apreensão, Roubo, Furto, Perda)
    """
    df = carregar_csv()  # Usa cache!
    resultado = df[df["TIPO_OCORRENCIA"] == tipo.upper()]
    return f"Encontrei {len(resultado)} ocorrências tipo {tipo}"

@tool
def contar_armas_combinado(marca: str, tipo: str) -> str:
    """Conta armas por marca E tipo simultaneamente.
    
    Args:
        marca: Marca da arma
        tipo: Tipo de ocorrência
    """
    df = carregar_csv()  # Usa cache!
    resultado = df[
        (df["MARCA_ARMA"] == marca.upper()) & 
        (df["TIPO_OCORRENCIA"] == tipo.upper())
    ]
    return f"Encontrei {len(resultado)} armas {marca} do tipo {tipo}"

# ============================================================
# AGENTE COM 4 TOOLS
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("AGENTE COM 4 TOOLS + CACHE")
    print("="*60)
    
    llm = OllamaLLM(model="llama3", temperature=0)
    
    agente = initialize_agent(
        tools=[
            contar_armas_marca,
            contar_armas_calibre,
            contar_armas_tipo,
            contar_armas_combinado
        ],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    # Testar 4 perguntas
    perguntas = [
        "Quantas armas Taurus?",
        "Quantas armas calibre .38 TPC?",
        "Quantas apreensões?",
        "Quantas Taurus foram roubadas?"
    ]
    
    for p in perguntas:
        print(f"\n{'='*60}\n❓ {p}\n{'='*60}")
        resposta = agente.invoke({"input": p})
        print(f"✅ {resposta['output']}\n")
    
    # Ver estatísticas do cache
    print("\n" + "="*60)
    print("ESTATÍSTICAS DO CACHE")
    print("="*60)
    print(carregar_csv.cache_info())
    print("\nhits = quantas vezes usou cache")
    print("misses = quantas vezes precisou calcular")
