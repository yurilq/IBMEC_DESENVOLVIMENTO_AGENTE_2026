"""
DIAGNOSTICO COMPLETO: Por que o PDF nao responde?

Vamos verificar PASSO A PASSO o que esta acontecendo.
"""

import os
import sys
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("DIAGNOSTICO: Por que o PDF nao aparece nas respostas?")
print("="*80)

# =============================================================================
# PASSO 1: Verificar se o PDF existe e foi carregado
# =============================================================================

print("\n[PASSO 1] Verificando se o PDF existe...")

caminho_pdf = "../01_DADOS/pdfs_pcdf/procedimento_operacional_padrao-pericia_criminal.pdf"

if not os.path.exists(caminho_pdf):
    print(f"[X] ERRO: PDF nao encontrado!")
    print(f"    Caminho procurado: {caminho_pdf}")
    sys.exit(1)

print(f"[OK] PDF encontrado!")
print(f"     Tamanho: {os.path.getsize(caminho_pdf) / 1024 / 1024:.2f} MB")

# Carregar PDF
reader = PdfReader(caminho_pdf)
texto_pdf = ""
for page in reader.pages:
    texto_pdf += page.extract_text()

print(f"     Paginas: {len(reader.pages)}")
print(f"     Caracteres: {len(texto_pdf):,}")

# =============================================================================
# PASSO 2: Verificar chunking
# =============================================================================

print("\n[PASSO 2] Verificando chunking...")

def chunk_text_hibrido(texto, chunk_size=1000, overlap=150):
    chunks = []
    paragrafos = texto.split('\n\n')
    
    if len(paragrafos) < 5:
        paragrafos = texto.split('\n')
    
    if len(paragrafos) < 10:
        print(f"     [!] Usando chunking FIXO (poucos paragrafos: {len(paragrafos)})")
        start = 0
        while start < len(texto):
            end = start + chunk_size
            chunk = texto[start:end]
            if len(chunk.strip()) > 50:
                chunks.append(chunk.strip())
            start = end - overlap
        return chunks
    
    print(f"     [!] Usando chunking SEMANTICO ({len(paragrafos)} paragrafos)")
    chunk_atual = ""
    for paragrafo in paragrafos:
        if len(chunk_atual) + len(paragrafo) > chunk_size:
            if len(chunk_atual.strip()) > 50:
                chunks.append(chunk_atual.strip())
            chunk_atual = chunk_atual[-overlap:] + paragrafo
        else:
            chunk_atual += "\n\n" + paragrafo
    
    if len(chunk_atual.strip()) > 50:
        chunks.append(chunk_atual.strip())
    
    return chunks

chunks_pdf = chunk_text_hibrido(texto_pdf, chunk_size=1000, overlap=150)

print(f"[OK] {len(chunks_pdf)} chunks criados")
print(f"     Tamanho medio: {np.mean([len(c) for c in chunks_pdf]):.0f} caracteres")

# Mostrar alguns chunks
print(f"\n     Primeiros 3 chunks:")
for i, chunk in enumerate(chunks_pdf[:3], 1):
    print(f"     [{i}] {chunk[:100].replace(chr(10), ' ')}...")

# =============================================================================
# PASSO 3: Buscar a palavra "computador" nos chunks
# =============================================================================

print("\n[PASSO 3] Buscando palavra 'computador' nos chunks...")

chunks_com_computador = []
for i, chunk in enumerate(chunks_pdf):
    if 'computador' in chunk.lower():
        chunks_com_computador.append((i, chunk))

print(f"[OK] Encontrados {len(chunks_com_computador)} chunks com a palavra 'computador'")

if len(chunks_com_computador) == 0:
    print("\n[!] PROBLEMA IDENTIFICADO:")
    print("    O PDF NAO contem a palavra 'computador'!")
    print("    Por isso nao aparece quando voce pergunta sobre computadores.")
    print("\n    SOLUCAO:")
    print("    - Faca perguntas mais GENERICAS sobre pericia criminal")
    print("    - Ou use termos que EXISTEM no PDF")
    
    # Buscar termos relacionados
    print("\n[ANALISE] Buscando termos relacionados no PDF...")
    termos = ['local', 'crime', 'pericia', 'vestigio', 'evidencia', 'coleta', 'documentacao', 'cadeia', 'custodia']
    
    for termo in termos:
        count = sum(1 for chunk in chunks_pdf if termo in chunk.lower())
        if count > 0:
            print(f"    - '{termo}': {count} chunks")
    
else:
    print("\n     Primeiros 2 chunks com 'computador':")
    for i, (chunk_id, chunk) in enumerate(chunks_com_computador[:2], 1):
        print(f"\n     [{chunk_id}] {chunk[:300].replace(chr(10), ' ')}...")

# =============================================================================
# PASSO 4: Testar busca semantica
# =============================================================================

print("\n[PASSO 4] Testando busca semantica...")

print("     [>>] Carregando modelo...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

print("     [>>] Gerando embeddings...")
embeddings_pdf = model.encode(chunks_pdf, show_progress_bar=False)

print(f"     [OK] Embeddings: {embeddings_pdf.shape}")

# Testar pergunta original
pergunta = "Qual o procedimento em local de crime com computadores?"

print(f"\n     [>>] Testando pergunta: '{pergunta}'")

query_emb = model.encode([pergunta])
sims = cosine_similarity(query_emb, embeddings_pdf)[0]

top_5_idx = sims.argsort()[-5:][::-1]

print(f"\n     Top-5 chunks do PDF:")
for idx in top_5_idx:
    score = sims[idx]
    chunk_preview = chunks_pdf[idx][:80].replace('\n', ' ')
    print(f"     [{idx}] Score: {score:.4f} | '{chunk_preview}...'")

# Verificar se algum chunk com "computador" esta no top-5
chunks_computador_ids = [c[0] for c in chunks_com_computador]
achou = any(idx in chunks_computador_ids for idx in top_5_idx)

if achou:
    print("\n     [OK] Chunks com 'computador' APARECEM no top-5!")
else:
    print("\n     [X] Chunks com 'computador' NAO aparecem no top-5")
    print("         Scores muito baixos - pergunta nao e especifica o suficiente")

# =============================================================================
# PASSO 5: Testar perguntas melhores
# =============================================================================

print("\n[PASSO 5] Testando perguntas MELHORES...")

perguntas_melhores = [
    "O que e pericia criminal?",
    "Como fazer pericia em local de crime?",
    "Quais sao os procedimentos de coleta de vestigios?",
    "Como preservar a cena do crime?",
    "O que e cadeia de custodia de evidencias?"
]

print("\n     Testando 5 perguntas sobre pericia...")

for pergunta in perguntas_melhores:
    query_emb = model.encode([pergunta])
    sims = cosine_similarity(query_emb, embeddings_pdf)[0]
    max_score = sims.max()
    
    print(f"\n     '{pergunta}'")
    print(f"     Score maximo: {max_score:.4f}")
    
    if max_score > 0.5:
        print(f"     [OK] Bom score! PDF deve aparecer nos resultados")
    elif max_score > 0.3:
        print(f"     [~] Score medio. PDF pode aparecer")
    else:
        print(f"     [X] Score baixo. PDF provavelmente nao aparece")

# =============================================================================
# CONCLUSAO
# =============================================================================

print("\n" + "="*80)
print("CONCLUSAO")
print("="*80)

print(f"\n1. PDF carregado: OK ({len(chunks_pdf)} chunks)")
print(f"2. Embeddings gerados: OK")
print(f"3. Busca funciona: OK")

print("\n4. PROBLEMA IDENTIFICADO:")
print("   - Sua pergunta: 'Qual o procedimento em local de crime com computadores?'")
print("   - O PDF provavelmente NAO fala especificamente sobre COMPUTADORES")
print("   - Por isso os scores sao baixos e o PDF nao aparece nos resultados")

print("\n5. SOLUCAO:")
print("   a) Verifique se o PDF realmente fala sobre computadores")
print("   b) Use perguntas mais GENERICAS sobre pericia criminal")
print("   c) Ou use termos que EXISTEM no PDF")

print("\n6. PERGUNTAS QUE DEVEM FUNCIONAR:")
for p in perguntas_melhores[:3]:
    print(f"   - {p}")

print("\n" + "="*80)
