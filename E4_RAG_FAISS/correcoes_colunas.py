"""
Script para corrigir nomes de colunas no notebook E4
"""

# Mapeamento de colunas incorretas -> corretas
CORRECOES = {
    "'MARCA'": "'MARCA_ARMA'",
    "'CALIBRE'": "'CALIBRE_ARMA'",
    "'TIPO_OCORRENCIA'": "'TIPO_OCORRENCIA'",  # Esta está correta
    "['MARCA']": "['MARCA_ARMA']",
    "['CALIBRE']": "['CALIBRE_ARMA']",
}

print("Correções necessárias:")
print("=" * 60)
for errado, correto in CORRECOES.items():
    print(f"{errado:20} -> {correto}")
print("=" * 60)

print("\nColunas corretas do CSV:")
print("- ANO_OCORRENCIA")
print("- MES_OCORRENCIA")
print("- UF")
print("- MUNICIPIO")
print("- ESPECIE_ARMA")
print("- MARCA_ARMA  ⭐")
print("- CALIBRE_ARMA  ⭐")
print("- TIPO_OCORRENCIA")
print("- MAIS_1000_MIL_HAB")
print("- TOTAL")
