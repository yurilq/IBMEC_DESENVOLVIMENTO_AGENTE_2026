"""
Módulo de Processamento de Chunks

Responsável por dividir documentos em chunks menores:
- Chunking híbrido (semântico + fixo)
- Overlap para preservar contexto
- Validação de qualidade

Estratégias:
1. Fixo: 500 caracteres (E4)
2. Semântico: Por parágrafos/seções (E5)
3. Overlap: Chunks se sobrepõem (evita perder contexto)
"""

import numpy as np
from typing import List, Dict, Optional


def chunk_text_hibrido(
    texto: str,
    chunk_size: int = 1000,
    overlap: int = 150
) -> List[str]:
    """
    Chunking híbrido: tenta semântico, se falhar usa fixo.
    
    CORREÇÃO para PDFs grandes como procedimento_operacional_padrao-pericia_criminal.pdf
    
    Args:
        texto: Texto para dividir
        chunk_size: Tamanho do chunk (1000 para PDFs grandes, 500 para .txt)
        overlap: Sobreposição (150 para PDFs grandes, 50 para .txt)
    
    Returns:
        list: Lista de chunks
    
    Example:
        >>> chunks = chunk_text_hibrido(texto, chunk_size=500, overlap=50)
        >>> print(f"{len(chunks)} chunks criados")
    """
    chunks = []
    
    # Tentar dividir por parágrafos duplos
    paragrafos = texto.split('\n\n')
    
    # Se tiver poucos parágrafos, tentar quebra simples
    if len(paragrafos) < 5:
        paragrafos = texto.split('\n')
    
    # Se ainda tiver poucos, usar chunking FIXO (CORREÇÃO CRÍTICA)
    if len(paragrafos) < 10:
        # Chunking fixo para PDFs problemáticos
        start = 0
        while start < len(texto):
            end = start + chunk_size
            chunk = texto[start:end]
            
            if len(chunk.strip()) > 50:
                chunks.append(chunk.strip())
            
            start = end - overlap
        
        return chunks
    
    # Chunking semântico normal (para PDFs bem formatados)
    chunk_atual = ""
    
    for paragrafo in paragrafos:
        # Se adicionar este parágrafo ultrapassar o limite
        if len(chunk_atual) + len(paragrafo) > chunk_size:
            # Salvar chunk atual
            if len(chunk_atual.strip()) > 50:
                chunks.append(chunk_atual.strip())
            
            # Iniciar novo chunk (com overlap)
            chunk_atual = chunk_atual[-overlap:] + paragrafo
        else:
            chunk_atual += "\n\n" + paragrafo
    
    # Adicionar último chunk
    if len(chunk_atual.strip()) > 50:
        chunks.append(chunk_atual.strip())
    
    return chunks


def preparar_todos_chunks(
    docs_txt: List[Dict[str, str]],
    pdfs: List[Dict[str, any]],
    chunk_size_txt: int = 500,
    overlap_txt: int = 50,
    chunk_size_pdf: int = 1000,
    overlap_pdf: int = 150
) -> List[Dict[str, any]]:
    """
    Prepara chunks de TODOS os documentos (.txt + PDFs).
    
    CORREÇÃO: Usa chunk_text_hibrido e detecta PDFs grandes
    
    Args:
        docs_txt: Lista de documentos .txt
        pdfs: Lista de PDFs
        chunk_size_txt: Tamanho de chunk para .txt
        overlap_txt: Overlap para .txt
        chunk_size_pdf: Tamanho de chunk para PDFs
        overlap_pdf: Overlap para PDFs
    
    Returns:
        list: [{
            \"tipo\": str,
            \"arquivo\": str,
            \"chunk_id\": int,
            \"texto\": str
        }]
    
    Example:
        >>> todos_chunks = preparar_todos_chunks(docs_txt, pdfs)
        >>> print(f"{len(todos_chunks)} chunks preparados")
    """
    todos_chunks = []
    
    # Processar documentos .txt
    print("📚 Processando documentos .txt...")
    for doc in docs_txt:
        # Para .txt usar chunk_size menor (500)
        chunks = chunk_text_hibrido(doc['conteudo'], chunk_size=chunk_size_txt, overlap=overlap_txt)
        for i, chunk in enumerate(chunks):
            todos_chunks.append({
                'tipo': 'txt',
                'arquivo': doc['arquivo'],
                'chunk_id': i,
                'texto': chunk
            })
    
    print(f"✅ {len([c for c in todos_chunks if c['tipo'] == 'txt'])} chunks de .txt")
    
    # Processar PDFs
    if pdfs:
        print("\n📄 Processando PDFs...")
        for pdf in pdfs:
            # CORREÇÃO CRÍTICA: Detectar se é PDF grande
            tamanho = len(pdf['conteudo'])
            
            if tamanho > 100000:  # Maior que 100K caracteres
                print(f"   [!] {pdf['arquivo']}: PDF GRANDE ({tamanho:,} chars)")
                print(f"       Usando chunk_size=1000, overlap=150")
                chunk_size_atual = chunk_size_pdf
                overlap_atual = overlap_pdf
            else:
                chunk_size_atual = chunk_size_txt
                overlap_atual = overlap_txt
            
            chunks = chunk_text_hibrido(
                pdf['conteudo'], 
                chunk_size=chunk_size_atual, 
                overlap=overlap_atual
            )
            
            print(f"   ✅ {pdf['arquivo']}: {len(chunks)} chunks criados")
            
            for i, chunk in enumerate(chunks):
                todos_chunks.append({
                    'tipo': 'pdf',
                    'arquivo': pdf['arquivo'],
                    'chunk_id': i,
                    'texto': chunk
                })
        
        print(f"\n✅ {len([c for c in todos_chunks if c['tipo'] == 'pdf'])} chunks de PDFs")
    
    print(f"\n🎉 Total: {len(todos_chunks)} chunks preparados!")
    
    return todos_chunks


def validar_chunks(chunks: List[Dict[str, any]]) -> Dict[str, any]:
    """
    Valida qualidade dos chunks.
    
    Args:
        chunks: Lista de chunks
    
    Returns:
        dict: Estatísticas dos chunks
    
    Example:
        >>> stats = validar_chunks(todos_chunks)
        >>> print(f"Tamanho médio: {stats['tamanho_medio']}")
    """
    if not chunks:
        return {
            'total': 0,
            'tamanho_medio': 0,
            'tamanho_minimo': 0,
            'tamanho_maximo': 0
        }
    
    tamanhos = [len(c['texto']) for c in chunks]
    
    return {
        'total': len(chunks),
        'tamanho_medio': np.mean(tamanhos),
        'tamanho_minimo': min(tamanhos),
        'tamanho_maximo': max(tamanhos),
        'txt_chunks': len([c for c in chunks if c['tipo'] == 'txt']),
        'pdf_chunks': len([c for c in chunks if c['tipo'] == 'pdf'])
    }
