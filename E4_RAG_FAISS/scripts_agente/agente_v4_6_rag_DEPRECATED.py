# agente_v4_6_rag_fewshot_cot.py
# Agente v4.6 COM RAG + FEW-SHOT + CHAIN-OF-THOUGHT
# EVOLUÇÃO: v4.5 → v4.6 (Aplica técnicas de E2 e E3 no RAG do E4)
# OBJETIVO: Melhorar de 81% para 95%+ de acurácia

"""
PROGRESSÃO:
v4.0 (E4):  RAG básico + Zero-Shot
v4.5 (E4):  RAG melhorado + Zero-Shot
v4.6 (E4):  RAG + Few-Shot + CoT ← VOCÊ ESTÁ AQUI

MUDANÇAS em relação ao v4.5:
1. FEW_SHOT_EXAMPLES: 5 exemplos completos (input → análise → output)
2. COT_TEMPLATE: 4 etapas obrigatórias (Pensamento → Ação → Observação → Resposta)
3. Prompt melhorado: Agora força raciocínio estruturado
4. Melhoria esperada: 81% → 95%+ de acurácia

PRÉ-REQUISITO:
- config_llm.py (Multi-LLM)
- tools_basicas_v2.py (4 Tools)
- tool_rag_conceitual.py (RAG)
"""

import sys
from pathlib import Path

# Adicionar pasta raiz ao path
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from config_llm import criar_llm, validar_configuracao, LLM_TYPE
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)

# Tentar importar RAG (opcional se houver problemas com PyTorch)
try:
    from tool_rag_conceitual import buscar_conhecimento_sinarm
    RAG_DISPONIVEL = True
except ImportError as e:
    print(f"⚠️ RAG não disponível: {e}")
    print("⚠️ Continuando sem RAG (respostas conceituais usarão LLM puro)")
    RAG_DISPONIVEL = False
    
import re
import json

print("="*70)
print("AGENTE v4.6 - RAG + FEW-SHOT + CHAIN-OF-THOUGHT")
print("="*70)
print("\nEVOLUÇÃO:")
print("- v4.5: RAG + Zero-Shot (81% acurácia)")
print("- v4.6: RAG + Few-Shot + CoT (95%+ esperado) ← HOJE!")
print("\nTÉCNICAS APLICADAS:")
print("- ✅ RAG (E4)")
print("- ✅ Few-Shot Learning (E2)")
print("- ✅ Chain-of-Thought (E2)")
print(f"\nLLM CONFIGURADO: {LLM_TYPE.upper()}")
print("="*70)


# ========== FEW-SHOT EXAMPLES ==========

FEW_SHOT_EXAMPLES = """
╔══════════════════════════════════════════════════════════════╗
║ FEW-SHOT LEARNING (5 EXEMPLOS COMPLETOS)                    ║
╚══════════════════════════════════════════════════════════════╝

Você é um especialista em análise de perguntas sobre dados SINARM.
Sua missão é classificar perguntas e extrair parâmetros EXATOS.

Siga EXATAMENTE o formato dos exemplos abaixo:

─────────────────────────────────────────────────────────────
EXEMPLO 1: Pergunta sobre UMA marca
─────────────────────────────────────────────────────────────
Pergunta: "Quantas armas Taurus?"

Análise:
- Tipo: marca (menciona UMA marca específica)
- Marca mencionada: Taurus
- Sem calibre, sem tipo de ocorrência
- Ferramenta: contar_armas_marca

JSON:
{
    "tipo": "marca",
    "parametros": {
        "marca": "Taurus"
    },
    "justificativa": "Pergunta sobre quantidade de UMA marca específica (Taurus)"
}

─────────────────────────────────────────────────────────────
EXEMPLO 2: Pergunta combinada (marca + calibre)
─────────────────────────────────────────────────────────────
Pergunta: "Quantas Glock .40?"

Análise:
- Tipo: combinado (marca E calibre juntos)
- Marca: Glock
- Calibre: .40
- Ferramenta: busca combinada marca+calibre

JSON:
{
    "tipo": "combinado",
    "parametros": {
        "marca": "Glock",
        "calibre": ".40"
    },
    "justificativa": "Pergunta combinada: marca (Glock) E calibre (.40) na mesma query"
}

─────────────────────────────────────────────────────────────
EXEMPLO 3: Pergunta comparativa (MÚLTIPLAS marcas)
─────────────────────────────────────────────────────────────
Pergunta: "Há mais Taurus ou Glock?"

Análise:
- Tipo: comparacao (palavra "ou" indica comparação)
- Marcas mencionadas: Taurus, Glock (2 marcas)
- Precisa buscar AMBAS e comparar
- Ferramenta: múltiplas chamadas + comparação

JSON:
{
    "tipo": "comparacao",
    "parametros": {
        "marca": ["Taurus", "Glock"]
    },
    "justificativa": "Pergunta comparativa: compara DUAS marcas (Taurus vs Glock)"
}

─────────────────────────────────────────────────────────────
EXEMPLO 4: Pergunta sobre tipo de ocorrência
─────────────────────────────────────────────────────────────
Pergunta: "Quantas apreensões de armas?"

Análise:
- Tipo: tipo (menciona tipo de ocorrência)
- Tipo de ocorrência: Apreensão
- Sem marca, sem calibre
- Ferramenta: contar_armas_tipo

JSON:
{
    "tipo": "tipo",
    "parametros": {
        "tipo": "Apreensao"
    },
    "justificativa": "Pergunta sobre tipo de ocorrência (Apreensão)"
}

─────────────────────────────────────────────────────────────
EXEMPLO 5: Pergunta conceitual (sem dados)
─────────────────────────────────────────────────────────────
Pergunta: "O que é BO?"

Análise:
- Tipo: conceitual (pergunta "o que é")
- Não precisa buscar dados quantitativos
- Precisa de definição/explicação
- Ferramenta: RAG (busca em documentação)

JSON:
{
    "tipo": "conceitual",
    "parametros": {},
    "justificativa": "Pergunta conceitual: busca definição, não dados quantitativos"
}
"""

# ========== CHAIN-OF-THOUGHT TEMPLATE ==========

COT_TEMPLATE = """
╔══════════════════════════════════════════════════════════════╗
║ CHAIN-OF-THOUGHT (RACIOCÍNIO OBRIGATÓRIO EM 4 ETAPAS)       ║
╚══════════════════════════════════════════════════════════════╝

VOCÊ DEVE SEMPRE seguir estas 4 etapas antes de responder:

┌──────────────────────────────────────────────────────────────┐
│ ETAPA 1: PENSAMENTO                                          │
├──────────────────────────────────────────────────────────────┤
│ Pensamento: [Analise a pergunta]                            │
│   • Que tipo de pergunta é?                                  │
│   • Quantas entidades são mencionadas?                       │
│   • Quais parâmetros preciso extrair?                        │
│   • Qual ferramenta é apropriada?                            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ ETAPA 2: CLASSIFICAÇÃO                                       │
├──────────────────────────────────────────────────────────────┤
│ Classificação:                                               │
│   • Tipo: [marca|calibre|tipo|combinado|comparacao|conceitual]│
│   • Parâmetros extraídos: [valores EXATOS]                   │
│   • Ferramenta escolhida: [nome da tool]                     │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ ETAPA 3: VALIDAÇÃO                                           │
├──────────────────────────────────────────────────────────────┤
│ Validação:                                                   │
│   • Parâmetros estão corretos?                               │
│   • Valores estão no formato esperado?                       │
│   • Há ambiguidade?                                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ ETAPA 4: RESPOSTA JSON                                       │
├──────────────────────────────────────────────────────────────┤
│ JSON final:                                                  │
│   {                                                          │
│       "tipo": "...",                                         │
│       "parametros": {...},                                   │
│       "justificativa": "..."                                 │
│   }                                                          │
└──────────────────────────────────────────────────────────────┘

EXEMPLO COMPLETO DE RESPOSTA COM CoT:

Pergunta: "Quantas Glock .40?"

Pensamento: 
  • Pergunta menciona marca (Glock) E calibre (.40)
  • São 2 parâmetros combinados na mesma query
  • Preciso extrair: marca="Glock", calibre=".40"
  • Ferramenta apropriada: busca combinada

Classificação:
  • Tipo: combinado (marca + calibre)
  • Parâmetros: marca="Glock", calibre=".40"
  • Ferramenta: contar_armas_combinado ou busca marca+calibre

Validação:
  • Marca "Glock" está correta (capitalização OK)
  • Calibre ".40" está no formato esperado
  • Sem ambiguidade

JSON:
{
    "tipo": "combinado",
    "parametros": {
        "marca": "Glock",
        "calibre": ".40"
    },
    "justificativa": "Pergunta combinada: marca (Glock) E calibre (.40)"
}
"""


def agente_v4_6_rag_fewshot_cot(pergunta_usuario):
    """
    Agente v4.6 COM RAG + FEW-SHOT + CHAIN-OF-THOUGHT
    
    MUDANÇAS em relação ao v4.5:
    1. Prompt agora inclui FEW_SHOT_EXAMPLES (5 exemplos)
    2. Prompt agora inclui COT_TEMPLATE (4 etapas)
    3. LLM é forçado a raciocinar antes de responder
    4. Melhoria esperada: 81% → 95%+
    
    ESTRATÉGIA:
    - SQL tools: com Few-Shot + CoT
    - Conceitual: RAG + Few-Shot + CoT
    """
    
    # Criar LLM usando configuração do .env
    llm = criar_llm()
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*70)
    
    # ===== PASSO 1: LLM ANALISA COM FEW-SHOT + CoT =====
    print("\n[PASSO 1] LLM analisando com Few-Shot + CoT...")
    
    prompt_analise = f"""{FEW_SHOT_EXAMPLES}

{COT_TEMPLATE}

═══════════════════════════════════════════════════════════════
AGORA ANALISE A PERGUNTA ABAIXO SEGUINDO O FORMATO ACIMA
═══════════════════════════════════════════════════════════════

PERGUNTA DO USUÁRIO:
"{pergunta_usuario}"

FERRAMENTAS DISPONÍVEIS:
1. contar_armas_marca - Conta armas de UMA marca específica
2. contar_armas_calibre - Conta armas de UM calibre específico
3. contar_armas_tipo - Conta ocorrências de UM tipo (Apreensao/Roubo/Furto)
4. contar_armas_combinado - Conta armas de UMA marca E (tipo OU calibre)
5. COMPARACAO - Quando pergunta compara MÚLTIPLAS marcas
6. CONCEITUAL - Pergunta sobre conceito (não precisa dados quantitativos)

INSTRUÇÕES:
1. Siga as 4 etapas do Chain-of-Thought (Pensamento → Classificação → Validação → JSON)
2. Use os 5 exemplos Few-Shot como referência
3. Extraia valores EXATOS dos parâmetros
4. Se múltiplas marcas (ex: "Taurus ou Glock") → tipo = "comparacao"
5. Se uma marca E um calibre (ex: "Glock .40") → tipo = "combinado"
6. Se conceitual (ex: "O que é") → tipo = "conceitual"

RESPONDA SEGUINDO O FORMATO CoT (4 etapas) E TERMINE COM O JSON:"""

    resposta_llm = llm.invoke(prompt_analise)
    
    # Converter AIMessage para string (OpenRouter retorna AIMessage)
    if hasattr(resposta_llm, 'content'):
        resposta_llm = resposta_llm.content
    
    print(f"[LLM] Resposta completa:\n{resposta_llm}")
    print("-"*70)
    
    # Tentar parsear JSON
    try:
        # Extrair JSON da resposta (pode vir com texto extra do CoT)
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', resposta_llm, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            analise = json.loads(json_str)
        else:
            raise ValueError("JSON não encontrado na resposta")
        
        print(f"\n[ANÁLISE] Tipo: {analise['tipo']}")
        print(f"[ANÁLISE] Parâmetros: {analise['parametros']}")
        print(f"[ANÁLISE] Justificativa: {analise['justificativa']}")
        
    except Exception as e:
        print(f"\n[ERRO] LLM não retornou JSON válido: {e}")
        print(f"[FALLBACK] Usando detecção por palavras-chave...")
        
        # Fallback: detecção simples (mesmo do v4.5)
        analise = detectar_por_palavras_chave(pergunta_usuario)
    
    # ===== PASSO 2: EXECUTAR FERRAMENTA(S) =====
    print(f"\n[PASSO 2] Executando ferramenta...")
    
    tipo = analise['tipo']
    parametros = analise['parametros']
    
    # CASO 1: COMPARACAO (multiplas marcas)
    if tipo == "comparacao":
        marcas = parametros.get('marca', [])
        if isinstance(marcas, str):
            # Converter string "Taurus, Glock" em lista
            marcas = [m.strip() for m in marcas.split(',')]
        
        print(f"[TIPO] Comparação entre {len(marcas)} marcas")
        
        resultados = {}
        for marca in marcas:
            print(f"  - Buscando {marca}...")
            resultado = contar_armas_marca.func(marca)
            numeros = re.findall(r'\d+', resultado)
            total = int(numeros[0]) if numeros else 0
            resultados[marca] = total
            print(f"    [INFO] {marca}: {total:,} armas")
        
        # Ordenar
        marcas_ordenadas = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
        
        resposta = "Segundo o SINARM 2026:\n\n"
        resposta += "COMPARAÇÃO:\n"
        for i, (marca, total) in enumerate(marcas_ordenadas, 1):
            resposta += f"{i}. {marca.upper()}: {total:,} armas\n"
        
        marca_maior = marcas_ordenadas[0][0]
        total_maior = marcas_ordenadas[0][1]
        marca_menor = marcas_ordenadas[-1][0]
        total_menor = marcas_ordenadas[-1][1]
        diferenca = total_maior - total_menor
        
        resposta += f"\nCONCLUSÃO: {marca_maior.upper()} tem {diferenca:,} armas a mais.\n"
        resposta += f"Fonte: SINARM 2026"
        
        return resposta
    
    # CASO 2: MARCA
    elif tipo == "marca":
        marca = parametros.get('marca')
        print(f"[FERRAMENTA] contar_armas_marca('{marca}')")
        resultado = contar_armas_marca.func(marca)
        numeros = re.findall(r'\d+', resultado)
        total = numeros[0] if numeros else "?"
        
        resposta = f"Segundo o SINARM 2026:\n"
        resposta += f"- Marca: {marca.upper()}\n"
        resposta += f"- Total: {total} armas\n"
        resposta += f"Fonte: SINARM 2026"
        return resposta
    
    # CASO 3: CALIBRE
    elif tipo == "calibre":
        calibre = parametros.get('calibre')
        print(f"[FERRAMENTA] contar_armas_calibre('{calibre}')")
        resultado = contar_armas_calibre.func(calibre)
        numeros = re.findall(r'\d+', resultado)
        total = numeros[0] if numeros else "?"
        
        resposta = f"Segundo o SINARM 2026:\n"
        resposta += f"- Calibre: {calibre}\n"
        resposta += f"- Total: {total} armas\n"
        resposta += f"Fonte: SINARM 2026"
        return resposta
    
    # CASO 4: TIPO
    elif tipo == "tipo":
        tipo_ocorrencia = parametros.get('tipo')
        print(f"[FERRAMENTA] contar_armas_tipo('{tipo_ocorrencia}')")
        resultado = contar_armas_tipo.func(tipo_ocorrencia)
        numeros = re.findall(r'\d+', resultado)
        total = numeros[0] if numeros else "?"
        
        resposta = f"Segundo o SINARM 2026:\n"
        resposta += f"- Tipo: {tipo_ocorrencia}\n"
        resposta += f"- Total: {total} ocorrências\n"
        resposta += f"Fonte: SINARM 2026"
        return resposta
    
    # CASO 5: COMBINADO
    elif tipo == "combinado":
        marca = parametros.get('marca')
        tipo_ocorrencia = parametros.get('tipo')
        calibre = parametros.get('calibre')
        
        # Se tem marca + calibre (sem tipo), usar busca por marca e filtrar por calibre
        if marca and calibre and not tipo_ocorrencia:
            print(f"[FERRAMENTA] Busca combinada: marca={marca}, calibre={calibre}")
            
            # Buscar todas as armas da marca
            from tools_basicas_v2 import carregar_csv
            df = carregar_csv()
            
            resultado = df[
                (df["MARCA_ARMA"].str.contains(marca.upper(), case=False, na=False)) & 
                (df["CALIBRE_ARMA"].str.contains(calibre, case=False, na=False))
            ]
            total = len(resultado)
            
            resposta = f"Segundo o SINARM 2026:\n"
            resposta += f"- Marca: {marca.upper()}\n"
            resposta += f"- Calibre: {calibre}\n"
            resposta += f"- Total: {total:,} armas\n"
            resposta += f"Fonte: SINARM 2026"
            return resposta
        
        # Se tem marca + tipo (sem calibre), usar contar_armas_combinado
        elif marca and tipo_ocorrencia:
            print(f"[FERRAMENTA] contar_armas_combinado('{marca}', '{tipo_ocorrencia}')")
            resultado = contar_armas_combinado.func(marca, tipo_ocorrencia)
            numeros = re.findall(r'\d+', resultado)
            total = numeros[0] if numeros else "?"
            
            resposta = f"Segundo o SINARM 2026:\n"
            resposta += f"- Marca: {marca.upper()}\n"
            resposta += f"- Tipo: {tipo_ocorrencia}\n"
            resposta += f"- Total: {total} ocorrências\n"
            resposta += f"Fonte: SINARM 2026"
            return resposta
        
        else:
            return "❌ ERRO: Parâmetros insuficientes para busca combinada"
    
    # CASO 6: CONCEITUAL (usa RAG se disponível)
    elif tipo == "conceitual":
        if RAG_DISPONIVEL:
            print(f"[FERRAMENTA] RAG: buscar_conhecimento_sinarm('{pergunta_usuario}')")
            resposta_rag = buscar_conhecimento_sinarm.func(pergunta_usuario)
            
            # Se RAG retornou resposta válida
            if resposta_rag and not resposta_rag.startswith("❌"):
                return resposta_rag
        
        # Fallback: LLM puro
        print(f"[FALLBACK] RAG não disponível ou falhou, usando LLM puro...")
        resposta_llm = llm.invoke(f"Responda de forma breve e objetiva: {pergunta_usuario}")
        
        if hasattr(resposta_llm, 'content'):
            return resposta_llm.content
        return str(resposta_llm)
    
    else:
        return f"❌ ERRO: Tipo '{tipo}' não reconhecido"


def detectar_por_palavras_chave(pergunta):
    """
    Fallback: detecção simples por palavras-chave
    (mesmo do v4.5, sem mudanças)
    """
    pergunta_lower = pergunta.lower()
    
    # Detectar conceitual
    if any(palavra in pergunta_lower for palavra in ["o que é", "defina", "explique", "significa"]):
        return {
            "tipo": "conceitual",
            "parametros": {},
            "justificativa": "Pergunta conceitual detectada por palavras-chave"
        }
    
    # Detectar comparação (palavra "ou")
    if " ou " in pergunta_lower or " vs " in pergunta_lower:
        # Tentar extrair marcas
        marcas = []
        marcas_conhecidas = ["taurus", "glock", "beretta", "colt", "smith", "ruger", "sig"]
        for marca in marcas_conhecidas:
            if marca in pergunta_lower:
                marcas.append(marca.capitalize())
        
        if len(marcas) >= 2:
            return {
                "tipo": "comparacao",
                "parametros": {"marca": marcas},
                "justificativa": "Comparação detectada: múltiplas marcas mencionadas"
            }
    
    # Detectar tipo de ocorrência
    if "apreens" in pergunta_lower:
        return {
            "tipo": "tipo",
            "parametros": {"tipo": "Apreensao"},
            "justificativa": "Tipo de ocorrência detectado: Apreensão"
        }
    if "roub" in pergunta_lower:
        return {
            "tipo": "tipo",
            "parametros": {"tipo": "Roubo"},
            "justificativa": "Tipo de ocorrência detectado: Roubo"
        }
    if "furt" in pergunta_lower:
        return {
            "tipo": "tipo",
            "parametros": {"tipo": "Furto"},
            "justificativa": "Tipo de ocorrência detectado: Furto"
        }
    
    # Detectar calibre
    calibres = [".22", ".38", ".380", "9mm", ".40", ".45", "12", "7.62", "5.56"]
    for calibre in calibres:
        if calibre in pergunta_lower:
            return {
                "tipo": "calibre",
                "parametros": {"calibre": calibre},
                "justificativa": f"Calibre detectado: {calibre}"
            }
    
    # Detectar marca (default)
    marcas_conhecidas = ["taurus", "glock", "beretta", "colt", "smith", "ruger", "sig"]
    for marca in marcas_conhecidas:
        if marca in pergunta_lower:
            return {
                "tipo": "marca",
                "parametros": {"marca": marca.capitalize()},
                "justificativa": f"Marca detectada: {marca}"
            }
    
    # Se não detectou nada, default para conceitual
    return {
        "tipo": "conceitual",
        "parametros": {},
        "justificativa": "Não foi possível classificar, assumindo conceitual"
    }


if __name__ == "__main__":
    print("\n🤖 AGENTE SINARM v4.6 - RAG + FEW-SHOT + CoT")
    print("="*70)
    print("\nDIFERENÇAS vs v4.5:")
    print("- ✅ Few-Shot: 5 exemplos completos no prompt")
    print("- ✅ Chain-of-Thought: 4 etapas obrigatórias")
    print("- ✅ Raciocínio transparente e estruturado")
    print("- 📈 Acurácia esperada: 95%+ (vs 81% do v4.5)")
    print("="*70)
    
    while True:
        pergunta = input("\n❓ Pergunta (ou 'sair'): ")
        if pergunta.lower() == 'sair':
            break
        
        try:
            resposta = agente_v4_6_rag_fewshot_cot(pergunta)
            print(f"\n💬 RESPOSTA:\n{resposta}\n")
        except Exception as e:
            print(f"\n❌ ERRO: {e}")
