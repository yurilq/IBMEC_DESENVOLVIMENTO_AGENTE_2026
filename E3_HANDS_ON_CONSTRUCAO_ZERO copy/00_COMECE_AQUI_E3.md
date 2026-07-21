# 🚀 E3: CONSTRUÇÃO DO AGENTE DO ZERO

**Encontro 3 - Terça-feira 28/07/2026**  
**Horário:** 13h00 - 18h00 (5 horas)  
**Status:** 📦 PRONTO PARA USO

---

## ⚠️ LEIA PRIMEIRO: ESTRUTURA DE PASTAS

**IMPORTANTE:** Esta pasta contém MATERIAL DE REFERÊNCIA.  
Você vai trabalhar em uma **PASTA SEPARADA** que você criará.

📖 **Leia antes de começar:** [ESTRUTURA_PASTAS_E3.md](ESTRUTURA_PASTAS_E3.md)

**Resumo rápido:**
- ✅ **Esta pasta** = Material para consultar (guias, templates, exemplos)
- ✅ **Sua pasta de trabalho** = Onde você criará arquivos .py e colocará CSV
- ⚠️ NÃO trabalhe dentro desta pasta E3_HANDS_ON_CONSTRUCAO_ZERO!

---

## 🎯 O QUE VAMOS FAZER HOJE

Construir um **agente SINARM completo DO ZERO**, passo a passo, **JUNTO COM OS ALUNOS**.

### **Objetivo:**
✅ Cada aluno sai com agente funcional construído por ele mesmo  
✅ Entende @decorator profundamente  
✅ Aplica Few-Shot + CoT na prática  
✅ Consolida tudo que aprendeu em E1 + E2

---

## 📊 O QUE CONSTRUIREMOS

```python
# agente_v2_0_completo.py
# 
# ✅ 4 Tools SINARM (@tool decorator)
# ✅ Cache (@lru_cache)
# ✅ Few-Shot (3-5 exemplos)
# ✅ Chain-of-Thought (5 passos)
# ✅ Validação básica (security)
# ❌ Memory (não será hoje - deixar para E4)
#
# Total: ~150 linhas de código
```

---

## ⏰ CRONOGRAMA DO DIA

| Horário | Atividade | Duração |
|---------|-----------|---------|
| **13:00-13:45** | Parte 1: Setup + Hello World | 45 min |
| 13:45-14:00 | ☕ Pausa | 15 min |
| **14:00-15:00** | Parte 2: Primeira Tool (sem decorator) | 60 min |
| 15:00-15:15 | ☕ Pausa | 15 min |
| **15:15-16:00** | Parte 3: EXPLICAÇÃO @DECORATOR | 45 min |
| 16:00-16:15 | ☕ Pausa | 15 min |
| **16:15-17:15** | Parte 4: Agente com 4 Tools + Cache | 60 min |
| 17:15-17:30 | ☕ Pausa | 15 min |
| **17:30-18:00** | Parte 5: Few-Shot + CoT + Security | 30 min |

**Total:** 4h trabalho + 1h pausas = 5h

---

## 📂 ESTRUTURA DA PASTA

```
E3_CONSTRUCAO_DO_ZERO/
│
├── 00_COMECE_AQUI_E3.md              ← Você está aqui!
├── ROTEIRO_COMPLETO_E3.md            ← Timeline detalhada (para professor)
├── INDEX_E3.md                       ← Navegação completa
│
├── 01_GUIAS_ALUNO/
│   ├── PARTE_1_SETUP.md              ← 13:00-13:45
│   ├── PARTE_2_PRIMEIRA_TOOL.md      ← 14:00-15:00
│   ├── PARTE_3_DECORATOR.md          ← 15:15-16:00 ⭐ REFORÇADO
│   ├── PARTE_4_QUATRO_TOOLS.md       ← 16:15-17:15
│   └── PARTE_5_FEWSHOT_COT.md        ← 17:30-18:00
│
├── 02_TEMPLATES_PRONTOS/
│   ├── TEMPLATE_HORA_1.py            ← Código pronto Parte 1
│   ├── TEMPLATE_HORA_2.py            ← Código pronto Parte 2
│   ├── TEMPLATE_HORA_3.py            ← Código pronto Parte 3
│   ├── TEMPLATE_HORA_4.py            ← Código pronto Parte 4
│   └── TEMPLATE_HORA_5.py            ← Código pronto Parte 5
│
├── 03_CODIGO_INCREMENTAL/
│   ├── passo_01_hello_world.py
│   ├── passo_02_tool_simples.py
│   ├── ...
│   └── passo_20_agente_completo.py
│
└── 04_MATERIAL_APOIO/
    ├── GUIA_DECORATOR_DETALHADO.md   ⭐ Explicação 45 min
    ├── SLIDES_DECORATOR_VISUAL.md     ⭐ 10 slides
    ├── EXEMPLOS_DECORATOR.py          ⭐ 6 exemplos
    ├── CHECKPOINTS_E3.md              ← 20+ checks
    ├── FAQ_E3.md
    ├── TROUBLESHOOTING_E3.md
    └── COMPARACAO_E2_E3.md
```

---

## 🎓 PARA O PROFESSOR

### **Preparação (1 hora antes):**

```bash
# 1. Verificar Ollama rodando
ollama serve

# 2. Escolher e testar modelo (IMPORTANTE!)
# Se erro de memória, use modelo menor:
ollama pull llama3.2:1b
ollama run llama3.2:1b

# Se RAM suficiente (8GB+):
ollama run llama3

# 3. Verificar dados SINARM
ls DADOS_SINARM/OCORRENCIAS_2026.csv

# 4. Abrir arquivos no VSCode:
#    - ROTEIRO_COMPLETO_E3.md (timeline)
#    - PARTE_3_DECORATOR.md (slides decorator)
#    - TEMPLATE_HORA_5.py (código final)

# 5. Projetor + terminal prontos
```

### **Durante a aula:**

✅ **Seguir ROTEIRO_COMPLETO_E3.md** (passo a passo)  
✅ **Se aluno tiver erro de memória:** Ver [GUIA_ESCOLHA_MODELO_LLM.md](04_MATERIAL_APOIO/GUIA_ESCOLHA_MODELO_LLM.md)  
✅ **Parte 3 (15:15-16:00): REFORÇAR @decorator**  
   → Usar GUIA_DECORATOR_DETALHADO.md  
   → Mostrar EXEMPLOS_DECORATOR.py rodando  
✅ **Codar JUNTO com alunos** (não mostrar código pronto)  
✅ **Testar a cada 15 minutos** (checkpoints visuais)

---

## 👨‍🎓 PARA O ALUNO

### **O que você precisa:**

```
✅ Python 3.9+ instalado
✅ Ollama instalado e rodando
✅ VSCode (ou editor similar)
✅ Dados SINARM (OCORRENCIAS_2026.csv)
✅ Vontade de construir do zero!
```

### **Como seguir a aula:**

1. **Abra seu editor de código**
2. **Siga o professor** (ele vai codar junto)
3. **Digite o código** (não copie/cole ainda)
4. **Teste a cada checkpoint** (ver funcionar!)
5. **Se travar:** Templates prontos em `02_TEMPLATES_PRONTOS/`

---

## 🎯 O QUE VOCÊ VAI APRENDER

### **Competências Consolidadas:**

| Competência | E1 | E2 | E3 |
|-------------|----|----|-----|
| **Tools básicas** | ✅ Teoria | - | ✅ Prática |
| **ReAct loop** | ✅ Teoria | - | ✅ Prática |
| **@decorator** | ⚠️ Rápido | ❌ Faltou | ✅ **45 MIN REFORÇADO** |
| **@tool** | ⚠️ Rápido | ❌ Faltou | ✅ Prática |
| **@lru_cache** | ⚠️ Rápido | ❌ Faltou | ✅ Prática |
| **Few-Shot** | - | ✅ Teoria | ✅ **IMPLEMENTAR** |
| **CoT (5 passos)** | - | ✅ Teoria | ✅ **IMPLEMENTAR** |
| **Security** | - | ✅ Teoria | ✅ Validação básica |
| **Memory** | - | ❌ Não dado | ❌ Deixar E4 |

---

## ✅ CHECKPOINTS DO DIA

### **Checkpoint 1 (13:45):**
- [ ] Python funciona?
- [ ] Ollama responde?
- [ ] LLM retorna "Hello World"?

### **Checkpoint 2 (15:00):**
- [ ] Função Python simples criada?
- [ ] Tool conectada ao agente?
- [ ] Agente chamou a tool?

### **Checkpoint 3 (16:00):**
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

## 🚀 PRÓXIMOS PASSOS

### **Após E3:**
✅ Você tem agente completo (v2.0)  
✅ Consolida E1 + E2  
✅ Pronto para E4 (LangChain vs CrewAI + Memory)

### **E4 em diante:**
- **E4:** Refatorar v2.0 para LangChain + adicionar Memory
- **E5:** RAG + FAISS (busca semântica)
- **E6:** Deploy (API + Docker)
- **E7:** Métricas + Projeto Final

---

## 📞 SUPORTE

### **Durante a aula:**
- ✋ Levante a mão
- 💬 Pergunte sem medo
- 🤝 Ajude o colega ao lado

### **Materiais de apoio:**
- **FAQ_E3.md** - 20+ perguntas frequentes
- **TROUBLESHOOTING_E3.md** - Erros comuns resolvidos
- **GUIA_DECORATOR_DETALHADO.md** - Decorators explicados

### **Se você ficar para trás:**
- Templates prontos em `02_TEMPLATES_PRONTOS/`
- Copie/cole e DEPOIS entenda linha por linha
- Pergunte no final da aula

---

## 🎉 RESUMO

**Hoje você vai:**
1. ✅ Construir agente do ZERO (não código pronto!)
2. ✅ Entender @decorator profundamente
3. ✅ Aplicar Few-Shot + CoT na prática
4. ✅ Sair com agente v2.0 funcional

**Requisito para avançar:**
- Agente v2.0 funcionando ✅
- Entendeu decorators ✅
- Testou e validou ✅

---

## 📌 LEMBRE-SE

> **"Não vamos VER código pronto. Vamos CONSTRUIR juntos!"**

- Codar linha por linha ✅
- Testar a cada passo ✅
- Entender ANTES de avançar ✅
- Celebrar quando funcionar! 🎉

---

## 🗺️ NAVEGAÇÃO RÁPIDA

| Arquivo | Para quê? |
|---------|-----------|
| **ROTEIRO_COMPLETO_E3.md** | Timeline detalhada (professor) |
| **PARTE_1_SETUP.md** | Guia Parte 1 (13:00-13:45) |
| **PARTE_3_DECORATOR.md** | Guia decorators (15:15-16:00) ⭐ |
| **TEMPLATE_HORA_5.py** | Código final completo |
| **GUIA_DECORATOR_DETALHADO.md** | Explicação decorators 45 min |
| **FAQ_E3.md** | Dúvidas frequentes |

---

**Arquivo:** 00_COMECE_AQUI_E3.md  
**Localização:** E3_CONSTRUCAO_DO_ZERO/  
**Data:** 16/07/2026  
**Status:** ✅ PRONTO PARA AULA

**Bom trabalho! Vamos construir juntos! 🚀**
