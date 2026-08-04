"""
FIX: Chunking melhorado para PDFs grandes
"""

import os
import sys
import numpy as np
from PyPDF2 import PdfReader

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def chunk_text_hibrido(texto, chunk_size=800, overlap=100):
    """
    Chunking hibrido: tenta semantico, se falhar usa fixo.
    
    Args:
        texto: Texto para dividir
        chunk_size: Tamanho do chunk
        overlap: Sobreposicao
    
    Returns:
        list: Lista de chunks
    """
    chunks = []
    
    # Tentar dividir por paragrafos duplos
    paragrafos = texto.split('\n\n')
    
    # Se tiver poucos paragrafos, tentar quebra simples
    if len(paragrafos) < 5:
        paragrafos = texto.split('\n')
    
    # Se ainda tiver poucos, usar chunking fixo
    if len(paragrafos) < 10:
        print("   [AVISO] Poucos paragrafos, usando chunking FIXO")
        # Chunking fixo
        start = 0
        while start < len(texto):
            end = start + chunk_size
            chunk = texto[start:end]
            
            if len(chunk.strip()) > 50:
                chunks.append(chunk.strip())
            
            start = end - overlap
        
        return chunks
    
    # Chunking semantico normal
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


# Testar com o PDF problematico
caminho_pdf = "../01_DADOS/pdfs_pcdf/procedimento_operacional_padrao-pericia_criminal.pdf"

print("="*80)
print("TESTE: Chunking Hibrido para PDF Grande")
print("="*80)

reader = PdfReader(caminho_pdf)
texto = ""
for page in reader.pages:
    texto += page.extract_text()

print(f"\n[OK] Texto extraido: {len(texto):,} caracteres")

# Testar diferentes configuracoes
configs = [
    {"chunk_size": 500, "overlap": 50},
    {"chunk_size": 800, "overlap": 100},
    {"chunk_size": 1000, "overlap": 150},
    {"chunk_size": 1500, "overlap": 200},
]

print("\n" + "="*80)
print("COMPARACAO DE CONFIGURACOES:")
print("="*80)

for config in configs:
    print(f"\n[>>] Testando chunk_size={config['chunk_size']}, overlap={config['overlap']}")
    
    chunks = chunk_text_hibrido(texto, **config)
    
    tamanhos = [len(c) for c in chunks]
    
    print(f"   Total de chunks: {len(chunks)}")
    print(f"   Tamanho medio: {np.mean(tamanhos):.0f} caracteres")
    print(f"   Tamanho min: {min(tamanhos)}")
    print(f"   Tamanho max: {max(tamanhos)}")
    
    # Preview do primeiro chunk
    if len(chunks) > 0:
        print(f"   Preview chunk 1: '{chunks[0][:100]}...'")

print("\n" + "="*80)
print("RECOMENDACAO:")
print("="*80)
print("\n[!] Use chunk_size=1000 e overlap=150 para este PDF")
print("[!] Isso cria ~400-500 chunks em vez de 1 chunk gigante")
print("\n[!] No notebook, substitua a funcao chunk_text_semantico")
print("    por chunk_text_hibrido")
