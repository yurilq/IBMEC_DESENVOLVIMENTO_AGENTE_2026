"""
PASSO 2: GERAR EMBEDDINGS
Converte documentos textuais em vetores numéricos
"""

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import time

print("="*70)
print("PASSO 2: GERANDO EMBEDDINGS")
print("="*70)

# ===== CARREGAR DOCUMENTOS =====

OUTPUT_DIR = Path(__file__).parent.parent / "03_outputs"

print(f"\n[PASTA] Carregando documentos de: {OUTPUT_DIR / 'documentos.json'}")

with open(OUTPUT_DIR / "documentos.json", 'r', encoding='utf-8') as f:
    documentos = json.load(f)

print(f"[OK] {len(documentos):,} documentos carregados\n")

# ===== CARREGAR MODELO DE EMBEDDINGS =====

print("[MODEL] Carregando modelo de embeddings...")
print("Modelo: all-MiniLM-L6-v2 (384 dimensoes)")
print("(Primeira vez demora ~1min para download)")
print()

inicio = time.time()

# Modelo leve e eficiente (384 dimensões)
model = SentenceTransformer('all-MiniLM-L6-v2')

tempo_carregamento = time.time() - inicio
print(f"[OK] Modelo carregado em {tempo_carregamento:.2f}s\n")

# ===== GERAR EMBEDDINGS =====

print("[PROC] Gerando embeddings dos documentos...")
print("(Isso pode levar alguns minutos para muitos documentos)")
print()

inicio = time.time()

# Gerar embeddings em batches (mais eficiente)
batch_size = 32
embeddings_list = []

for i in range(0, len(documentos), batch_size):
    batch = documentos[i:i+batch_size]
    batch_embeddings = model.encode(batch, show_progress_bar=False)
    embeddings_list.extend(batch_embeddings)
    
    # Progresso
    if (i + batch_size) % 100 == 0 or (i + batch_size) >= len(documentos):
        print(f"  Processados: {min(i + batch_size, len(documentos)):,} / {len(documentos):,} documentos...")

# Converter para numpy array
embeddings = np.array(embeddings_list, dtype='float32')

tempo_geracao = time.time() - inicio
print(f"\n[OK] Embeddings gerados em {tempo_geracao:.2f}s\n")

# ===== INFORMAÇÕES SOBRE EMBEDDINGS =====

print("="*70)
print("INFORMAÇÕES DOS EMBEDDINGS:")
print("="*70)
print(f"Quantidade: {embeddings.shape[0]:,} vetores")
print(f"Dimensões: {embeddings.shape[1]} por vetor")
print(f"Tipo: {embeddings.dtype}")
print(f"Tamanho em memória: {embeddings.nbytes / (1024*1024):.2f} MB")
print()

# Mostrar exemplo de embedding
print("Exemplo do primeiro embedding:")
print(f"Vetor (primeiras 10 dimensões): {embeddings[0][:10]}")
print(f"Norma L2: {np.linalg.norm(embeddings[0]):.4f}")
print()

# ===== SALVAR EMBEDDINGS =====

print("[SAVE] Salvando embeddings...")

# Salvar embeddings como numpy array
embeddings_path = OUTPUT_DIR / "embeddings.npy"
np.save(embeddings_path, embeddings)

print(f"[OK] Embeddings salvos em: {embeddings_path}")
print()

# ===== ESTATÍSTICAS =====

print("="*70)
print("ESTATÍSTICAS:")
print("="*70)
print(f"Total de embeddings: {len(embeddings):,}")
print(f"Dimensões por vetor: {embeddings.shape[1]}")
print(f"Tempo de geração: {tempo_geracao:.2f}s")
print(f"Velocidade: {len(embeddings) / tempo_geracao:.0f} docs/segundo")
print()

print("[OK] PASSO 2 CONCLUÍDO!")
print("[INFO]  Próximo: Execute 03_criar_indice_faiss.py")


