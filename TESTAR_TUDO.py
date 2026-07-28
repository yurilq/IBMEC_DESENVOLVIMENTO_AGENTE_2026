#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE RAPIDO DE VALIDACAO - CODIGOS_AULA
Verifica se a mudanca de pasta quebrou alguma coisa
"""

import sys
import os
from pathlib import Path

print("="*60)
print(" VALIDACAO RAPIDA - CODIGOS_AULA")
print("="*60)
print()

# Adicionar pasta raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

errors = []
successes = []

# ============================================================
# TESTE 1: Verificar estrutura de pastas
# ============================================================
print("[1/7] Verificando estrutura de pastas...")

required_dirs = [
    "E1_ANATOMIA_DO_AGENTE",
    "E2_QUALIDADE_E_MEMORIA", 
    "E3_HANDS_ON_CONSTRUCAO_ZERO",
    "DADOS_SINARM",
    "utils",
    "_SETUP",
    "_DOCUMENTACAO",
]

for dir_name in required_dirs:
    dir_path = root_dir / dir_name
    if dir_path.exists():
        successes.append(f"  OK: {dir_name}/")
    else:
        errors.append(f"  ERRO: {dir_name}/ NAO ENCONTRADO")

# ============================================================
# TESTE 2: Verificar arquivos principais
# ============================================================
print("[2/7] Verificando arquivos principais...")

required_files = [
    "README.md",
    "QUICK_START.md",
    "INDICE.md",
    "requirements.txt",
    "E1_tools_sinarm.py",
]

for file_name in required_files:
    file_path = root_dir / file_name
    if file_path.exists():
        successes.append(f"  OK: {file_name}")
    else:
        errors.append(f"  ERRO: {file_name} NAO ENCONTRADO")

# ============================================================
# TESTE 3: Verificar imports basicos
# ============================================================
print("[3/7] Verificando imports basicos...")

try:
    import pandas as pd
    successes.append("  OK: pandas")
except ImportError as e:
    errors.append(f"  ERRO: pandas - {e}")

try:
    import numpy as np
    successes.append("  OK: numpy")
except ImportError as e:
    errors.append(f"  ERRO: numpy - {e}")

try:
    from pathlib import Path
    successes.append("  OK: pathlib")
except ImportError as e:
    errors.append(f"  ERRO: pathlib - {e}")

# ============================================================
# TESTE 4: Verificar utils/tools_sinarm.py
# ============================================================
print("[4/7] Verificando utils/tools_sinarm.py...")

utils_tools = root_dir / "utils" / "tools_sinarm.py"
if utils_tools.exists():
    successes.append(f"  OK: utils/tools_sinarm.py existe")
    
    # Tentar importar
    try:
        sys.path.insert(0, str(root_dir / "utils"))
        from tools_sinarm import (
            buscar_ocorrencias,
            buscar_portes,
            buscar_registros,
            buscar_requerimentos
        )
        successes.append("  OK: Tools SINARM importadas com sucesso")
        successes.append(f"    - buscar_ocorrencias")
        successes.append(f"    - buscar_portes")
        successes.append(f"    - buscar_registros")
        successes.append(f"    - buscar_requerimentos")
    except Exception as e:
        errors.append(f"  ERRO: Falha ao importar tools - {e}")
else:
    errors.append(f"  ERRO: utils/tools_sinarm.py NAO ENCONTRADO")

# ============================================================
# TESTE 5: Verificar dados SINARM
# ============================================================
print("[5/7] Verificando dados SINARM...")

dados_dir = root_dir / "DADOS_SINARM"
if dados_dir.exists():
    # Procurar em subpastas também
    csv_files = list(dados_dir.glob("**/*.csv"))
    if csv_files:
        successes.append(f"  OK: {len(csv_files)} arquivos CSV encontrados")
        # Agrupar por pasta
        from collections import defaultdict
        by_folder = defaultdict(list)
        for csv in csv_files:
            folder = csv.parent.name
            by_folder[folder].append(csv.name)
        
        for folder, files in by_folder.items():
            successes.append(f"    - {folder}/: {len(files)} arquivos")
    else:
        errors.append("  ERRO: Nenhum arquivo CSV em DADOS_SINARM/")
else:
    errors.append("  ERRO: DADOS_SINARM/ NAO ENCONTRADO")

# ============================================================
# TESTE 6: Verificar codigos E1
# ============================================================
print("[6/7] Verificando codigos E1...")

e1_dir = root_dir / "E1_ANATOMIA_DO_AGENTE"
if e1_dir.exists():
    # Verificar estrutura E1
    e1_subdirs = ["conceitos", "solucao_final"]
    for subdir in e1_subdirs:
        subdir_path = e1_dir / subdir
        if subdir_path.exists():
            py_files = list(subdir_path.rglob("*.py"))
            successes.append(f"  OK: E1/{subdir}/ ({len(py_files)} arquivos .py)")
        else:
            errors.append(f"  AVISO: E1/{subdir}/ nao encontrado")
else:
    errors.append("  ERRO: E1_ANATOMIA_DO_AGENTE/ NAO ENCONTRADO")

# ============================================================
# TESTE 7: Verificar paths relativos
# ============================================================
print("[7/7] Verificando paths relativos...")

# Simular import de E1
e1_conceitos = root_dir / "E1_ANATOMIA_DO_AGENTE" / "conceitos"
if e1_conceitos.exists():
    # Verificar se consegue acessar utils de dentro de E1
    test_path = e1_conceitos / ".." / ".." / "utils" / "tools_sinarm.py"
    test_path_resolved = test_path.resolve()
    
    if test_path_resolved.exists():
        successes.append("  OK: Path relativo E1 -> utils funciona")
    else:
        errors.append("  ERRO: Path relativo E1 -> utils QUEBRADO")
else:
    errors.append("  AVISO: Nao foi possivel testar paths relativos")

# ============================================================
# RESULTADO FINAL
# ============================================================
print()
print("="*60)
print(" RESULTADO DOS TESTES")
print("="*60)
print()

print(f"Sucessos: {len(successes)}")
print(f"Erros: {len(errors)}")
print()

if errors:
    print("ERROS ENCONTRADOS:")
    print("-"*60)
    for error in errors:
        print(error)
    print()

if successes and not errors:
    print("DETALHES:")
    print("-"*60)
    for success in successes[:10]:  # Mostrar apenas primeiros 10
        print(success)
    if len(successes) > 10:
        print(f"  ... e mais {len(successes) - 10} itens OK")
    print()

print("="*60)
if errors:
    print(" STATUS: FALHOU - Correcoes necessarias")
    sys.exit(1)
else:
    print(" STATUS: SUCESSO - Tudo funcionando!")
    sys.exit(0)
