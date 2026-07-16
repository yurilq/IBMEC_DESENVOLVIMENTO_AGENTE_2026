"""
TESTE DE IMPORTS - Verifica se reorganização de pastas funcionou
Execute este script para validar que todos os imports estão corretos.
"""

import sys
import os
from pathlib import Path

# Fix encoding Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.version_info >= (3, 7):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ajustar path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

print("="*70)
print("TESTE DE IMPORTS - ESTRUTURA MODULAR")
print("="*70)

# Teste 1: Utils
print("\n1️⃣  Testando utils/tools_sinarm.py...")
try:
    from utils.tools_sinarm import (
        buscar_ocorrencias,
        buscar_portes,
        buscar_registros,
        buscar_requerimentos
    )
    print("   ✅ utils.tools_sinarm importado com sucesso!")
    print(f"      - buscar_ocorrencias: {type(buscar_ocorrencias)}")
    print(f"      - buscar_portes: {type(buscar_portes)}")
    print(f"      - buscar_registros: {type(buscar_registros)}")
    print(f"      - buscar_requerimentos: {type(buscar_requerimentos)}")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

# Teste 2: E1 - agente_v1.8.py
print("\n2️⃣  Testando E1_ANATOMIA_DO_AGENTE/solucao_final/agente_v1.8.py...")
try:
    sys.path.insert(0, str(BASE_DIR / "E1_ANATOMIA_DO_AGENTE" / "solucao_final"))
    # Apenas verificar se arquivo existe e tem imports corretos
    arquivo_v18 = BASE_DIR / "E1_ANATOMIA_DO_AGENTE" / "solucao_final" / "agente_v1.8.py"
    if arquivo_v18.exists():
        with open(arquivo_v18, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        if "from utils.tools_sinarm import" in conteudo:
            print("   ✅ agente_v1.8.py usa 'utils.tools_sinarm' (correto!)")
        elif "from E1_tools_sinarm import" in conteudo:
            print("   ⚠️  agente_v1.8.py ainda usa 'E1_tools_sinarm' (precisa atualizar)")
        else:
            print("   ⚠️  Import não encontrado no arquivo")
    else:
        print(f"   ❌ Arquivo não encontrado: {arquivo_v18}")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

# Teste 3: E1 - E1_agente_react_v3.py
print("\n3️⃣  Testando E1_ANATOMIA_DO_AGENTE/solucao_final/E1_agente_react_v3.py...")
try:
    arquivo_v3 = BASE_DIR / "E1_ANATOMIA_DO_AGENTE" / "solucao_final" / "E1_agente_react_v3.py"
    if arquivo_v3.exists():
        with open(arquivo_v3, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        if "from utils.tools_sinarm import" in conteudo:
            print("   ✅ E1_agente_react_v3.py usa 'utils.tools_sinarm' (correto!)")
        elif "from E1_tools_sinarm import" in conteudo:
            print("   ⚠️  E1_agente_react_v3.py ainda usa 'E1_tools_sinarm' (precisa atualizar)")
    else:
        print(f"   ❌ Arquivo não encontrado: {arquivo_v3}")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

# Teste 4: E2 - agente_v2.0_fewshot.py
print("\n4️⃣  Testando E2_QUALIDADE_E_MEMORIA/solucao_final/agente_v2.0_fewshot.py...")
try:
    arquivo_v20 = BASE_DIR / "E2_QUALIDADE_E_MEMORIA" / "solucao_final" / "agente_v2.0_fewshot.py"
    if arquivo_v20.exists():
        with open(arquivo_v20, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        if "from utils.tools_sinarm import" in conteudo:
            print("   ✅ agente_v2.0_fewshot.py usa 'utils.tools_sinarm' (correto!)")
        elif "from E1_tools_sinarm import" in conteudo:
            print("   ⚠️  agente_v2.0_fewshot.py ainda usa 'E1_tools_sinarm' (precisa atualizar)")
    else:
        print(f"   ❌ Arquivo não encontrado: {arquivo_v20}")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

# Teste 5: E2 - agente_v2.5_cot.py
print("\n5️⃣  Testando E2_QUALIDADE_E_MEMORIA/solucao_final/agente_v2.5_cot.py...")
try:
    arquivo_v25 = BASE_DIR / "E2_QUALIDADE_E_MEMORIA" / "solucao_final" / "agente_v2.5_cot.py"
    if arquivo_v25.exists():
        with open(arquivo_v25, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        if "from utils.tools_sinarm import" in conteudo:
            print("   ✅ agente_v2.5_cot.py usa 'utils.tools_sinarm' (correto!)")
        elif "from E1_tools_sinarm import" in conteudo:
            print("   ⚠️  agente_v2.5_cot.py ainda usa 'E1_tools_sinarm' (precisa atualizar)")
    else:
        print(f"   ❌ Arquivo não encontrado: {arquivo_v25}")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

# Teste 6: Verificar estrutura de pastas
print("\n6️⃣  Verificando estrutura de pastas...")
try:
    estrutura = {
        "utils/": BASE_DIR / "utils",
        "E1_ANATOMIA_DO_AGENTE/": BASE_DIR / "E1_ANATOMIA_DO_AGENTE",
        "E2_QUALIDADE_E_MEMORIA/": BASE_DIR / "E2_QUALIDADE_E_MEMORIA",
        "DADOS_SINARM/": BASE_DIR / "DADOS_SINARM",
        "logs/": BASE_DIR / "logs"
    }
    
    for nome, caminho in estrutura.items():
        if caminho.exists():
            print(f"   ✅ {nome} existe")
        else:
            print(f"   ❌ {nome} NÃO existe")
except Exception as e:
    print(f"   ❌ ERRO: {e}")

# Resumo Final
print("\n" + "="*70)
print("RESUMO")
print("="*70)
print("""
Se todos os testes passaram (✅), a reorganização está correta!

Se há ⚠️ ou ❌:
1. Verifique se os arquivos foram movidos corretamente
2. Verifique se os imports foram atualizados (E1_tools_sinarm → utils.tools_sinarm)
3. Verifique se os paths foram ajustados (parent.parent.parent para chegar em 03_CODIGOS_PRONTOS)

Para executar um agente:
  cd E1_ANATOMIA_DO_AGENTE/solucao_final
  python agente_v1.8.py

Para executar atividades E2:
  cd E2_QUALIDADE_E_MEMORIA/conceitos/01_fewshot
  python ATIVIDADE_1A_baseline.py
""")
print("="*70)
