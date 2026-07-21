# 🔧 PARTE 2: PRIMEIRA TOOL

**Horário:** 14:00-15:00 (60 minutos)  
**Objetivo:** Criar função Python e conectar ao LLM (sem decorator ainda)  
**Nível:** Intermediário

---

## ⚠️ IMPORTANTE: LangChain 1.3+ 

**ATENÇÃO:** Este guia foi atualizado para LangChain 1.3+

**O que mudou:**
- ❌ `initialize_agent` não existe mais
- ❌ `AgentType` não existe mais  
- ✅ Construímos agente **manualmente** (melhor para aprender!)

**Se você viu código antigo (E2):** Não funciona mais! Use este guia atualizado.

**Ver detalhes:** [MUDANCAS_LANGCHAIN_1_3.md](../04_MATERIAL_APOIO/MUDANCAS_LANGCHAIN_1_3.md)

---

## 🎯 O QUE VOCÊ VAI FAZER

1. Criar função Python que consulta dados SINARM
2. Testar função isoladamente
3. Transformar função em Tool (manualmente)
4. Criar agente que usa a Tool
5. Ver agente raciocinar e chamar sua função

---

## ✅ PRÉ-REQUISITOS

- [ ] Parte 1 concluída (LLM funcionando)
- [ ] Arquivo CSV: `DADOS_SINARM/OCORRENCIAS_2026.csv`
- [ ] Biblioteca pandas instalada

---

## 📋 PASSO A PASSO

### PASSO 1: Preparar Dados (5 min)

Crie pasta para dados:

```bash
mkdir DADOS_SINARM
```

Copie arquivo `OCORRENCIAS_2026.csv` para dentro dessa pasta.

**Verificar arquivo:**
```bash
ls DADOS_SINARM/
# Deve listar: OCORRENCIAS_2026.csv
```

---

### PASSO 2: Criar Função Python Simples (15 min)

Crie arquivo: `tools_basicas.py`

Digite **acompanhando o professor**:

```python
# tools_basicas.py
# Funções para consultar SINARM

import pandas as pd

def contar_armas_marca(marca: str):
    """Conta quantas armas de uma marca específica"""
    
    # PASSO 1: Carregar CSV
    print(f"🔍 Buscando armas da marca: {marca}")
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", 
                     sep=";", 
                     encoding="latin1")
    
    # PASSO 2: Filtrar por marca
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    
    # PASSO 3: Contar linhas
    total = len(resultado)
    
    # PASSO 4: Retornar texto
    return f"Encontrei {total} armas da marca {marca}"

# Fim da função
```

---

### PASSO 3: Testar Função Isolada (10 min)

Adicione no final de `tools_basicas.py`:

```python
# Teste da função
if __name__ == "__main__":
    print("="*60)
    print("TESTANDO FUNÇÃO")
    print("="*60)
    
    # Teste 1: Taurus
    resultado = contar_armas_marca("Taurus")
    print(f"✅ {resultado}")
    
    # Teste 2: Glock
    resultado = contar_armas_marca("Glock")
    print(f"✅ {resultado}")
    
    print("="*60)
```

**Executar:**
```bash
python tools_basicas.py
```

**Resultado esperado:**
```
============================================================
TESTANDO FUNÇÃO
============================================================
🔍 Buscando armas da marca: Taurus
✅ Encontrei 0 armas da marca Taurus  ← ⚠️ PROBLEMA!
🔍 Buscando armas da marca: Glock
✅ Encontrei 0 armas da marca Glock   ← ⚠️ PROBLEMA!
============================================================
```

**⚠️ ATENÇÃO:** Se retornou **0 armas**, NÃO SE PREOCUPE! Este é um problema PROPOSITAL para aprendermos algo importante!

---

## 🔍 INVESTIGAÇÃO: POR QUE RETORNA 0? (15 min)

### O Problema

Nossa função retorna **0 armas** mesmo sabendo que Taurus e Glock existem no CSV!

**Por quê?** Vamos investigar como verdadeiros cientistas de dados! 🔬

---

### PASSO 3.1: Analisar os Dados (8 min)

Crie arquivo: `analisar_dados.py`

```python
# analisar_dados.py
# Script para entender o CSV

import pandas as pd

# Carregar primeiras 100 linhas para análise rápida
df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                 sep=";", encoding="latin1", nrows=100)

print("="*60)
print("ANÁLISE DO CSV")
print("="*60)

# 1. Ver primeiras linhas
print("\n1. PRIMEIRAS 3 LINHAS:")
print(df.head(3))

# 2. Ver marcas únicas
print("\n2. MARCAS ÚNICAS (primeiras 10):")
marcas = df["MARCA_ARMA"].unique()[:10]
for i, marca in enumerate(marcas, 1):
    # repr() mostra caracteres invisíveis (espaços)
    print(f"{i}. {repr(marca)} (comprimento: {len(marca)} caracteres)")

# 3. Testar diferentes métodos de busca
print("\n3. TESTANDO BUSCA 'TAURUS':")
print(f"   Método 1 (==): {len(df[df['MARCA_ARMA'] == 'TAURUS'])} resultados")
print(f"   Método 2 (contains): {len(df[df['MARCA_ARMA'].str.contains('TAURUS', case=False, na=False)])} resultados")

# 4. Mostrar exemplo de marca encontrada
taurus = df[df["MARCA_ARMA"].str.contains("TAURUS", case=False, na=False)]
if len(taurus) > 0:
    print(f"\n4. EXEMPLO DE MARCA ENCONTRADA:")
    print(f"   {repr(taurus.iloc[0]['MARCA_ARMA'])}")
```

**Execute:**
```bash
python analisar_dados.py
```

**Você vai ver algo assim:**
```
2. MARCAS ÚNICAS (primeiras 10):
1. 'BOITO (E.R. AMANTINO & CIA)                                           ' (comprimento: 70 caracteres)
2. 'TAURUS ARMAS S.A.                                                     ' (comprimento: 70 caracteres)
3. 'GLOCK GMBH (ÁUSTRIA)                                                  ' (comprimento: 70 caracteres)
```

---

### 💡 DESCOBERTA!

Você encontrou **3 problemas**:

1. **Espaços extras**: Todas marcas têm exatamente 70 caracteres (padding com espaços)
2. **Nome completo**: `'TAURUS ARMAS S.A.'` (não apenas "TAURUS")
3. **Comparação exata falha**: `==` busca texto EXATO, não funciona com espaços extras

**É por isso que retorna 0!**

---

### PASSO 3.2: Aprender Técnicas de Limpeza (7 min)

#### Técnica 1: `.str.strip()` - Remover Espaços

```python
# ANTES (70 caracteres com espaços)
marca_suja = "TAURUS ARMAS S.A.                                                     "
print(f"Comprimento: {len(marca_suja)}")  # 70

# DEPOIS (limpa)
marca_limpa = marca_suja.strip()
print(f"Comprimento: {len(marca_limpa)}")  # 17
print(f"Limpa: '{marca_limpa}'")  # 'TAURUS ARMAS S.A.'
```

**`.strip()`** remove espaços do início e fim da string.

---

#### Técnica 2: `.str.contains()` - Busca Parcial

**O que é busca parcial?**

Imagine que você tem uma frase grande e quer saber se uma palavra está DENTRO dela:

```
Frase grande: "TAURUS ARMAS S.A.                    " (70 caracteres)
Palavra pequena: "TAURUS" (6 caracteres)

Pergunta: "TAURUS" está DENTRO de "TAURUS ARMAS S.A. ..."?
Resposta: SIM! ✅ (nos primeiros 6 caracteres)
```

**Comparação visual:**

```
String no CSV: "T A U R U S   A R M A S   S . A . ..."
                ^ ^ ^ ^ ^ ^
                    |
              ENCONTROU "TAURUS" aqui!
```

**Em Python:**

```python
# MÉTODO 1: == (comparação EXATA) ❌
# Compara TUDO, caractere por caractere
texto_csv = "TAURUS ARMAS S.A.                    "  # 70 chars
busca = "TAURUS"  # 6 chars
texto_csv == busca  # False - tamanhos diferentes!

# MÉTODO 2: in (busca PARCIAL) ✅
# Verifica se "TAURUS" existe EM QUALQUER LUGAR
busca in texto_csv  # True - encontrou!

# MÉTODO 3: .contains() (busca PARCIAL em DataFrame) ✅
# Igual ao 'in', mas funciona com pandas
df[df["MARCA_ARMA"].str.contains("TAURUS", case=False)]  # ✅ Encontra!
```

**Por que funciona?**

`.contains()` procura a palavra **EM QUALQUER POSIÇÃO** da string:

```
"TAURUS ARMAS S.A."  ← "TAURUS" está aqui (posição 0) ✅
"ARMAS TAURUS S.A."  ← "TAURUS" está aqui (posição 6) ✅
"S.A. TAURUS ARMAS"  ← "TAURUS" está aqui (posição 5) ✅
"GLOCK GMBH"         ← "TAURUS" NÃO está aqui ❌
```

**Analogia do dia a dia:**

- **`==`** é como perguntar: "Você é **exatamente** João Silva Santos?"
  - Só responde sim se o nome for IDÊNTICO
  
- **`.contains()`** é como perguntar: "Seu nome **tem** 'João'?"
  - Responde sim para "João Silva", "Maria João", "João Pedro", etc.

**Parâmetros importantes:**

```python
.str.contains("TAURUS", case=False, na=False)
```

- `case=False` → Ignora maiúsculas/minúsculas
  - "taurus" = "TAURUS" = "Taurus" (todos iguais)
  
- `na=False` → Ignora valores nulos (None, NaN)
  - Se encontrar linha vazia, não quebra o código

---

#### Técnica 3: Combinar `.strip()` + `.contains()`

```python
# MELHOR SOLUÇÃO: Combinar as duas técnicas
df[
    df["MARCA_ARMA"]
    .str.strip()          # 1. Remove espaços
    .str.contains("TAURUS", case=False, na=False)  # 2. Busca parcial
]
```

---

### PASSO 3.3: Refatorar Código (5 min)

Agora vamos **corrigir** nossa função!

Abra `tools_basicas.py` e **modifique**:

```python
# tools_basicas.py (VERSÃO CORRIGIDA)

import pandas as pd

def contar_armas_marca(marca: str):
    """Conta quantas armas de uma marca específica"""
    
    # PASSO 1: Carregar CSV
    print(f"Buscando armas da marca: {marca}")
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", 
                     sep=";", 
                     encoding="latin1")
    
    # PASSO 2: Filtrar por marca (CORRIGIDO!)
    # ANTES (não funcionava):
    # resultado = df[df["MARCA_ARMA"] == marca.upper()]
    
    # DEPOIS (funciona!):
    resultado = df[
        df["MARCA_ARMA"]
        .str.strip()                           # Remove espaços extras
        .str.contains(marca, case=False, na=False)  # Busca parcial
    ]
    
    # PASSO 3: Contar linhas
    total = len(resultado)
    
    # PASSO 4: Retornar texto (melhorado)
    if total > 0:
        # Mostrar nome completo encontrado
        marca_completa = resultado.iloc[0]["MARCA_ARMA"].strip()
        return f"Encontrei {total} armas da marca '{marca_completa}'"
    else:
        return f"Nenhuma arma encontrada para '{marca}'"

# Teste
if __name__ == "__main__":
    print("="*60)
    print("TESTANDO FUNÇÃO (CORRIGIDA)")
    print("="*60)
    
    resultado = contar_armas_marca("Taurus")
    print(f"[OK] {resultado}")
    
    resultado = contar_armas_marca("Glock")
    print(f"[OK] {resultado}")
    
    print("="*60)
```

**Execute novamente:**
```bash
python tools_basicas.py
```

**Agora sim! Resultado correto:**
```
============================================================
TESTANDO FUNÇÃO (CORRIGIDA)
============================================================
Buscando armas da marca: Taurus
[OK] Encontrei 42 armas da marca 'TAURUS ARMAS S.A.'
Buscando armas da marca: Glock
[OK] Encontrei 8 armas da marca 'GLOCK GMBH (ÁUSTRIA)'
============================================================
```

**🎉 FUNCIONA!**

---

## 📚 O QUE VOCÊ APRENDEU

### Conceitos de Ciência de Dados:

✅ **Dados reais são sujos**
- CSVs do mundo real têm problemas (espaços, encodings, etc)
- Sempre inspecione seus dados ANTES de usar

✅ **Análise Exploratória**
- Ver primeiras linhas: `df.head()`
- Analisar valores únicos: `df["coluna"].unique()`
- Usar `repr()` para ver caracteres invisíveis
- Investigar quando código não funciona

✅ **Técnicas de Limpeza com Pandas**
- `.str.strip()` → Remove espaços extras
- `.str.contains()` → Busca parcial (flexível)
- `case=False` → Ignora maiúsculas/minúsculas
- `na=False` → Ignora valores nulos

✅ **Debugging**
- Criar scripts de análise
- Testar hipóteses
- Refatorar com base em descobertas

---

## ✅ CHECKPOINT 2A (Revisado)

- [ ] Arquivo `tools_basicas.py` criado
- [ ] Descobriu problema dos espaços extras
- [ ] Criou `analisar_dados.py` para investigar
- [ ] Entendeu `.str.strip()` e `.str.contains()`
- [ ] Refatorou função com tratamento correto
- [ ] Teste retorna números corretos (não zero)
- [ ] Função mostra nome completo da marca

**Se todos ✅:** Parabéns! Você acabou de fazer análise exploratória de dados! 🎉

---

### PASSO 4: Entender a Função (10 min)

**Discussão com professor:**

#### Linha: Parâmetro com Type Hint

```python
def contar_armas_marca(marca: str):
```

**O que é `marca: str`?**
- `marca` = nome do parâmetro
- `: str` = type hint (anotação de tipo)
- Informa que marca deve ser string

---

#### Linha: Docstring

```python
"""Conta quantas armas de uma marca específica"""
```

**Para que serve?**
- Documentação da função
- Explica o que função faz
- Será usado depois pelo decorator @tool

---

#### Linha: Pandas read_csv

```python
df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", 
                 sep=";", 
                 encoding="latin1")
```

**Parâmetros:**
- `sep=";"` → CSV brasileiro usa ponto-vírgula
- `encoding="latin1"` → Aceita acentos portugueses

---

#### Linha: Filtro DataFrame

```python
resultado = df[df["MARCA_ARMA"] == marca.upper()]
```

**O que faz:**
1. `df["MARCA_ARMA"]` → Pega coluna MARCA_ARMA
2. `== marca.upper()` → Compara com marca em maiúsculo
3. `df[...]` → Filtra DataFrame (só linhas True)

**Por que `.upper()`?**
- CSV tem marcas em maiúsculo: "TAURUS"
- Usuário pode digitar minúsculo: "taurus"
- `.upper()` padroniza: "taurus" → "TAURUS"

---

### PASSO 5: Criar Tool e Agente (20 min)

Crie arquivo: `agente_v0_1.py`

**IMPORTANTE:** LangChain 1.3+ removeu `initialize_agent`. Construímos **manualmente**!

```python
# agente_v0_1.py
# Agente manual - LangChain 1.3+

from langchain_ollama import OllamaLLM
from langchain_core.tools import Tool  # ← Import mudou!
from tools_basicas import contar_armas_marca
import re

print("="*60)
print("CRIANDO AGENTE MANUAL - LangChain 1.3+")
print("="*60)

# PARTE 1: Criar LLM
print("\n[1/3] Criando LLM...")
llm = OllamaLLM(model="llama3.2:1b", temperature=0)
print("      [OK] LLM criado")

# PARTE 2: Criar Tool
print("\n[2/3] Criando Tool...")
tool_contar = Tool(
    name="contar_armas_marca",
    func=contar_armas_marca,
    description="Conta quantas armas de uma marca específica. Input: nome da marca"
)
print("      [OK] Tool criada")

# PARTE 3: Criar função agente (implementa ReAct manualmente)
print("\n[3/3] Criando agente...")

def agente_simples(pergunta_usuario):
    """
    Implementa ciclo ReAct manualmente:
    THOUGHT → ACTION → OBSERVATION → THOUGHT → ANSWER
    """
    
    # THOUGHT: Analisar pergunta
    print(f"\n[THOUGHT] Processando: '{pergunta_usuario}'")
    
    # Detectar marca na pergunta
    marcas = ["taurus", "glock", "rossi", "beretta", "smith"]
    marca_encontrada = None
    
    for marca in marcas:
        if marca in pergunta_usuario.lower():
            marca_encontrada = marca.capitalize()
            break
    
    if not marca_encontrada:
        return "Não identifiquei a marca. Tente: Taurus, Glock, Rossi..."
    
    # ACTION: Chamar tool
    print(f"[ACTION] Chamando: {tool_contar.name}('{marca_encontrada}')")
    resultado_tool = tool_contar.func(marca_encontrada)
    
    # OBSERVATION: Ver resultado
    print(f"[OBSERVATION] {resultado_tool}")
    
    # THOUGHT + ANSWER: Formatar com LLM
    print(f"[THOUGHT] Formatando resposta...")
    
    # Extrair número do resultado
    numeros = re.findall(r'\d+', resultado_tool)
    total = numeros[0] if numeros else "?"
    
    prompt = f"""Dados do SINARM: {resultado_tool}

Responda APENAS o número e a marca de forma direta.
Exemplo: "Existem 17.760 armas Taurus."

Resposta:"""
    
    resposta_final = llm.invoke(prompt)
    
    return resposta_final

print("      [OK] Agente pronto")

# PARTE 4: Testar
print("\n" + "="*60)
print("TESTANDO AGENTE")
print("="*60)

pergunta = "Quantas armas Taurus existem?"
print(f"\nPERGUNTA: {pergunta}")
print("-"*60)

resposta = agente_simples(pergunta)

print("-"*60)
print(f"\nRESPOSTA FINAL: {resposta}\n")
print("="*60)
```

**O que mudou vs código antigo (E2)?**

| Aspecto | E2 (antigo) | E3 (novo) |
|---------|-------------|-----------|
| **Import Tool** | `langchain.agents` | `langchain_core.tools` |
| **initialize_agent** | ✅ Usava | ❌ Não existe mais |
| **AgentType** | ✅ Usava | ❌ Não existe mais |
| **Agente** | Automático ("mágico") | Manual (explícito) |
| **ReAct** | Oculto | **Visível!** (THOUGHT, ACTION...) |
| **Controle** | Pouco | Total |

**Vantagem pedagógica:** Você VÊ cada passo do ReAct! 👀



---

### PASSO 6: Executar Agente (5 min)

```bash
python agente_v0_1.py
```

**Aguarde... (LLM pode levar 10-30 segundos)**

**Resultado esperado:**

```
============================================================
CRIANDO AGENTE MANUAL - LangChain 1.3+
============================================================

[1/3] Criando LLM...
      [OK] LLM criado

[2/3] Criando Tool...
      [OK] Tool criada

[3/3] Criando agente...
      [OK] Agente pronto

============================================================
TESTANDO AGENTE
============================================================

PERGUNTA: Quantas armas Taurus existem?
------------------------------------------------------------

[THOUGHT] Processando: 'Quantas armas Taurus existem?'
[ACTION] Chamando: contar_armas_marca('Taurus')
Buscando armas da marca: Taurus
[OBSERVATION] Encontrei 17760 armas da marca 'TAURUS ARMAS S.A.'
[THOUGHT] Formatando resposta...
------------------------------------------------------------

RESPOSTA FINAL: 17760 Taurus

============================================================
```

**Analisar:**
- ✅ `[THOUGHT]` → Agente pensou (ReAct!)
- ✅ `[ACTION]` → Chamou tool (ReAct!)
- ✅ `[OBSERVATION]` → Viu resultado (ReAct!)
- ✅ `[THOUGHT]` → Pensou de novo (ReAct!)
- ✅ Resposta final correta

**Você acabou de ver o ciclo ReAct COMPLETO! 🎉**

ACTION: ContarArmas
ACTION INPUT: "Taurus"

OBSERVATION: Encontrei 17760 armas da marca Taurus

THOUGHT: Agora tenho a resposta

FINAL ANSWER: Há 17.760 armas Taurus registradas no SINARM.

> Finished chain.

✅ RESPOSTA FINAL: Há 17.760 armas Taurus registradas no SINARM.

============================================================
```

---

## ✅ CHECKPOINT 2B

- [ ] Agente executou sem erro
- [ ] Viu o "THOUGHT → ACTION → OBSERVATION"
- [ ] Tool foi chamada (viu "ContarArmas")
- [ ] Resposta final correta (17.760 ou número próximo)

**Se funcionou:** PARABÉNS! Você criou seu primeiro agente! 🎉

---

## 🔍 ENTENDENDO O AGENTE

### 📊 VISÃO GERAL: O Que Acabamos de Construir

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTE COMPLETO                          │
│                                                             │
│  ┌─────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │             │     │              │     │             │ │
│  │     LLM     │ →   │    AGENTE    │ →   │    TOOL     │ │
│  │  (Cérebro)  │     │  (Executor)  │     │  (Ação)     │ │
│  │             │     │              │     │             │ │
│  └─────────────┘     └──────────────┘     └─────────────┘ │
│       ↑                                          ↓         │
│       │                                          │         │
│       └──────────────  FEEDBACK  ────────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘

FLUXO:
1. LLM lê pergunta do usuário
2. AGENTE coordena: "Preciso usar tool?"
3. TOOL executa ação (busca dados)
4. FEEDBACK volta pro LLM
5. LLM formula resposta final
```

---

### 🧩 COMPONENTES DETALHADOS

### Tool Manual

```python
tool_contar = Tool(
    name="ContarArmas",
    func=contar_armas_marca,
    description="..."
)
```

**3 Componentes obrigatórios:**

1. **name**: Como LLM vai chamar
   - LLM vê: "Você tem ferramenta: ContarArmas"
   - LLM decide: "Vou usar ContarArmas"

2. **func**: Função Python que executa
   - AgentExecutor chama: `contar_armas_marca("Taurus")`
   - LLM NÃO executa (só AgentExecutor)

3. **description**: Explicação para o LLM
   - LLM lê para decidir QUANDO usar
   - Quanto mais clara, melhor decisão

---

### AgentType.ZERO_SHOT_REACT_DESCRIPTION

```python
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
```

#### **O QUE É ISSO?**

`AgentType` é uma **classe Enum** (lista de opções pré-definidas) criada pelo LangChain.  
`.ZERO_SHOT_REACT_DESCRIPTION` é uma **constante** dessa classe.

**Analogia:** Como um cardápio de restaurante - você **aponta** a opção em vez de digitar livre.

**De onde vem:**
- Arquivo: `langchain/agents/agent_types.py`
- Definido pelos desenvolvedores do LangChain
- Valor real: `"zero-shot-react-description"` (string)

**Por que usar Enum?**
```python
# OPÇÃO 1: Usar Enum (recomendado - IDE autocompleta)
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION

# OPÇÃO 2: Usar string direto (equivalente, mas propenso a erros)
agent="zero-shot-react-description"  # ← pode errar digitação!
```

✅ **Vantagem:** IDE mostra todas opções disponíveis (não precisa decorar!)

---

#### **ANATOMIA DO NOME:**

```
ZERO_SHOT_REACT_DESCRIPTION
│         │     │
│         │     └─ DESCRIPTION: Usa descrição das tools para decidir
│         │
│         └─ REACT: Padrão ReAct (Reasoning + Acting)
│
└─ ZERO_SHOT: Sem exemplos prévios
```

---

#### **1. ZERO_SHOT (Zero Exemplos)**

**O que significa:**
- Agente decide **sozinho** o que fazer
- **NÃO** recebe exemplos de como agir
- Aprende apenas lendo as descriptions das tools

**Comparação:**

| Tipo | Exemplos Dados | Como Decide |
|------|----------------|-------------|
| **Zero-Shot** | ❌ Nenhum | Lê description e decide |
| **Few-Shot** | ✅ 3-5 exemplos | Imita exemplos dados |
| **One-Shot** | ✅ 1 exemplo | Segue exemplo único |

**Analogia:**
```
Zero-Shot = Dar o manual e deixar descobrir sozinho
Few-Shot  = Mostrar 3 exemplos antes de pedir
```

**Exemplo prático:**
```python
# ZERO-SHOT: Só recebe as tools
agente = initialize_agent(
    tools=[tool_contar],  # ← SÓ isso
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Agente lê description e decide quando usar
agente.invoke({"input": "Quantas armas Taurus?"})
# → Pensa: "Preciso de dados... vou usar tool_contar!"
```

---

#### **2. REACT (Reasoning + Acting)**

**O que significa:**
- Padrão de raciocínio criado em 2022 (Paper: "ReAct: Synergizing Reasoning and Acting in Language Models")
- Alterna entre **PENSAR** e **AGIR**

**Ciclo ReAct:**
```
1. THOUGHT (Pensamento)  → "O que preciso fazer?"
2. ACTION (Ação)         → "Vou chamar esta tool"
3. OBSERVATION (Resultado) → "A tool retornou X"
4. THOUGHT (Novo pensamento) → "Com isso, posso responder..."
5. FINAL ANSWER (Resposta) → "A resposta é Y"
```

**Exemplo REAL de output (verbose=True):**
```
> Entering new AgentExecutor chain...

THOUGHT: Preciso descobrir quantas armas Taurus existem.
         Vou usar a ferramenta de contagem.

ACTION: contar_armas_marca
ACTION INPUT: "Taurus"

OBSERVATION: Encontrei 17760 armas da marca TAURUS ARMAS S.A.

THOUGHT: Agora sei a resposta!

FINAL ANSWER: Existem 17.760 armas Taurus registradas no SINARM.

> Finished chain.
```

**Por que "ReAct" e não só "Act"?**
- LLM pode **raciocinar antes** de agir (mais inteligente)
- Evita chamar tool errada (pensa primeiro)
- Pode encadear múltiplas actions se necessário

**Comparação:**

| Padrão | Como Funciona |
|--------|---------------|
| **ReAct** | PENSAR → AGIR → VER RESULTADO → PENSAR → RESPONDER |
| **Act** | AGIR → VER RESULTADO → RESPONDER (sem raciocínio explícito) |

---

#### **3. DESCRIPTION (Baseado em Descrição)**

**O que significa:**
- Agente **lê a `description`** de cada tool
- Decide qual usar baseado nessa leitura
- **NÃO** usa exemplos ou histórico

**Como funciona:**

```python
# Tool com DESCRIPTION detalhada
Tool(
    name="contar_armas_marca",
    func=contar_armas_marca,
    description="""Conta quantas armas de uma marca específica estão 
    registradas no SINARM. 
    
    Input: Nome da marca (ex: 'Taurus')
    Output: Total de armas encontradas
    
    Use quando usuário perguntar sobre QUANTIDADE de armas."""
)
```

**Agente lê e pensa:**
```
Pergunta: "Quantas armas Taurus existem?"

THOUGHT: Preciso contar armas de uma marca.
         Tenho estas tools disponíveis:
         
         1. contar_armas_marca: "Conta quantas armas..."
            ↑ ISSO! Fala de QUANTIDADE e MARCA!
         
         2. buscar_por_calibre: "Busca por calibre..."
            ↑ Não serve, fala de calibre, não marca
         
         DECISÃO: Vou usar contar_armas_marca!
```

**Description ruim = Agente confuso:**
```python
# ❌ RUIM
description="Conta armas"
# → Agente: "Contar o quê? Quando usar?"

# ✅ BOM
description="""Conta quantas armas de uma marca específica.
Use quando usuário perguntar sobre QUANTIDADE + MARCA."""
# → Agente: "Ah! Quantidade + Marca = usar esta tool"
```

---

#### **JUNTANDO TUDO:**

```python
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
```

**Tradução completa:**

> "Crie um agente que:
> - **ZERO_SHOT**: Decide sozinho (sem exemplos prévios)
> - **REACT**: Usa ciclo Pensamento → Ação → Observação
> - **DESCRIPTION**: Escolhe tools lendo suas descriptions"

---

#### **FLUXO COMPLETO DE EXECUÇÃO:**

```
USUÁRIO
   ↓
   "Quantas armas Taurus?"
   ↓
AGENTE (ZERO_SHOT)
   ↓
THOUGHT (REACT - passo 1)
   "Preciso contar armas de uma marca"
   ↓
   LÊ DESCRIPTIONS (DESCRIPTION)
   ↓
   "tool_contar fala de QUANTIDADE + MARCA"
   ↓
ACTION (REACT - passo 2)
   "Vou chamar contar_armas_marca('Taurus')"
   ↓
TOOL EXECUTA
   "Encontrei 17760 armas"
   ↓
OBSERVATION (REACT - passo 3)
   "Recebi: 17760 armas"
   ↓
THOUGHT (REACT - passo 4)
   "Tenho a resposta!"
   ↓
FINAL ANSWER (REACT - passo 5)
   "Existem 17.760 armas Taurus"
   ↓
USUÁRIO RECEBE RESPOSTA
```

---

#### **OUTROS TIPOS DE AGENTE (Comparação):**

```python
# 1. ZERO_SHOT_REACT_DESCRIPTION (o que usamos)
AgentType.ZERO_SHOT_REACT_DESCRIPTION
# → Decide sozinho, ciclo ReAct, usa descriptions

# 2. CONVERSATIONAL_REACT_DESCRIPTION
AgentType.CONVERSATIONAL_REACT_DESCRIPTION
# → Igual acima + MEMÓRIA de conversas anteriores

# 3. CHAT_ZERO_SHOT_REACT_DESCRIPTION
AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION
# → Otimizado para modelos de chat (ex: GPT-4)

# 4. OPENAI_FUNCTIONS
AgentType.OPENAI_FUNCTIONS
# → Usa Function Calling da OpenAI (mais eficiente)
```

**Por que escolhemos ZERO_SHOT_REACT_DESCRIPTION?**
- ✅ Simples (não precisa exemplos)
- ✅ Transparente (verbose mostra raciocínio)
- ✅ Funciona com qualquer LLM
- ✅ Ideal para aprendizado

---

#### **IMPORTANTE: LangChain 0.2+ Mudou!**

```python
# ❌ LangChain 0.1 (antiga - E2)
from langchain.agents import AgentType, initialize_agent

agente = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    # ...
)

# ✅ LangChain 0.2+ (nova - E3)
from langchain.agents import create_react_agent

# AgentType NÃO EXISTE MAIS!
# Agora construímos manualmente (mais controle)
agente = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt  # ← Customizamos tudo!
)
```

**Por que mudou?**
- Mais flexível (você controla prompt)
- Menos "mágico" (mais explícito)
- Preparar para LangGraph (futuro)

**Nesta aula (E3):**
- Construímos agente **manualmente** (sem AgentType)
- Entendemos **como funciona por baixo**
- Mais controle, mais aprendizado!

---

#### **📚 PARA SABER MAIS:**

**Paper original ReAct:**
- Yao et al. (2022) - "ReAct: Synergizing Reasoning and Acting in Language Models"
- https://arxiv.org/abs/2210.03629

**Ver todas opções AgentType:**
```python
from langchain.agents import AgentType

# Listar TODOS os tipos disponíveis
for tipo in AgentType:
    print(f"{tipo.name:45} = '{tipo.value}'")
```

**Guia completo:**
- Ver: `04_MATERIAL_APOIO/GUIA_AGENTTYPE_EXPLICADO.md`
- Executar: `python 04_MATERIAL_APOIO/exemplo_enum_agenttype.py`

---

### verbose=True

```python
verbose=True
```

**Por que usar:**
- Mostra raciocínio completo do agente
- Vê THOUGHT, ACTION, OBSERVATION
- Essencial para aprender e debugar

**Em produção:** `verbose=False` (não mostra passos)

---

### temperature=0

```python
llm = OllamaLLM(model="llama3", temperature=0)
```

**Por que 0:**
- Respostas determinísticas (sempre iguais)
- Menos criativo, mais factual
- Ideal para consultas técnicas

---

## 🧪 EXPERIMENTO: VENDO REACT EM AÇÃO

### **Teste Prático: Ver THOUGHT → ACTION → OBSERVATION**

Crie arquivo: `experimento_react.py`

```python
"""
Experimento para VISUALIZAR o ciclo ReAct
"""

from langchain_ollama import OllamaLLM
from langchain.agents import Tool, initialize_agent, AgentType
from tools_basicas import contar_armas_marca

print("="*70)
print("EXPERIMENTO: VISUALIZANDO REACT")
print("="*70)

# 1. Criar LLM
llm = OllamaLLM(model="llama3", temperature=0)

# 2. Criar Tool
tool = Tool(
    name="contar_armas_marca",
    func=contar_armas_marca,
    description="Conta quantas armas de uma marca específica. Input: marca"
)

# 3. Criar Agente (ZERO_SHOT_REACT_DESCRIPTION)
agente = initialize_agent(
    tools=[tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  # ← IMPORTANTE: Mostra raciocínio!
    max_iterations=3
)

# 4. Fazer pergunta
print("\nPERGUNTA: Quantas armas Taurus existem?")
print("-"*70)

resposta = agente.invoke({"input": "Quantas armas Taurus existem?"})

print("-"*70)
print(f"\nRESPOSTA FINAL: {resposta['output']}")

print("\n" + "="*70)
print("ANALISE O OUTPUT ACIMA:")
print("="*70)
print("""
Você deve ver:

1. THOUGHT: "Preciso descobrir quantas armas..."
   └─ ZERO_SHOT em ação: agente pensando sozinho

2. ACTION: contar_armas_marca
   └─ REACT em ação: decidiu AGIR

3. ACTION INPUT: "Taurus"
   └─ DESCRIPTION em ação: entendeu que precisa do nome da marca

4. OBSERVATION: "Encontrei 17760 armas..."
   └─ REACT em ação: viu resultado da action

5. THOUGHT: "Tenho a resposta!"
   └─ REACT em ação: pensou novamente

6. FINAL ANSWER: "Existem 17.760 armas..."
   └─ Resposta final ao usuário

ISSO É O CICLO ReAct COMPLETO! 
""")
```

**Execute:**
```bash
python experimento_react.py
```

**O que observar:**
1. **THOUGHT** aparece 2+ vezes (raciocínio antes e depois)
2. **ACTION** chama a tool
3. **OBSERVATION** mostra retorno da tool
4. **FINAL ANSWER** responde ao usuário

---

### **Comparação: Com vs Sem ReAct**

#### **SEM ReAct (LLM sozinho):**
```
USUÁRIO: "Quantas armas Taurus?"
   ↓
LLM: "Hmm... não tenho acesso a dados... vou chutar..."
   ↓
RESPOSTA: "Provavelmente milhares" ← CHUTE!
```

#### **COM ReAct (ZERO_SHOT_REACT_DESCRIPTION):**
```
USUÁRIO: "Quantas armas Taurus?"
   ↓
THOUGHT: "Não sei, preciso consultar dados"
   ↓
ACTION: Chama contar_armas_marca("Taurus")
   ↓
OBSERVATION: "17760 armas"
   ↓
THOUGHT: "Agora sei!"
   ↓
RESPOSTA: "Existem 17.760 armas Taurus" ← PRECISO!
```

---

### **Desafio: Quebrar o Ciclo ReAct**

**Teste 1: Description vaga**
```python
# Description RUIM
tool = Tool(
    name="contar",
    func=contar_armas_marca,
    description="Conta coisas"  # ← VAGO!
)
```

**Resultado:**
- Agente NÃO usa a tool
- Responde "chute" direto
- DESCRIPTION falhou!

---

**Teste 2: Sem verbose**
```python
agente = initialize_agent(
    verbose=False  # ← Não mostra raciocínio
)
```

**Resultado:**
- ReAct AINDA acontece (internamente)
- Mas você NÃO VÊ os passos
- Parece "mágica"

---

**Teste 3: Temperature alta**
```python
llm = OllamaLLM(model="llama3", temperature=0.9)  # ← Muito criativo
```

**Resultado:**
- THOUGHT pode divagar
- Pode não usar tool
- ZERO_SHOT funciona mal com temperatura alta

---

## 🎓 EXERCÍCIO

Modifique `agente_v0_1.py` para fazer 3 perguntas:

```python
perguntas = [
    "Quantas armas Taurus existem?",
    "Quantas armas Glock existem?",
    "Quantas armas Rossi existem?"
]

for pergunta in perguntas:
    print(f"\n{'='*60}")
    print(f"❓ PERGUNTA: {pergunta}")
    print('='*60)
    
    resposta = agente.invoke({"input": pergunta})
    print(f"\n✅ RESPOSTA: {resposta['output']}\n")
```

---

## ⚠️ PROBLEMAS COMUNS

### Erro: "FileNotFoundError: OCORRENCIAS_2026.csv"

**Solução:**
- Verificar caminho: `ls DADOS_SINARM/`
- Caminho relativo: executar de dentro da pasta do projeto

---

### Agente não chama Tool (responde direto)

**Causa:** Description vaga

**Solução:** Melhorar description:
```python
description="""Conta quantas armas de uma marca específica estão registradas no SINARM.

Input: Nome da marca (string) - ex: 'Taurus', 'Glock', 'Rossi'
Output: Total numérico de armas encontradas

Use esta ferramenta quando usuário perguntar sobre QUANTIDADE de armas de uma MARCA específica."""
```

---

### Agente demora muito (>60 segundos)

**Causa:** LLM processando + leitura CSV

**Solução temporária:** Usar dataset menor para teste

---

### UnicodeDecodeError

**Causa:** Encoding errado

**Solução:**
```python
df = pd.read_csv("...", encoding="latin1")  # ou "utf-8"
```

---

## 📚 CONCEITOS APRENDIDOS

### ✅ Técnicos

- **Tool**: Wrapper que permite LLM usar função Python  
- **AgentExecutor**: Orquestra LLM + Tools  
- **ReAct**: Padrão Thought → Action → Observation  
- **verbose**: Mostrar raciocínio do agente  
- **temperature**: Controla criatividade (0 = determinístico)  
- **description**: Documentação para LLM decidir quando usar tool

### ✅ Python

- **Enum**: Lista fechada de opções (`AgentType`)
- **Atributo de classe**: Acesso direto sem instância (`.ZERO_SHOT_REACT_DESCRIPTION`)
- **Type hints**: Documentar tipos (`marca: str`)

### ✅ Conceitual

- **Zero-Shot**: Agente decide sem exemplos prévios
- **Reasoning + Acting**: Pensar antes/depois de agir
- **Description-based**: Decisão baseada em leitura de texto

---

## 📖 REFERÊNCIAS COMPLEMENTARES

### **Aprofundar ZERO_SHOT_REACT_DESCRIPTION:**
- 📄 [GUIA_AGENTTYPE_EXPLICADO.md](../04_MATERIAL_APOIO/GUIA_AGENTTYPE_EXPLICADO.md) - Explicação completa (600+ linhas)
- 🐍 [exemplo_enum_agenttype.py](../04_MATERIAL_APOIO/exemplo_enum_agenttype.py) - Demo interativa executável

### **Entender ReAct:**
- 📄 Paper original: "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022)
- 🔗 https://arxiv.org/abs/2210.03629

### **Dúvidas frequentes:**
- ❓ [FAQ_E3.md](../04_MATERIAL_APOIO/FAQ_E3.md) - Q34: O que é AgentType?
- 🔧 [TROUBLESHOOTING_E3.md](../04_MATERIAL_APOIO/TROUBLESHOOTING_E3.md)

### **Código pronto:**
- 📝 [TEMPLATE_HORA_2.py](../02_TEMPLATES_PRONTOS/TEMPLATE_HORA_2.py) - Código completo desta parte

---

## 🎯 RESUMO VISUAL: ZERO_SHOT_REACT_DESCRIPTION

```
╔═══════════════════════════════════════════════════════════╗
║     AgentType.ZERO_SHOT_REACT_DESCRIPTION                 ║
╚═══════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────┐
│ ZERO_SHOT                                               │
│ - Sem exemplos prévios                                  │
│ - Agente decide sozinho                                 │
│ - Aprende lendo descriptions                            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ REACT (Reasoning + Acting)                              │
│                                                         │
│  THOUGHT    →  ACTION    →  OBSERVATION                │
│  (Pensar)      (Agir)       (Ver resultado)            │
│     ↓             ↓              ↓                      │
│  "Preciso      Chamar         "Recebi                  │
│   de dados"    tool           17760"                   │
│                                                         │
│  THOUGHT    →  FINAL ANSWER                            │
│  (Pensar)      (Responder)                             │
│     ↓              ↓                                    │
│  "Agora sei!"   "Existem 17.760..."                    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ DESCRIPTION                                             │
│ - Lê description de cada tool                           │
│ - Decide qual usar baseado na leitura                   │
│ - "Conta armas... marca..." → USAR ESTA!               │
└─────────────────────────────────────────────────────────┘

RESULTADO: Agente inteligente que decide, age e aprende!
```

---

## 🚀 PRÓXIMOS PASSOS

Você criou tool **MANUALMENTE** (chato, muitas linhas).

Na **PARTE 3**, você vai aprender:
- O que são decorators Python
- Como usar `@tool` (automático, 1 linha!)
- Diferença com/sem decorator

**Arquivo:** [PARTE_3_DECORATOR.md](PARTE_3_DECORATOR.md)

---

## 📞 AJUDA

**Travou?**
- [FAQ_E3.md](../04_MATERIAL_APOIO/FAQ_E3.md)
- [TROUBLESHOOTING_E3.md](../04_MATERIAL_APOIO/TROUBLESHOOTING_E3.md)
- [TEMPLATE_HORA_2.py](../02_TEMPLATES_PRONTOS/TEMPLATE_HORA_2.py)

---

**Parte:** 2/5  
**Tempo:** 60 minutos  
**Status:** ✅ PRONTO PARA USO

**Continue construindo! 🔧**
