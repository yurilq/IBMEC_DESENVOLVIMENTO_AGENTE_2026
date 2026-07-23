# 🔍 DIAGNÓSTICO COMPLETO - PROBLEMA OLLAMA

**Data:** 22/07/2026 19:30  
**Contexto:** Erro ao executar agente v4.5 durante aula

---

## ✅ TESTES REALIZADOS

### 1. Ollama Instalado
```bash
ollama --version
```
**Resultado:** ✅ `ollama version is 0.32.1`

---

### 2. Processo Ollama Rodando
```bash
Get-Process -Name "ollama"
```
**Resultado:** ✅ `PID: 43540` (Ollama está rodando)

---

### 3. Modelos Disponíveis
```bash
ollama list
```
**Resultado:** ✅ 8 modelos encontrados, incluindo `llama3:latest`

---

### 4. API HTTP Respondendo
```bash
curl http://localhost:11434/api/tags
```
**Resultado:** ✅ API responde (mas erro ao parsear JSON no PowerShell)

---

### 5. Invocação Direta do Modelo
```bash
echo "Say Hello" | ollama run llama3
```
**Resultado:** ✅ Modelo responde corretamente

---

### 6. Porta 11434 Listening
```bash
netstat -ano | Select-String "11434"
```
**Resultado:** ✅ `TCP 127.0.0.1:11434 LISTENING` (PID: 43540)

---

### 7. LangChain Ollama (PROBLEMA IDENTIFICADO!)
```python
from langchain_ollama import OllamaLLM
llm = OllamaLLM(model='llama3', temperature=0, num_ctx=4096)
llm.invoke('Say Hello')
```
**Resultado:** ❌ **TIMEOUT após 60 segundos!**

---

## 🎯 PROBLEMA IDENTIFICADO

### Sintoma:
- Ollama funciona perfeitamente via CLI
- LangChain trava ao tentar invocar o modelo
- Timeout após 60 segundos sem resposta

### Possíveis Causas:

#### 1. **Versão Incompatível LangChain-Ollama**
**Hipótese:** `langchain-ollama==1.1.0` pode ter incompatibilidade com Ollama 0.32.1

**Evidência:**
- requirements.txt tinha `1.3.0` (não existe), corrigimos para `1.1.0`
- Ollama está na versão `0.32.1` (recente)
- Pode haver breaking changes na API

**Solução:**
```bash
# Testar com versão mais recente
pip install langchain-ollama --upgrade
```

---

#### 2. **Timeout Padrão Muito Curto**
**Hipótese:** Primeira invocação carrega modelo na memória (pode demorar)

**Evidência:**
- Modelo llama3 tem 4.7 GB
- Primeira invocação sempre é mais lenta
- LangChain pode ter timeout padrão curto

**Solução:**
```python
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3",
    temperature=0,
    num_ctx=4096,
    timeout=120  # ← ADICIONAR timeout maior
)
```

---

#### 3. **Modelo Não Está Pré-carregado**
**Hipótese:** Ollama precisa carregar modelo na RAM antes de responder

**Evidência:**
- `ollama list` mostra modelos, mas não significa que estão carregados
- Primeira invocação pode demorar muito

**Solução:**
```bash
# Pré-carregar modelo antes de executar agente
ollama run llama3 --keep-alive 5m

# Manter modelo em memória por 5 minutos
```

---

#### 4. **Problema de Rede/Localhost**
**Hipótese:** LangChain não consegue se conectar ao localhost:11434

**Evidência:**
- API responde ao curl
- Mas LangChain pode usar cliente HTTP diferente

**Solução:**
```python
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3",
    base_url="http://localhost:11434",  # ← EXPLICITAR URL
    temperature=0,
    num_ctx=4096
)
```

---

#### 5. **Conflito de Versão torch/CUDA**
**Hipótese:** torch instalado é versão CPU, Ollama pode estar esperando GPU

**Evidência:**
- `torch==2.13.0+cpu` (versão CPU)
- Ollama por padrão tenta usar GPU se disponível

**Solução:**
```bash
# Forçar Ollama usar CPU
set OLLAMA_NUM_GPU=0
ollama serve
```

---

## 🔧 SOLUÇÕES RECOMENDADAS (EM ORDEM)

### ✅ Solução 1: Pré-carregar Modelo (MAIS PROVÁVEL)

**Antes de executar o agente:**
```bash
# Terminal 1: Manter modelo carregado
ollama run llama3

# Digitar qualquer coisa para carregar modelo
> teste
[modelo responde]

# Deixar terminal aberto

# Terminal 2: Executar agente
python scripts_agente/agente_v4_5_rag.py
```

**Explicação:**
- Primeira invocação carrega 4.7 GB na RAM
- Pode demorar 30-60 segundos
- LangChain timeout antes de carregar completamente
- Com modelo pré-carregado, responde instantaneamente

---

### ✅ Solução 2: Adicionar Timeout no Código

**Editar `scripts_agente/agente_v4_5_rag.py` linha 43:**

```python
# ANTES:
llm = OllamaLLM(
    model="llama3",
    temperature=0,
    num_ctx=4096
)

# DEPOIS:
llm = OllamaLLM(
    model="llama3",
    temperature=0,
    num_ctx=4096,
    timeout=120,  # ← NOVO: 120 segundos
    request_timeout=120  # ← NOVO: timeout de requisição
)
```

---

### ✅ Solução 3: Atualizar LangChain-Ollama

```bash
# Ativar venv
venv\Scripts\activate

# Atualizar para versão mais recente
pip install langchain-ollama --upgrade

# Verificar versão instalada
pip show langchain-ollama
```

---

### ✅ Solução 4: Usar Modelo Menor para Testes

**Editar `scripts_agente/agente_v4_5_rag.py` linha 44:**

```python
# ANTES:
model="llama3",  # 4.7 GB

# DEPOIS (temporário para testes):
model="llama3.2:1b",  # 1.3 GB - carrega mais rápido
```

**Nota:** Qualidade da resposta pode ser menor, mas serve para testar se o problema é o tempo de carregamento.

---

## 🧪 SCRIPT DE TESTE DIAGNÓSTICO

Salvar como `testar_ollama_langchain.py`:

```python
from langchain_ollama import OllamaLLM
import time

print("="*70)
print("TESTE DE DIAGNOSTICO - OLLAMA + LANGCHAIN")
print("="*70)

configs = [
    {
        "nome": "Teste 1: Configuracao padrao",
        "params": {
            "model": "llama3",
            "temperature": 0,
            "num_ctx": 4096
        }
    },
    {
        "nome": "Teste 2: Com timeout aumentado",
        "params": {
            "model": "llama3",
            "temperature": 0,
            "num_ctx": 4096,
            "timeout": 120
        }
    },
    {
        "nome": "Teste 3: Modelo menor (llama3.2:1b)",
        "params": {
            "model": "llama3.2:1b",
            "temperature": 0,
            "num_ctx": 2048
        }
    }
]

for config in configs:
    print(f"\n{config['nome']}")
    print("-" * 70)
    
    try:
        print("[INFO] Criando instancia LLM...")
        start = time.time()
        llm = OllamaLLM(**config['params'])
        print(f"[OK] LLM criado em {time.time()-start:.2f}s")
        
        print("[INFO] Testando invocacao...")
        start = time.time()
        response = llm.invoke("Say 'Hello'")
        elapsed = time.time() - start
        
        print(f"[SUCCESS] Resposta em {elapsed:.2f}s: {response[:50]}")
        
        # Se chegou aqui, encontramos a configuração que funciona!
        print("\n" + "="*70)
        print("CONFIGURACAO FUNCIONAL ENCONTRADA!")
        print("="*70)
        print(f"Parametros: {config['params']}")
        break
        
    except Exception as e:
        print(f"[ERRO] {type(e).__name__}: {str(e)[:100]}")
        continue

print("\n" + "="*70)
print("FIM DO DIAGNOSTICO")
print("="*70)
```

**Executar:**
```bash
python testar_ollama_langchain.py
```

---

## 📝 RECOMENDAÇÃO PARA A AULA

### Para o Professor:

**ANTES da aula:**
```bash
# 1. Pré-carregar modelo
ollama run llama3
> teste
[deixar rodando]

# 2. Em outro terminal, executar agente
python scripts_agente/agente_v4_5_rag.py
```

**OU aplicar Solução 2 (adicionar timeout) no código**

---

### Para os Alunos:

Adicionar no `README.md` ou `docs/TROUBLESHOOTING.md`:

```markdown
## Problema: Agente trava ao conectar com Ollama

**Sintoma:**
- Ollama funciona via CLI
- Agente trava por 60s e dá timeout

**Solução:**
1. Pré-carregar modelo antes de executar agente:
   ```bash
   ollama run llama3
   # Digite qualquer coisa e deixe rodando
   ```

2. Em outro terminal, execute o agente

**Explicação:**
Primeira invocação carrega 4.7 GB na RAM, pode demorar 30-60s.
LangChain timeout antes de completar. Com modelo pré-carregado,
responde instantaneamente.
```

---

## ✅ CONCLUSÃO

**Problema:** LangChain timeout ao carregar modelo llama3 (4.7 GB)

**Causa raiz:** Primeira invocação demora muito para carregar modelo na RAM

**Soluções (escolher uma):**
1. ✅ **Pré-carregar modelo** (mais simples)
2. ✅ **Adicionar timeout=120** no código (mais robusto)
3. ✅ **Atualizar langchain-ollama** (pode resolver)
4. ✅ **Usar modelo menor** para testes (temporário)

**Recomendação:** Aplicar Solução 1 + Solução 2 (ambas)

---

**Diagnóstico realizado em:** 22/07/2026 19:35  
**Status:** ✅ Problema identificado e soluções propostas  
**Próximo passo:** Testar soluções propostas
