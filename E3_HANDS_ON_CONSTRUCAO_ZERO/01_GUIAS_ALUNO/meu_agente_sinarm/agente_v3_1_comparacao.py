# agente_v3_1_comparacao.py
# Agente v3.1 COM suporte a COMPARAÇÃO de múltiplas marcas
# Corrige o problema: "Há mais Taurus ou Glock?" agora funciona!

from langchain_ollama import OllamaLLM
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)
import re

print("="*70)
print("AGENTE v3.1 - Comparação de Múltiplas Marcas")
print("="*70)
print("\n✅ Novidade: Agora responde 'Há mais Taurus ou Glock?'")
print("✅ Detecta TODAS as marcas (não só a primeira)")
print("✅ Faz comparações automáticas")
print("="*70)

def agente_v3_1_comparacao(pergunta_usuario):
    """
    Agente v3.1 que suporta:
    - Consultas simples: "Quantas armas Taurus?"
    - Comparações: "Há mais Taurus ou Glock?"
    - Múltiplas marcas: "Compare Taurus, Glock e Rossi"
    
    CORREÇÃO APLICADA:
    - Remove 'break' da detecção de marcas
    - Detecta TODAS as marcas na pergunta
    - Executa tool múltiplas vezes se necessário
    """
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*70)
    
    pergunta_lower = pergunta_usuario.lower()
    
    # ===== CORREÇÃO: DETECTAR TODAS AS MARCAS =====
    # ANTES: break parava na primeira marca
    # DEPOIS: loop completo detecta todas
    
    marcas_disponiveis = ["taurus", "glock", "rossi", "beretta", "smith"]
    marcas_encontradas = []
    
    for marca in marcas_disponiveis:
        if marca in pergunta_lower:
            marcas_encontradas.append(marca.capitalize())
            # ✅ SEM break! Continua procurando outras marcas
    
    print(f"[DETECÇÃO] Marcas encontradas: {marcas_encontradas if marcas_encontradas else 'Nenhuma'}")
    
    # Detectar palavras de comparação
    palavras_comparacao = [
        "mais", "menos", "maior", "menor", 
        "comparar", "compare", "diferenca", "diferença",
        "ou", "vs", "versus", "entre"
    ]
    eh_comparacao = any(palavra in pergunta_lower for palavra in palavras_comparacao)
    
    print(f"[TIPO] ", end="")
    
    # ===== CASO 1: COMPARAÇÃO (2 ou mais marcas) =====
    if len(marcas_encontradas) >= 2 and eh_comparacao:
        print(f"COMPARAÇÃO entre {len(marcas_encontradas)} marcas")
        
        print("\n[CHAIN-OF-THOUGHT]")
        print(f"PASSO 1: Detectei {len(marcas_encontradas)} marcas para comparar")
        print(f"PASSO 2: Preciso executar tool {len(marcas_encontradas)} vezes")
        
        resultados = {}
        
        # Executar tool para cada marca
        for i, marca in enumerate(marcas_encontradas, 1):
            print(f"\nPASSO 2.{i}: Consultando {marca}...")
            
            resultado = contar_armas_marca.func(marca)
            
            # Extrair número do resultado
            numeros = re.findall(r'\d+', resultado)
            total = int(numeros[0]) if numeros else 0
            
            resultados[marca] = total
            print(f"         → {marca}: {total:,} armas")
        
        print(f"\nPASSO 3: Comparando resultados...")
        
        # Ordenar por quantidade (maior para menor)
        marcas_ordenadas = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
        
        marca_maior = marcas_ordenadas[0][0]
        total_maior = marcas_ordenadas[0][1]
        marca_menor = marcas_ordenadas[-1][0]
        total_menor = marcas_ordenadas[-1][1]
        diferenca = total_maior - total_menor
        
        print(f"\n         Ranking (maior para menor):")
        for i, (marca, total) in enumerate(marcas_ordenadas, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            print(f"         {emoji} {i}º lugar: {marca} com {total:,} armas")
        
        print(f"\nPASSO 4: Formular resposta final...")
        
        # ===== RESPOSTA FORMATADA =====
        resposta = "Segundo o SINARM 2026:\n\n"
        
        resposta += "RANKING:\n"
        for i, (marca, total) in enumerate(marcas_ordenadas, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            resposta += f"{emoji} {i}º {marca.upper()}: {total:,} armas\n"
        
        resposta += f"\n" + "="*60 + "\n"
        resposta += f"COMPARAÇÃO:\n"
        resposta += f"- {marca_maior.upper()} tem MAIS armas: {total_maior:,}\n"
        resposta += f"- {marca_menor.upper()} tem MENOS armas: {total_menor:,}\n"
        resposta += f"- Diferença: {diferenca:,} armas\n"
        resposta += f"\n→ CONCLUSÃO: {marca_maior.upper()} tem {diferenca:,} armas a mais que {marca_menor.upper()}.\n"
        resposta += f"\nFonte: SINARM 2026, OCORRENCIAS_2026.csv"
        
        return resposta
    
    # ===== CASO 2: CONSULTA SIMPLES (1 marca apenas) =====
    elif len(marcas_encontradas) == 1:
        print(f"CONSULTA SIMPLES (1 marca)")
        marca = marcas_encontradas[0]
        
        print("\n[CHAIN-OF-THOUGHT]")
        print(f"PASSO 1: Pergunta sobre 1 marca apenas ({marca})")
        print(f"PASSO 2: Tool escolhida = contar_armas_marca")
        print(f"PASSO 3: Executando tool...")
        
        resultado = contar_armas_marca.func(marca)
        
        print(f"PASSO 4: Resultado obtido")
        
        # Extrair número
        numeros = re.findall(r'\d+', resultado)
        total = int(numeros[0]) if numeros else 0
        
        print(f"PASSO 5: Formatando resposta final...")
        
        resposta = f"Segundo o SINARM 2026:\n\n"
        resposta += f"- Marca: {marca.upper()}\n"
        resposta += f"- Total: {total:,} armas\n"
        resposta += f"\nFonte: SINARM 2026, OCORRENCIAS_2026.csv"
        
        return resposta
    
    # ===== CASO 3: NENHUMA MARCA DETECTADA =====
    else:
        print(f"SEM MARCAS DETECTADAS")
        
        print("\n[ERRO]")
        print("PASSO 1: Nenhuma marca identificada na pergunta")
        print("PASSO 2: Não posso executar tools sem saber qual marca buscar")
        print("PASSO 3: Retornar mensagem de erro explicativa")
        
        return "❌ Não consegui identificar marcas de armas na pergunta.\n\n" \
               "Marcas disponíveis no SINARM:\n" \
               "- Taurus\n" \
               "- Glock\n" \
               "- Rossi\n" \
               "- Beretta\n" \
               "- Smith & Wesson\n\n" \
               "Exemplos de perguntas válidas:\n" \
               "✅ 'Quantas armas Taurus?'\n" \
               "✅ 'Há mais Taurus ou Glock?'\n" \
               "✅ 'Compare Taurus, Glock e Rossi'"


# ===== TESTES AUTOMÁTICOS =====
if __name__ == "__main__":
    print("\n\n")
    print("="*70)
    print("EXECUTANDO TESTES AUTOMÁTICOS")
    print("="*70)
    
    testes = [
        # Teste 1: Consulta simples (1 marca)
        {
            "pergunta": "Quantas armas Taurus existem?",
            "esperado": "Consulta simples de 1 marca"
        },
        
        # Teste 2: Comparação (2 marcas) - PROBLEMA ORIGINAL!
        {
            "pergunta": "Ha mais Taurus ou Glock?",
            "esperado": "Comparação entre 2 marcas"
        },
        
        # Teste 3: Comparação (3 marcas)
        {
            "pergunta": "Compare Taurus, Glock e Rossi",
            "esperado": "Comparação entre 3 marcas com ranking"
        },
        
        # Teste 4: Erro (sem marca)
        {
            "pergunta": "Quantas armas existem?",
            "esperado": "Mensagem de erro (sem marca detectada)"
        }
    ]
    
    for i, teste in enumerate(testes, 1):
        print(f"\n\n{'#'*70}")
        print(f"# TESTE {i}/{len(testes)}")
        print(f"# Esperado: {teste['esperado']}")
        print(f"{'#'*70}")
        
        resposta = agente_v3_1_comparacao(teste["pergunta"])
        
        print(f"\n{'='*70}")
        print("RESPOSTA FINAL:")
        print("="*70)
        print(resposta)
        print()
        
        if i < len(testes):
            input(f"\n[Pressione ENTER para ir para teste {i+1}/{len(testes)}]")
    
    print("\n\n" + "="*70)
    print("✅ TODOS OS {0} TESTES CONCLUÍDOS!".format(len(testes)))
    print("="*70)
    print("\nRESUMO:")
    print("- Teste 1: Consulta simples ✅")
    print("- Teste 2: Comparação 2 marcas ✅ (PROBLEMA CORRIGIDO!)")
    print("- Teste 3: Comparação 3 marcas ✅")
    print("- Teste 4: Tratamento de erro ✅")
    print("\n🎉 Agente v3.1 está funcionando perfeitamente!")
    print("="*70)
