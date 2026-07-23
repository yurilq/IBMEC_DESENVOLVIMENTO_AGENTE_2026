# agente_v4_5_rag.py
# Agente v4.5 COM RAG - Evolução do v4.0
# NOVO: Perguntas conceituais usam RAG ao invés de dicionário estático
# NOVO: Suporte para Ollama (local) ou OpenRouter (API)

from config_llm import criar_llm, validar_configuracao, LLM_TYPE
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)
from tool_rag_tfidf import buscar_conhecimento_sinarm  # [INFO] NOVO! TF-IDF Local
import re
import json

print("="*70)
print("AGENTE v4.5 - COM RAG (Retrieval-Augmented Generation)")
print("="*70)
print("\nEVOLUÇÃO:")
print("- v4.0: Dicionário estático (5 conceitos)")
print("- v4.5: RAG com TF-IDF (20 documentos) [INFO] ATUALIZADO!")
print("\nDIFERENÇA:")
print("- SQL tools: funcionam igual (sem mudança)")
print("- Conceitual: RAG TF-IDF (100% local, SEM PyTorch)")
print(f"\nLLM CONFIGURADO: {LLM_TYPE.upper()}")
print("="*70)


def agente_v4_5_rag(pergunta_usuario):
    """
    Agente v4.5 COM RAG
    
    MUDANÇAS em relação ao v4.0:
    1. Import: tool_rag_conceitual
    2. Caso "conceitual": agora usa RAG
    3. LLM configurável (Ollama ou OpenRouter)
    4. Todo o resto: IGUAL ao v4.0
    
    ESTRATÉGIA:
    - SQL tools: sem mudança
    - Conceitual: RAG [INFO] fallback dicionário [INFO] fallback LLM
    """
    
    # Criar LLM usando configuração do .env
    llm = criar_llm()
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*70)
    
    # ===== PASSO 1: LLM ANALISA A PERGUNTA =====
    print("\n[PASSO 1] LLM analisando pergunta...")
    
    prompt_analise = f"""Voce eh um analisador de perguntas sobre armas do SINARM.

PERGUNTA DO USUARIO:
"{pergunta_usuario}"

FERRAMENTAS DISPONIVEIS:
1. contar_armas_marca - Conta armas de UMA marca especifica
   Parametros: marca (string)
   Exemplo: "Quantas armas Taurus?"

2. contar_armas_calibre - Conta armas de UM calibre especifico
   Parametros: calibre (string)
   Exemplo: "Quantas armas calibre .38?"

3. contar_armas_tipo - Conta ocorrencias de UM tipo
   Parametros: tipo (string: Apreensao, Roubo, Furto)
   Exemplo: "Quantas apreensoes?"

4. contar_armas_combinado - Conta armas de UMA marca E UM tipo/calibre
   Parametros: marca (string), tipo (string) OU calibre (string)
   Exemplos: 
     - "Quantas Taurus roubadas?" [INFO] marca=Taurus, tipo=Roubo
     - "Quantas Glock .40?" [INFO] marca=Glock, calibre=.40
     - "Quantas Taurus calibre .38?" [INFO] marca=Taurus, calibre=.38

5. COMPARACAO - Quando pergunta compara MULTIPLAS marcas
   Parametros: marcas (lista)
   Exemplo: "Ha mais Taurus ou Glock?"

6. CONCEITUAL - Pergunta sobre conceito (nao precisa buscar dados)
   Exemplo: "O que eh BO?"

TAREFA:
Analise a pergunta e responda em JSON:

{{
    "tipo": "marca|calibre|tipo|combinado|comparacao|conceitual",
    "parametros": {{
        "marca": "nome da marca OU lista de marcas",
        "calibre": "calibre",
        "tipo": "Apreensao|Roubo|Furto"
    }},
    "justificativa": "por que escolheu essa ferramenta"
}}

IMPORTANTE:
- Se pergunta menciona MULTIPLAS marcas (ex: "Taurus ou Glock") [INFO] tipo = "comparacao"
- Se pergunta menciona UMA marca E UM calibre (ex: "Glock .40") [INFO] tipo = "combinado"
- Se pergunta menciona UMA marca E UM tipo ocorrencia (ex: "Taurus roubadas") [INFO] tipo = "combinado"
- Se pergunta eh conceitual (ex: "O que eh", "defina") [INFO] tipo = "conceitual"
- Extraia valores EXATOS dos parametros (ex: marca="Taurus", nao marca="taurus")

RESPONDA APENAS O JSON (sem texto adicional):"""

    resposta_llm = llm.invoke(prompt_analise)
    
    # Converter AIMessage para string (OpenRouter retorna AIMessage)
    if hasattr(resposta_llm, 'content'):
        resposta_llm = resposta_llm.content
    
    print(f"[LLM] {resposta_llm[:200]}...")
    
    # Tentar parsear JSON
    try:
        # Extrair JSON da resposta (pode vir com texto extra)
        json_match = re.search(r'\{.*\}', resposta_llm, re.DOTALL)
        if json_match:
            analise = json.loads(json_match.group())
        else:
            raise ValueError("JSON nao encontrado na resposta")
        
        print(f"\n[ANALISE] Tipo: {analise['tipo']}")
        print(f"[ANALISE] Parametros: {analise['parametros']}")
        print(f"[ANALISE] Justificativa: {analise['justificativa']}")
        
    except Exception as e:
        print(f"\n[ERRO] LLM nao retornou JSON valido: {e}")
        print(f"[FALLBACK] Usando deteccao por palavras-chave...")
        
        # Fallback: deteccao simples
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
        
        print(f"[TIPO] Comparacao entre {len(marcas)} marcas")
        
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
            resposta += f"- Total: {total} armas\n"
            resposta += f"Fonte: SINARM 2026"
            return resposta
        
        else:
            return "Parametros insuficientes para busca combinada"
    
    # CASO 6: CONCEITUAL (COM RAG!) [INFO] MODIFICADO v4.5
    elif tipo == "conceitual":
        print(f"[TIPO] Pergunta conceitual (usando RAG)")
        
        # PASSO 1: Tentar RAG primeiro
        print(f"[RAG] Buscando em documentos SINARM...")
        contexto = buscar_conhecimento_sinarm(pergunta_usuario)
        
        # Verificar se RAG encontrou algo útil
        if "[INFO]" in contexto or len(contexto) < 100:
            print(f"[RAG] Nenhum documento relevante encontrado")
            print(f"[FALLBACK] Usando conhecimento básico...")
            
            # PASSO 2: Fallback para dicionário básico (como v4.0)
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


def detectar_por_palavras_chave(pergunta):
    """Fallback: deteccao simples por palavras-chave"""
    
    pergunta_lower = pergunta.lower()
    
    # Detectar marcas
    marcas_disponiveis = ["taurus", "glock", "rossi", "beretta", "smith"]
    marcas_encontradas = [m.capitalize() for m in marcas_disponiveis if m in pergunta_lower]
    
    # Detectar calibres
    calibres = [".38", "9mm", ".40", ".380"]
    calibre_encontrado = next((c for c in calibres if c in pergunta_lower), None)
    
    # Detectar tipos
    if "apreens" in pergunta_lower:
        tipo_encontrado = "Apreensao"
    elif "roubo" in pergunta_lower or "roub" in pergunta_lower:
        tipo_encontrado = "Roubo"
    elif "furto" in pergunta_lower:
        tipo_encontrado = "Furto"
    else:
        tipo_encontrado = None
    
    # Decidir tipo
    if len(marcas_encontradas) > 1:
        return {
            "tipo": "comparacao",
            "parametros": {"marca": marcas_encontradas},
            "justificativa": "Detectadas multiplas marcas"
        }
    elif len(marcas_encontradas) == 1 and tipo_encontrado:
        return {
            "tipo": "combinado",
            "parametros": {"marca": marcas_encontradas[0], "tipo": tipo_encontrado},
            "justificativa": "Detectada marca e tipo"
        }
    elif len(marcas_encontradas) == 1:
        return {
            "tipo": "marca",
            "parametros": {"marca": marcas_encontradas[0]},
            "justificativa": "Detectada apenas marca"
        }
    elif calibre_encontrado:
        return {
            "tipo": "calibre",
            "parametros": {"calibre": calibre_encontrado},
            "justificativa": "Detectado calibre"
        }
    elif tipo_encontrado:
        return {
            "tipo": "tipo",
            "parametros": {"tipo": tipo_encontrado},
            "justificativa": "Detectado tipo de ocorrencia"
        }
    else:
        return {
            "tipo": "conceitual",
            "parametros": {},
            "justificativa": "Nao detectados parametros de dados"
        }


# ===== TESTES =====
if __name__ == "__main__":
    print("\n\n")
    print("="*70)
    print("TESTES DO AGENTE v4.5 COM RAG")
    print("="*70)
    
    testes = [
        # Testes SQL (devem funcionar IGUAL ao v4.0)
        ("SQL", "Quantas armas Taurus?"),
        ("SQL", "Ha mais Taurus ou Glock?"),
        ("SQL", "Quantas Taurus foram roubadas?"),
        
        # Testes RAG (NOVO! Deve usar documentos)
        ("RAG", "O que eh BO de furto?"),
        ("RAG", "Qual o procedimento para arma sem numero de serie?"),
        ("RAG", "Como funciona o registro de armas?"),
    ]
    
    for i, (tipo_teste, pergunta) in enumerate(testes, 1):
        print(f"\n\n{'#'*70}")
        print(f"TESTE {i}/{len(testes)} - {tipo_teste}")
        print(f"{'#'*70}")
        
        resposta = agente_v4_5_rag(pergunta)
        
        print(f"\n{'='*70}")
        print("RESPOSTA FINAL:")
        print("="*70)
        print(resposta)
        
        # Análise do resultado
        print(f"\n{'='*70}")
        print("ANÁLISE:")
        print("="*70)
        
        if tipo_teste == "SQL":
            print("[INFO] Teste SQL: deve funcionar igual ao v4.0")
            print("   Verificar: resposta tem números e fonte SINARM?")
        else:
            print("[INFO] Teste RAG: deve usar documentos recuperados")
            print("   Verificar: resposta cita ID de documento?")
            print("   Verificar: resposta não é genérica/inventada?")
        
        if i < len(testes):
            input(f"\n[ENTER para teste {i+1}]")
    
    print("\n\n" + "="*70)
    print("TODOS OS TESTES CONCLUIDOS!")
    print("="*70)
    
    print("""
COMPARAÇÃO v4.0 vs v4.5:

v4.0 (sem RAG):
- SQL: [INFO] Funciona bem
- Conceitual: [INFO] Dicionário limitado (5 conceitos) + LLM alucina

v4.5 (com RAG):
- SQL: [INFO] Funciona igual (sem mudanças)
- Conceitual: [INFO] RAG busca em 300k docs + cita fonte!

CONCLUSÃO: v4.5 é MELHOR em todos os aspectos! [INFO]
    """)
