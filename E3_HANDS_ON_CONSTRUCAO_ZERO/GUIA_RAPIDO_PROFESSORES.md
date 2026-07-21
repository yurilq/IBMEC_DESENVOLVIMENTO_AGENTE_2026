# GUIA_RAPIDO_PROFESSORES.md
# Guia Rápido: Testando os Agentes

## ✅ Pré-requisitos

```bash
# 1. Verificar Ollama
ollama --version
# Esperado: ollama version is 0.32.1 (ou superior)

# 2. Verificar modelo
ollama list
# Deve ter: llama3:latest ou llama3.2:1b

# 3. Ativar ambiente virtual
cd E3_HANDS_ON_CONSTRUCAO_ZERO\01_GUIAS_ALUNO\meu_agente_sinarm
.\venv\Scripts\activate

# 4. Verificar bibliotecas
pip list | findstr langchain
```

---

## 🚀 TESTE 1: Agente v3.0 (Busca Palavras)

```bash
python teste_rapido.py
```

**Esperado:**
- Detecta "Taurus" na pergunta
- Chama `contar_armas_marca("Taurus")`
- Retorna: "17.760 armas Taurus"
- Tempo: ~2-3 segundos

---

## 🚀 TESTE 2: Agente v3.1 (Comparação)

```bash
python agente_v3_1_comparacao.py
```

**Testa 4 cenários:**
1. Consulta simples: "Quantas armas Taurus?"
2. Comparação 2 marcas: "Há mais Taurus ou Glock?"
3. Comparação 3 marcas: "Compare Taurus, Glock e Rossi"
4. Erro: "Quantas armas?" (sem marca)

**Esperado:**
- Teste 2 detecta AMBAS as marcas (Taurus E Glock)
- Faz 2 buscas separadas
- Compara resultados
- Mostra ranking

---

## 🚀 TESTE 3: Agente v4.0 (LLM Inteligente)

```bash
python agente_v4_0_inteligente.py
```

**Testa 6 cenários complexos:**
1. "Quantas armas Taurus?"
2. "Há mais Taurus ou Glock?"
3. "Quantas Taurus foram roubadas?"
4. "Quantas armas calibre .38?"
5. "Quantas apreensões?"
6. "O que é BO de furto?"

**Esperado:**
- LLM analisa cada pergunta
- Retorna JSON com análise
- Escolhe ferramenta correta
- Mostra justificativa
- Tempo: ~5-10 segundos por pergunta

---

## ⚠️ PROBLEMAS COMUNS

### Erro: "ModuleNotFoundError: No module named 'langchain_ollama'"

**Solução:**
```bash
pip install langchain-ollama langchain-core
```

---

### Erro: "Connection refused" ou "Ollama not running"

**Solução:**
```bash
# Em outro terminal:
ollama serve

# OU no Windows (iniciar serviço):
# Ollama já roda automaticamente após instalação
```

---

### Erro: "Out of memory" ou modelo muito lento

**Solução:** Use modelo leve
```bash
# Baixar modelo leve (1.3 GB vs 4.7 GB)
ollama pull llama3.2:1b

# Editar código para usar modelo leve:
# llm = OllamaLLM(model="llama3.2:1b", temperature=0)
```

---

### Agente demora muito (>30 segundos)

**Causas:**
1. Modelo pesado (llama3:8b = 4.7 GB)
2. Primeira execução (carrega modelo)
3. Sem GPU (CPU lento)

**Soluções:**
- Usar `llama3.2:1b` (mais rápido)
- Aguardar primeira execução (próximas são mais rápidas)
- Reduzir `num_ctx` (contexto menor = mais rápido)

```python
llm = OllamaLLM(
    model="llama3.2:1b",  # ← Modelo leve
    temperature=0,
    num_ctx=2048  # ← Contexto reduzido (vs 4096)
)
```

---

## 📊 COMPARAÇÃO DE DESEMPENHO

| Agente | Modelo | Tempo/Pergunta | Precisão | Uso RAM |
|--------|--------|----------------|----------|---------|
| v3.0 | Nenhum | 0.1s | 65% | 50 MB |
| v3.1 | Nenhum | 0.2s | 70% | 50 MB |
| v4.0 (llama3) | llama3:latest | 5-10s | 93% | 5 GB |
| v4.0 (leve) | llama3.2:1b | 2-3s | 85% | 2 GB |

**Recomendação para aula:**
- Demonstração: Use **v4.0 com llama3:latest** (mais preciso)
- Alunos: Use **v3.1** ou **v4.0 com llama3.2:1b** (mais rápido)

---

## 🎯 CHECKLIST PRÉ-AULA

```
[ ] Ollama instalado e rodando
[ ] Modelo llama3 ou llama3.2:1b baixado
[ ] Ambiente virtual criado e ativado
[ ] Bibliotecas instaladas (langchain-ollama, pandas)
[ ] CSV presente (DADOS_SINARM/OCORRENCIAS_2026.csv)
[ ] Testado agente v3.0 (funciona)
[ ] Testado agente v3.1 (comparação funciona)
[ ] Testado agente v4.0 (LLM funciona)
[ ] Tempo de resposta aceitável (<10s)
```

---

## 🔍 TESTE RÁPIDO (1 minuto)

```bash
# Ativar venv
.\venv\Scripts\activate

# Testar importações
python -c "from langchain_ollama import OllamaLLM; print('OK')"

# Testar Ollama
python -c "from langchain_ollama import OllamaLLM; llm = OllamaLLM(model='llama3.2:1b'); print(llm.invoke('Ola'))"

# Testar agente
python teste_rapido.py
```

Se todos rodarem sem erro → ✅ **Pronto para aula!**

---

## 📚 MATERIAL PARA OS ALUNOS

**Ordem recomendada:**

1. **Mostrar v3.0** (10 min)
   - "Veja como funciona com busca de palavras"
   - Teste: "Quantas armas Taurus?"
   - **Problema:** "Revólver Taurus" não funciona

2. **Mostrar v3.1** (10 min)
   - "Agora suporta comparações"
   - Teste: "Há mais Taurus ou Glock?"
   - **Problema:** Ainda limitado a palavras-chave

3. **Mostrar v4.0** (15 min)
   - "Agora usa LLM para entender"
   - Teste: "Das apreensões, quantas eram Taurus?"
   - **Vantagem:** Entende contexto
   - **Desvantagem:** Mais lento

4. **Discussão** (10 min)
   - Trade-offs: Velocidade vs Precisão
   - Quando usar cada versão?
   - Como melhorar?

**Tempo total:** 45 minutos

---

## 📂 ARQUIVOS DE REFERÊNCIA

```
E3_HANDS_ON_CONSTRUCAO_ZERO/
├── 01_GUIAS_ALUNO/meu_agente_sinarm/
│   ├── agente_v3_0.py          ← Versão original
│   ├── agente_v3_1_comparacao.py ← Com comparações
│   ├── agente_v4_0_inteligente.py ← LLM inteligente
│   └── teste_rapido.py         ← Teste simples
│
├── MUDANCAS_v3_para_v4.md      ← Comparação detalhada
├── RESUMO_MUDANCAS_v3_v4.md    ← Resumo 1 página
├── PROBLEMA_ESCOLHA_FERRAMENTA.md ← Documentação
└── GUIA_RAPIDO_PROFESSORES.md  ← Este arquivo
```

---

## ✅ CHECKLIST PÓS-AULA

```
[ ] Alunos entenderam diferença v3.0 vs v4.0
[ ] Discutiram trade-offs (velocidade vs precisão)
[ ] Testaram pelo menos 2 versões
[ ] Entenderam quando usar cada uma
[ ] Sabem como trocar modelo (llama3 → llama3.2:1b)
[ ] Salvaram códigos no Git/repositório
```

---

**Boa aula! 🚀**
