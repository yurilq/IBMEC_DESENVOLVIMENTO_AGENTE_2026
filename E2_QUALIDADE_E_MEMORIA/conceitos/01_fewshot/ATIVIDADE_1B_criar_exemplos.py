"""
ATIVIDADE 1B: CRIAR EXEMPLOS FEW-SHOT
Encontro 2 - Conceito: Few-Shot Learning
Duração: 20 minutos

OBJETIVO:
Criar 3 exemplos de alta qualidade (input → output) para ensinar o agente
como responder queries complexas sobre SINARM.

O QUE VOCÊ VAI FAZER:
1. Entender anatomia de um bom exemplo Few-Shot
2. Criar 3 exemplos seguindo template fornecido
3. Validar qualidade dos exemplos (checklist)
4. Salvar em JSON para usar na Atividade 1C

POR QUE ISSO É IMPORTANTE:
- Exemplos = "aulas" para o LLM (aprende por demonstração)
- Qualidade dos exemplos impacta DIRETAMENTE na performance
- Exemplos ruins → agente confuso → respostas piores
- Exemplos bons → agente confiante → respostas melhores

CONCEITO: Anatomia de um Exemplo Few-Shot
┌─────────────────────────────────────────────────────────────┐
│ INPUT (Query do usuário)                                     │
│ "Quantas pistolas Taurus calibre .380 foram furtadas no DF?"│
├─────────────────────────────────────────────────────────────┤
│ THOUGHT (Raciocínio do agente - CoT simplificado)           │
│ "Preciso buscar no dataset OCORRENCIAS com 3 filtros:       │
│  marca:Taurus, especie:Pistola, calibre:.380, tipo:Furto"   │
├─────────────────────────────────────────────────────────────┤
│ ACTION (Tool call exato)                                     │
│ buscar_ocorrencias("marca:Taurus")                           │
│ [filtra manualmente especie, calibre, tipo]                  │
├─────────────────────────────────────────────────────────────┤
│ OUTPUT (Resposta formatada)                                  │
│ "Foram encontradas 47 pistolas Taurus calibre .380          │
│  furtadas no DF em 2026. Dados: SINARM/OCORRENCIAS."        │
└─────────────────────────────────────────────────────────────┘

CHECKLIST QUALIDADE:
✓ Exemplo é realista (query que usuário faria)?
✓ Dataset escolhido está correto?
✓ Campos mapeados corretamente?
✓ Resposta é precisa e completa?
✓ Fonte citada corretamente?
✓ Linguagem natural e clara?
"""

import json
from pathlib import Path
from datetime import datetime

# ========== TEMPLATE EXEMPLO ==========

TEMPLATE_EXEMPLO = {
    "id": 1,
    "input": "Query do usuário aqui",
    "thought": "Raciocínio: qual dataset, quais campos, como processar",
    "action": "buscar_[dataset](\"campo:valor\")",
    "observation": "Resultado da tool (resumido)",
    "output": "Resposta final formatada para o usuário",
    "dataset_usado": "ocorrencias|portes|registros|requerimentos",
    "complexidade": "baixa|média|alta",
    "criado_em": datetime.now().isoformat()
}

# ========== EXEMPLOS PRÉ-PREENCHIDOS (REFERÊNCIA) ==========

EXEMPLOS_REFERENCIA = [
    {
        "id": 1,
        "input": "Quantas pistolas Taurus calibre .380 foram furtadas no DF?",
        "thought": "Preciso buscar no dataset OCORRENCIAS filtros: marca=Taurus, especie=Pistola, calibre=.380, tipo=Furto, uf=DF. Como a tool buscar_ocorrencias aceita apenas 1 campo por vez, vou buscar pela marca e depois filtrar manualmente os outros critérios.",
        "action": "buscar_ocorrencias(\"marca:Taurus\")",
        "observation": "Retornou 1.247 ocorrências de Taurus. Filtrei manualmente: especie=Pistola (892), calibre=.380 (347), tipo=Furto (289), uf=DF (47).",
        "output": "Foram encontradas 47 pistolas Taurus calibre .380 furtadas no DF em 2026. Fonte: SINARM/OCORRENCIAS (74.758 registros).",
        "dataset_usado": "ocorrencias",
        "complexidade": "alta",
        "criado_em": datetime.now().isoformat()
    },
    {
        "id": 2,
        "input": "Quais marcas de arma têm portes válidos no DF?",
        "thought": "Preciso buscar no dataset PORTES com filtros: status=Válido, uf=DF. Depois agrupar por marca e contar.",
        "action": "buscar_portes(\"status:Válido\")",
        "observation": "Retornou 1.856 portes válidos. Filtrei uf=DF (312). Marcas encontradas: Taurus (187), Glock (67), Beretta (31), Imbel (18), Outras (9).",
        "output": "No DF há 312 portes válidos distribuídos assim: Taurus (60%), Glock (21%), Beretta (10%), Imbel (6%), Outras (3%). Fonte: SINARM/PORTES.",
        "dataset_usado": "portes",
        "complexidade": "média",
        "criado_em": datetime.now().isoformat()
    },
    {
        "id": 3,
        "input": "Qual a taxa de aprovação de requerimentos de porte?",
        "thought": "Preciso buscar no dataset REQUERIMENTOS e calcular: (decisao=Aprovado / total) * 100. Vou buscar aprovados e depois total.",
        "action": "buscar_requerimentos(\"decisao:Aprovado\")",
        "observation": "Retornou 28.347 aprovados. Total dataset: 46.116. Taxa = (28.347 / 46.116) * 100 = 61,47%.",
        "output": "A taxa de aprovação de requerimentos de porte é 61,47% (28.347 aprovados de 46.116 totais). Fonte: SINARM/REQUERIMENTOS.",
        "dataset_usado": "requerimentos",
        "complexidade": "média",
        "criado_em": datetime.now().isoformat()
    }
]

# ========== VALIDAÇÃO ==========

def validar_exemplo(exemplo):
    """
    Valida qualidade de um exemplo Few-Shot.
    
    Retorna: (is_valid, erros[])
    """
    erros = []
    
    # Check 1: Campos obrigatórios
    campos_obrigatorios = ["id", "input", "thought", "action", "output", "dataset_usado"]
    for campo in campos_obrigatorios:
        if campo not in exemplo or not exemplo[campo]:
            erros.append(f"❌ Campo '{campo}' obrigatório está vazio")
    
    # Check 2: Input realista (mínimo 10 caracteres)
    if len(exemplo.get("input", "")) < 10:
        erros.append("❌ Input muito curto (mínimo 10 caracteres)")
    
    # Check 3: Thought tem raciocínio (mínimo 20 caracteres)
    if len(exemplo.get("thought", "")) < 20:
        erros.append("❌ Thought precisa explicar o raciocínio (mínimo 20 caracteres)")
    
    # Check 4: Action usa tool correta
    action = exemplo.get("action", "")
    tools_validas = ["buscar_ocorrencias", "buscar_portes", "buscar_registros", "buscar_requerimentos"]
    if not any(tool in action for tool in tools_validas):
        erros.append(f"❌ Action deve usar uma das tools: {', '.join(tools_validas)}")
    
    # Check 5: Dataset usado é válido
    datasets_validos = ["ocorrencias", "portes", "registros", "requerimentos"]
    if exemplo.get("dataset_usado") not in datasets_validos:
        erros.append(f"❌ Dataset deve ser um de: {', '.join(datasets_validos)}")
    
    # Check 6: Output tem fonte citada
    output = exemplo.get("output", "")
    if "SINARM" not in output and "Fonte:" not in output:
        erros.append("❌ Output deve citar a fonte (ex: 'Fonte: SINARM/OCORRENCIAS')")
    
    # Check 7: Output tem resposta clara (mínimo 20 caracteres)
    if len(output) < 20:
        erros.append("❌ Output muito curto (mínimo 20 caracteres)")
    
    return (len(erros) == 0, erros)

# ========== INTERFACE CRIAÇÃO ==========

def criar_exemplo_interativo(id_exemplo):
    """
    Interface interativa para criar exemplo Few-Shot.
    """
    
    print(f"\n{'='*70}")
    print(f"CRIANDO EXEMPLO #{id_exemplo}")
    print("="*70)
    
    exemplo = {"id": id_exemplo}
    
    # Input
    print("\n1️⃣  INPUT (Query do usuário)")
    print("   Exemplo: 'Quantas pistolas foram furtadas no DF?'")
    exemplo["input"] = input("   Digite a query: ").strip()
    
    # Thought
    print("\n2️⃣  THOUGHT (Raciocínio do agente)")
    print("   Exemplo: 'Preciso buscar no dataset OCORRENCIAS com filtros...'")
    exemplo["thought"] = input("   Digite o raciocínio: ").strip()
    
    # Action
    print("\n3️⃣  ACTION (Tool call)")
    print("   Exemplo: buscar_ocorrencias(\"marca:Taurus\")")
    exemplo["action"] = input("   Digite a action: ").strip()
    
    # Observation
    print("\n4️⃣  OBSERVATION (Resultado da tool - opcional)")
    exemplo["observation"] = input("   Digite a observação (ou ENTER para pular): ").strip()
    
    # Output
    print("\n5️⃣  OUTPUT (Resposta final formatada)")
    print("   Exemplo: 'Foram encontradas 47 pistolas... Fonte: SINARM/OCORRENCIAS'")
    exemplo["output"] = input("   Digite a resposta: ").strip()
    
    # Dataset
    print("\n6️⃣  DATASET USADO")
    print("   Opções: ocorrencias, portes, registros, requerimentos")
    exemplo["dataset_usado"] = input("   Digite o dataset: ").strip()
    
    # Complexidade
    print("\n7️⃣  COMPLEXIDADE")
    print("   Opções: baixa, média, alta")
    exemplo["complexidade"] = input("   Digite a complexidade: ").strip()
    
    # Timestamp
    exemplo["criado_em"] = datetime.now().isoformat()
    
    # Validar
    print("\n🔍 VALIDANDO EXEMPLO...")
    valido, erros = validar_exemplo(exemplo)
    
    if valido:
        print("✅ Exemplo válido!")
        return exemplo
    else:
        print("❌ Exemplo tem erros:")
        for erro in erros:
            print(f"   {erro}")
        
        refazer = input("\n🔄 Refazer exemplo? (S/N): ").strip().upper()
        if refazer == "S":
            return criar_exemplo_interativo(id_exemplo)
        else:
            return None

# ========== SALVAR EXEMPLOS ==========

def salvar_exemplos(exemplos, arquivo="exemplos_fewshot.json"):
    """Salvar exemplos em JSON."""
    
    caminho = Path(__file__).parent / arquivo
    
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(exemplos, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Exemplos salvos em: {caminho}")

# ========== MAIN ==========

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  ATIVIDADE 1B: CRIAR EXEMPLOS FEW-SHOT                       ║
║  Encontro 2 - Few-Shot Learning                              ║
╚═══════════════════════════════════════════════════════════════╝

INSTRUÇÕES:
1. Você vai criar 3 exemplos de alta qualidade
2. Cada exemplo tem 7 campos (input, thought, action, observation, output, dataset, complexidade)
3. Use os exemplos de referência como guia
4. O sistema vai validar automaticamente
5. Exemplos serão salvos em JSON para usar na Atividade 1C

DICA: Crie exemplos que cubram diferentes datasets e complexidades!
""")
    
    # Mostrar exemplos de referência
    print("\n📚 EXEMPLOS DE REFERÊNCIA (para se inspirar):")
    for ex in EXEMPLOS_REFERENCIA:
        print(f"\n🔹 Exemplo {ex['id']}:")
        print(f"   Input:  {ex['input']}")
        print(f"   Output: {ex['output'][:60]}...")
    
    input("\nPressione ENTER para começar a criar seus exemplos...")
    
    # Criar 3 exemplos
    meus_exemplos = []
    
    for i in range(1, 4):
        exemplo = criar_exemplo_interativo(i)
        if exemplo:
            meus_exemplos.append(exemplo)
            print(f"\n✅ Exemplo {i}/3 criado com sucesso!")
        else:
            print(f"\n⚠️  Exemplo {i} pulado.")
    
    # Salvar
    if meus_exemplos:
        salvar_exemplos(meus_exemplos)
        
        print(f"\n{'='*70}")
        print(f"RESUMO: {len(meus_exemplos)}/3 exemplos criados")
        print("="*70)
        for ex in meus_exemplos:
            valido, _ = validar_exemplo(ex)
            status = "✅" if valido else "❌"
            print(f"{status} Exemplo {ex['id']}: {ex['input'][:50]}...")
        
        print("\n✅ PRÓXIMO PASSO: ATIVIDADE 1C - Implementar Few-Shot no Agente")
        print("   Você vai adicionar esses exemplos ao agente v1.8 → v2.0\n")
    else:
        print("\n⚠️  Nenhum exemplo criado. Rode o script novamente.\n")
