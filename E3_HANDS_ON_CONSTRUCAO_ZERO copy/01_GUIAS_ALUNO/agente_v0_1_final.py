# agente_v0_1_final.py
# Versão final funcional com modelo menor e prompt melhorado

from langchain_ollama import OllamaLLM
from tools_basicas import contar_armas_marca

print("="*60)
print("AGENTE SINARM v0.1 - Modelo Menor")
print("="*60)

# Criar LLM com modelo menor
print("\n[1/3] Criando LLM...")
llm = OllamaLLM(model="llama3.2:1b", temperature=0)
print("      OK - LLM criado")

# Função agente simplificada
def agente_sinarm(pergunta_usuario):
    """Agente que consulta SINARM e responde perguntas sobre armas"""
    
    print(f"\n[2/3] Processando pergunta...")
    print(f"      '{pergunta_usuario}'")
    
    # Identificar marca na pergunta
    marcas_conhecidas = {
        "taurus": "Taurus",
        "glock": "Glock", 
        "rossi": "Rossi",
        "beretta": "Beretta",
        "smith": "Smith"
    }
    
    marca_encontrada = None
    for chave, marca in marcas_conhecidas.items():
        if chave in pergunta_usuario.lower():
            marca_encontrada = marca
            break
    
    if not marca_encontrada:
        return "Não identifiquei qual marca você quer consultar. Tente: Taurus, Glock, Rossi, Beretta ou Smith."
    
    # Consultar banco de dados
    print(f"      Consultando banco SINARM para: {marca_encontrada}")
    resultado_tool = contar_armas_marca(marca_encontrada)
    
    # Extrair número do resultado
    import re
    numeros = re.findall(r'\d+', resultado_tool)
    total = numeros[0] if numeros else "?"
    
    # LLM apenas formata a resposta (prompt mais direto)
    print(f"\n[3/3] Formatando resposta...")
    
    prompt = f"""Você é um assistente do sistema SINARM.

Dados obtidos: {resultado_tool}

Tarefa: Responda APENAS com o número e a marca, de forma direta.

Exemplo: "Existem 17.760 armas Taurus registradas no SINARM."

Sua resposta (seja breve e direto):"""
    
    resposta_final = llm.invoke(prompt)
    
    return resposta_final

print("      OK - Agente pronto")

# Testar
print("\n" + "="*60)
print("TESTANDO AGENTE")
print("="*60)

perguntas = [
    "Quantas armas Taurus existem?",
    "Quantas Glock?",
    "Quantas Rossi?"
]

for i, pergunta in enumerate(perguntas, 1):
    print(f"\n{'-'*60}")
    print(f"TESTE {i}: {pergunta}")
    print('-'*60)
    
    try:
        resposta = agente_sinarm(pergunta)
        print(f"\n[OK] RESPOSTA: {resposta}\n")
    except Exception as e:
        print(f"\n[ERRO] {e}\n")

print("="*60)
print("TESTES CONCLUÍDOS!")
print("="*60)
