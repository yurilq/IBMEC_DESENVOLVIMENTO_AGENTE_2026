# tools_basicas.py (VERSÃO CORRIGIDA)

import pandas as pd

def contar_armas_marca(marca: str):
    """Conta quantas armas de uma marca específica"""
    
    # PASSO 1: Carregar CSV
    print(f"Buscando armas da marca: {marca}")
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", 
                     sep=";", 
                     encoding="latin1")
    
    # PASSO 2: Filtrar por marca (CORRIGIDO!)
    # ANTES (não funcionava):
    # resultado = df[df["MARCA_ARMA"] == marca.upper()]
    
    # DEPOIS (funciona!):
    resultado = df[
        df["MARCA_ARMA"]
        .str.strip()                           # Remove espaços extras
        .str.contains(marca, case=False, na=False)  # Busca parcial
    ]
    
    # PASSO 3: Contar linhas
    total = len(resultado)
    
    # PASSO 4: Retornar texto (melhorado)
    if total > 0:
        # Mostrar nome completo encontrado
        marca_completa = resultado.iloc[0]["MARCA_ARMA"].strip()
        return f"Encontrei {total} armas da marca '{marca_completa}'"
    else:
        return f"Nenhuma arma encontrada para '{marca}'"

# Teste
if __name__ == "__main__":
    print("="*60)
    print("TESTANDO FUNÇÃO (CORRIGIDA)")
    print("="*60)
    
    resultado = contar_armas_marca("Taurus")
    print(f"[OK] {resultado}")
    
    resultado = contar_armas_marca("Glock")
    print(f"[OK] {resultado}")
    
    print("="*60)