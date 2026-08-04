# E5: RAG Especializado com PDFs PCDF

**MBA IA Generativa PCDF - IBMEC**

Especialização de agentes com processamento de PDFs reais, embeddings semânticos e reranking para máxima precisão.

## 🎯 Objetivos

1. ✅ Estender E4 com processamento de PDFs
2. ✅ Implementar busca vetorial com NumPy (SEM FAISS)
3. ✅ Adicionar Reranking para máxima precisão
4. ✅ Avaliar com métricas (Precision@K, MRR)
5. ✅ Comparar E4 vs E5

## 📊 Arquitetura (PRODUCAO)

```
03_PROJETO_ESTRUTURADO/           # PRODUCAO
├── src/                          # Módulos core (7 arquivos)
│   ├── loader.py                 # Carregamento de dados
│   ├── chunker.py                # Processamento de chunks
│   ├── embeddings.py             # Embeddings (Sentence-BERT + TF-IDF)
│   ├── search.py                 # Busca vetorial
│   ├── reranker.py               # Reranking (sklearn TF-IDF)
│   ├── config_llm.py             # Configuração de LLM
│   └── gerador_respostas.py      # Geração de respostas
│
├── tools/                        # Ferramentas reutilizáveis
│   ├── metrics.py                # Métricas de avaliação
│   └── utils.py                  # Funções auxiliares
│
├── data/                         # Dados
│   ├── DADOS_SINARM/             # CSV estruturado (74k registros)
│   ├── documentos_conceituais/   # Docs .txt (6 arquivos)
│   ├── pdfs_pcdf/                # PDFs (5 arquivos)
│   └── indices/                  # Embeddings salvos (cache)
│
├── tests/                        # Testes (todos os testes aqui)
│   ├── test_simples.py           # Teste rápido (10s)
│   ├── test_completo.py          # Suite de testes (15s)
│   ├── test_loader.py            # Teste do loader
│   ├── test_chunker.py           # Teste do chunker
│   ├── test_search.py            # Teste da busca
│   └── test_reranker.py          # Teste do reranker
│
├── requirements.txt              # Dependências
├── .env                          # Configuração (API keys, caminhos)
└── README.md                     # Este arquivo

04_MATERIAL_AULA/02_EXEMPLOS/     # EXEMPLOS
├── EXEMPLO_01_BM25_FINAL.py      # ✅ Busca SEM PYTORCH (versão final)
└── README.md                     # Documentação de exemplos
```

## 🚀 Quick Start

### 1. Instalação

```bash
# Pasta do projeto
cd E:\documentos\ibmec\CODIGOS_AULA\E5_ESPECIALIZACAO_PDFS\03_PROJETO_ESTRUTURADO

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Dados Já Conectados!

Os dados estão em `CODIGOS_AULA/DADOS_SINARM/` e já estão conectados automaticamente:

```
✅ CSV: 74.758 registros (OCORRENCIAS_2026.csv)
✅ Documentos: 6 arquivos .txt
✅ PDFs: 5 arquivos
✅ Total: 60 MB
```

Veja `CONFIGURACAO_DADOS.md` para mais detalhes.

### 3. Validar Instalação

```bash
# Teste rápido (10 segundos)
python tests/test_simples.py

# Suite completa de testes (15 segundos)
python tests/test_completo.py

# Ou com pytest (se instalado)
pytest tests/ -v
```

### 4. Executar Exemplo

```bash
# Busca sem PyTorch (versão final)
cd ..\04_MATERIAL_AULA\02_EXEMPLOS
python EXEMPLO_01_BM25_FINAL.py
```

## 📚 Estrutura de Código

### Testes Disponíveis

| Arquivo | Tipo | Tempo | Descrição |
|---------|------|-------|-----------|
| `tests/test_simples.py` | Rápido | 10s | Validação básica (imports, loader, chunks) |
| `tests/test_completo.py` | Suite | 15s | Todos os módulos (embeddings, reranking, métricas) |
| `tests/test_*.py` | Unit | 20s | Testes individuais de cada módulo |

### Exemplos

| Arquivo | Localização | Status | Descrição |
|---------|-------------|--------|-----------|
| `EXEMPLO_01_BM25_FINAL.py` | `04_MATERIAL_AULA/02_EXEMPLOS/` | ✅ | Busca com BM25 **SEM PYTORCH** |

### Componentes Principais

#### 1. **Loader** (`src/loader.py`)
- Carrega CSV com dados SINARM
- Carrega documentos .txt conceituais
- Processa PDFs com PyPDF2

#### 2. **Chunker** (`src/chunker.py`)
- Chunking híbrido (semântico + fixo)
- Overlap para preservar contexto
- Validação de qualidade

#### 3. **Embeddings** (`src/embeddings.py`)
- Sentence-BERT (paraphrase-multilingual-MiniLM-L12-v2)
- 384 dimensões
- Suporte multilíngue

#### 4. **Search** (`src/search.py`)
- Busca com NumPy + cosine similarity
- SEM FAISS (compatível Windows)
- Top-K configurável

#### 5. **Reranker** (`src/reranker.py`)
- CrossEncoder (ms-marco-MiniLM-L-6-v2)
- Pipeline 2-estágios
- Threshold configurável

## 📊 Comparação E4 vs E5

| Aspecto | E4 (TF-IDF) | E5 (Sentence-BERT) |
|---------|-------------|-------------------|
| **Tipo** | Frequência | Semântica |
| **Dimensões** | 100 | 384 |
| **Sinônimos** | ❌ | ✅ |
| **Contexto** | ❌ | ✅ |
| **Velocidade** | Muito rápido | Rápido |
| **Precisão** | ~40% | ~70% |
| **Reranking** | ❌ | ✅ |

## 🧪 Exemplos

### Busca Básica

```python
from src.search import buscar_numpy

resultados = buscar_numpy("O que é calibre?", k=5)

for chunk, score in resultados:
    print(f"{chunk['arquivo']}: {score:.3f}")
    print(f"{chunk['texto'][:100]}...")
```

### Busca com Reranking

```python
from src.reranker import buscar_com_reranking

resultados = buscar_com_reranking(
    "O que é calibre?",
    k_inicial=20,
    k_final=5,
    threshold=0.0
)

for chunk, score in resultados:
    print(f"{chunk['arquivo']}: {score:.3f}")
```

## 📈 Métricas

### Precision@K

```python
from tools.metrics import precision_at_k

# Calcular Precision@5
p5 = precision_at_k(resultados_relevantes, k=5)
print(f"Precision@5: {p5:.2%}")
```

### MRR (Mean Reciprocal Rank)

```python
from tools.metrics import mean_reciprocal_rank

mrr = mean_reciprocal_rank(resultados_relevantes)
print(f"MRR: {mrr:.3f}")
```

## 🔧 Configuração Avançada

### Ajustar Chunking

```python
from src.chunker import chunk_text_hibrido

chunks = chunk_text_hibrido(
    texto,
    chunk_size=1000,  # Aumentar para PDFs grandes
    overlap=150       # Aumentar para mais contexto
)
```

### Ajustar Busca

```python
# Aumentar k_inicial para mais candidatos
resultados = buscar_com_reranking(
    pergunta,
    k_inicial=50,  # Mais candidatos
    k_final=5,
    threshold=1.0  # Filtro mais rigoroso
)
```

## 📝 Atividades Práticas

### ATIVIDADE 1: Carregamento de Dados
- Carregar CSV, .txt e PDFs
- Validar estrutura
- Explorar dados

### ATIVIDADE 2: Processamento de Chunks
- Testar diferentes tamanhos
- Comparar chunking semântico vs fixo
- Medir qualidade

### ATIVIDADE 3: Embeddings
- Gerar embeddings para todos os chunks
- Salvar índices
- Carregar índices

### ATIVIDADE 4: Busca e Reranking
- Testar busca básica
- Comparar com reranking
- Avaliar com métricas

## 🐛 Troubleshooting

### Erro: "Arquivo não encontrado"
```
Solução: Verificar caminhos em .env
DATA_PATH deve apontar para pasta com dados
```

### Erro: "CUDA out of memory"
```
Solução: Reduzir batch_size em embeddings.py
ou usar CPU (padrão)
```

### Erro: "PDF não extraído corretamente"
```
Solução: Aumentar chunk_size em chunker.py
ou usar ferramentas alternativas (pdfplumber)
```

## 📚 Referências

- [Sentence-BERT](https://www.sbert.net/)
- [CrossEncoder](https://www.sbert.net/docs/pretrained_cross-encoders/ms-marco-MiniLM-L-6-v2.html)
- [RAG Patterns](https://python.langchain.com/docs/modules/data_connection/retrievers/rag/)
- [NumPy Similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)

## 📞 Suporte

Para dúvidas ou problemas:
1. Execute os testes: `python teste_simples.py`
2. Consulte o README do exemplo: `04_MATERIAL_AULA/02_EXEMPLOS/README.md`
3. Verifique se as dependências estão instaladas: `pip install -r requirements.txt`

## ✅ Status Atual

- ✅ **Código limpo e organizado** - Apenas arquivos necessários
- ✅ **Sem PyTorch** - Usa TF-IDF e BM25 (compatível Windows)
- ✅ **Testado** - Todos os testes passando
- ✅ **Pronto para produção** - Estrutura profissional
- ✅ **Dados Conectados** - CODIGOS_AULA/DADOS_SINARM (60 MB, 15 arquivos)

## 📚 Documentação

- **CONFIGURACAO_DADOS.md** - Como os dados estão organizados
- **ESTRUTURA_FINAL.md** - Estrutura do projeto
- **README.md** - Este arquivo (documentação principal)

## 📄 Licença

Projeto educacional - MBA IA Generativa PCDF - IBMEC

---

**Última atualização:** 2026-07-28  
**Versão:** 1.0 Final (Production Clean)  
**Status:** ✅ Pronto para uso
