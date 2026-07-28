"""
Script para corrigir nomes de colunas no notebook E4_RAG_FAISS.ipynb
"""

import json
import re

# Caminho do notebook
notebook_path = r"E:\documentos\ibmec\CODIGOS_AULA\E4_RAG_FAISS\02_NOTEBOOK_PASSO_A_PASSO\E4_RAG_FAISS.ipynb"

# Carregar notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Contador de correções
correcoes = 0

# Percorrer todas as células
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        
        # Se source é lista de strings
        if isinstance(source, list):
            for i, line in enumerate(source):
                original = line
                
                # Correções
                line = line.replace("['MARCA']", "['MARCA_ARMA']")
                line = line.replace('["MARCA"]', '["MARCA_ARMA"]')
                line = line.replace("df['MARCA']", "df['MARCA_ARMA']")
                line = line.replace('df["MARCA"]', 'df["MARCA_ARMA"]')
                
                line = line.replace("['CALIBRE']", "['CALIBRE_ARMA']")
                line = line.replace('["CALIBRE"]', '["CALIBRE_ARMA"]')
                line = line.replace("df['CALIBRE']", "df['CALIBRE_ARMA']")
                line = line.replace('df["CALIBRE"]', 'df["CALIBRE_ARMA"]')
                
                if original != line:
                    source[i] = line
                    correcoes += 1
                    print(f"Corrigido: {original.strip()[:50]}...")
        
        # Se source é string única
        elif isinstance(source, str):
            original = source
            
            source = source.replace("['MARCA']", "['MARCA_ARMA']")
            source = source.replace('["MARCA"]', '["MARCA_ARMA"]')
            source = source.replace("df['MARCA']", "df['MARCA_ARMA']")
            source = source.replace('df["MARCA"]', 'df["MARCA_ARMA"]')
            
            source = source.replace("['CALIBRE']", "['CALIBRE_ARMA']")
            source = source.replace('["CALIBRE"]', '["CALIBRE_ARMA"]')
            source = source.replace("df['CALIBRE']", "df['CALIBRE_ARMA']")
            source = source.replace('df["CALIBRE"]', 'df["CALIBRE_ARMA"]')
            
            if original != source:
                cell['source'] = source
                correcoes += 1
                print(f"Corrigido: {original[:50]}...")

# Salvar notebook corrigido
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"\n✅ Total de correções: {correcoes}")
print(f"✅ Notebook salvo: {notebook_path}")
