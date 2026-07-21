# agente_v4_0_inteligente.py
# Agente v4.0 que USA O LLM para escolher ferramentas
# Resolve: "Os alunos dizem que o agente nao consegue escolher a ferramenta correta"

from langchain_ollama import OllamaLLM
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)
import re
import json

print("="*70)
print("AGENTE v4.0 - Usa LLM para Escolher Ferramentas")
print("="*70)
print("\nDIFERENCAL:")
print("- v3.0: Busca palavras-chave (limitado)")
print("- v4.0: LLM entende a pergunta e escolhe ferramenta (inteligente)")
print("="*70)


def agente_v4_0_inteligente(pergunta_usuario):
    """
    Agente v4.0 que USA O LLM para:
    1. Entender a pergunta
    2. Escolher a ferramenta correta
    3. Extrair parametros
    4. Formatar resposta
    
    PROBLEMA RESOLVIDO:
    - v3.0 usava apenas palavras-chave (if "taurus" in pergunta)
    - v4.0 usa LLM para entender CONTEXTO da pergunta
    """
    
    # Criar LLM novo (sem vazamento de contexto)
    llm = OllamaLLM(
        model="llama3",
        temperature=0,
        num_ctx=4096
    )
    
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

4. contar_armas_combinado - Conta armas de UMA marca E UM tipo
   Parametros: marca (string), tipo (string)
   Exemplo: "Quantas Taurus roubadas?"

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
- Se pergunta menciona MULTIPLAS marcas (ex: "Taurus ou Glock") → tipo = "comparacao"
- Se pergunta eh conceitual (ex: "O que eh", "defina") → tipo = "conceitual"
- Extraia valores EXATOS dos parametros (ex: marca="Taurus", nao marca="taurus")

RESPONDA APENAS O JSON (sem texto adicional):"""

    resposta_llm = llm.invoke(prompt_analise)
    
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
            print(f"    → {marca}: {total:,} armas")
        
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
    
    # CASO 6: CONCEITUAL
    elif tipo == "conceitual":
        print(f"[TIPO] Pergunta conceitual (sem busca de dados)")
        
        conhecimento = {
            "bo": "BO (Boletim de Ocorrencia) eh registro policial de crime.",
            "furto": "Furto eh apropriacao SEM violencia.",
            "roubo": "Roubo eh apropriacao COM violencia.",
            "calibre": "Calibre eh diametro do cano da arma.",
            "apreensao": "Apreensao eh retirada de arma de circulacao pela policia."
        }
        
        pergunta_lower = pergunta_usuario.lower()
        for conceito, definicao in conhecimento.items():
            if conceito in pergunta_lower:
                return f"{definicao}\nFonte: Manual PCDF"
        
        # Se nao encontrou conceito, usar LLM
        prompt = f"Voce eh investigador PCDF. Responda de forma tecnica e objetiva: {pergunta_usuario}"
        return llm.invoke(prompt)
    
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
    print("TESTES DO AGENTE v4.0")
    print("="*70)
    
    testes = [
        "Quantas armas Taurus?",
        "Ha mais Taurus ou Glock?",
        "Quantas Taurus foram roubadas?",
        "Quantas armas calibre .38?",
        "Quantas apreensoes?",
        "O que eh BO de furto?",
    ]
    
    for i, pergunta in enumerate(testes, 1):
        print(f"\n\n{'#'*70}")
        print(f"TESTE {i}/{len(testes)}")
        print(f"{'#'*70}")
        
        resposta = agente_v4_0_inteligente(pergunta)
        
        print(f"\n{'='*70}")
        print("RESPOSTA FINAL:")
        print("="*70)
        print(resposta)
        
        if i < len(testes):
            input(f"\n[ENTER para teste {i+1}]")
    
    print("\n\n" + "="*70)
    print("TODOS OS TESTES CONCLUIDOS!")
    print("="*70)
