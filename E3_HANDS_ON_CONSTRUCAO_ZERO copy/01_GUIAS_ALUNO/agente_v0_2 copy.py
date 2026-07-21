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
