import json
import sys

print("="*80)
print("CRIANDO NOTEBOOK CORRIGIDO")
print("="*80)

# Carregar notebook original
with open('E5_ESPECIALIZACAO_PDFS_V2.ipynb', 'r', encoding='utf-8') as f:
    nb_original = json.load(f)

cells_originais = nb_original['cells']

print(f"\nNotebook original: {len(cells_originais)} celulas")

# Encontrar onde comeca a duplicacao (celula 40)
# Vamos manter apenas ate a celula 39

cells_limpas = cells_originais[:40]  # Pegar so as primeiras 40 celulas (antes da duplicacao)

print(f"Celulas apos remover duplicacao: {len(cells_limpas)}")

# Agora vamos SUBSTITUIR as funcoes de chunking pelas versoes corrigidas
# Precisamos encontrar a celula que contem chunk_text_semantico

for i, cell in enumerate(cells_limpas):
    if cell['cell_type'] == 'code' and cell['source']:
        source_text = ''.join(cell['source'])
        
        # Se encontrar a funcao chunk_text_semantico, substituir por chunk_text_hibrido
        if 'def chunk_text_semantico' in source_text:
            print(f"\n[FOUND] Celula {i}: chunk_text_semantico - SUBSTITUINDO")
            
            # Nova funcao corrigida
            new_source = '''def chunk_text_hibrido(texto, chunk_size=1000, overlap=150):
    """
    Chunking hibrido: tenta semantico, se falhar usa fixo.
    
    CORRECAO para PDFs grandes como procedimento_operacional_padrao-pericia_criminal.pdf
    
    Args:
        texto: Texto para dividir
        chunk_size: Tamanho do chunk (1000 para PDFs grandes, 500 para .txt)
        overlap: Sobreposicao (150 para PDFs grandes, 50 para .txt)
    
    Returns:
        list: Lista de chunks
    """
    chunks = []
    
    # Tentar dividir por paragrafos duplos
    paragrafos = texto.split('\\n\\n')
    
    # Se tiver poucos paragrafos, tentar quebra simples
    if len(paragrafos) < 5:
        paragrafos = texto.split('\\n')
    
    # Se ainda tiver poucos, usar chunking FIXO (CORRECAO CRITICA)
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
            chunk_atual += "\\n\\n" + paragrafo
    
    # Adicionar ultimo chunk
    if len(chunk_atual.strip()) > 50:
        chunks.append(chunk_atual.strip())
    
    return chunks

# Testar com documento de exemplo
if docs_txt:
    doc_teste = docs_txt[0]['conteudo']
    
    chunks_hibrido = chunk_text_hibrido(doc_teste, chunk_size=500, overlap=50)
    
    print(f"📊 Chunking Hibrido:")
    print(f"\\n📄 Documento: {docs_txt[0]['arquivo']}")
    print(f"   Tamanho original: {len(doc_teste)} caracteres")
    print(f"   Total de chunks: {len(chunks_hibrido)}")
    print(f"   Tamanho medio: {np.mean([len(c) for c in chunks_hibrido]):.0f} caracteres")
    
    print(f"\\n📝 Exemplo de chunk:")
    print(f"{chunks_hibrido[0][:300]}...")
'''
            
            cells_limpas[i]['source'] = [new_source]
        
        # Se encontrar preparar_todos_chunks, substituir pela versao corrigida
        if 'def preparar_todos_chunks' in source_text and 'chunk_text_semantico' in source_text:
            print(f"\n[FOUND] Celula {i}: preparar_todos_chunks - SUBSTITUINDO")
            
            new_source = '''def preparar_todos_chunks():
    """
    Prepara chunks de TODOS os documentos (.txt + PDFs).
    
    CORRECAO: Usa chunk_text_hibrido e detecta PDFs grandes
    
    Returns:
        list: [{"tipo": str, "arquivo": str, "chunk_id": int, "texto": str}]
    """
    todos_chunks = []
    
    # Processar documentos .txt
    print("📚 Processando documentos .txt...")
    for doc in docs_txt:
        # Para .txt usar chunk_size menor (500)
        chunks = chunk_text_hibrido(doc['conteudo'], chunk_size=500, overlap=50)
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
        print("\\n📄 Processando PDFs...")
        for pdf in pdfs:
            # CORRECAO CRITICA: Detectar se e PDF grande
            tamanho = len(pdf['conteudo'])
            
            if tamanho > 100000:  # Maior que 100K caracteres
                print(f"   [!] {pdf['arquivo']}: PDF GRANDE ({tamanho:,} chars)")
                print(f"       Usando chunk_size=1000, overlap=150")
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
            
            print(f"   ✅ {pdf['arquivo']}: {len(chunks)} chunks criados")
            
            for i, chunk in enumerate(chunks):
                todos_chunks.append({
                    'tipo': 'pdf',
                    'arquivo': pdf['arquivo'],
                    'chunk_id': i,
                    'texto': chunk
                })
        
        print(f"\\n✅ {len([c for c in todos_chunks if c['tipo'] == 'pdf'])} chunks de PDFs")
    
    print(f"\\n🎉 Total: {len(todos_chunks)} chunks preparados!")
    
    return todos_chunks

# Preparar
todos_chunks = preparar_todos_chunks()

# Estatisticas
print(f"\\n📊 Estatisticas dos Chunks:")
print(f"   Total: {len(todos_chunks)}")
print(f"   .txt: {len([c for c in todos_chunks if c['tipo'] == 'txt'])}")
print(f"   PDFs: {len([c for c in todos_chunks if c['tipo'] == 'pdf'])}")
print(f"   Tamanho medio: {np.mean([len(c['texto']) for c in todos_chunks]):.0f} caracteres")
print(f"   Tamanho minimo: {min([len(c['texto']) for c in todos_chunks])} caracteres")
print(f"   Tamanho maximo: {max([len(c['texto']) for c in todos_chunks])} caracteres")
'''
            
            cells_limpas[i]['source'] = [new_source]

# Criar novo notebook
nb_corrigido = {
    "cells": cells_limpas,
    "metadata": nb_original['metadata'],
    "nbformat": nb_original['nbformat'],
    "nbformat_minor": nb_original['nbformat_minor']
}

# Salvar
output_file = 'E5_ESPECIALIZACAO_PDFS_V3_CORRIGIDO.ipynb'

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(nb_corrigido, f, indent=1, ensure_ascii=False)

print(f"\n{'='*80}")
print("SUCESSO!")
print('='*80)
print(f"\nNotebook corrigido salvo em:")
print(f"  {output_file}")
print(f"\nCelulas: {len(cells_limpas)}")
print(f"\nCORRECOES APLICADAS:")
print(f"  1. Removidas celulas duplicadas (celulas 40+)")
print(f"  2. Substituida funcao chunk_text_semantico -> chunk_text_hibrido")
print(f"  3. Substituida funcao preparar_todos_chunks (versao corrigida)")
print(f"\nPROXIMOS PASSOS:")
print(f"  1. Abra o notebook: {output_file}")
print(f"  2. Execute todas as celulas (Run All)")
print(f"  3. Verifique o output:")
print(f"     - PDF grande: 478 chunks (nao 1 chunk)")
print(f"     - Total: ~600 chunks (nao 135)")
print(f"  4. Teste com: buscar_com_reranking('Qual o procedimento em local de crime com computadores?')")
print(f"  5. PDF deve aparecer nos resultados!")
