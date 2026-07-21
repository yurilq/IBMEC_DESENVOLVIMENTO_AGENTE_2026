"""
EXPERIMENTO: VISUALIZANDO REACT - LangChain 1.3+

Este experimento mostra o ciclo ReAct de forma visual e educativa.
Adaptado para funcionar com LangChain 1.3+ (sem initialize_agent).
"""

from langchain_ollama import OllamaLLM
from langchain_core.tools import Tool  # ← Import atualizado!
from tools_basicas import contar_armas_marca
import re

print("="*70)
print("EXPERIMENTO: VISUALIZANDO REACT (LangChain 1.3+)")
print("="*70)

# 1. Criar LLM
print("\n[Setup] Criando LLM...")
llm = OllamaLLM(model="llama3.2:1b", temperature=0)

# 2. Criar Tool
print("[Setup] Criando Tool...")
tool = Tool(
    name="contar_armas_marca",
    func=contar_armas_marca,
    description="Conta quantas armas de uma marca específica. Input: marca"
)

# 3. Implementar ReAct manualmente (para visualizar cada passo)
print("[Setup] Agente ReAct pronto!")

def agente_react_visual(pergunta_usuario):
    """
    Implementa ReAct com verbose MÁXIMO para fins educativos
    Mostra CADA PASSO do ciclo
    """
    
    print("\n" + "="*70)
    print("INICIANDO CICLO ReAct")
    print("="*70)
    
    # ========================================
    # PASSO 1: THOUGHT (Raciocínio inicial)
    # ========================================
    print("\n[PASSO 1/5] THOUGHT (Pensamento Inicial)")
    print("-"*70)
    print(f"Pergunta recebida: '{pergunta_usuario}'")
    print("Raciocínio: Preciso descobrir a quantidade de armas de uma marca.")
    print("Decisão: Vou identificar qual marca e usar a ferramenta de contagem.")
    
    # Detectar marca
    marcas = ["taurus", "glock", "rossi", "beretta", "smith"]
    marca_encontrada = None
    
    for marca in marcas:
        if marca in pergunta_usuario.lower():
            marca_encontrada = marca.capitalize()
            print(f"Marca identificada: {marca_encontrada}")
            break
    
    if not marca_encontrada:
        print("- ERRO: Marca não identificada")
        return "Não consegui identificar a marca na pergunta."
    
    # ========================================
    # PASSO 2: ACTION (Escolher ferramenta)
    # ========================================
    print("\n[PASSO 2/5] ACTION (Escolher Ferramenta)")
    print("-"*70)
    print(f"Ferramenta escolhida: {tool.name}")
    print(f"Descrição da tool: {tool.description}")
    print(f"Input para a tool: '{marca_encontrada}'")
    print("Executando tool...")
    
    # ========================================
    # PASSO 3: TOOL EXECUTION (Executar)
    # ========================================
    print("\n[PASSO 3/5] TOOL EXECUTION (Execução)")
    print("-"*70)
    
    try:
        resultado_tool = tool.func(marca_encontrada)
        print(f"[OK] Tool executada com sucesso")
    except Exception as e:
        print(f"[ERRO] Erro na execucao: {e}")
        return "Erro ao executar ferramenta"
    
    # ========================================
    # PASSO 4: OBSERVATION (Ver resultado)
    # ========================================
    print("\n[PASSO 4/5] OBSERVATION (Observação do Resultado)")
    print("-"*70)
    print(f"Resultado da tool: {resultado_tool}")
    
    # Extrair número
    numeros = re.findall(r'\d+', resultado_tool)
    total = numeros[0] if numeros else "?"
    print(f"Número extraído: {total}")
    
    # ========================================
    # PASSO 5: THOUGHT + FINAL ANSWER
    # ========================================
    print("\n[PASSO 5/5] THOUGHT + FINAL ANSWER (Resposta Final)")
    print("-"*70)
    print("Raciocínio: Tenho os dados necessários.")
    print("Decisão: Vou formatar uma resposta clara para o usuário.")
    print("Usando LLM para formatar...")
    
    prompt = f"""Dados do SINARM: {resultado_tool}

Tarefa: Responda de forma direta.
Exemplo: "Existem 17.760 armas Taurus."

Resposta:"""
    
    resposta_final = llm.invoke(prompt)
    
    print(f"Resposta formatada: {resposta_final}")
    
    print("\n" + "="*70)
    print("CICLO ReAct CONCLUÍDO!")
    print("="*70)
    
    return resposta_final

# 4. EXECUTAR EXPERIMENTO
print("\n" + "="*70)
print("EXECUTANDO EXPERIMENTO")
print("="*70)

pergunta = "Quantas armas Taurus existem?"
print(f"\nPergunta: {pergunta}")

resposta = agente_react_visual(pergunta)

print("\n" + "="*70)
print("RESULTADO FINAL")
print("="*70)
print(f"\n{resposta}\n")

# 5. ANÁLISE EDUCATIVA
print("="*70)
print("ANALISE O OUTPUT ACIMA - O QUE ACONTECEU:")
print("="*70)
print("""
Voce acabou de ver o ciclo ReAct COMPLETO em 5 passos:

PASSO 1: THOUGHT (Pensamento)
- Agente analisa a pergunta
- Decide que precisa de dados
- Identifica a marca mencionada
- ZERO_SHOT: Sem exemplos, decide sozinho!

PASSO 2: ACTION (Acao - Escolher Tool)
- Escolhe qual ferramenta usar
- DESCRIPTION: Leu a description da tool!
- Prepara input para a tool

PASSO 3: TOOL EXECUTION (Executar)
- Chama a funcao Python
- Consulta banco de dados SINARM
- Retorna resultado bruto

PASSO 4: OBSERVATION (Observacao)
- Agente VE o resultado da tool
- REACT: Observa o que aconteceu!
- Extrai informacao relevante

PASSO 5: THOUGHT + FINAL ANSWER (Resposta)
- Agente pensa: "Tenho dados suficientes?"
- REACT: Pensa novamente!
- Formata resposta clara ao usuario
- Retorna resposta final

CONCEITOS APLICADOS:

[OK] ZERO_SHOT: Agente decidiu sozinho (sem exemplos previos)
[OK] REACT: Alternou entre Reasoning (pensar) e Acting (agir)
[OK] DESCRIPTION: Usou description da tool para decidir

DIFERENCA vs LLM PURO:

[X] LLM sozinho: "Chutaria" ou diria "nao sei"
[OK] Agente ReAct: CONSULTOU DADOS REAIS e deu resposta precisa!

Isso e o poder de agentes!
""")

print("="*70)
print("EXPERIMENTO CONCLUIDO!")
print("="*70)
print("\nProximos passos:")
print("  1. Execute novamente com outra marca")
print("  2. Observe cada passo do ciclo")
print("  3. Entenda por que ReAct e poderoso")
print("  4. Continue para PARTE_3 (decorators)")

