"""
EXEMPLO: Entendendo Enum (Como AgentType funciona)

Demonstração prática de Enum em Python para entender como
LangChain implementou AgentType.ZERO_SHOT_REACT_DESCRIPTION

Execute: python exemplo_enum_agenttype.py
"""

print("="*70)
print("DEMONSTRAÇÃO: ENTENDENDO Enum (AgentType)")
print("="*70)

# ============================================================================
# PARTE 1: SEM ENUM (Problema)
# ============================================================================

print("\n" + "-"*70)
print("PARTE 1: SEM ENUM - Usando strings direto (PROBLEMAS)")
print("-"*70)

def criar_agente_sem_enum(tipo_agente):
    """Simula criação de agente usando string"""
    if tipo_agente == "zero-shot-react-description":
        return "Agente ReAct criado [OK]"
    elif tipo_agente == "conversational-react-description":
        return "Agente Conversacional criado [OK]"
    else:
        return "ERRO: Tipo desconhecido [X]"

# Teste 1: Correto
resultado1 = criar_agente_sem_enum("zero-shot-react-description")
print(f"\nTeste 1 (correto): {resultado1}")

# Teste 2: Erro de digitação (PROBLEMA!)
resultado2 = criar_agente_sem_enum("zero-shot-react-descripton")  # falta 'i'
print(f"Teste 2 (erro digitação): {resultado2}")
print("  -- PROBLEMA: Erro só aparece em tempo de execução!")

# Teste 3: Sem autocomplete
print("\nTeste 3: Sem IDE ajuda")
print("  -- Precisa DECORAR ou CONSULTAR documentação")

# ============================================================================
# PARTE 2: COM ENUM (Solução)
# ============================================================================

print("\n" + "-"*70)
print("PARTE 2: COM ENUM - Como LangChain faz (SOLUÇÃO)")
print("-"*70)

from enum import Enum

class TipoAgente(str, Enum):
    """Lista fechada de tipos de agentes (como LangChain AgentType)"""
    
    ZERO_SHOT_REACT = "zero-shot-react-description"
    CONVERSATIONAL_REACT = "conversational-react-description"
    SELF_ASK_SEARCH = "self-ask-with-search"

def criar_agente_com_enum(tipo_agente):
    """Simula criação de agente usando Enum"""
    if tipo_agente == TipoAgente.ZERO_SHOT_REACT.value:
        return "Agente ReAct criado [OK]"
    elif tipo_agente == TipoAgente.CONVERSATIONAL_REACT.value:
        return "Agente Conversacional criado [OK]"
    else:
        return "ERRO: Tipo desconhecido [X]"

# Teste 1: Usando Enum
print("\n1. Usando Enum (recomendado):")
resultado = criar_agente_com_enum(TipoAgente.ZERO_SHOT_REACT.value)
print(f"   {resultado}")

# Teste 2: Ver todas opções
print("\n2. Ver TODAS as opções disponíveis:")
for tipo in TipoAgente:
    print(f"   - {tipo.name:25} = '{tipo.value}'")

# Teste 3: Impossível errar
print("\n3. Tentando erro de digitação:")
print("   TipoAgente.ZERO_SHOT_REACT_DESCRIPTON  <- IDE avisa ANTES!")
print("   -- AttributeError: 'TipoAgente' has no attribute '...'")

# Teste 4: Autocomplete
print("\n4. Autocomplete da IDE:")
print("   Digite: TipoAgente.")
print(f"   IDE mostra: ZERO_SHOT_REACT | CONVERSATIONAL_REACT | SELF_ASK_SEARCH")
print(f"   Nao precisa decorar! [OK]")

# ============================================================================
# PARTE 3: ANATOMIA DO ENUM
# ============================================================================

print("\n" + "-"*70)
print("PARTE 3: ANATOMIA - O que está acontecendo?")
print("-"*70)

tipo = TipoAgente.ZERO_SHOT_REACT

print(f"\n1. Objeto completo:")
print(f"   {tipo}")
print(f"   -- Tipo: {type(tipo)}")

print(f"\n2. Nome (MAIÚSCULAS):")
print(f"   {tipo.name}")
print(f"   -- O que você escreve no código")

print(f"\n3. Valor (string):")
print(f"   {tipo.value}")
print(f"   -- O que LangChain usa internamente")

print(f"\n4. São equivalentes?")
print(f"   TipoAgente.ZERO_SHOT_REACT.value == 'zero-shot-react-description'")
print(f"   {tipo.value == 'zero-shot-react-description'} [OK]")

# ============================================================================
# PARTE 4: COMO LANGCHAIN USA
# ============================================================================

print("\n" + "-"*70)
print("PARTE 4: COMO LANGCHAIN USA (Simulação)")
print("-"*70)

# Simulando AgentType do LangChain
class AgentType(str, Enum):
    """Cópia simplificada do AgentType real do LangChain"""
    ZERO_SHOT_REACT_DESCRIPTION = "zero-shot-react-description"
    CONVERSATIONAL_REACT_DESCRIPTION = "conversational-react-description"
    SELF_ASK_WITH_SEARCH = "self-ask-with-search"

# Simulando initialize_agent()
def initialize_agent(agent, llm=None, tools=None):
    """Simulação da função do LangChain"""
    # Converter Enum para string
    if isinstance(agent, AgentType):
        agent_type = agent.value
    else:
        agent_type = agent
    
    return f"Agente '{agent_type}' inicializado [OK]"

print("\n1. Uso com Enum (moderno):")
resultado1 = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
print(f"   {resultado1}")

print("\n2. Uso com string (antigo):")
resultado2 = initialize_agent(
    agent="zero-shot-react-description"
)
print(f"   {resultado2}")

print(f"\n3. São idênticos?")
print(f"   {resultado1 == resultado2} [OK]")

# ============================================================================
# PARTE 5: CRIANDO SEU PRÓPRIO ENUM
# ============================================================================

print("\n" + "-"*70)
print("PARTE 5: EXERCÍCIO - Criar seu próprio Enum")
print("-"*70)

# Exemplo: Enum para modelos LLM
class ModeloLLM(str, Enum):
    """Modelos disponíveis no Ollama"""
    LLAMA3_8B = "llama3"
    LLAMA3_1B = "llama3.2:1b"
    MISTRAL = "mistral"
    PHI3 = "phi3"
    TINYLLAMA = "tinyllama"

print("\n1. Modelos disponíveis:")
for modelo in ModeloLLM:
    print(f"   - {modelo.name:15} -> {modelo.value}")

print("\n2. Usar no código:")
print("   from langchain_ollama import OllamaLLM")
print(f"   llm = OllamaLLM(model=ModeloLLM.LLAMA3_1B.value)")
print(f"   -- Valor real: '{ModeloLLM.LLAMA3_1B.value}'")

# ============================================================================
# PARTE 6: COMPARAÇÃO VISUAL
# ============================================================================

print("\n" + "-"*70)
print("PARTE 6: COMPARAÇÃO VISUAL")
print("-"*70)

print("""
ANATOMIA:
=========

AgentType.ZERO_SHOT_REACT_DESCRIPTION
-         -
-         -- Constante (atributo da classe)
-            - Nome: ZERO_SHOT_REACT_DESCRIPTION
-            - Valor: "zero-shot-react-description"
-            - Tipo: str
-
-- Classe Enum
   - Arquivo: langchain/agents/agent_types.py
   - Herda: str, Enum
   - Propósito: Lista fechada de opções


ANALOGIA:
=========

1. SEM ENUM (pedir falando):
   pedir_pizza("calabresa com queijo")  <- pode errar falando

2. COM ENUM (apontar cardápio):
   pedir_pizza(Cardapio.CALABRESA)      <- impossível errar


VANTAGENS:
==========

[OK] IDE autocompleta (Tab mostra opções)
[OK] Erro aparece ANTES de rodar (compile time)
[OK] Type hints (validação de tipo)
[OK] Documentação inline (hover mostra descrição)
[OK] Refatoração segura
[OK] Código mais legível
""")

# ============================================================================
# PARTE 7: INVESTIGANDO O REAL LANGCHAIN
# ============================================================================

print("\n" + "-"*70)
print("PARTE 7: INVESTIGANDO LANGCHAIN REAL")
print("-"*70)

try:
    from langchain.agents import AgentType as RealAgentType
    
    print("\n[OK] LangChain instalado! Explorando AgentType real...\n")
    
    print("1. Tipos disponíveis no LangChain:")
    for i, tipo in enumerate(RealAgentType, 1):
        print(f"   {i:2}. {tipo.name:45} = '{tipo.value}'")
    
    print(f"\n2. Total de tipos: {len(list(RealAgentType))}")
    
    print("\n3. Exemplo de uso:")
    print(f"   AgentType.ZERO_SHOT_REACT_DESCRIPTION")
    print(f"   -- Valor: '{RealAgentType.ZERO_SHOT_REACT_DESCRIPTION.value}'")
    
except ImportError:
    print("\n[!] LangChain não instalado")
    print("   Instale: pip install langchain")

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("\n" + "="*70)
print("RESUMO: AgentType.ZERO_SHOT_REACT_DESCRIPTION")
print("="*70)

print("""
O QUE É:
--------
• AgentType          -> Classe Enum (definida pelo LangChain)
• .ZERO_SHOT_REACT   -> Constante/atributo dessa classe
• Valor real         -> "zero-shot-react-description" (string)

DE ONDE VEM:
------------
• Arquivo: langchain/agents/agent_types.py
• Criado por: Desenvolvedores do LangChain
• Propósito: Padronizar tipos de agentes

COMO USAR:
----------
from langchain.agents import AgentType

# Opção 1 (recomendado):
agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION

# Opção 2 (equivalente):
agent = "zero-shot-react-description"

POR QUE ENUM:
-------------
[OK] IDE autocompleta
[OK] Erro antes de executar
[OK] Não precisa decorar nomes
[OK] Código profissional

IMPORTANTE:
-----------
[!] LangChain 0.2+ removeu AgentType!
  Agora usa create_react_agent() diretamente
  (mais flexível, menos mágico)
""")

print("="*70)
print("DEMONSTRAÇÃO CONCLUÍDA!")
print("="*70)
print("\nPróximos passos:")
print("  1. Teste modificando os enums acima")
print("  2. Crie seu próprio Enum para outros casos")
print("  3. Consulte GUIA_AGENTTYPE_EXPLICADO.md para detalhes")



