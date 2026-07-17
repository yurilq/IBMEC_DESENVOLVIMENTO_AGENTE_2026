# 📋 ROTEIRO COMPLETO E3 - CONSTRUÇÃO DO ZERO
## Terça-feira 28/07/2026 | 13h00 - 18h00

**Para:** Professor  
**Duração:** 5 horas (4h trabalho + 1h pausas)  
**Objetivo:** Construir agente SINARM completo passo a passo COM os alunos

---

## 🎯 VISÃO GERAL DO DIA

### **O que construir:**
```python
# agente_v2_0_completo.py (~150 linhas)
# 
# Inclui:
# ✅ 4 Tools SINARM (@tool decorator)
# ✅ Cache (@lru_cache para performance)
# ✅ Few-Shot (3-5 exemplos PCDF)
# ✅ Chain-of-Thought (5 passos estruturados)
# ✅ Validação básica (security contra injection)
# 
# NÃO inclui:
# ❌ Memory (deixar para E4)
```

### **Foco Especial:**
⭐ **PARTE 3 (15:15-16:00): EXPLICAR @DECORATOR PROFUNDAMENTE**
- 45 minutos dedicados
- Analogia visual
- 6 exemplos progressivos
- Conectar @tool e @lru_cache

---

## ⏰ CRONOGRAMA DETALHADO

### **PARTE 1: Setup + Hello World (13:00-13:45) - 45 min**

#### **13:00-13:15 | Verificar Ambiente (15 min)**

**Objetivo:** Garantir que todos estão prontos para começar

**Checklist projetar:**
```
VERIFICAÇÃO DE AMBIENTE
═══════════════════════

Digite no terminal:

1️⃣ python --version
   ✅ Esperado: Python 3.9 ou superior

2️⃣ ollama list
   ✅ Esperado: llama3 instalado

3️⃣ code --version
   ✅ Esperado: VSCode instalado

4️⃣ ls DADOS_SINARM/
   ✅ Esperado: OCORRENCIAS_2026.csv presente

TODOS PRONTOS? VAMOS COMEÇAR! 🚀
```

**Ações:**
- Perguntar: "Quem tem erro em algum item?"
- Resolver problemas individuais (máx 10 min)
- Se maioria OK, seguir (ajudar resto depois)

---

#### **13:15-13:30 | Hello World LLM (15 min)**

**Objetivo:** Ver LLM responder pela primeira vez

**Instrução aos alunos:**
```
"Vamos criar nosso primeiro arquivo.
Abram VSCode e criem: teste_llm.py"
```

**Codar JUNTO (linha por linha):**

```python
# teste_llm.py
# Nosso primeiro contato com LLM

# LINHA 1: Importar LangChain
from langchain_ollama import OllamaLLM

# Pausa: "O que é OllamaLLM?"
# Resposta: "Conexão com modelo local Ollama"

# LINHA 2: Criar conexão
llm = OllamaLLM(model="llama3")

# Pausa: "O que fizemos?"
# Resposta: "Criamos objeto que fala com Ollama"

# LINHA 3: Enviar pergunta
resposta = llm.invoke("Olá, tudo bem?")

# Pausa: "O que é invoke?"
# Resposta: "Enviar mensagem e receber resposta"

# LINHA 4: Mostrar resposta
print(resposta)

# Pausa: "O que print faz?"
# Resposta: "Mostra na tela"
```

**Testar AGORA:**
```bash
python teste_llm.py
```

**Checkpoint Visual:**
```
✅ CHECKPOINT 1: LLM RESPONDEU?

Se sim: "Parabéns! LLM funciona! 🎉"
Se não: "Vamos debugar juntos"

Erros comuns:
- Ollama não rodando: ollama serve
- Modelo não existe: ollama pull llama3
```

---

#### **13:30-13:45 | Entender o Código (15 min)**

**Discussão guiada:**

**Pergunta 1:** "O que é a linha 1?"
- Importar = trazer ferramenta de outro lugar
- OllamaLLM = ferramenta para falar com Ollama

**Pergunta 2:** "O que é a linha 2?"
- Criar objeto = preparar ferramenta
- model="llama3" = escolher qual modelo usar

**Pergunta 3:** "O que é a linha 3?"
- invoke = enviar pergunta
- resposta = guardar o que volta

**Pergunta 4:** "O que é a linha 4?"
- print = mostrar na tela

**Exercício rápido:**
"Mude a pergunta para 'Quantas armas existem?' e rode de novo"

---

### **☕ PAUSA (13:45-14:00) - 15 min**

---

### **PARTE 2: Primeira Tool SEM Decorator (14:00-15:00) - 60 min**

#### **14:00-14:20 | Criar Função Python Simples (20 min)**

**Objetivo:** Criar função que conta armas antes de virar tool

**Instrução:**
```
"Vamos criar uma FUNÇÃO PYTHON normal.
Ainda NÃO é tool! Só função Python básica.

Criem arquivo: tools_basicas.py"
```

**Codar JUNTO:**

```python
# tools_basicas.py
# Funções para consultar SINARM

import pandas as pd

def contar_armas_marca(marca: str):
    """Conta quantas armas de uma marca"""
    
    # PASSO 1: Carregar CSV
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", 
                     sep=";", encoding="latin1")
    
    # Pausa: "O que é DataFrame?"
    # Resposta: "Tabela em memória (como Excel)"
    
    # PASSO 2: Filtrar por marca
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    
    # Pausa: "O que é filtro?"
    # Resposta: "Pegar só linhas que atendem condição"
    
    # PASSO 3: Contar linhas
    total = len(resultado)
    
    # PASSO 4: Retornar texto
    return f"Encontrei {total} armas {marca}"

# Fim da função
```

**Testar ISOLADO:**
```python
# Adicionar no final do arquivo:
if __name__ == "__main__":
    resultado = contar_armas_marca("Taurus")
    print(resultado)
```

**Rodar:**
```bash
python tools_basicas.py
```

**Checkpoint:**
```
✅ CHECKPOINT 2: FUNÇÃO RETORNA NÚMERO?

Esperado: "Encontrei 17760 armas Taurus"
Se sim: Função funciona! ✅
Se não: Debugar (caminho CSV? encoding?)
```

---

#### **14:20-14:40 | Conectar Função ao LLM (SEM decorator) (20 min)**

**Objetivo:** Fazer LLM chamar nossa função (manualmente)

**Instrução:**
```
"Agora vamos conectar função ao LLM.
Ainda SEM @decorator! Jeito 'chato' primeiro.

Criem arquivo: agente_v0_1.py"
```

**Codar JUNTO:**

```python
# agente_v0_1.py
# Agente básico SEM decorator

from langchain_ollama import OllamaLLM
from langchain.agents import Tool, initialize_agent, AgentType
from tools_basicas import contar_armas_marca

# PARTE 1: Criar LLM
print("Criando LLM...")
llm = OllamaLLM(model="llama3", temperature=0)

# PARTE 2: Criar Tool MANUALMENTE (jeito chato)
print("Criando tool manualmente...")
tool_contar = Tool(
    name="ContarArmas",
    func=contar_armas_marca,
    description="Conta armas por marca. Use: ContarArmas('Taurus')"
)

# Pausa: "O que é Tool()?"
# Resposta: "Embrulho que permite LLM chamar nossa função"

# PARTE 3: Criar agente
print("Criando agente...")
agente = initialize_agent(
    tools=[tool_contar],        # Lista de tools
    llm=llm,                    # LLM para usar
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True                # Mostrar pensamento
)

# PARTE 4: Testar
print("\n" + "="*60)
print("TESTANDO AGENTE")
print("="*60 + "\n")

pergunta = "Quantas armas Taurus existem?"
resposta = agente.invoke({"input": pergunta})
print(f"\n✅ RESPOSTA: {resposta['output']}\n")
```

**Rodar:**
```bash
python agente_v0_1.py
```

**O que observar:**
```
THOUGHT: Preciso contar armas Taurus
ACTION: ContarArmas("Taurus")
OBSERVATION: Encontrei 17760 armas Taurus
FINAL ANSWER: Há 17.760 armas Taurus
```

**Checkpoint:**
```
✅ CHECKPOINT 3: AGENTE CHAMOU A FUNÇÃO?

Se verbose mostra THOUGHT → ACTION → OBSERVATION: ✅
Se não: Debugar (Ollama rodando? Sintaxe correta?)
```

---

#### **14:40-15:00 | Entender Código Linha por Linha (20 min)**

**Discussão profunda:**

**Bloco 1: LLM**
```python
llm = OllamaLLM(model="llama3", temperature=0)
```
- "Por que temperature=0?"
- Resposta: "Respostas determinísticas (sempre iguais)"

**Bloco 2: Tool Manual**
```python
tool_contar = Tool(
    name="ContarArmas",
    func=contar_armas_marca,
    description="..."
)
```
- "Por que precisamos Tool()?"
- Resposta: "LLM precisa saber NOME, O QUE FAZ, COMO USAR"
- "Isso é chato de repetir! Existe jeito melhor?"
- Resposta: "@decorator! Vamos ver depois da pausa!"

**Bloco 3: AgentExecutor**
```python
agente = initialize_agent(
    tools=[...],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
```
- "O que é ZERO_SHOT_REACT?"
- Resposta: "Padrão ReAct: THOUGHT → ACTION → OBSERVATION"

**Bloco 4: Invoke**
```python
resposta = agente.invoke({"input": pergunta})
```
- "Por que dicionário {"input": ...}?"
- Resposta: "Formato que agente espera"

---

### **☕ PAUSA (15:00-15:15) - 15 min**

**Durante pausa:** Preparar slides decorators

---

### **PARTE 3: EXPLICAÇÃO @DECORATOR (15:15-16:00) - 45 min ⭐**

**FOCO ESPECIAL: REFORÇAR DECORATORS PROFUNDAMENTE**

#### **15:15-15:25 | O Que É Uma Função Normal? (10 min)**

**Slide 1: Função Simples**

Projetar e codar:

```python
# exemplo_funcao.py

def somar(a, b):
    """Soma dois números"""
    return a + b

# Testar
resultado = somar(2, 3)
print(f"2 + 3 = {resultado}")  # 5
```

**Perguntar:** "Todos entendem função básica?"

**Slide 2: Problema - Código Repetido**

```python
# Quero adicionar LOG em toda função

def somar(a, b):
    print("Chamando somar...")  # ← Repetir!
    resultado = a + b
    print(f"Resultado: {resultado}")  # ← Repetir!
    return resultado

def multiplicar(a, b):
    print("Chamando multiplicar...")  # ← Repetir!
    resultado = a * b
    print(f"Resultado: {resultado}")  # ← Repetir!
    return resultado

def dividir(a, b):
    print("Chamando dividir...")  # ← Repetir!
    resultado = a / b
    print(f"Resultado: {resultado}")  # ← Repetir!
    return resultado
```

**Perguntar:** "Viram o problema? Estamos repetindo código!"

---

#### **15:25-15:35 | O Que É Um Decorator? (10 min)**

**Slide 3: Analogia do Embrulho**

Desenhar na lousa:

```
ANALOGIA: Decorator é PAPEL DE PRESENTE

┌─────────────────────────┐
│    PAPEL DE PRESENTE    │  ← Decorator (adiciona funcionalidade)
│  ┌─────────────────┐   │
│  │   PRESENTE      │   │  ← Função original
│  │   (função)      │   │
│  └─────────────────┘   │
└─────────────────────────┘

Decorator "embrulha" função SEM mudar o presente dentro!
```

**Explicar:**
- Presente = função original
- Papel = decorator (adiciona algo)
- Presente embrulhado = função decorada

**Slide 4: Anatomia do Decorator**

```python
@decorator_name
def minha_funcao():
    pass

# É a mesma coisa que:
minha_funcao = decorator_name(minha_funcao)
```

---

#### **15:35-15:45 | Exemplo Prático 1: Decorator Manual (10 min)**

**Slide 5: Criar Decorator**

Codar JUNTO:

```python
# decorator_exemplo.py

# PASSO 1: Criar função decorator
def mostrar_log(funcao):
    """Decorator que adiciona log"""
    
    def funcao_embrulhada(a, b):
        # ANTES de chamar função
        print(f"Chamando {funcao.__name__}...")
        
        # CHAMAR função original
        resultado = funcao(a, b)
        
        # DEPOIS de chamar função
        print(f"Resultado: {resultado}")
        
        return resultado
    
    return funcao_embrulhada

# PASSO 2: Usar decorator
@mostrar_log
def somar(a, b):
    return a + b

@mostrar_log
def multiplicar(a, b):
    return a * b

# PASSO 3: Testar
print("="*40)
somar(2, 3)
print("="*40)
multiplicar(4, 5)
print("="*40)
```

**Rodar:**
```bash
python decorator_exemplo.py
```

**Saída esperada:**
```
========================================
Chamando somar...
Resultado: 5
========================================
Chamando multiplicar...
Resultado: 20
========================================
```

**Checkpoint:**
```
✅ CHECKPOINT 4: ENTENDEU DECORATOR?

Perguntar aos alunos:
- "O que @mostrar_log faz?"
- "Por que não precisamos repetir print em cada função?"
- "Decorator mudou a função somar por dentro?"
```

---

#### **15:45-15:55 | Conectar com @tool e @lru_cache (10 min)**

**Slide 6: Decorators Prontos**

Explicar:

```python
# Agora vocês entendem decorators!
# 
# LangChain e Python têm decorators PRONTOS:
#
# 1️⃣ @tool (LangChain)
#    └─ "Embrulha" função para LLM reconhecer
#
# 2️⃣ @lru_cache (Python)
#    └─ "Embrulha" função para guardar resultado (cache)
```

**Slide 7: Exemplo @tool**

```python
from langchain_core.tools import tool

# ANTES (jeito chato):
def contar_armas(marca):
    return f"Encontrei X armas {marca}"

tool_manual = Tool(
    name="ContarArmas",
    func=contar_armas,
    description="Conta armas"
)

# DEPOIS (com @tool):
@tool
def contar_armas(marca: str):
    """Conta armas por marca"""  # ← description automática!
    return f"Encontrei X armas {marca}"

# Pronto! @tool faz o "embrulho" automaticamente!
```

**Slide 8: Exemplo @lru_cache**

```python
from functools import lru_cache

# Problema: Ler CSV toda vez é LENTO

def carregar_csv():
    print("Lendo CSV...") # ← Executa TODA vez!
    df = pd.read_csv("arquivo.csv")
    return df

# Solução: Cache!

@lru_cache(maxsize=1)
def carregar_csv():
    print("Lendo CSV...") # ← Executa SÓ na 1ª vez!
    df = pd.read_csv("arquivo.csv")
    return df

# Primeira chamada: Lê CSV (lento)
# Segunda chamada: USA CACHE (rápido!)
```

---

#### **15:55-16:00 | Recap + Perguntas (5 min)**

**Recap Visual:**

```
O QUE APRENDEMOS:
═══════════════════════════════════════

1️⃣ Função normal: faz uma coisa

2️⃣ Problema: repetir código é ruim

3️⃣ Decorator: "embrulha" função para adicionar funcionalidade

4️⃣ @tool: embrulha função para LLM reconhecer

5️⃣ @lru_cache: embrulha função para guardar resultado

═══════════════════════════════════════
ENTENDERAM? ✅
```

**Perguntas aos alunos:**
- "Alguém tem dúvida sobre decorators?"
- "Conseguem explicar @tool para um colega?"
- "Por que @lru_cache é útil?"

---

### **☕ PAUSA (16:00-16:15) - 15 min**

---

### **PARTE 4: Agente com 4 Tools + Cache (16:15-17:15) - 60 min**

#### **16:15-16:35 | Refatorar Tool 1 com @tool (20 min)**

**Objetivo:** Simplificar código usando @tool

**Instrução:**
```
"Vamos REFATORAR nossa tool usando @tool decorator.
Muito mais simples!

Modifiquem tools_basicas.py"
```

**Codar JUNTO:**

```python
# tools_basicas.py (VERSÃO 2 - com @tool)

import pandas as pd
from langchain_core.tools import tool

# VERSÃO ANTIGA (comentada):
# def contar_armas_marca(marca: str):
#     df = pd.read_csv(...)
#     ...

# VERSÃO NOVA (com @tool):
@tool
def contar_armas_marca(marca: str) -> str:
    """Conta quantas armas de uma marca específica.
    
    Args:
        marca: Nome da marca (ex: Taurus, Glock)
    
    Returns:
        String com total encontrado
    """
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    total = len(resultado)
    return f"Encontrei {total} armas {marca}"
```

**Modificar agente_v0_1.py:**

```python
# agente_v0_1.py (VERSÃO 2)

from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from tools_basicas import contar_armas_marca  # Agora já é @tool!

llm = OllamaLLM(model="llama3", temperature=0)

# ANTES precisava Tool():
# tool_contar = Tool(name="...", func=..., description="...")

# AGORA direto:
agente = initialize_agent(
    tools=[contar_armas_marca],  # ← Direto! Mais simples!
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Testar
resposta = agente.invoke({"input": "Quantas Taurus?"})
print(resposta["output"])
```

**Checkpoint:**
```
✅ CHECKPOINT 5: @TOOL FUNCIONA?

Agente responde igual antes? Sim: ✅
Código ficou mais simples? Sim: ✅
```

---

#### **16:35-16:55 | Adicionar Tools 2, 3, 4 (20 min)**

**Objetivo:** 4 tools funcionando

**Instrução:**
```
"Vamos adicionar mais 3 tools.
Mesmo padrão: @tool decorator."
```

**Codar JUNTO (tools_basicas.py):**

```python
# ... (tool 1 já existe)

@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta armas por calibre.
    
    Args:
        calibre: Calibre da arma (ex: .38 TPC, 9mm)
    """
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    resultado = df[df["CALIBRE"] == calibre]
    total = len(resultado)
    return f"Encontrei {total} armas calibre {calibre}"

@tool
def contar_armas_tipo(tipo: str) -> str:
    """Conta armas por tipo de ocorrência.
    
    Args:
        tipo: Tipo (ex: Apreensão, Roubo, Furto)
    """
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    resultado = df[df["TIPO_OCORRENCIA"] == tipo.upper()]
    total = len(resultado)
    return f"Encontrei {total} ocorrências tipo {tipo}"

@tool
def contar_armas_combinado(marca: str, tipo: str) -> str:
    """Conta armas por marca E tipo simultaneamente.
    
    Args:
        marca: Marca da arma
        tipo: Tipo de ocorrência
    """
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    resultado = df[
        (df["MARCA_ARMA"] == marca.upper()) & 
        (df["TIPO_OCORRENCIA"] == tipo.upper())
    ]
    total = len(resultado)
    return f"Encontrei {total} armas {marca} do tipo {tipo}"
```

**Atualizar agente:**

```python
# agente_v0_1.py (VERSÃO 3 - 4 tools)

from tools_basicas import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)

agente = initialize_agent(
    tools=[
        contar_armas_marca,
        contar_armas_calibre,
        contar_armas_tipo,
        contar_armas_combinado
    ],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Testar com 4 perguntas
perguntas = [
    "Quantas armas Taurus?",
    "Quantas armas calibre .38 TPC?",
    "Quantas apreensões?",
    "Quantas Taurus foram roubadas?"
]

for p in perguntas:
    print(f"\n{'='*60}\nPERGUNTA: {p}\n{'='*60}")
    resposta = agente.invoke({"input": p})
    print(f"RESPOSTA: {resposta['output']}\n")
```

**Checkpoint:**
```
✅ CHECKPOINT 6: 4 TOOLS FUNCIONAM?

Cada pergunta usa tool certa? ✅
Última pergunta usa tool 4 (combinado)? ✅
```

---

#### **16:55-17:15 | Adicionar @lru_cache para Performance (20 min)**

**Objetivo:** Cache acelera consultas

**Problema:**
"Cada tool lê CSV do zero! Lento! 4 perguntas = 4 leituras!"

**Solução:**
"@lru_cache lê UMA VEZ, guarda na memória"

**Codar JUNTO:**

```python
# tools_basicas.py (VERSÃO 4 - com cache)

import pandas as pd
from functools import lru_cache  # ← Novo import
from langchain_core.tools import tool

# NOVA FUNÇÃO: Carregar CSV com cache
@lru_cache(maxsize=1)
def carregar_csv():
    """Carrega CSV UMA VEZ e guarda em cache"""
    print("🔄 Carregando CSV...")  # ← Ver quando lê
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    print(f"✅ CSV carregado! {len(df)} linhas")
    return df

# REFATORAR todas as tools para usar cache:

@tool
def contar_armas_marca(marca: str) -> str:
    """Conta armas por marca"""
    df = carregar_csv()  # ← USA CACHE!
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    return f"Encontrei {len(resultado)} armas {marca}"

@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta armas por calibre"""
    df = carregar_csv()  # ← USA CACHE!
    resultado = df[df["CALIBRE"] == calibre]
    return f"Encontrei {len(resultado)} armas calibre {calibre}"

@tool
def contar_armas_tipo(tipo: str) -> str:
    """Conta armas por tipo"""
    df = carregar_csv()  # ← USA CACHE!
    resultado = df[df["TIPO_OCORRENCIA"] == tipo.upper()]
    return f"Encontrei {len(resultado)} ocorrências tipo {tipo}"

@tool
def contar_armas_combinado(marca: str, tipo: str) -> str:
    """Conta armas por marca E tipo"""
    df = carregar_csv()  # ← USA CACHE!
    resultado = df[
        (df["MARCA_ARMA"] == marca.upper()) & 
        (df["TIPO_OCORRENCIA"] == tipo.upper())
    ]
    return f"Encontrei {len(resultado)} armas {marca} tipo {tipo}"
```

**Testar com timing:**

```python
import time

print("\nTESTANDO CACHE:")
print("="*60)

perguntas = [
    "Quantas Taurus?",
    "Quantas Glock?",
    "Quantas Rossi?",
    "Quantas Beretta?"
]

for i, p in enumerate(perguntas, 1):
    inicio = time.time()
    resposta = agente.invoke({"input": p})
    fim = time.time()
    tempo = fim - inicio
    print(f"\n{i}. {p}")
    print(f"   Tempo: {tempo:.2f}s")
    print(f"   Resposta: {resposta['output']}")
```

**Observar saída:**
```
1. Quantas Taurus?
   🔄 Carregando CSV...
   ✅ CSV carregado! 500000 linhas
   Tempo: 3.5s  ← PRIMEIRA vez: LENTO

2. Quantas Glock?
   Tempo: 0.2s  ← CACHE! RÁPIDO!

3. Quantas Rossi?
   Tempo: 0.2s  ← CACHE! RÁPIDO!

4. Quantas Beretta?
   Tempo: 0.2s  ← CACHE! RÁPIDO!
```

**Checkpoint:**
```
✅ CHECKPOINT 7: CACHE FUNCIONA?

1ª pergunta lenta? Sim (lê CSV): ✅
2ª-4ª rápidas? Sim (usa cache): ✅
Viu mensagem "Carregando CSV" só 1 vez? Sim: ✅
```

---

### **☕ PAUSA (17:15-17:30) - 15 min**

---

### **PARTE 5: Few-Shot + CoT + Security (17:30-18:00) - 30 min**

#### **17:30-17:40 | Adicionar Few-Shot (10 min)**

**Objetivo:** Agente entende contexto PCDF

**Problema:**
"Agente não conhece siglas PCDF (BO, furto vs roubo, etc)"

**Solução:**
"Few-Shot: Dar exemplos!"

**Codar JUNTO (agente_v0_1.py → agente_v2_0.py):**

```python
# agente_v2_0.py (VERSÃO FINAL - Parte 1)

from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from tools_basicas import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)

# LLM
llm = OllamaLLM(model="llama3", temperature=0)

# SYSTEM MESSAGE com FEW-SHOT
system_message = """
Você é investigador PCDF especialista em SINARM.

=== EXEMPLOS (Few-Shot Learning) ===

Pergunta: "O que é BO de furto?"
Resposta: "BO de furto é Boletim de Ocorrência tipo=Furto no SINARM"

Pergunta: "Calibre .38?"
Resposta: "Calibre .38 TPC é munição de revólver, catalogado no SINARM"

Pergunta: "Arma roubada?"
Resposta: "Arma roubada tem tipo=Roubo no SINARM (diferente de Furto)"

=== INSTRUÇÕES ===

Use linguagem técnica PCDF.
Sempre cite "Fonte: SINARM OCORRENCIAS_2026.csv".
"""

# Criar agente com system message
agente = initialize_agent(
    tools=[contar_armas_marca, contar_armas_calibre,
           contar_armas_tipo, contar_armas_combinado],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"system_message": system_message}
)

# Testar
resposta = agente.invoke({"input": "O que é BO de furto?"})
print(resposta["output"])
```

**Checkpoint:**
```
✅ CHECKPOINT 8: FEW-SHOT MELHOROU?

ANTES: "BO é boletim de ocorrência..." (genérico)
DEPOIS: "BO de furto é tipo=Furto no SINARM" (específico)

Resposta ficou mais técnica? ✅
```

---

#### **17:40-17:50 | Adicionar Chain-of-Thought (10 min)**

**Objetivo:** Agente mostra raciocínio

**Adicionar ao system_message:**

```python
system_message = """
Você é investigador PCDF especialista em SINARM.

=== EXEMPLOS (Few-Shot) ===
[... exemplos anteriores ...]

=== CHAIN-OF-THOUGHT (Sempre seguir) ===

Ao responder QUALQUER pergunta, siga estes passos:

PASSO 1 - ANÁLISE:
- O que está sendo perguntado?
- É pergunta sobre dados (use tools) ou conceito (explique)?

PASSO 2 - BUSCA:
- Se dados: qual tool usar?
- Quais parâmetros passar?

PASSO 3 - RESULTADO:
- O que as tools retornaram?
- Valores exatos.

PASSO 4 - RESPOSTA:
- Conclusão clara.
- Sempre citar: "Fonte: SINARM OCORRENCIAS_2026.csv"

=== INSTRUÇÕES ===
Use linguagem técnica PCDF.
"""
```

**Testar:**
```python
pergunta = "Há mais Taurus ou Rossi apreendidas?"
resposta = agente.invoke({"input": pergunta})
print(resposta["output"])
```

**Saída esperada:**
```
PASSO 1 - ANÁLISE:
Preciso comparar duas marcas com tipo Apreensão

PASSO 2 - BUSCA:
Tool: contar_armas_combinado
Parâmetros: marca="Taurus", tipo="Apreensão"
           marca="Rossi", tipo="Apreensão"

PASSO 3 - RESULTADO:
Taurus + Apreensão: 342
Rossi + Apreensão: 198

PASSO 4 - RESPOSTA:
Há 144 armas Taurus a mais que Rossi apreendidas.
Fonte: SINARM OCORRENCIAS_2026.csv
```

**Checkpoint:**
```
✅ CHECKPOINT 9: COT MOSTRA RACIOCÍNIO?

Resposta tem 4 passos? ✅
Mostra qual tool usou? ✅
Mostra números intermediários? ✅
```

---

#### **17:50-18:00 | Adicionar Validação (10 min)**

**Objetivo:** Proteger contra SQL injection

**Adicionar função validação:**

```python
# agente_v2_0.py (VERSÃO FINAL COMPLETA)

def validar_input(texto: str):
    """Valida input do usuário contra ataques"""
    
    # Validação 1: Tamanho
    if len(texto) > 500:
        raise ValueError("Query muito longa (máx 500 chars)")
    
    # Validação 2: Caracteres perigosos
    caracteres_perigosos = [";", "--", "DROP", "DELETE", "INSERT", "UPDATE"]
    for char in caracteres_perigosos:
        if char.lower() in texto.lower():
            raise ValueError(f"Caractere perigoso detectado: {char}")
    
    return True

# Wrapper seguro
def perguntar_agente_seguro(pergunta: str):
    """Pergunta ao agente com validação"""
    try:
        validar_input(pergunta)
        resposta = agente.invoke({"input": pergunta})
        return resposta["output"]
    except ValueError as e:
        return f"❌ ERRO DE SEGURANÇA: {e}"
    except Exception as e:
        return f"❌ ERRO: {e}"

# Testar com SQL injection
print("\n" + "="*60)
print("TESTE DE SEGURANÇA")
print("="*60)

# Teste 1: Normal
print("\n1. Pergunta normal:")
print(perguntar_agente_seguro("Quantas Taurus?"))

# Teste 2: SQL Injection
print("\n2. SQL Injection:")
print(perguntar_agente_seguro("marca:Taurus'; DROP TABLE--"))

# Teste 3: Query muito longa
print("\n3. Query longa:")
print(perguntar_agente_seguro("A" * 600))
```

**Checkpoint:**
```
✅ CHECKPOINT 10: VALIDAÇÃO FUNCIONA?

Pergunta normal: passa ✅
SQL injection: bloqueada ✅
Query longa: bloqueada ✅
```

---

#### **18:00 | FINAL - Recap + Celebrar! 🎉**

**Recap Visual:**

```
═══════════════════════════════════════════════════════════
🎉 PARABÉNS! VOCÊS CONSTRUÍRAM UM AGENTE COMPLETO! 🎉
═══════════════════════════════════════════════════════════

O QUE CONSTRUÍMOS HOJE:

✅ Agente funcional do ZERO
✅ Entenderam @decorator profundamente
✅ 4 Tools SINARM (@tool)
✅ Cache para performance (@lru_cache)
✅ Few-Shot (3 exemplos PCDF)
✅ Chain-of-Thought (4 passos)
✅ Validação de segurança

TOTAL: ~150 linhas de código
RESULTADO: agente_v2_0_completo.py ✅

═══════════════════════════════════════════════════════════
PRÓXIMO ENCONTRO: E4 (04/08)
- Refatorar para LangChain
- Adicionar Memory
- Comparar com CrewAI
═══════════════════════════════════════════════════════════
```

**Checkpoint Final:**
```
✅ CHECKPOINT FINAL: TUDO FUNCIONA?

□ Agente responde perguntas? ✅
□ Usa 4 tools? ✅
□ Cache acelera? ✅
□ Few-Shot melhora respostas? ✅
□ CoT mostra raciocínio? ✅
□ Validação bloqueia ataques? ✅

SE TODOS ✅: PARABÉNS! AGENTE COMPLETO! 🎉
```

**Encerramento:**
- "Salvem o código!"
- "Testem em casa!"
- "Próxima aula: E4 (LangChain + Memory)"
- "Dúvidas? Consultem FAQ_E3.md"

---

## 📊 RESUMO PARA PROFESSOR

### **Material usado:**
- ✅ GUIA_DECORATOR_DETALHADO.md (Parte 3)
- ✅ SLIDES_DECORATOR_VISUAL.md (Parte 3)
- ✅ EXEMPLOS_DECORATOR.py (Parte 3)
- ✅ TEMPLATE_HORA_5.py (referência código final)

### **Checkpoints alcançados:**
1. ✅ LLM respondeu (13:45)
2. ✅ Função Python criada (15:00)
3. ✅ Agente chamou função (15:00)
4. ✅ Entendeu decorator (16:00)
5. ✅ @tool funciona (16:35)
6. ✅ 4 tools funcionam (16:55)
7. ✅ Cache funciona (17:15)
8. ✅ Few-Shot melhora (17:40)
9. ✅ CoT mostra raciocínio (17:50)
10. ✅ Validação bloqueia ataques (18:00)

### **Tempo real vs planejado:**
- Planejado: 5h (4h trabalho + 1h pausas)
- Crítico: Parte 3 (decorators) - garantir 45 min completos
- Flexível: Parte 5 pode ser reduzida se necessário

### **Se ficar atrasado:**
- Prioridade 1: Parte 3 (decorators) - NÃO pular
- Prioridade 2: Parte 4 (4 tools + cache)
- Pode reduzir: Parte 5 (deixar Few-Shot/CoT como exercício casa)

---

**Arquivo:** ROTEIRO_COMPLETO_E3.md  
**Localização:** E3_CONSTRUCAO_DO_ZERO/  
**Data:** 16/07/2026  
**Status:** ✅ PRONTO PARA AULA

**Boa aula! Construam juntos! 🚀**
