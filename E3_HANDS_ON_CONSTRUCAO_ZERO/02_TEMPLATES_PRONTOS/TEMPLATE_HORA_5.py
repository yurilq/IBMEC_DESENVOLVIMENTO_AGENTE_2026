# TEMPLATE_HORA_5.py
# AGENTE SINARM v2.0 COMPLETO
# Código de referência para Parte 5: Few-Shot + CoT + Security
# CÓDIGO FINAL COMPLETO DA AULA
#
# ⚠️ ATUALIZADO PARA LANGCHAIN 1.3+
# Usa agente MANUAL com Few-Shot e Chain-of-Thought

import pandas as pd
from functools import lru_cache
from langchain_core.tools import tool
import re

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
        
        # Executar agente manual
        resposta = agente_v3_fewshot_cot(pergunta)
        return resposta
        
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
        calibre: Calibre da arma (ex: .38, 9mm, .40)
    """
    df = carregar_csv()
    # Limpar espaços e usar contains (mais robusto)
    df["CALIBRE_ARMA"] = df["CALIBRE_ARMA"].str.strip()
    resultado = df[df["CALIBRE_ARMA"].str.contains(calibre, case=False, na=False)]
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
# AGENTE v3.0 COM FEW-SHOT + CHAIN-OF-THOUGHT (LangChain 1.3+)
# ============================================================

def agente_v3_fewshot_cot(pergunta_usuario):
    """Agente v3.0 com Few-Shot + Chain-of-Thought + detecção conceitual"""
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*60)
    
    pergunta_lower = pergunta_usuario.lower()
    
    # FEW-SHOT: Base de conhecimento para perguntas CONCEITUAIS
    palavras_conceituais = ["o que eh", "o que e", "define", "explique", "diferenca", "diferença"]
    palavras_quantidade = ["quantas", "quanto", "total", "existem"]
    
    eh_conceitual = any(p in pergunta_lower for p in palavras_conceituais)
    pede_quantidade = any(p in pergunta_lower for p in palavras_quantidade)
    
    # CHAIN-OF-THOUGHT - PASSO 1: Detectar tipo de pergunta
    if eh_conceitual and not pede_quantidade:
        print("[CHAIN-OF-THOUGHT]")
        print("PASSO 1: Pergunta CONCEITUAL (não precisa de dados)")
        print("PASSO 2: Consultar base de conhecimento (Few-Shot)")
        
        # FEW-SHOT: Exemplos pré-definidos
        respostas = {
            "bo": "BO (Boletim de Ocorrência) é o registro policial de um crime. No SINARM documenta ocorrências com armas de fogo.",
            "furto": "Furto é apropriação de bem SANS violência ou ameaça. Registrado no SINARM como 'Furto de Arma de Fogo'.",
            "roubo": "Roubo é apropriação de bem COM violência ou ameaça. Registrado no SINARM como 'Roubo de Arma de Fogo'.",
            "calibre": "Calibre é o diâmetro interno do cano da arma. Exemplos: .38 (9mm), 9mm, .40 (10mm), .380 (9mm curto).",
            "sinarm": "SINARM (Sistema Nacional de Armas) é o banco de dados da Polícia Federal que registra armas de fogo no Brasil.",
            "apreens": "Apreensão é o ato de polícia retirar arma de circulação. Registrada no SINARM como 'Apreensão de Arma de Fogo'.",
            "pcdf": "PCDF (Polícia Civil do Distrito Federal) é órgão responsável por investigação criminal no DF.",
        }
        
        for topico, resposta in respostas.items():
            if topico in pergunta_lower:
                print(f"PASSO 3: Conceito encontrado = '{topico}'")
                print(f"PASSO 4: Retornar explicação")
                return resposta
        
        return "Não tenho informação sobre esse conceito na base de conhecimento."
    
    # CHAIN-OF-THOUGHT - PASSO 1: Pergunta sobre DADOS
    print("[CHAIN-OF-THOUGHT]")
    print("PASSO 1: Pergunta sobre DADOS (precisa consultar CSV)")
    
    # Detectar entidades (marca, calibre, tipo)
    marcas = ["taurus", "glock", "rossi", "beretta"]
    marca_encontrada = None
    for marca in marcas:
        if marca in pergunta_lower:
            marca_encontrada = marca.capitalize()
            break
    
    calibres = [".38", "9mm", ".40", ".380"]
    calibre_encontrado = None
    for calibre in calibres:
        if calibre in pergunta_lower:
            calibre_encontrado = calibre
            break
    
    tipos = {"apreens": "Apreens", "roubo": "Roubo", "furto": "Furto"}
    tipo_encontrado = None
    for palavra, tipo in tipos.items():
        if palavra in pergunta_lower:
            tipo_encontrado = tipo
            break
    
    # PASSO 2: Selecionar tool
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
    
    if not tool_escolhida:
        return "Não consegui identificar sobre o que você quer consultar."
    
    print(f"PASSO 2: Tool escolhida = {tool_escolhida.name}")
    print(f"PASSO 3: Parâmetros = {parametros}")
    print(f"PASSO 4: Executando tool...")
    
    # PASSO 3: Executar tool
    resultado_tool = tool_escolhida.func(**parametros)
    
    print(f"PASSO 5: Resultado = {resultado_tool}")
    print(f"PASSO 6: Formatando resposta final...")
    
    # PASSO 4: Extrair número e formatar resposta
    numeros = re.findall(r'\d+', resultado_tool)
    total = numeros[0] if numeros else "?"
    
    # Formatar resposta com contexto
    if marca_encontrada and tipo_encontrado:
        resposta_final = f"Segundo o SINARM 2026, existem {total} armas {marca_encontrada} do tipo {tipo_encontrado}. (Fonte: OCORRENCIAS_2026.csv)"
    elif marca_encontrada:
        resposta_final = f"Segundo o SINARM 2026, existem {total} armas da marca {marca_encontrada}. (Fonte: OCORRENCIAS_2026.csv)"
    elif calibre_encontrado:
        resposta_final = f"Segundo o SINARM 2026, existem {total} armas calibre {calibre_encontrado}. (Fonte: OCORRENCIAS_2026.csv)"
    elif tipo_encontrado:
        resposta_final = f"Segundo o SINARM 2026, foram registradas {total} ocorrências do tipo {tipo_encontrado}. (Fonte: OCORRENCIAS_2026.csv)"
    else:
        resposta_final = resultado_tool
    
    return resposta_final

# ============================================================
# TESTES E DEMONSTRAÇÃO
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 AGENTE SINARM v3.0 COMPLETO (LangChain 1.3+)")
    print("="*60)
    print("\nRecursos:")
    print("✅ 4 Tools SINARM (@tool decorator)")
    print("✅ Cache (@lru_cache)")
    print("✅ Few-Shot Learning (7 conceitos)")
    print("✅ Chain-of-Thought (6 passos visíveis)")
    print("✅ Validação de Segurança")
    print("✅ Detecção Conceitual vs Dados")
    print("="*60 + "\n")
    
    # Teste automatizado
    print("TESTES AUTOMATIZADOS:")
    print("-"*60)
    
    testes = [
        "Quantas armas Taurus?",
        "O que é BO de furto?",
        "Quantas armas calibre .38?",
        "Explique diferença entre roubo e furto"
    ]
    
    for i, teste in enumerate(testes, 1):
        print(f"\n{i}️⃣ TESTE {i}: {teste}")
        print("="*60)
        resposta = perguntar_agente_seguro(teste)
        print(f"\n💬 RESPOSTA: {resposta}\n")
    
    # Teste de segurança
    print("\n" + "="*60)
    print("TESTE DE SEGURANÇA:")
    print("="*60)
    
    print("\n🔒 SQL Injection (deve bloquear):")
    print(perguntar_agente_seguro("Taurus'; DROP TABLE--"))
    
    print("\n🔒 Query muito longa (deve bloquear):")
    print(perguntar_agente_seguro("A" * 600))
    
    print("\n" + "="*60)
    print("ESTATÍSTICAS DO CACHE:")
    print("="*60)
    print(carregar_csv.cache_info())
    print("hits = vezes que usou cache (rápido)")
    print("misses = vezes que leu CSV (lento)")
    
    print("\n" + "="*60)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("="*60)
    
    # Modo interativo (opcional)
    print("\n🎮 Quer testar manualmente?")
    resposta = input("Digite 's' para modo interativo ou Enter para sair: ")
    
    if resposta.lower() == 's':
        print("\n" + "="*60)
        print("MODO INTERATIVO:")
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
    else:
        print("\n👋 Até logo!")
