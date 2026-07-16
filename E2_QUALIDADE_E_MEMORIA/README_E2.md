# 📘 E2: QUALIDADE E MEMÓRIA - GUIA COMPLETO

## 🎯 Visão Geral

**Encontro 2** foca em **melhorar qualidade e adicionar contexto** aos agentes ReAct desenvolvidos no E1.

### Tópicos Principais:
1. **Few-Shot Learning** (40 min prática)
2. **Chain-of-Thought - CoT** (45 min prática)
3. **Memory Conversacional** (10 min prática)
4. **Security Basics** (10 min prática)

### Objetivos de Aprendizagem:
- ✅ Implementar Few-Shot para melhorar accuracy (+15-30%)
- ✅ Usar CoT para queries complexas (raciocínio explícito)
- ✅ Adicionar memória conversacional (contexto multi-turno)
- ✅ Proteger agente contra injection attacks

---

## 📂 Estrutura do E2

```
E2_QUALIDADE_E_MEMORIA/
│
├── README_E2.md                    # Este arquivo
├── INDEX.md                        # Navegação rápida
│
├── conceitos/                      # 📚 Práticas modulares (10 atividades)
│   │
│   ├── 01_fewshot/                 # Few-Shot Learning (4 atividades)
│   │   ├── ATIVIDADE_1A_baseline.py         # Medir Zero-Shot
│   │   ├── ATIVIDADE_1B_criar_exemplos.py   # Criar exemplos
│   │   ├── ATIVIDADE_1C_implementar.py      # Implementar v2.0
│   │   ├── ATIVIDADE_1D_comparar.py         # Medir impacto
│   │   └── EXPLICACAO.md                    # Teoria completa
│   │
│   ├── 02_cot/                     # Chain-of-Thought (4 atividades)
│   │   ├── ATIVIDADE_2A_classificar.py      # Simples vs Complexa
│   │   ├── ATIVIDADE_2B_trace_manual.py     # Escrever CoT
│   │   ├── ATIVIDADE_2C_implementar.py      # Implementar v2.5
│   │   ├── ATIVIDADE_2D_parser.py           # Parser (opcional)
│   │   └── template_cot.txt                 # Template reutilizável
│   │
│   ├── 03_memory_conversacional/   # Memory (1 atividade)
│   │   └── ATIVIDADE_3A_buffer.py           # Short-term buffer
│   │
│   └── 04_security_basica/         # Security (2 atividades)
│       ├── ATIVIDADE_4A_validation.py       # Input validation
│       └── ATIVIDADE_4B_testar_ataque.py    # Testar ataques
│
├── solucao_final/                  # 🎯 Versões integradas
│   ├── agente_v2.0_fewshot.py      # v2.0 (Few-Shot)
│   ├── agente_v2.5_cot.py          # v2.5 (Few-Shot + CoT)
│   ├── COMPARACAO_V1_V2.py         # Script comparativo
│   └── README_SOLUCAO.md           # Documentação
│
└── demo_professor/                 # 👨‍🏫 Material do professor
    ├── DEMO_AULA.py                # Demo ao vivo
    ├── ROTEIRO_PROFESSOR.md        # Timing aula
    └── resultados_esperados.json   # Backup resultados
```

---

## 🎓 Roteiro de Estudo

### 📍 BLOCO 1: Few-Shot Learning (80 minutos)

**Teoria (10 min)**: O que é Few-Shot? Quando usar? Trade-offs?
- Leia: `conceitos/01_fewshot/EXPLICACAO.md`

**Prática (70 min)**:
1. **ATIVIDADE 1A** (20 min): Medir baseline v1.8 (Zero-Shot)
   - Execute 5 queries teste
   - Preencha tabela de resultados
   - Calcule accuracy, latência, taxa erro

2. **ATIVIDADE 1B** (20 min): Criar exemplos Few-Shot
   - Entenda anatomia de um bom exemplo
   - Crie 3 exemplos de alta qualidade
   - Valide com checklist (7 critérios)

3. **ATIVIDADE 1C** (25 min): Implementar v2.0 (Few-Shot)
   - Integre exemplos ao prompt system
   - Teste agente v2.0
   - Compare mentalmente com v1.8

4. **ATIVIDADE 1D** (15 min): Comparar v1.8 vs v2.0
   - Execute 5 queries no v2.0
   - Calcule Δ accuracy, Δ latência
   - Conclusão: Few-Shot vale a pena?

**Resultado esperado**: Agente v2.0 com +15-30% accuracy

---

### 📍 BLOCO 2: Chain-of-Thought (90 minutos)

**Teoria (15 min)**: O que é CoT? Quando usar? Como implementar?
- Leia seção CoT no `TOPICOS_DETALHADOS_E2.md`

**Prática (75 min)**:
1. **ATIVIDADE 2A** (15 min): Classificar queries (Simples vs Complexa)
   - Analise 10 queries SINARM
   - Critérios: datasets, filtros, cálculos, etapas
   - Escala: SIMPLES (0-2pt), MÉDIA (3-5pt), COMPLEXA (6+pt)

2. **ATIVIDADE 2B** (10 min): Escrever trace CoT manualmente
   - Escolha query complexa
   - Escreva: Thought → Action → Observation → Answer
   - Valide com checklist (12 pontos)

3. **ATIVIDADE 2C** (20 min): Implementar v2.5 (Few-Shot + CoT)
   - Adicione template CoT ao prompt
   - Adicione exemplos Few-Shot+CoT
   - Teste com query complexa

4. **ATIVIDADE 2D** (10 min - OPCIONAL): Parser CoT
   - Extrair seções do trace
   - Estruturar em JSON
   - Usar para debugging/métricas

**Resultado esperado**: Agente v2.5 com raciocínio explícito

---

### 📍 BLOCO 3: Memory + Security (30 minutos)

**Memory (10 min)**:
- **ATIVIDADE 3A**: Implementar ShortTermMemory (buffer)
  - Classe com buffer de 5 mensagens
  - Testar conversação multi-turno
  - Comparar com/sem memory

**Security (20 min)**:
- **ATIVIDADE 4A** (5 min): Input Validation
  - Criar InputValidator
  - Adicionar palavras proibidas (~30 termos)
  - Detectar SQL injection, prompt injection

- **ATIVIDADE 4B** (5 min): Testar Ataques
  - Executar 10 ataques pré-definidos
  - Verificar bloqueios
  - Analisar logs de segurança

**Resultado esperado**: Agente protegido contra ataques básicos

---

## 🚀 Como Usar Este Material

### Para Alunos:

1. **Siga ordem**: 1A → 1B → 1C → 1D → 2A → 2B → 2C → 3A → 4A → 4B
2. **Faça as atividades**: Não apenas leia, **execute os scripts**!
3. **Anote dúvidas**: Pergunte no fórum ou ao professor
4. **Compare resultados**: Suas métricas vs esperadas

### Para Professores:

1. **Use demo_professor/**: Material para demonstração ao vivo
2. **Ajuste timing**: Atividades têm duração sugerida, adapte
3. **Foque em hands-on**: 70% prática, 30% teoria
4. **Mostre trade-offs**: Cada técnica tem custo (latência, tokens)

---

## 📊 Progressão de Versões

```
v1.8 (E1 - Baseline)
  ├─ ReAct básico
  ├─ 4 tools SINARM
  ├─ Error handling
  └─ Accuracy: 60-70%

v2.0 (E2 - Few-Shot)  ← ATIVIDADE 1C
  ├─ v1.8 + Few-Shot (3 exemplos)
  ├─ Accuracy: 75-85% (+15pp)
  └─ Latência: +10%

v2.5 (E2 - Few-Shot + CoT)  ← ATIVIDADE 2C
  ├─ v2.0 + Chain-of-Thought
  ├─ Accuracy: 80-90% (+5-10pp em queries complexas)
  ├─ Raciocínio explícito
  └─ Latência: +30%

v2.5+ (E2 - Completo)  ← SOLUÇÃO FINAL
  ├─ v2.5 + Memory (buffer 5)
  ├─ v2.5 + Security (input validation)
  ├─ Conversação multi-turno
  └─ Protegido contra ataques básicos

v3.0 (E3 - LangChain/CrewAI)  ← PRÓXIMO ENCONTRO
  └─ Refactoring com frameworks
```

---

## 🔗 Links Úteis

### Dentro do Projeto:
- [TOPICOS_DETALHADOS_E2.md](../TOPICOS_DETALHADOS_E2.md) - Especificação completa
- [PROPOSTA_E2_OTIMIZADA.md](../PROPOSTA_E2_OTIMIZADA.md) - Planejamento original
- [SLIDES_E2_ESTRUTURA_GAMMA.md](../SLIDES_E2_ESTRUTURA_GAMMA.md) - Estrutura dos slides
- [utils/tools_sinarm.py](../../utils/tools_sinarm.py) - Tools compartilhadas

### Externos:
- [Language Models are Few-Shot Learners (GPT-3 paper)](https://arxiv.org/abs/2005.14165)
- [Chain-of-Thought Prompting Elicits Reasoning in LLMs](https://arxiv.org/abs/2201.11903)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---

## ❓ FAQ

### 1. Posso fazer as atividades fora de ordem?
**Não recomendado.** Atividades são incrementais (1D depende de 1C depende de 1B depende de 1A).

### 2. Quanto tempo leva para completar tudo?
**Total: ~3h30** (1A-1D: 80min, 2A-2C: 60min, 2D: 10min opcional, 3A: 10min, 4A-4B: 10min, buffer: 30min).

### 3. Preciso rodar TODAS as atividades?
**Mínimo**: 1A, 1C, 1D, 2A, 2C, 3A, 4A (core concepts).  
**Opcional mas recomendado**: 1B, 2B, 2D, 4B (hands-on aprofundado).

### 4. O agente v2.5 substitui o v1.8?
**Não necessariamente.** Depende do caso de uso:
- Queries simples: v1.8 é mais rápido e barato
- Queries complexas: v2.5 é mais preciso (mas +30% latência)
- Produção: Use AMBOS com roteador inteligente (simples→v1.8, complexa→v2.5)

### 5. Como sei se meu Few-Shot está bom?
**Métricas** (ATIVIDADE 1D):
- Accuracy v2.0 deve ser 10-20pp maior que v1.8
- Se não melhorou: exemplos estão ruins (refaça ATIVIDADE 1B)
- Se piorou: exemplos estão **confundindo** o modelo (use menos exemplos ou exemplos mais diversos)

### 6. CoT deixa o agente muito lento. E agora?
**Trade-offs**:
- CoT completo: +30% latência (todas queries)
- CoT seletivo: +10% latência média (só queries complexas)
- **Solução**: Classificador (ATIVIDADE 2A) → Se simples: sem CoT, Se complexa: com CoT

### 7. Onde estão os dados SINARM?
`../../../E2_QUALIDADE_E_MEMORIA/DADOS_SINARM/` (volta 3 níveis de 03_CODIGOS_PRONTOS/).  
Ou use caminho relativo configurado em `utils/tools_sinarm.py`.

---

## ✅ Checklist de Conclusão

Ao final do E2, você deve ser capaz de:

- [ ] Explicar o que é Few-Shot Learning e quando usar
- [ ] Criar exemplos Few-Shot de alta qualidade (7 critérios)
- [ ] Implementar Few-Shot em um agente (ATIVIDADE 1C)
- [ ] Medir impacto de Few-Shot com métricas (ATIVIDADE 1D)
- [ ] Classificar queries em Simples/Média/Complexa (ATIVIDADE 2A)
- [ ] Escrever trace CoT manualmente (ATIVIDADE 2B)
- [ ] Implementar CoT em um agente (ATIVIDADE 2C)
- [ ] Implementar memory conversacional (buffer) (ATIVIDADE 3A)
- [ ] Proteger agente com input validation (ATIVIDADE 4A)
- [ ] Testar agente contra injection attacks (ATIVIDADE 4B)
- [ ] Entender trade-offs (accuracy vs latência vs custo)

---

## 🎓 Próximos Passos

**Concluiu E2?** Parabéns! 🎉

**Próximo**: E3 - LangChain & CrewAI
- Refatorar agente v2.5 usando frameworks
- Comparar: código manual vs LangChain
- Multi-agent systems com CrewAI

**Preparação para E3**:
1. Revise código do agente_v2.5_completo.py
2. Liste pontos que parecem "repetitivos" ou "boilerplate"
3. Pense: "Como um framework poderia simplificar isso?"

---

**Boa jornada! 🚀**

_Dúvidas? Abra issue no repositório ou pergunte no fórum da disciplina._
