# agente_v3_0.py
# Agente v3.0 COM Few-Shot + Chain-of-Thought

from langchain.agents import initialize_agent, AgentType
from langchain_ollama import ChatOllama

from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)

tools = [
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
]

llm = ChatOllama(model="llama3", temperature=0)
agente = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
resp = agente.invoke({"input": "Há mais armas Taurus ou Glock?"})
print("="*60)
print("Resposta da agente:", resp["output"])