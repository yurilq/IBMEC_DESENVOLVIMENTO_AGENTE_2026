# analisar_dados.py
# Script para entender o CSV

import pandas as pd

# Carregar primeiras 100 linhas para análise rápida
df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                 sep=";", encoding="latin1", nrows=100)

print("="*60)
print("ANÁLISE DO CSV")
print("="*60)

# 1. Ver primeiras linhas
print("\n1. PRIMEIRAS 3 LINHAS:")
print(df.head(3))

# 2. Ver marcas únicas
print("\n2. MARCAS ÚNICAS (primeiras 10):")
marcas = df["MARCA_ARMA"].unique()[:10]
for i, marca in enumerate(marcas, 1):
    # repr() mostra caracteres invisíveis (espaços)
    print(f"{i}. {repr(marca)} (comprimento: {len(marca)} caracteres)")

# 3. Testar diferentes métodos de busca
print("\n3. TESTANDO BUSCA 'TAURUS':")
print(f"   Método 1 (==): {len(df[df['MARCA_ARMA'] == 'TAURUS'])} resultados")
print(f"   Método 2 (contains): {len(df[df['MARCA_ARMA'].str.contains('TAURUS', case=False, na=False)])} resultados")

# 4. Mostrar exemplo de marca encontrada
taurus = df[df["MARCA_ARMA"].str.contains("TAURUS", case=False, na=False)]
if len(taurus) > 0:
    print(f"\n4. EXEMPLO DE MARCA ENCONTRADA:")
    print(f"   {repr(taurus.iloc[0]['MARCA_ARMA'])}")

# ANTES (70 caracteres com espaços)
marca_suja = "TAURUS ARMAS S.A.                                                     "
print(f"Comprimento: {len(marca_suja)}")  # 70

# DEPOIS (limpa)
marca_limpa = marca_suja.strip()
print(f"Comprimento: {len(marca_limpa)}")  # 17
print(f"Limpa: '{marca_limpa}'")  # 'TAURUS ARMAS S.A.'    