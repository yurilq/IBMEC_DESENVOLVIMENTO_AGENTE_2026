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
    
    # PASSO 1: Detectar se eh pergunta CONCEITUAL ou de DADOS
    palavras_conceituais = [
        "o que eh", "o que e", "que eh", "que e",
        "define", "definicao", "conceito", "significa",
        "explique", "explicar", "diferenca", "vs", "versus"
    ]
    
    eh_conceitual = any(palavra in pergunta_lower for palavra in palavras_conceituais)
    
    # PASSO 2: Detectar se pergunta por QUANTIDADE
    palavras_quantidade = [
        "quantas", "quanto", "quantos", "total", "numero",
        "existem", "tem", "ha", "possui"
    ]
    
    pede_quantidade = any(palavra in pergunta_lower for palavra in palavras_quantidade)
    
    # Se eh pergunta CONCEITUAL e NAO pede quantidade, responder sem tool
    if eh_conceitual and not pede_quantidade:
        print("[CHAIN-OF-THOUGHT]")
        print("PASSO 1: Pergunta CONCEITUAL (nao pede dados numericos)")
        print("PASSO 2: Consultar base de conhecimento (Few-Shot)")
        print("PASSO 3: Formular resposta baseada nos exemplos")
        
        # Base de conhecimento (respostas pre-definidas baseadas em Few-Shot)
        respostas_conceituais = {
            "bo": "BO (Boletim de Ocorrencia) eh o registro policial de um crime ou incidente. No SINARM, cada BO documenta ocorrencias envolvendo armas de fogo no Distrito Federal.",
            
            "furto": "Furto eh a apropriacao de bem alheio SEM violencia ou ameaca. No SINARM, 'Furto de Arma de Fogo' registra armas subtraidas sem confronto direto com a vitima.",
            
            "roubo": "Roubo eh a apropriacao de bem alheio COM violencia ou grave ameaca. No SINARM, 'Roubo de Arma de Fogo' indica que a arma foi tomada mediante violencia.",
            
            "apreensao": "Apreensao eh quando a policia recolhe arma de fogo encontrada em poder irregular (sem registro, em local de crime, etc). Registrada no SINARM como 'Apreensao de Arma de Fogo'.",
            
            "sinarm": "SINARM (Sistema Nacional de Armas) eh o banco de dados nacional que registra armas de fogo, suas ocorrencias (roubo, furto, apreensao) e proprietarios. Gerido pela Policia Federal.",
            
            "calibre": "Calibre eh o diametro interno do cano da arma. Exemplos: .38 (9.65mm), 9mm, .40 (10.16mm), .45 (11.43mm). Determina que municao a arma usa.",
            
            "pcdf": "PCDF (Policia Civil do Distrito Federal) eh responsavel pela investigacao criminal no DF. Usa dados do SINARM para rastrear armas envolvidas em crimes."
        }
        
        # Detectar topico da pergunta
        resposta = None
        for topico, definicao in respostas_conceituais.items():
            if topico in pergunta_lower:
                resposta = definicao
                break
        
        # Se detectou diferenca/comparacao
        if any(palavra in pergunta_lower for palavra in ["diferenca", "vs", "versus", "comparar"]):
            if "roubo" in pergunta_lower and "furto" in pergunta_lower:
                resposta = "DIFERENCA entre ROUBO e FURTO:\n\n" \
                          "ROUBO = Apropriacao COM violencia ou ameaca.\n" \
                          "FURTO = Apropriacao SEM violencia.\n\n" \
                          "Ambos sao registrados no SINARM quando envolvem armas de fogo. " \
                          "A diferenca legal eh a presenca de violencia."
        
        if resposta:
            return resposta
        else:
            return "Nao tenho informacao conceitual sobre esse topico. Posso responder sobre: BO, furto, roubo, apreensao, SINARM, calibre, PCDF."
    
    # Se pede quantidade, continuar com deteccao de entidades
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
    
    # Se nao identificou dados, responder que nao entendeu
    if not tool_escolhida:
        print("[CHAIN-OF-THOUGHT]")
        print("PASSO 1: Nao identifiquei entidades (marca, calibre, tipo)")
        print("PASSO 2: Responder que precisa de mais informacoes")
        
        return "Nao consegui identificar sobre o que voce quer dados. Tente perguntar sobre: marca (Taurus, Glock), calibre (.38, 9mm) ou tipo (apreensao, roubo, furto)."
    
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
    
    # Formatar resposta diretamente (sem LLM para evitar bloqueios de seguranca)
    if marca_encontrada and tipo_encontrado:
        resposta_final = f"Segundo o SINARM 2026, existem {total} armas {marca_encontrada} do tipo {tipo_encontrado} registradas no Distrito Federal."
    elif marca_encontrada:
        resposta_final = f"Segundo o SINARM 2026, existem {total} armas da marca {marca_encontrada} registradas no Distrito Federal."
    elif calibre_encontrado:
        resposta_final = f"Segundo o SINARM 2026, existem {total} armas calibre {calibre_encontrado} registradas no Distrito Federal."
    elif tipo_encontrado:
        resposta_final = f"Segundo o SINARM 2026, foram registradas {total} ocorrencias do tipo {tipo_encontrado} no Distrito Federal."
    else:
        resposta_final = resultado_tool
    
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