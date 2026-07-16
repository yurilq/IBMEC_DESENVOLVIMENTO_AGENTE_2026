"""
ATIVIDADE 2A: CLASSIFICAR QUERIES (Simples vs Complexa)
Encontro 2 - Conceito: Chain-of-Thought (CoT)
Duração: 15 minutos

OBJETIVO:
Aprender a identificar queries que PRECISAM de raciocínio explícito (CoT) vs
queries simples que funcionam bem com resposta direta.

O QUE VOCÊ VAI FAZER:
1. Analisar 10 queries sobre SINARM
2. Classificar cada uma como: SIMPLES, MÉDIA ou COMPLEXA
3. Justificar sua classificação usando critérios objetivos
4. Preencher tabela de análise

POR QUE ISSO É IMPORTANTE:
- CoT adiciona latência (~30%) e custo (+40% tokens)
- Usar CoT em query simples = desperdício de recursos
- NÃO usar CoT em query complexa = resposta errada/incompleta
- Classificação correta = otimização custo-benefício

CONCEITO: O que torna uma query COMPLEXA?

┌──────────────────────────────────────────────────────────────┐
│ QUERY SIMPLES (NÃO precisa CoT)                             │
├──────────────────────────────────────────────────────────────┤
│ ✓ 1 dataset                                                  │
│ ✓ 1-2 filtros                                                │
│ ✓ Resposta direta (buscar + contar)                         │
│ ✓ Sem cálculos complexos                                    │
│                                                              │
│ Exemplo: "Quantas pistolas Taurus existem?"                 │
│   → buscar_registros("marca:Taurus")                        │
│   → filtrar especie=Pistola                                 │
│   → contar                                                  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ QUERY COMPLEXA (PRECISA CoT)                                │
├──────────────────────────────────────────────────────────────┤
│ ✓ 2+ datasets (cruzamento)                                  │
│ ✓ 3+ filtros (multi-critério)                               │
│ ✓ Cálculos (taxa, média, ranking, comparação)              │
│ ✓ Múltiplas etapas (buscar → calcular → comparar)          │
│ ✓ Lógica condicional (se X então Y)                        │
│                                                              │
│ Exemplo: "Qual marca tem maior taxa de furto vs registro?"  │
│   → buscar_ocorrencias(tipo:Furto) [dataset 1]             │
│   → buscar_registros() [dataset 2]                          │
│   → agrupar por marca                                       │
│   → calcular taxa = furtos / registros                      │
│   → ranquear marcas                                         │
│   → retornar top 3                                          │
└──────────────────────────────────────────────────────────────┘

CRITÉRIOS DE CLASSIFICAÇÃO:
- Pontos de Complexidade (0-10):
  * +1 por dataset adicional
  * +1 por filtro adicional (após 1º)
  * +2 por cálculo matemático
  * +2 por cruzamento de datasets
  * +1 por agregação (soma, média, ranking)
  * +1 por condicional (if/else)

ESCALA:
  0-2 pontos: SIMPLES (não precisa CoT)
  3-5 pontos: MÉDIA (CoT opcional, mas ajuda)
  6+ pontos: COMPLEXA (CoT essencial)
"""

import json
from pathlib import Path

# ========== QUERIES PARA CLASSIFICAR ==========

QUERIES_CLASSIFICACAO = [
    {
        "id": 1,
        "query": "Quantas pistolas Taurus estão registradas?",
        "gabarito": {
            "complexidade": "SIMPLES",
            "pontos": 2,
            "justificativa": "1 dataset (REGISTROS), 2 filtros (marca+especie), resposta direta",
            "datasets": ["registros"],
            "filtros": ["marca:Taurus", "especie:Pistola"],
            "calculos": ["contar"],
            "etapas": 1
        }
    },
    {
        "id": 2,
        "query": "Qual a taxa de aprovação de requerimentos de porte no DF?",
        "gabarito": {
            "complexidade": "MÉDIA",
            "pontos": 4,
            "justificativa": "1 dataset, 2 filtros, 1 cálculo matemático (aprovados/total)",
            "datasets": ["requerimentos"],
            "filtros": ["tipo:Porte", "uf:DF", "decisao:Aprovado"],
            "calculos": ["contar aprovados", "contar total", "dividir", "percentual"],
            "etapas": 2
        }
    },
    {
        "id": 3,
        "query": "Quais marcas têm mais furtos no DF?",
        "gabarito": {
            "complexidade": "MÉDIA",
            "pontos": 3,
            "justificativa": "1 dataset, 2 filtros, agregação (group by marca)",
            "datasets": ["ocorrencias"],
            "filtros": ["tipo:Furto", "uf:DF"],
            "calculos": ["agrupar por marca", "contar por grupo", "ordenar"],
            "etapas": 2
        }
    },
    {
        "id": 4,
        "query": "Compare a proporção de pistolas vs revólveres em portes válidos e registros ativos.",
        "gabarito": {
            "complexidade": "COMPLEXA",
            "pontos": 8,
            "justificativa": "2 datasets (cruzamento), múltiplos filtros, 2 cálculos de proporção, comparação",
            "datasets": ["portes", "registros"],
            "filtros": ["status:Válido", "status:Ativo", "especie:Pistola", "especie:Revólver"],
            "calculos": ["contar pistolas PORTES", "contar revólveres PORTES", "calc proporção 1",
                        "contar pistolas REGISTROS", "contar revólveres REGISTROS", "calc proporção 2",
                        "comparar proporções"],
            "etapas": 4
        }
    },
    {
        "id": 5,
        "query": "Quantos portes válidos existem?",
        "gabarito": {
            "complexidade": "SIMPLES",
            "pontos": 1,
            "justificativa": "1 dataset, 1 filtro, resposta direta",
            "datasets": ["portes"],
            "filtros": ["status:Válido"],
            "calculos": ["contar"],
            "etapas": 1
        }
    },
    {
        "id": 6,
        "query": "Qual marca tem a maior diferença entre número de registros e número de furtos?",
        "gabarito": {
            "complexidade": "COMPLEXA",
            "pontos": 7,
            "justificativa": "2 datasets, agregação por marca em ambos, cálculo de diferença, ranking",
            "datasets": ["registros", "ocorrencias"],
            "filtros": ["tipo:Furto"],
            "calculos": ["agrupar REGISTROS por marca", "agrupar FURTOS por marca",
                        "calcular diferença (registros - furtos)", "ranquear por diferença"],
            "etapas": 3
        }
    },
    {
        "id": 7,
        "query": "Liste todas as armas calibre 9mm.",
        "gabarito": {
            "complexidade": "SIMPLES",
            "pontos": 1,
            "justificativa": "Pode usar qualquer dataset (REGISTROS mais adequado), 1 filtro",
            "datasets": ["registros"],
            "filtros": ["calibre:9mm"],
            "calculos": ["listar"],
            "etapas": 1
        }
    },
    {
        "id": 8,
        "query": "Entre as marcas com mais de 100 registros ativos, qual tem a menor taxa de requerimentos negados?",
        "gabarito": {
            "complexidade": "COMPLEXA",
            "pontos": 9,
            "justificativa": "2 datasets, filtro condicional (>100), cálculo de taxa, ranking inverso",
            "datasets": ["registros", "requerimentos"],
            "filtros": ["status:Ativo", "decisao:Negado"],
            "calculos": ["agrupar REGISTROS por marca", "filtrar marcas >100",
                        "agrupar REQUERIMENTOS por marca", "calcular taxa negados/total",
                        "ranquear (menor taxa)"],
            "etapas": 4
        }
    },
    {
        "id": 9,
        "query": "Quantas ocorrências de furto aconteceram em 2026?",
        "gabarito": {
            "complexidade": "SIMPLES",
            "pontos": 2,
            "justificativa": "1 dataset, 2 filtros (tipo+ano), resposta direta",
            "datasets": ["ocorrencias"],
            "filtros": ["tipo:Furto", "ano:2026"],
            "calculos": ["contar"],
            "etapas": 1
        }
    },
    {
        "id": 10,
        "query": "Para cada UF, calcule a média de dias entre requerimento e decisão, mas só para requerimentos aprovados de CAC.",
        "gabarito": {
            "complexidade": "COMPLEXA",
            "pontos": 7,
            "justificativa": "1 dataset, múltiplos filtros, cálculo de diferença de datas, agregação por UF, média",
            "datasets": ["requerimentos"],
            "filtros": ["decisao:Aprovado", "categoria:CAC"],
            "calculos": ["calcular dias (data_decisao - data_requerimento)",
                        "agrupar por UF", "calcular média por grupo"],
            "etapas": 3
        }
    }
]

# ========== FUNÇÃO DE ANÁLISE ==========

def analisar_query(query_info):
    """
    Ajuda o aluno a analisar uma query e classificar complexidade.
    """
    
    print(f"\n{'='*70}")
    print(f"QUERY {query_info['id']}: {query_info['query']}")
    print("="*70)
    
    print("\n🔍 ANÁLISE:")
    print("\n1. Quantos DATASETS são necessários?")
    print("   (ocorrencias, portes, registros, requerimentos)")
    datasets = input("   Digite datasets separados por vírgula: ").strip().split(',')
    datasets = [d.strip() for d in datasets]
    num_datasets = len(datasets)
    
    print("\n2. Quantos FILTROS são necessários?")
    print("   (marca:X, tipo:Y, status:Z, etc.)")
    filtros = input("   Digite filtros separados por vírgula: ").strip().split(',')
    filtros = [f.strip() for f in filtros if f.strip()]
    num_filtros = len(filtros)
    
    print("\n3. Quais CÁLCULOS são necessários?")
    print("   (contar, somar, média, taxa, ranking, diferença, etc.)")
    calculos = input("   Digite cálculos separados por vírgula: ").strip().split(',')
    calculos = [c.strip() for c in calculos if c.strip()]
    num_calculos = len(calculos)
    
    print("\n4. Quantas ETAPAS são necessárias?")
    print("   (1 etapa: buscar+contar | 2 etapas: buscar+calcular | 3+: múltiplas operações)")
    etapas = int(input("   Digite número de etapas: ").strip())
    
    # Calcular pontos
    pontos = 0
    pontos += (num_datasets - 1)  # +1 por dataset adicional
    pontos += max(0, num_filtros - 1)  # +1 por filtro adicional
    pontos += num_calculos * 1  # +1 por cálculo
    if num_datasets > 1:
        pontos += 2  # +2 por cruzamento de datasets
    if etapas > 2:
        pontos += (etapas - 2)  # +1 por etapa adicional (após 2)
    
    # Classificar
    if pontos <= 2:
        complexidade = "SIMPLES"
    elif pontos <= 5:
        complexidade = "MÉDIA"
    else:
        complexidade = "COMPLEXA"
    
    print(f"\n📊 RESULTADO DA ANÁLISE:")
    print(f"   Datasets: {num_datasets} ({', '.join(datasets)})")
    print(f"   Filtros: {num_filtros}")
    print(f"   Cálculos: {num_calculos}")
    print(f"   Etapas: {etapas}")
    print(f"   Pontos: {pontos}")
    print(f"   Complexidade: {complexidade}")
    
    # Comparar com gabarito
    gabarito = query_info['gabarito']
    acertou = (complexidade == gabarito['complexidade'])
    
    print(f"\n✅ GABARITO:")
    print(f"   Complexidade esperada: {gabarito['complexidade']} ({gabarito['pontos']} pontos)")
    print(f"   Justificativa: {gabarito['justificativa']}")
    
    if acertou:
        print(f"\n🎉 CORRETO! Você classificou corretamente.")
    else:
        print(f"\n⚠️  DIVERGÊNCIA: Sua análise diferiu do gabarito.")
        print(f"   Revise os critérios e compare com a justificativa acima.")
    
    return {
        "query_id": query_info['id'],
        "sua_classificacao": complexidade,
        "seus_pontos": pontos,
        "gabarito": gabarito['complexidade'],
        "acertou": acertou
    }

# ========== TABELA RESUMO ==========

def gerar_tabela_resumo():
    """Gera tabela resumo para o aluno preencher."""
    
    print("\n" + "="*80)
    print("TABELA DE CLASSIFICAÇÃO - QUERIES SINARM")
    print("="*80)
    print(f"{'ID':<4} {'Query (resumida)':<40} {'Datasets':<12} {'Filtros':<8} {'Calc':<6} {'Etapas':<8} {'Complex':<10}")
    print("-"*80)
    
    for q in QUERIES_CLASSIFICACAO:
        query_curta = q['query'][:37] + "..." if len(q['query']) > 40 else q['query']
        print(f"{q['id']:<4} {query_curta:<40} {'[ ]':<12} {'[ ]':<8} {'[ ]':<6} {'[ ]':<8} {'[     ]':<10}")
    
    print("-"*80)
    print("\nLEGENDA:")
    print("  Datasets: Número de datasets necessários (1-4)")
    print("  Filtros: Número de filtros (marca, tipo, status, etc.)")
    print("  Calc: Número de cálculos (contar, taxa, média, etc.)")
    print("  Etapas: Número de passos sequenciais")
    print("  Complex: SIMPLES (0-2pt), MÉDIA (3-5pt), COMPLEXA (6+pt)")
    print("\n")
    print("CRITÉRIOS DE PONTUAÇÃO:")
    print("  +1 por dataset adicional (após 1º)")
    print("  +1 por filtro adicional (após 1º)")
    print("  +1 por cálculo")
    print("  +2 por cruzamento de datasets")
    print("  +1 por etapa adicional (após 2ª)")
    print("="*80)

# ========== MAIN ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  ATIVIDADE 2A: CLASSIFICAR QUERIES (Simples vs Complexa)     ║
║  Encontro 2 - Chain-of-Thought (CoT)                         ║
╚═══════════════════════════════════════════════════════════════╝

OBJETIVO:
Aprender a identificar queries que PRECISAM de raciocínio explícito (CoT).

INSTRUÇÕES:
1. Para cada query, analise:
   - Quantos datasets?
   - Quantos filtros?
   - Quais cálculos?
   - Quantas etapas?
2. Calcule pontos de complexidade
3. Classifique: SIMPLES, MÉDIA ou COMPLEXA
4. Compare com gabarito

POR QUE ISSO IMPORTA:
- CoT é caro (+40% tokens) e lento (+30% latência)
- Use apenas quando REALMENTE necessário
- Queries simples: resposta direta
- Queries complexas: raciocínio explícito (CoT)
""")
    
    modo = input("\nEscolha o modo:\n1. Análise guiada (1 query)\n2. Ver tabela completa\n3. Analisar todas (10 queries)\n\nOpção: ").strip()
    
    if modo == "1":
        # Análise de 1 query
        query_id = int(input("Digite o ID da query (1-10): ").strip())
        query_info = next((q for q in QUERIES_CLASSIFICACAO if q['id'] == query_id), None)
        if query_info:
            analisar_query(query_info)
        else:
            print("❌ Query não encontrada.")
    
    elif modo == "2":
        # Mostrar tabela para preencher manualmente
        gerar_tabela_resumo()
    
    elif modo == "3":
        # Analisar todas as 10 queries
        resultados = []
        for q in QUERIES_CLASSIFICACAO:
            resultado = analisar_query(q)
            resultados.append(resultado)
            input("\nPressione ENTER para próxima query...")
        
        # Resumo final
        acertos = sum(1 for r in resultados if r['acertou'])
        print(f"\n{'='*70}")
        print(f"RESUMO FINAL: {acertos}/10 acertos ({acertos*10}%)")
        print("="*70)
        
        if acertos >= 8:
            print("🎉 EXCELENTE! Você domina classificação de complexidade.")
        elif acertos >= 6:
            print("✅ BOM! Continue praticando para identificar nuances.")
        else:
            print("⚠️  Revise os critérios e tente novamente.")
    
    print("\n✅ PRÓXIMO PASSO: ATIVIDADE 2B - Escrever Trace CoT Manualmente")
    print("   Você vai praticar raciocínio passo-a-passo para query complexa.\n")
