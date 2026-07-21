# ❓ FAQ E3 - PERGUNTAS FREQUENTES

**Encontro 3:** Construção do Agente do Zero  
**Atualizado:** 20/07/2026

---

## 📑 ÍNDICE

1. [Ambiente e Setup](#ambiente-e-setup)
2. [LLM e Ollama](#llm-e-ollama)
3. [Pandas e Dados](#pandas-e-dados)
4. [Tools e Agentes](#tools-e-agentes)
5. [Decorators](#decorators)
6. [Cache](#cache)
7. [Performance](#performance)
8. [Erros Comuns](#erros-comuns)
9. [Conceitos Python](#conceitos-python)

---

## AMBIENTE E SETUP

### Q1: Qual versão do Python preciso?

**A:** Python 3.9 ou superior.

Verificar:
```bash
python --version
```

### Q2: Como instalar dependências?

**A:**
```bash
pip install langchain-ollama langchain pandas
```

### Q3: Preciso de GPU?

**A:** Não obrigatório, mas recomendado.
- **CPU**: 1-5 tokens/s (funciona, mas lento)
- **GPU**: 20-100 tokens/s (rápido)

---

## LLM E OLLAMA

### Q4: Como instalar Ollama?

**A:** Download em [https://ollama.ai/download](https://ollama.ai/download)

Após instalar:
```bash
ollama pull llama3
ollama serve
```

### Q5: Ollama serve falha com "porta em uso"

**A:** Ollama já está rodando ou porta 11434 ocupada.

Verificar:
```bash
# Windows
netstat -ano | findstr :11434

# Mac/Linux
lsof -i :11434
```

Matar processo ou usar outra porta.

### Q6: LLM demora muito (>30s)

**A:** Normal em CPU. Soluções:
- Usar modelo menor: `model="llama3.2:1b"` (muito mais rápido!)
- Fechar outros programas
- Reduzir contexto (perguntas mais curtas)

Ver: `GUIA_ESCOLHA_MODELO_LLM.md`

### Q6.1: Erro "out of memory" ao carregar llama3

**A:** RAM insuficiente. Solução:

```bash
# 1. Baixar modelo menor
ollama pull llama3.2:1b

# 2. Usar no código
llm = OllamaLLM(model="llama3.2:1b", temperature=0)
```

**Diferença:**
- llama3 (8B): 4.7GB, alta qualidade
- llama3.2:1b (1B): 1.3GB, boa qualidade

**Impacto:** Modelo menor é 2-4x mais rápido e usa 70% menos RAM.  
Qualidade: suficiente para 90% dos casos.

Ver guia completo: `04_MATERIAL_APOIO/GUIA_ESCOLHA_MODELO_LLM.md`

### Q6.2: Qual modelo usar em produção?

**A:** Depende dos recursos:

| Cenário | Modelo Recomendado | RAM |
|---------|-------------------|-----|
| Laptop/dev | llama3.2:1b | 2-3GB |
| Workstation | llama3 (8B) | 8GB+ |
| Servidor CPU | llama3.2:3b | 4-6GB |
| Servidor GPU | llama3 (70B) | 40GB+ |

**Regra:** Use o maior modelo que seu hardware suporta confortavelmente.

### Q7: Resposta do LLM em inglês

**A:** Adicione instrução explícita:
```python
llm.invoke("Responda em português: sua pergunta")
```

Ou no system_message:
```python
system_message = "Você responde SEMPRE em português..."
```

---

## PANDAS E DADOS

### Q8: FileNotFoundError ao ler CSV

**A:** Verificar:
1. Caminho correto: `DADOS_SINARM/OCORRENCIAS_2026.csv`
2. Executar de dentro da pasta do projeto
3. CSV existe: `ls DADOS_SINARM/`

### Q9: UnicodeDecodeError ao ler CSV

**A:** Encoding errado. Usar:
```python
df = pd.read_csv("arquivo.csv", encoding="latin1")
# ou
df = pd.read_csv("arquivo.csv", encoding="utf-8")
```

### Q10: CSV brasileiro com ponto-vírgula

**A:** Usar `sep=";"`:
```python
df = pd.read_csv("arquivo.csv", sep=";", encoding="latin1")
```

### Q11: Como ver primeiras linhas do DataFrame?

**A:**
```python
print(df.head())  # Primeiras 5
print(df.head(10))  # Primeiras 10
```

### Q12: Como ver colunas do CSV?

**A:**
```python
print(df.columns.tolist())
```

---

## TOOLS E AGENTES

### Q13: Tool não é chamada pelo agente

**Causas possíveis:**
1. Description vaga → melhorar explicação
2. Nome genérico → usar nome descritivo
3. LLM "esquece" → adicionar no prompt

**Solução:**
```python
description="""Conta armas por marca no SINARM.

Input: string marca (ex: 'Taurus')
Output: total numérico

Use SEMPRE que usuário perguntar QUANTIDADE de uma MARCA."""
```

### Q14: Agente entra em loop infinito

**A:** Adicionar `max_iterations`:
```python
agente = initialize_agent(
    ...,
    max_iterations=5  # Máx 5 tentativas
)
```

### Q15: verbose=True não mostra nada

**A:** Verificar:
- Output está sendo capturado?
- Redirecionar: `python script.py 2>&1`

### Q16: Agente responde sem usar tool

**A:** LLM "chuta" resposta. Forçar uso de tool:
```python
system_message = """
REGRA: SEMPRE use tools disponíveis.
NUNCA responda sem consultar ferramentas.
"""
```

---

## DECORATORS

### Q17: O que é @tool exatamente?

**A:** Decorator que transforma função Python em Tool LangChain.

Extrai automaticamente:
- `name` do nome da função
- `description` da docstring
- `args_schema` dos type hints

### Q18: Posso usar @tool em métodos de classe?

**A:** Não diretamente. @tool funciona com funções puras.

**Workaround:**
```python
class MinhaClasse:
    def metodo(self, x):
        return x * 2

# Criar wrapper
@tool
def minha_tool(x: int) -> int:
    """Descrição"""
    obj = MinhaClasse()
    return obj.metodo(x)
```

### Q19: Type hints são obrigatórios com @tool?

**A:** SIM! @tool precisa para criar schema.

```python
# ERRADO
@tool
def funcao(x):  # Sem type hint
    return x

# CERTO
@tool
def funcao(x: int) -> int:  # Com type hints
    return x
```

### Q20: Docstring obrigatória?

**A:** SIM! Vira description para o LLM.

```python
# ERRADO
@tool
def funcao(x: int) -> int:
    return x  # Sem docstring

# CERTO
@tool
def funcao(x: int) -> int:
    """Descrição clara do que faz"""
    return x
```

---

## CACHE

### Q21: Como funciona @lru_cache?

**A:** Guarda resultado na memória (RAM).

Primeira chamada: calcula e guarda
Próximas chamadas: retorna do cache (instantâneo)

### Q22: maxsize=1 é suficiente?

**A:** Depende:
- **Sem parâmetros**: maxsize=1 suficiente
- **Com parâmetros**: maxsize maior (ex: 128)

```python
@lru_cache(maxsize=1)
def carregar_csv():  # Sem params
    return df

@lru_cache(maxsize=128)
def buscar(id):  # Com param (muitos valores)
    return dados[id]
```

### Q23: Cache persiste entre execuções?

**A:** NÃO! @lru_cache é RAM (memória volátil).

Programa fecha → cache apagado
Programa inicia → cache vazio

### Q24: Como limpar cache manualmente?

**A:**
```python
funcao.cache_clear()  # Limpa cache
```

### Q25: Como ver estatísticas do cache?

**A:**
```python
print(funcao.cache_info())
# CacheInfo(hits=5, misses=2, maxsize=128, currsize=2)
```

---

## PERFORMANCE

### Q26: Agente está lento, como otimizar?

**Checklist:**
1. ✅ Usar @lru_cache para I/O
2. ✅ temperature=0 (mais rápido)
3. ✅ Modelo menor (llama3:8b)
4. ✅ Reduzir verbose=False (menos print)
5. ✅ GPU se disponível

### Q27: Ler CSV toda vez é lento

**A:** Usar cache:
```python
@lru_cache(maxsize=1)
def carregar_csv():
    return pd.read_csv(...)
```

### Q28: Agente faz múltiplas chamadas desnecessárias

**A:** Melhorar prompt:
```python
system_message = """
Minimize chamadas a tools.
Reutilize resultados anteriores quando possível.
"""
```

---

## ERROS COMUNS

### Q29: ModuleNotFoundError: langchain_ollama

**A:**
```bash
pip install langchain-ollama
```

### Q30: ImportError: cannot import Tool

**A:**
```python
# ERRADO
from langchain import Tool

# CERTO
from langchain.agents import Tool
```

### Q31: AttributeError: 'str' object has no attribute 'invoke'

**A:** Você está tentando invoke() em string, não LLM.

```python
# ERRADO
llm = "llama3"
llm.invoke(...)

# CERTO
llm = OllamaLLM(model="llama3")
llm.invoke(...)
```

### Q32: KeyError: 'output'

**A:** Agente retorna dicionário. Acessar corretamente:

```python
resposta = agente.invoke({"input": "pergunta"})
print(resposta["output"])  # Não resposta.output
```

### Q33: ValueError: Could not parse LLM output

**A:** LLM não formatou resposta corretamente.

Soluções:
1. temperature=0 (mais determinístico)
2. Melhorar system_message (instruções claras)
3. Usar handle_parsing_errors=True

---

## CONCEITOS PYTHON

### Q34: O que é `AgentType.ZERO_SHOT_REACT_DESCRIPTION`?

**A:** É uma **constante Enum** definida pelo LangChain.

```python
from langchain.agents import AgentType

# AgentType = classe Enum (lista de opções)
# .ZERO_SHOT_REACT_DESCRIPTION = constante

# Valor real: "zero-shot-react-description" (string)
print(AgentType.ZERO_SHOT_REACT_DESCRIPTION)
# Output: zero-shot-react-description
```

**De onde vem?**
- Arquivo: `langchain/agents/agent_types.py`
- Definido pelos desenvolvedores do LangChain
- Lista de tipos de agentes disponíveis

**Por que usar Enum?**
- ✅ IDE autocompleta (não precisa decorar)
- ✅ Evita erros de digitação
- ✅ Código mais profissional

**Equivalência:**
```python
# OPÇÃO 1: Usar Enum (recomendado)
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION

# OPÇÃO 2: Usar string direto
agent="zero-shot-react-description"

# São idênticos!
```

**Ver guia completo:** `GUIA_AGENTTYPE_EXPLICADO.md`

### Q35: O que é Enum em Python?

**A:** **Enum** = Enumeração = Lista fechada de opções pré-definidas.

```python
from enum import Enum

# Definir
class ModeloLLM(str, Enum):
    LLAMA3 = "llama3"
    LLAMA3_SMALL = "llama3.2:1b"
    MISTRAL = "mistral"

# Usar
modelo = ModeloLLM.LLAMA3
print(modelo)        # ModeloLLM.LLAMA3
print(modelo.value)  # "llama3"
```

**Analogia:** Como cardápio de restaurante - você aponta a opção, não digita livre.

**Vantagens:**
1. IDE mostra opções (autocomplete)
2. Impossível errar digitação
3. Type hints (validação de tipo)

### Q36: Diferença entre atributo de classe e instância?

**A:**

```python
class Exemplo:
    # ATRIBUTO DE CLASSE (compartilhado por todos)
    CONSTANTE = 100
    
    def __init__(self, nome):
        # ATRIBUTO DE INSTÂNCIA (único por objeto)
        self.nome = nome

# Atributo de classe: acesso direto
print(Exemplo.CONSTANTE)  # 100

# Atributo de instância: precisa criar objeto
obj = Exemplo("João")
print(obj.nome)  # "João"
```

**AgentType usa atributo de classe:**
```python
AgentType.ZERO_SHOT_REACT_DESCRIPTION  # ← acesso direto
```

### Q37: O que é *args e **kwargs?

**A:** Argumentos variáveis em Python.

```python
*args   = argumentos POSICIONAIS (vira tupla)
**kwargs = argumentos NOMEADOS (vira dict)
```

**Exemplo:**
```python
def funcao(*args, **kwargs):
    print(f"args = {args}")      # tupla
    print(f"kwargs = {kwargs}")  # dict

funcao(1, 2, 3)                    # args = (1, 2, 3)
funcao(a=1, b=2)                   # kwargs = {'a': 1, 'b': 2}
funcao(1, 2, x=10, y=20)          # args = (1, 2), kwargs = {'x': 10, 'y': 20}
```

**Onde você vê:**
```python
def wrapper(*args, **kwargs):  # ← Decorators!
    return funcao(*args, **kwargs)
```

**Por quê?**
- Aceita QUALQUER combinação de argumentos
- Passa adiante SEM saber quais são
- Essencial para decorators genéricos

**Ver guia completo:** `EXPLICACAO_ARGS_KWARGS.md`  
**Executar exemplo:** `python experimento_args_kwargs.py`

### Q38: Por que "args" e "kwargs" (esses nomes)?

**A:** Convenção da comunidade Python.

- `*args` = **arg**ument**s** (argumentos)
- `**kwargs` = **k**eyword **arg**ument**s** (argumentos com palavra-chave)

**Você PODE usar outros nomes:**
```python
def funcao(*numeros, **opcoes):  # Funciona!
    pass
```

**MAS:** Use `args` e `kwargs` (todo mundo usa, melhor legibilidade!)

---
print(Exemplo.CONSTANTE)  # 100

# Atributo de instância: precisa criar objeto
obj = Exemplo("João")
print(obj.nome)  # "João"
```

**AgentType usa atributo de classe:**
```python
AgentType.ZERO_SHOT_REACT_DESCRIPTION  # ← acesso direto
```

---

## 📞 AINDA COM DÚVIDA?

1. Consulte [TROUBLESHOOTING_E3.md](TROUBLESHOOTING_E3.md)
2. Consulte [CONCEITOS_DETALHADOS_E3.md](CONCEITOS_DETALHADOS_E3.md)
3. Consulte [GUIA_AGENTTYPE_EXPLICADO.md](GUIA_AGENTTYPE_EXPLICADO.md)
4. Pergunte ao professor
5. Pergunte ao colega

---

**Arquivo:** FAQ_E3.md  
**Localização:** 04_MATERIAL_APOIO/  
**Status:** ✅ 33 perguntas respondidas
