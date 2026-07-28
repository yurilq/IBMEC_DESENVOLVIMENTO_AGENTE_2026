# ✅ CHECKLIST AULA PRÁTICA E2

## 📅 PRÉ-AULA (1 SEMANA ANTES)

```
□ Email enviado aos alunos com pré-requisitos
  • Python 3.10+
  • LangChain instalado
  • Ollama funcionando
  • Agente v1.8 testado

□ Pasta E2_QUALIDADE_E_MEMORIA compartilhada no LMS

□ Grupos de 3-4 alunos definidos

□ Sala/plataforma reservada
```

---

## 📅 PRÉ-AULA (1 DIA ANTES)

```
□ TODOS os scripts testados no meu ambiente

□ Slides preparados (15 slides mínimos):
  • Slide 1: Objetivos E2
  • Slide 2: Progressão v1.8 → v2.0 → v2.5
  • Slide 3: O que é Few-Shot
  • Slide 4: Zero-Shot vs Few-Shot
  • Slide 5: Checklist 7 critérios
  • Slide 6: Resultados esperados v1.8 vs v2.0
  • Slide 7: O que é Chain-of-Thought
  • Slide 8: Quando usar CoT
  • Slide 9: Anatomia trace CoT
  • Slide 10: Resultados v2.0 vs v2.5
  • Slide 11: Memory conversacional
  • Slide 12: Security básica
  • Slide 13: Retrospectiva
  • Slide 14: Entregáveis
  • Slide 15: Próxima aula (E3)

□ Checklists impressos (30 cópias):
  • Checklist Few-Shot (7 critérios)
  • Checklist CoT (12 pontos)

□ Backup preparado:
  • resultados_esperados.json
  • Videos demo (se Ollama falhar)
  • Prints de tela
```

---

## 📅 PRÉ-AULA (2 HORAS ANTES)

```
□ Ollama testado
  Terminal: ollama run llama3.2
  Verificar: Responde normalmente?

□ VS Code aberto com E2_QUALIDADE_E_MEMORIA

□ Terminal split configurado:
  • Esquerda: Editor de código
  • Direita: Execução/Output

□ Navegador aberto com:
  • Paper Few-Shot (GPT-3)
  • Paper Chain-of-Thought
  • OWASP Top 10 for LLM

□ Projetor/compartilhamento de tela testado

□ Áudio/vídeo testado (se remoto)

□ Cronômetro/relógio visível na tela
```

---

## ⏰ DURANTE AULA - TIMELINE

### 19h00-19h10 | ABERTURA (10 min)

```
□ Apresentar objetivos do E2
□ Mostrar progressão v1.8 → v2.0 → v2.5
□ Explicar estrutura da aula (70% prática)
□ Avisar: "Salvem TODOS os outputs!"
□ Perguntar: "Quem tem v1.8 funcionando?"
```

### 19h10-19h20 | TEORIA FEW-SHOT (10 min)

```
□ Explicar conceito Few-Shot (analogia criança+cachorro)
□ DEMO: Zero-Shot vs Few-Shot no Ollama (5 min)
□ Mostrar slide comparativo
□ Perguntar: "Faz sentido?"
```

### 19h20-19h40 | ATIVIDADE 1A (20 min)

```
□ Explicar tarefa: Medir baseline v1.8
□ Instruir: "Abram ATIVIDADE_1A_baseline.py"
□ Dar 15 minutos
□ Circular pela sala ajudando
□ 19h35: Discussão resultados (5 min)
□ Anotar no quadro: Erros comuns
```

### 19h40-20h00 | ATIVIDADE 1B (20 min)

```
□ Explicar: "Criar 3 exemplos de QUALIDADE"
□ Distribuir checklist impresso (7 critérios)
□ Mostrar exemplo RUIM vs BOM no slide
□ Formar duplas
□ Instruir: "Abram ATIVIDADE_1B_criar_exemplos.py"
□ Dar 15 minutos
□ 19h55: Validação coletiva (escolher 2 duplas)
```

### 20h00-20h25 | ATIVIDADE 1C (25 min)

```
□ DEMO ao vivo (5 min):
  • Mostrar v1.8 vs v2.0 lado a lado
  • Executar v2.0 no terminal
  • Apontar diferença no código
□ Instruir: "Abram ATIVIDADE_1C_implementar.py"
□ Dar 20 minutos
□ Circular ajudando (erros de import são comuns)
```

### 20h25-20h30 | ATIVIDADE 1D (15 min)

```
□ Explicar: "Comparar v1.8 vs v2.0 com métricas"
□ Instruir: "Abram ATIVIDADE_1D_comparar.py"
□ Dar 10 minutos
□ Mostrar tabela esperada:
  • Accuracy: v1.8=65%, v2.0=82% (+17pp)
□ Pedir 2-3 alunos compartilharem resultados
```

### 20h30-20h40 | ☕ INTERVALO

```
□ Anunciar: "10 minutos de pausa"
□ Sugerir reflexão:
  • Few-Shot valeu?
  • Exemplos foram bons?
  • Custo vale a pena?
```

### 20h40-20h55 | TEORIA CoT + ATIVIDADE 2A (15 min)

```
□ Explicar conceito CoT (5 min)
□ DEMO: Query complexa com/sem CoT
□ Mostrar slide: Quando usar CoT?
□ Formar trios
□ Instruir: "Abram ATIVIDADE_2A_classificar.py"
□ Dar 10 minutos
□ Discussão: Query mais polêmica?
```

### 20h55-21h05 | ATIVIDADE 2B (10 min)

```
□ DEMO no quadro (3 min):
  • Escrever trace CoT manualmente
  • Query 6: "Marca maior diferença..."
  • Mostrar estrutura Thought→Action→Obs→Answer
□ Instruir: "Abram ATIVIDADE_2B_trace_manual.py"
□ Dar 10 minutos
□ Não precisa discussão (atividade individual)
```

### 21h05-21h25 | ATIVIDADE 2C (20 min)

```
□ DEMO ao vivo (5 min):
  • Mostrar v2.0 vs v2.5 código lado a lado
  • Apontar COT_TEMPLATE
  • Executar v2.5 com query complexa
  • Mostrar output com Thought/Action
□ Instruir: "Abram ATIVIDADE_2C_implementar.py"
□ Dar 15 minutos
□ Circular (problema comum: template não concatenado)
```

### 21h25-21h30 | COMPARAÇÃO v2.0 vs v2.5 (5 min)

```
□ Mostrar tabela comparativa:
  • Queries simples: v2.5 = +5pp
  • Queries complexas: v2.5 = +14pp
  • Latência: +33%
□ Explicar decisão de uso:
  • Simples → v2.0
  • Complexas → v2.5
```

### 21h30-21h40 | ATIVIDADE 3A - MEMORY (10 min)

```
□ Explicar por que Memory?
  • Exemplo: "E Glock?" após "Quantas Taurus?"
□ Instruir: "Abram ATIVIDADE_3A_buffer.py"
□ Rodar demo (auto-executável)
□ Mostrar classe ShortTermMemory no código
□ Explicar trade-off: buffer 5 = +20% tokens
```

### 21h40-21h45 | ATIVIDADE 4A - SECURITY (5 min)

```
□ Explicar tipos de ataque:
  • SQL Injection
  • Prompt Injection
  • Command Injection
□ Instruir: "Abram ATIVIDADE_4A_validation.py"
□ Rodar demo (5 ataques bloqueados)
□ Mostrar classe InputValidator
□ Avisar: "Isso é básico! Produção precisa mais"
```

### 21h45-21h50 | ATIVIDADE 4B - TESTAR (5 min)

```
□ Instruir: "Abram ATIVIDADE_4B_testar_ataque.py"
□ Rodar (testa 10 ataques)
□ Verificar: 100% bloqueados?
□ Não precisa discussão profunda
```

### 21h50-22h00 | ENCERRAMENTO (10 min)

```
□ Resumir o que criaram:
  • v2.0 (Few-Shot)
  • v2.5 (CoT)
  • Memory
  • Security
□ Mostrar progressão final:
  • v1.8: 65% → v2.5: 87% (+22pp!)
□ Perguntas rápidas (3):
  • "Few-Shot valeu?" (levantar mão)
  • "CoT muito lento?" (levantar mão)
  • "Qual técnica teve maior impacto?"
□ Anunciar entregáveis
□ Anunciar próxima aula (E3)
```

---

## 📦 LEMBRAR NO FINAL

```
□ ENTREGA até sexta 19/07:
  • agente_v2.0_fewshot.py
  • agente_v2.5_cot.py
  • exemplos_fewshot.json
  • comparacao_v1_v2.json
  • trace_cot_manual.txt

□ PREPARAR para E3:
  • pip install langchain
  • Revisar código v2.5
```

---

## 🚨 TROUBLESHOOTING (TER À MÃO)

| Problema | Solução |
|----------|---------|
| v1.8 não roda | Pair com colega ou usar `solucao_final/` |
| Ollama travou | `ollama ps` → kill → reiniciar |
| Exemplos não carregam | Verificar path JSON (absoluto vs relativo) |
| v2.5 sem CoT | `print(prompt_system)` → Falta template? |
| Muito lento | Batch (não todos ao mesmo tempo) |

---

## 📊 MÉTRICAS ESPERADAS (PARA VALIDAR)

```
v1.8: Accuracy 60-70%, Latência 2.1s
v2.0: Accuracy 75-85%, Latência 2.4s (+17pp, +0.3s)
v2.5: Accuracy 80-90%, Latência 3.2s (+5pp, +0.8s)

Se divergir muito → Investigar!
```

---

## ✅ PÓS-AULA

```
□ Salvar resultados médios da turma
□ Coletar feedback (Google Forms)
□ Compartilhar gabarito oficial
□ Responder dúvidas fórum (24h)
□ Ajustar timing para próxima turma
□ Arquivar materiais (logs, prints)
```

---

## 🎯 OBJETIVOS VALIDADOS? (PERGUNTAR A 3 ALUNOS)

```
□ "Por que Few-Shot melhora accuracy?"
  ✅ "Exemplos ensinam o LLM"

□ "Quando usar CoT?"
  ✅ "Queries complexas (6+ pontos)"

□ "Vantagem de CoT?"
  ✅ "Raciocínio verificável/debugável"
```

---

**🎓 SE TODOS OS ✅ MARCADOS → AULA FOI SUCESSO!**

_Imprimir e manter na mesa durante a aula_
