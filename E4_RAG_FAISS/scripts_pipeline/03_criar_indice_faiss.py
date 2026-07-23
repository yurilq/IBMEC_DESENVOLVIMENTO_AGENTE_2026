"""
PASSO 3: CRIAR ÍNDICE FAISS
Indexa embeddings para busca vetorial rápida
"""

import json
import numpy as np
import faiss
from pathlib import Path
import time

print("="*70)
print("PASSO 3: CRIANDO ÍNDICE FAISS")
print("="*70)

# ===== CARREGAR DADOS =====

OUTPUT_DIR = Path(__file__).parent.parent / "03_outputs"

print(f"\n[PASTA] Carregando embeddings de: {OUTPUT_DIR / 'embeddings.npy'}")

embeddings = np.load(OUTPUT_DIR / "embeddings.npy")

print(f"[OK] {embeddings.shape[0]:,} embeddings carregados")
print(f"   Dimensões: {embeddings.shape[1]}")
print()

# Carregar documentos e metadados
with open(OUTPUT_DIR / "documentos.json", 'r', encoding='utf-8') as f:
    documentos = json.load(f)

with open(OUTPUT_DIR / "metadados.json", 'r', encoding='utf-8') as f:
    metadados = json.load(f)

print(f"[OK] {len(documentos):,} documentos carregados")
print(f"[OK] {len(metadados):,} metadados carregados\n")

# ===== CRIAR ÍNDICE FAISS =====

print("[BUILD] Criando indice FAISS...")
print("Tipo: IndexFlatL2 (busca exata por distancia L2)")
print()

inicio = time.time()

# Dimensões dos embeddings
d = embeddings.shape[1]

# Criar índice FAISS (busca exata)
# IndexFlatL2: busca exata usando distância L2 (Euclidiana)
index = faiss.IndexFlatL2(d)

print(f"Índice criado: {index.ntotal} vetores indexados")
print(f"Dimensões: {d}")
print()

# ===== ADICIONAR VETORES AO ÍNDICE =====

print("[PROC] Adicionando embeddings ao índice...")

# Adicionar todos os embeddings
index.add(embeddings)

tempo_indexacao = time.time() - inicio

print(f"[OK] {index.ntotal:,} vetores adicionados ao índice em {tempo_indexacao:.2f}s\n")

# ===== TESTAR ÍNDICE =====

print("="*70)
print("TESTE RÁPIDO DO ÍNDICE:")
print("="*70)

# Testar busca com o primeiro documento
query_vector = embeddings[0:1]  # Usar primeiro embedding como query

k = 3  # Top-3 resultados
distances, indices = index.search(query_vector, k)

print(f"\nQuery: Documento ID 0")
print(f"Top-{k} documentos mais similares:")
print()

for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
    print(f"Resultado {i+1}:")
    print(f"  Índice: {idx}")
    print(f"  Distância L2: {dist:.4f}")
    print(f"  Documento (preview): {documentos[idx][:100]}...")
    print()

# ===== SALVAR ÍNDICE =====

print("="*70)
print("SALVANDO ÍNDICE:")
print("="*70)
print()

# Salvar índice FAISS
index_path = OUTPUT_DIR / "faiss_index.bin"
faiss.write_index(index, str(index_path))
print(f"[OK] Índice FAISS salvo em: {index_path}")

# Salvar configuração
config = {
    'num_vectors': index.ntotal,
    'dimensions': d,
    'index_type': 'IndexFlatL2',
    'num_documents': len(documentos),
    'tempo_indexacao': tempo_indexacao
}

config_path = OUTPUT_DIR / "index_config.json"
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2)

print(f"[OK] Configuração salva em: {config_path}")
print()

# ===== ESTATÍSTICAS =====

print("="*70)
print("ESTATÍSTICAS DO ÍNDICE:")
print("="*70)
print(f"Vetores indexados: {index.ntotal:,}")
print(f"Dimensões: {d}")
print(f"Tipo de índice: IndexFlatL2 (busca exata)")
print(f"Tempo de indexação: {tempo_indexacao:.2f}s")
print(f"Tamanho em disco: {index_path.stat().st_size / (1024*1024):.2f} MB")
print()

print("[OK] PASSO 3 CONCLUÍDO!")
print("[INFO][INFO]  Próximo: Execute 04_testar_retrieval.py")



