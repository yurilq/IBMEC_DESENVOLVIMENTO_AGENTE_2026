"""
Script de teste simples: Faca perguntas e veja se o PDF grande aparece nos resultados!

USO:
    python teste_perguntas_pdf.py

EXEMPLO:
    Digite sua pergunta: O que é perícia criminal?
    
    Resultados:
    1. procedimento_operacional_padrao-pericia_criminal.pdf (score: 8.234)
    2. tipos_armas.txt (score: 5.123)
    ...
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
# FUNCOES DE CHUNKING (COPIADAS DO PATCH)
# =============================================================================

def chunk_text_hibrido(texto, chunk_size=1000, overlap=150):
    """Chunking hibrido: tenta semantico, se falhar usa fixo."""
    chunks = []
    
    # Tentar dividir por paragrafos duplos
    paragrafos = texto.split('\n\n')
    
    # Se tiver poucos paragrafos, tentar quebra simples
    if len(paragrafos) < 5:
        paragrafos = texto.split('\n')
    
    # Se ainda tiver poucos, usar chunking FIXO
    if len(paragrafos) < 10:
        # Chunking fixo para PDFs problematicos
        start = 0
        while start < len(texto):
            end = start + chunk_size
            chunk = texto[start:end]
            
            if len(chunk.strip()) > 50:
                chunks.append(chunk.strip())
            
            start = end - overlap
        
        return chunks
    
    # Chunking semantico normal (para PDFs bem formatados)
    chunk_atual = ""
    
    for paragrafo in paragrafos:
        # Se adicionar este paragrafo ultrapassar o limite
        if len(chunk_atual) + len(paragrafo) > chunk_size:
            # Salvar chunk atual
            if len(chunk_atual.strip()) > 50:
                chunks.append(chunk_atual.strip())
            
            # Iniciar novo chunk (com overlap)
            chunk_atual = chunk_atual[-overlap:] + paragrafo
        else:
            chunk_atual += "\n\n" + paragrafo
    
    # Adicionar ultimo chunk
    if len(chunk_atual.strip()) > 50:
        chunks.append(chunk_atual.strip())
    
    return chunks


# =============================================================================
# CARREGAR DOCUMENTOS
# =============================================================================

@lru_cache(maxsize=1)
def carregar_documentos_txt():
    """Carrega documentos .txt"""
    caminhos_possiveis = [
        "../../E4_RAG_FAISS/01_DADOS/documentos_conceituais/",
        "../01_DADOS/documentos_conceituais/"
    ]
    
    caminho_docs = None
    for c in caminhos_possiveis:
        if os.path.exists(c):
            caminho_docs = c
            break
    
    if not caminho_docs:
        return []
    
    documentos = []
    for arquivo in os.listdir(caminho_docs):
        if arquivo.endswith('.txt'):
            caminho_completo = os.path.join(caminho_docs, arquivo)
            with open(caminho_completo, 'r', encoding='utf-8') as f:
                documentos.append({
                    "arquivo": arquivo,
                    "conteudo": f.read()
                })
    
    return documentos


@lru_cache(maxsize=1)
def carregar_pdfs():
    """Carrega PDFs"""
    caminhos_possiveis = [
        "../01_DADOS/pdfs_pcdf/",
        "../../E5_ESPECIALIZACAO_PDFS/01_DADOS/pdfs_pcdf/"
    ]
    
    caminho_pdfs = None
    for c in caminhos_possiveis:
        if os.path.exists(c):
            caminho_pdfs = c
            break
    
    if not caminho_pdfs:
        return []
    
    pdfs = []
    
    for root, dirs, files in os.walk(caminho_pdfs):
        for file in files:
            if file.endswith('.pdf'):
                caminho = os.path.join(root, file)
                try:
                    reader = PdfReader(caminho)
                    texto = ""
                    for page in reader.pages:
                        texto += page.extract_text()
                    
                    if len(texto.strip()) > 100:
                        pdfs.append({
                            'arquivo': file,
                            'conteudo': texto,
                            'num_paginas': len(reader.pages)
                        })
                except:
                    pass
    
    return pdfs


def preparar_todos_chunks():
    """Prepara chunks de TODOS os documentos (.txt + PDFs)."""
    todos_chunks = []
    
    docs_txt = carregar_documentos_txt()
    pdfs = carregar_pdfs()
    
    # Processar documentos .txt
    print("[>>] Processando documentos .txt...")
    for doc in docs_txt:
        chunks = chunk_text_hibrido(doc['conteudo'], chunk_size=500, overlap=50)
        for i, chunk in enumerate(chunks):
            todos_chunks.append({
                'tipo': 'txt',
                'arquivo': doc['arquivo'],
                'chunk_id': i,
                'texto': chunk
            })
    
    print(f"[OK] {len([c for c in todos_chunks if c['tipo'] == 'txt'])} chunks de .txt")
    
    # Processar PDFs
    if pdfs:
        print("[>>] Processando PDFs...")
        for pdf in pdfs:
            tamanho = len(pdf['conteudo'])
            
            if tamanho > 100000:  # PDF grande
                print(f"     [!] {pdf['arquivo']}: PDF GRANDE ({tamanho:,} chars)")
                print(f"         Usando chunk_size=1000, overlap=150")
                chunk_size_pdf = 1000
                overlap_pdf = 150
            else:
                chunk_size_pdf = 500
                overlap_pdf = 50
            
            chunks = chunk_text_hibrido(
                pdf['conteudo'], 
                chunk_size=chunk_size_pdf, 
                overlap=overlap_pdf
            )
            
            print(f"     [OK] {pdf['arquivo']}: {len(chunks)} chunks criados")
            
            for i, chunk in enumerate(chunks):
                todos_chunks.append({
                    'tipo': 'pdf',
                    'arquivo': pdf['arquivo'],
                    'chunk_id': i,
                    'texto': chunk
                })
        
        print(f"[OK] {len([c for c in todos_chunks if c['tipo'] == 'pdf'])} chunks de PDFs")
    
    print(f"\n[OK] Total: {len(todos_chunks)} chunks preparados!")
    
    return todos_chunks


# =============================================================================
# BUSCA COM RERANKING
# =============================================================================

def buscar_com_reranking(pergunta, todos_chunks, embeddings, embedding_model, reranker, k_inicial=20, k_final=5):
    """Busca com pipeline de 2 estagios: NumPy + Reranking."""
    
    # Estagio 1: Busca inicial com NumPy
    query_embedding = embedding_model.encode([pergunta])
    similaridades = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = similaridades.argsort()[-k_inicial:][::-1]
    
    # Coletar candidatos
    candidatos = []
    for idx in top_indices:
        if idx < len(todos_chunks):
            candidatos.append(todos_chunks[idx])
    
    # Estagio 2: Reranking com CrossEncoder
    pares = [[pergunta, chunk['texto']] for chunk in candidatos]
    scores = reranker.predict(pares)
    
    # Ordenar por score
    indices_ordenados = np.argsort(scores)[::-1]
    
    # Retornar top-K final
    resultados = []
    for i in indices_ordenados[:k_final]:
        chunk = candidatos[i]
        score = float(scores[i])
        resultados.append((chunk, score))
    
    return resultados


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("="*80)
    print("TESTE: Busca no PDF Grande")
    print("="*80)
    print("\n[>>] Carregando documentos e gerando embeddings...")
    print("    (Primeira vez pode demorar ~2-3 minutos)\n")
    
    # Preparar chunks
    todos_chunks = preparar_todos_chunks()
    
    # Carregar modelos
    print("\n[>>] Carregando Sentence-BERT...")
    embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    print("[>>] Carregando CrossEncoder...")
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    # Gerar embeddings
    print("\n[>>] Gerando embeddings...")
    textos_chunks = [chunk['texto'] for chunk in todos_chunks]
    embeddings = embedding_model.encode(textos_chunks, show_progress_bar=True)
    
    print(f"\n[OK] Sistema pronto!")
    print(f"     Total de chunks: {len(todos_chunks)}")
    print(f"     Embeddings: {embeddings.shape}")
    
    # Loop de perguntas
    print("\n" + "="*80)
    print("TESTE INTERATIVO")
    print("="*80)
    print("\nDigite suas perguntas (ou 'sair' para encerrar)")
    print("\nSugestoes:")
    print("  - O que e pericia criminal?")
    print("  - Como fazer pericia em local de crime?")
    print("  - Quais sao os procedimentos de coleta de vestigios?")
    print("  - Como documentar uma cena de crime?")
    print("  - O que e cadeia de custodia?")
    print("  - O que e calibre de arma?")
    print("  - Como funciona o SINARM?")
    print("\n" + "-"*80)
    
    while True:
        try:
            pergunta = input("\nDigite sua pergunta: ").strip()
            
            if not pergunta or pergunta.lower() == 'sair':
                print("\n[OK] Encerrando...")
                break
            
            print("\n[>>] Buscando...")
            resultados = buscar_com_reranking(
                pergunta, 
                todos_chunks, 
                embeddings, 
                embedding_model, 
                reranker,
                k_inicial=20, 
                k_final=5
            )
            
            print("\n" + "="*80)
            print(f"RESULTADOS: '{pergunta}'")
            print("="*80)
            
            if not resultados:
                print("\n[!] Nenhum resultado encontrado")
            else:
                for i, (chunk, score) in enumerate(resultados, 1):
                    tipo_emoji = "[PDF]" if chunk['tipo'] == "pdf" else "[TXT]"
                    
                    # Indicador de score
                    if score > 5.0:
                        score_emoji = "[EXCELENTE]"
                    elif score > 2.0:
                        score_emoji = "[BOM]"
                    elif score > 0:
                        score_emoji = "[OK]"
                    else:
                        score_emoji = "[FRACO]"
                    
                    print(f"\n{i}. {tipo_emoji} {chunk['arquivo']}")
                    print(f"   Score: {score:.3f} {score_emoji}")
                    print(f"   Chunk ID: {chunk['chunk_id']}")
                    print(f"   Preview: {chunk['texto'][:200].replace(chr(10), ' ')}...")
            
            print("\n" + "-"*80)
            
        except KeyboardInterrupt:
            print("\n\n[OK] Encerrando...")
            break
        except Exception as e:
            print(f"\n[ERRO] {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
