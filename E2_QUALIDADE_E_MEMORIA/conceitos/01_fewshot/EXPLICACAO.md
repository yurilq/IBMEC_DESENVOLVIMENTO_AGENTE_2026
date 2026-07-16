# 📚 FEW-SHOT LEARNING - EXPLICAÇÃO COMPLETA

## 🎯 O QUE É FEW-SHOT LEARNING?

**Few-Shot Learning** é uma técnica de prompt engineering que melhora a performance de LLMs fornecendo **exemplos de entrada-saída** no prompt, sem necessidade de fine-tuning.

### Comparação:

| Abordagem | Exemplos | Treino | Custo | Tempo | Accuracy |
|-----------|----------|--------|-------|-------|----------|
| **Zero-Shot** | 0 | Não | R$ 0 | 0 | 60-70% |
| **Few-Shot** | 3-5 | Não | R$ 0 | 0 | 75-90% |
| **Fine-Tuning** | 1000+ | Sim | R$ 5.000+ | 2-7 dias | 90-95% |

**Conclusão**: Few-Shot é o **melhor custo-benefício** para a maioria dos casos.

---

## 🧠 COMO FUNCIONA?

LLMs aprendem **por analogia**. Quando você fornece exemplos, o modelo:
1. Identifica **padrões** nos exemplos
2. **Generaliza** o padrão para novas queries
3. **Imita** a estrutura de resposta dos exemplos

### Exemplo Visual:

```
┌─────────────────────────────────────────────────────────────┐
│ PROMPT ZERO-SHOT (60% accuracy)                            │
├─────────────────────────────────────────────────────────────┤
│ System: Responda perguntas sobre armas SINARM.             │
│                                                             │
│ User: Quantas Taurus foram furtadas no DF?                 │
│                                                             │
│ LLM: [TEM QUE ADIVINHAR]                                   │
│   → Pode escolher dataset errado                           │
│   → Pode esquecer filtros                                  │
│   → Pode não formatar bem                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROMPT FEW-SHOT (85% accuracy)                             │
├─────────────────────────────────────────────────────────────┤
│ System: Responda perguntas sobre armas SINARM.             │
│                                                             │
│ EXEMPLO 1:                                                  │
│   User: Quantas Glock foram furtadas em SP?                │
│   Thought: Buscar OCORRENCIAS: marca=Glock, tipo=Furto,    │
│            uf=SP                                            │
│   Action: buscar_ocorrencias("marca:Glock")                │
│   Answer: 127 pistolas Glock foram furtadas em SP.         │
│                                                             │
│ EXEMPLO 2: [...]                                            │
│ EXEMPLO 3: [...]                                            │
│                                                             │
│ User: Quantas Taurus foram furtadas no DF?                 │
│                                                             │
│ LLM: [IMITA OS EXEMPLOS]                                   │
│   → Escolhe OCORRENCIAS (correto!)                         │
│   → Aplica filtros marca + tipo + uf (correto!)           │
│   → Formata resposta clara (correto!)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ QUANDO USAR FEW-SHOT?

### Use Few-Shot quando:
- ✅ Tarefa tem **padrão claro** (ex: classificação, extração, formatação)
- ✅ Você tem **3-10 exemplos de alta qualidade**
- ✅ Latência extra (+10-30%) é **aceitável**
- ✅ Não quer investir em **fine-tuning**

### NÃO use Few-Shot quando:
- ❌ Tarefa é **trivial** (Zero-Shot já funciona bem)
- ❌ Tarefa é **muito complexa** (precisa fine-tuning)
- ❌ Latência é **crítica** (prompt maior = mais tokens)
- ❌ Não tem **exemplos de qualidade**

---

## 🎨 ANATOMIA DE UM BOM EXEMPLO

### Critérios de Qualidade:

1. **Realista**: Query que usuário realmente faria
   - ✅ "Quantas pistolas Taurus foram furtadas no DF?"
   - ❌ "Execute SQL SELECT * FROM armas WHERE marca='Taurus'"

2. **Completo**: Mostra TODO o fluxo (input → raciocínio → ação → output)
   - ✅ Input + Thought + Action + Observation + Answer
   - ❌ Apenas Input + Answer (pula raciocínio)

3. **Preciso**: Usa campos, datasets, valores corretos
   - ✅ buscar_ocorrencias("marca:Taurus")
   - ❌ buscar_armas("Taurus") [tool inexistente]

4. **Formatado**: Resposta clara, com fonte, números precisos
   - ✅ "47 pistolas Taurus .380 furtadas. Fonte: SINARM/OCORRENCIAS."
   - ❌ "Encontrei algumas armas" [vago]

5. **Diverso**: Exemplos cobrem diferentes cenários
   - ✅ Exemplo 1: OCORRENCIAS, Exemplo 2: PORTES, Exemplo 3: REGISTROS
   - ❌ 3 exemplos idênticos (só muda a marca)

---

## 📊 IMPACTO ESPERADO

### Métricas Típicas:

| Métrica | Zero-Shot | Few-Shot (3 ex) | Few-Shot (5 ex) |
|---------|-----------|-----------------|-----------------|
| Accuracy | 60-70% | 75-85% | 80-90% |
| Latência | 2.0s | 2.5s (+25%) | 3.0s (+50%) |
| Erros | 30-40% | 15-25% | 10-20% |
| Tokens | 500 | 1.200 (+140%) | 1.800 (+260%) |

**Trade-off**: +15-20pp accuracy por +0.5-1.0s latência

---

## 🔧 IMPLEMENTAÇÃO

### 1. Criar Exemplos (ATIVIDADE_1B)
```python
exemplo = {
    "input": "Query do usuário",
    "thought": "Raciocínio",
    "action": "Tool call",
    "observation": "Resultado",
    "output": "Resposta formatada"
}
```

### 2. Formatar no Prompt (ATIVIDADE_1C)
```python
def formatar_exemplos_fewshot(exemplos):
    texto = "## EXEMPLOS:\n\n"
    for ex in exemplos:
        texto += f"User: {ex['input']}\n"
        texto += f"Thought: {ex['thought']}\n"
        texto += f"Action: {ex['action']}\n"
        texto += f"Answer: {ex['output']}\n\n"
    return texto
```

### 3. Integrar ao Agente
```python
prompt = base_prompt + formatar_exemplos_fewshot(exemplos)
agent = create_react_agent(llm, tools, prompt)
```

---

## 📈 OTIMIZAÇÕES

### 1. **Seleção Dinâmica** (Avançado)
Em vez de sempre usar os mesmos 3 exemplos, escolha os **mais relevantes** para cada query:

```python
def selecionar_exemplos_relevantes(query, exemplos, k=3):
    """Seleciona k exemplos mais similares à query."""
    embeddings_exemplos = embed(exemplos)
    embedding_query = embed(query)
    scores = cosine_similarity(embedding_query, embeddings_exemplos)
    top_k = argsort(scores)[:k]
    return [exemplos[i] for i in top_k]
```

**Vantagem**: Accuracy +5-10pp, latência constante (sempre k exemplos)

### 2. **Compressão de Exemplos**
Remover tokens desnecessários:

```python
# Antes (verboso)
"Thought: Preciso buscar no dataset OCORRENCIAS com os seguintes filtros: marca igual a Taurus, tipo igual a Furto, uf igual a DF."

# Depois (compacto)
"Thought: OCORRENCIAS: marca=Taurus, tipo=Furto, uf=DF"
```

**Vantagem**: -30% tokens, latência -15%, accuracy igual

### 3. **Exemplos Adversariais**
Incluir exemplos de casos **difíceis** que o modelo costuma errar:

```python
exemplos_adversariais = [
    {
        "input": "Quantas armas .380 existem?",  # Ambíguo!
        "thought": "Query ambígua - qual dataset? Vou perguntar.",
        "output": "Preciso de mais informações. Você quer OCORRENCIAS (furtos/apreensões), REGISTROS (armas registradas) ou PORTES (portes válidos)?"
    }
]
```

**Vantagem**: Reduz respostas erradas em casos ambíguos

---

## 🎯 CHECKLIST FINAL

Antes de usar Few-Shot em produção:

- [ ] Tenho 3-5 exemplos de **alta qualidade**?
- [ ] Exemplos cobrem **cenários diversos**?
- [ ] Validei **accuracy** com A/B test (baseline vs few-shot)?
- [ ] Trade-off latência é **aceitável**?
- [ ] Custo de tokens extra está **dentro do orçamento**?
- [ ] Documentei **quais exemplos usei** (para manutenção)?
- [ ] Testei **edge cases** (queries ambíguas, dados ausentes)?

---

## 📚 REFERÊNCIAS

- [Language Models are Few-Shot Learners (GPT-3 paper)](https://arxiv.org/abs/2005.14165)
- [Few-Shot Learning with Retrieval Augmented Language Models](https://arxiv.org/abs/2208.03299)
- [Prompt Engineering Guide - Few-Shot Prompting](https://www.promptingguide.ai/techniques/fewshot)

---

## 🎓 PRÓXIMOS PASSOS

Agora que domina Few-Shot, evolua para:
1. **Chain-of-Thought (CoT)**: Raciocínio passo-a-passo explícito
2. **Retrieval-Augmented Few-Shot**: Buscar exemplos dinamicamente
3. **Few-Shot + Fine-Tuning**: Combinar ambas técnicas

➡️ **PRÓXIMA ATIVIDADE**: ATIVIDADE_2A - Chain-of-Thought (CoT)
