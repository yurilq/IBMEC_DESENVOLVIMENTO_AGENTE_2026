# ⚠️ IMPORTANTE: MUDANÇAS LANGCHAIN 1.3+

**Data descoberta:** 20/07/2026  
**Versão instalada:** LangChain 1.3.13  
**Impacto:** ALTO - Código E2 (antigo) não funciona mais!

---

## 🚨 PROBLEMA

```python
# ❌ NÃO FUNCIONA MAIS (LangChain < 1.0)
from langchain.agents import Tool, initialize_agent, AgentType

agente = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # ...
)
```

**Erro:**
```
ImportError: cannot import name 'Tool' from 'langchain.agents'
ImportError: cannot import name 'initialize_agent' from 'langchain.agents'
```

---

## ✅ SOLUÇÃO

### **O que mudou:**

| Item | LangChain < 1.0 (E2) | LangChain 1.3+ (E3) |
|------|---------------------|---------------------|
| **Tool** | `langchain.agents.Tool` | `langchain_core.tools.Tool` |
| **initialize_agent** | ✅ Existe | ❌ REMOVIDO |
| **AgentType** | ✅ Existe | ❌ REMOVIDO |
| **create_react_agent** | ❌ Não existe | ❌ Também não existe! |

### **Nova abordagem:**

LangChain 1.3+ não tem mais "agentes prontos". Você constrói **manualmente**.

---

## 📝 CÓDIGO ATUALIZADO

### **Imports corretos:**

```python
# ✅ CORRETO (LangChain 1.3+)
from langchain_ollama import OllamaLLM
from langchain_core.tools import Tool  # ← mudou de lugar!
```

### **Agente manual (sem initialize_agent):**

```python
from langchain_ollama import OllamaLLM
from langchain_core.tools import Tool
import re

# Criar LLM
llm = OllamaLLM(model="llama3.2:1b", temperature=0)

# Criar Tool
tool_contar = Tool(
    name="contar_armas_marca",
    func=contar_armas_marca,
    description="Conta armas de uma marca. Input: nome da marca"
)

# Criar agente MANUAL (ciclo ReAct explícito)
def agente_simples(pergunta_usuario):
    """Implementa ReAct manualmente"""
    
    # THOUGHT: Identificar intenção
    print(f"[THOUGHT] Processando: '{pergunta_usuario}'")
    
    # Detectar marca
    marcas = ["taurus", "glock", "rossi"]
    marca = None
    for m in marcas:
        if m in pergunta_usuario.lower():
            marca = m.capitalize()
            break
    
    if not marca:
        return "Marca não identificada"
    
    # ACTION: Chamar tool
    print(f"[ACTION] Chamando: {tool_contar.name}('{marca}')")
    resultado = tool_contar.func(marca)
    
    # OBSERVATION
    print(f"[OBSERVATION] {resultado}")
    
    # THOUGHT + ANSWER: Formatar com LLM
    print("[THOUGHT] Formatando resposta...")
    prompt = f"Dados: {resultado}\nResponda direto:"
    resposta = llm.invoke(prompt)
    
    return resposta

# Usar
resposta = agente_simples("Quantas armas Taurus?")
print(f"RESPOSTA: {resposta}")
```

---

## 🔄 COMPARAÇÃO

### **LangChain < 1.0 (E2 - Antiga):**

```python
# Código "mágico" - oculta implementação
from langchain.agents import initialize_agent, AgentType

agente = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    tools=[tool],
    llm=llm,
    verbose=True
)

resposta = agente.invoke({"input": "pergunta"})
```

**Vantagens:**
- ✅ Poucas linhas
- ✅ "Funciona" rápido

**Desvantagens:**
- ❌ "Mágico" (não sabe o que acontece)
- ❌ Pouco controle
- ❌ Difícil customizar

---

### **LangChain 1.3+ (E3 - Nova):**

```python
# Código explícito - você controla tudo
from langchain_core.tools import Tool

def agente_simples(pergunta):
    # THOUGHT
    print("[THOUGHT] Analisando...")
    # ... sua lógica
    
    # ACTION
    print("[ACTION] Chamando tool...")
    resultado = tool.func(input)
    
    # OBSERVATION
    print(f"[OBSERVATION] {resultado}")
    
    # ANSWER
    resposta = llm.invoke(prompt)
    return resposta
```

**Vantagens:**
- ✅ Controle total
- ✅ Entende cada passo
- ✅ Fácil customizar
- ✅ Transparente (nada oculto)

**Desvantagens:**
- ⚠️ Mais linhas de código
- ⚠️ Precisa implementar ReAct manualmente

---

## 🎓 PARA A AULA

### **Impacto:**

- ✅ **POSITIVO**: Alunos aprendem como agente funciona **por baixo**
- ✅ **PEDAGÓGICO**: Implementar ReAct manualmente = entender melhor
- ⚠️ **ATENÇÃO**: Código E2 (slides antigos) NÃO funciona mais

### **O que fazer:**

1. **NÃO** usar `initialize_agent` (não existe!)
2. **NÃO** usar `AgentType` (não existe!)
3. **SIM** construir agente manual
4. **SIM** explicar ciclo ReAct explicitamente

### **Vantagem pedagógica:**

```python
# Antes (E2): "mágico"
agente = initialize_agent(...)  # O que acontece aqui? 🤷

# Agora (E3): "explícito"
def agente_simples(pergunta):
    # THOUGHT
    print("[THOUGHT] ...")  # ← ALUNO VÊ!
    
    # ACTION
    print("[ACTION] ...")   # ← ALUNO VÊ!
    
    # OBSERVATION
    print("[OBSERVATION]...") # ← ALUNO VÊ!
```

**Resultado**: Aluno entende **exatamente** o que é ReAct!

---

## 📦 VERSÕES

### **Verificar versão instalada:**

```bash
python -c "import langchain; print(langchain.__version__)"
```

### **Versões importantes:**

| Versão | Status | initialize_agent | AgentType | Tool Location |
|--------|--------|------------------|-----------|---------------|
| 0.0.x - 0.2.x | Antiga | ✅ Tem | ✅ Tem | `langchain.agents` |
| 1.0.x - 1.2.x | Transição | ⚠️ Deprecated | ⚠️ Deprecated | `langchain_core.tools` |
| 1.3.x+ | Nova | ❌ Removido | ❌ Removido | `langchain_core.tools` |

### **Instalar versão específica (se necessário):**

```bash
# Downgrade para versão antiga (NÃO RECOMENDADO)
pip install langchain==0.2.16

# Manter versão nova (RECOMENDADO)
pip install --upgrade langchain langchain-core
```

---

## 🔧 MIGRAÇÃO RÁPIDA

### **Se você tem código antigo (E2):**

**ANTES:**
```python
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")

tool = Tool(name="...", func=..., description="...")

agente = initialize_agent(
    tools=[tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

resposta = agente.invoke({"input": "pergunta"})
```

**DEPOIS:**
```python
from langchain_core.tools import Tool  # ← mudou!
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2:1b")

tool = Tool(name="...", func=..., description="...")

# Agente manual
def agente_simples(pergunta):
    # Identificar se precisa tool
    # ...
    
    # Chamar tool
    resultado = tool.func(input_detectado)
    
    # Formatar com LLM
    resposta = llm.invoke(f"Dados: {resultado}")
    
    return resposta

# Usar
resposta = agente_simples("pergunta")
```

---

## 📚 REFERÊNCIAS

**Changelog LangChain:**
- https://github.com/langchain-ai/langchain/releases

**Migration Guide (oficial):**
- https://python.langchain.com/docs/versions/migrating_chains/

**Arquivos atualizados neste projeto:**
- `agente_v0_1.py` - ✅ Atualizado
- `agente_v0_1_final.py` - ✅ Atualizado
- `PARTE_2_PRIMEIRA_TOOL.md` - ⚠️ Precisa atualizar

---

## ⚠️ ATENÇÃO PROFESSORES

**Se você usou código E2 em aulas anteriores:**

1. ✅ Avise alunos que API mudou
2. ✅ Explique que é **evolução natural** (bibliotecas mudam)
3. ✅ Use como oportunidade de ensinar sobre **breaking changes**
4. ✅ Mostre que "construir manualmente" = **mais aprendizado**

**Vantagem:**
- Alunos entendem **como funciona** (não é "mágica")
- Prepara para quando precisarem customizar
- Ensina realidade de desenvolvimento (libs mudam!)

---

## 🎯 RESUMO

| Aspecto | Mudança |
|---------|---------|
| **Tool** | `langchain.agents` → `langchain_core.tools` |
| **initialize_agent** | ❌ Removido → Implementar manualmente |
| **AgentType** | ❌ Removido → Construir ReAct explícito |
| **Complexidade código** | Simples → Mais linhas |
| **Transparência** | "Mágico" → Explícito |
| **Aprendizado** | Superficial → Profundo ✅ |

---

**Arquivo:** MUDANCAS_LANGCHAIN_1_3.md  
**Localização:** 04_MATERIAL_APOIO/  
**Status:** ✅ Documentado  
**Impacto:** CRÍTICO - Atualizar todos guias!

**Mudanças são oportunidades de aprendizado! 📚**
