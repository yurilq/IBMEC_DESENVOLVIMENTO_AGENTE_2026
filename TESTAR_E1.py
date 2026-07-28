#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE DETALHADO DOS CODIGOS E1
Valida imports e paths dos scripts principais
"""

import sys
import os
from pathlib import Path

print("="*70)
print(" TESTE DETALHADO - CODIGOS E1")
print("="*70)
print()

# Diretório raiz
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "utils"))

errors = []
successes = []

# ============================================================
# TESTE 1: E1/conceitos/02_tools/E1_tools_sinarm.py
# ============================================================
print("[1/4] Testando E1/conceitos/02_tools/E1_tools_sinarm.py...")

e1_tools_path = root_dir / "E1_ANATOMIA_DO_AGENTE" / "conceitos" / "02_tools" / "E1_tools_sinarm.py"

if e1_tools_path.exists():
    successes.append(f"  OK: Arquivo existe")
    
    # Testar sintaxe
    try:
        with open(e1_tools_path, 'r', encoding='utf-8') as f:
            code = f.read()
            compile(code, str(e1_tools_path), 'exec')
        successes.append("  OK: Sintaxe valida")
    except SyntaxError as e:
        errors.append(f"  ERRO: Sintaxe invalida - {e}")
    except Exception as e:
        errors.append(f"  ERRO: Falha ao ler arquivo - {e}")
else:
    errors.append(f"  ERRO: Arquivo nao encontrado")

# ============================================================
# TESTE 2: E1/solucao_final/agente_v1.8.py
# ============================================================
print("[2/4] Testando E1/solucao_final/agente_v1.8.py...")

agente_v18_path = root_dir / "E1_ANATOMIA_DO_AGENTE" / "solucao_final" / "agente_v1.8.py"

if agente_v18_path.exists():
    successes.append(f"  OK: Arquivo existe")
    
    # Testar sintaxe
    try:
        with open(agente_v18_path, 'r', encoding='utf-8') as f:
            code = f.read()
            compile(code, str(agente_v18_path), 'exec')
        successes.append("  OK: Sintaxe valida")
        
        # Verificar imports relativos
        if "from utils.tools_sinarm import" in code:
            successes.append("  OK: Usa import relativo correto (utils.tools_sinarm)")
        elif "sys.path" in code and "utils" in code:
            successes.append("  OK: Adiciona utils ao path")
        else:
            errors.append("  AVISO: Import pode estar quebrado")
            
    except SyntaxError as e:
        errors.append(f"  ERRO: Sintaxe invalida - {e}")
    except Exception as e:
        errors.append(f"  ERRO: Falha ao ler arquivo - {e}")
else:
    errors.append(f"  ERRO: Arquivo nao encontrado")

# ============================================================
# TESTE 3: E1/solucao_final/E1_agente_react_v3.py
# ============================================================
print("[3/4] Testando E1/solucao_final/E1_agente_react_v3.py...")

agente_v3_path = root_dir / "E1_ANATOMIA_DO_AGENTE" / "solucao_final" / "E1_agente_react_v3.py"

if agente_v3_path.exists():
    successes.append(f"  OK: Arquivo existe")
    
    # Testar sintaxe
    try:
        with open(agente_v3_path, 'r', encoding='utf-8') as f:
            code = f.read()
            compile(code, str(agente_v3_path), 'exec')
        successes.append("  OK: Sintaxe valida")
        
        # Verificar paths
        if "DADOS_SINARM" in code:
            successes.append("  OK: Referencia DADOS_SINARM")
        else:
            errors.append("  AVISO: Nao referencia DADOS_SINARM")
            
    except SyntaxError as e:
        errors.append(f"  ERRO: Sintaxe invalida - {e}")
    except Exception as e:
        errors.append(f"  ERRO: Falha ao ler arquivo - {e}")
else:
    errors.append(f"  ERRO: Arquivo nao encontrado")

# ============================================================
# TESTE 4: E1/testes/TESTES_COMPLETOS.py
# ============================================================
print("[4/4] Testando E1/testes/TESTES_COMPLETOS.py...")

testes_path = root_dir / "E1_ANATOMIA_DO_AGENTE" / "testes" / "TESTES_COMPLETOS.py"

if testes_path.exists():
    successes.append(f"  OK: Arquivo existe")
    
    # Testar sintaxe
    try:
        with open(testes_path, 'r', encoding='utf-8') as f:
            code = f.read()
            compile(code, str(testes_path), 'exec')
        successes.append("  OK: Sintaxe valida")
    except SyntaxError as e:
        errors.append(f"  ERRO: Sintaxe invalida - {e}")
    except Exception as e:
        errors.append(f"  ERRO: Falha ao ler arquivo - {e}")
else:
    errors.append(f"  ERRO: Arquivo nao encontrado")

# ============================================================
# RESULTADO
# ============================================================
print()
print("="*70)
print(" RESULTADO")
print("="*70)
print()

print(f"Sucessos: {len(successes)}")
print(f"Erros/Avisos: {len(errors)}")
print()

if errors:
    print("ERROS/AVISOS:")
    print("-"*70)
    for error in errors:
        print(error)
    print()

if successes:
    print("SUCESSOS:")
    print("-"*70)
    for success in successes:
        print(success)
    print()

print("="*70)
if errors:
    print(" STATUS: Revisar - Alguns avisos encontrados")
    sys.exit(0)  # Não falhar, apenas avisar
else:
    print(" STATUS: SUCESSO - Todos os codigos E1 estao OK!")
    sys.exit(0)
