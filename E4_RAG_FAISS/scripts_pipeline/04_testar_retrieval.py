"""
PASSO 4: TESTAR RETRIEVAL
Testa busca de documentos relevantes com queries reais
"""

import json
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer

print("="*70)
print("PASSO 4: TESTANDO RETRIEVAL (BUSCA)")
print("="*70)

# ===== CARREGAR RECURSOS =====

OUTPUT_DIR = Path(__file__).parent.parent / "03_outputs"

print("\n[PASTA] Carregando recursos...")

# Carregar índice FAISS
index = faiss.read_index(str(OUTPUT_DIR / "faiss_index.bin"))
print(f"[OK] Índice FAISS carregado ({index.ntotal:,} vetores)")

# Carregar documentos
with open(OUTPUT_DIR / "documentos.json", 'r', encoding='utf-8') as f:
    documentos = json.load(f)
print(f"[OK] {len(documentos):,} documentos carregados")

# Carregar metadados
with open(OUTPUT_DIR / "metadados.json", 'r', encoding='utf-8') as f:
    metadados = json.load(f)
print(f"[OK] {len(metadados):,} metadados carregados")

# Carregar modelo de embeddings
print("\n[INFO] Carregando modelo de embeddings...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("[OK] Modelo carregado\n")

# ===== FUNÇÃO DE BUSCA =====

def buscar_documentos(query: str, k: int = 5):
    """
    Busca top-k documentos mais relevantes para a query
    
    Args:
        query: Texto da pergunta/busca
        k: Número de documentos a retornar
    
    Returns:
        Lista de dicionários com resultados
    """
    # Gerar embedding da query
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding, dtype='float32')
    
    # Buscar no índice FAISS
    distances, indices = index.search(query_embedding, k)
    
    # Montar resultados
    resultados = []
    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        resultados.append({
            'rank': i + 1,
            'indice': int(idx),
            'distancia': float(dist),
            'similaridade': 1 / (1 + dist),  # Converter distância em similaridade
            'documento': documentos[idx],
            'metadados': metadados[idx]
        })
    
    return resultados

# ===== TESTES COM QUERIES REAIS =====

print("="*70)
print("TESTES DE RETRIEVAL:")
print("="*70)
print()

# Lista de queries de teste
queries_teste = [
    "Pistola Glock roubada em Brasília",
    "Revolver calibre 38 apreendido",
    "Armas da marca Taurus",
    "Ocorrências de furto de arma",
    "Pistola sem número de série"
]

for i, query in enumerate(queries_teste, 1):
    print(f"{'='*70}")
    print(f"TESTE {i}: {query}")
    print(f"{'='*70}")
    print()
    
    # Buscar top-3 documentos
    resultados = buscar_documentos(query, k=3)
    
    for resultado in resultados:
        print(f"Rank {resultado['rank']}:")
        print(f"  Similaridade: {resultado['similaridade']:.4f}")
        print(f"  Distância L2: {resultado['distancia']:.4f}")
        print(f"  Metadados: {resultado['metadados']}")
        print(f"  Documento (preview):")
        # Mostrar primeiras 3 linhas do documento
        doc_lines = resultado['documento'].split('\n')[:3]
        for line in doc_lines:
            print(f"    {line}")
        print()
    
    print()

# ===== TESTE INTERATIVO (OPCIONAL) =====

print("="*70)
print("TESTE INTERATIVO (opcional):")
print("="*70)
print("\nDeseja testar com suas próprias queries?")
print("Digite 's' para sim, qualquer tecla para pular: ", end='')

resposta = input().strip().lower()

if resposta == 's':
    print("\n" + "="*70)
    print("MODO INTERATIVO")
    print("Digite 'sair' para encerrar")
    print("="*70)
    print()
    
    while True:
        query = input("\nSua query: ").strip()
        
        if query.lower() == 'sair':
            break
        
        if not query:
            continue
        
        print(f"\n[BUSCA] Buscando: '{query}'")
        print("-"*70)
        
        resultados = buscar_documentos(query, k=3)
        
        for resultado in resultados:
            print(f"\nRank {resultado['rank']} (similaridade: {resultado['similaridade']:.4f}):")
            print(resultado['documento'])
            print("-"*70)

# ===== ESTATÍSTICAS FINAIS =====

print("\n" + "="*70)
print("ESTATÍSTICAS DO RETRIEVAL:")
print("="*70)
print(f"Índice FAISS: {index.ntotal:,} vetores")
print(f"Documentos disponíveis: {len(documentos):,}")
print(f"Modelo de embeddings: all-MiniLM-L6-v2 (384 dim)")
print(f"Tipo de busca: Distância L2 (Euclidiana)")
print()

print("[OK] PASSO 4 CONCLUÍDO!")
print()
print("="*70)
print("PIPELINE RAG COMPLETO!")
print("="*70)
print("\n[OK] Todos os passos concluídos:")
print("  1. [OK] Documentos preparados")
print("  2. [OK] Embeddings gerados")
print("  3. [OK] Índice FAISS criado")
print("  4. [OK] Retrieval testado")
print()
print("[INFO]  Próximo: Integrar ao agente v4.0")
print("    Execute: agente_v4_5_rag.py")


