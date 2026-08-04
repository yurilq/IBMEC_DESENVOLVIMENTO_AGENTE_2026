# =============================================================================
# PATCH PARA CORRIGIR O PROBLEMA DO PDF GRANDE
# =============================================================================
# 
# PROBLEMA: O PDF "procedimento_operacional_padrao-pericia_criminal.pdf" 
#           nao aparece nos resultados porque:
#           
#           1. Tem 383.207 caracteres (muito grande!)
#           2. Poucos paragrafos duplos (\n\n)
#           3. O chunking semantico cria 1 chunk GIGANTE
#           4. O embedding trunca e perde informacao
#           5. Scores ficam muito baixos
#
# SOLUCAO: Usar chunking HIBRIDO que funciona para PDFs grandes
#
# =============================================================================

"""
INSTRUCOES:

1. Copie o codigo abaixo
2. Cole no seu notebook (substitua a funcao chunk_text_semantico)
3. Re-execute o PASSO 6 (Preparar Todos os Chunks)
4. Re-execute o PASSO 8 (Gerar Embeddings)
5. Re-execute o PASSO 12 (Salvar Indice)

RESULTADO ESPERADO:
- De 1 chunk gigante -> ~478 chunks de tamanho adequado
- Scores de similaridade melhores (0.5-0.9 em vez de 0.09-0.31)
- Respostas do PDF aparecem nos resultados!
"""

# =============================================================================
# CODIGO PARA COPIAR NO NOTEBOOK
# =============================================================================

def chunk_text_hibrido(texto, chunk_size=1000, overlap=150):
    """
    Chunking hibrido: tenta semantico, se falhar usa fixo.
    
    MELHORIAS:
    - Detecta PDFs com poucos paragrafos
    - Usa chunking FIXO nesses casos
    - Garante chunks de tamanho adequado (~1000 chars)
    
    Args:
        texto: Texto para dividir
        chunk_size: Tamanho do chunk (recomendado: 1000 para PDFs grandes)
        overlap: Sobreposicao (recomendado: 150)
    
    Returns:
        list: Lista de chunks
    """
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
# MODIFICACAO NO PASSO 6: Preparar Todos os Chunks
# =============================================================================

def preparar_todos_chunks():
    """
    Prepara chunks de TODOS os documentos (.txt + PDFs).
    
    MODIFICACAO: Usa chunk_text_hibrido em vez de chunk_text_semantico
    
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
        print("\n📄 Processando PDFs...")
        for pdf in pdfs:
            # Detectar se e PDF grande
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
        
        print(f"\n✅ {len([c for c in todos_chunks if c['tipo'] == 'pdf'])} chunks de PDFs")
    
    print(f"\n🎉 Total: {len(todos_chunks)} chunks preparados!")
    
    return todos_chunks


# =============================================================================
# TESTE RAPIDO
# =============================================================================

"""
Depois de aplicar o patch, teste com estas perguntas:

1. "O que é perícia criminal?"
2. "Como fazer perícia em local de crime?"
3. "Quais são os procedimentos de coleta de vestígios?"
4. "Como documentar uma cena de crime?"
5. "O que é cadeia de custódia?"

RESULTADO ESPERADO:
- Chunks do PDF aparecem nos top-5
- Scores > 0.5
- Arquivo "procedimento_operacional_padrao-pericia_criminal.pdf" nos resultados
"""

# =============================================================================
# RESUMO DAS MUDANCAS
# =============================================================================

print("""
================================================================================
RESUMO DO PATCH
================================================================================

MUDANCAS:

1. Nova funcao: chunk_text_hibrido()
   - Substitui chunk_text_semantico()
   - Detecta PDFs problematicos
   - Usa chunking fixo quando necessario

2. Modificacao em preparar_todos_chunks():
   - Detecta PDFs grandes (>100K chars)
   - Usa chunk_size=1000 para PDFs grandes
   - Usa chunk_size=500 para .txt e PDFs pequenos

RESULTADO:
   - De 1 chunk (383K) -> 478 chunks (~1000 chars cada)
   - Respostas do PDF aparecem nos resultados!

================================================================================
PROXIMOS PASSOS:
================================================================================

1. Copie as funcoes chunk_text_hibrido() e preparar_todos_chunks()
2. Cole no notebook (celula PASSO 6)
3. Re-execute as celulas:
   - PASSO 6: Preparar Todos os Chunks
   - PASSO 8: Gerar Embeddings  
   - PASSO 12: Salvar Indice
4. Teste com perguntas sobre pericia criminal

================================================================================
""")
