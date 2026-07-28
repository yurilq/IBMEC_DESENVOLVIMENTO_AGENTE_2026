import json

notebook_path = r"E:\documentos\ibmec\CODIGOS_AULA\E4_RAG_FAISS\02_NOTEBOOK_PASSO_A_PASSO\E4_RAG_FAISS.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

marcas = 0
marcas_arma = 0
calibres = 0
calibres_arma = 0

for cell in nb['cells']:
    source_str = str(cell.get('source', ''))
    if "'MARCA']" in source_str or '["MARCA"]' in source_str:
        marcas += 1
    if "'MARCA_ARMA']" in source_str or '["MARCA_ARMA"]' in source_str:
        marcas_arma += 1
    if "'CALIBRE']" in source_str or '["CALIBRE"]' in source_str:
        calibres += 1
    if "'CALIBRE_ARMA']" in source_str or '["CALIBRE_ARMA"]' in source_str:
        calibres_arma += 1

print("Validacao de correcoes:")
print(f"MARCA (errado): {marcas}")
print(f"MARCA_ARMA (correto): {marcas_arma}")
print(f"CALIBRE (errado): {calibres}")
print(f"CALIBRE_ARMA (correto): {calibres_arma}")

if marcas == 0 and calibres == 0:
    print("\nSUCESSO! Todas as colunas foram corrigidas!")
else:
    print("\nAVISO: Ainda existem colunas incorretas!")
