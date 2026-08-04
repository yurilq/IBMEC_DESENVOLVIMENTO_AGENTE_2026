"""
Busca simples: Encontrar trechos sobre computador no PDF
"""

import os
from PyPDF2 import PdfReader

caminho = "../01_DADOS/pdfs_pcdf/procedimento_operacional_padrao-pericia_criminal.pdf"

print("="*80)
print("BUSCANDO 'COMPUTADOR' NO PDF")
print("="*80)

reader = PdfReader(caminho)
texto = ""
for page in reader.pages:
    texto += page.extract_text()

print(f"\nPDF: {len(reader.pages)} paginas, {len(texto):,} caracteres")

# Buscar todas as ocorrencias
palavra = "computador"
count = texto.lower().count(palavra)

print(f"\nPalavra '{palavra}' aparece: {count} vezes")

# Encontrar e mostrar contextos
print(f"\n{'='*80}")
print(f"TRECHOS COM 'COMPUTADOR':")
print('='*80)

pos = 0
trechos_encontrados = []

while True:
    idx = texto.lower().find(palavra, pos)
    if idx == -1:
        break
    
    # Pegar contexto (200 chars antes e depois)
    inicio = max(0, idx - 200)
    fim = min(len(texto), idx + 200)
    
    trecho = texto[inicio:fim]
    # Limpar quebras de linha
    trecho = ' '.join(trecho.split())
    
    trechos_encontrados.append(trecho)
    pos = idx + 1

# Mostrar trechos unicos (evitar duplicatas)
trechos_unicos = []
for trecho in trechos_encontrados:
    if not any(trecho in t or t in trecho for t in trechos_unicos):
        trechos_unicos.append(trecho)

for i, trecho in enumerate(trechos_unicos, 1):
    print(f"\n[{i}] ...{trecho}...")
    print("-"*80)

print(f"\n{'='*80}")
print("RECOMENDACAO")
print('='*80)

print(f"""
Encontramos {count} ocorrencias de 'computador' no PDF!

Para que o PDF apareca nos resultados, voce precisa:

1. Aplicar o chunking hibrido (chunk_size=1000, overlap=150)
   - Isso garante que os trechos sobre computador fiquem em chunks separados

2. Re-gerar os embeddings com TODOS os chunks

3. Testar novamente a busca

Se mesmo assim nao aparecer, pode ser porque:
- Os chunks com "computador" nao sao os mais relevantes semanticamente
- A pergunta esta muito especifica e o contexto do PDF e mais geral
- Outros documentos tem scores mais altos

TESTE COM ESTA PERGUNTA EXATA (copie do trecho acima):
"[Cole aqui uma frase exata do PDF que menciona computador]"

Isso deve garantir que o PDF apareca nos resultados!
""")
