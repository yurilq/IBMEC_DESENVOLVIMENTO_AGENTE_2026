# 🚀 E4 - RAG com FAISS (Parte Prática)

**MBA IA Generativa PCDF - IBMEC**  
**Encontro 4:** RAG + Busca Semântica

---

## 🎯 Objetivos

- Implementar RAG (Retrieval-Augmented Generation)
- Usar FAISS para busca vetorial
- Gerar embeddings com TF-IDF
- Integrar busca semântica com tools E3
- Responder perguntas conceituais

---

## 📁 Estrutura

```
E4_RAG_FAISS/
├── 01_DADOS/
│   ├── DADOS_SINARM/              # Dados estruturados (E3)
│   └── documentos_conceituais/    # Documentos para RAG
│
├── 02_NOTEBOOK_PASSO_A_PASSO/
│   ├── scripts_auxiliares/        # Pipeline RAG
│   │   ├── 01_preparar_documentos.py
│   │   ├── 02_gerar_embeddings.py
│   │   ├── 03_criar_indice_faiss.py
│   │   └── 04_testar_retrieval.py
│   └── E4_RAG_FAISS.ipynb        # Notebook completo
│
├── 03_AGENTE_CONSOLIDADO/
│   ├── agente_v4_7_rag_fewshot_cot.py  # Agente final
│   ├── tool_rag_tfidf.py               # Tool RAG
│   ├── tools_basicas_v2.py             # Tools E3
│   └── config_llm.py                   # Config LLM
│
└── 04_UTILITARIOS/
    ├── verificar_ambiente.py
    └── executar_completo.bat
```

---

## 🚀 Como Usar

### Passo 1: Configurar Ambiente

```bash
# 1. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Verificar ambiente
python 04_UTILITARIOS/verificar_ambiente.py
```

---

### Passo 2: Pipeline RAG

Execute os scripts na ordem:

```bash
cd 02_NOTEBOOK_PASSO_A_PASSO/scripts_auxiliares

# 1. Preparar documentos
python 01_preparar_documentos.py

# 2. Gerar embeddings (TF-IDF)
python 02_gerar_embeddings.py

# 3. Criar índice FAISS
python 03_criar_indice_faiss.py

# 4. Testar retrieval
python 04_testar_retrieval.py
```

---

### Passo 3: Usar Agente Completo

```bash
cd 03_AGENTE_CONSOLIDADO

# Modo 1: Testes automáticos
python agente_v4_7_rag_fewshot_cot.py

# Modo 2: Pergunta única
python agente_v4_7_rag_fewshot_cot.py "O que é calibre?"

# Modo 3: Modo interativo
python agente_v4_7_rag_fewshot_cot.py --interativo
```

---

## 🛠️ Funcionalidades

### Tools do E3 (Mantidas)
1. `contar_armas_marca` - Conta por marca
2. `contar_armas_calibre` - Conta por calibre
3. `contar_armas_tipo` - Conta por tipo
4. `contar_armas_combinado` - Marca + tipo
5. `ranking_marcas` - TOP 5 marcas
6. `ranking_calibres` - TOP 5 calibres
7. `estatisticas_gerais` - Resumo completo
8. `distribuicao_marca_por_tipo` - Distribuição

### Tool RAG (Nova)
9. `buscar_conceito` - Busca semântica em documentos

---

## 💡 Exemplos

### Perguntas Estruturadas (usa tools E3)
```
✅ "Quantas armas Taurus?"
✅ "Top 5 marcas"
✅ "Glock roubadas"
✅ "Distribuição Beretta"
```

### Perguntas Conceituais (usa RAG)
```
✅ "O que é calibre?"
✅ "Como funciona SINARM?"
✅ "Diferença entre furto e roubo?"
✅ "O que é uma arma de fogo?"
```

---

## 📋 Requisitos

```txt
pandas>=2.0.0
langchain-core>=0.3.0
scikit-learn>=1.3.0
faiss-cpu>=1.7.4
langchain-ollama>=0.1.0
```

---

## 🔄 Progressão E3 → E4

| Aspecto | E3 | E4 |
|---------|----|----|
| **Tools** | 8 básicas | 8 + 1 RAG |
| **Dados** | Estruturados | Estruturados + Não-estruturados |
| **Busca** | Filtros pandas | Filtros + Busca semântica |
| **Perguntas** | Estruturadas | Estruturadas + Conceituais |

---

## 📚 Material Teórico

Consulte a pasta de disciplina para:
- Conceitos de RAG
- Conceitos de FAISS
- Conceitos de Embeddings
- Roteiro da aula
- Material de apoio

**Localização:** `MODULO 01\00_DISCIPLINAS\DISCIPLINA_1_DESENVOLVIMENTO_AGENTE\E4_RAG_FAISS`

---

## 🆘 Suporte

- **FAQ:** Consulte material teórico
- **Troubleshooting:** Consulte material teórico
- **Dúvidas:** Professor do encontro

---

**Última atualização:** 26/07/2026  
**Versão:** 4.7  
**Status:** ✅ Reorganizado padrão IBMEC
