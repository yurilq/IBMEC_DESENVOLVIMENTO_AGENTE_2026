# 📑 INDEX E3 - CONSTRUÇÃO DO ZERO
## Navegação Completa do Encontro 3

**Data:** 28/07/2026 | **Horário:** 13h-18h | **Status:** ✅ PRONTO

---

## 🚀 INÍCIO RÁPIDO

### **👨‍🏫 Sou Professor**
1. Leia: **[ROTEIRO_COMPLETO_E3.md](ROTEIRO_COMPLETO_E3.md)** (timeline detalhada)
2. Prepare: **[04_MATERIAL_APOIO/GUIA_DECORATOR_DETALHADO.md](04_MATERIAL_APOIO/GUIA_DECORATOR_DETALHADO.md)** (Parte 3)
3. Tenha aberto: **[02_TEMPLATES_PRONTOS/TEMPLATE_HORA_5.py](02_TEMPLATES_PRONTOS/TEMPLATE_HORA_5.py)** (código final)

### **👨‍🎓 Sou Aluno**
1. Leia: **[00_COMECE_AQUI_E3.md](00_COMECE_AQUI_E3.md)** (visão geral)
2. Durante aula: Siga professor + guias em **[01_GUIAS_ALUNO/](01_GUIAS_ALUNO/)**
3. Se travar: Templates prontos em **[02_TEMPLATES_PRONTOS/](02_TEMPLATES_PRONTOS/)**

---

## 📂 ESTRUTURA COMPLETA

```
E3_CONSTRUCAO_DO_ZERO/
│
├── 00_COMECE_AQUI_E3.md              ← ⭐ LEIA PRIMEIRO
├── ROTEIRO_COMPLETO_E3.md            ← ⭐ Para professor (timeline)
├── INDEX_E3.md                       ← Você está aqui!
│
├── 01_GUIAS_ALUNO/                   ← Guias passo a passo
│   ├── PARTE_1_SETUP.md
│   ├── PARTE_2_PRIMEIRA_TOOL.md
│   ├── PARTE_3_DECORATOR.md          ← ⭐ REFORÇADO (45 min)
│   ├── PARTE_4_QUATRO_TOOLS.md
│   └── PARTE_5_FEWSHOT_COT.md
│
├── 02_TEMPLATES_PRONTOS/             ← Código pronto para copiar
│   ├── TEMPLATE_HORA_1.py
│   ├── TEMPLATE_HORA_2.py
│   ├── TEMPLATE_HORA_3.py
│   ├── TEMPLATE_HORA_4.py
│   └── TEMPLATE_HORA_5.py            ← ⭐ Código final completo
│
├── 03_CODIGO_INCREMENTAL/            ← 20 passos progressivos
│   └── [passo_01.py até passo_20.py]
│
└── 04_MATERIAL_APOIO/                ← Suporte e referência
    ├── GUIA_DECORATOR_DETALHADO.md   ← ⭐ Explicação 45 min
    ├── SLIDES_DECORATOR_VISUAL.md
    ├── EXEMPLOS_DECORATOR.py
    ├── CHECKPOINTS_E3.md
    ├── FAQ_E3.md
    ├── TROUBLESHOOTING_E3.md
    └── COMPARACAO_E2_E3.md
```

---

## ⏰ CRONOGRAMA

| Horário | Parte | Duração | Arquivos Usados |
|---------|-------|---------|-----------------|
| **13:00-13:45** | Parte 1: Setup + Hello World | 45 min | PARTE_1_SETUP.md, TEMPLATE_HORA_1.py |
| 13:45-14:00 | ☕ Pausa | 15 min | - |
| **14:00-15:00** | Parte 2: Primeira Tool | 60 min | PARTE_2_PRIMEIRA_TOOL.md, TEMPLATE_HORA_2.py |
| 15:00-15:15 | ☕ Pausa | 15 min | - |
| **15:15-16:00** | Parte 3: @DECORATOR ⭐ | 45 min | PARTE_3_DECORATOR.md, GUIA_DECORATOR_DETALHADO.md |
| 16:00-16:15 | ☕ Pausa | 15 min | - |
| **16:15-17:15** | Parte 4: 4 Tools + Cache | 60 min | PARTE_4_QUATRO_TOOLS.md, TEMPLATE_HORA_4.py |
| 17:15-17:30 | ☕ Pausa | 15 min | - |
| **17:30-18:00** | Parte 5: Few-Shot + CoT | 30 min | PARTE_5_FEWSHOT_COT.md, TEMPLATE_HORA_5.py |

---

## 📚 GUIAS POR PARTE

### **PARTE 1 (13:00-13:45) - Setup + Hello World**
- **Objetivo:** LLM responder pela primeira vez
- **Guia:** [01_GUIAS_ALUNO/PARTE_1_SETUP.md](01_GUIAS_ALUNO/PARTE_1_SETUP.md)
- **Template:** [02_TEMPLATES_PRONTOS/TEMPLATE_HORA_1.py](02_TEMPLATES_PRONTOS/TEMPLATE_HORA_1.py)
- **Checkpoint:** ✅ LLM respondeu?

### **PARTE 2 (14:00-15:00) - Primeira Tool**
- **Objetivo:** Criar função Python e conectar ao agente (SEM decorator)
- **Guia:** [01_GUIAS_ALUNO/PARTE_2_PRIMEIRA_TOOL.md](01_GUIAS_ALUNO/PARTE_2_PRIMEIRA_TOOL.md)
- **Template:** [02_TEMPLATES_PRONTOS/TEMPLATE_HORA_2.py](02_TEMPLATES_PRONTOS/TEMPLATE_HORA_2.py)
- **Checkpoint:** ✅ Agente chamou função?

### **PARTE 3 (15:15-16:00) - @DECORATOR ⭐ REFORÇADO**
- **Objetivo:** Entender decorators profundamente
- **Guia:** [01_GUIAS_ALUNO/PARTE_3_DECORATOR.md](01_GUIAS_ALUNO/PARTE_3_DECORATOR.md)
- **Material Apoio:** [04_MATERIAL_APOIO/GUIA_DECORATOR_DETALHADO.md](04_MATERIAL_APOIO/GUIA_DECORATOR_DETALHADO.md)
- **Slides:** [04_MATERIAL_APOIO/SLIDES_DECORATOR_VISUAL.md](04_MATERIAL_APOIO/SLIDES_DECORATOR_VISUAL.md)
- **Exemplos:** [04_MATERIAL_APOIO/EXEMPLOS_DECORATOR.py](04_MATERIAL_APOIO/EXEMPLOS_DECORATOR.py)
- **Template:** [02_TEMPLATES_PRONTOS/TEMPLATE_HORA_3.py](02_TEMPLATES_PRONTOS/TEMPLATE_HORA_3.py)
- **Checkpoint:** ✅ Entendeu o que é decorator?

### **PARTE 4 (16:15-17:15) - 4 Tools + Cache**
- **Objetivo:** Refatorar com @tool, adicionar 3 tools, adicionar @lru_cache
- **Guia:** [01_GUIAS_ALUNO/PARTE_4_QUATRO_TOOLS.md](01_GUIAS_ALUNO/PARTE_4_QUATRO_TOOLS.md)
- **Template:** [02_TEMPLATES_PRONTOS/TEMPLATE_HORA_4.py](02_TEMPLATES_PRONTOS/TEMPLATE_HORA_4.py)
- **Checkpoint:** ✅ 4 tools funcionam? Cache acelera?

### **PARTE 5 (17:30-18:00) - Few-Shot + CoT + Security**
- **Objetivo:** Aplicar conceitos E2 na prática
- **Guia:** [01_GUIAS_ALUNO/PARTE_5_FEWSHOT_COT.md](01_GUIAS_ALUNO/PARTE_5_FEWSHOT_COT.md)
- **Template:** [02_TEMPLATES_PRONTOS/TEMPLATE_HORA_5.py](02_TEMPLATES_PRONTOS/TEMPLATE_HORA_5.py) ⭐ Final
- **Checkpoint:** ✅ Agente v2.0 completo?

---

## 🎯 ARQUIVOS POR OBJETIVO

### **Para Preparar Aula (Professor)**
1. ✅ [ROTEIRO_COMPLETO_E3.md](ROTEIRO_COMPLETO_E3.md) - Timeline detalhada
2. ✅ [04_MATERIAL_APOIO/GUIA_DECORATOR_DETALHADO.md](04_MATERIAL_APOIO/GUIA_DECORATOR_DETALHADO.md)
3. ✅ [04_MATERIAL_APOIO/SLIDES_DECORATOR_VISUAL.md](04_MATERIAL_APOIO/SLIDES_DECORATOR_VISUAL.md)
4. ✅ [02_TEMPLATES_PRONTOS/TEMPLATE_HORA_5.py](02_TEMPLATES_PRONTOS/TEMPLATE_HORA_5.py)

### **Para Seguir Aula (Aluno)**
1. ✅ [00_COMECE_AQUI_E3.md](00_COMECE_AQUI_E3.md) - Visão geral
2. ✅ [01_GUIAS_ALUNO/](01_GUIAS_ALUNO/) - Guias de cada parte
3. ✅ [02_TEMPLATES_PRONTOS/](02_TEMPLATES_PRONTOS/) - Se travar

### **Para Entender Decorators (Todos)**
1. ✅ [04_MATERIAL_APOIO/GUIA_DECORATOR_DETALHADO.md](04_MATERIAL_APOIO/GUIA_DECORATOR_DETALHADO.md)
2. ✅ [04_MATERIAL_APOIO/SLIDES_DECORATOR_VISUAL.md](04_MATERIAL_APOIO/SLIDES_DECORATOR_VISUAL.md)
3. ✅ [04_MATERIAL_APOIO/EXEMPLOS_DECORATOR.py](04_MATERIAL_APOIO/EXEMPLOS_DECORATOR.py)

### **Para Tirar Dúvidas**
1. ✅ [04_MATERIAL_APOIO/FAQ_E3.md](04_MATERIAL_APOIO/FAQ_E3.md)
2. ✅ [04_MATERIAL_APOIO/TROUBLESHOOTING_E3.md](04_MATERIAL_APOIO/TROUBLESHOOTING_E3.md)
3. ✅ [04_MATERIAL_APOIO/CHECKPOINTS_E3.md](04_MATERIAL_APOIO/CHECKPOINTS_E3.md)

### **Para Comparar E2 e E3**
1. ✅ [04_MATERIAL_APOIO/COMPARACAO_E2_E3.md](04_MATERIAL_APOIO/COMPARACAO_E2_E3.md)

---

## ✅ CHECKPOINTS DO DIA

### **Checkpoint 1 (13:45):**
- [ ] Python funciona?
- [ ] Ollama responde?
- [ ] LLM retornou "Hello World"?

### **Checkpoint 2 (15:00):**
- [ ] Função Python criada?
- [ ] Tool conectada ao agente?
- [ ] Agente chamou a tool?

### **Checkpoint 3 (16:00) ⭐:**
- [ ] Entendeu o que é decorator?
- [ ] Viu diferença com/sem decorator?
- [ ] Sabe explicar @tool e @lru_cache?

### **Checkpoint 4 (17:15):**
- [ ] 4 tools funcionando?
- [ ] Cache acelera consultas?
- [ ] Agente responde corretamente?

### **Checkpoint 5 (18:00):**
- [ ] Few-Shot melhorou respostas?
- [ ] CoT mostra raciocínio?
- [ ] Validação bloqueia ataques?
- [ ] **Agente v2.0 completo?** ✅

---

## 🎓 O QUE SERÁ CONSTRUÍDO

### **Código Final: agente_v2_0_completo.py**

```python
# Componentes:
✅ 4 Tools SINARM (@tool decorator)
✅ Cache (@lru_cache para performance)
✅ Few-Shot (3-5 exemplos PCDF)
✅ Chain-of-Thought (5 passos)
✅ Validação básica (security)

# Total: ~150 linhas
# Consolida: E1 + E2 na prática
```

---

## 📊 CONSOLIDAÇÃO E1 + E2

| Conceito | E1 | E2 | E3 |
|----------|----|----|-----|
| **Tools básicas** | ✅ Teoria | - | ✅ Prática |
| **ReAct loop** | ✅ Teoria | - | ✅ Prática |
| **@decorator** | ⚠️ Rápido | ❌ Não dado | ✅ **45 MIN** |
| **@tool** | ⚠️ Rápido | ❌ Não dado | ✅ Prática |
| **@lru_cache** | ⚠️ Rápido | ❌ Não dado | ✅ Prática |
| **Few-Shot** | - | ✅ Teoria | ✅ **IMPLEMENTAR** |
| **CoT** | - | ✅ Teoria | ✅ **IMPLEMENTAR** |
| **Security** | - | ✅ Teoria | ✅ Implementar |
| **Memory** | - | ❌ Não dado | ❌ E4 |

---

## 🚀 PRÓXIMOS PASSOS

### **Após E3:**
✅ Agente v2.0 completo  
✅ Consolidou E1 + E2  
✅ Pronto para E4

### **E4 em diante:**
- **E4 (04/08):** LangChain vs CrewAI + Memory
- **E5 (11/08):** RAG + FAISS
- **E6 (18/08):** Deploy + Guardrails
- **E7 (25/08):** Métricas + Projeto Final

---

## 📞 SUPORTE

### **Durante a aula:**
- Levante a mão
- Pergunte sem medo
- Templates prontos disponíveis

### **Após a aula:**
- FAQ_E3.md
- TROUBLESHOOTING_E3.md
- Email professor

---

## 🗺️ MAPA MENTAL

```
E3 - CONSTRUÇÃO DO ZERO
│
├── PREPARAÇÃO
│   ├── Setup ambiente ✅
│   └── Hello World LLM ✅
│
├── FUNDAMENTOS
│   ├── Função Python simples ✅
│   └── Tool conectada ao agente ✅
│
├── DECORATORS ⭐ (45 MIN)
│   ├── O que é decorator? ✅
│   ├── Exemplos progressivos ✅
│   └── @tool + @lru_cache ✅
│
├── APLICAÇÃO
│   ├── 4 Tools funcionando ✅
│   └── Cache performance ✅
│
└── CONSOLIDAÇÃO E2
    ├── Few-Shot ✅
    ├── Chain-of-Thought ✅
    └── Security ✅
```

---

## 📌 LEMBRE-SE

> **"Não vamos VER código pronto. Vamos CONSTRUIR juntos!"**

- Codar linha por linha ✅
- Testar a cada passo ✅
- Entender ANTES de avançar ✅
- Celebrar quando funcionar! 🎉

---

**Arquivo:** INDEX_E3.md  
**Localização:** E3_CONSTRUCAO_DO_ZERO/  
**Data:** 16/07/2026  
**Status:** ✅ PRONTO

**Navegue pelos arquivos e boa aula! 🚀**
