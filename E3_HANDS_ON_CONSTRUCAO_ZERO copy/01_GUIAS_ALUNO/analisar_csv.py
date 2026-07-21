# analisar_csv.py
# Script para entender a estrutura do CSV

import pandas as pd
import os

# Path correto
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "DADOS_SINARM", "OCORRENCIAS_2026.csv")

print("="*60)
print("ANALISANDO CSV")
print("="*60)

# Tentar diferentes encodings
for encoding in ["latin1", "utf-8", "iso-8859-1", "cp1252"]:
    try:
        print(f"\nTentando encoding: {encoding}")
        df = pd.read_csv(csv_path, sep=";", encoding=encoding, nrows=100)
        print(f"SUCESSO! {len(df)} linhas lidas")
        break
    except Exception as e:
        print(f"FALHOU: {e}")
        continue

# Ver estrutura
print("\n" + "="*60)
print("COLUNAS DO CSV")
print("="*60)
print(df.columns.tolist())

# Ver primeiras linhas
print("\n" + "="*60)
print("PRIMEIRAS 3 LINHAS")
print("="*60)
print(df.head(3))

# Analisar coluna MARCA_ARMA
print("\n" + "="*60)
print("VALORES ÚNICOS DE MARCA_ARMA (primeiras 20)")
print("="*60)
marcas = df["MARCA_ARMA"].unique()[:20]
for i, marca in enumerate(marcas, 1):
    # Mostrar com repr() para ver espaços
    print(f"{i}. [{marca!r}] (len={len(marca)})")

# Verificar se tem Taurus
print("\n" + "="*60)
print("BUSCANDO 'TAURUS'")
print("="*60)
taurus_com_espacos = df[df["MARCA_ARMA"].str.contains("TAURUS", case=False, na=False)]
print(f"Linhas com 'TAURUS' (case-insensitive): {len(taurus_com_espacos)}")

# Verificar se tem Glock
print("\n" + "="*60)
print("BUSCANDO 'GLOCK'")
print("="*60)
glock = df[df["MARCA_ARMA"].str.contains("GLOCK", case=False, na=False)]
print(f"Linhas com 'GLOCK' (case-insensitive): {len(glock)}")
if len(glock) > 0:
    print(f"Exemplo: [{glock.iloc[0]['MARCA_ARMA']!r}]")

# Total de linhas
print("\n" + "="*60)
print(f"TOTAL DE LINHAS NO CSV (primeiras 100): {len(df)}")
print("="*60)
