# TEMPLATE_HORA_5.py
# AGENTE SINARM v2.0 COMPLETO
# Código de referência para Parte 5: Few-Shot + CoT + Security
# CÓDIGO FINAL COMPLETO DA AULA

import pandas as pd
from functools import lru_cache
from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType

# ============================================================
# VALIDAÇÃO DE SEGURANÇA
# ============================================================

def validar_input(texto: str):
    """Valida input do usuário contra ataques"""
    
    # 1. Validação de tamanho
    if len(texto) > 500:
        raise ValueError("Query muito longa (máx 500 caracteres)")
    
    if len(texto) < 3:
        raise ValueError("Query muito curta (mín 3 caracteres)")
    
    # 2. Caracteres perigosos (SQL injection)
    caracteres_perigosos = [";", "--", "DROP", "DELETE", "INSERT", "UPDATE"]
    for char in caracteres_perigosos:
        if char in texto.upper():
            raise ValueError(f"Caractere perigoso detectado: {char}")
    
    # 3. Palavras proibidas (Prompt injection)
    palavras_proibidas = ["ignore instruções", "esqueça", "você agora é"]
    for palavra in palavras_proibidas:
        if palavra.lower() in texto.lower():
            raise ValueError(f"Possível prompt injection: {palavra}")
    
    return True


def perguntar_agente_seguro(pergunta: str):
    """Wrapper seguro para perguntar ao agente"""
    try:
        # Validar input
        validar_input(pergunta)
        
        # Executar agente
        resposta = agente.invoke({"input": pergunta})
        return resposta["output"]
        
    except ValueError as e:
        return f"❌ ERRO DE SEGURANÇA: {e}"
    except Exception as e:
        return f"❌ ERRO: {e}"


# ============================================================
# CACHE + TOOLS
# ============================================================

@lru_cache(maxsize=1)
def carregar_csv():
    """Carrega CSV UMA VEZ e guarda em cache"""
    print("🔄 Carregando CSV...")
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv",
                     sep=";", encoding="latin1")
    print(f"✅ CSV carregado! {len(df)} linhas")
    return df


@tool
def contar_armas_marca(marca: str) -> str:
    """Conta quantas armas de uma marca específica.
    
    Args:
        marca: Nome da marca (ex: Taurus, Glock, Rossi)
    """
    df = carregar_csv()
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    return f"Encontrei {len(resultado)} armas {marca}"


@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta quantas armas de um calibre específico.
    
    Args:
        calibre: Calibre da arma (ex: .38 TPC, 9mm, .40 S&W)
    """
    df = carregar_csv()
    resultado = df[df["CALIBRE"] == calibre]
    return f"Encontrei {len(resultado)} armas calibre {calibre}"


@tool
def contar_armas_tipo(tipo: str) -> str:
    """Conta armas por tipo de ocorrência.
    
    Args:
        tipo: Tipo (ex: Apreensão, Roubo, Furto, Perda)
    """
    df = carregar_csv()
    resultado = df[df["TIPO_OCORRENCIA"] == tipo.upper()]
    return f"Encontrei {len(resultado)} ocorrências tipo {tipo}"


@tool
def contar_armas_combinado(marca: str, tipo: str) -> str:
    """Conta armas por marca E tipo simultaneamente.
    
    Args:
        marca: Marca da arma
        tipo: Tipo de ocorrência
    """
    df = carregar_csv()
    resultado = df[
        (df["MARCA_ARMA"] == marca.upper()) & 
        (df["TIPO_OCORRENCIA"] == tipo.upper())
    ]
    return f"Encontrei {len(resultado)} armas {marca} do tipo {tipo}"


# ============================================================
# CONFIGURAÇÃO DO AGENTE (FEW-SHOT + COT)
# ============================================================

llm = OllamaLLM(model="llama3", temperature=0)

system_message = """
Você é um investigador da PCDF especialista em análise de dados do SINARM.

=== EXEMPLOS (Few-Shot Learning) ===

Pergunta: "O que é BO de furto?"
Resposta: "BO de furto é Boletim de Ocorrência com tipo=FURTO no SINARM. Furto é apropriação de bem sem violência ou ameaça."

Pergunta: "Calibre .38?"
Resposta: "Calibre .38 TPC é munição de revólver calibre nominal 9mm, comum em armas apreendidas no Brasil."

Pergunta: "Diferença entre roubo e furto?"
Resposta: "ROUBO: crime com violência ou ameaça. FURTO: crime sem violência. Ambos registrados no SINARM com tipos diferentes."

=== CHAIN-OF-THOUGHT (Sempre seguir) ===

Ao responder QUALQUER pergunta, siga estes passos:

PASSO 1 - ANÁLISE:
- Tipo de pergunta: consulta de dados ou conceito teórico?
- Dados necessários: marca? calibre? tipo de ocorrência?

PASSO 2 - BUSCA (se precisar de dados):
- Tool escolhida: [nome da ferramenta]
- Parâmetros: [valores a serem passados]
- Executar tool

PASSO 3 - RESULTADO:
- Valores obtidos: [números exatos]
- Validação: resultado faz sentido? (não é zero, não é absurdo)

PASSO 4 - RESPOSTA FINAL:
- Conclusão clara e objetiva
- Sempre citar: "Fonte: SINARM OCORRENCIAS_2026.csv"
- Linguagem técnica PCDF

=== INSTRUÇÕES ===

- Use terminologia técnica da PCDF
- Sempre mostre seu raciocínio (PASSO 1, 2, 3, 4)
- Seja preciso com números (não arredonde)
- Sempre cite a fonte dos dados
"""

agente = initialize_agent(
    tools=[
        contar_armas_marca,
        contar_armas_calibre,
        contar_armas_tipo,
        contar_armas_combinado
    ],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"system_message": system_message}
)


# ============================================================
# INTERFACE INTERATIVA
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 AGENTE SINARM v2.0 COMPLETO")
    print("="*60)
    print("\nRecursos:")
    print("✅ 4 Tools SINARM (@tool decorator)")
    print("✅ Cache (@lru_cache)")
    print("✅ Few-Shot Learning (3 exemplos)")
    print("✅ Chain-of-Thought (4 passos)")
    print("✅ Validação de Segurança")
    print("="*60 + "\n")
    
    # Teste de segurança
    print("TESTE DE SEGURANÇA:")
    print("-"*60)
    
    print("\n1️⃣ Pergunta normal:")
    print(perguntar_agente_seguro("Quantas Taurus?"))
    
    print("\n2️⃣ SQL Injection (bloqueado):")
    print(perguntar_agente_seguro("Taurus'; DROP TABLE--"))
    
    print("\n3️⃣ Query muito longa (bloqueada):")
    print(perguntar_agente_seguro("A" * 600))
    
    print("\n" + "="*60)
    
    # Modo interativo
    print("\nMODO INTERATIVO:")
    print("Digite suas perguntas (ou 'sair' para encerrar)")
    print("="*60 + "\n")
    
    while True:
        pergunta = input("❓ Sua pergunta: ")
        
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            print("\n👋 Até logo!")
            break
        
        if not pergunta.strip():
            continue
        
        resposta = perguntar_agente_seguro(pergunta)
        print(f"\n💬 {resposta}\n")
        print("-"*60 + "\n")
