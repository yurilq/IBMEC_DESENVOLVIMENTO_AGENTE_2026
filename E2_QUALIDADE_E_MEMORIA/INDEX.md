# 📑 E2: ÍNDICE DE NAVEGAÇÃO RÁPIDA

## 🎯 Acesso Rápido

### 📚 Documentação
- [README_E2.md](README_E2.md) - Guia completo do E2
- [PROPOSTA_ESTRUTURA_MODULAR.md](../PROPOSTA_ESTRUTURA_MODULAR.md) - Arquitetura de pastas
- [TOPICOS_DETALHADOS_E2.md](../TOPICOS_DETALHADOS_E2.md) - Especificação detalhada

---

## 🔢 Atividades Por Conceito

### 1️⃣ FEW-SHOT LEARNING (4 atividades - 80 min)

| # | Atividade | Arquivo | Duração | Objetivo |
|---|-----------|---------|---------|----------|
| 1A | Medir Baseline | [ATIVIDADE_1A_baseline.py](conceitos/01_fewshot/ATIVIDADE_1A_baseline.py) | 20 min | Medir v1.8 Zero-Shot |
| 1B | Criar Exemplos | [ATIVIDADE_1B_criar_exemplos.py](conceitos/01_fewshot/ATIVIDADE_1B_criar_exemplos.py) | 20 min | 3 exemplos qualidade |
| 1C | Implementar | [ATIVIDADE_1C_implementar.py](conceitos/01_fewshot/ATIVIDADE_1C_implementar.py) | 25 min | Agente v2.0 Few-Shot |
| 1D | Comparar | [ATIVIDADE_1D_comparar.py](conceitos/01_fewshot/ATIVIDADE_1D_comparar.py) | 15 min | Medir impacto |

📖 **Teoria**: [EXPLICACAO.md](conceitos/01_fewshot/EXPLICACAO.md)

---

### 2️⃣ CHAIN-OF-THOUGHT (4 atividades - 90 min)

| # | Atividade | Arquivo | Duração | Objetivo |
|---|-----------|---------|---------|----------|
| 2A | Classificar Queries | [ATIVIDADE_2A_classificar.py](conceitos/02_cot/ATIVIDADE_2A_classificar.py) | 15 min | Simples vs Complexa |
| 2B | Trace Manual | [ATIVIDADE_2B_trace_manual.py](conceitos/02_cot/ATIVIDADE_2B_trace_manual.py) | 10 min | Escrever CoT |
| 2C | Implementar | [ATIVIDADE_2C_implementar.py](conceitos/02_cot/ATIVIDADE_2C_implementar.py) | 20 min | Agente v2.5 CoT |
| 2D | Parser (opcional) | [ATIVIDADE_2D_parser.py](conceitos/02_cot/ATIVIDADE_2D_parser.py) | 10 min | Extrair seções |

📄 **Template**: [template_cot.txt](conceitos/02_cot/template_cot.txt)

---

### 3️⃣ MEMORY CONVERSACIONAL (1 atividade - 10 min)

| # | Atividade | Arquivo | Duração | Objetivo |
|---|-----------|---------|---------|----------|
| 3A | Buffer Simples | [ATIVIDADE_3A_buffer.py](conceitos/03_memory_conversacional/ATIVIDADE_3A_buffer.py) | 10 min | Short-term memory |

---

### 4️⃣ SECURITY BASICS (2 atividades - 10 min)

| # | Atividade | Arquivo | Duração | Objetivo |
|---|-----------|---------|---------|----------|
| 4A | Input Validation | [ATIVIDADE_4A_validation.py](conceitos/04_security_basica/ATIVIDADE_4A_validation.py) | 5 min | Proteger inputs |
| 4B | Testar Ataques | [ATIVIDADE_4B_testar_ataque.py](conceitos/04_security_basica/ATIVIDADE_4B_testar_ataque.py) | 5 min | 10 ataques |

---

## 🎯 Soluções Finais

| Versão | Arquivo | Descrição |
|--------|---------|-----------|
| v2.0 | [agente_v2.0_fewshot.py](solucao_final/agente_v2.0_fewshot.py) | Few-Shot integrado |
| v2.5 | [agente_v2.5_cot.py](solucao_final/agente_v2.5_cot.py) | Few-Shot + CoT |
| Demo | [COMPARACAO_V1_V2.py](demo_professor/DEMO_COMPARATIVA_E2.py) | Script comparativo |

📘 **Documentação**: [README_SOLUCAO.md](solucao_final/README_SOLUCAO.md)

---

## 🛠️ Utilitários

| Arquivo | Descrição |
|---------|-----------|
| [utils/tools_sinarm.py](../../utils/tools_sinarm.py) | Tools SINARM compartilhadas (E1-E7) |
| [utils/__init__.py](../../utils/__init__.py) | Inicializador |

---

## 📊 Fluxo de Trabalho Recomendado

```
START
  │
  ├─→ 1A: Medir Baseline (v1.8)
  │     └─→ Resultados: accuracy, latência, erros
  │
  ├─→ 1B: Criar Exemplos Few-Shot
  │     └─→ Output: exemplos_fewshot.json (3 exemplos)
  │
  ├─→ 1C: Implementar v2.0 (Few-Shot)
  │     └─→ Output: agente v2.0 funcionando
  │
  ├─→ 1D: Comparar v1.8 vs v2.0
  │     └─→ Decisão: Few-Shot vale a pena? ✅ Sim (continuar)
  │
  ├─→ 2A: Classificar Queries (Simples/Complexa)
  │     └─→ Entendimento: Quando usar CoT?
  │
  ├─→ 2B: Escrever Trace CoT Manualmente
  │     └─→ Output: trace_cot_query1.txt (prática)
  │
  ├─→ 2C: Implementar v2.5 (CoT)
  │     └─→ Output: agente v2.5 com raciocínio explícito
  │
  ├─→ [2D: Parser CoT - OPCIONAL]
  │
  ├─→ 3A: Implementar Memory (Buffer)
  │     └─→ Output: ShortTermMemory class
  │
  ├─→ 4A: Input Validation
  │     └─→ Output: InputValidator class
  │
  └─→ 4B: Testar Ataques
        └─→ Output: Relatório de segurança
        
END → Agente v2.5 COMPLETO (Few-Shot + CoT + Memory + Security)
```

---

## ⏱️ Estimativa de Tempo

| Bloco | Atividades | Tempo Teórico | Tempo Real* |
|-------|------------|---------------|-------------|
| Few-Shot | 1A-1D | 80 min | 90-120 min |
| CoT | 2A-2C | 60 min | 75-90 min |
| CoT Opcional | 2D | 10 min | 10-15 min |
| Memory | 3A | 10 min | 10-15 min |
| Security | 4A-4B | 10 min | 15-20 min |
| **TOTAL** | **1A-4B** | **170 min** | **200-260 min** |

\* Tempo real inclui leitura de documentação, debugging, experimentação.

---

## 🎓 Para Professores

### Material de Aula
- [demo_professor/DEMO_AULA.py](demo_professor/DEMO_AULA.py) - Demo ao vivo
- [demo_professor/ROTEIRO_PROFESSOR.md](demo_professor/ROTEIRO_PROFESSOR.md) - Timing detalhado
- [demo_professor/resultados_esperados.json](demo_professor/resultados_esperados.json) - Backup

### Slides
- Criados no Gamma.app usando [PROMPTS_CRIACAO_CONTEUDO_E2.md](../PROMPTS_CRIACAO_CONTEUDO_E2.md)
- 40 slides divididos em 4 blocos de 10

---

## 📞 Suporte

### Dúvidas Comuns
- **"Few-Shot não melhorou accuracy"** → Revise exemplos (ATIVIDADE 1B) - qualidade importa!
- **"CoT deixou agente lento"** → Use seletivamente (só queries complexas)
- **"Memory não funciona"** → Verifique buffer_size (default: 5 mensagens)
- **"Ataques passam"** → Adicione regras ao InputValidator (ATIVIDADE 4A)

### Onde Pedir Ajuda
- Fórum da disciplina
- Issues no repositório
- Email do professor
- Monitoria

---

## ✅ Checklist Rápido

Antes de considerar E2 completo, verifique:

- [ ] Executei TODAS as atividades obrigatórias (1A-1D, 2A-2C, 3A, 4A-4B)
- [ ] Comparei v1.8 vs v2.0 vs v2.5 com métricas
- [ ] Few-Shot melhorou accuracy em pelo menos 10pp
- [ ] Entendo quando usar CoT (queries complexas)
- [ ] Memory mantém contexto em conversações
- [ ] Security bloqueia ataques básicos
- [ ] Salvei todos os outputs (JSONs, traces, comparações)
- [ ] Li README_E2.md completo

---

**📌 Atalhos Rápidos**

- [⬆️ Voltar ao README principal](README_E2.md)
- [📂 Ver estrutura de pastas](../PROPOSTA_ESTRUTURA_MODULAR.md)
- [📝 Ver especificação E2](../TOPICOS_DETALHADOS_E2.md)
- [🏠 Voltar à raiz do projeto](../../)

---

_Última atualização: 2026-07-15 | Versão: 1.0_
