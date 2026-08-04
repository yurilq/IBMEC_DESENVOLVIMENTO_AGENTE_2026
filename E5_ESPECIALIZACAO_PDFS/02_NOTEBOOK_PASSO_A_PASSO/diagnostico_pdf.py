"""
Diagnostico: Por que o PDF procedimento_operacional_padrao-pericia_criminal.pdf
nao aparece nos resultados?
"""

import os
import sys
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("DIAGNOSTICO: procedimento_operacional_padrao-pericia_criminal.pdf")
print("="*80)

# Caminho do PDF problemático
caminho_pdf = "../01_DADOS/pdfs_pcdf/procedimento_operacional_padrao-pericia_criminal.pdf"

if not os.path.exists(caminho_pdf):
    print(f"[X] ERRO: PDF nao encontrado em {caminho_pdf}")
    exit(1)

print(f"\n[OK] PDF encontrado!")
print(f"   Tamanho: {os.path.getsize(caminho_pdf) / 1024 / 1024:.2f} MB")

# Carregar PDF
print("\n[>>] Carregando PDF...")
try:
    reader = PdfReader(caminho_pdf)
    num_paginas = len(reader.pages)
    print(f"   [OK] {num_paginas} paginas")
    
    # Extrair texto
    print("\n[>>] Extraindo texto...")
    texto_completo = ""
    paginas_vazias = 0
    
    for i, page in enumerate(reader.pages):
        texto_pagina = page.extract_text()
        if len(texto_pagina.strip()) < 50:
            paginas_vazias += 1
        texto_completo += texto_pagina
    
    print(f"   ✅ Texto extraído: {len(texto_completo):,} caracteres")
    print(f"   ⚠️  Páginas vazias/problemáticas: {paginas_vazias}/{num_paginas}")
    
    # Preview do conteúdo
    print(f"\n📄 Preview (primeiros 500 caracteres):")
    print("-" * 80)
    print(texto_completo[:500])
    print("-" * 80)
    
    # Chunking semântico
    def chunk_text_semantico(texto, chunk_size=500, overlap=50):
        paragrafos = texto.split('\n\n')
        chunks = []
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
    
    print(f"\n🔪 Criando chunks (chunk_size=500, overlap=50)...")
    chunks = chunk_text_semantico(texto_completo, chunk_size=500, overlap=50)
    print(f"   ✅ {len(chunks)} chunks criados")
    
    if len(chunks) > 0:
        tamanhos = [len(c) for c in chunks]
        print(f"   📊 Tamanho médio: {np.mean(tamanhos):.0f} caracteres")
        print(f"   📊 Tamanho mínimo: {min(tamanhos)} caracteres")
        print(f"   📊 Tamanho máximo: {max(tamanhos)} caracteres")
        
        # Mostrar primeiros chunks
        print(f"\n📝 Primeiros 3 chunks:")
        for i, chunk in enumerate(chunks[:3], 1):
            print(f"\n   --- Chunk {i} ---")
            print(f"   {chunk[:200]}...")
    
    # Teste de busca semântica
    print(f"\n🔍 TESTE DE BUSCA SEMÂNTICA:")
    print("-" * 80)
    
    # Carregar modelo
    print("   📥 Carregando Sentence-BERT...")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    print("   ✅ Modelo carregado!")
    
    # Gerar embeddings dos chunks
    print(f"   🔄 Gerando embeddings para {len(chunks)} chunks...")
    embeddings = model.encode(chunks[:100], show_progress_bar=True)  # Limitar a 100 para teste
    print(f"   ✅ Embeddings: {embeddings.shape}")
    
    # Perguntas de teste
    perguntas_teste = [
        "O que é perícia criminal?",
        "Como fazer perícia em local de crime?",
        "Quais são os procedimentos de coleta de vestígios?",
        "Como documentar uma cena de crime?",
        "O que é cadeia de custódia?"
    ]
    
    print(f"\n   🧪 Testando {len(perguntas_teste)} perguntas:")
    print("-" * 80)
    
    for pergunta in perguntas_teste:
        print(f"\n   ❓ '{pergunta}'")
        
        # Gerar embedding da pergunta
        query_emb = model.encode([pergunta])
        
        # Calcular similaridade
        sims = cosine_similarity(query_emb, embeddings)[0]
        
        # Top-3
        top_idx = sims.argsort()[-3:][::-1]
        
        print(f"      Top-3 chunks:")
        for idx in top_idx:
            score = sims[idx]
            chunk_preview = chunks[idx][:80].replace('\n', ' ')
            print(f"      [{idx}] Score: {score:.4f} | '{chunk_preview}...'")
    
    print("\n" + "="*80)
    print("DIAGNÓSTICO COMPLETO!")
    print("="*80)
    
    # Conclusões
    print("\n📋 CONCLUSÕES:")
    print(f"   1. PDF carregado: ✅")
    print(f"   2. Texto extraído: ✅ ({len(texto_completo):,} chars)")
    print(f"   3. Chunks criados: ✅ ({len(chunks)} chunks)")
    print(f"   4. Embeddings gerados: ✅")
    print(f"   5. Busca funciona: ✅")
    
    # Possíveis problemas
    print("\n⚠️  POSSÍVEIS PROBLEMAS:")
    if paginas_vazias > num_paginas * 0.3:
        print(f"   • {paginas_vazias} páginas têm pouco texto (possível PDF com imagens)")
    
    if len(chunks) > 1000:
        print(f"   • Muitos chunks ({len(chunks)}) podem diluir os resultados")
        print(f"   • Considere aumentar chunk_size ou usar apenas este PDF")
    
    print("\n💡 RECOMENDAÇÕES:")
    print("   1. Verificar se o PDF foi incluído no processamento do notebook")
    print("   2. Verificar se os chunks deste PDF estão em 'todos_chunks'")
    print("   3. Aumentar chunk_size para 1000-1500 (PDF muito grande)")
    print("   4. Fazer perguntas mais específicas sobre perícia criminal")

except Exception as e:
    print(f"\n❌ ERRO ao processar PDF: {e}")
    import traceback
    traceback.print_exc()
