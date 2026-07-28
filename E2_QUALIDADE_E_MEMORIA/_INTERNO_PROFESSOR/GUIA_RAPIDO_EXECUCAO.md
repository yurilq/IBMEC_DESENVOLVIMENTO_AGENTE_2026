# ⚡ GUIA RÁPIDO: EXECUTAR PRÁTICA E2

## 🎯 RESUMO EXECUTIVO

**Duração:** 3h30  
**Formato:** 70% Prática Hands-On  
**Objetivo:** Evoluir agente v1.8 → v2.0 (Few-Shot) → v2.5 (CoT)

---

## 📋 PRÉ-AULA (1 HORA ANTES)

### Checklist Técnico

```bash
# 1. Testar Ollama
ollama run llama3.2
# Verificar: Responde normalmente?

# 2. Testar estrutura E2
cd "00_DISCIPLINAS/.../E2_QUALIDADE_E_MEMORIA"
ls -la conceitos/  # Deve ter 4 pastas

# 3. Abrir VS Code
code .

# 4. Terminal split (Ctrl+Shift+5)
# Esquerda: Editor
# Direita: Execução
```

### Materiais Físicos

```markdown
□ Slides impressos (backup)
□ Checklist Few-Shot (15 cópias)
□ Lista de alunos para grupos
□ Cronômetro visível
```

---

## ⏰ TIMELINE - COLINHA DO PROFESSOR

| Hora | Ação | Comando/Fala-Chave |
|------|------|-------------------|
| **19h00** | Abertura | "Hoje 70% prática. Salvem TODOS outputs!" |
| **19h10** | Demo Few-Shot | `ollama run llama3.2` (Zero vs Few) |
| **19h20** | ATIVIDADE 1A | "Meçam v1.8. 15 min. GO!" |
| **19h35** | Discussão 1A | "Quem teve <60%? >80%?" |
| **19h40** | ATIVIDADE 1B | "Duplas. Criem 3 exemplos. Checklist!" |
| **19h55** | Validação 1B | "Dupla X, mostre exemplo na tela" |
| **20h00** | Demo 1C | `python ATIVIDADE_1C_implementar.py` |
| **20h05** | ATIVIDADE 1C | "Integrar Few-Shot. 20 min!" |
| **20h25** | ATIVIDADE 1D | "Comparar v1.8 vs v2.0. 10 min!" |
| **20h35** | Mostrar tabela | "Esperado: +17pp accuracy" |
| **20h30** | ☕ INTERVALO | "10 min. Reflitam: Few-Shot valeu?" |
| **20h40** | Teoria CoT | Demo: Query complexa com/sem CoT |
| **20h45** | ATIVIDADE 2A | "Trios. Classificar 10 queries!" |
| **20h55** | ATIVIDADE 2B | Demo no quadro: Escrever trace |
| **21h05** | ATIVIDADE 2C | "Implementar v2.5. 20 min!" |
| **21h25** | Comparar v2.0/v2.5 | "Complexas: +14pp com CoT!" |
| **21h30** | ATIVIDADE 3A | `python ATIVIDADE_3A_buffer.py` |
| **21h40** | ATIVIDADE 4A | "Security. 5 min observação" |
| **21h45** | ATIVIDADE 4B | "Testar 10 ataques" |
| **21h50** | Encerramento | "O que criamos hoje? Reflexão!" |
| **22h00** | Entrega | "Enviar até sexta: 5 arquivos" |

---

## 🎬 DEMOS CRÍTICAS (PREPARAR ANTES)

### 1. Few-Shot Demo (19h10 - 5 min)

**Terminal 1:**
```bash
ollama run llama3.2
>>> Quantas pistolas Taurus no SINARM?
# Resultado: Alucina/inventa
```

**Terminal 2:**
```bash
ollama run llama3.2
>>> Você é especialista SINARM.

EXEMPLO:
Pergunta: "Quantos revólveres apreendidos?"
Resposta: "Consultei SINARM/OCORRENCIAS. Filtrei tipo='Revólver', status='Apreendido'. Resultado: 2.340."

Agora: Quantas pistolas Taurus no SINARM?
# Resultado: Segue padrão do exemplo!
```

**Fala:** "Viram a diferença? EXEMPLO ensina o LLM!"

---

### 2. CoT Demo (20h40 - 5 min)

**No Quadro (ou slide):**

```
Query: "Marca com maior diferença registros vs furtos?"

TRACE CoT:

Thought: Preciso buscar 2 datasets, calcular diferença
Action: buscar_registros()
Observation: Taurus=13.240, Glock=5.821, CBC=4.892
Action: buscar_ocorrencias(tipo='Furto')
Observation: Taurus=4.892, Glock=2.341, CBC=1.987
Thought: Diferenças: Taurus=8.348, Glock=3.480
Answer: Taurus (8.348 diferença)
```

**Fala:** "Raciocínio VISÍVEL = debugável!"

---

### 3. Memory Demo (21h30 - 3 min)

```bash
python conceitos/03_memory_conversacional/ATIVIDADE_3A_buffer.py
```

**Mostrar output:**
```
Turno 1:
User: "Quantas pistolas Taurus?"
Agent: "892 pistolas"

Turno 2:
User: "E Glock?" ← REFERÊNCIA
Agent: "487 pistolas Glock" ✅ LEMBROU CONTEXTO!
```

---

## 📊 MÉTRICAS ESPERADAS (PARA COMPARAR)

```
┌──────────────┬─────────┬──────────┬──────────┐
│              │ v1.8    │ v2.0     │ v2.5     │
├──────────────┼─────────┼──────────┼──────────┤
│ Accuracy     │ 65%     │ 82%      │ 87%      │
│ Latência     │ 2.1s    │ 2.4s     │ 3.2s     │
│ Tokens       │ 350     │ 620      │ 890      │
│ Raciocínio   │ Não     │ Não      │ Sim ✅    │
└──────────────┴─────────┴──────────┴──────────┘
```

**Se aluno divergir muito:**
- Accuracy <50% em v1.8 → v1.8 mal implementado
- Few-Shot não melhora → Exemplos ruins (checklist!)
- v2.5 sem Thought/Action → Template não concatenado

---

## 🚨 TROUBLESHOOTING RÁPIDO

| Problema | Solução em 30 segundos |
|----------|------------------------|
| "v1.8 não roda" | Pair com colega ou usar `solucao_final/` |
| "Ollama travou" | `ollama ps` → `kill` → reiniciar |
| "Exemplos não carregam" | Verificar caminho JSON (path absoluto?) |
| "v2.5 sem CoT" | `print(prompt_system)` → Falta COT_TEMPLATE? |
| "Muito lento" | Rodar em batch (não 30 alunos ao mesmo tempo) |

---

## 💬 FRASES-CHAVE (REPETIR DURANTE AULA)

```
✅ "Métricas > Intuição" (sempre medir!)
✅ "Exemplo ruim = Few-Shot não funciona"
✅ "CoT só para queries complexas" (não desperdiçar)
✅ "Trade-off: não existe almoço grátis"
✅ "Raciocínio verificável = debugável"
```

---

## 📦 ENTREGA - LEMBRAR NO FINAL

```
📂 E2_[NOME_ALUNO]/
   ├── agente_v2.0_fewshot.py
   ├── agente_v2.5_cot.py
   ├── exemplos_fewshot.json (3 exemplos)
   ├── comparacao_v1_v2.json (métricas)
   └── trace_cot_manual.txt (ATIVIDADE 2B)

Prazo: Sexta 19/07/2026 até 23h59
Local: LMS (Moodle/Canvas)
```

---

## 🎯 OBJETIVOS DE APRENDIZAGEM (VALIDAR NO FINAL)

Perguntar a 3 alunos:

```
1. "Por que Few-Shot melhora accuracy?" 
   ✅ Resposta: "Exemplos ensinam o LLM"

2. "Quando usar CoT?"
   ✅ Resposta: "Queries complexas (6+ pontos)"

3. "Qual a vantagem de CoT?"
   ✅ Resposta: "Raciocínio verificável/debugável"
```

Se não souberem → **Revisitar conceito rapidamente!**

---

## 🔄 PLANO B (SE ATRASOU 15+ MIN)

**Cortar nesta ordem:**
1. ❌ ATIVIDADE 2D (opcional - parser)
2. ❌ Discussões 5min → 3min
3. ❌ Validação coletiva 1B → Apenas mostrar 1 exemplo
4. ❌ Memory+Security → Demo única 10min (não fazer atividades)

**Mínimo viável:**
- ✅ 1A, 1C, 1D (Few-Shot)
- ✅ 2A, 2C (CoT)
- ✅ Demo Memory+Security (3min)

---

## ✅ CHECKLIST PÓS-AULA

```markdown
□ Coletar feedback (Google Forms)
□ Compartilhar gabarito oficial (solucao_final/)
□ Responder dúvidas no fórum (24h)
□ Ajustar timing para próxima turma
□ Salvar resultados médios da turma
```

---

## 📞 EMERGÊNCIA

**Ollama offline:**
→ Usar API OpenAI (fallback)
→ Ou demonstrar com prints pré-salvos

**Projetor falha:**
→ Alunos seguem roteiro escrito (README_E2.md)
→ Professor circula ajudando individualmente

**Sala vazia (>50% falta):**
→ Gravar aula e disponibilizar
→ Remarcar prática presencial

---

## 🎓 ÚLTIMA DICA

**70% do aprendizado vem de FAZER, não assistir.**

→ Minimize fala, maximize hands-on  
→ Circular > Palestrar  
→ Debugar junto > Resolver sozinho  

**BOA AULA! 🚀**

---

_Última atualização: 16/07/2026_
