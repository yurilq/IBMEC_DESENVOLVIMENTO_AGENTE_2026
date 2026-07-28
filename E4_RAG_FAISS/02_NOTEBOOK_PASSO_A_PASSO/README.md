# 📓 Notebook Passo a Passo - E4 RAG FAISS

## 🎯 Objetivo

Implementar RAG (Retrieval-Augmented Generation) de forma **incremental**, célula por célula, dando continuidade ao E3.

---

## 📚 Estrutura do Notebook

### E4_RAG_FAISS.ipynb (35-40 células)

```
PARTE 1: RECAP E3 (células 1-5)
├── Introdução E4
├── Recap das 8 tools do E3
├── Imports necessários
├── Carregar dados SINARM
└── Testar tools E3

PARTE 2: CONCEITOS RAG (células 6-10)
├── O que é RAG?
├── Por que usar RAG?
├── Arquitetura RAG
├── RAG vs Fine-tuning
└── Casos de uso

PARTE 3: PREPARAR DOCUMENTOS (células 11-15)
├── Preparação de documentos
├── Listar documentos conceituais
├── Ler e processar textos
├── Limpar e normalizar
└── Validar documentos

PARTE 4: EMBEDDINGS (células 16-20)
├── O que são embeddings?
├── TF-IDF vs Transformers
├── Gerar embeddings TF-IDF
├── Visualizar embeddings
└── Testar similaridade

PARTE 5: FAISS (células 21-25)
├── O que é FAISS?
├── Criar índice FAISS
├── Adicionar embeddings ao índice
├── Buscar documentos similares
└── Testar retrieval

PARTE 6: TOOL RAG (células 26-30)
├── Criar tool RAG
├── Função buscar_conceito()
├── Decorator @tool
├── Testar tool RAG
└── Validar respostas

PARTE 7: INTEGRAÇÃO E3+E4 (células 31-35)
├── Roteador expandido
├── Classificar tipo de pergunta
├── Agente completo E3+E4
├── Testar perguntas estruturadas
└── Testar perguntas conceituais

PARTE 8: CONCLUSÃO (células 36-40)
├── Resumo E4
├── Comparação E3 vs E4
├── Testes finais
├── Próximos passos (E5)
└── Exercícios propostos
```

---

## 🎓 Como Usar

### Durante a Aula (5h)

#### 1. Abrir Notebook
```bash
cd 02_NOTEBOOK_PASSO_A_PASSO
jupyter notebook E4_RAG_FAISS.ipynb
```

#### 2. Executar Célula por Célula
- **NÃO** execute "Run All"
- Execute célula por célula
- Entenda cada passo
- Teste imediatamente

#### 3. Checkpoints
- **13:45** - Células 1-10 (Recap + Conceitos)
- **14:45** - Células 11-20 (Documentos + Embeddings)
- **15:45** - Células 21-30 (FAISS + Tool RAG)
- **16:45** - Células 31-35 (Integração)
- **17:45** - Células 36-40 (Conclusão)

---

## 🔄 Progressão E3 → E4

### E3 (29 células)
```
✅ 8 tools básicas
✅ Roteador simples
✅ Cache
✅ Validação
✅ Dados estruturados (CSV)
```

### E4 (35-40 células)
```
✅ Mantém 8 tools E3
✅ Adiciona tool RAG
✅ Roteador expandido
✅ Dados estruturados + não-estruturados
✅ Busca semântica
```

**Filosofia:** E4 AGREGA ao E3, não substitui!

---

## 📊 Tipos de Células

### Markdown (Teoria)
```markdown
# Conceito: O que é RAG?

RAG (Retrieval-Augmented Generation) combina:
1. Recuperação de documentos relevantes
2. Geração de respostas com LLM

Vantagens:
- Respostas baseadas em documentos
- Sem necessidade de fine-tuning
- Atualização fácil (adicionar documentos)
```

### Code (Implementação)
```python
# Gerar embeddings TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
embeddings = vectorizer.fit_transform(documentos)
print(f"Embeddings gerados: {embeddings.shape}")
```

### Code (Teste)
```python
# Testar busca
pergunta = "O que é calibre?"
resultado = buscar_conceito(pergunta)
print(resultado)
```

---

## ✅ Validação

### Checkpoint 1 (Células 1-10)
- [ ] E3 funciona?
- [ ] Entendeu RAG?
- [ ] Documentos carregados?

### Checkpoint 2 (Células 11-20)
- [ ] Documentos preparados?
- [ ] Embeddings gerados?
- [ ] Similaridade funciona?

### Checkpoint 3 (Células 21-30)
- [ ] Índice FAISS criado?
- [ ] Busca funciona?
- [ ] Tool RAG criada?

### Checkpoint 4 (Células 31-35)
- [ ] Roteador expandido?
- [ ] Agente E3+E4 funciona?
- [ ] Ambos tipos de perguntas?

### Checkpoint 5 (Células 36-40)
- [ ] Testes passam?
- [ ] Entendeu diferença E3 vs E4?
- [ ] Pronto para E5?

---

## 🎯 Resultado Esperado

Ao final do notebook, você terá:

✅ Agente que responde perguntas estruturadas (E3)  
✅ Agente que responde perguntas conceituais (E4 - RAG)  
✅ Roteador inteligente que escolhe a abordagem  
✅ Código limpo e documentado  
✅ Testes validados  

---

## 📚 Material de Apoio

### Scripts de Referência
```
04_MATERIAL_APOIO/scripts_referencia/
├── 01_preparar_documentos.py
├── 02_gerar_embeddings.py
├── 03_criar_indice_faiss.py
└── 04_testar_retrieval.py
```

**Uso:** Consulta opcional, não executar diretamente

---

## 🔄 Próximos Passos

### Após E4
1. ✅ Consolidar código em .py (03_AGENTE_CONSOLIDADO)
2. ✅ Testar agente completo
3. ✅ Preparar para E5 (Memory + Multi-Agent)

---

## 🆘 Problemas?

### Erro: "Célula não executa"
- Verificar se células anteriores foram executadas
- Reiniciar kernel: Kernel → Restart & Clear Output

### Erro: "Module not found"
```bash
pip install -r ../requirements.txt
```

### Erro: "Documentos não encontrados"
- Verificar pasta: `../01_DADOS/documentos_conceituais/`

---

**Importante:** Execute célula por célula, não "Run All"!
