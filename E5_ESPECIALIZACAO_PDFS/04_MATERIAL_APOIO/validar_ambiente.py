"""
Script de Validação do Notebook E5
Verifica se todas as dependências e arquivos necessários estão presentes
"""
import sys
import os
import json

print("="*60)
print("VALIDACAO DO NOTEBOOK E5")
print("="*60)

# 1. Verificar Python
print("\n[1/6] Verificando Python...")
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 8:
    print(f"  OK: Python {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    print(f"  ERRO: Python {python_version.major}.{python_version.minor} (necessario 3.8+)")

# 2. Verificar dependências
print("\n[2/6] Verificando dependencias...")
dependencias = {
    'pandas': 'pandas',
    'numpy': 'numpy',
    'sklearn': 'scikit-learn',
    'langchain_core': 'langchain-core',
    'sentence_transformers': 'sentence-transformers',
    'faiss': 'faiss-cpu',
    'PyPDF2': 'PyPDF2',
    'transformers': 'transformers',
    'torch': 'torch',
}

deps_ok = []
deps_faltando = []

for modulo, pacote in dependencias.items():
    try:
        __import__(modulo)
        deps_ok.append(pacote)
        print(f"  OK: {pacote}")
    except ImportError:
        deps_faltando.append(pacote)
        print(f"  FALTANDO: {pacote}")

# 3. Verificar notebook
print("\n[3/6] Verificando notebook...")
notebook_path = r'E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\02_NOTEBOOK_PASSO_A_PASSO\E5_ESPECIALIZACAO_PDFS.ipynb'

if os.path.exists(notebook_path):
    print(f"  OK: Notebook encontrado")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    print(f"  OK: {len(notebook['cells'])} celulas")
else:
    print(f"  ERRO: Notebook nao encontrado")

# 4. Verificar dados
print("\n[4/6] Verificando dados...")

# CSV
csv_path = r'E:\documentos\ibmec\CODIGOS_AULA\E4_RAG_FAISS\01_DADOS\DADOS_SINARM\OCORRENCIAS\OCORRENCIAS_2026.csv'
if os.path.exists(csv_path):
    print(f"  OK: CSV SINARM encontrado")
else:
    print(f"  AVISO: CSV SINARM nao encontrado")

# Documentos .txt
docs_path = r'E:\documentos\ibmec\CODIGOS_AULA\E4_RAG_FAISS\01_DADOS\documentos_conceituais'
if os.path.exists(docs_path):
    txt_files = [f for f in os.listdir(docs_path) if f.endswith('.txt')]
    print(f"  OK: {len(txt_files)} documentos .txt encontrados")
else:
    print(f"  AVISO: Pasta de documentos .txt nao encontrada")

# PDFs
pdfs_path = r'E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\01_DADOS\pdfs_pcdf'
if os.path.exists(pdfs_path):
    pdf_files = [f for f in os.listdir(pdfs_path) if f.endswith('.pdf')]
    print(f"  OK: {len(pdf_files)} PDFs encontrados")
    for pdf in pdf_files:
        print(f"     - {pdf}")
else:
    print(f"  AVISO: Pasta de PDFs nao encontrada")

# 5. Verificar estrutura
print("\n[5/6] Verificando estrutura de pastas...")
pastas_necessarias = [
    r'E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\01_DADOS',
    r'E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\02_NOTEBOOK_PASSO_A_PASSO',
    r'E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\03_AGENTE_CONSOLIDADO',
    r'E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\04_MATERIAL_APOIO',
]

for pasta in pastas_necessarias:
    if os.path.exists(pasta):
        print(f"  OK: {os.path.basename(pasta)}")
    else:
        print(f"  ERRO: {os.path.basename(pasta)} nao encontrada")

# 6. Resumo
print("\n[6/6] Resumo...")
print("="*60)

total_deps = len(dependencias)
print(f"\nDependencias: {len(deps_ok)}/{total_deps} OK")
if deps_faltando:
    print(f"\nFaltando instalar:")
    for dep in deps_faltando:
        print(f"  pip install {dep}")

print(f"\nDados:")
print(f"  - CSV SINARM: {'OK' if os.path.exists(csv_path) else 'FALTANDO'}")
print(f"  - Documentos .txt: {'OK' if os.path.exists(docs_path) else 'FALTANDO'}")
print(f"  - PDFs: {'OK' if os.path.exists(pdfs_path) else 'FALTANDO'}")

print("\n" + "="*60)

if len(deps_faltando) == 0:
    print("STATUS: PRONTO PARA EXECUTAR!")
    print("\nProximos passos:")
    print("  1. Abrir Jupyter: jupyter notebook")
    print("  2. Abrir E5_ESPECIALIZACAO_PDFS.ipynb")
    print("  3. Executar celulas sequencialmente")
else:
    print("STATUS: DEPENDENCIAS FALTANDO")
    print("\nInstale as dependencias primeiro:")
    print("  pip install " + " ".join(deps_faltando))

print("="*60)
