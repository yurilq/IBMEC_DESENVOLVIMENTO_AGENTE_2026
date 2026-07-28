# 📄 GUIA: USANDO PDFs NO NOTEBOOK E5

**Objetivo:** Guia rápido para trabalhar com os PDFs adicionados ao E5

---

## 📚 PDFs DISPONÍVEIS

Você adicionou 4 PDFs na pasta `01_DADOS/pdfs_pcdf/`:

1. **estatuto_desarmamento.pdf** (22 páginas, ~60 KB)
   - Estatuto do Desarmamento
   - Câmara dos Deputados, 2004

2. **LEI-10.826-03-SINARM.pdf** (14 páginas, ~313 KB)
   - Lei 10.826/2003
   - Sistema Nacional de Armas (SINARM)
   - Presidência da República

3. **cartilha-de-armamento-e-tiro.pdf** (27 páginas, ~1 MB)
   - Cartilha da Academia Nacional de Polícia
   - Serviço de Armamento e Tiro (SAT)
   - CONAT/DARM

4. **Anexo XVII - Porte de arma de fogo.pdf** (1 página, ~38 KB)
   - Certificado de porte federal
   - Deveres do portador

---

## ✅ O QUE FOI ATUALIZADO NO NOTEBOOK

### 1. Dataset de Teste (Passo 16)

**Antes:** 5 perguntas genéricas sobre .txt

**Agora:** 12 perguntas específicas dos PDFs reais:

```python
dataset_teste = [
    # SINARM (2 perguntas)
    {"pergunta": "O que é o SINARM?", ...},
    {"pergunta": "Onde funciona o SINARM?", ...},
    
    # Porte de Arma (2 perguntas)
    {"pergunta": "O que acontece se o portador for detido embriagado?", ...},
    {"pergunta": "O porte de arma é transferível?", ...},
    
    # Capacitação (2 perguntas)
    {"pergunta": "O que é necessário para comprovar capacidade técnica?", ...},
    {"pergunta": "Quem elaborou a cartilha de armamento e tiro?", ...},
    
    # Lei 10.826 (2 perguntas)
    {"pergunta": "O que a Lei 10.826 regulamenta?", ...},
    {"pergunta": "Quando foi sancionada a Lei 10.826?", ...},
    
    # Conceituais .txt (2 perguntas)
    {"pergunta": "O que é calibre de arma?", ...},
    {"pergunta": "Diferença entre pistola e revólver?", ...},
    
    # Cruzadas (2 perguntas)
    {"pergunta": "Como funciona o registro de armas no Brasil?", ...},
    {"pergunta": "Quais documentos regulam o porte de arma?", ...},
]
```

### 2. Nova Célula de Teste (Passo 22)

Adicionada célula para testar perguntas específicas dos PDFs:

```python
perguntas_pdfs = [
    "O que é o SINARM?",
    "O que acontece se o portador de arma for detido embriagado?",
    "O porte de arma é transferível?",
    "Quem elaborou a cartilha de armamento e tiro?",
    "O que a Lei 10.826 regulamenta?",
]
```

---

## 🧪 COMO TESTAR

### Opção 1: Executar Notebook Completo

1. Abrir notebook: `E5_ESPECIALIZACAO_PDFS.ipynb`
2. Executar células na ordem (1-63)
3. Observar resultados no **Passo 22**

### Opção 2: Testar Perguntas Específicas

Após executar até o Passo 15 (reranking implementado), você pode testar:

```python
# Testar pergunta específica
pergunta = "O que é o SINARM?"
resultados = buscar_com_reranking(pergunta, k_inicial=20, k_final=5)

for i, (chunk, score) in enumerate(resultados, 1):
    print(f"{i}. {chunk['arquivo']} (score: {score:.3f})")
    print(f"   {chunk['texto'][:200]}...")
```

**Resultado esperado:**
```
1. LEI-10.826-03-SINARM.pdf (score: 0.850)
   Art. 1o O Sistema Nacional de Armas – Sinarm, instituído no Ministério da Justiça...

2. sistema_sinarm.txt (score: 0.720)
   # Sistema SINARM - Sistema Nacional de Armas...
```

---

## 📊 RESULTADOS ESPERADOS

### Métricas com PDFs Reais

| Métrica | Objetivo | Descrição |
|---------|----------|-----------|
| **Precision@5** | > 0.80 | 80%+ dos top-5 são relevantes |
| **MRR** | > 0.70 | Primeiro relevante nas primeiras posições |
| **Recall@5** | > 0.75 | 75%+ dos relevantes são recuperados |

### Casos de Sucesso

✅ **Pergunta:** "O que é o SINARM?"
- **Esperado:** `LEI-10.826-03-SINARM.pdf` em 1º lugar
- **Score:** > 0.80

✅ **Pergunta:** "O porte de arma é transferível?"
- **Esperado:** `Anexo XVII - Porte de arma de fogo.pdf` em 1º lugar
- **Score:** > 0.85

✅ **Pergunta:** "Quem elaborou a cartilha?"
- **Esperado:** `cartilha-de-armamento-e-tiro.pdf` em 1º lugar
- **Score:** > 0.75

---

## ⚠️ PROBLEMAS CONHECIDOS

### 1. Encoding dos PDFs

**Problema:** Alguns PDFs têm caracteres estranhos (�, �, etc.)

**Causa:** Encoding problemático (não UTF-8)

**Solução:** PyPDF2 extrai o texto, mas pode ter erros. Não afeta a busca semântica.

**Exemplo:**
```
Original: "Polícia Federal"
Extraído: "Pol�cia Federal"
```

**Impacto:** Mínimo. Sentence-BERT captura o significado mesmo com erros.

### 2. PDFs Escaneados

**Problema:** Se o PDF for escaneado (imagem), PyPDF2 não extrai texto.

**Solução:** Usar OCR (Tesseract) - não implementado no E5.

**Como identificar:**
```python
texto = page.extract_text()
if len(texto.strip()) < 100:
    print("⚠️ Possível PDF escaneado")
```

### 3. Layouts Complexos

**Problema:** Tabelas, múltiplas colunas podem ser extraídas de forma confusa.

**Solução:** Chunking semântico ajuda a reorganizar o texto.

---

## 🔧 AJUSTES RECOMENDADOS

### 1. Tamanho dos Chunks

**Atual:** 500 caracteres

**Testar:**
- 300 caracteres (chunks menores, mais precisos)
- 700 caracteres (chunks maiores, mais contexto)

```python
chunks = chunk_text_semantico(texto, chunk_size=300, overlap=50)
```

### 2. Número de Candidatos (k_inicial)

**Atual:** 20 candidatos na busca inicial

**Testar:**
- 10 candidatos (mais rápido)
- 30 candidatos (mais abrangente)

```python
resultados = buscar_com_reranking(pergunta, k_inicial=30, k_final=5)
```

### 3. Overlap dos Chunks

**Atual:** 50 caracteres

**Testar:**
- 100 caracteres (mais contexto compartilhado)
- 25 caracteres (menos redundância)

```python
chunks = chunk_text_semantico(texto, chunk_size=500, overlap=100)
```

---

## 📝 PERGUNTAS ADICIONAIS PARA TESTAR

### Perguntas Específicas dos PDFs

```python
perguntas_extras = [
    # SINARM
    "Quais são as competências do SINARM?",
    "O SINARM funciona em qual ministério?",
    
    # Porte
    "Qual a validade do porte federal de arma?",
    "O porte de arma pode ser revogado?",
    
    # Capacitação
    "Quais são as normas de segurança para manuseio de arma?",
    "O que é necessário demonstrar no exame de capacitação?",
    
    # Lei 10.826
    "O que a Lei 10.826 define sobre crimes?",
    "Quem sancionou a Lei 10.826?",
    
    # Estatuto
    "Quando foi publicado o Estatuto do Desarmamento?",
    "O que é o Estatuto do Desarmamento?",
]
```

### Perguntas Cruzadas (PDFs + .txt)

```python
perguntas_cruzadas = [
    "Como funciona o registro de armas no Brasil?",  # Lei + sistema_sinarm.txt
    "Quais documentos regulam o porte de arma?",     # Múltiplos PDFs
    "O que é necessário para portar uma arma?",      # Lei + Anexo XVII + cartilha
]
```

---

## 🎯 PRÓXIMOS PASSOS

### 1. Adicionar Mais PDFs

Sugestões:
- Decreto 9.847/2019 (regulamenta Lei 10.826)
- Portarias da PCDF sobre armamento
- Manuais de procedimentos

### 2. Melhorar Chunking

- Implementar chunking por seções (detectar títulos)
- Preservar estrutura de artigos/parágrafos

### 3. Adicionar Metadata

```python
chunk = {
    'tipo': 'pdf',
    'arquivo': 'LEI-10.826-03-SINARM.pdf',
    'pagina': 3,
    'artigo': 'Art. 1º',
    'texto': '...'
}
```

### 4. Criar Interface

- Streamlit para interface web
- Mostrar PDFs originais
- Highlight do texto encontrado

---

## 📚 RECURSOS

### Documentação
- **PyPDF2:** https://pypdf2.readthedocs.io/
- **Sentence-Transformers:** https://www.sbert.net/
- **FAISS:** https://github.com/facebookresearch/faiss

### Datasets
- **DATASET_TESTE_PDFS.md:** Dataset completo com perguntas e respostas esperadas

---

**Última atualização:** 26/07/2026  
**Versão:** 1.0  
**Status:** ✅ Pronto para uso
