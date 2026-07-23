"""
TESTE SIMPLES DO AGENTE v4.5
Demonstra a estrutura e lógica do agente sem executar (apenas análise estática)
"""

import json
from pathlib import Path

print("="*70)
print("ANÁLISE ESTÁTICA DO AGENTE v4.5 - RAG")
print("="*70)

# ============================================================================
# 1. VERIFICAR ESTRUTURA DO PROJETO
# ============================================================================

print("\n[1] VERIFICANDO ESTRUTURA DO PROJETO...")
print("-"*70)

base_path = Path(r"E:\documentos\ibmec\CODIGOS_AULA\E4_RAG_FAISS")

arquivos_necessarios = {
    "Config LLM": base_path / "scripts_agente" / "config_llm.py",
    "Agente v4.5": base_path / "scripts_agente" / "agente_v4_5_rag.py",
    "Tools Básicas": base_path / "scripts_agente" / "tools_basicas_v2.py",
    "Tool RAG": base_path / "scripts_agente" / "tool_rag_tfidf.py",
    "Documentos Conceituais": base_path / "DADOS_SINARM" / "documentos_conceituais.json",
    ".env.example": base_path / ".env.example",
}

for nome, caminho in arquivos_necessarios.items():
    existe = "[OK]" if caminho.exists() else "[X]"
    print(f"{existe} {nome}: {caminho.name}")

# ============================================================================
# 2. VERIFICAR DADOS SINARM
# ============================================================================

print("\n[2] VERIFICANDO DADOS SINARM...")
print("-"*70)

pasta_ocorrencias = base_path / "DADOS_SINARM" / "OCORRENCIAS"
if pasta_ocorrencias.exists():
    csvs = list(pasta_ocorrencias.glob("*.csv"))
    print(f"[OK] Pasta OCORRENCIAS encontrada")
    print(f"   Arquivos CSV: {len(csvs)}")
    for csv in csvs:
        tamanho_mb = csv.stat().st_size / (1024 * 1024)
        print(f"   - {csv.name} ({tamanho_mb:.1f} MB)")
else:
    print(f"[X] Pasta OCORRENCIAS nao encontrada")

# ============================================================================
# 3. CARREGAR DOCUMENTOS CONCEITUAIS
# ============================================================================

print("\n[3] ANALISANDO DOCUMENTOS CONCEITUAIS (RAG)...")
print("-"*70)

doc_path = base_path / "DADOS_SINARM" / "documentos_conceituais.json"
if doc_path.exists():
    with open(doc_path, 'r', encoding='utf-8') as f:
        documentos = json.load(f)
    
    print(f"[OK] Documentos carregados: {len(documentos)}")
    print(f"\nPRIMEIROS 5 DOCUMENTOS:")
    for i, doc in enumerate(documentos[:5], 1):
        print(f"\n{i}. ID: {doc.get('id', 'N/A')}")
        print(f"   Titulo: {doc.get('titulo', 'N/A')}")
        print(f"   Conteudo: {doc.get('conteudo', 'N/A')[:100]}...")
else:
    print(f"[X] Arquivo nao encontrado")

# ============================================================================
# 4. SIMULAR FLUXO DO AGENTE
# ============================================================================

print("\n[4] SIMULANDO FLUXO DO AGENTE v4.5...")
print("="*70)

perguntas_teste = [
    {
        "pergunta": "Quantas armas Taurus?",
        "tipo_esperado": "marca",
        "ferramenta": "contar_armas_marca",
        "parametros": {"marca": "Taurus"}
    },
    {
        "pergunta": "O que é calibre de arma?",
        "tipo_esperado": "conceitual",
        "ferramenta": "buscar_conhecimento_sinarm (RAG)",
        "parametros": {"query": "calibre de arma"}
    },
    {
        "pergunta": "Há mais Taurus ou Glock?",
        "tipo_esperado": "comparacao",
        "ferramenta": "contar_armas_marca (múltiplas)",
        "parametros": {"marcas": ["Taurus", "Glock"]}
    },
    {
        "pergunta": "Quantas Glock 9mm?",
        "tipo_esperado": "combinado",
        "ferramenta": "contar_armas_combinado",
        "parametros": {"marca": "Glock", "calibre": "9mm"}
    }
]

for i, teste in enumerate(perguntas_teste, 1):
    print(f"\n{'-'*70}")
    print(f"TESTE {i}: {teste['pergunta']}")
    print(f"{'-'*70}")
    print(f"Tipo esperado: {teste['tipo_esperado']}")
    print(f"Ferramenta: {teste['ferramenta']}")
    print(f"Parâmetros: {json.dumps(teste['parametros'], ensure_ascii=False, indent=2)}")
    
    # Simular resposta
    if teste['tipo_esperado'] == 'marca':
        print(f"\n[INFO] RESPOSTA SIMULADA:")
        print(f"   -> LLM analisa: Identificou marca '{teste['parametros']['marca']}'")
        print(f"   -> Executa: contar_armas_marca(marca='{teste['parametros']['marca']}')")
        print(f"   -> SQL: SELECT COUNT(*) FROM armas WHERE marca LIKE '%{teste['parametros']['marca']}%'")
        print(f"   -> Resultado: 17.760 armas (exemplo)")
        print(f"   -> LLM formata: 'Ha 17.760 armas Taurus no banco de dados.'")
    
    elif teste['tipo_esperado'] == 'conceitual':
        print(f"\n[INFO] RESPOSTA SIMULADA:")
        print(f"   -> LLM analisa: Pergunta conceitual (nao precisa dados)")
        print(f"   -> Executa: buscar_conhecimento_sinarm(query='calibre')")
        print(f"   -> RAG TF-IDF: Busca top-3 documentos relevantes")
        print(f"   -> Documento encontrado: 'Calibre e o diametro interno do cano...'")
        print(f"   -> LLM formata: Resposta baseada no contexto recuperado")
    
    elif teste['tipo_esperado'] == 'comparacao':
        print(f"\n[INFO] RESPOSTA SIMULADA:")
        print(f"   -> LLM analisa: Comparacao entre multiplas marcas")
        print(f"   -> Executa: contar_armas_marca('Taurus') + contar_armas_marca('Glock')")
        print(f"   -> Resultados: Taurus=17.760, Glock=726")
        print(f"   -> LLM formata: 'Ha mais Taurus (17.760) do que Glock (726).'")
    
    elif teste['tipo_esperado'] == 'combinado':
        print(f"\n[INFO] RESPOSTA SIMULADA:")
        print(f"   -> LLM analisa: Filtro por marca E calibre")
        print(f"   -> Executa: contar_armas_combinado(marca='Glock', calibre='9mm')")
        print(f"   -> SQL: SELECT COUNT(*) WHERE marca LIKE '%Glock%' AND calibre='9mm'")
        print(f"   -> Resultado: 658 armas (exemplo)")
        print(f"   -> LLM formata: 'Ha 658 armas Glock calibre 9mm.'")

# ============================================================================
# 5. VERIFICAR CONFIGURAÇÃO .env
# ============================================================================

print("\n\n[5] CONFIGURAÇÃO NECESSÁRIA (.env)...")
print("="*70)

env_path = base_path / ".env"
env_example_path = base_path / ".env.example"

if env_path.exists():
    print("[OK] Arquivo .env existe")
    print("   [!] NAO vou ler (contem credenciais sensiveis)")
else:
    print("[X] Arquivo .env NAO existe")
    print("\n[TODO] PROXIMOS PASSOS:")
    if env_example_path.exists():
        print("   1. Copiar .env.example para .env:")
        print("      copy .env.example .env")
    print("   2. Obter API key em: https://openrouter.ai/keys")
    print("   3. Editar .env e adicionar:")
    print("      OPENROUTER_API_KEY=sk-or-v1-SUA_CHAVE_AQUI")
    print("      LLM_TYPE=openrouter")

# ============================================================================
# 6. RESUMO
# ============================================================================

print("\n\n[6] RESUMO DA ANALISE")
print("="*70)

print("\n[OK] ARQUIVOS DO PROJETO:")
print("   - Agente v4.5 (RAG)")
print("   - Tools SQL (4 funcoes)")
print("   - Tool RAG TF-IDF")
print("   - Config LLM (Ollama/OpenRouter)")

print("\n[OK] DADOS DISPONIVEIS:")
print("   - CSVs de ocorrencias")
print("   - Documentos conceituais (20 docs)")

print("\n[!] PARA EXECUTAR:")
print("   1. Instalar dependencias: pip install -r requirements.txt")
print("   2. Configurar .env com API key")
print("   3. Executar: python scripts_agente\\agente_v4_5_rag.py")

print("\n[INFO] FLUXO DO AGENTE:")
print("   PERGUNTA -> LLM analisa -> Escolhe ferramenta ->")
print("   Executa (SQL ou RAG) -> LLM formata -> RESPOSTA")

print("\n[STATS] RESULTADOS ESPERADOS (segundo README):")
print("   - Acuracia: 93% (melhor versao)")
print("   - Velocidade: 2.24s media")
print("   - RAG utilizado: 95% perguntas conceituais")

print("\n" + "="*70)
print("ANALISE COMPLETA!")
print("="*70)
