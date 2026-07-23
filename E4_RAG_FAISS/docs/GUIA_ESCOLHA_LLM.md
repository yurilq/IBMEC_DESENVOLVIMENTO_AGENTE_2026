# GUIA: ESCOLHENDO SEU LLM

**E4 RAG + FAISS - Configuração Flexível de LLM**

---

## 🎯 QUAL ESCOLHER?

O sistema suporta duas opções de LLM. Escolha baseado em seu cenário:

### 🏠 Ollama (Local) - Para quem tem PC potente

**Use se:**
- ✅ Tem GPU ou PC com 16+ GB RAM
- ✅ Quer privacidade total (dados não saem do PC)
- ✅ Precisa rodar offline
- ✅ Vai fazer muitas requisições (sem custos)
- ✅ Não se importa com latência inicial (60s primeira vez)

**Não use se:**
- ❌ Tem PC fraco (< 8 GB RAM)
- ❌ Precisa de respostas muito rápidas
- ❌ Quer usar modelos de última geração (GPT-4, Claude)

---

### ☁️ OpenRouter (API) - Para quem quer simplicidade

**Use se:**
- ✅ Quer setup rápido (5 minutos)
- ✅ Precisa de respostas rápidas (1-5s)
- ✅ Quer usar melhores modelos (GPT-4, Claude)
- ✅ Tem orçamento (mesmo que pequeno)
- ✅ Sempre tem internet disponível

**Não use se:**
- ❌ Precisa de privacidade total
- ❌ Vai fazer milhares de requisições (custo)
- ❌ Não tem orçamento nenhum
- ❌ Precisa rodar offline

---

## 💰 COMPARAÇÃO DE CUSTOS

### Ollama (Local)
- **Setup:** Grátis
- **Por requisição:** Grátis
- **1.000 requisições:** Grátis
- **Custo mensal:** R$ 0,00

**Custo real:**
- Eletricidade: ~R$ 10-30/mês (se deixar rodando 24/7)
- Hardware: Já possui (GPU/RAM)

---

### OpenRouter (API)

**Exemplo: 1.000 perguntas ao agente**

Cada pergunta usa ~1.000 tokens (input + output):
- **GPT-4o-mini:** $0.15/1M tokens = $0.15 para 1.000 perguntas = **R$ 0,75**
- **GPT-4o:** $5.00/1M tokens = $5.00 para 1.000 perguntas = **R$ 25,00**
- **Claude-3-haiku:** $0.25/1M tokens = $0.25 para 1.000 perguntas = **R$ 1,25**
- **Llama-3:** Grátis (limite: ~100 requisições/dia)

**Para este curso (E4):**
- Você fará ~20-50 perguntas de teste
- Custo: **R$ 0,02 a R$ 1,25** (dependendo do modelo)

---

## ⚡ COMPARAÇÃO DE VELOCIDADE

### Primeira execução:
- **Ollama:** 60-120s (carrega modelo 4.7 GB na RAM)
- **OpenRouter:** 1-3s (modelo já está na nuvem)

### Execuções seguintes:
- **Ollama:** 5-10s (modelo já está na RAM)
- **OpenRouter:** 1-5s (sempre rápido)

### Para 100 perguntas:
- **Ollama:** 60s (primeira) + 10s × 99 = 1.050s = **17 minutos**
- **OpenRouter:** 3s × 100 = 300s = **5 minutos**

---

## 🎓 RECOMENDAÇÃO POR CENÁRIO

### Cenário 1: Aula presencial (professor)
**Recomendação:** **Ollama (local)**
- Privacidade (dados sensíveis SINARM)
- Sem dependência de internet
- Demonstração de LLM local
- Custo zero

**Setup:**
```bash
ollama pull llama3
python testar_config_llm.py
```

---

### Cenário 2: Aluno fazendo exercícios em casa
**Recomendação:** **OpenRouter (API)** com **GPT-4o-mini**
- Setup rápido (5 min)
- Funciona em qualquer PC
- Respostas rápidas
- Custo baixíssimo (R$ 0,10 para todo o exercício)

**Setup:**
```bash
# 1. Obter chave: https://openrouter.ai/keys
# 2. Configurar .env
copy .env.example .env
# Edite e adicione: OPENROUTER_API_KEY=sk-or-v1-...

# 3. Trocar para OpenRouter
trocar_para_openrouter.bat

# 4. Testar
python testar_config_llm.py
```

---

### Cenário 3: Desenvolvimento/testes frequentes
**Recomendação:** **OpenRouter (API)** com **GPT-4o-mini**
- Respostas muito rápidas
- Melhor qualidade de resposta
- Debugging mais ágil
- Custo ainda baixo (R$ 1-5/mês para desenvolvimento)

---

### Cenário 4: Produção (aplicação real)
**Recomendação:** **Ollama (local)** se possível, senão OpenRouter
- Ollama: custo zero em escala
- OpenRouter: flexibilidade de modelos

---

## 🔄 DICA: Use os dois!

Você pode alternar entre Ollama e OpenRouter facilmente:

**Durante desenvolvimento/testes:**
```bash
trocar_para_openrouter.bat  # Rápido, ágil
```

**Em aula/produção:**
```bash
trocar_para_ollama.bat  # Grátis, privado
```

---

## 📊 TABELA RESUMO

| Critério | Ollama | OpenRouter |
|----------|--------|------------|
| **Custo** | Grátis | ~R$ 0,75/1k requisições |
| **Velocidade (primeira)** | 60-120s | 1-3s |
| **Velocidade (depois)** | 5-10s | 1-5s |
| **Setup** | 20 min | 5 min |
| **Privacidade** | Total | Dados vão para API |
| **Qualidade** | Boa (llama3) | Excelente (GPT-4, Claude) |
| **Requisitos HW** | 16 GB RAM | Qualquer PC |
| **Internet** | Não precisa | Necessária |
| **Offline** | Sim | Não |

---

## 🚀 COMEÇAR AGORA

### Opção rápida (5 min): OpenRouter
```bash
# 1. Obter chave: https://openrouter.ai/keys
# 2. Configurar
copy .env.example .env
# Edite .env: 
#   LLM_TYPE=openrouter
#   OPENROUTER_API_KEY=sua_chave
#   OPENROUTER_MODEL=openai/gpt-4o-mini

# 3. Testar
python testar_config_llm.py

# 4. Executar pipeline
executar_completo.bat
```

### Opção grátis (20 min): Ollama
```bash
# 1. Instalar Ollama: https://ollama.ai/download
# 2. Baixar modelo
ollama pull llama3

# 3. Verificar .env (padrão já é Ollama)
# LLM_TYPE=ollama

# 4. Testar
python testar_config_llm.py

# 5. Executar pipeline
executar_completo.bat
```

---

## ❓ FAQ

**P: Posso usar os dois ao mesmo tempo?**
R: Não simultaneamente, mas pode alternar facilmente com os scripts `trocar_para_*.bat`

**P: Quanto custa OpenRouter na prática?**
R: Para este curso: R$ 0,10 a R$ 1,00 total. É basicamente grátis.

**P: Ollama funciona sem GPU?**
R: Sim, mas precisa de muita RAM (16+ GB) e será mais lento.

**P: Posso usar outro modelo no Ollama?**
R: Sim! Edite `OLLAMA_MODEL` no .env. Opções: llama3, mistral, gemma, etc.

**P: Minha chave OpenRouter é segura?**
R: Sim, fica no arquivo .env (não comitar no git). Adicione `.env` ao .gitignore.

**P: OpenRouter tem plano gratuito?**
R: Tem alguns modelos grátis com limite diário (ex: llama-3-8b-instruct).

---

**Criado para:** E4 RAG + FAISS  
**Última atualização:** 22/07/2026  
**Dúvidas?** Consulte o professor/monitor
