import json

# Analisar notebook
with open('E5_ESPECIALIZACAO_PDFS_V2.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

print(f"Total de celulas: {len(cells)}")
print(f"Markdown cells: {len([c for c in cells if c['cell_type']=='markdown'])}")
print(f"Code cells: {len([c for c in cells if c['cell_type']=='code'])}")

print("\n" + "="*80)
print("ESTRUTURA DO NOTEBOOK:")
print("="*80)

# Procurar duplicacoes
titulos_vistos = {}

for i, cell in enumerate(cells):
    if cell['cell_type'] == 'markdown' and cell['source']:
        primeira_linha = cell['source'][0].strip()
        
        # Capturar titulos principais
        if primeira_linha.startswith('# ') or primeira_linha.startswith('## PASSO'):
            titulo = primeira_linha[:60]
            
            if titulo in titulos_vistos:
                print(f"\n[DUPLICADO] Celula {i}:")
                print(f"  Titulo: {titulo}")
                print(f"  Primeira ocorrencia: celula {titulos_vistos[titulo]}")
            else:
                titulos_vistos[titulo] = i
                print(f"\n[OK] Celula {i}: {titulo}")

print("\n" + "="*80)
print(f"Total de titulos unicos: {len(titulos_vistos)}")
