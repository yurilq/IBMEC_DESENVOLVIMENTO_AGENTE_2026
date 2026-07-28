# tools_basicas_v2.py
# Funcoes para consultar SINARM COM @tool (PARTE 4)

import pandas as pd
from functools import lru_cache
from langchain_core.tools import tool
from pathlib import Path

# FUNCAO COM CACHE para carregar CSV
@lru_cache(maxsize=1)
def carregar_csv():
    """Carrega CSV UMA VEZ e guarda em cache"""
    print("[CACHE] Carregando CSV...")
    
    # Caminho local para dados SINARM
    # Script está em: 03_CODIGOS_PRONTOS/scripts_agente/
    # Dados estão em: 03_CODIGOS_PRONTOS/DADOS_SINARM/
    CAMINHO_DADOS = Path(__file__).parent.parent / "DADOS_SINARM"
    
    # Verificar se existe
    if not CAMINHO_DADOS.exists():
        raise FileNotFoundError(f"Pasta DADOS_SINARM não encontrada em: {CAMINHO_DADOS}")
    
    csv_path = CAMINHO_DADOS / "OCORRENCIAS" / "OCORRENCIAS_2026.csv"
    
    # Tentar múltiplos encodings (compatibilidade Windows/Linux/Mac)
    encodings = ['latin1', 'utf-8', 'cp1252', 'iso-8859-1']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_path, sep=";", encoding=encoding)
            print(f"[OK] CSV carregado com encoding '{encoding}' - {len(df)} linhas")
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if df is None:
        raise ValueError(f"Não foi possível ler o CSV com nenhum encoding: {encodings}")
    
    # Limpar espacos em todas as colunas relevantes
    df["MARCA_ARMA"] = df["MARCA_ARMA"].str.strip()
    df["CALIBRE_ARMA"] = df["CALIBRE_ARMA"].str.strip()
    df["TIPO_OCORRENCIA"] = df["TIPO_OCORRENCIA"].str.strip()
    
    return df


# TOOL 1: Contar por marca
@tool
def contar_armas_marca(marca: str) -> str:
    """Conta quantas armas de uma marca especifica estao registradas.
    
    Args:
        marca: Nome da marca (ex: Taurus, Glock, Rossi, Beretta)
    
    Returns:
        Total de armas encontradas dessa marca
    """
    df = carregar_csv()  # <- USA CACHE!
    resultado = df[df["MARCA_ARMA"].str.contains(marca.upper(), case=False, na=False)]
    total = len(resultado)
    
    if total > 0:
        marca_real = resultado["MARCA_ARMA"].iloc[0]
        return f"Encontrei {total} armas da marca '{marca_real}'"
    else:
        return f"Nao encontrei armas da marca '{marca}'"


# TOOL 2: Contar por calibre
@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta quantas armas de um calibre especifico.
    
    Args:
        calibre: Calibre da arma (ex: .38, 9mm, .40, .380)
    
    Returns:
        Total de armas do calibre especificado
    """
    df = carregar_csv()  # <- USA CACHE!
    resultado = df[df["CALIBRE_ARMA"].str.contains(calibre, case=False, na=False)]
    total = len(resultado)
    
    if total > 0:
        calibre_real = resultado["CALIBRE_ARMA"].iloc[0]
        return f"Encontrei {total} armas calibre '{calibre_real}'"
    else:
        return f"Nao encontrei armas calibre '{calibre}'"


# TOOL 3: Contar por tipo de ocorrencia
@tool
def contar_armas_tipo(tipo: str) -> str:
    """Conta armas por tipo de ocorrencia.
    
    Args:
        tipo: Tipo de ocorrencia (ex: Apreens, Roubo, Furto, Perda)
    
    Returns:
        Total de ocorrencias do tipo especificado
    """
    df = carregar_csv()  # <- USA CACHE!
    resultado = df[df["TIPO_OCORRENCIA"].str.contains(tipo.upper(), case=False, na=False)]
    total = len(resultado)
    
    if total > 0:
        tipo_real = resultado["TIPO_OCORRENCIA"].iloc[0]
        return f"Encontrei {total} ocorrencias tipo '{tipo_real}'"
    else:
        return f"Nao encontrei ocorrencias tipo '{tipo}'"


# TOOL 4: Contar combinado (marca + tipo)
@tool
def contar_armas_combinado(marca: str, tipo: str) -> str:
    """Conta armas por marca E tipo de ocorrencia simultaneamente.
    
    Args:
        marca: Marca da arma
        tipo: Tipo de ocorrencia
    
    Returns:
        Total de armas que atendem ambos criterios
    """
    df = carregar_csv()  # <- USA CACHE!
    resultado = df[
        (df["MARCA_ARMA"].str.contains(marca.upper(), case=False, na=False)) & 
        (df["TIPO_OCORRENCIA"].str.contains(tipo.upper(), case=False, na=False))
    ]
    total = len(resultado)
    
    if total > 0:
        return f"Encontrei {total} armas {marca} do tipo {tipo}"
    else:
        return f"Nao encontrei armas {marca} do tipo {tipo}"


# Teste direto
if __name__ == "__main__":
    print("="*60)
    print("TESTANDO 4 TOOLS COM @tool + CACHE")
    print("="*60)
    
    print("\n[TESTE 1] Contar armas Taurus:")
    resultado = contar_armas_marca.func("Taurus")
    print(f"   {resultado}")
    
    print("\n[TESTE 2] Contar armas calibre .38:")
    resultado = contar_armas_calibre.func(".38")
    print(f"   {resultado}")
    
    print("\n[TESTE 3] Contar apreensoes:")
    resultado = contar_armas_tipo.func("Apreens")
    print(f"   {resultado}")
    
    print("\n[TESTE 4] Contar Taurus roubadas:")
    resultado = contar_armas_combinado.func("Taurus", "Roubo")
    print(f"   {resultado}")
    
    print("\n" + "="*60)
    print("OBSERVE: 'Carregando CSV...' apareceu SO UMA VEZ!")
    print("Cache funcionou!")
    print("="*60)