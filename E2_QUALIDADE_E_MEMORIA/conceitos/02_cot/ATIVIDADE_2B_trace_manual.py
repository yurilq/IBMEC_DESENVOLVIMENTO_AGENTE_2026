"""
ATIVIDADE 2B: ESCREVER TRACE COT MANUALMENTE
Encontro 2 - Conceito: Chain-of-Thought (CoT)
Duração: 10 minutos

OBJETIVO:
Praticar a escrita de raciocínio passo-a-passo (CoT trace) manualmente,
antes de implementar no agente.

O QUE VOCÊ VAI FAZER:
1. Receber 2 queries complexas (ATIVIDADE_2A)
2. Escrever o trace CoT completo para cada uma
3. Seguir template de 4 seções: Pensamento → Ação → Observação → Resposta
4. Validar trace com checklist de qualidade

POR QUE ISSO É IMPORTANTE:
- Entender CoT "na mão" antes de automatizar
- Desenvolver intuição sobre raciocínio estruturado
- Criar exemplos de alta qualidade para Few-Shot+CoT
- Debugging: se agente erra, você saberá qual etapa falhou

CONCEITO: Anatomia de um Trace CoT

┌──────────────────────────────────────────────────────────────┐
│ TEMPLATE CoT (4 SEÇÕES)                                      │
├──────────────────────────────────────────────────────────────┤
│ 1. PENSAMENTO (Thought)                                      │
│    O que preciso fazer? Qual a estratégia?                  │
│    Quais datasets? Quais filtros? Quais cálculos?           │
│                                                              │
│ 2. AÇÃO (Action)                                             │
│    Executar tool call específica                            │
│    buscar_[dataset]("campo:valor")                          │
│                                                              │
│ 3. OBSERVAÇÃO (Observation)                                  │
│    O que a tool retornou?                                   │
│    Quantos registros? Valores relevantes?                   │
│                                                              │
│ 4. RESPOSTA (Answer - se tiver info suficiente)             │
│    Resposta final formatada para o usuário                  │
│    OU "Preciso de mais dados..." → volta para Pensamento    │
└──────────────────────────────────────────────────────────────┘

EXEMPLO COMPLETO:

Query: "Qual marca tem maior taxa de furto em relação a registros ativos no DF?"

═══════════════════════════════════════════════════════════════
PENSAMENTO 1:
Preciso calcular taxa de furto = (furtos / registros) para cada marca.
Estratégia:
1. Buscar furtos no DF (dataset OCORRENCIAS)
2. Buscar registros ativos no DF (dataset REGISTROS)
3. Cruzar dados por marca
4. Calcular taxa para cada marca
5. Retornar marca com maior taxa

Começando com furtos...
───────────────────────────────────────────────────────────────
AÇÃO 1:
buscar_ocorrencias("tipo:Furto")
───────────────────────────────────────────────────────────────
OBSERVAÇÃO 1:
Retornou 18.347 furtos. Filtrando uf=DF: 1.256 furtos no DF.
Marcas encontradas:
  - Taurus: 487 furtos
  - Glock: 312 furtos
  - Beretta: 189 furtos
  - Imbel: 147 furtos
  - Outras: 121 furtos

Preciso agora buscar registros ativos...
═══════════════════════════════════════════════════════════════
PENSAMENTO 2:
Agora busco registros ativos no DF para calcular a taxa.
───────────────────────────────────────────────────────────────
AÇÃO 2:
buscar_registros("status:Ativo")
───────────────────────────────────────────────────────────────
OBSERVAÇÃO 2:
Retornou 9.847 registros ativos. Filtrando uf=DF: 2.134 no DF.
Marcas encontradas:
  - Taurus: 1.289 registros
  - Glock: 487 registros
  - Beretta: 198 registros
  - Imbel: 102 registros
  - Outras: 58 registros

Agora posso calcular as taxas...
═══════════════════════════════════════════════════════════════
PENSAMENTO 3:
Calculando taxa de furto = (furtos / registros) * 100 para cada marca:

Marca       Furtos    Registros    Taxa
Taurus      487       1.289        37,8%
Glock       312       487          64,1%  ← MAIOR
Beretta     189       198          95,5%  ← MAIOR AINDA!
Imbel       147       102          144,1% ← IMPOSSÍVEL! Erro nos dados?
Outras      121       58           208,6% ← IMPOSSÍVEL!

ANÁLISE: Taxas >100% indicam mais furtos que registros, possível porque:
- Furtos incluem armas não registradas (ilegais)
- Armas podem ser furtadas múltiplas vezes
- Dados de anos diferentes

Considerando apenas marcas principais (Taurus, Glock, Beretta):
Beretta tem maior taxa: 95,5%
───────────────────────────────────────────────────────────────
RESPOSTA FINAL:
Beretta tem a maior taxa de furto em relação a registros ativos no DF: 
95,5% (189 furtos para 198 registros).

Isso significa que para cada 100 armas Beretta registradas no DF, 
aproximadamente 95 foram furtadas em 2026.

Observação: Marcas menos comuns (Imbel, Outras) apresentam taxas >100%, 
indicando que furtos incluem armas não registradas ou de outros estados.

Fonte: SINARM/OCORRENCIAS + SINARM/REGISTROS.
═══════════════════════════════════════════════════════════════

CHECKLIST QUALIDADE:
✓ Pensamento explicita estratégia completa?
✓ Ações usam tools corretas com sintaxe certa?
✓ Observações registram dados numéricos relevantes?
✓ Raciocínio é sequencial e lógico?
✓ Resposta final é clara e completa?
✓ Fonte citada?
✓ Edge cases considerados (taxas >100%, dados ausentes)?
"""

from pathlib import Path
import json

# ========== QUERIES PARA PRATICAR ==========

QUERIES_COT_PRATICA = [
    {
        "id": 1,
        "query": "Compare a proporção de pistolas vs revólveres em portes válidos e registros ativos.",
        "dica": "Precisa buscar 2 datasets (PORTES e REGISTROS), calcular proporção em cada um, depois comparar.",
        "template": """
═══════════════════════════════════════════════════════════════
PENSAMENTO 1:
[Sua estratégia aqui - qual dataset? quais filtros? qual cálculo?]
───────────────────────────────────────────────────────────────
AÇÃO 1:
[Tool call aqui - ex: buscar_portes("status:Válido")]
───────────────────────────────────────────────────────────────
OBSERVAÇÃO 1:
[O que a tool retornou? Quantas pistolas? Quantos revólveres?]
═══════════════════════════════════════════════════════════════
PENSAMENTO 2:
[Próximo passo - buscar registros? calcular proporção?]
───────────────────────────────────────────────────────────────
AÇÃO 2:
[Tool call]
───────────────────────────────────────────────────────────────
OBSERVAÇÃO 2:
[Resultado]
═══════════════════════════════════════════════════════════════
PENSAMENTO 3:
[Cálculo das proporções]
───────────────────────────────────────────────────────────────
RESPOSTA FINAL:
[Resposta completa, formatada, com fonte]
═══════════════════════════════════════════════════════════════
"""
    },
    {
        "id": 2,
        "query": "Qual marca tem a maior diferença entre número de registros ativos e número de furtos no DF?",
        "dica": "Buscar REGISTROS (status:Ativo, uf:DF), buscar OCORRENCIAS (tipo:Furto, uf:DF), calcular diferença por marca, ranquear.",
        "template": """
═══════════════════════════════════════════════════════════════
PENSAMENTO 1:
[Estratégia: quais datasets? quais filtros? como calcular diferença?]
───────────────────────────────────────────────────────────────
AÇÃO 1:
[buscar_registros(...)]
───────────────────────────────────────────────────────────────
OBSERVAÇÃO 1:
[Resultados por marca]
═══════════════════════════════════════════════════════════════
PENSAMENTO 2:
[...]
───────────────────────────────────────────────────────────────
AÇÃO 2:
[buscar_ocorrencias(...)]
───────────────────────────────────────────────────────────────
OBSERVAÇÃO 2:
[...]
═══════════════════════════════════════════════════════════════
PENSAMENTO 3:
[Calcular diferença = registros - furtos para cada marca]
───────────────────────────────────────────────────────────────
RESPOSTA FINAL:
[Marca com maior diferença + números]
═══════════════════════════════════════════════════════════════
"""
    }
]

# ========== VALIDAÇÃO TRACE ==========

def validar_trace_cot(trace_texto):
    """
    Valida qualidade do trace CoT escrito pelo aluno.
    
    Retorna: (is_valid, erros[], pontuacao)
    """
    
    erros = []
    pontuacao = 0
    
    # Check 1: Tem seções PENSAMENTO?
    pensamentos = trace_texto.upper().count("PENSAMENTO")
    if pensamentos >= 2:
        pontuacao += 2
    elif pensamentos == 1:
        pontuacao += 1
        erros.append("⚠️  Apenas 1 PENSAMENTO (ideal: 2-3 para query complexa)")
    else:
        erros.append("❌ Nenhum PENSAMENTO encontrado")
    
    # Check 2: Tem seções AÇÃO?
    acoes = trace_texto.upper().count("AÇÃO") + trace_texto.upper().count("ACAO")
    if acoes >= 2:
        pontuacao += 2
    elif acoes == 1:
        pontuacao += 1
        erros.append("⚠️  Apenas 1 AÇÃO (ideal: 2+ para query complexa)")
    else:
        erros.append("❌ Nenhuma AÇÃO encontrada")
    
    # Check 3: Tem seções OBSERVAÇÃO?
    observacoes = trace_texto.upper().count("OBSERVAÇÃO") + trace_texto.upper().count("OBSERVACAO")
    if observacoes >= 2:
        pontuacao += 2
    elif observacoes == 1:
        pontuacao += 1
        erros.append("⚠️  Apenas 1 OBSERVAÇÃO")
    else:
        erros.append("❌ Nenhuma OBSERVAÇÃO encontrada")
    
    # Check 4: Tem RESPOSTA FINAL?
    if "RESPOSTA FINAL" in trace_texto.upper() or "ANSWER" in trace_texto.upper():
        pontuacao += 2
    else:
        erros.append("❌ Faltou RESPOSTA FINAL")
    
    # Check 5: Usa tools SINARM?
    tools_validas = ["buscar_ocorrencias", "buscar_portes", "buscar_registros", "buscar_requerimentos"]
    tools_usadas = sum(1 for tool in tools_validas if tool in trace_texto)
    if tools_usadas >= 2:
        pontuacao += 2
    elif tools_usadas == 1:
        pontuacao += 1
    else:
        erros.append("❌ Não usa tools SINARM válidas")
    
    # Check 6: Tem números/dados (evidência de cálculo)?
    import re
    numeros = re.findall(r'\d+', trace_texto)
    if len(numeros) >= 5:
        pontuacao += 1
    else:
        erros.append("⚠️  Poucos números/dados (trace vago)")
    
    # Check 7: Cita fonte?
    if "SINARM" in trace_texto.upper() or "Fonte:" in trace_texto:
        pontuacao += 1
    else:
        erros.append("⚠️  Não cita fonte dos dados")
    
    # Avaliar
    max_pontos = 12
    percentual = (pontuacao / max_pontos) * 100
    
    return (len(erros) == 0, erros, pontuacao, percentual)

# ========== INTERFACE PRÁTICA ==========

def praticar_trace_cot(query_info):
    """Interface para aluno escrever trace CoT."""
    
    print(f"\n{'='*70}")
    print(f"QUERY {query_info['id']}: {query_info['query']}")
    print("="*70)
    print(f"\n💡 DICA: {query_info['dica']}")
    print("\n📝 TEMPLATE:\n")
    print(query_info['template'])
    
    print("\n" + "="*70)
    print("Escreva seu trace CoT seguindo o template acima.")
    print("Quando terminar, salve em um arquivo .txt e informe o caminho.")
    print("="*70)
    
    caminho_arquivo = input("\nCaminho do arquivo (ou ENTER para digitar aqui): ").strip()
    
    if caminho_arquivo:
        # Ler de arquivo
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                trace = f.read()
        except FileNotFoundError:
            print("❌ Arquivo não encontrado.")
            return None
    else:
        # Digitar aqui
        print("\nDigite seu trace (termine com linha contendo apenas 'FIM'):")
        linhas = []
        while True:
            linha = input()
            if linha.strip().upper() == "FIM":
                break
            linhas.append(linha)
        trace = "\n".join(linhas)
    
    # Validar
    print("\n🔍 VALIDANDO TRACE...")
    valido, erros, pontos, percentual = validar_trace_cot(trace)
    
    print(f"\n{'='*70}")
    print(f"AVALIAÇÃO DO TRACE")
    print("="*70)
    print(f"Pontuação: {pontos}/12 ({percentual:.0f}%)")
    
    if valido:
        print("\n✅ TRACE VÁLIDO!")
    else:
        print(f"\n⚠️  TRACE TEM {len(erros)} PROBLEMAS:")
        for erro in erros:
            print(f"   {erro}")
    
    if percentual >= 80:
        print("\n🎉 EXCELENTE! Trace CoT de alta qualidade.")
    elif percentual >= 60:
        print("\n✅ BOM! Pequenos ajustes melhorariam ainda mais.")
    else:
        print("\n⚠️  REVISE: Faltam elementos importantes do CoT.")
    
    # Salvar
    caminho_output = Path(__file__).parent / f"trace_cot_query{query_info['id']}.txt"
    with open(caminho_output, "w", encoding="utf-8") as f:
        f.write(trace)
    
    print(f"\n💾 Trace salvo em: {caminho_output}")
    
    return {
        "query_id": query_info['id'],
        "pontuacao": pontos,
        "percentual": percentual,
        "valido": valido,
        "num_erros": len(erros)
    }

# ========== MAIN ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  ATIVIDADE 2B: ESCREVER TRACE COT MANUALMENTE                ║
║  Encontro 2 - Chain-of-Thought (CoT)                         ║
╚═══════════════════════════════════════════════════════════════╝

OBJETIVO:
Praticar raciocínio passo-a-passo (CoT) escrevendo traces manualmente.

INSTRUÇÕES:
1. Escolha uma query complexa (1 ou 2)
2. Escreva o trace CoT completo seguindo o template
3. Inclua: PENSAMENTO → AÇÃO → OBSERVAÇÃO → RESPOSTA
4. Valide com checklist automático

TEMPLATE CoT (4 SEÇÕES):
  1. PENSAMENTO: Estratégia (qual dataset? quais filtros? cálculos?)
  2. AÇÃO: Tool call específica
  3. OBSERVAÇÃO: O que a tool retornou?
  4. RESPOSTA: Resposta final formatada (ou "preciso mais dados...")

DICA: Queries complexas precisam 2-3 ciclos de Pensamento→Ação→Observação
      antes da Resposta Final.
""")
    
    print("\n📋 QUERIES DISPONÍVEIS:\n")
    for q in QUERIES_COT_PRATICA:
        print(f"{q['id']}. {q['query']}")
        print(f"   💡 {q['dica']}\n")
    
    query_id = int(input("Escolha a query (1 ou 2): ").strip())
    query_info = next((q for q in QUERIES_COT_PRATICA if q['id'] == query_id), None)
    
    if query_info:
        resultado = praticar_trace_cot(query_info)
        
        if resultado and resultado['percentual'] >= 80:
            print("\n✅ Você está pronto para ATIVIDADE 2C - Implementar CoT no Agente!")
        else:
            print("\n💪 Pratique mais uma query para dominar CoT!")
    else:
        print("❌ Query inválida.")
    
    print("\n✅ PRÓXIMO PASSO: ATIVIDADE 2C - Implementar CoT no Agente v2.5")
    print("   Você vai automatizar o raciocínio CoT que praticou aqui.\n")
