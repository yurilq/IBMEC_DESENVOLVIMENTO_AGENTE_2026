# LLAMA 3.2 TEM FUNCIONALIDADE DE AGENTES?

## ✅ SIM! Llama 3.2 tem SUPORTE NATIVO para Tool Calling (Agentes)

---

## 🔍 EVIDÊNCIAS NO MODELFILE

Ao rodar `ollama show llama3.2:1b --modelfile`, encontramos:

### **1. Detecção de Tools no Template**

```
{{- if .Tools }}When you receive a tool call response, use the output to format an answer to the orginal user question.

You are a helpful assistant with tool calling capabilities.
{{- end }}
```

**Significado:** O modelo SABE quando ferramentas estão disponíveis e muda seu comportamento.

---

### **2. Formato JSON para Tool Calling**

```
Given the following functions, please respond with a JSON for a function call with its proper arguments that best answers the given prompt.

Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}. Do not use variables.
```

**Significado:** O modelo foi TREINADO para retornar JSON estruturado escolhendo ferramentas!

---

### **3. Role "tool" Suportada**

```
{{- else if eq .Role "tool" }}<|start_header_id|>ipython<|end_header_id|>

{{ .Content }}<|eot_id|>
```

**Significado:** O modelo entende conversas com ferramentas (user → assistant → tool → assistant).

---

## 🎯 O QUE ISSO SIGNIFICA?

### **Llama 3.2 É UM MODELO DE AGENTE NATIVO!**

Diferente do Llama 3.0, o **Llama 3.2** foi especificamente treinado para:

1. ✅ **Entender listas de ferramentas** disponíveis
2. ✅ **Escolher qual ferramenta usar** baseado na pergunta
3. ✅ **Retornar JSON estruturado** com nome da ferramenta e parâmetros
4. ✅ **Processar resultados de ferramentas** e formular resposta final

---

## 📊 COMPARAÇÃO: Llama 3.0 vs 3.2

| Capacidade | Llama 3.0 | Llama 3.2 |
|------------|-----------|-----------|
| **Tool Calling Nativo** | ❌ NÃO | ✅ SIM |
| **Retorna JSON estruturado** | ⚠️ Inconsistente | ✅ Confiável |
| **Entende role "tool"** | ❌ NÃO | ✅ SIM |
| **Treinado para agentes** | ❌ NÃO | ✅ SIM (Sept 2024) |
| **Precisa de prompt manual** | ✅ SIM | ⚠️ Opcional |

---

## 🚀 COMO USAR COM LANGCHAIN

### **Método 1: LangChain Nativo (Recomendado)**

```python
from langchain_ollama import ChatOllama
from langchain_core.tools import tool

# Definir tool
@tool
def contar_armas_marca(marca: str) -> str:
    """Conta quantas armas de uma marca específica."""
    # ... código ...
    return f"Encontrei {total} armas {marca}"

# Criar modelo com suporte a tools
llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)

# BIND tools ao modelo (Llama 3.2 entende automaticamente!)
llm_with_tools = llm.bind_tools([contar_armas_marca])

# Usar
response = llm_with_tools.invoke("Quantas armas Taurus?")

# Llama 3.2 retorna:
# {
#   "name": "contar_armas_marca",
#   "parameters": {"marca": "Taurus"}
# }
```

**Vantagens:**
- ✅ Llama 3.2 ESCOLHE a tool automaticamente
- ✅ Retorna JSON estruturado
- ✅ Não precisa de prompt manual complicado
- ✅ LangChain gerencia o ciclo ReAct

---

### **Método 2: Prompt Manual (Como fizemos em v4.0)**

```python
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2:1b", temperature=0)

prompt = f"""
Ferramentas disponíveis:
1. contar_armas_marca - Conta armas de uma marca
2. contar_armas_calibre - Conta armas de um calibre

Pergunta: "{pergunta}"

Responda em JSON: {{"name": "...", "parameters": {{...}}}}
"""

resposta = llm.invoke(prompt)
```

**Desvantagens:**
- ⚠️ Mais trabalho manual
- ⚠️ Precisa parsear JSON manualmente
- ⚠️ Gerenciar ciclo ReAct manualmente

---

## 💡 POR QUE FIZEMOS v4.0 COM PROMPT MANUAL?

### **Razão Pedagógica:**

**v3.0 → v4.0 → v5.0 (evolução)**

1. **v3.0:** if/elif hardcoded (fundamentos)
   - Ensina: tools, decorators, lógica básica

2. **v4.0:** Prompt manual para LLM escolher
   - Ensina: como LLMs escolhem, JSON parsing, ReAct manual
   - **Mostra "por dentro" como funciona**

3. **v5.0:** LangChain `.bind_tools()` (profissional)
   - Ensina: uso profissional, abstrações, agentes reais
   - **Usa capacidade nativa do Llama 3.2**

---

## 🎓 IMPLICAÇÃO PARA A AULA

### **DECISÃO: Mostrar TODAS as 3 versões!**

#### **Aula Atual (E3):**
- v3.0: Fundamentos (if/elif) ← **JÁ FEITO**
- v3.1: Comparações ← **JÁ FEITO**
- v4.0: Prompt manual ← **JÁ FEITO**

#### **Próxima Aula (E4):**
- **v5.0: Usar `.bind_tools()` nativo do Llama 3.2** ← **NOVO!**

**Por quê?**
1. Alunos veem EVOLUÇÃO completa
2. Entendem "por dentro" antes de usar abstrações
3. Aprendem capacidades nativas do Llama 3.2
4. Prontos para produção (uso profissional)

---

## 🔧 IMPLEMENTAÇÃO: Agente v5.0 (Nativo)

```python
# agente_v5_0_nativo.py
# Usa capacidade NATIVA de tool calling do Llama 3.2

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Definir tools
@tool
def contar_armas_marca(marca: str) -> str:
    """Conta quantas armas de uma marca específica no SINARM 2026."""
    # ... código ...
    return resultado

@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta quantas armas de um calibre específico no SINARM 2026."""
    # ... código ...
    return resultado

@tool
def contar_armas_tipo(tipo: str) -> str:
    """Conta ocorrências de um tipo específico no SINARM 2026."""
    # ... código ...
    return resultado

# Criar modelo
llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)

# BIND tools (Llama 3.2 entende nativamente!)
llm_with_tools = llm.bind_tools([
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo
])

def agente_v5_nativo(pergunta: str):
    """
    Agente v5.0 que usa capacidade NATIVA de tool calling do Llama 3.2
    
    DIFERENÇA de v4.0:
    - v4.0: Prompt manual + JSON parsing manual
    - v5.0: .bind_tools() + LangChain gerencia tudo
    """
    
    print(f"\n[PERGUNTA] {pergunta}")
    print("-"*70)
    
    # PASSO 1: LLM escolhe tool (AUTOMÁTICO!)
    print("\n[PASSO 1] Llama 3.2 analisando e escolhendo tool...")
    
    response = llm_with_tools.invoke([HumanMessage(content=pergunta)])
    
    # Llama 3.2 retornou tool call?
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        
        print(f"[LLM ESCOLHEU] {tool_call['name']}")
        print(f"[PARAMETROS] {tool_call['args']}")
        
        # PASSO 2: Executar tool
        print(f"\n[PASSO 2] Executando tool...")
        
        # Mapear nome para função
        tools_map = {
            "contar_armas_marca": contar_armas_marca,
            "contar_armas_calibre": contar_armas_calibre,
            "contar_armas_tipo": contar_armas_tipo
        }
        
        tool_func = tools_map[tool_call['name']]
        resultado = tool_func.func(**tool_call['args'])
        
        print(f"[RESULTADO] {resultado}")
        
        # PASSO 3: LLM formula resposta final
        print(f"\n[PASSO 3] Llama 3.2 formulando resposta final...")
        
        # Criar mensagem de tool result
        messages = [
            HumanMessage(content=pergunta),
            response,
            ToolMessage(
                content=resultado,
                tool_call_id=tool_call['id']
            )
        ]
        
        final_response = llm.invoke(messages)
        
        return final_response.content
    
    else:
        # Pergunta conceitual (sem tool)
        print("[TIPO] Pergunta conceitual (LLM responde diretamente)")
        return response.content


# TESTE
if __name__ == "__main__":
    perguntas = [
        "Quantas armas Taurus?",
        "Quantas armas calibre .38?",
        "O que é BO de furto?"
    ]
    
    for p in perguntas:
        print("\n" + "="*70)
        resposta = agente_v5_nativo(p)
        print(f"\n[RESPOSTA FINAL]\n{resposta}")
```

---

## 📈 EVOLUÇÃO COMPLETA

### **Trajetória de Aprendizado:**

```
v3.0: Script com if/elif
   ↓ "Mas isso não é agente de verdade..."
   ↓
v4.0: LLM escolhe via prompt manual
   ↓ "Ah! LLM pode escolher tools!"
   ↓
v5.0: Usa capacidade nativa do Llama 3.2
   ↓ "Uau! O modelo foi treinado para isso!"
   ↓
PRODUÇÃO: Agente profissional
```

---

## ✅ RESPOSTA À PERGUNTA

### **"Llama 3.2 tem funcionalidade de agentes?"**

**SIM! Absolutamente!** 🎯

**Evidências:**
1. ✅ Template nativo para tool calling
2. ✅ Retorna JSON estruturado
3. ✅ Entende role "tool"
4. ✅ Treinado especificamente para isso (Sept 2024)
5. ✅ LangChain tem suporte via `.bind_tools()`

**Implicação:**
- v4.0 (prompt manual) é **educacional**
- v5.0 (nativo) é **profissional**
- Ambos são válidos e complementares!

---

## 🎯 RECOMENDAÇÃO PARA AULA

### **Aula E3 (Atual):**
✅ Continuar com v3.0, v3.1, v4.0 (fundamentos + prompt manual)

### **Aula E4 (Próxima):**
✅ Introduzir v5.0 usando `.bind_tools()` nativo do Llama 3.2

**Mensagem aos Alunos:**

> "Vocês aprenderam a construir agentes DO ZERO (v3.0 → v4.0).
>  Agora vamos usar a capacidade NATIVA do Llama 3.2!
>  O modelo JÁ FOI TREINADO para escolher ferramentas.
>  Vamos apenas 'desbloquear' essa funcionalidade! 🚀"

---

## 📚 REFERÊNCIAS

- **Llama 3.2 Release:** September 25, 2024
- **Tool Calling:** Nativo no template
- **LangChain Docs:** https://python.langchain.com/docs/integrations/chat/ollama
- **Ollama Docs:** https://ollama.ai/blog/tool-support

---

**TL;DR:** SIM! Llama 3.2 tem tool calling nativo. v4.0 (manual) é educacional. v5.0 (nativo) é profissional. Mostre AMBOS! 🎓
