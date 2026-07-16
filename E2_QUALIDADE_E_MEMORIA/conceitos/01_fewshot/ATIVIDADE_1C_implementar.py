"""
ATIVIDADE 1C: IMPLEMENTAR FEW-SHOT NO AGENTE
Encontro 2 - Conceito: Few-Shot Learning
Duração: 25 minutos

OBJETIVO:
Adicionar Few-Shot Learning ao agente v1.8, transformando-o em v2.0.
Usar os exemplos criados na Atividade 1B para melhorar a performance.

O QUE VOCÊ VAI FAZER:
1. Carregar exemplos Few-Shot do JSON (Atividade 1B)
2. Formatar exemplos no prompt system do agente
3. Integrar ao AgentExecutor (LangChain)
4. Testar o agente v2.0 com Few-Shot
5. Comparar com v1.8 (baseline)

POR QUE ISSO É IMPORTANTE:
- Aprende técnica MAIS USADA para melhorar LLMs em produção
- Few-Shot é barato (sem fine-tuning) e rápido (sem treino)
- Melhora 15-30% accuracy com apenas 3-5 exemplos
- Aplicável a QUALQUER tarefa (não só SINARM)

CONCEITO: Como Few-Shot Funciona
┌─────────────────────────────────────────────────────────────┐
│ PROMPT ZERO-SHOT (v1.8 - SEM EXEMPLOS)                     │
├─────────────────────────────────────────────────────────────┤
│ System: Você é um agente que consulta dados SINARM.        │
│         Use as tools disponíveis: buscar_ocorrencias, ...   │
│                                                              │
│ User: Quantas pistolas Taurus foram furtadas no DF?        │
│                                                              │
│ → LLM TEM QUE ADIVINHAR como usar as tools                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROMPT FEW-SHOT (v2.0 - COM EXEMPLOS)                      │
├─────────────────────────────────────────────────────────────┤
│ System: Você é um agente que consulta dados SINARM.        │
│         Use as tools disponíveis: buscar_ocorrencias, ...   │
│                                                              │
│ EXEMPLOS (Few-Shot):                                        │
│   Exemplo 1:                                                 │
│     User: Quantas pistolas Glock foram furtadas no DF?      │
│     Thought: Preciso buscar OCORRENCIAS...                   │
│     Action: buscar_ocorrencias("marca:Glock")                │
│     Output: Foram encontradas 23 pistolas Glock...          │
│                                                              │
│   Exemplo 2: ...                                             │
│   Exemplo 3: ...                                             │
│                                                              │
│ User: Quantas pistolas Taurus foram furtadas no DF?        │
│                                                              │
│ → LLM APRENDE POR ANALOGIA (imita os exemplos)             │
└─────────────────────────────────────────────────────────────┘

ARQUITETURA v2.0:
┌─────────────────────────────────────────────────────────────┐
│ 1. CARREGAR EXEMPLOS                                        │
│    exemplos_fewshot.json → lista de dicts                   │
├─────────────────────────────────────────────────────────────┤
│ 2. FORMATAR PROMPT                                          │
│    system_prompt = base_prompt + format_exemplos(exemplos)  │
├─────────────────────────────────────────────────────────────┤
│ 3. CRIAR AGENTE                                             │
│    agent = create_react_agent(llm, tools, system_prompt)    │
├─────────────────────────────────────────────────────────────┤
│ 4. EXECUTAR                                                 │
│    agent.invoke(user_query) → resposta melhorada            │
└─────────────────────────────────────────────────────────────┘
"""

import sys
from pathlib import Path
import json

# Ajustar path para importar utils
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from utils.tools_sinarm import buscar_ocorrencias, buscar_portes, buscar_registros, buscar_requerimentos

# LangChain imports
from langchain_aws import ChatBedrock
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# ========== CONFIGURAÇÃO BEDROCK ==========

llm = ChatBedrock(
    model_id="anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    model_kwargs={
        "temperature": 0.0,  # Determinístico (importante para comparação)
        "max_tokens": 4096
    }
)

# ========== CARREGAR EXEMPLOS FEW-SHOT ==========

def carregar_exemplos():
    """Carrega exemplos Few-Shot do JSON (Atividade 1B)."""
    
    caminho = Path(__file__).parent / "exemplos_fewshot.json"
    
    if not caminho.exists():
        print(f"⚠️  Arquivo {caminho} não encontrado!")
        print("   Execute ATIVIDADE_1B_criar_exemplos.py primeiro.")
        return []
    
    with open(caminho, "r", encoding="utf-8") as f:
        exemplos = json.load(f)
    
    print(f"✅ {len(exemplos)} exemplos carregados de {caminho}")
    return exemplos

# ========== FORMATAR EXEMPLOS NO PROMPT ==========

def formatar_exemplos_fewshot(exemplos):
    """
    Formata exemplos Few-Shot para inserir no prompt system.
    
    Formato:
    EXEMPLO 1:
    User: {input}
    Thought: {thought}
    Action: {action}
    Observation: {observation}
    Answer: {output}
    """
    
    if not exemplos:
        return ""
    
    texto_exemplos = "\n\n## 📚 EXEMPLOS (Few-Shot Learning)\n\n"
    texto_exemplos += "Aqui estão exemplos de como você deve responder:\n\n"
    
    for ex in exemplos:
        texto_exemplos += f"### EXEMPLO {ex['id']}:\n"
        texto_exemplos += f"**User Query:** {ex['input']}\n\n"
        texto_exemplos += f"**Thought:** {ex['thought']}\n\n"
        texto_exemplos += f"**Action:** {ex['action']}\n\n"
        
        if ex.get('observation'):
            texto_exemplos += f"**Observation:** {ex['observation']}\n\n"
        
        texto_exemplos += f"**Answer:** {ex['output']}\n\n"
        texto_exemplos += "---\n\n"
    
    texto_exemplos += "Agora responda a query do usuário seguindo o mesmo padrão:\n\n"
    
    return texto_exemplos

# ========== PROMPT SYSTEM v2.0 (FEW-SHOT) ==========

def criar_prompt_v2_fewshot(exemplos):
    """Cria prompt system v2.0 com Few-Shot."""
    
    base_prompt = """Você é um agente especializado em consultar dados do SINARM (Sistema Nacional de Armas).

## 🎯 SUA MISSÃO
Responder perguntas sobre armas de fogo no Brasil usando 4 datasets:
1. OCORRENCIAS (74.758 registros) - Furtos, apreensões, recuperações
2. PORTES (2.328 registros) - Portes de armas válidos/vencidos
3. REGISTROS (12.798 registros) - Registros de armas para defesa pessoal
4. REQUERIMENTOS (46.116 registros) - Requerimentos de porte/registro

## 🛠️ TOOLS DISPONÍVEIS
{tools}

## 📋 FORMATO DE RESPOSTA (ReAct)
Use SEMPRE este formato:

Thought: [seu raciocínio sobre qual dataset e campos usar]
Action: [nome_da_tool]
Action Input: [query no formato "campo:valor"]
Observation: [resultado da tool]
... (repita Thought/Action/Observation quantas vezes necessário)
Thought: Agora sei a resposta final
Final Answer: [resposta completa, formatada, com fonte citada]

## ⚠️ REGRAS IMPORTANTES
1. Use formato "campo:valor" (ex: "marca:Taurus", "status:Válido")
2. Cite SEMPRE a fonte (ex: "Fonte: SINARM/OCORRENCIAS")
3. Se não encontrar dados, diga claramente "Não há dados..."
4. Não invente números - use apenas os dados retornados pelas tools
5. Remova campo "idade" se aparecer (conformidade LGPD)
"""
    
    # Adicionar exemplos Few-Shot
    texto_exemplos = formatar_exemplos_fewshot(exemplos)
    prompt_completo = base_prompt + texto_exemplos
    
    # Template LangChain
    template = prompt_completo + """
{agent_scratchpad}"""
    
    return PromptTemplate(
        template=template,
        input_variables=["tools", "agent_scratchpad"]
    )

# ========== CRIAR AGENTE v2.0 (FEW-SHOT) ==========

def criar_agente_v2_fewshot(exemplos):
    """Cria agente v2.0 com Few-Shot Learning."""
    
    # Tools disponíveis
    tools = [
        buscar_ocorrencias,
        buscar_portes,
        buscar_registros,
        buscar_requerimentos
    ]
    
    # Prompt com Few-Shot
    prompt = criar_prompt_v2_fewshot(exemplos)
    
    # Criar agente ReAct
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    
    return agent_executor

# ========== TESTE ==========

def testar_agente_v2():
    """Testa agente v2.0 com Few-Shot."""
    
    print("\n" + "="*70)
    print("TESTANDO AGENTE v2.0 (FEW-SHOT)")
    print("="*70)
    
    # Carregar exemplos
    exemplos = carregar_exemplos()
    
    if not exemplos:
        print("❌ Sem exemplos Few-Shot. Execute ATIVIDADE_1B primeiro.")
        return
    
    # Criar agente
    print("\n🔧 Criando agente v2.0 com Few-Shot...")
    agente = criar_agente_v2_fewshot(exemplos)
    print("✅ Agente criado!")
    
    # Query de teste
    query_teste = "Quantas pistolas Taurus calibre .380 foram furtadas no DF?"
    
    print(f"\n📝 Query de teste: {query_teste}")
    print("\n⏳ Executando...")
    
    try:
        resultado = agente.invoke({"input": query_teste})
        
        print("\n" + "="*70)
        print("RESULTADO v2.0 (FEW-SHOT)")
        print("="*70)
        print(resultado["output"])
        print("\n✅ Teste concluído!")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")

# ========== MAIN ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  ATIVIDADE 1C: IMPLEMENTAR FEW-SHOT NO AGENTE                ║
║  Encontro 2 - Few-Shot Learning                              ║
╚═══════════════════════════════════════════════════════════════╝

INSTRUÇÕES:
1. Certifique-se que executou ATIVIDADE_1B (exemplos criados)
2. Este script vai:
   - Carregar seus exemplos Few-Shot
   - Criar agente v2.0 com exemplos integrados
   - Testar com query complexa
   - Comparar com baseline (v1.8)

ARQUITETURA v2.0:
- Base: Agente v1.8 (ReAct + 4 tools SINARM)
- Novo: Few-Shot Learning (3 exemplos no prompt)
- Resultado esperado: +15-30% accuracy

PRÓXIMO PASSO: ATIVIDADE_1D - Comparar v1.8 vs v2.0 com métricas
""")
    
    input("Pressione ENTER para começar o teste...")
    
    testar_agente_v2()
    
    print("\n✅ PRÓXIMO PASSO: ATIVIDADE_1D - Comparar v1.8 vs v2.0")
    print("   Você vai medir o impacto do Few-Shot com métricas objetivas.\n")
