#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE COMPLETO - TODOS OS ENCONTROS
Valida que a mudança de pasta não quebrou nada
"""

import sys
import os
from pathlib import Path
import py_compile

print("="*70)
print(" TESTE COMPLETO - VALIDACAO FINAL")
print("="*70)
print()

root_dir = Path(__file__).parent
errors = []
successes = []
warnings = []

# ============================================================
# TESTE 1: Estrutura de pastas
# ============================================================
print("[1/5] Validando estrutura...")

required_structure = {
    "E1_ANATOMIA_DO_AGENTE": ["conceitos", "solucao_final", "testes"],
    "E2_QUALIDADE_E_MEMORIA": ["conceitos", "solucao_final"],
    "E3_HANDS_ON_CONSTRUCAO_ZERO": [],
    "DADOS_SINARM": ["OCORRENCIAS", "PORTES", "REGISTROS", "REQUERIMENTOS"],
    "utils": [],
    "_SETUP": [],
    "_DOCUMENTACAO": [],
}

for main_dir, subdirs in required_structure.items():
    main_path = root_dir / main_dir
    if main_path.exists():
        successes.append(f"  OK: {main_dir}/")
        for subdir in subdirs:
            subdir_path = main_path / subdir
            if subdir_path.exists():
                successes.append(f"    OK: {main_dir}/{subdir}/")
            else:
                warnings.append(f"    AVISO: {main_dir}/{subdir}/ nao encontrado")
    else:
        errors.append(f"  ERRO: {main_dir}/ NAO ENCONTRADO")

# ============================================================
# TESTE 2: Compilação de todos os .py
# ============================================================
print("[2/5] Compilando todos os arquivos Python...")

py_files = list(root_dir.glob("**/*.py"))
py_files = [f for f in py_files if "__pycache__" not in str(f) and "_versoes_antigas" not in str(f)]

compiled = 0
failed = 0

for py_file in py_files:
    try:
        py_compile.compile(str(py_file), doraise=True)
        compiled += 1
    except py_compile.PyCompileError as e:
        failed += 1
        rel_path = py_file.relative_to(root_dir)
        errors.append(f"  ERRO: {rel_path} - Sintaxe invalida")

successes.append(f"  OK: {compiled} arquivos compilados com sucesso")
if failed > 0:
    errors.append(f"  ERRO: {failed} arquivos falharam")

# ============================================================
# TESTE 3: Imports principais
# ============================================================
print("[3/5] Testando imports principais...")

# Adicionar paths
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "utils"))

# Testar utils
try:
    from tools_sinarm import buscar_ocorrencias, buscar_portes
    successes.append("  OK: utils/tools_sinarm.py importa corretamente")
except Exception as e:
    errors.append(f"  ERRO: utils/tools_sinarm.py - {e}")

# Testar E1 tools
e1_tools = root_dir / "E1_ANATOMIA_DO_AGENTE" / "conceitos" / "02_tools" / "E1_tools_sinarm.py"
if e1_tools.exists():
    try:
        spec = compile(open(e1_tools, encoding='utf-8').read(), str(e1_tools), 'exec')
        successes.append("  OK: E1/conceitos/02_tools/E1_tools_sinarm.py compila")
    except Exception as e:
        errors.append(f"  ERRO: E1 tools - {e}")

# ============================================================
# TESTE 4: Dados SINARM
# ============================================================
print("[4/5] Verificando dados SINARM...")

dados_sinarm = root_dir / "DADOS_SINARM"
total_csvs = 0

for subdir in ["OCORRENCIAS", "PORTES", "REGISTROS", "REQUERIMENTOS"]:
    subdir_path = dados_sinarm / subdir
    if subdir_path.exists():
        csvs = list(subdir_path.glob("*.csv"))
        total_csvs += len(csvs)
        if csvs:
            successes.append(f"  OK: DADOS_SINARM/{subdir}/ - {len(csvs)} CSVs")
        else:
            warnings.append(f"  AVISO: DADOS_SINARM/{subdir}/ sem CSVs")
    else:
        errors.append(f"  ERRO: DADOS_SINARM/{subdir}/ NAO ENCONTRADO")

successes.append(f"  OK: Total de {total_csvs} arquivos CSV encontrados")

# ============================================================
# TESTE 5: Paths relativos (E1, E2, E3)
# ============================================================
print("[5/5] Testando paths relativos nos códigos...")

# Verificar se códigos referenciam corretamente
test_files = [
    ("E1_ANATOMIA_DO_AGENTE/solucao_final/agente_v1.8.py", "utils.tools_sinarm"),
    ("E1_ANATOMIA_DO_AGENTE/solucao_final/E1_agente_react_v3.py", "parent.parent.parent"),
]

for file_path, expected_ref in test_files:
    full_path = root_dir / file_path
    if full_path.exists():
        try:
            content = open(full_path, 'r', encoding='utf-8').read()
            if expected_ref in content:
                successes.append(f"  OK: {file_path} usa {expected_ref}")
            else:
                warnings.append(f"  AVISO: {file_path} pode nao usar paths corretos")
        except Exception as e:
            errors.append(f"  ERRO: {file_path} - {e}")

# ============================================================
# RESULTADO FINAL
# ============================================================
print()
print("="*70)
print(" RESULTADO FINAL")
print("="*70)
print()

print(f"✓ Sucessos: {len(successes)}")
print(f"⚠ Avisos: {len(warnings)}")
print(f"✗ Erros: {len(errors)}")
print()

if errors:
    print("ERROS CRITICOS:")
    print("-"*70)
    for error in errors[:10]:
        print(error)
    if len(errors) > 10:
        print(f"  ... e mais {len(errors)-10} erros")
    print()

if warnings:
    print("AVISOS (nao criticos):")
    print("-"*70)
    for warning in warnings[:5]:
        print(warning)
    if len(warnings) > 5:
        print(f"  ... e mais {len(warnings)-5} avisos")
    print()

print("RESUMO:")
print("-"*70)
print(f"Arquivos Python testados: {compiled + failed}")
print(f"Compilados com sucesso: {compiled}")
print(f"Falhas de compilacao: {failed}")
print(f"Arquivos CSV encontrados: {total_csvs}")
print()

print("="*70)
if errors:
    print(" STATUS: FALHOU - Correcoes necessarias")
    print()
    print("Recomendacao:")
    print("  1. Revisar erros acima")
    print("  2. Corrigir paths quebrados")
    print("  3. Executar teste novamente")
    sys.exit(1)
elif warnings:
    print(" STATUS: PASSOU COM AVISOS - Revisar avisos")
    print()
    print("Os avisos nao impedem o funcionamento,")
    print("mas devem ser revisados para garantir qualidade.")
    sys.exit(0)
else:
    print(" STATUS: SUCESSO TOTAL! ✓")
    print()
    print("Todos os testes passaram!")
    print("A mudanca de pasta NAO quebrou nada.")
    print()
    print("Pode usar com confianca! 🎉")
    sys.exit(0)
