# agente_v0_1_simples.py
# Agente básico SIMPLIFICADO para LangChain 1.3+
# Usa abordagem direta com LLM + Tool

from langchain_ollama import OllamaLLM
from langchain_core.tools import tool
from tools_basicas import contar_armas_marca
import json

print("="*60)
print("CRIANDO AGENTE SIMPLES COM 1 TOOL")
print("="*60)

# PARTE 1: Criar LLM
print("\n1. Criando LLM...")
llm = OllamaLLM(model="llama3", temperature=0)
print("   [OK] LLM criado")

# PARTE 2: Explicar tool disponível ao LLM
print("\n2. Preparando tool...")

# Criar descrição da tool para o LLM
tool_description = """
Você tem acesso à seguinte ferramenta:

Tool: ContarArmas
Descrição: Conta quantas armas de uma marca específica existem no banco de dados SINARM
Input: Nome da marca (string) - ex: 'Taurus', 'Glock', 'Rossi'
Output: Texto com o total de armas encontradas

Para usar a tool, responda EXATAMENTE neste formato:
Action: ContarArmas
Action Input: [nome da marca]

Exemplo:
Action: ContarArmas
Action Input: Taurus
"""

print("   [OK] Tool preparada")

# PARTE 3: Função agente manual
print("\n3. Criando função agente...")

def agente_simples(pergunta):
    """Agente que usa LLM + Tool manualmente"""
    
    # Criar prompt completo
    prompt = f"""{tool_description}

Pergunta do usuário: {pergunta}

Pense passo a passo:
1. Analise a pergunta
2. Decida se precisa usar a tool
3. Se sim, formate a ação corretamente
4. Responda ao usuário

Sua resposta:"""
    
    # Chamar LLM
    print("\n[Agente pensando...]")
    resposta_llm = llm.invoke(prompt)
    print(f"\nPensamento do LLM:\n{resposta_llm}")
    
    # Verificar se LLM quer usar tool
    if "Action: ContarArmas" in resposta_llm:
        print("\n[Agente decidiu usar a tool ContarArmas]")
        
        # Extrair o input (marca)
        try:
            lines = resposta_llm.split('\n')
            action_input = None
            for line in lines:
                if "Action Input:" in line:
                    action_input = line.split("Action Input:")[-1].strip()
                    break
            
            if action_input:
                print(f"[Executando: ContarArmas('{action_input}')]")
                
                # Chamar tool
                resultado_tool = contar_armas_marca(action_input)
                print(f"[Resultado da tool: {resultado_tool}]")
                
                # Dar resultado ao LLM para formular resposta final
                prompt_final = f"""Você usou a tool ContarArmas e obteve o seguinte resultado:
{resultado_tool}

Pergunta original: {pergunta}

Agora formule uma resposta final clara e objetiva para o usuário:"""
                
                resposta_final = llm.invoke(prompt_final)
                return resposta_final
            else:
                return "Erro: Não consegui extrair o input da ação"
                
        except Exception as e:
            return f"Erro ao processar ação: {e}"
    else:
        # LLM respondeu diretamente sem usar tool
        return resposta_llm

print("   [OK] Agente criado")

# PARTE 4: Testar
print("\n" + "="*60)
print("TESTANDO AGENTE")
print("="*60 + "\n")

pergunta = "Quantas armas Taurus existem?"
print(f"PERGUNTA: {pergunta}\n")

resposta = agente_simples(pergunta)

print(f"\n" + "="*60)
print(f"RESPOSTA FINAL: {resposta}")
print("="*60)
