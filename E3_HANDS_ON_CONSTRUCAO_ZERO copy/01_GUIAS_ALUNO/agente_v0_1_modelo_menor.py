# agente_v0_1_modelo_menor.py
# Versão com modelo menor (llama3.2:1b) para economizar RAM

from langchain_ollama import OllamaLLM
from tools_basicas import contar_armas_marca

print("="*60)
print("AGENTE COM MODELO MENOR (llama3.2:1b)")
print("="*60)

# PARTE 1: Criar LLM com modelo menor
print("\n1. Criando LLM com modelo menor...")
llm = OllamaLLM(model="llama3.2:1b", temperature=0)
print("   [OK] LLM criado")

# PARTE 2: Teste básico do LLM
print("\n2. Testando LLM...")
try:
    resposta_teste = llm.invoke("Responda apenas: OK")
    print(f"   [OK] LLM respondeu: {resposta_teste[:50]}...")
except Exception as e:
    print(f"   [ERRO] {e}")
    exit(1)

# PARTE 3: Testar tool diretamente
print("\n3. Testando tool diretamente...")
resultado_tool = contar_armas_marca("Taurus")
print(f"   [OK] Tool funcionou: {resultado_tool}")

# PARTE 4: Agente simples - LLM usa resultado da tool
print("\n4. Criando agente simples...")

def agente_simples_v2(pergunta_usuario):
    """Agente simplificado: executa tool e LLM formata resposta"""
    
    print(f"\n   Pergunta: {pergunta_usuario}")
    
    # Extrair marca da pergunta (simplificado)
    marcas_conhecidas = ["Taurus", "Glock", "Rossi", "Beretta", "Smith"]
    marca_encontrada = None
    
    for marca in marcas_conhecidas:
        if marca.lower() in pergunta_usuario.lower():
            marca_encontrada = marca
            break
    
    if not marca_encontrada:
        return "Não consegui identificar qual marca você quer consultar."
    
    # Executar tool
    print(f"   Consultando dados para: {marca_encontrada}")
    resultado_tool = contar_armas_marca(marca_encontrada)
    print(f"   Resultado da tool: {resultado_tool}")
    
    # LLM formata resposta final
    prompt = f"""Pergunta do usuário: {pergunta_usuario}

Dados obtidos do banco SINARM: {resultado_tool}

Responda ao usuário de forma clara e objetiva:"""
    
    print("   LLM formatando resposta...")
    resposta_final = llm.invoke(prompt)
    
    return resposta_final

print("   [OK] Agente criado")

# PARTE 5: Testar agente
print("\n" + "="*60)
print("TESTANDO AGENTE")
print("="*60)

perguntas = [
    "Quantas armas Taurus existem?",
    "Quantas Glock?",
]

for pergunta in perguntas:
    print(f"\n{'='*60}")
    print(f"PERGUNTA: {pergunta}")
    print("="*60)
    
    try:
        resposta = agente_simples_v2(pergunta)
        print(f"\nRESPOSTA FINAL:\n{resposta}")
    except Exception as e:
        print(f"\n[ERRO]: {e}")
    
    print()

print("="*60)
print("TESTES CONCLUÍDOS!")
print("="*60)
