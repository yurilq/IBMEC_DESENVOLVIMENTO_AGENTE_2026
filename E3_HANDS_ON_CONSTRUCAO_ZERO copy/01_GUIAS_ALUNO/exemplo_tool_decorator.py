# exemplo_tool_decorator.py
# Demonstracao de @tool do LangChain

from langchain_core.tools import tool

print("="*60)
print("EXEMPLO: @TOOL DO LANGCHAIN")
print("="*60)

# FUNCAO NORMAL (sem decorator)
print("\n1. FUNCAO NORMAL (sem @tool):\n")

def calcular_soma_normal(a: int, b: int) -> int:
    """Soma dois numeros"""
    return a + b

print(f"   Tipo: {type(calcular_soma_normal)}")
print(f"   Nome: {calcular_soma_normal.__name__}")
print(f"   Resultado: {calcular_soma_normal(5, 3)}")

# FUNCAO COM @tool
print("\n" + "-"*60)
print("2. FUNCAO COM @tool:\n")

@tool
def calcular_soma(a: int, b: int) -> int:
    """Soma dois numeros"""
    return a + b

print(f"   Tipo: {type(calcular_soma)}")
print(f"   Nome: {calcular_soma.name}")  # <- .name (nao __name__)
print(f"   Descricao: {calcular_soma.description}")
print(f"   Args: {calcular_soma.args}")

# Para executar, usar .invoke() ou .func()
print(f"\n   Executar com .invoke(): {calcular_soma.invoke({'a': 5, 'b': 3})}")
print(f"   Executar com .func(): {calcular_soma.func(5, 3)}")

# COMPARACAO
print("\n" + "="*60)
print("COMPARACAO")
print("="*60)

print("""
FUNCAO NORMAL:
- Chama direto: funcao(5, 3)
- Sem metadados
- Nao funciona com LangChain agents

FUNCAO COM @tool:
- Chama com: tool.invoke({'a': 5, 'b': 3}) ou tool.func(5, 3)
- TEM metadados: name, description, args
- FUNCIONA com LangChain agents
- Agent consegue "ver" a funcao e decidir quando usar!
""")

# EXEMPLO PRATICO
print("="*60)
print("EXEMPLO PRATICO: MULTIPLAS TOOLS")
print("="*60)

@tool
def somar(a: int, b: int) -> int:
    """Soma dois numeros"""
    return a + b

@tool
def multiplicar(a: int, b: int) -> int:
    """Multiplica dois numeros"""
    return a * b

@tool
def dividir(a: int, b: int) -> float:
    """Divide dois numeros"""
    return a / b

# Lista de tools
tools = [somar, multiplicar, dividir]

print("\nTools disponiveis:\n")
for t in tools:
    print(f"   - {t.name}: {t.description}")

# Agent pode "ver" as tools e escolher qual usar
print("\nPergunta: 'Quanto eh 10 * 5?'")
print("Agent escolhe: multiplicar")
print(f"Resultado: {multiplicar.func(10, 5)}")

print("\nPergunta: 'Quanto eh 100 / 4?'")
print("Agent escolhe: dividir")
print(f"Resultado: {dividir.func(100, 4)}")

print("\n" + "="*60)
print("CONCEITO APRENDIDO:")
print("="*60)
print("""
@tool transforma funcao Python em "ferramenta" que:
1. LangChain agents conseguem "ver"
2. TEM metadados (nome, descricao, args)
3. Agent decide QUANDO usar baseado na descricao
4. ESSENCIAL para criar agents inteligentes!

SINTAXE:

@tool
def minha_funcao(parametro: tipo) -> tipo:
    \"\"\"Descricao clara do que faz\"\"\"
    return resultado

IMPORTANTE: Descricao (docstring) eh CRITICA!
Agent le a descricao para decidir se deve usar a tool.
""")

print("="*60)
print("EXEMPLO CONCLUIDO!")
print("="*60)
