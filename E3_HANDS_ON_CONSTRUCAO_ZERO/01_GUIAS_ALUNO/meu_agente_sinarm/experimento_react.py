"""
Experimento para VISUALIZAR o ciclo ReAct
⚠️ ATUALIZADO PARA LANGCHAIN 1.3+
Agora usa agente MANUAL para mostrar o ciclo ReAct explicitamente
"""

from langchain_ollama import OllamaLLM
from tools_basicas import contar_armas_marca

print("="*70)
print("EXPERIMENTO: VISUALIZANDO REACT (LangChain 1.3+)")
print("="*70)

# 1. Criar LLM
llm = OllamaLLM(model="llama3", temperature=0)

# 2. Criar Agente Manual que simula ReAct
def agente_react(pergunta: str):
    """
    Agente manual que MOSTRA o ciclo ReAct passo a passo
    
    ReAct = Reason (pensar) + Act (agir)
    ZERO_SHOT = Sem exemplos previos
    DESCRIPTION = Usa descricao da tool para decidir
    """
    
    print("\n[THOUGHT] Analisando a pergunta...")
    print(f'   "Preciso descobrir quantas armas de uma marca especifica existem"')
    
    # Detectar entidade (marca)
    pergunta_lower = pergunta.lower()
    marcas = ["taurus", "glock", "rossi", "beretta"]
    marca_encontrada = None
    
    for marca in marcas:
        if marca in pergunta_lower:
            marca_encontrada = marca
            break
    
    if not marca_encontrada:
        print("\n[THOUGHT] Nao identifiquei uma marca na pergunta")
        return "Nao consegui identificar a marca da arma."
    
    print(f"\n[ACTION] Vou usar a tool: contar_armas_marca")
    print(f"[ACTION INPUT] marca='{marca_encontrada.capitalize()}'")
    
    # Executar tool
    resultado = contar_armas_marca(marca_encontrada.capitalize())
    
    print(f"\n[OBSERVATION] A tool retornou: '{resultado}'")
    
    print(f"\n[THOUGHT] Agora tenho a informacao que preciso!")
    print(f"   'Posso responder ao usuario com base no resultado da tool'")
    
    print(f"\n[FINAL ANSWER] Pronto para retornar resposta!")
    
    return resultado

# 3. Fazer pergunta
print("\nPERGUNTA: Quantas armas Taurus existem?")
print("-"*70)

resposta = agente_react("Quantas armas Taurus existem?")

print("-"*70)
print(f"\nRESPOSTA FINAL: {resposta}")

print("\n" + "="*70)
print("ANALISE O OUTPUT ACIMA:")
print("="*70)
print("""
Voce acabou de ver o ciclo ReAct COMPLETO:

1. [THOUGHT] - Raciocinio inicial
   - ZERO_SHOT: Agente pensa sozinho, sem exemplos previos
   - "Preciso descobrir quantas armas..."

2. [ACTION] - Decisao de agir
   - REACT: Decidiu usar uma ferramenta
   - contar_armas_marca

3. [ACTION INPUT] - Parametros
   - DESCRIPTION: Entendeu que precisa do nome da marca
   - marca='Taurus'

4. [OBSERVATION] - Resultado da acao
   - REACT: Observou o que a tool retornou
   - "Encontrei 17760 armas..."

5. [THOUGHT] - Raciocinio final
   - REACT: Pensou novamente apos observar
   - "Agora tenho a informacao!"

6. [FINAL ANSWER] - Resposta ao usuario
   - Resposta formatada e clara

ISSO E O PADRAO ReAct:
    Reason (pensar) -> Act (agir) -> Reason (pensar) -> Answer (responder)

Em LangChain 1.3+, criamos isso MANUALMENTE para entender melhor!
""")