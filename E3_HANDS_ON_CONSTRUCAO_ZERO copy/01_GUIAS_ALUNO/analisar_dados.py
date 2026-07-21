# analisar_dados.py
# Script para entender o CSV

import pandas as pd

# Carregar primeiras 100 linhas para análise rápida
df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                 sep=";", encoding="latin1", nrows=100)


# PROBLEMA: Comparação exata (==) não funciona
df[df["MARCA_ARMA"] == "TAURUS"]  # ❌ Retorna 0

# SOLUÇÃO: Busca parcial (.contains)
df[df["MARCA_ARMA"].str.contains("TAURUS", case=False)]  # ✅ Encontra!



df[
    df["MARCA_ARMA"]
    .str.strip()          # 1. Remove espaços
    .str.contains("TAURUS", case=False, na=False)  # 2. Busca parcial
]

print(df["MARCA_ARMA"])