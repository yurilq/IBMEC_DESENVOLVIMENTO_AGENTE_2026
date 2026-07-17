# 🎓 ROTEIRO DA PRÁTICA: E2 - QUALIDADE E MEMÓRIA

## 📋 INFORMAÇÕES GERAIS

**Encontro:** E2 - Qualidade e Memória  
**Duração:** 3h30 (210 minutos)  
**Formato:** 70% Prática Hands-On + 30% Teoria  
**Objetivo:** Evoluir seu agente v1.8 → v2.0 (Few-Shot) → v2.5 (CoT)

---

## 🎯 O QUE VOCÊ VAI CRIAR HOJE

Ao final da aula, você terá:

✅ **agente_v2.0_fewshot.py** - Agente com Few-Shot Learning (+15-30% accuracy)  
✅ **agente_v2.5_cot.py** - Agente com Chain-of-Thought (raciocínio explícito)  
✅ **ShortTermMemory** - Memória conversacional (buffer 5 mensagens)  
✅ **InputValidator** - Proteção contra injection attacks  

---

## 📦 PRÉ-REQUISITOS

### ✅ Checklist Técnico

Antes da aula, verifique se você tem:

```bash
# 1. Python 3.10+
python --version

# 2. LangChain instalado
pip install langchain

# 3. Ollama funcionando
ollama run llama3.2
# Digite "oi" para testar. Deve responder.

# 4. Agente v1.8 do E1 funcionando
# Se não funciona, peça ajuda ANTES da aula!

# 5. Pasta E2_QUALIDADE_E_MEMORIA baixada
cd "caminho/para/E2_QUALIDADE_E_MEMORIA"
ls conceitos/  # Deve ter 4 pastas
```

### 📂 Estrutura da Pasta E2

```
E2_QUALIDADE_E_MEMORIA/
├── README_E2.md               ← Guia completo
├── INDEX.md                   ← Navegação rápida
│
├── conceitos/                 ← Atividades práticas
│   ├── 01_fewshot/            (4 atividades)
│   ├── 02_cot/                (4 atividades)
│   ├── 03_memory_conversacional/ (1 atividade)
│   └── 04_security_basica/    (2 atividades)
│
└── solucao_final/             ← Código completo (referência)
    ├── agente_v2.0_fewshot.py
    └── agente_v2.5_cot.py
```

---

## ⏰ CRONOGRAMA DA AULA

| Horário | Bloco | O que você vai fazer |
|---------|-------|----------------------|
| **19h00** | 🎯 Abertura | Entender objetivos do E2 |
| **19h10** | 📚 Few-Shot | Teoria + Demo (Zero-Shot vs Few-Shot) |
| **19h20** | 🔨 ATIVIDADE 1A | Medir baseline (v1.8) |
| **19h40** | 🔨 ATIVIDADE 1B | Criar 3 exemplos Few-Shot |
| **20h00** | 🔨 ATIVIDADE 1C | Implementar v2.0 (Few-Shot) |
| **20h25** | 🔨 ATIVIDADE 1D | Comparar v1.8 vs v2.0 |
| **20h30** | ☕ Intervalo | 10 minutos |
| **20h40** | 🧠 CoT | Teoria + Demo (Chain-of-Thought) |
| **20h45** | 🔨 ATIVIDADE 2A | Classificar queries (simples/complexa) |
| **20h55** | 🔨 ATIVIDADE 2B | Escrever trace CoT manualmente |
| **21h05** | 🔨 ATIVIDADE 2C | Implementar v2.5 (CoT) |
| **21h30** | 🔨 ATIVIDADE 3A | Memory conversacional |
| **21h40** | 🔨 ATIVIDADE 4A | Input validation (security) |
| **21h45** | 🔨 ATIVIDADE 4B | Testar ataques |
| **21h50** | 🎉 Encerramento | Retrospectiva + Entregáveis |

---

## 🚀 ATIVIDADES PASSO A PASSO

---

## 📚 BLOCO 1: FEW-SHOT LEARNING

### 🎯 Objetivo

Melhorar accuracy do agente adicionando **exemplos de qualidade** ao prompt.

**Resultado esperado:** v1.8 (65%) → v2.0 (82%) = **+17pp accuracy!**

---

### 🔨 ATIVIDADE 1A: MEDIR BASELINE (20 min)

**O que fazer:**

1. Abra o arquivo:
   ```bash
   conceitos/01_fewshot/ATIVIDADE_1A_baseline.py
   ```

2. Execute:
   ```bash
   python ATIVIDADE_1A_baseline.py
   ```

3. Para cada uma das **5 queries**:
   - Execute a query no seu **agente v1.8** (do E1)
   - Avalie a resposta:
     - Dataset correto? [X] ou [ ]
     - Campos corretos? [X] ou [ ]
     - Qualidade (1-5)
   - Meça o tempo (use cronômetro)

4. Preencha a tabela no terminal

5. Calcule:
   - **Accuracy:** Quantas queries acertou? (X/5 = %)
   - **Latência média:** Soma tempos / 5
   - **Taxa de erro:** Quantas erraram? (X/5 = %)

**⚠️ IMPORTANTE:** Anote os erros! Você vai comparar depois.

---

### 🔨 ATIVIDADE 1B: CRIAR EXEMPLOS FEW-SHOT (20 min)

**O que fazer:**

1. Abra:
   ```bash
   conceitos/01_fewshot/ATIVIDADE_1B_criar_exemplos.py
   ```

2. Execute (modo guiado):
   ```bash
   python ATIVIDADE_1B_criar_exemplos.py
   ```

3. **Crie 3 exemplos de QUALIDADE:**
   - **Exemplo 1:** Query SIMPLES (1 filtro, resposta direta)
   - **Exemplo 2:** Query MÉDIA (2-3 filtros, agregação)
   - **Exemplo 3:** Query COMPLEXA (cálculos, múltiplos datasets)

4. **Valide com checklist** (7 critérios):
   ```
   ✅ 1. Query CLARA e específica?
   ✅ 2. Raciocínio explícito (passo-a-passo)?
   ✅ 3. Dados REAIS (não inventados)?
   ✅ 4. Resposta COMPLETA (números + fonte)?
   ✅ 5. Formato CONSISTENTE (entre exemplos)?
   ✅ 6. Diversidade (simples + média + complexa)?
   ✅ 7. SEM ambiguidade (claro para LLM)?
   ```

5. Salve em: `exemplos_fewshot.json`

**💡 DICA:** Trabalhe em DUPLA! Dois olhares melhoram qualidade.

---

### 🔨 ATIVIDADE 1C: IMPLEMENTAR v2.0 (25 min)

**O que fazer:**

1. Abra:
   ```bash
   conceitos/01_fewshot/ATIVIDADE_1C_implementar.py
   ```

2. Execute:
   ```bash
   python ATIVIDADE_1C_implementar.py
   ```

3. O script vai:
   - ✅ Carregar seus 3 exemplos (`exemplos_fewshot.json`)
   - ✅ Adicionar ao prompt system
   - ✅ Gerar `agente_v2.0_fewshot.py`

4. **Teste o v2.0** com 2 queries:
   ```bash
   python agente_v2.0_fewshot.py
   ```

5. **Observe:** A resposta segue o formato dos exemplos?

**⚠️ Se não funcionar:**
- Verifique se `exemplos_fewshot.json` existe
- Veja se os exemplos estão bem formatados (JSON válido)

---

### 🔨 ATIVIDADE 1D: COMPARAR v1.8 vs v2.0 (15 min)

**O que fazer:**

1. Abra:
   ```bash
   conceitos/01_fewshot/ATIVIDADE_1D_comparar.py
   ```

2. Execute:
   ```bash
   python ATIVIDADE_1D_comparar.py
   ```

3. O script vai:
   - Executar as **mesmas 5 queries** (da 1A) no **v2.0**
   - Comparar com baseline (v1.8)
   - Calcular: Δ Accuracy, Δ Latência, Δ Qualidade

4. Preencha a tabela comparativa

5. **Analise:**
   - Accuracy melhorou? (Esperado: +10-20%)
   - Latência aumentou? (Esperado: +0.2-0.5s)
   - **Vale a pena?** (Trade-off accuracy vs latência)

6. Salve em: `comparacao_v1_v2.json`

---

## ☕ INTERVALO (10 min)

Reflita:
- Few-Shot melhorou meu agente?
- Meus exemplos foram bons?
- O custo (+tokens) vale a pena?

---

## 🧠 BLOCO 2: CHAIN-OF-THOUGHT

### 🎯 Objetivo

Adicionar **raciocínio explícito** para queries complexas.

**Resultado esperado:** Queries complexas: v2.0 (78%) → v2.5 (92%) = **+14pp!**

---

### 🔨 ATIVIDADE 2A: CLASSIFICAR QUERIES (15 min)

**O que fazer:**

1. Abra:
   ```bash
   conceitos/02_cot/ATIVIDADE_2A_classificar.py
   ```

2. Execute (modo interativo):
   ```bash
   python ATIVIDADE_2A_classificar.py
   ```

3. Para cada uma das **10 queries**, identifique:
   - Quantos **datasets** necessários?
   - Quantos **filtros**?
   - Quais **cálculos**?
   - Quantas **etapas**?

4. **Calcule pontos** (0-10):
   ```
   +1 por dataset adicional
   +1 por filtro adicional
   +1 por cálculo
   +2 se cruzar datasets
   +1 por etapa adicional (após 2)
   ```

5. **Classifique:**
   - **0-2 pontos:** SIMPLES (não precisa CoT)
   - **3-5 pontos:** MÉDIA (CoT opcional)
   - **6+ pontos:** COMPLEXA (CoT essencial)

6. Compare com gabarito (automático no script)

**💡 DICA:** Trabalhe em TRIO! Discutam cada classificação.

---

### 🔨 ATIVIDADE 2B: ESCREVER TRACE CoT (10 min)

**O que fazer:**

1. Escolha **1 query COMPLEXA** (da 2A)

2. Abra:
   ```bash
   conceitos/02_cot/ATIVIDADE_2B_trace_manual.py
   ```

3. Execute:
   ```bash
   python ATIVIDADE_2B_trace_manual.py
   ```

4. **Escreva o trace completo** (raciocínio passo-a-passo):

   ```
   Thought: [O que preciso fazer?]
   Action: [Qual tool usar? Com quais parâmetros?]
   Observation: [O que retornou?]
   [Repetir Thought → Action → Observation se necessário]
   Answer: [Resposta final com fonte]
   ```

5. **Valide com checklist** (12 pontos)

6. Salve em: `trace_cot_manual.txt`

**💡 Por que fazer manualmente?**  
Para ENTENDER a estrutura antes de automatizar!

---

### 🔨 ATIVIDADE 2C: IMPLEMENTAR v2.5 (20 min)

**O que fazer:**

1. Abra:
   ```bash
   conceitos/02_cot/ATIVIDADE_2C_implementar.py
   ```

2. Execute:
   ```bash
   python ATIVIDADE_2C_implementar.py
   ```

3. O script vai:
   - ✅ Carregar template CoT (`conceitos/02_cot/template_cot.txt`)
   - ✅ Adicionar ao prompt system (v2.0 → v2.5)
   - ✅ Gerar `agente_v2.5_cot.py`

4. **Teste o v2.5** com query COMPLEXA:
   ```bash
   python agente_v2.5_cot.py
   ```

5. **Observe:** A resposta inclui "Thought:", "Action:", "Observation:"?

**⚠️ Se não mostrar raciocínio:**
- Template CoT não foi concatenado ao prompt
- Verifique código do prompt_system

---

## 🔒 BLOCO 3: MEMORY + SECURITY

### 🎯 Objetivo

- **Memory:** Manter contexto em conversações multi-turno
- **Security:** Proteger contra injection attacks

---

### 🔨 ATIVIDADE 3A: MEMORY CONVERSACIONAL (10 min)

**O que fazer:**

1. Abra:
   ```bash
   conceitos/03_memory_conversacional/ATIVIDADE_3A_buffer.py
   ```

2. Execute (demo automática):
   ```bash
   python ATIVIDADE_3A_buffer.py
   ```

3. **Observe** a conversação com 4 turnos:
   ```
   Turno 1: "Quantas pistolas Taurus?"
   Turno 2: "E Glock?" ← REFERÊNCIA ao turno anterior
   Turno 3: "Qual dessas duas tem mais furtos?"
   Turno 4: "Por quê?"
   ```

4. **Analise** a classe `ShortTermMemory` no código:
   - Como funciona o buffer?
   - O que acontece quando passa de 5 mensagens?
   - Como o contexto é adicionado ao prompt?

**💡 Trade-off:**
- Buffer 3: +10% tokens, contexto básico
- Buffer 5: +20% tokens, contexto bom ← **RECOMENDADO**
- Buffer 10: +40% tokens, contexto excelente

---

### 🔨 ATIVIDADE 4A: INPUT VALIDATION (5 min)

**O que fazer:**

1. Abra:
   ```bash
   conceitos/04_security_basica/ATIVIDADE_4A_validation.py
   ```

2. Execute:
   ```bash
   python ATIVIDADE_4A_validation.py
   ```

3. **Observe** a classe `InputValidator`:
   - Quais palavras são proibidas?
   - Como funciona a validação?

4. **Teste** 5 inputs maliciosos (automático no script)

**Tipos de ataque bloqueados:**
- SQL Injection: `' OR 1=1; --`
- Prompt Injection: `Ignore previous instructions`
- Command Injection: `rm -rf /`

---

### 🔨 ATIVIDADE 4B: TESTAR ATAQUES (5 min)

**O que fazer:**

1. Abra:
   ```bash
   conceitos/04_security_basica/ATIVIDADE_4B_testar_ataque.py
   ```

2. Execute:
   ```bash
   python ATIVIDADE_4B_testar_ataque.py
   ```

3. O script testa **10 ataques** pré-definidos

4. **Verifique:** Taxa de bloqueio = 100%?

5. **Analise** logs de segurança

**⚠️ IMPORTANTE:** Isso é security BÁSICA!  
Produção precisa: WAF, rate limiting, sandboxing, audit logs.

---

## 🎉 ENCERRAMENTO

### ✅ O que você criou hoje

```
✅ agente_v2.0_fewshot.py
✅ agente_v2.5_cot.py
✅ ShortTermMemory (buffer conversacional)
✅ InputValidator (security básica)
```

### 📊 Progressão

```
v1.8 (E1) → Accuracy: 60-70%
v2.0 (E2) → Accuracy: 75-85% (+15pp Few-Shot)
v2.5 (E2) → Accuracy: 80-90% (+5-10pp CoT)
```

**Total: +22pp de melhoria!** 🎉

---

## 📦 ENTREGÁVEIS (ATÉ SEXTA 19/07)

Crie uma pasta `E2_SEU_NOME/` com:

```
E2_SEU_NOME/
├── agente_v2.0_fewshot.py
├── agente_v2.5_cot.py
├── exemplos_fewshot.json (seus 3 exemplos)
├── comparacao_v1_v2.json (resultados ATIVIDADE 1D)
└── trace_cot_manual.txt (ATIVIDADE 2B)
```

**Enviar via:** LMS (Moodle/Canvas)  
**Prazo:** Sexta 19/07/2026 até 23h59

---

## 🔜 PRÓXIMA AULA: E3 - LangChain & CrewAI

**Preparação:**

```bash
# Instalar LangChain
pip install langchain

# Revisar código do v2.5
# Pensar: "Quais partes parecem repetitivas?"
# Frameworks podem simplificar!
```

**Próximo objetivo:** Refatorar v2.5 usando frameworks profissionais.

---

## ❓ DÚVIDAS FREQUENTES

### "Meu v1.8 não funciona. E agora?"

→ Trabalhe em dupla com colega que tem v1.8 funcionando  
→ Ou use o v1.8 de referência: `solucao_final/` (temporariamente)

### "Few-Shot não melhorou minha accuracy. Por quê?"

→ Revise seus exemplos com o **checklist de 7 critérios**  
→ Exemplos ruins = Few-Shot não funciona  
→ Use exemplos do gabarito: `conceitos/01_fewshot/EXPLICACAO.md`

### "v2.5 não mostra Thought/Action. Por quê?"

→ Template CoT não foi concatenado ao prompt  
→ Teste: `print(prompt_system)` e veja se aparece "Thought:", "Action:"

### "Muito lento! O que fazer?"

→ Normal se muitos alunos rodarem Ollama ao mesmo tempo  
→ Rode em batch (espere sua vez)  
→ Ou use API externa (OpenAI, Anthropic) se disponível

---

## 📞 SUPORTE

**Dúvidas durante aula:**
- Levante a mão
- Peça ajuda ao monitor
- Trabalhe em grupo (pair programming)

**Dúvidas depois da aula:**
- Fórum da disciplina
- Email do professor
- Monitoria (horários no LMS)

---

**🎓 BOA AULA! Lembre-se: 70% do aprendizado vem de FAZER!**

_Este roteiro foi criado para você EXECUTAR, não apenas ler._
