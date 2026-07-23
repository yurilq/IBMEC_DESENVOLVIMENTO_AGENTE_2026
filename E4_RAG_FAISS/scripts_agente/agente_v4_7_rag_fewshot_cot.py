# agente_v4_7_rag_fewshot_cot.py
# Agente v4.7 - MELHOR DOS DOIS MUNDOS
# = v4.5 RAG TF-IDF (93%) + v4.6 Few-Shot + CoT (91%)
# OBJETIVO: Superar 93% combinando todas as técnicas

from config_llm import criar_llm, validar_configuracao, LLM_TYPE
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)
from tool_rag_tfidf import buscar_conhecimento_sinarm  # RAG TF-IDF Local
import re
import json

print("="*70)
print("AGENTE v4.7 - RAG + FEW-SHOT + CHAIN-OF-THOUGHT")
print("="*70)
print("\nEVOLUÇÃO:")
print("- v4.5: Zero-Shot + RAG TF-IDF (93%)")
print("- v4.6: Few-Shot + CoT (91%)")
print("- v4.7: RAG + Few-Shot + CoT (95%+ esperado) [INFO] HOJE!")
print("\nCOMBINAÇÃO:")
print("- RAG TF-IDF: 20 docs SINARM (perguntas conceituais)")
print("- Few-Shot: 5 exemplos (melhora classificação)")
print("- Chain-of-Thought: 4 etapas (raciocínio estruturado)")
print(f"\nLLM CONFIGURADO: {LLM_TYPE.upper()}")
print("="*70)


def agente_v4_7_rag_fewshot_cot(pergunta_usuario):
    """
    Agente v4.7 - RAG + FEW-SHOT + COT
    
    COMBINAÇÃO:
    1. RAG TF-IDF do v4.5 (perguntas conceituais)
    2. Few-Shot do v4.6 (5 exemplos no prompt)
    3. Chain-of-Thought do v4.6 (4 etapas de análise)
    
    HIPÓTESE:
    - RAG: +12 pontos (81% → 93%)
    - Few-Shot + CoT: +10 pontos (81% → 91%)
    - COMBINADOS: 95%+ esperado
    """
    
    # Criar LLM usando configuração do .env
    llm = criar_llm()
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*70)
    
    # ===== PASSO 1: LLM ANALISA COM FEW-SHOT + COT =====
    print("\n[PASSO 1] LLM analisando com Few-Shot + CoT...")
    
    # Prompt com Few-Shot + CoT (do v4.6)
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
EXEMPLO 2: Pergunta sobre UM calibre
─────────────────────────────────────────────────────────────
Pergunta: "Total de armas calibre .38"

JSON:
{{
    "tipo": "calibre",
    "parametros": {{"calibre": ".38"}},
    "justificativa": "Pergunta sobre quantidade de UM calibre especifico (.38)"
}}

─────────────────────────────────────────────────────────────
EXEMPLO 3: Pergunta COMBINADA (marca + calibre)
─────────────────────────────────────────────────────────────
Pergunta: "Quantas Glock 9mm?"

JSON:
{{
    "tipo": "combinado",
    "parametros": {{"marca": "Glock", "calibre": "9mm"}},
    "justificativa": "Pergunta menciona marca E calibre: busca combinada"
}}

─────────────────────────────────────────────────────────────
EXEMPLO 4: Pergunta COMPARATIVA (duas marcas)
─────────────────────────────────────────────────────────────
Pergunta: "Há mais Taurus ou Glock?"

JSON:
{{
    "tipo": "comparacao",
    "parametros": {{"marca": ["Taurus", "Glock"]}},
    "justificativa": "Pergunta compara DUAS ou mais marcas"
}}

─────────────────────────────────────────────────────────────
EXEMPLO 5: Pergunta CONCEITUAL (definição/explicação)
─────────────────────────────────────────────────────────────
Pergunta: "O que é calibre?"

JSON:
{{
    "tipo": "conceitual",
    "parametros": {{}},
    "justificativa": "Pergunta solicita definicao ou explicacao (nao eh contagem)"
}}

╔══════════════════════════════════════════════════════════════╗
║ CHAIN-OF-THOUGHT (RACIOCÍNIO EM 4 ETAPAS)                   ║
╚══════════════════════════════════════════════════════════════╝

Agora analise esta pergunta seguindo as 4 etapas:

ETAPA 1: Identificar TIPO de pergunta
- É contagem de marca? (ex: "Quantas Taurus?")
- É contagem de calibre? (ex: "Total .38?")
- É contagem de tipo? (ex: "Quantos roubos?")
- É combinado? (ex: "Taurus 9mm?")
- É comparacao? (ex: "Taurus ou Glock?")
- É conceitual? (ex: "O que é...?", "Explique...", "Diferença...")

ETAPA 2: Extrair PARAMETROS exatos
- Se marca: extrair nome da marca (Taurus, Glock, etc)
- Se calibre: extrair calibre (.38, 9mm, etc)
- Se tipo: extrair tipo (Roubo, Furto, Apreensao)
- Se combinado: extrair marca E calibre/tipo
- Se comparacao: extrair lista de marcas/calibres/tipos

ETAPA 3: Validar CONSISTÊNCIA
- Tipo "marca" tem parametro "marca"?
- Tipo "combinado" tem 2+ parametros?
- Tipo "comparacao" tem lista com 2+ itens?
- Tipo "conceitual" tem parametros vazios?

ETAPA 4: Gerar JSON final
- Formato: {{"tipo": "...", "parametros": {{...}}, "justificativa": "..."}}
- Sem comentarios ou texto extra
- Apenas JSON valido

╔══════════════════════════════════════════════════════════════╗
║ PERGUNTA DO USUÁRIO                                          ║
╚══════════════════════════════════════════════════════════════╝

"{pergunta_usuario}"

╔══════════════════════════════════════════════════════════════╗
║ SUA RESPOSTA (APENAS JSON, SEM TEXTO EXTRA)                 ║
╚══════════════════════════════════════════════════════════════╝
"""
    
    resposta_analise = llm.invoke(prompt_analise)
    
    # Converter AIMessage para string
    if hasattr(resposta_analise, 'content'):
        resposta_analise = resposta_analise.content
    
    print(f"[LLM] {resposta_analise[:200]}...")
    
    # Extrair JSON da resposta
    try:
        # Tentar achar JSON entre chaves
        match = re.search(r'\{.*\}', resposta_analise, re.DOTALL)
        if match:
            json_str = match.group()
            analise = json.loads(json_str)
        else:
            # Fallback: resposta inteira eh JSON
            analise = json.loads(resposta_analise)
        
        tipo = analise.get('tipo', '')
        parametros = analise.get('parametros', {})
        justificativa = analise.get('justificativa', '')
        
        print(f"\n[ANALISE] Tipo: {tipo}")
        print(f"[ANALISE] Parametros: {parametros}")
        print(f"[ANALISE] Justificativa: {justificativa}")
    
    except Exception as e:
        print(f"[ERRO] Falha ao extrair JSON: {e}")
        tipo = "conceitual"  # Fallback
        parametros = {}
    
    # ===== PASSO 2: EXECUTAR FERRAMENTA =====
    print(f"\n[PASSO 2] Executando ferramenta...")
    
    # CASO 1: MARCA
    if tipo == "marca":
        marca = parametros.get('marca', '')
        if marca:
            print(f"[FERRAMENTA] contar_armas_marca('{marca}')")
            resposta = contar_armas_marca.invoke({"marca": marca})
            return resposta
        else:
            return "Parametro 'marca' nao encontrado"
    
    # CASO 2: CALIBRE
    elif tipo == "calibre":
        calibre = parametros.get('calibre', '')
        if calibre:
            print(f"[FERRAMENTA] contar_armas_calibre('{calibre}')")
            resposta = contar_armas_calibre.invoke({"calibre": calibre})
            return resposta
        else:
            return "Parametro 'calibre' nao encontrado"
    
    # CASO 3: TIPO
    elif tipo == "tipo":
        tipo_ocorrencia = parametros.get('tipo', '')
        if tipo_ocorrencia:
            print(f"[FERRAMENTA] contar_armas_tipo('{tipo_ocorrencia}')")
            resposta = contar_armas_tipo.invoke({"tipo": tipo_ocorrencia})
            return resposta
        else:
            return "Parametro 'tipo' nao encontrado"
    
    # CASO 4: COMBINADO (marca + calibre/tipo)
    elif tipo == "combinado":
        marca = parametros.get('marca', '')
        calibre = parametros.get('calibre', '')
        tipo_ocorrencia = parametros.get('tipo', '')
        
        # Priorizar marca + tipo
        if marca and tipo_ocorrencia:
            print(f"[FERRAMENTA] contar_armas_combinado('{marca}', '{tipo_ocorrencia}')")
            resposta = contar_armas_combinado.invoke({"marca": marca, "tipo": tipo_ocorrencia})
            return resposta
        
        # Marca + calibre (usar SQL direto)
        elif marca and calibre:
            print(f"[FERRAMENTA] Busca combinada: marca={marca}, calibre={calibre}")
            import pandas as pd
            from pathlib import Path
            
            csv_path = Path(__file__).parent.parent / "DADOS_SINARM" / "OCORRENCIAS" / "OCORRENCIAS_2026.csv"
            df = pd.read_csv(csv_path, sep=";", encoding="latin1")
            
            # Limpar
            df["MARCA_ARMA"] = df["MARCA_ARMA"].str.strip()
            df["CALIBRE_ARMA"] = df["CALIBRE_ARMA"].str.strip()
            
            # Filtrar
            resultado = df[
                (df['MARCA_ARMA'].str.upper() == marca.upper()) & 
                (df['CALIBRE_ARMA'].str.contains(calibre, case=False, na=False))
            ]
            
            total = len(resultado)
            resposta = f"Segundo o SINARM 2026:\n- Marca: {marca}\n- Calibre: {calibre}\n- Total: {total} armas\nFonte: SINARM 2026"
            return resposta
        
        else:
            return "Parametros insuficientes para busca combinada"
    
    # CASO 5: COMPARACAO (2+ marcas/calibres/tipos)
    elif tipo == "comparacao":
        # Aceitar "marca" ou "marcas" como chave
        itens_comparar = parametros.get('marca', parametros.get('marcas', []))
        
        if isinstance(itens_comparar, list) and len(itens_comparar) >= 2:
            print(f"[TIPO] Comparacao entre {len(itens_comparar)} marcas")
            
            resultados_comparacao = []
            for item in itens_comparar:
                print(f"  - Buscando {item}...")
                count = contar_armas_marca.invoke({"marca": item})
                
                # Extrair numero
                match_num = re.search(r'Total:\s*(\d[\d,]*)', count)
                if match_num:
                    numero = int(match_num.group(1).replace(',', ''))
                    resultados_comparacao.append({
                        'item': item,
                        'total': numero
                    })
                    print(f"    [INFO] {item}: {numero:,} armas")
                else:
                    resultados_comparacao.append({
                        'item': item,
                        'total': 0
                    })
            
            # Ordenar por total
            resultados_comparacao.sort(key=lambda x: x['total'], reverse=True)
            
            # Construir resposta
            resposta = "COMPARAÇÃO SINARM 2026:\n\n"
            for i, res in enumerate(resultados_comparacao, 1):
                resposta += f"{i}º lugar: {res['item']} com {res['total']:,} armas\n"
            
            maior = resultados_comparacao[0]
            resposta += f"\nRESPOSTA: {maior['item']} é o mais comum ({maior['total']:,} armas)"
            resposta += f"\n\nFonte: SINARM 2026"
            
            return resposta
        
        else:
            return "Parametros insuficientes para comparacao (precisa 2+ itens)"
    
    # CASO 6: CONCEITUAL (COM RAG TF-IDF!)
    elif tipo == "conceitual":
        print(f"[TIPO] Pergunta conceitual (usando RAG TF-IDF)")
        
        # PASSO 1: Tentar RAG primeiro
        print(f"[RAG] Buscando em documentos SINARM...")
        contexto = buscar_conhecimento_sinarm(pergunta_usuario)
        
        # Verificar se RAG encontrou algo útil
        if "[INFO]" in contexto or len(contexto) < 100:
            print(f"[RAG] Nenhum documento relevante encontrado")
            print(f"[FALLBACK] Usando conhecimento básico...")
            
            # PASSO 2: Fallback para dicionário básico
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
                    return f"{definicao}\n(Fonte: Conhecimento básico PCDF)"
            
            # PASSO 3: Último recurso - LLM puro (com aviso)
            print(f"[FALLBACK] Usando LLM (última opção)...")
            prompt = f"Voce eh investigador PCDF. Responda de forma tecnica e objetiva: {pergunta_usuario}"
            resposta = llm.invoke(prompt)
            
            # Converter AIMessage para string
            if hasattr(resposta, 'content'):
                resposta = resposta.content
            
            return f"{resposta}\n\n[INFO] AVISO: Resposta gerada por LLM sem fonte documental."
        
        else:
            # RAG encontrou documentos! Usar contexto
            print(f"[RAG] [INFO] Contexto recuperado ({len(contexto)} chars)")
            
            # Construir prompt para LLM responder baseado no contexto
            prompt_resposta = f"""Voce eh investigador PCDF especialista.

CONTEXTO RECUPERADO DOS DOCUMENTOS SINARM:
{contexto}

PERGUNTA DO USUARIO:
{pergunta_usuario}

INSTRUCOES OBRIGATORIAS:
1. Responda APENAS com base no CONTEXTO recuperado acima
2. Use linguagem tecnica e objetiva (estilo policial)
3. CITE a fonte: mencione o ID do documento usado
4. Se contexto nao responde completamente, diga o que sabe e o que falta
5. NUNCA invente informacao que nao esta no contexto

FORMATO DA RESPOSTA:
[Sua resposta aqui baseada no contexto]

(Fonte: SINARM registro ID [numero do documento])

RESPOSTA:"""
            
            resposta = llm.invoke(prompt_resposta)
            
            # Converter AIMessage para string
            if hasattr(resposta, 'content'):
                resposta = resposta.content
            
            return resposta
    
    else:
        return "Nao consegui identificar o tipo de pergunta."


# ============================================================================
# MAIN (para teste rápido)
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTE RÁPIDO - AGENTE v4.7")
    print("="*70 + "\n")
    
    perguntas_teste = [
        "Quantas armas Taurus?",
        "O que é calibre?",
        "Quantas Glock 9mm?",
        "Há mais Taurus ou Glock?"
    ]
    
    for pergunta in perguntas_teste:
        print("\n" + "="*70)
        resposta = agente_v4_7_rag_fewshot_cot(pergunta)
        print(f"\nRESPOSTA FINAL:\n{resposta}")
        print("="*70)
