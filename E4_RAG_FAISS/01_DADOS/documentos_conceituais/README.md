# 📚 Documentos Conceituais para RAG

Esta pasta contém documentos de texto usados pelo sistema RAG (Retrieval-Augmented Generation) do E4.

## 📁 Arquivos Disponíveis

### 1. `calibres_armas.txt`
**Conteúdo:** Informações completas sobre calibres de armas de fogo
- O que é calibre
- Principais calibres (pistolas, revólveres, espingardas, rifles)
- Classificação por potência
- Legislação brasileira
- Aplicações na PCDF

**Perguntas que responde:**
- "O que é calibre?"
- "Qual a diferença entre 9mm e .40?"
- "Quais calibres são permitidos para civis?"
- "O que é .38 Special?"

### 2. `marcas_armas.txt`
**Conteúdo:** Informações sobre marcas de armas de fogo
- Marcas brasileiras (Taurus, CBC, Rossi, IMBEL)
- Marcas internacionais (Glock, Beretta, Sig Sauer, etc.)
- História e características
- Uso policial e militar

**Perguntas que responde:**
- "O que é Taurus?"
- "Qual a diferença entre Glock e Beretta?"
- "Quais marcas são usadas pela PCDF?"
- "O que é IMBEL?"

### 3. `tipos_armas.txt`
**Conteúdo:** Classificação e tipos de armas de fogo
- Armas curtas (pistolas, revólveres)
- Armas longas (espingardas, rifles, carabinas)
- Mecanismos de disparo
- Classificação legal brasileira

**Perguntas que responde:**
- "Qual a diferença entre pistola e revólver?"
- "O que é uma espingarda?"
- "O que é uso restrito?"
- "Quais são os tipos de rifles?"

### 4. `sistema_sinarm.txt`
**Conteúdo:** Informações sobre o Sistema Nacional de Armas
- O que é SINARM
- Estrutura e dados registrados
- Tipos de ocorrências
- Legislação relacionada

**Perguntas que responde:**
- "O que é SINARM?"
- "Como funciona o registro de armas?"
- "O que é uma ocorrência de furto?"
- "Quais dados o SINARM armazena?"

### 5. `rag_conceitos.txt`
**Conteúdo:** Conceitos sobre RAG (Retrieval-Augmented Generation)
- O que é RAG
- Como funciona
- Embeddings e bancos vetoriais
- Implementação e boas práticas

**Perguntas que responde:**
- "O que é RAG?"
- "Como funciona busca semântica?"
- "O que são embeddings?"
- "O que é FAISS?"

## 🎯 Como Usar

### No Notebook E4
```python
# 1. Carregar documentos
documentos = carregar_documentos_conceituais()

# 2. Criar índice RAG
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documentos)

# 3. Buscar
def buscar_rag(pergunta, k=3):
    query_vec = vectorizer.transform([pergunta])
    similarities = cosine_similarity(query_vec, tfidf_matrix)
    top_k = similarities.argsort()[0][-k:][::-1]
    return [documentos[i] for i in top_k]

# 4. Usar
docs_relevantes = buscar_rag("O que é calibre?")
```

### No Agente Consolidado
```python
# Tool RAG
@tool
def buscar_conhecimento(pergunta: str) -> str:
    """Busca informações conceituais sobre armas."""
    docs = buscar_rag(pergunta, k=3)
    return "\n\n".join(docs[:500])  # Primeiros 500 chars de cada
```

## 📊 Estatísticas

| Arquivo | Linhas | Palavras | Tamanho |
|---------|--------|----------|---------|
| calibres_armas.txt | ~400 | ~3.500 | ~25 KB |
| marcas_armas.txt | ~500 | ~4.000 | ~30 KB |
| tipos_armas.txt | ~600 | ~5.000 | ~35 KB |
| sistema_sinarm.txt | ~450 | ~3.800 | ~28 KB |
| rag_conceitos.txt | ~550 | ~4.500 | ~32 KB |
| **TOTAL** | **~2.500** | **~20.800** | **~150 KB** |

## 🔍 Exemplos de Perguntas

### Perguntas Conceituais (RAG)
✅ "O que é calibre?"
✅ "Qual a diferença entre pistola e revólver?"
✅ "O que é SINARM?"
✅ "Quais marcas são brasileiras?"
✅ "O que é uso restrito?"

### Perguntas sobre Dados (Tools E3)
✅ "Quantas armas Taurus existem?"
✅ "Qual o calibre mais comum?"
✅ "Quantas armas foram roubadas?"
✅ "Ranking de marcas"
✅ "Estatísticas gerais"

## 🎓 Progressão E3 → E4

### E3: Apenas Dados Estruturados
```
Pergunta: "Quantas armas Taurus?"
→ Tool: contar_armas_marca("TAURUS")
→ Resposta: "45.234 armas"

Pergunta: "O que é Taurus?"
→ ❌ Não consegue responder
```

### E4: Dados + RAG
```
Pergunta: "Quantas armas Taurus?"
→ Roteador: dados estruturados
→ Tool: contar_armas_marca("TAURUS")
→ Resposta: "45.234 armas"

Pergunta: "O que é Taurus?"
→ Roteador: conceitual
→ RAG: busca em marcas_armas.txt
→ Resposta: "Taurus é a maior fabricante..."
```

## 🛠️ Manutenção

### Adicionar Novo Documento
1. Criar arquivo `.txt` nesta pasta
2. Escrever conteúdo em formato texto simples
3. Recarregar documentos no notebook
4. Recriar índice RAG

### Atualizar Documento Existente
1. Editar arquivo `.txt`
2. Recarregar documentos no notebook
3. Recriar índice RAG

### Formato Recomendado
```
# Título Principal

## Subtítulo

### Seção

Texto explicativo com parágrafos bem estruturados.

**Negrito** para ênfase.

- Lista de itens
- Outro item

1. Lista numerada
2. Outro item
```

## 📝 Boas Práticas

### Conteúdo
- ✅ Texto claro e objetivo
- ✅ Parágrafos curtos (3-5 linhas)
- ✅ Estrutura hierárquica (títulos)
- ✅ Exemplos práticos
- ✅ Informações verificadas

### Formato
- ✅ Encoding UTF-8
- ✅ Quebras de linha consistentes
- ✅ Sem formatação complexa
- ✅ Markdown simples

### Tamanho
- ✅ Documentos de 20-50 KB
- ✅ Chunks de 200-500 tokens
- ✅ Overlap de 10-20%

## 🚀 Próximos Passos

### Documentos Futuros
- [ ] `legislacao_armas.txt` - Leis e decretos
- [ ] `procedimentos_pcdf.txt` - Procedimentos operacionais
- [ ] `casos_uso.txt` - Casos de uso reais
- [ ] `glossario.txt` - Termos técnicos
- [ ] `faq.txt` - Perguntas frequentes

### Melhorias
- [ ] Adicionar metadados (autor, data, versão)
- [ ] Criar índice automático
- [ ] Validação de qualidade
- [ ] Versionamento

## 📚 Referências

### Fontes
- Estatuto do Desarmamento (Lei 10.826/2003)
- Decreto 11.615/2023
- Manuais técnicos de fabricantes
- Documentação Polícia Federal
- Literatura especializada

### Validação
- Revisado por especialistas em armamento
- Atualizado conforme legislação vigente
- Verificado com fontes oficiais

---

**Última atualização:** 26/07/2026  
**Total de documentos:** 5  
**Status:** ✅ Completo e funcional
