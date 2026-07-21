# 🎓 PARTE 5: FEW-SHOT + CHAIN-OF-THOUGHT

**Horario:** 17:15-18:00 (45 minutos)  
**Objetivo:** Melhorar prompts do agente com tecnicas avancadas  
**Nivel:** Avancado

---

## ⚠️ IMPORTANTE: Continuacao da PARTE 4

**Esta parte usa os arquivos da PARTE 4:**
- ✅ `tools_basicas_v2.py` (4 tools com @tool + cache)
- ✅ `agente_v0_2.py` (agente manual funcional)

**Vamos criar:**
- ✅ `agente_v3_0.py` (versao final com Few-Shot + CoT)

---

## 🎯 O QUE VOCE VAI FAZER

1. Entender Few-Shot Learning (aprender com exemplos)
2. Entender Chain-of-Thought (raciocinio passo a passo)
3. Melhorar prompts do agente manual
4. Testar comparacao: v0_2 vs v3_0

---

## ✅ PRE-REQUISITOS

- [ ] PARTE 4 concluida (agente_v0_2.py funcionando)
- [ ] Entendeu agente manual (ReAct)
- [ ] tools_basicas_v2.py funcionando

---

## 📚 CONCEITOS

### 🧠 Few-Shot Learning

**O que eh:** Ensinar LLM mostrando EXEMPLOS

**Sem Few-Shot:**
```
Pergunta: "O que eh BO de furto?"
LLM: "BO significa... talvez seja... nao tenho certeza..."
```

**Com Few-Shot:**
```
EXEMPLOS:
- Pergunta: "O que eh BO?" → Resposta: "BO = Boletim de Ocorrencia"
- Pergunta: "O que eh furto?" → Resposta: "Furto = crime sem violencia"

Pergunta: "O que eh BO de furto?"
LLM: "BO de furto eh Boletim de Ocorrencia de furto (crime sem violencia)."
```

**Vantagem:** LLM aprende o ESTILO e CONTEXTO!

**IMPORTANTE:** No nosso agente, usamos uma base de conhecimento pre-definida (respostas conceituais) para evitar bloqueios de seguranca do modelo. Isso eh mais confiavel para contextos sensiveis como dados policiais.

---

### 🔗 Chain-of-Thought (CoT)

**O que eh:** LLM mostra RACIOCINIO passo a passo

**Sem CoT:**
```
Pergunta: "Ha mais Taurus ou Glock?"
LLM: "Taurus." (nao explica)
```

**Com CoT:**
```
Pergunta: "Ha mais Taurus ou Glock?"
LLM:
PASSO 1: Vou buscar total Taurus
PASSO 2: Vou buscar total Glock
PASSO 3: Comparar: 17760 > 726
RESPOSTA: Taurus (17760 vs 726 Glock)
```

**Vantagem:** Usuario ve COMO o agente chegou na resposta!

---

## 📋 PASSO A PASSO

### PASSO 1: Criar agente_v3_0.py (15 min)

Crie arquivo novo: `agente_v3_0.py`

```python
# agente_v3_0.py
# Agente v3.0 COM Few-Shot + Chain-of-Thought

from langchain_ollama import OllamaLLM
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)
import re

print("="*60)
print("AGENTE v3.0 - Few-Shot + Chain-of-Thought")
print("="*60)

# PARTE 1: Criar LLM
print("\n[1/4] Criando LLM...")
llm = OllamaLLM(model="llama3.2:1b", temperature=0)
print("      [OK] LLM criado")

# PARTE 2: Registrar tools
print("\n[2/4] Registrando tools...")
tools = [
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
]

for tool in tools:
    print(f"      - {tool.name}")

print("      [OK] 4 tools registradas")

# PARTE 3: Criar agente COM Few-Shot + CoT
print("\n[3/4] Criando agente v3.0...")

# PROMPT COM FEW-SHOT + CHAIN-OF-THOUGHT
SYSTEM_PROMPT = """Voce eh um investigador da PCDF especialista em analise de dados do SINARM.

=== EXEMPLOS (Few-Shot Learning) ===

Exemplo 1:
Pergunta: "O que eh BO de furto?"
Resposta: "BO de furto eh Boletim de Ocorrencia com tipo FURTO no SINARM. Furto eh apropriacao SEM violencia."

Exemplo 2:
Pergunta: "Calibre .38?"
Resposta: "Calibre .38 eh municao de revolver, comum em armas apreendidas no DF."

Exemplo 3:
Pergunta: "Diferenca roubo vs furto?"
Resposta: "ROUBO = com violencia/ameaca. FURTO = sem violencia. Ambos registrados no SINARM."

=== CHAIN-OF-THOUGHT (Sempre seguir) ===

Ao responder QUALQUER pergunta, siga estes PASSOS:

PASSO 1 - ANALISE:
- Tipo de pergunta: dados ou conceito?
- Dados necessarios: marca? calibre? tipo?

PASSO 2 - BUSCA (se precisar):
- Tool escolhida: [qual]
- Parametros: [valores]

PASSO 3 - RESULTADO:
- Valores: [numeros exatos]

PASSO 4 - RESPOSTA FINAL:
- Conclusao objetiva
- Fonte: SINARM 2026

=== INSTRUCOES ===

- Use linguagem tecnica PCDF
- Sempre cite fonte
- Mostre raciocinio (PASSO 1, 2, 3, 4)
- Seja preciso com numeros
"""

def agente_v3_fewshot_cot(pergunta_usuario):
    """
    Agente v3.0 com Few-Shot + Chain-of-Thought
    """
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*60)
    
    pergunta_lower = pergunta_usuario.lower()
    
    # Detectar marca
    marcas = ["taurus", "glock", "rossi", "beretta", "smith"]
    marca_encontrada = None
    for marca in marcas:
        if marca in pergunta_lower:
            marca_encontrada = marca.capitalize()
            break
    
    # Detectar calibre
    calibres = [".38", ".380", "9mm", ".40", ".45"]
    calibre_encontrado = None
    for calibre in calibres:
        if calibre in pergunta_lower:
            calibre_encontrado = calibre
            break
    
    # Detectar tipo
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
            break
    
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
    
    # Se nao identificou dados, responder com conceito
    if not tool_escolhida:
        print("[CHAIN-OF-THOUGHT]")
        print("PASSO 1: Pergunta conceitual (nao precisa de dados)")
        print("PASSO 2: Consultar conhecimento interno")
        print("PASSO 3: Formular resposta tecnica")
        
        prompt = f"""{SYSTEM_PROMPT}

Pergunta do usuario: "{pergunta_usuario}"

IMPORTANTE: Esta eh uma pergunta CONCEITUAL (nao precisa buscar dados).
Responda usando os EXEMPLOS como guia.
Mostre seu RACIOCINIO (PASSO 1, 2, 3, 4).

Resposta:"""
        
        resposta = llm.invoke(prompt)
        return resposta
    
    # Se identificou dados, chamar tool
    print("[CHAIN-OF-THOUGHT]")
    print(f"PASSO 1: Pergunta sobre DADOS")
    print(f"PASSO 2: Tool escolhida = {tool_escolhida.name}")
    print(f"PASSO 3: Buscando dados...")
    
    resultado_tool = tool_escolhida.func(**parametros)
    
    print(f"PASSO 4: Dados obtidos = {resultado_tool}")
    print(f"PASSO 5: Formatando resposta...")
    
    # Extrair numero
    numeros = re.findall(r'\d+', resultado_tool)
    total = numeros[0] if numeros else "?"
    
    prompt = f"""{SYSTEM_PROMPT}

Dados do SINARM: {resultado_tool}

Pergunta do usuario: "{pergunta_usuario}"

IMPORTANTE: 
- Responda de forma OBJETIVA
- Cite a fonte: "SINARM 2026"
- Mostre confianca (voce tem os dados!)

Resposta:"""
    
    resposta_final = llm.invoke(prompt)
    
    return resposta_final

print("      [OK] Agente v3.0 pronto")

# PARTE 4: Testar
print("\n[4/4] Testando agente v3.0...")
print("="*60)

perguntas = [
    "Quantas armas Taurus existem?",
    "O que eh BO de furto?",
    "Ha mais Taurus ou Glock?"  # Requer 2 buscas (desafio!)
]

for i, pergunta in enumerate(perguntas, 1):
    print(f"\n{'='*60}")
    print(f"TESTE {i}:")
    print("="*60)
    
    resposta = agente_v3_fewshot_cot(pergunta)
    
    print("\n[RESPOSTA FINAL]")
    print(resposta)
    print()

print("="*60)
print("AGENTE v3.0 CONCLUIDO!")
print("="*60)
```

---

### PASSO 2: Testar agente_v3_0.py (10 min)

Execute:

```bash
python agente_v3_0.py
```

**Observe:**
1. **Teste 1** (dados): Mostra Chain-of-Thought (PASSO 1, 2, 3, 4, 5)
2. **Teste 2** (conceito): Usa Few-Shot (exemplos ensinaram o estilo)
3. **Teste 3** (complexo): Requer 2 tools (desafio avancado!)

---

### PASSO 3: Comparar v0_2 vs v3_0 (10 min)

**Professor vai demonstrar ao vivo:**

**agente_v0_2.py (PARTE 4):**
```
Pergunta: "Quantas armas Taurus?"
Resposta: "17760"  # Seco, sem contexto
```

**agente_v3_0.py (PARTE 5):**
```
Pergunta: "Quantas armas Taurus?"
[CHAIN-OF-THOUGHT]
PASSO 1: Pergunta sobre DADOS
PASSO 2: Tool escolhida = contar_armas_marca
PASSO 3: Buscando dados...
PASSO 4: Dados obtidos = Encontrei 17760 armas...
PASSO 5: Formatando resposta...

Resposta: "Existem 17.760 armas Taurus registradas no SINARM 2026."
# Mais profissional, cita fonte!
```

**Diferenca:**
- v0_2: Funcional, basico
- v3_0: Profissional, mostra raciocinio, cita fonte

---

## ✅ CHECKPOINT 5

- [ ] agente_v3_0.py criado
- [ ] Teste 1 funcionou (dados)
- [ ] Teste 2 funcionou (conceito - Few-Shot)
- [ ] Viu Chain-of-Thought (PASSO 1, 2, 3, 4, 5)
- [ ] Entendeu diferenca v0_2 vs v3_0

---

## 🎓 DESAFIO AVANCADO (10 min)

**Teste 3 do agente_v3_0.py:**

```python
pergunta = "Ha mais Taurus ou Glock?"
```

**Problema:** Precisa chamar **2 tools diferentes**:
1. `contar_armas_marca("Taurus")` → 17760
2. `contar_armas_marca("Glock")` → 726
3. Comparar: 17760 > 726

**Atualmente:** Agente so chama 1 tool por vez!

**Exercicio:** Como voce modificaria o agente para:
1. Detectar que precisa de 2 buscas?
2. Chamar ambas as tools?
3. Comparar resultados?

**Dica:** Adicionar logica de detecao de palavras comparativas ("mais", "maior", "vs", "ou")

---

## 📚 CONCEITOS APRENDIDOS

✅ **Few-Shot Learning**: Ensinar LLM com exemplos  
✅ **Chain-of-Thought**: Mostrar raciocinio passo a passo  
✅ **System Prompt**: Instrucoes permanentes para LLM  
✅ **Prompt Engineering**: Arte de escrever prompts eficazes  
✅ **Contexto PCDF**: Vocabulario tecnico especializado  
✅ **Citacao de Fonte**: Credibilidade profissional

---

## 🎯 COMPARACAO FINAL

### EVOLUCAO DO AGENTE

**PARTE 2 - agente_v0_1.py:**
- 1 tool manual
- Sem decorators
- Basico, funcional

**PARTE 4 - agente_v0_2.py:**
- 4 tools com @tool
- Cache otimizado
- Selecao automatica de tool

**PARTE 5 - agente_v3_0.py:**
- 4 tools com @tool + cache
- Few-Shot Learning
- Chain-of-Thought
- Prompts profissionais
- Vocabulario PCDF

---

## 📊 COMPARACAO DE SAIDA

### Pergunta: "Quantas armas Taurus?"

**v0_1 (PARTE 2):**
```
17760
```

**v0_2 (PARTE 4):**
```
17760
```

**v3_0 (PARTE 5):**
```
[CHAIN-OF-THOUGHT]
PASSO 1: Pergunta sobre DADOS
PASSO 2: Tool escolhida = contar_armas_marca
PASSO 3: Buscando dados...
PASSO 4: Dados obtidos = Encontrei 17760 armas da marca 'TAURUS ARMAS S.A.'
PASSO 5: Formatando resposta...

[RESPOSTA FINAL]
Existem 17.760 armas Taurus registradas no SINARM 2026, 
conforme dados de ocorrencias do Distrito Federal.
```

**Evolucao clara!** 🚀

---

## 🔍 TECNICAS EXTRAS (Opcional)

### 1. Validacao de Input

```python
def validar_input(texto: str) -> bool:
    """Valida input do usuario"""
    # Bloquear SQL injection
    if any(x in texto.lower() for x in ["drop", "delete", "truncate"]):
        return False
    
    # Bloquear comandos shell
    if any(x in texto for x in [";", "|", "&", "$"]):
        return False
    
    return True

# Usar antes do agente
if not validar_input(pergunta):
    print("ERRO: Input invalido!")
```

### 2. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(max_calls=5, period=60):
    """Limita chamadas por periodo"""
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remover chamadas antigas
            calls[:] = [c for c in calls if now - c < period]
            
            if len(calls) >= max_calls:
                print(f"ERRO: Maximo {max_calls} chamadas por {period}s")
                return None
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=10, period=60)
def agente_protegido(pergunta):
    return agente_v3_fewshot_cot(pergunta)
```

### 3. Logging Profissional

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='agente.log'
)

logger = logging.getLogger(__name__)

def agente_com_log(pergunta):
    logger.info(f"Pergunta recebida: {pergunta}")
    try:
        resposta = agente_v3_fewshot_cot(pergunta)
        logger.info(f"Resposta gerada: {resposta[:100]}...")
        return resposta
    except Exception as e:
        logger.error(f"Erro: {e}")
        raise
```

---

## 📝 RESUMO DA PARTE 5

**Arquivo criado:**
- ✅ `agente_v3_0.py` (Few-Shot + Chain-of-Thought)

**Conceitos dominados:**
- ✅ Few-Shot Learning (aprender com exemplos)
- ✅ Chain-of-Thought (raciocinio explicito)
- ✅ System Prompts (instrucoes permanentes)
- ✅ Prompt Engineering (escrever prompts eficazes)
- ✅ Vocabulario especializado (PCDF)

**Evolucao completa:**
- v0_1: Basico (PARTE 2)
- v0_2: Otimizado (PARTE 4)
- v3_0: Profissional (PARTE 5)

---

## 🎉 CURSO CONCLUIDO!

**Parabens! Voce completou E3 - Hands-On Construcao Zero!**

**Voce aprendeu:**
1. ✅ LLMs e Ollama (PARTE 1)
2. ✅ Primeira Tool manual (PARTE 2)
3. ✅ Decorators Python (PARTE 3)
4. ✅ 4 Tools + Cache (PARTE 4)
5. ✅ Few-Shot + CoT (PARTE 5)

**Proximos passos:**
- 🚀 LangGraph (agentes complexos)
- 🚀 RAG (Retrieval-Augmented Generation)
- 🚀 Multi-Agent Systems
- 🚀 Production deployment

---

**Parte:** 5/5  
**Tempo:** 45 minutos  
**Status:** ✅ ATUALIZADO LangChain 1.3+  
**Testado:** ✅ Python 3.11 + Ollama llama3.2:1b  
**Alinhado:** ✅ PARTE 4 (agente manual + tools_basicas_v2)
