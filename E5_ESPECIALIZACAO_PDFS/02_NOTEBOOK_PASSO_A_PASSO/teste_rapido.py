"""
TESTE RAPIDO: Verifique se o PDF grande aparece nos resultados

USO:
    python teste_rapido.py
    
    Vai testar 5 perguntas automaticamente e mostrar se o PDF
    'procedimento_operacional_padrao-pericia_criminal.pdf' aparece!
"""

import os
import sys
import numpy as np
from functools import lru_cache
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, CrossEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Fix encoding Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# =============================================================================
# CHUNKING HIBRIDO
# =============================================================================

def chunk_text_hibrido(texto, chunk_size=1000, overlap=150):
    chunks = []
    paragrafos = texto.split('\n\n')
    
    if len(paragrafos) < 5:
        paragrafos = texto.split('\n')
    
    if len(paragrafos) < 10:
        start = 0
        while start < len(texto):
            end = start + chunk_size
            chunk = texto[start:end]
            if len(chunk.strip()) > 50:
                chunks.append(chunk.strip())
            start = end - overlap
        return chunks
    
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


# =============================================================================
# CARREGAR DADOS
# =============================================================================

def carregar_tudo():
    """Carrega documentos .txt e PDFs"""
    todos_chunks = []
    
    # TXT
    caminhos_txt = [
        "../../E4_RAG_FAISS/01_DADOS/documentos_conceituais/",
        "../01_DADOS/documentos_conceituais/"
    ]
    
    for caminho_docs in caminhos_txt:
        if os.path.exists(caminho_docs):
            for arquivo in os.listdir(caminho_docs):
                if arquivo.endswith('.txt'):
                    with open(os.path.join(caminho_docs, arquivo), 'r', encoding='utf-8') as f:
                        chunks = chunk_text_hibrido(f.read(), chunk_size=500, overlap=50)
                        for i, chunk in enumerate(chunks):
                            todos_chunks.append({
                                'tipo': 'txt',
                                'arquivo': arquivo,
                                'chunk_id': i,
                                'texto': chunk
                            })
            break
    
    # PDFs
    caminhos_pdf = [
        "../01_DADOS/pdfs_pcdf/",
        "../../E5_ESPECIALIZACAO_PDFS/01_DADOS/pdfs_pcdf/"
    ]
    
    for caminho_pdfs in caminhos_pdf:
        if os.path.exists(caminho_pdfs):
            for file in os.listdir(caminho_pdfs):
                if file.endswith('.pdf'):
                    try:
                        reader = PdfReader(os.path.join(caminho_pdfs, file))
                        texto = "".join([page.extract_text() for page in reader.pages])
                        
                        if len(texto.strip()) > 100:
                            tamanho = len(texto)
                            chunk_size_pdf = 1000 if tamanho > 100000 else 500
                            overlap_pdf = 150 if tamanho > 100000 else 50
                            
                            chunks = chunk_text_hibrido(texto, chunk_size=chunk_size_pdf, overlap=overlap_pdf)
                            
                            for i, chunk in enumerate(chunks):
                                todos_chunks.append({
                                    'tipo': 'pdf',
                                    'arquivo': file,
                                    'chunk_id': i,
                                    'texto': chunk
                                })
                    except:
                        pass
            break
    
    return todos_chunks


# =============================================================================
# MAIN
# =============================================================================

print("="*80)
print("TESTE RAPIDO: Busca no PDF Grande")
print("="*80)

print("\n[1/4] Carregando documentos...")
todos_chunks = carregar_tudo()
print(f"      OK: {len(todos_chunks)} chunks")

# Contar chunks do PDF grande
pdf_chunks = [c for c in todos_chunks if 'procedimento_operacional' in c['arquivo']]
print(f"      OK: {len(pdf_chunks)} chunks do PDF 'procedimento_operacional_padrao-pericia_criminal.pdf'")

if len(pdf_chunks) == 0:
    print("\n[!] AVISO: PDF grande nao encontrado!")
    print("    Verifique se o arquivo existe em:")
    print("    - ../01_DADOS/pdfs_pcdf/")
    sys.exit(1)

print("\n[2/4] Carregando Sentence-BERT...")
embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
print("      OK")

print("\n[3/4] Gerando embeddings...")
textos_chunks = [chunk['texto'] for chunk in todos_chunks]
embeddings = embedding_model.encode(textos_chunks, show_progress_bar=True)
print(f"      OK: {embeddings.shape}")

print("\n[4/4] Carregando CrossEncoder...")
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
print("      OK")

print("\n" + "="*80)
print("TESTANDO PERGUNTAS")
print("="*80)

# Perguntas de teste
perguntas = [
    "O que e pericia criminal?",
    "Como fazer pericia em local de crime?",
    "Quais sao os procedimentos de coleta de vestigios?",
    "Como documentar uma cena de crime?",
    "O que e cadeia de custodia?"
]

pdf_apareceu_count = 0

for pergunta in perguntas:
    print(f"\n{'='*80}")
    print(f"PERGUNTA: {pergunta}")
    print('='*80)
    
    # Busca
    query_embedding = embedding_model.encode([pergunta])
    similaridades = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = similaridades.argsort()[-20:][::-1]
    
    candidatos = [todos_chunks[idx] for idx in top_indices if idx < len(todos_chunks)]
    
    pares = [[pergunta, chunk['texto']] for chunk in candidatos]
    scores = reranker.predict(pares)
    
    indices_ordenados = np.argsort(scores)[::-1]
    resultados = [(candidatos[i], float(scores[i])) for i in indices_ordenados[:5]]
    
    # Verificar se PDF grande apareceu
    pdf_apareceu = False
    
    for i, (chunk, score) in enumerate(resultados, 1):
        tipo = "[PDF]" if chunk['tipo'] == "pdf" else "[TXT]"
        
        # Marcar se e o PDF grande
        if 'procedimento_operacional' in chunk['arquivo']:
            tipo = "[PDF-GRANDE]"
            pdf_apareceu = True
        
        score_nivel = "[EXCELENTE]" if score > 5.0 else "[BOM]" if score > 2.0 else "[OK]" if score > 0 else "[FRACO]"
        
        print(f"\n{i}. {tipo} {chunk['arquivo']}")
        print(f"   Score: {score:.3f} {score_nivel}")
        print(f"   Trecho: {chunk['texto'][:150].replace(chr(10), ' ')}...")
    
    if pdf_apareceu:
        print("\n>>> [SUCESSO] PDF grande APARECEU nos resultados!")
        pdf_apareceu_count += 1
    else:
        print("\n>>> [FALHA] PDF grande NAO apareceu nos resultados")

print("\n" + "="*80)
print("RESUMO DO TESTE")
print("="*80)

print(f"\nTotal de perguntas: {len(perguntas)}")
print(f"PDF grande apareceu: {pdf_apareceu_count}/{len(perguntas)} vezes")

if pdf_apareceu_count == len(perguntas):
    print("\n[SUCESSO TOTAL] O PDF grande esta aparecendo em TODAS as buscas!")
elif pdf_apareceu_count > 0:
    print(f"\n[SUCESSO PARCIAL] O PDF grande aparece em algumas buscas ({pdf_apareceu_count}/{len(perguntas)})")
else:
    print("\n[FALHA] O PDF grande NAO esta aparecendo nos resultados")
    print("\nPOSSIVEIS CAUSAS:")
    print("  1. Chunking nao foi aplicado corretamente")
    print("  2. PDF nao foi carregado")
    print("  3. Perguntas nao sao especificas o suficiente")

print("\n" + "="*80)
