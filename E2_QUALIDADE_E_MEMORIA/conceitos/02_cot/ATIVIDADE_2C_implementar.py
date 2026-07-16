"""
ATIVIDADE 2C: IMPLEMENTAR COT NO AGENTE v2.5
Encontro 2 - Conceito: Chain-of-Thought (CoT)
Duração: 20 minutos

OBJETIVO:
Adicionar Chain-of-Thought ao agente v2.0 (Few-Shot), transformando-o em v2.5.
Usar template CoT para forçar raciocínio explícito em queries complexas.

O QUE VOCÊ VAI FAZER:
1. Carregar template CoT estruturado
2. Integrar template ao prompt system
3. Adicionar exemplos Few-Shot+CoT
4. Criar agente v2.5 (Few-Shot + CoT)
5. Testar com query complexa

POR QUE ISSO É IMPORTANTE:
- CoT melhora accuracy em queries complexas de 70% → 90%
- Raciocínio explícito permite debugging (ver onde agente errou)
- CoT + Few-Shot = combinação poderosa (melhora aditiva)
- Técnica usada em produção (ChatGPT, Claude, Gemini)

CONCEITO: Few-Shot vs Few-Shot+CoT

┌──────────────────────────────────────────────────────────────┐
│ FEW-SHOT (v2.0) - Raciocínio Implícito                      │
├──────────────────────────────────────────────────────────────┤
│ EXEMPLO:                                                      │
│   User: Quantas Taurus foram furtadas no DF?                │
│   Action: buscar_ocorrencias("marca:Taurus")                │
│   Answer: 47 pistolas Taurus furtadas no DF.                │
│                                                              │
│ ❌ PROBLEMA: Não mostra COMO chegou na resposta             │
│ ❌ Dificulta debugging se resposta estiver errada           │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ FEW-SHOT + COT (v2.5) - Raciocínio Explícito                │
├──────────────────────────────────────────────────────────────┤
│ EXEMPLO:                                                      │
│   User: Quantas Taurus foram furtadas no DF?                │
│                                                              │
│   Thought: Preciso buscar OCORRENCIAS com filtros:          │
│            marca=Taurus, tipo=Furto, uf=DF                  │
│                                                              │
│   Action: buscar_ocorrencias("marca:Taurus")                │
│                                                              │
│   Observation: 1.247 registros Taurus. Filtrando tipo=Furto │
│                e uf=DF resulta em 47 ocorrências.           │
│                                                              │
│   Answer: 47 pistolas Taurus foram furtadas no DF em 2026.  │
│           Fonte: SINARM/OCORRENCIAS.                         │
│                                                              │
│ ✅ VANTAGEM: Raciocínio transparente                        │
│ ✅ Debugging fácil (ver qual etapa falhou)                  │
│ ✅ Accuracy +10-20pp em queries complexas                   │
└──────────────────────────────────────────────────────────────┘

ARQUITETURA v2.5:
┌──────────────────────────────────────────────────────────────┐
│ 1. TEMPLATE COT                                              │
│    Força estrutura: Thought → Action → Observation → Answer │
├──────────────────────────────────────────────────────────────┤
│ 2. EXEMPLOS FEW-SHOT+COT                                     │
│    3-5 exemplos com raciocínio explícito                    │
├──────────────────────────────────────────────────────────────┤
│ 3. PROMPT SYSTEM v2.5                                        │
│    base_prompt + template_cot + exemplos_fewshot_cot        │
├──────────────────────────────────────────────────────────────┤
│ 4. AGENTE                                                    │
│    create_react_agent(llm, tools, prompt_v2.5)              │
└──────────────────────────────────────────────────────────────┘
"""

import sys
from pathlib import Path
import json

# Ajustar path
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
        "temperature": 0.0,
        "max_tokens": 4096
    }
)

# ========== TEMPLATE COT ==========

TEMPLATE_COT = """
## 🧠 CHAIN-OF-THOUGHT (CoT) - RACIOCÍNIO PASSO-A-PASSO

Para queries COMPLEXAS (múltiplos datasets, cálculos, comparações), use este formato:

**THOUGHT (Pensamento):**
Explique sua estratégia:
- Qual dataset preciso? Por quê?
- Quais filtros são necessários?
- Quais cálculos farei?
- Quantas etapas preciso?

**ACTION (Ação):**
Execute uma tool específica:
buscar_[dataset]("campo:valor")

**OBSERVATION (Observação):**
Registre o que a tool retornou:
- Quantos registros?
- Valores relevantes?
- Dados suficientes para responder?

**[REPETIR Thought→Action→Observation se precisar mais dados]**

**FINAL ANSWER (Resposta Final):**
Quando tiver todos os dados necessários, formate a resposta:
- Clara e precisa
- Com números exatos
- Cite a fonte (SINARM/[dataset])
- Explique cálculos se relevante

---

**IMPORTANTE:**
- Queries SIMPLES (1 dataset, 1-2 filtros): responda direto (sem CoT)
- Queries COMPLEXAS (2+ datasets, cálculos): USE CoT obrigatoriamente
"""

# ========== EXEMPLOS FEW-SHOT + COT ==========

EXEMPLOS_FEWSHOT_COT = [
    {
        "id": 1,
        "query": "Qual a taxa de aprovação de requerimentos de porte no DF?",
        "complexidade": "MÉDIA",
        "trace": """
**THOUGHT:**
Preciso calcular: (requerimentos aprovados / total requerimentos) * 100
Dataset: REQUERIMENTOS
Filtros: tipo_requerimento=Porte, uf=DF, decisao=Aprovado
Etapas:
1. Buscar requerimentos aprovados (porte, DF)
2. Buscar total de requerimentos (porte, DF)
3. Calcular percentual

**ACTION:**
buscar_requerimentos("tipo_requerimento:Porte")

**OBSERVATION:**
Retornou 28.456 requerimentos de porte. Filtrando uf=DF: 3.847 totais.
Destes, decisao=Aprovado: 2.312 aprovados.

**THOUGHT:**
Agora posso calcular a taxa:
Taxa = (2.312 / 3.847) * 100 = 60,1%

**FINAL ANSWER:**
A taxa de aprovação de requerimentos de porte no DF é 60,1%.
Foram aprovados 2.312 de 3.847 requerimentos totais em 2026.
Fonte: SINARM/REQUERIMENTOS.
"""
    },
    {
        "id": 2,
        "query": "Compare a proporção de pistolas vs revólveres em portes válidos e registros ativos.",
        "complexidade": "COMPLEXA",
        "trace": """
**THOUGHT:**
Query complexa - preciso cruzar 2 datasets:
1. PORTES (status=Válido) → contar pistolas vs revólveres
2. REGISTROS (status=Ativo) → contar pistolas vs revólveres
3. Calcular proporção em cada dataset
4. Comparar

Começando com PORTES...

**ACTION:**
buscar_portes("status:Válido")

**OBSERVATION:**
1.856 portes válidos encontrados.
Filtrando por espécie:
  - Pistola: 1.423 (76,7%)
  - Revólver: 433 (23,3%)

Proporção PORTES: 76,7% pistolas / 23,3% revólveres

Agora busco REGISTROS...

**THOUGHT:**
Preciso dos mesmos dados para REGISTROS.

**ACTION:**
buscar_registros("status:Ativo")

**OBSERVATION:**
9.847 registros ativos encontrados.
Filtrando por espécie:
  - Pistola: 6.789 (68,9%)
  - Revólver: 3.058 (31,1%)

Proporção REGISTROS: 68,9% pistolas / 31,1% revólveres

**THOUGHT:**
Agora posso comparar:
- PORTES: 76,7% pistolas (maior preferência)
- REGISTROS: 68,9% pistolas
- Diferença: +7,8pp mais pistolas em PORTES

**FINAL ANSWER:**
Comparação pistolas vs revólveres:

PORTES VÁLIDOS:
  • Pistolas: 1.423 (76,7%)
  • Revólveres: 433 (23,3%)

REGISTROS ATIVOS:
  • Pistolas: 6.789 (68,9%)
  • Revólveres: 3.058 (31,1%)

ANÁLISE: Pistolas predominam em ambos os casos, mas são 7,8 pontos percentuais
mais comuns em PORTES (76,7%) do que em REGISTROS (68,9%).

Fonte: SINARM/PORTES + SINARM/REGISTROS.
"""
    },
    {
        "id": 3,
        "query": "Quantas pistolas Taurus calibre .380 foram furtadas no DF?",
        "complexidade": "ALTA",
        "trace": """
**THOUGHT:**
Query com múltiplos filtros:
Dataset: OCORRENCIAS
Filtros: marca=Taurus, especie=Pistola, calibre=.380, tipo=Furto, uf=DF

Como buscar_ocorrencias aceita 1 campo por vez, estratégia:
1. Buscar marca:Taurus
2. Filtrar manualmente: especie, calibre, tipo, uf

**ACTION:**
buscar_ocorrencias("marca:Taurus")

**OBSERVATION:**
1.247 ocorrências de Taurus encontradas.
Aplicando filtros manuais:
  - especie=Pistola: 892 registros
  - calibre=.380: 347 registros
  - tipo=Furto: 289 registros
  - uf=DF: 47 registros finais

**FINAL ANSWER:**
Foram encontradas 47 pistolas Taurus calibre .380 furtadas no DF em 2026.
Fonte: SINARM/OCORRENCIAS (74.758 registros totais).
"""
    }
]

# ========== FORMATAR EXEMPLOS COT NO PROMPT ==========

def formatar_exemplos_cot(exemplos):
    """Formata exemplos Few-Shot+CoT para prompt."""
    
    texto = "\n\n## 📚 EXEMPLOS (Few-Shot + CoT)\n\n"
    texto += "Veja como aplicar Chain-of-Thought em queries de diferentes complexidades:\n\n"
    
    for ex in exemplos:
        texto += f"### EXEMPLO {ex['id']} (Complexidade: {ex['complexidade']})\n"
        texto += f"**User Query:** {ex['query']}\n\n"
        texto += ex['trace']
        texto += "\n\n---\n\n"
    
    texto += "Agora responda a query do usuário seguindo o MESMO padrão:\n"
    texto += "- Query SIMPLES: responda direto\n"
    texto += "- Query COMPLEXA: use CoT (Thought→Action→Observation→Answer)\n\n"
    
    return texto

# ========== CRIAR PROMPT v2.5 (FEW-SHOT + COT) ==========

def criar_prompt_v25_cot():
    """Cria prompt system v2.5 com Few-Shot + CoT."""
    
    base_prompt = """Você é um agente especializado em consultar dados do SINARM (Sistema Nacional de Armas).

## 🎯 SUA MISSÃO
Responder perguntas sobre armas de fogo no Brasil usando 4 datasets:
1. OCORRENCIAS (74.758 registros) - Furtos, apreensões, recuperações
2. PORTES (2.328 registros) - Portes de armas válidos/vencidos
3. REGISTROS (12.798 registros) - Registros de armas para defesa pessoal
4. REQUERIMENTOS (46.116 registros) - Requerimentos de porte/registro

## 🛠️ TOOLS DISPONÍVEIS
{tools}

## ⚠️ REGRAS IMPORTANTES
1. Use formato "campo:valor" (ex: "marca:Taurus", "status:Válido")
2. Cite SEMPRE a fonte (ex: "Fonte: SINARM/OCORRENCIAS")
3. Se não encontrar dados, diga claramente "Não há dados..."
4. Não invente números - use apenas os dados retornados pelas tools
5. Remova campo "idade" se aparecer (conformidade LGPD)
6. Para queries COMPLEXAS, use Chain-of-Thought (raciocínio explícito)
"""
    
    # Adicionar template CoT
    prompt_completo = base_prompt + TEMPLATE_COT
    
    # Adicionar exemplos Few-Shot+CoT
    prompt_completo += formatar_exemplos_cot(EXEMPLOS_FEWSHOT_COT)
    
    # Template LangChain
    template = prompt_completo + """
{agent_scratchpad}"""
    
    return PromptTemplate(
        template=template,
        input_variables=["tools", "agent_scratchpad"]
    )

# ========== CRIAR AGENTE v2.5 (FEW-SHOT + COT) ==========

def criar_agente_v25():
    """Cria agente v2.5 com Few-Shot + CoT."""
    
    # Tools
    tools = [
        buscar_ocorrencias,
        buscar_portes,
        buscar_registros,
        buscar_requerimentos
    ]
    
    # Prompt v2.5
    prompt = criar_prompt_v25_cot()
    
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
        max_iterations=15  # CoT pode precisar mais iterações
    )
    
    return agent_executor

# ========== TESTE ==========

def testar_agente_v25():
    """Testa agente v2.5 com query complexa."""
    
    print("\n" + "="*70)
    print("TESTANDO AGENTE v2.5 (FEW-SHOT + COT)")
    print("="*70)
    
    # Criar agente
    print("\n🔧 Criando agente v2.5...")
    agente = criar_agente_v25()
    print("✅ Agente v2.5 pronto!")
    
    # Query de teste (COMPLEXA - deve usar CoT)
    query_teste = "Qual a taxa de aprovação de requerimentos de porte no DF?"
    
    print(f"\n📝 Query de teste (COMPLEXA): {query_teste}")
    print("\n⏳ Executando...")
    print("\n" + "─"*70)
    print("TRACE CoT (observe o raciocínio passo-a-passo):")
    print("─"*70)
    
    try:
        resultado = agente.invoke({"input": query_teste})
        
        print("\n" + "="*70)
        print("RESULTADO v2.5 (FEW-SHOT + COT)")
        print("="*70)
        print(resultado["output"])
        print("\n✅ Teste concluído!")
        
        print("\n" + "="*70)
        print("ANÁLISE DO TRACE:")
        print("="*70)
        print("✓ O agente usou Thought (pensamento)?")
        print("✓ O agente executou Actions (ferramentas)?")
        print("✓ O agente registrou Observations (resultados)?")
        print("✓ O agente chegou a uma Final Answer (resposta)?")
        print("✓ O raciocínio foi lógico e sequencial?")
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")

# ========== SALVAR TEMPLATE COT ==========

def salvar_template_cot():
    """Salva template CoT em arquivo separado para reutilização."""
    
    caminho = Path(__file__).parent / "template_cot.txt"
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(TEMPLATE_COT)
    
    print(f"📄 Template CoT salvo em: {caminho}")

# ========== MAIN ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  ATIVIDADE 2C: IMPLEMENTAR COT NO AGENTE v2.5                ║
║  Encontro 2 - Chain-of-Thought (CoT)                         ║
╚═══════════════════════════════════════════════════════════════╝

INSTRUÇÕES:
1. Este script cria o agente v2.5 com Few-Shot + CoT
2. Teste com query complexa para ver CoT em ação
3. Observe o trace: Thought → Action → Observation → Answer
4. Compare mentalmente com v2.0 (sem CoT explícito)

ARQUITETURA v2.5:
- Base: v2.0 (ReAct + Few-Shot)
- Novo: Template CoT (raciocínio estruturado)
- Novo: Exemplos Few-Shot+CoT (3 exemplos)
- Resultado: Accuracy +10-20pp em queries complexas

PRÓXIMO: ATIVIDADE_2D - Avaliar quando CoT ajuda vs quando é overhead
""")
    
    # Salvar template CoT
    salvar_template_cot()
    
    input("\nPressione ENTER para testar agente v2.5...")
    
    testar_agente_v25()
    
    print("\n✅ PRÓXIMO PASSO: ATIVIDADE 2D - Avaliar Efetividade do CoT")
    print("   Você vai testar v2.5 em queries simples e complexas para medir quando CoT ajuda.\n")
