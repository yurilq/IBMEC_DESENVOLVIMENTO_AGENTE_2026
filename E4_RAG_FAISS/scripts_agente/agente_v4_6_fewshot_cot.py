# agente_v4_6_fewshot_cot.py
# Agente v4.6 - v4.5 + FEW-SHOT + CHAIN-OF-THOUGHT
# EVOLUÇÃO: v4.5 → v4.6 (adiciona Few-Shot e CoT no prompt)
# SEM NOVAS BIBLIOTECAS: mesmas dependências do v4.5

from config_llm import criar_llm, validar_configuracao, LLM_TYPE
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)
import re
import json

# Tentar importar RAG (opcional, como no v4.5)
try:
    from tool_rag_conceitual import buscar_conhecimento_sinarm
    RAG_DISPONIVEL = True
except:
    RAG_DISPONIVEL = False
    print("[AVISO] RAG não disponível, usando fallback para perguntas conceituais")

print("="*70)
print("AGENTE v4.6 - FEW-SHOT + CHAIN-OF-THOUGHT")
print("="*70)
print("\nEVOLUÇÃO:")
print("- v4.5: Zero-Shot (81% acurácia)")
print("- v4.6: Few-Shot + CoT (90% esperado) [INFO] HOJE!")
print("\nMUDANÇAS:")
print("- Prompt: 5 exemplos Few-Shot + 4 etapas CoT")
print("- Bibliotecas: MESMAS do v4.5 (sem adicionar nada)")
print(f"\nLLM CONFIGURADO: {LLM_TYPE.upper()}")
print("="*70)


def agente_v4_6_fewshot_cot(pergunta_usuario):
    """
    Agente v4.6 - v4.5 + FEW-SHOT + COT
    
    MUDANÇAS em relação ao v4.5:
    1. Prompt de análise: adiciona 5 exemplos Few-Shot
    2. Prompt de análise: adiciona 4 etapas Chain-of-Thought
    3. Resto: EXATAMENTE IGUAL ao v4.5
    
    BIBLIOTECAS:
    - MESMAS do v4.5 (config_llm, tools_basicas_v2, re, json)
    - SEM adicionar nenhuma nova biblioteca
    """
    
    # Criar LLM usando configuração do .env (igual v4.5)
    llm = criar_llm()
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*70)
    
    # ===== PASSO 1: LLM ANALISA COM FEW-SHOT + COT =====
    print("\n[PASSO 1] LLM analisando com Few-Shot + CoT...")
    
    # NOVO v4.6: Prompt com Few-Shot + CoT
    prompt_analise = f"""
╔══════════════════════════════════════════════════════════════╗
║ FEW-SHOT LEARNING (5 EXEMPLOS COMPLETOS)                    ║
╚══════════════════════════════════════════════════════════════╝

Voce eh especialista em analise de perguntas sobre dados SINARM.
Sua missao eh classificar perguntas e extrair parametros EXATOS.

Siga EXATAMENTE o formato dos exemplos abaixo:

─────────────────────────────────────────────────────────────
EXEMPLO 1: Pergunta sobre UMA marca
─────────────────────────────────────────────────────────────
Pergunta: "Quantas armas Taurus?"

JSON:
{{
    "tipo": "marca",
    "parametros": {{"marca": "Taurus"}},
    "justificativa": "Pergunta sobre quantidade de UMA marca especifica (Taurus)"
}}

─────────────────────────────────────────────────────────────
EXEMPLO 2: Pergunta combinada (marca + calibre)
─────────────────────────────────────────────────────────────
Pergunta: "Quantas Glock .40?"

JSON:
{{
    "tipo": "combinado",
    "parametros": {{"marca": "Glock", "calibre": ".40"}},
    "justificativa": "Pergunta combinada: marca (Glock) E calibre (.40)"
}}

─────────────────────────────────────────────────────────────
EXEMPLO 3: Pergunta comparativa (MULTIPLAS marcas)
─────────────────────────────────────────────────────────────
Pergunta: "Ha mais Taurus ou Glock?"

JSON:
{{
    "tipo": "comparacao",
    "parametros": {{"marca": ["Taurus", "Glock"]}},
    "justificativa": "Pergunta comparativa: compara DUAS marcas (Taurus vs Glock)"
}}

─────────────────────────────────────────────────────────────
EXEMPLO 4: Pergunta sobre tipo de ocorrencia
─────────────────────────────────────────────────────────────
Pergunta: "Quantas apreensoes de armas?"

JSON:
{{
    "tipo": "tipo",
    "parametros": {{"tipo": "Apreensao"}},
    "justificativa": "Pergunta sobre tipo de ocorrencia (Apreensao)"
}}

─────────────────────────────────────────────────────────────
EXEMPLO 5: Pergunta conceitual (sem dados)
─────────────────────────────────────────────────────────────
Pergunta: "O que e BO?"

JSON:
{{
    "tipo": "conceitual",
    "parametros": {{}},
    "justificativa": "Pergunta conceitual: busca definicao, nao dados quantitativos"
}}


╔══════════════════════════════════════════════════════════════╗
║ CHAIN-OF-THOUGHT (RACIOCINIO OBRIGATORIO EM 4 ETAPAS)       ║
╚══════════════════════════════════════════════════════════════╝

VOCE DEVE SEMPRE seguir estas 4 etapas antes de responder:

ETAPA 1 - PENSAMENTO:
  • Que tipo de pergunta e?
  • Quantas entidades sao mencionadas?
  • Quais parametros preciso extrair?
  • Qual ferramenta e apropriada?

ETAPA 2 - CLASSIFICACAO:
  • Tipo: [marca|calibre|tipo|combinado|comparacao|conceitual]
  • Parametros extraidos: [valores EXATOS]
  • Ferramenta escolhida: [nome da tool]

ETAPA 3 - VALIDACAO:
  • Parametros estao corretos?
  • Valores estao no formato esperado?
  • Ha ambiguidade?

ETAPA 4 - RESPOSTA JSON:
  • JSON final estruturado


═══════════════════════════════════════════════════════════════
AGORA ANALISE A PERGUNTA ABAIXO SEGUINDO O FORMATO ACIMA
═══════════════════════════════════════════════════════════════

PERGUNTA DO USUARIO:
"{pergunta_usuario}"

FERRAMENTAS DISPONIVEIS:
1. contar_armas_marca - Conta armas de UMA marca especifica
2. contar_armas_calibre - Conta armas de UM calibre especifico
3. contar_armas_tipo - Conta ocorrencias de UM tipo (Apreensao/Roubo/Furto)
4. contar_armas_combinado - Conta armas de UMA marca E (tipo OU calibre)
5. COMPARACAO - Quando pergunta compara MULTIPLAS marcas
6. CONCEITUAL - Pergunta sobre conceito (nao precisa dados quantitativos)

INSTRUCOES:
1. Siga as 4 etapas do Chain-of-Thought
2. Use os 5 exemplos Few-Shot como referencia
3. Extraia valores EXATOS dos parametros
4. Se multiplas marcas (ex: "Taurus ou Glock") → tipo = "comparacao"
5. Se uma marca E um calibre (ex: "Glock .40") → tipo = "combinado"
6. Se conceitual (ex: "O que e") → tipo = "conceitual"

RESPONDA SEGUINDO O FORMATO CoT (4 etapas) E TERMINE COM O JSON:"""

    resposta_llm = llm.invoke(prompt_analise)
    
    # Converter AIMessage para string (OpenRouter retorna AIMessage)
    if hasattr(resposta_llm, 'content'):
        resposta_llm = resposta_llm.content
    
    print(f"[LLM] {resposta_llm[:300]}...")
    
    # Tentar parsear JSON
    try:
        # Extrair JSON da resposta (pode vir com texto extra do CoT)
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', resposta_llm, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            analise = json.loads(json_str)
        else:
            raise ValueError("JSON nao encontrado na resposta")
        
        print(f"\n[ANALISE] Tipo: {analise['tipo']}")
        print(f"[ANALISE] Parametros: {analise['parametros']}")
        print(f"[ANALISE] Justificativa: {analise['justificativa']}")
        
    except Exception as e:
        print(f"\n[ERRO] LLM nao retornou JSON valido: {e}")
        print(f"[FALLBACK] Usando deteccao por palavras-chave...")
        
        # Fallback: deteccao simples (mesmo do v4.5)
        analise = detectar_por_palavras_chave(pergunta_usuario)
    
    # ===== PASSO 2: EXECUTAR FERRAMENTA(S) =====
    # RESTO É EXATAMENTE IGUAL AO v4.5!
    
    print(f"\n[PASSO 2] Executando ferramenta...")
    
    tipo = analise['tipo']
    parametros = analise['parametros']
    
    # CASO 1: COMPARACAO (multiplas marcas)
    if tipo == "comparacao":
        marcas = parametros.get('marca', [])
        if isinstance(marcas, str):
            marcas = [m.strip() for m in marcas.split(',')]
        
        print(f"[TIPO] Comparacao entre {len(marcas)} marcas")
        
        resultados = {}
        for marca in marcas:
            print(f"  - Buscando {marca}...")
            resultado = contar_armas_marca.func(marca)
            numeros = re.findall(r'\d+', resultado)
            total = int(numeros[0]) if numeros else 0
            resultados[marca] = total
            print(f"    [INFO] {marca}: {total:,} armas")
        
        marcas_ordenadas = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
        
        resposta = "Segundo o SINARM 2026:\n\n"
        resposta += "COMPARACAO:\n"
        for i, (marca, total) in enumerate(marcas_ordenadas, 1):
            resposta += f"{i}. {marca.upper()}: {total:,} armas\n"
        
        marca_maior = marcas_ordenadas[0][0]
        total_maior = marcas_ordenadas[0][1]
        marca_menor = marcas_ordenadas[-1][0]
        total_menor = marcas_ordenadas[-1][1]
        diferenca = total_maior - total_menor
        
        resposta += f"\nCONCLUSAO: {marca_maior.upper()} tem {diferenca:,} armas a mais.\n"
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
        resposta += f"- Total: {total} ocorrencias\n"
        resposta += f"Fonte: SINARM 2026"
        return resposta
    
    # CASO 5: COMBINADO
    elif tipo == "combinado":
        marca = parametros.get('marca')
        tipo_ocorrencia = parametros.get('tipo')
        calibre = parametros.get('calibre')
        
        if marca and calibre and not tipo_ocorrencia:
            print(f"[FERRAMENTA] Busca combinada: marca={marca}, calibre={calibre}")
            
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
        
        elif marca and tipo_ocorrencia:
            print(f"[FERRAMENTA] contar_armas_combinado('{marca}', '{tipo_ocorrencia}')")
            resultado = contar_armas_combinado.func(marca, tipo_ocorrencia)
            numeros = re.findall(r'\d+', resultado)
            total = numeros[0] if numeros else "?"
            
            resposta = f"Segundo o SINARM 2026:\n"
            resposta += f"- Marca: {marca.upper()}\n"
            resposta += f"- Tipo: {tipo_ocorrencia}\n"
            resposta += f"- Total: {total} armas\n"
            resposta += f"Fonte: SINARM 2026"
            return resposta
        
        else:
            return "Parametros insuficientes para busca combinada"
    
    # CASO 6: CONCEITUAL (mesmo do v4.5)
    elif tipo == "conceitual":
        print(f"[TIPO] Pergunta conceitual")
        
        # Tentar RAG se disponível
        if RAG_DISPONIVEL:
            try:
                print(f"[RAG] Buscando em documentos SINARM...")
                contexto = buscar_conhecimento_sinarm(pergunta_usuario)
                if contexto and "[INFO]" not in contexto and len(contexto) >= 100:
                    return contexto
            except:
                pass
        
        # Fallback: dicionário básico
        print(f"[FALLBACK] Usando conhecimento basico...")
        conhecimento_basico = {
            "bo": "BO (Boletim de Ocorrencia) eh registro policial de crime.",
            "furto": "Furto eh apropriacao SEM violencia.",
            "roubo": "Roubo eh apropriacao COM violencia.",
            "calibre": "Calibre eh diametro do cano da arma.",
            "apreensao": "Apreensao eh retirada de arma de circulacao pela policia."
        }
        
        pergunta_lower = pergunta_usuario.lower()
        for conceito, definicao in conhecimento_basico.items():
            if conceito in pergunta_lower:
                return f"{definicao}\n(Fonte: Conhecimento basico PCDF)"
        
        # Último recurso: LLM puro
        print(f"[FALLBACK] Usando LLM...")
        prompt = f"Voce eh investigador PCDF. Responda de forma tecnica e objetiva: {pergunta_usuario}"
        resposta = llm.invoke(prompt)
        
        if hasattr(resposta, 'content'):
            resposta = resposta.content
        
        return f"{resposta}\n\n[INFO] AVISO: Resposta gerada por LLM sem fonte documental."
    
    else:
        return f"Tipo '{tipo}' nao reconhecido"


def detectar_por_palavras_chave(pergunta):
    """Fallback: deteccao simples (mesmo do v4.5)"""
    pergunta_lower = pergunta.lower()
    
    if any(palavra in pergunta_lower for palavra in ["o que e", "defina", "explique", "significa"]):
        return {"tipo": "conceitual", "parametros": {}, "justificativa": "Conceitual por palavras-chave"}
    
    if " ou " in pergunta_lower or " vs " in pergunta_lower:
        marcas = []
        marcas_conhecidas = ["taurus", "glock", "beretta", "colt", "smith", "ruger", "sig"]
        for marca in marcas_conhecidas:
            if marca in pergunta_lower:
                marcas.append(marca.capitalize())
        
        if len(marcas) >= 2:
            return {"tipo": "comparacao", "parametros": {"marca": marcas}, "justificativa": "Comparacao detectada"}
    
    if "apreens" in pergunta_lower:
        return {"tipo": "tipo", "parametros": {"tipo": "Apreensao"}, "justificativa": "Tipo Apreensao"}
    if "roub" in pergunta_lower:
        return {"tipo": "tipo", "parametros": {"tipo": "Roubo"}, "justificativa": "Tipo Roubo"}
    if "furt" in pergunta_lower:
        return {"tipo": "tipo", "parametros": {"tipo": "Furto"}, "justificativa": "Tipo Furto"}
    
    calibres = [".22", ".38", ".380", "9mm", ".40", ".45", "12", "7.62", "5.56"]
    for calibre in calibres:
        if calibre in pergunta_lower:
            return {"tipo": "calibre", "parametros": {"calibre": calibre}, "justificativa": f"Calibre {calibre}"}
    
    marcas_conhecidas = ["taurus", "glock", "beretta", "colt", "smith", "ruger", "sig"]
    for marca in marcas_conhecidas:
        if marca in pergunta_lower:
            return {"tipo": "marca", "parametros": {"marca": marca.capitalize()}, "justificativa": f"Marca {marca}"}
    
    return {"tipo": "conceitual", "parametros": {}, "justificativa": "Nao classificado"}


if __name__ == "__main__":
    print("\n🤖 AGENTE SINARM v4.6 - FEW-SHOT + CoT")
    print("="*70)
    print("\nDIFERENÇAS vs v4.5:")
    print("- ✅ Few-Shot: 5 exemplos completos no prompt")
    print("- ✅ Chain-of-Thought: 4 etapas obrigatórias")
    print("- ✅ Raciocínio transparente e estruturado")
    print("- 📈 Acurácia esperada: 90%+ (vs 81% do v4.5)")
    print("="*70)
    
    while True:
        pergunta = input("\n❓ Pergunta (ou 'sair'): ")
        if pergunta.lower() == 'sair':
            break
        
        try:
            resposta = agente_v4_6_fewshot_cot(pergunta)
            print(f"\n💬 RESPOSTA:\n{resposta}\n")
        except Exception as e:
            print(f"\n❌ ERRO: {e}")
