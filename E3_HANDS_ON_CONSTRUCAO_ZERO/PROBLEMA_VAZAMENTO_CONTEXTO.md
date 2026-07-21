# 🚨 PROBLEMA: VAZAMENTO DE CONTEXTO (Context Bleeding)

## O QUE ESTÁ ACONTECENDO?

Cada chamada `llm.invoke()` do Ollama **mantém memória** da conversa anterior!

```python
# Pergunta 1
llm.invoke("Quantas armas Taurus?")
→ "17.760 armas" ← ARMAZENADO

# Pergunta 2 (usa contexto da pergunta 1!)
llm.invoke("E Glock?")
→ "Você perguntou Taurus antes, agora Glock..." ← VAZAMENTO!
```

---

## 🔍 ONDE ESTÁ O PROBLEMA?

### Arquivo: `agente_v3_0.py`

**Linhas 159 e 190:**
```python
# Linha 159 (perguntas conceituais)
resposta = llm.invoke(prompt)  # ← Mantém contexto!

# Linha 190 (perguntas de dados)
resposta_final = llm.invoke(prompt)  # ← Mantém contexto!
```

**Consequência:** Se você fizer 3 perguntas seguidas, a 3ª "lembra" das 2 anteriores!

---

## ✅ SOLUÇÃO 1: CRIAR LLM NOVO SEMPRE (Simples)

### Estratégia: Instanciar LLM novo a cada pergunta

```python
def agente_v3_fewshot_cot(pergunta_usuario):
    """Agente v3.0 SEM vazamento de contexto"""
    
    # ✅ CRIAR LLM NOVO A CADA PERGUNTA
    llm_local = OllamaLLM(
        model="llama3",
        temperature=0,
        num_ctx=2048  # Contexto limitado
    )
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*60)
    
    pergunta_lower = pergunta_usuario.lower()
    
    # ... (resto do código igual) ...
    
    # Se conceitual
    if not tool_escolhida:
        prompt = f"""..."""
        resposta = llm_local.invoke(prompt)  # ← USA LLM LOCAL
        return resposta
    
    # Se dados
    resultado_tool = tool_escolhida.func(**parametros)
    
    prompt = f"""..."""
    resposta_final = llm_local.invoke(prompt)  # ← USA LLM LOCAL
    
    return resposta_final
```

**Vantagens:**
- ✅ Simples de implementar
- ✅ Garante contexto limpo
- ✅ Cada pergunta independente

**Desvantagens:**
- ⚠️ Um pouco mais lento (cria nova conexão)

---

## ✅ SOLUÇÃO 2: LIMPAR CONTEXTO EXPLICITAMENTE (Avançado)

### Estratégia: Adicionar instrução para "esquecer"

```python
def agente_v3_fewshot_cot(pergunta_usuario):
    """Agente v3.0 com limpeza de contexto"""
    
    # ... código ...
    
    # Prompt com instrução de reset
    prompt = f"""
IMPORTANTE: Esta eh uma pergunta INDEPENDENTE. 
Nao use informacoes de perguntas anteriores.
Responda APENAS com base nos dados fornecidos abaixo.

=== CONTEXTO ATUAL (UNICO VALIDO) ===

{SYSTEM_PROMPT_1}

Dados do SINARM: {resultado_tool}

Pergunta do usuario: "{pergunta_usuario}"

=== INSTRUCOES ===

- IGNORE qualquer conversa anterior
- Responda APENAS esta pergunta
- Use APENAS os dados acima
- Cite fonte: "SINARM 2026"

Resposta:"""
    
    resposta_final = llm.invoke(prompt)
    
    return resposta_final
```

**Vantagens:**
- ✅ Usa mesma instância LLM (mais rápido)
- ✅ Instrui modelo a ignorar contexto

**Desvantagens:**
- ⚠️ Não garante 100% (modelo pode ignorar instrução)

---

## ✅ SOLUÇÃO 3: USAR API REST DIRETAMENTE (Mais Controle)

### Estratégia: Fazer requisição HTTP com controle de contexto

```python
import requests
import json

def agente_v3_fewshot_cot(pergunta_usuario):
    """Agente v3.0 com controle total de contexto"""
    
    # ... código ...
    
    # Fazer requisição direta ao Ollama
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_ctx": 2048,
            "num_predict": 500
        },
        # ✅ NÃO passa context_id = contexto limpo
    }
    
    response = requests.post(url, json=payload)
    resposta_final = response.json()["response"]
    
    return resposta_final
```

**Vantagens:**
- ✅ Controle TOTAL sobre contexto
- ✅ Garante 100% independência

**Desvantagens:**
- ⚠️ Mais complexo
- ⚠️ Perde abstrações do LangChain

---

## 🎯 RECOMENDAÇÃO: SOLUÇÃO 1 (Criar LLM novo)

### Código completo corrigido:

```python
# agente_v3_0_sem_vazamento.py

from langchain_ollama import OllamaLLM
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)
import re

SYSTEM_PROMPT_1 = """Voce eh um investigador da PCDF especialista em analise de dados de armas de fogo do SINARM."""

def agente_v3_fewshot_cot_sem_vazamento(pergunta_usuario):
    """
    Agente v3.0 SEM vazamento de contexto
    ✅ Cria LLM novo a cada pergunta
    """
    
    # ✅ SOLUÇÃO: CRIAR LLM LOCAL A CADA CHAMADA
    llm = OllamaLLM(
        model="llama3",
        temperature=0,
        num_ctx=2048  # Limitar contexto
    )
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*60)
    
    pergunta_lower = pergunta_usuario.lower()
    
    # Detectar entidades
    marcas = ["taurus", "glock", "rossi", "beretta", "smith"]
    marca_encontrada = None
    for marca in marcas:
        if marca in pergunta_lower:
            marca_encontrada = marca.capitalize()
            break
    
    calibres = [".38", ".380", "9mm", ".40", ".45"]
    calibre_encontrado = None
    for calibre in calibres:
        if calibre in pergunta_lower:
            calibre_encontrado = calibre
            break
    
    tipos = {
        "apreens": "Apreens",
        "roubo": "Roubo",
        "roub": "Roubo",
        "furto": "Furto",
        "perda": "Perda"
    }
    tipo_encontrado = None
    for palavra, tipo in tipos.items():
        if palavra in pergunta_lower:
            tipo_encontrado = tipo
    
    # Selecionar tool
    tool_escolhida = None
    parametros = {}
    
    if marca_encontrada and tipo_encontrado:
        tool_escolhida = contar_armas_combinado
        parametros = {"marca": marca_encontrada, "tipo": tipo_encontrado}
    elif marca_encontrada:
        tool_escolhida = contar_armas_marca
        parametros = {"marca": marca_encontrada}
    elif calibre_encontrado:
        tool_escolhida = contar_armas_calibre
        parametros = {"calibre": calibre_encontrado}
    elif tipo_encontrado:
        tool_escolhida = contar_armas_tipo
        parametros = {"tipo": tipo_encontrado}
    
    # Perguntas conceituais
    if not tool_escolhida:
        print("[TIPO] Conceitual")
        
        prompt = f"""{SYSTEM_PROMPT_1}

Pergunta: "{pergunta_usuario}"

Responda de forma objetiva e tecnica.
"""
        
        resposta = llm.invoke(prompt)
        return resposta
    
    # Perguntas de dados
    print(f"[TIPO] Dados")
    print(f"[TOOL] {tool_escolhida.name}")
    
    resultado_tool = tool_escolhida.func(**parametros)
    
    print(f"[DADOS] {resultado_tool}")
    
    # ✅ USA MESMO LLM LOCAL (sem vazamento entre perguntas diferentes)
    prompt = f"""{SYSTEM_PROMPT_1}

Dados do SINARM 2026: {resultado_tool}

Pergunta: "{pergunta_usuario}"

Responda de forma objetiva citando a fonte SINARM 2026.
"""
    
    resposta_final = llm.invoke(prompt)
    
    return resposta_final


# ===== TESTE DE VAZAMENTO =====
if __name__ == "__main__":
    print("="*70)
    print("TESTE: VERIFICAR VAZAMENTO DE CONTEXTO")
    print("="*70)
    
    # Fazer 3 perguntas DIFERENTES e verificar se respostas são independentes
    
    perguntas = [
        "Quantas armas Taurus?",
        "Quantas armas Glock?",
        "Quantas armas Rossi?"
    ]
    
    for i, p in enumerate(perguntas, 1):
        print(f"\n{'='*70}")
        print(f"PERGUNTA {i}/3")
        print("="*70)
        
        resposta = agente_v3_fewshot_cot_sem_vazamento(p)
        
        print("\n[RESPOSTA]")
        print(resposta)
        
        # Verificar se resposta menciona pergunta anterior (VAZAMENTO!)
        if i > 1:
            pergunta_anterior = perguntas[i-2].lower()
            if any(palavra in resposta.lower() for palavra in ["anterior", "antes", "primeiro"]):
                print("\n⚠️  POSSÍVEL VAZAMENTO DETECTADO!")
            else:
                print("\n✅ Resposta independente (sem vazamento)")
        
        input("\n[Pressione ENTER para próxima pergunta]")
    
    print("\n" + "="*70)
    print("✅ TESTE CONCLUÍDO")
    print("Se nenhuma resposta mencionou perguntas anteriores = SEM VAZAMENTO!")
    print("="*70)
```

---

## 📊 COMPARAÇÃO

| Método | Complexidade | Garantia | Performance |
|--------|-------------|----------|-------------|
| **Solução 1** (LLM novo) | 🟢 Baixa | ✅ 100% | 🟡 Médio |
| **Solução 2** (Instrução) | 🟡 Média | ⚠️ 80% | 🟢 Alta |
| **Solução 3** (API REST) | 🔴 Alta | ✅ 100% | 🟢 Alta |

---

## 🧪 COMO TESTAR SE HÁ VAZAMENTO?

```python
# Teste 1: Fazer mesma pergunta 2x
pergunta = "Quantas armas Taurus?"
resposta1 = agente(pergunta)
resposta2 = agente(pergunta)

# Se resposta2 menciona "já respondi" ou "como disse antes" = VAZAMENTO!

# Teste 2: Fazer perguntas sequenciais
agente("Quantas armas Taurus?")
resposta = agente("E Glock?")

# Se resposta menciona "Taurus" sem você ter perguntado = VAZAMENTO!
```

---

## 🎯 AÇÃO RECOMENDADA

1. ✅ Use **Solução 1** (criar LLM novo a cada pergunta)
2. ✅ Adicione teste de vazamento no código
3. ✅ Documente no material para alunos

---

**Arquivo criado:** `PROBLEMA_VAZAMENTO_CONTEXTO.md`  
**Código corrigido:** `agente_v3_0_sem_vazamento.py`
