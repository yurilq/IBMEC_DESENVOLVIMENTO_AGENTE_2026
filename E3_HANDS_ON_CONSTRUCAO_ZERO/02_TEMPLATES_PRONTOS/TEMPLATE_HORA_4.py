# TEMPLATE_HORA_4.py
# Código de referência para Parte 4: 4 Tools + Cache
# Use se ficar travado na Parte 4
#
# ⚠️ ATUALIZADO PARA LANGCHAIN 1.3+
# Usa agente MANUAL (sem initialize_agent que foi removido)

import pandas as pd
from functools import lru_cache
from langchain_core.tools import tool
from langchain_ollama import OllamaLLM

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
        calibre: Calibre da arma (ex: .38, 9mm, .40)
    """
    df = carregar_csv()  # Usa cache!
    # Limpar espaços e usar contains (mais robusto)
    df["CALIBRE_ARMA"] = df["CALIBRE_ARMA"].str.strip()
    resultado = df[df["CALIBRE_ARMA"].str.contains(calibre, case=False, na=False)]
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
# AGENTE MANUAL (LangChain 1.3+)
# ============================================================

def agente_manual(pergunta: str):
    """Agente manual simples que seleciona e executa tools"""
    
    print(f"\n[PERGUNTA] {pergunta}")
    print("-"*60)
    
    pergunta_lower = pergunta.lower()
    
    # Detectar marca
    marcas = ["taurus", "glock", "rossi", "beretta"]
    marca_encontrada = None
    for marca in marcas:
        if marca in pergunta_lower:
            marca_encontrada = marca.capitalize()
            break
    
    # Detectar calibre
    calibres = [".38", "9mm", ".40", ".380"]
    calibre_encontrado = None
    for calibre in calibres:
        if calibre in pergunta_lower:
            calibre_encontrado = calibre
            break
    
    # Detectar tipo
    tipos = {"apreens": "Apreens", "roubo": "Roubo", "furto": "Furto"}
    tipo_encontrado = None
    for palavra, tipo in tipos.items():
        if palavra in pergunta_lower:
            tipo_encontrado = tipo
            break
    
    # Selecionar tool e executar
    if marca_encontrada and tipo_encontrado:
        print(f"[TOOL] contar_armas_combinado(marca={marca_encontrada}, tipo={tipo_encontrado})")
        return contar_armas_combinado.func(marca_encontrada, tipo_encontrado)
    elif marca_encontrada:
        print(f"[TOOL] contar_armas_marca(marca={marca_encontrada})")
        return contar_armas_marca.func(marca_encontrada)
    elif calibre_encontrado:
        print(f"[TOOL] contar_armas_calibre(calibre={calibre_encontrado})")
        return contar_armas_calibre.func(calibre_encontrado)
    elif tipo_encontrado:
        print(f"[TOOL] contar_armas_tipo(tipo={tipo_encontrado})")
        return contar_armas_tipo.func(tipo_encontrado)
    else:
        return "Não consegui identificar sobre o que você quer."


# ============================================================
# TESTE
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("AGENTE COM 4 TOOLS + CACHE (LangChain 1.3+)")
    print("="*60)
    
    # Testar 4 perguntas
    perguntas = [
        "Quantas armas Taurus?",
        "Quantas armas calibre .38?",
        "Quantas apreensões?",
        "Quantas Taurus foram roubadas?"
    ]
    
    for p in perguntas:
        print(f"\n{'='*60}")
        resposta = agente_manual(p)
        print(f"[RESPOSTA] {resposta}")
    
    # Ver estatísticas do cache
    print("\n" + "="*60)
    print("ESTATÍSTICAS DO CACHE")
    print("="*60)
    print(carregar_csv.cache_info())
    print("\nhits = quantas vezes usou cache")
    print("misses = quantas vezes precisou calcular")
