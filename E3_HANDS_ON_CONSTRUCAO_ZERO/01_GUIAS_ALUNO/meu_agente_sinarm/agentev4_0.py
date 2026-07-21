
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado,
)

print("=" * 60)
print("AGENTE COM TOOL CALLING REAL (a LLM escolhe a tool)")
print("=" * 60)

# ---------------------------------------------------------------
# 1) LLM de CHAT + bind das tools.
#    ChatOllama expoe .tool_calls; OllamaLLM (o do roteador) NAO.
# ---------------------------------------------------------------
tools = [
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado,
]
tools_por_nome = {t.name: t for t in tools}

llm = ChatOllama(model="llama3", temperature=0, num_gpu=0)  # CPU
llm_com_tools = llm.bind_tools(tools)  # <- aqui a LLM PASSA a conhecer as tools

for t in tools:
    print(f"  - {t.name}")

# ---------------------------------------------------------------
# 2) System prompt: orienta QUANDO usar tools. Nao faz o parsing;
#    apenas instrui o modelo. A decisao final eh do modelo.
# ---------------------------------------------------------------
SYSTEM_PROMPT = """Voce eh um investigador da PCDF especialista no SINARM.

GLOSSARIO:
BO=Boletim de Ocorrencia; FURTO=sem violencia; ROUBO=com violencia;
APREENSAO=arma retirada de circulacao; PERDA=arma extraviada;
SINARM=Sistema Nacional de Armas; PCDF=Policia Civil do DF.

REGRAS:
- Para perguntas sobre QUANTIDADES/estatisticas, USE as tools disponiveis.
- Para comparacoes (ex: "mais X ou Y?"), chame a tool uma vez para CADA item.
- Para perguntas conceituais (definicoes), responda direto, SEM tools.
- Sempre cite a fonte "SINARM 2026" e use linguagem tecnica PCDF.
"""


# ---------------------------------------------------------------
# 3) Loop de agente (estilo ReAct minimo).
# ---------------------------------------------------------------
def agente(pergunta: str, max_iteracoes: int = 5) -> str:
    print(f"\n[PERGUNTA] {pergunta}")
    print("-" * 60)

    mensagens = [SystemMessage(SYSTEM_PROMPT), HumanMessage(pergunta)]

    for passo in range(1, max_iteracoes + 1):
        resposta_ia = llm_com_tools.invoke(mensagens)
        mensagens.append(resposta_ia)

        # A LLM NAO pediu tool -> resposta final.
        if not resposta_ia.tool_calls:
            print(f"[iter {passo}] LLM respondeu sem pedir tools -> fim")
            return resposta_ia.content

        # A LLM pediu uma ou mais tools. Executamos cada uma.
        for chamada in resposta_ia.tool_calls:
            nome = chamada["name"]
            args = chamada["args"]
            print(f"[iter {passo}] LLM ESCOLHEU a tool '{nome}' com args {args}")

            tool = tools_por_nome.get(nome)
            if tool is None:
                resultado = f"Tool '{nome}' nao existe."
            else:
                resultado = tool.invoke(args)

            print(f"          resultado -> {resultado}")
            mensagens.append(
                ToolMessage(content=str(resultado), tool_call_id=chamada["id"])
            )
        # volta ao topo do loop: a LLM ve os ToolMessages e continua.

    return "[LIMITE] Numero maximo de iteracoes atingido sem resposta final."


# ---------------------------------------------------------------
# TESTES
# ---------------------------------------------------------------
if __name__ == "__main__":
    perguntas = [
        "Quantas armas Taurus existem?",
        "O que eh BO de furto?",
        "Ha mais Taurus ou Glock?",
    ]
    for i, pergunta in enumerate(perguntas, 1):
        print(f"\n{'=' * 60}\nTESTE {i}\n{'=' * 60}")
        print("\n[RESPOSTA FINAL]")
        print(agente(pergunta))

#fim da solução 


agente_v3_0.py

# agente_v3_0.py
# Agente v3.0 COM Few-Shot + Chain-of-Thought

from langchain_ollama import OllamaLLM
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)
import re

print("="*60)
print("AGENTE v3.0 - Few-Shot + Chain-of-Thought")
print("="*60)

# PARTE 1: Criar LLM
print("\n[1/4] Criando LLM...")
llm = OllamaLLM(model="llama3.2:1b", temperature=0)
print("      [OK] LLM criado")

# PARTE 2: Registrar tools
print("\n[2/4] Registrando tools...")
tools = [
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
]

for tool in tools:
    print(f"      - {tool.name}")

print("      [OK] 4 tools registradas")

# PARTE 3: Criar agente COM Few-Shot + CoT
print("\n[3/4] Criando agente v3.0...")

# PROMPT COM FEW-SHOT + CHAIN-OF-THOUGHT
SYSTEM_PROMPT = """Voce eh um investigador da PCDF especialista em analise de dados do SINARM.

=== EXEMPLOS (Few-Shot Learning) ===

Exemplo 1:
Pergunta: "O que eh BO de furto?"
Resposta: "BO de furto eh Boletim de Ocorrencia com tipo FURTO no SINARM. Furto eh apropriacao SEM violencia."

Exemplo 2:
Pergunta: "Calibre .38?"
Resposta: "Calibre .38 eh municao de revolver, comum em armas apreendidas no DF."

Exemplo 3:
Pergunta: "Diferenca roubo vs furto?"
Resposta: "ROUBO = com violencia/ameaca. FURTO = sem violencia. Ambos registrados no SINARM."

=== CHAIN-OF-THOUGHT (Sempre seguir) ===

Ao responder QUALQUER pergunta, siga estes PASSOS:

PASSO 1 - ANALISE:
- Tipo de pergunta: dados ou conceito?
- Dados necessarios: marca? calibre? tipo?

PASSO 2 - BUSCA (se precisar):
- Tool escolhida: [qual]
- Parametros: [valores]

PASSO 3 - RESULTADO:
- Valores: [numeros exatos]

PASSO 4 - RESPOSTA FINAL:
- Conclusao objetiva
- Fonte: SINARM 2026

=== INSTRUCOES ===

- Use linguagem tecnica PCDF
- Sempre cite fonte
- Mostre raciocinio (PASSO 1, 2, 3, 4)
- Seja preciso com numeros
"""

def agente_v3_fewshot_cot(pergunta_usuario):
    """
    Agente v3.0 com Few-Shot + Chain-of-Thought
    """
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*60)
    
    pergunta_lower = pergunta_usuario.lower()
    
    # Detectar marca
    marcas = ["taurus", "glock", "rossi", "beretta", "smith"]
    marca_encontrada = None
    for marca in marcas:
        if marca in pergunta_lower:
            marca_encontrada = marca.capitalize()
            break
    
    # Detectar calibre
    calibres = [".38", ".380", "9mm", ".40", ".45"]
    calibre_encontrado = None
    for calibre in calibres:
        if calibre in pergunta_lower:
            calibre_encontrado = calibre
            break
    
    # Detectar tipo
    tipos = {
        "apreens": "Apreens",
        "roubo": "Roubo",
        "roub": "Roubo",
        "furto": "Furto",
        "perda": "Perda"
    }
    tipo_encontrado = None
    for palavra, tipo in tipos.items():
        if palavra in pergunta_lower:
            tipo_encontrado = tipo
            break
    
    # Selecionar tool
    tool_escolhida = None
    parametros = {}
    
    if marca_encontrada and tipo_encontrado:
        tool_escolhida = contar_armas_combinado
        parametros = {"marca": marca_encontrada, "tipo": tipo_encontrado}
    elif marca_encontrada:
        tool_escolhida = contar_armas_marca
        parametros = {"marca": marca_encontrada}
    elif calibre_encontrado:
        tool_escolhida = contar_armas_calibre
        parametros = {"calibre": calibre_encontrado}
    elif tipo_encontrado:
        tool_escolhida = contar_armas_tipo
        parametros = {"tipo": tipo_encontrado}
    
    # Se nao identificou dados, responder com conceito
    if not tool_escolhida:
        print("[CHAIN-OF-THOUGHT]")
        print("PASSO 1: Pergunta conceitual (nao precisa de dados)")
        print("PASSO 2: Consultar conhecimento interno")
        print("PASSO 3: Formular resposta tecnica")
        
        prompt = f"""{SYSTEM_PROMPT}

Pergunta do usuario: "{pergunta_usuario}"

IMPORTANTE: Esta eh uma pergunta CONCEITUAL (nao precisa buscar dados).
Responda usando os EXEMPLOS como guia.
Mostre seu RACIOCINIO (PASSO 1, 2, 3, 4).

Resposta:"""
        
        resposta = llm.invoke(prompt)
        return resposta
    
    # Se identificou dados, chamar tool
    print("[CHAIN-OF-THOUGHT]")
    print(f"PASSO 1: Pergunta sobre DADOS")
    print(f"PASSO 2: Tool escolhida = {tool_escolhida.name}")
    print(f"PASSO 3: Buscando dados...")
    
    resultado_tool = tool_escolhida.func(**parametros)
    
    print(f"PASSO 4: Dados obtidos = {resultado_tool}")
    print(f"PASSO 5: Formatando resposta...")
    
    # Extrair numero
    numeros = re.findall(r'\d+', resultado_tool)
    total = numeros[0] if numeros else "?"
    
    prompt = f"""{SYSTEM_PROMPT}

Dados do SINARM: {resultado_tool}

Pergunta do usuario: "{pergunta_usuario}"

IMPORTANTE: 
- Responda de forma OBJETIVA
- Cite a fonte: "SINARM 2026"
- Mostre confianca (voce tem os dados!)

Resposta:"""
    
    resposta_final = llm.invoke(prompt)
    
    return resposta_final

print("      [OK] Agente v3.0 pronto")

# PARTE 4: Testar
print("\n[4/4] Testando agente v3.0...")
print("="*60)

perguntas = [
    "Quantas armas Taurus existem?",
    "O que eh BO de furto?",
    "Ha mais Taurus ou Glock?"  # Requer 2 buscas (desafio!)
]

for i, pergunta in enumerate(perguntas, 1):
    print(f"\n{'='*60}")
    print(f"TESTE {i}:")
    print("="*60)
    
    resposta = agente_v3_fewshot_cot(pergunta)
    
    print("\n[RESPOSTA FINAL]")
    print(resposta)
    print()

print("="*60)
print("AGENTE v3.0 CONCLUIDO!")
print("="*60)
