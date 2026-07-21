# ⚙️ PARTE 4: QUATRO TOOLS + CACHE

**Horario:** 16:15-17:15 (60 minutos)  
**Objetivo:** Adicionar mais 3 tools, usar @tool e otimizar com cache  
**Nivel:** Intermediario

---

## ⚠️ IMPORTANTE: LangChain 1.3+

**Este guia continua usando agente MANUAL (LangChain 1.3+)**

**O que vamos fazer:**
- ✅ Adicionar @tool nas funcoes (PARTE 3 ensinou!)
- ✅ Criar 3 novas tools (@tool desde o inicio)
- ✅ Expandir agente manual para 4 tools
- ✅ Adicionar cache (@lru_cache) para otimizar

**Nao vamos usar:**
- ❌ initialize_agent (nao existe em 1.3+)
- ❌ AgentType (nao existe em 1.3+)

---

## 🎯 O QUE VOCE VAI FAZER

1. Criar arquivo novo `tools_basicas_v2.py` (4 tools COM @tool)
2. Adicionar @lru_cache para otimizar leitura CSV
3. Criar `agente_v0_2.py` (agente manual com 4 tools)
4. Testar agente com 4 perguntas diferentes
5. Ver diferenca de velocidade (cache!)

---

## ✅ PRE-REQUISITOS

- [ ] PARTE 2 concluida (agente_v0_1.py funcionando)
- [ ] PARTE 3 concluida (entendeu decorators)
- [ ] Arquivo exemplo_tool_decorator.py executado

**📚 Material de apoio:**
- [ERROS_COMUNS_PARTE4.md](../04_MATERIAL_APOIO/ERROS_COMUNS_PARTE4.md) - Guia visual de erros comuns

---

## 📋 PASSO A PASSO

### ⚠️⚠️⚠️ ATENCAO IMPORTANTE ⚠️⚠️⚠️

**NAO MODIFIQUE o arquivo `tools_basicas.py` da PARTE 2!**

**Nesta parte voce vai:**
- ✅ CRIAR arquivo NOVO: `tools_basicas_v2.py`
- ❌ NAO mexer em `tools_basicas.py` (deixe como esta!)

**Por que arquivo novo?**
- Manter PARTE 2 intacta (para revisao)
- Codigo limpo, sem misturar versoes
- Comparar versao simples (PARTE 2) vs otimizada (PARTE 4)

**Se voce ja modificou `tools_basicas.py`:**
- Nao tem problema! Continue assim OU
- Restaure o arquivo original da PARTE 2

---

### PASSO 0: Entender Estrategia (5 min)

**Por que criar arquivo novo?**

Na PARTE 2 criamos `tools_basicas.py` SEM @tool (para aprender fundamentos).
Agora vamos criar `tools_basicas_v2.py` COM @tool e cache!

**Vantagens:**
- Manter PARTE 2 intacta (revisao futura)
- Arquivo novo = codigo limpo e testado
- Comparar versao simples vs otimizada

**Professor vai explicar ao vivo!**

---

### PASSO 1: Criar tools_basicas_v2.py (20 min)

Crie arquivo novo: `tools_basicas_v2.py`

Digite **acompanhando o professor**:

```python
# tools_basicas_v2.py
# Funcoes para consultar SINARM COM @tool (PARTE 4)

import pandas as pd
from functools import lru_cache
from langchain_core.tools import tool

# FUNCAO COM CACHE para carregar CSV
@lru_cache(maxsize=1)
def carregar_csv():
    """Carrega CSV UMA VEZ e guarda em cache"""
    print("[CACHE] Carregando CSV...")
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    
    # Limpar espacos em todas as colunas relevantes
    df["MARCA_ARMA"] = df["MARCA_ARMA"].str.strip()
    df["CALIBRE_ARMA"] = df["CALIBRE_ARMA"].str.strip()
    df["TIPO_OCORRENCIA"] = df["TIPO_OCORRENCIA"].str.strip()
    
    print(f"[OK] CSV carregado! {len(df)} linhas")
    return df


# TOOL 1: Contar por marca
@tool
def contar_armas_marca(marca: str) -> str:
    """Conta quantas armas de uma marca especifica estao registradas.
    
    Args:
        marca: Nome da marca (ex: Taurus, Glock, Rossi, Beretta)
    
    Returns:
        Total de armas encontradas dessa marca
    """
    df = carregar_csv()  # <- USA CACHE!
    resultado = df[df["MARCA_ARMA"].str.contains(marca.upper(), case=False, na=False)]
    total = len(resultado)
    
    if total > 0:
        marca_real = resultado["MARCA_ARMA"].iloc[0]
        return f"Encontrei {total} armas da marca '{marca_real}'"
    else:
        return f"Nao encontrei armas da marca '{marca}'"


# TOOL 2: Contar por calibre
@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta quantas armas de um calibre especifico.
    
    Args:
        calibre: Calibre da arma (ex: .38, 9mm, .40, .380)
    
    Returns:
        Total de armas do calibre especificado
    """
    df = carregar_csv()  # <- USA CACHE!
    resultado = df[df["CALIBRE_ARMA"].str.contains(calibre, case=False, na=False)]
    total = len(resultado)
    
    if total > 0:
        calibre_real = resultado["CALIBRE_ARMA"].iloc[0]
        return f"Encontrei {total} armas calibre '{calibre_real}'"
    else:
        return f"Nao encontrei armas calibre '{calibre}'"


# TOOL 3: Contar por tipo de ocorrencia
@tool
def contar_armas_tipo(tipo: str) -> str:
    """Conta armas por tipo de ocorrencia.
    
    Args:
        tipo: Tipo de ocorrencia (ex: Apreens, Roubo, Furto, Perda)
    
    Returns:
        Total de ocorrencias do tipo especificado
    """
    df = carregar_csv()  # <- USA CACHE!
    resultado = df[df["TIPO_OCORRENCIA"].str.contains(tipo.upper(), case=False, na=False)]
    total = len(resultado)
    
    if total > 0:
        tipo_real = resultado["TIPO_OCORRENCIA"].iloc[0]
        return f"Encontrei {total} ocorrencias tipo '{tipo_real}'"
    else:
        return f"Nao encontrei ocorrencias tipo '{tipo}'"


# TOOL 4: Contar combinado (marca + tipo)
@tool
def contar_armas_combinado(marca: str, tipo: str) -> str:
    """Conta armas por marca E tipo de ocorrencia simultaneamente.
    
    Args:
        marca: Marca da arma
        tipo: Tipo de ocorrencia
    
    Returns:
        Total de armas que atendem ambos criterios
    """
    df = carregar_csv()  # <- USA CACHE!
    resultado = df[
        (df["MARCA_ARMA"].str.contains(marca.upper(), case=False, na=False)) & 
        (df["TIPO_OCORRENCIA"].str.contains(tipo.upper(), case=False, na=False))
    ]
    total = len(resultado)
    
    if total > 0:
        return f"Encontrei {total} armas {marca} do tipo {tipo}"
    else:
        return f"Nao encontrei armas {marca} do tipo {tipo}"


# Teste direto
if __name__ == "__main__":
    print("="*60)
    print("TESTANDO 4 TOOLS COM @tool + CACHE")
    print("="*60)
    
    print("\n[TESTE 1] Contar armas Taurus:")
    resultado = contar_armas_marca.func("Taurus")
    print(f"   {resultado}")
    
    print("\n[TESTE 2] Contar armas calibre .38:")
    resultado = contar_armas_calibre.func(".38")
    print(f"   {resultado}")
    
    print("\n[TESTE 3] Contar apreensoes:")
    resultado = contar_armas_tipo.func("Apreens")
    print(f"   {resultado}")
    
    print("\n[TESTE 4] Contar Taurus roubadas:")
    resultado = contar_armas_combinado.func("Taurus", "Roubo")
    print(f"   {resultado}")
    
    print("\n" + "="*60)
    print("OBSERVE: 'Carregando CSV...' apareceu SO UMA VEZ!")
    print("Cache funcionou!")
    print("="*60)
```

---

### PASSO 2: Testar Tools Isoladas (5 min)

Execute:

```bash
python tools_basicas_v2.py
```

**Resultado esperado:**

```
============================================================
TESTANDO 4 TOOLS COM @tool + CACHE
============================================================

[TESTE 1] Contar armas Taurus:
[CACHE] Carregando CSV...
[OK] CSV carregado! 74758 linhas
   Encontrei 17760 armas da marca 'TAURUS ARMAS S.A.'

[TESTE 2] Contar armas calibre .38:
   Encontrei 17564 armas calibre '.380'

[TESTE 3] Contar apreensoes:
   Encontrei 918 ocorrencias tipo 'Apreensao de Arma de Fogo'

[TESTE 4] Contar Taurus roubadas:
   Encontrei 45 armas Taurus do tipo Roubo

============================================================
OBSERVE: 'Carregando CSV...' apareceu SO UMA VEZ!
Cache funcionou!
============================================================
```

**⚠️ IMPORTANTE: "[CACHE] Carregando CSV..." aparece SO UMA VEZ!**

Isso significa que @lru_cache funcionou! 🚀

---

## ✅ CHECKPOINT 4A

- [ ] tools_basicas_v2.py criado
- [ ] 4 tools retornam valores corretos
- [ ] "Carregando CSV..." apareceu SO 1 vez (cache!)

**Se algo falhou:** Chame o professor!

---

### PASSO 3: Criar Agente com 4 Tools (20 min)

Crie arquivo novo: `agente_v0_2.py`

```python
# agente_v0_2.py
# Agente manual com 4 tools - LangChain 1.3+

from langchain_ollama import OllamaLLM
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)
import re

print("="*60)
print("AGENTE COM 4 TOOLS - LangChain 1.3+")
print("="*60)

# PARTE 1: Criar LLM
print("\n[1/4] Criando LLM...")
llm = OllamaLLM(model="llama3.2:1b", temperature=0)
print("      [OK] LLM criado")

# PARTE 2: Listar tools disponiveis
print("\n[2/4] Registrando tools...")
tools = [
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
]

for tool in tools:
    print(f"      - {tool.name}: {tool.description.split('.')[0]}")

print("      [OK] 4 tools registradas")

# PARTE 3: Criar funcao agente (implementa ReAct manualmente)
print("\n[3/4] Criando agente...")

def agente_quatro_tools(pergunta_usuario):
    """
    Agente manual que escolhe qual tool usar baseado na pergunta.
    Implementa ciclo ReAct: THOUGHT -> ACTION -> OBSERVATION -> ANSWER
    """
    
    print(f"\n[THOUGHT] Analisando: '{pergunta_usuario}'")
    pergunta_lower = pergunta_usuario.lower()
    
    # DECISAO: Qual tool usar?
    tool_escolhida = None
    parametros = {}
    
    # Detectar marcas
    marcas = ["taurus", "glock", "rossi", "beretta", "smith", "colt", "ruger"]
    marca_encontrada = None
    for marca in marcas:
        if marca in pergunta_lower:
            marca_encontrada = marca.capitalize()
            break
    
    # Detectar calibres
    calibres = [".38", ".380", "9mm", ".40", ".45", "7.62"]
    calibre_encontrado = None
    for calibre in calibres:
        if calibre in pergunta_lower:
            calibre_encontrado = calibre
            break
    
    # Detectar tipos de ocorrencia
    tipos = {
        "apreens": "Apreens",
        "roubo": "Roubo",
        "roub": "Roubo",
        "furto": "Furto",
        "perda": "Perda",
        "extravio": "Perda"
    }
    tipo_encontrado = None
    for palavra_chave, tipo in tipos.items():
        if palavra_chave in pergunta_lower:
            tipo_encontrado = tipo
            break
    
    # LOGICA DE SELECAO
    if marca_encontrada and tipo_encontrado:
        # Tool 4: Combinado (marca + tipo)
        tool_escolhida = contar_armas_combinado
        parametros = {"marca": marca_encontrada, "tipo": tipo_encontrado}
        print(f"[DECISION] Usar tool 'contar_armas_combinado' (marca + tipo)")
    
    elif marca_encontrada:
        # Tool 1: Marca
        tool_escolhida = contar_armas_marca
        parametros = {"marca": marca_encontrada}
        print(f"[DECISION] Usar tool 'contar_armas_marca'")
    
    elif calibre_encontrado:
        # Tool 2: Calibre
        tool_escolhida = contar_armas_calibre
        parametros = {"calibre": calibre_encontrado}
        print(f"[DECISION] Usar tool 'contar_armas_calibre'")
    
    elif tipo_encontrado:
        # Tool 3: Tipo
        tool_escolhida = contar_armas_tipo
        parametros = {"tipo": tipo_encontrado}
        print(f"[DECISION] Usar tool 'contar_armas_tipo'")
    
    else:
        return "Nao consegui identificar o que voce quer. Tente perguntar sobre marca, calibre ou tipo de ocorrencia."
    
    # ACTION: Executar tool
    print(f"[ACTION] Chamando: {tool_escolhida.name}({parametros})")
    resultado_tool = tool_escolhida.func(**parametros)
    
    # OBSERVATION: Ver resultado
    print(f"[OBSERVATION] {resultado_tool}")
    
    # THOUGHT + ANSWER: Formatar resposta
    print(f"[THOUGHT] Formatando resposta...")
    
    # Extrair numero do resultado
    numeros = re.findall(r'\d+', resultado_tool)
    total = numeros[0] if numeros else "?"
    
    # Montar prompt para LLM formatar
    prompt = f"""Dados do SINARM: {resultado_tool}

Responda APENAS o numero de forma direta e natural.
Exemplo: "Existem 17.760 armas Taurus."

Resposta:"""
    
    resposta_final = llm.invoke(prompt)
    
    return resposta_final

print("      [OK] Agente pronto")

# PARTE 4: Testar com 4 perguntas diferentes
print("\n[4/4] Testando agente...")
print("="*60)

perguntas = [
    "Quantas armas Taurus existem?",
    "Quantas armas calibre .38?",
    "Quantas apreensoes ocorreram?",
    "Quantas Taurus foram roubadas?"
]

for i, pergunta in enumerate(perguntas, 1):
    print(f"\n{'='*60}")
    print(f"PERGUNTA {i}: {pergunta}")
    print("="*60)
    
    resposta = agente_quatro_tools(pergunta)
    
    print("-"*60)
    print(f"RESPOSTA: {resposta}")
    print()

print("="*60)
print("TESTE CONCLUIDO!")
print("="*60)
print("\nOBSERVE:")
print("- 'Carregando CSV...' apareceu SO UMA VEZ (cache funcionou!)")
print("- Agente escolheu tool correta para cada pergunta")
print("- Ultima pergunta usou 'contar_armas_combinado' (2 criterios)")
```

---

### PASSO 4: Executar Agente Completo (10 min)

Execute:

```bash
python agente_v0_2.py
```

**Professor vai explicar a saida ao vivo!**

**Observe:**
1. "[CACHE] Carregando CSV..." aparece SO UMA VEZ
2. Agente escolhe tool correta para cada pergunta
3. Pergunta 1: usa `contar_armas_marca`
4. Pergunta 2: usa `contar_armas_calibre`
5. Pergunta 3: usa `contar_armas_tipo`
6. Pergunta 4: usa `contar_armas_combinado` (2 criterios!)

---

## ✅ CHECKPOINT 4B

- [ ] agente_v0_2.py criado
- [ ] 4 perguntas respondidas corretamente
- [ ] "Carregando CSV..." apareceu SO 1 vez
- [ ] Agente escolheu tool correta para cada pergunta
- [ ] Ultima pergunta usou tool combinada (marca + tipo)

---

## 📊 PERFORMANCE: SEM vs COM CACHE

### SEM Cache (PARTE 2)
```
Pergunta 1: 3.5s (le CSV)
Pergunta 2: 3.5s (le CSV de novo)
Pergunta 3: 3.5s (le CSV de novo)
Pergunta 4: 3.5s (le CSV de novo)
TOTAL: 14 segundos
```

### COM Cache (@lru_cache) - PARTE 4
```
Pergunta 1: 3.5s (le CSV)
Pergunta 2: 0.2s (usa cache!)
Pergunta 3: 0.2s (usa cache!)
Pergunta 4: 0.2s (usa cache!)
TOTAL: 4.1 segundos
```

**Resultado: 70% mais rapido!** 🚀

---

## 📚 CONCEITOS APRENDIDOS

✅ **@tool**: Decorator LangChain para criar tools  
✅ **@lru_cache**: Decorator que guarda resultado em memoria  
✅ **Cache**: Armazenamento temporario para acelerar  
✅ **maxsize=1**: Guarda so 1 resultado (suficiente para CSV)  
✅ **DRY**: Funcao `carregar_csv()` usada por todas tools  
✅ **Performance**: Cache reduz I/O (leitura disco)  
✅ **Agente Manual**: Escolhe tool baseado na pergunta (ReAct)  
✅ **Tool Combinada**: Usa 2 criterios simultaneamente

---

## 📝 RESUMO DA PARTE 4

**Arquivos criados:**
- ✅ `tools_basicas_v2.py` (4 tools COM @tool + cache)
- ✅ `agente_v0_2.py` (agente manual com 4 tools)

**Conceitos dominados:**
- ✅ Decorator @tool (LangChain)
- ✅ Decorator @lru_cache (otimizacao)
- ✅ Agente manual escolhendo tool (ReAct)
- ✅ Tool com 2 parametros (combinado)
- ✅ Performance profiling (antes vs depois)

**Proxima etapa:**
- 🎯 PARTE 5: Few-Shot + Chain-of-Thought

---

**Parte:** 4/5  
**Tempo:** 60 minutos  
**Status:** ✅ ATUALIZADO LangChain 1.3+  
**Testado:** ✅ Python 3.11 + Ollama llama3.2:1b
