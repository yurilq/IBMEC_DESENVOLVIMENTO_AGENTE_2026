# agente_v0_1.py
# Agente básico SEM decorator (jeito manual)
# Compatível com LangChain 1.3+

from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from tools_basicas import contar_armas_marca

print("="*60)
print("CRIANDO AGENTE COM 1 TOOL - LangChain 1.3+")
print("="*60)

# PARTE 1: Criar LLM
print("\n1. Criando LLM...")
llm = OllamaLLM(model="llama3", temperature=0)
print("   [OK] LLM criado")

# PARTE 2: Criar Tool MANUALMENTE (jeito chato)
print("\n2. Criando Tool manualmente...")
tool_contar = Tool(
    name="ContarArmas",
    func=contar_armas_marca,
    description="Conta quantas armas de uma marca específica. Input: string com nome da marca (ex: 'Taurus', 'Glock'). Output: Total de armas encontradas."
)
print("   [OK] Tool criada")

# PARTE 3: Criar prompt template (necessário no LangChain 1.3+)
print("\n3. Criando prompt...")
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)
print("   [OK] Prompt criado")

# PARTE 4: Criar agente
print("\n4. Criando agente...")
tools = [tool_contar]
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
print("   [OK] Agente criado")

# PARTE 5: Testar
print("\n" + "="*60)
print("TESTANDO AGENTE")
print("="*60 + "\n")

pergunta = "Quantas armas Taurus existem?"
print(f"PERGUNTA: {pergunta}\n")

resposta = agent_executor.invoke({"input": pergunta})

print(f"\n[OK] RESPOSTA FINAL: {resposta['output']}\n")
print("="*60)
