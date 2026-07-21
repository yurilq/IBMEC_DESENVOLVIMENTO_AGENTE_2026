import pandas as pd
from functools import lru_cache  # ← NOVO!
from langchain_core.tools import tool

# NOVA FUNÇÃO: Carregar CSV com cache
@lru_cache(maxsize=1)
def carregar_csv():
    """Carrega CSV UMA VEZ e guarda em cache"""
    print("🔄 Carregando CSV...")  # ← Ver quando lê
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    print(f"✅ CSV carregado! {len(df)} linhas")
    return df

# REFATORAR todas as tools:

@tool
def contar_armas_marca(marca: str) -> str:
    """Conta armas por marca"""
    df = carregar_csv()  # ← USA CACHE!
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    return f"Encontrei {len(resultado)} armas {marca}"

@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta armas por calibre"""
    df = carregar_csv()  # ← USA CACHE!
    resultado = df[df["CALIBRE"] == calibre]
    return f"Encontrei {len(resultado)} armas calibre {calibre}"

@tool
def contar_armas_tipo(tipo: str) -> str:
    """Conta armas por tipo"""
    df = carregar_csv()  # ← USA CACHE!
    resultado = df[df["TIPO_OCORRENCIA"] == tipo.upper()]
    return f"Encontrei {len(resultado)} ocorrências tipo {tipo}"

@tool
def contar_armas_combinado(marca: str, tipo: str) -> str:
    """Conta armas por marca E tipo"""
    df = carregar_csv()  # ← USA CACHE!
    resultado = df[
        (df["MARCA_ARMA"] == marca.upper()) & 
        (df["TIPO_OCORRENCIA"] == tipo.upper())
    ]
    return f"Encontrei {len(resultado)} armas {marca} tipo {tipo}"