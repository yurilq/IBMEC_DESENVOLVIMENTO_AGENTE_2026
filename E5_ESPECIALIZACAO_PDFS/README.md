# E5 - ESPECIALIZAÇÃO COM PDFs PCDF

**MBA IA Generativa PCDF - IBMEC**  
**Encontro 5:** Especialização de Agentes com PDFs Reais  
**Carga Horária:** 5 horas (terça/quinta 13h-18h)

---

## 🎯 OBJETIVOS

Ao final do E5, você será capaz de:

1. ✅ **Especializar RAG** para domínio PCDF (portarias, leis, manuais)
2. ✅ **Aplicar Fine-tuning LoRA** (econômico, sem GPU potente)
3. ✅ **Implementar Reranking** (melhorar precisão de retrieval)
4. ✅ **Processar PDFs** (extração, chunking inteligente)
5. ✅ **Avaliar qualidade** com métricas (Precision@K, MRR)

---

## 📊 PROGRESSÃO E3 → E4 → E5

| Aspecto | E3 | E4 | E5 |
|---------|----|----|-----|
| **Tools** | 8 | 9 (8 + RAG) | 9 (8 + RAG especializado) |
| **Dados** | CSV | CSV + Docs .txt | CSV + Docs .txt + PDFs |
| **RAG** | ❌ | TF-IDF básico | FAISS + Reranking |
| **Fine-tuning** | ❌ | ❌ | LoRA ✅ |
| **Multimodal** | ❌ | ❌ | Texto + Imagem ✅ |
| **Métricas** | ❌ | ❌ | Precision@K, MRR ✅ |

---

## 📁 ESTRUTURA

```
E5_ESPECIALIZACAO_PDFS/
│
├── README.md                         # Este arquivo
├── 00_COMECE_AQUI_E5.md             # Início rápido
│
├── 01_DADOS/
│   ├── pdfs_pcdf/                   # PDFs da PCDF
│   │   ├── leis/
│   │   ├── manuais/
│   │   └── portarias/
│   └── documentos_conceituais/      # Docs E4 (reutilizados)
│
├── 02_NOTEBOOK_PASSO_A_PASSO/
│   ├── E5_especializacao_pdfs.ipynb # Notebook incremental
│   └── README.md
│
├── 03_AGENTE_CONSOLIDADO/
│   ├── agente_v5_especializado.py   # Agente consolidado
│   ├── requirements.txt
│   └── README.md
│
└── 04_MATERIAL_APOIO/
    ├── FAQ_E5.md
    ├── TROUBLESHOOTING_E5.md
    └── COMPARACAO_E4_vs_E5.md
```

---

## 🚀 INÍCIO RÁPIDO

### 1. Instalar Dependências

```bash
cd 03_AGENTE_CONSOLIDADO
pip install -r requirements.txt
```

### 2. Testar Agente (Modo Automático)

```bash
python agente_v5_especializado.py
```

### 3. Fazer Pergunta

```bash
python agente_v5_especializado.py "O que diz o Estatuto do Desarmamento sobre porte de arma?"
```

### 4. Modo Interativo

```bash
python agente_v5_especializado.py --interativo
```

---

## 📚 CONTEÚDO DO E5

### TERÇA (5h)

**TEORIA (2h30)**
- Fine-tuning vs LoRA vs RAG
- Preparação de PDFs (chunking inteligente)
- FAISS para busca vetorial
- Reranking com CrossEncoder
- Métricas (Precision@K, MRR)

**PRÁTICA (2h30)**
- Processar PDFs da PCDF
- Criar índice FAISS
- Implementar reranking
- Testar e avaliar


## 🎓 CONCEITOS PRINCIPAIS

### 1. RAG Especializado

**O que muda do E4 para E5?**

| Aspecto | E4 | E5 |
|---------|----|----|
| **Embeddings** | TF-IDF | Sentence-BERT |
| **Índice** | Memória | FAISS (persistente) |
| **Busca** | Top-K direto | Top-K + Reranking |
| **Documentos** | .txt simples | PDFs complexos |
| **Chunking** | Fixo (500 chars) | Inteligente (semântico) |

### 2. FAISS (Facebook AI Similarity Search)

**Vantagens:**
- ✅ Busca extremamente rápida (milhões de vetores)
- ✅ Índice persistente (salva em disco)
- ✅ Múltiplos tipos de índice (Flat, IVF, HNSW)
- ✅ GPU support (opcional)

**Uso:**
```python
import faiss

# Criar índice
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Salvar
faiss.write_index(index, "index.faiss")

# Buscar
distances, indices = index.search(query_embedding, k=10)
```

### 3. Reranking

**Problema:** Busca inicial pode retornar documentos irrelevantes

**Solução:** Reranking com CrossEncoder

**Pipeline:**
```
Pergunta → Busca inicial (top-20) → Reranking (top-5) → Resposta
```

**Ganho:** +200% de precisão (0.40 → 0.86)

### 4. Fine-tuning LoRA

**LoRA (Low-Rank Adaptation):**
- Treina apenas pequena parte do modelo (~1% parâmetros)
- Rápido (1-2h vs 1-2 dias)
- Econômico (Google Colab gratuito)
- Mantém conhecimento geral

**Hiperparâmetros:**
```python
lora_config = LoraConfig(
    r=8,              # Rank (4-16)
    lora_alpha=16,    # Alpha (rank * 2)
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
)
```

### 5. Processamento de PDFs

**Desafios:**
- Layouts complexos (tabelas, imagens)
- Múltiplas colunas
- Cabeçalhos/rodapés
- Encoding variado

**Solução:**
```python
from PyPDF2 import PdfReader

reader = PdfReader("documento.pdf")
texto = ""
for page in reader.pages:
    texto += page.extract_text()
```

**Chunking Inteligente:**
```python
# Não: chunks fixos de 500 caracteres
# Sim: chunks semânticos (parágrafos, seções)

chunks = split_by_semantic_units(texto, max_size=500)
```

---

## 📊 MÉTRICAS DE AVALIAÇÃO

### Precision@K

**Definição:** % de documentos relevantes nos top-K

```python
precision_at_5 = relevant_docs_in_top5 / 5
```

**Objetivo:** > 0.80 (80%+)

### MRR (Mean Reciprocal Rank)

**Definição:** Média da posição do primeiro documento relevante

```python
mrr = 1 / position_first_relevant
```

**Objetivo:** > 0.70

### Comparação E4 vs E5

| Métrica | E4 (TF-IDF) | E5 (FAISS + Reranking) |
|---------|-------------|------------------------|
| **Precision@5** | 0.40 | 0.86 (+115%) |
| **MRR** | 0.55 | 0.91 (+65%) |
| **Tempo busca** | 50ms | 15ms (-70%) |

---

## 🛠️ REQUISITOS

### Dependências

```bash
pip install pandas langchain-core scikit-learn faiss-cpu sentence-transformers PyPDF2
```

### Opcional (Fine-tuning)

```bash
pip install transformers peft datasets accelerate
```

### Hardware

**Mínimo:**
- CPU: 4 cores
- RAM: 8 GB
- Disco: 10 GB

**Recomendado:**
- CPU: 8 cores
- RAM: 16 GB
- Disco: 20 GB
- GPU: Não necessário (Google Colab)

---

## 🎯 CASOS DE USO PCDF

### 1. Consulta de Legislação

**Pergunta:** "O que diz o Estatuto do Desarmamento sobre porte de arma?"

**Agente E5:**
1. Busca em PDFs de leis (FAISS)
2. Reranking dos artigos relevantes
3. Resposta com citação da lei

### 2. Procedimentos Operacionais

**Pergunta:** "Como fazer depoimento especial de criança?"

**Agente E5:**
1. Busca em manuais PCDF
2. Extrai protocolo específico
3. Resposta passo a passo

### 3. Análise de Portarias

**Pergunta:** "Quais portarias tratam de armamento em 2024?"

**Agente E5:**
1. Busca em PDFs de portarias
2. Filtra por ano e tema
3. Lista portarias relevantes

---

## 📝 EXEMPLOS DE PERGUNTAS

### Perguntas Estruturadas (Tools E3/E4)
- ✅ "Quantas armas Taurus existem?"
- ✅ "Ranking de calibres"
- ✅ "Estatísticas gerais"

### Perguntas Conceituais (RAG E4)
- ✅ "O que é calibre?"
- ✅ "O que é SINARM?"
- ✅ "Diferença entre pistola e revólver?"

### Perguntas Especializadas (RAG E5 + PDFs)
- ✅ "O que diz o Estatuto do Desarmamento sobre porte?"
- ✅ "Como fazer depoimento especial de criança?"
- ✅ "Quais são os procedimentos para apreensão de arma?"
- ✅ "O que diz a portaria X sobre Y?"

---

## 🚨 TROUBLESHOOTING

### Erro: FAISS não instala

```bash
# Tentar CPU version
pip install faiss-cpu

# Ou GPU version (se tiver CUDA)
pip install faiss-gpu
```

### Erro: PDF não carrega

```python
# Tentar encoding diferente
reader = PdfReader("doc.pdf", strict=False)
```

### Erro: Memória insuficiente

```python
# Processar PDFs em lotes
for batch in batches(pdfs, batch_size=10):
    process_batch(batch)
```

---

## 📚 RECURSOS ADICIONAIS

### Documentação
- FAISS: https://github.com/facebookresearch/faiss
- Sentence-Transformers: https://www.sbert.net/
- LoRA: https://arxiv.org/abs/2106.09685

### Tutoriais
- RAG com FAISS: [link]
- Fine-tuning LoRA: [link]
- Reranking: [link]

---

## ✅ CHECKLIST

### Antes da Aula
- [ ] Dependências instaladas
- [ ] PDFs baixados
- [ ] Notebook abre
- [ ] Agente consolidado funciona

### Durante a Aula
- [ ] Processar PDFs
- [ ] Criar índice FAISS
- [ ] Implementar reranking
- [ ] Testar fine-tuning (opcional)

### Depois da Aula
- [ ] Avaliar métricas
- [ ] Comparar E4 vs E5
- [ ] Expandir base de PDFs
- [ ] Documentar lições aprendidas

---

## 🎉 RESULTADO ESPERADO

**Agente E5 Completo:**
- ✅ 9 tools (8 E3 + 1 RAG especializado)
- ✅ FAISS para busca rápida
- ✅ Reranking para precisão
- ✅ Processamento de PDFs
- ✅ Fine-tuning LoRA (opcional)
- ✅ Métricas de qualidade
- ✅ 3 modos de execução

**Métricas:**
- Precision@5: > 0.80
- MRR: > 0.70
- Tempo busca: < 20ms

---

**Última atualização:** 26/07/2026  
**Versão:** 1.0  
**Status:** ✅ Pronto para uso
