#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICAR PRIVACIDADE - Pre-Push Check
Valida que nenhum arquivo privado do professor será enviado ao GitHub
"""

import subprocess
import sys
import os
from pathlib import Path

print("="*70)
print(" VERIFICACAO DE PRIVACIDADE - PRE-PUSH CHECK")
print("="*70)
print()

root_dir = Path(__file__).parent
os.chdir(root_dir)

# Padrões que NÃO devem aparecer no git status (devem estar ignorados)
private_patterns = [
    "_INTERNO",
    "_INTERNO_PROFESSOR",
    "TESTAR_",
    "VALIDACAO_",
    "RELATORIO_VALIDACAO",
    "GABARITO",
    "ROTEIRO_PROFESSOR",
    "ROTEIRO_TERCA",
    "ROTEIRO_QUINTA",
    "SOLUCAO_PROFESSOR",
    "_versoes_antigas",
    "CONCLUSAO_ESTRUTURACAO",
    "CONFIRMACAO_FINAL",
    "RESUMO_ESTRUTURACAO",
    "SCRIPTS_AUTOMATIZADOS",
]

print("[1/3] Verificando git status...")

# Executar git status
try:
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True,
        check=True
    )
    status_output = result.stdout
except Exception as e:
    print(f"ERRO: Nao foi possivel executar git status - {e}")
    sys.exit(1)

# Verificar se algum arquivo privado está no status (exceto deleted)
problems = []
for line in status_output.split('\n'):
    if not line.strip():
        continue
    
    # Pegar status e nome do arquivo
    parts = line.split()
    if len(parts) >= 2:
        status_code = parts[0]
        filename = parts[1]
        
        # Ignorar se for "D" (deleted) - isso é OK, estamos removendo
        if status_code == 'D':
            continue
        
        # Verificar se contém padrão privado
        for pattern in private_patterns:
            if pattern.upper() in filename.upper():
                problems.append(f"  PROBLEMA: {filename} (contém '{pattern}')")
                break

if problems:
    print("[X] ARQUIVOS PRIVADOS DETECTADOS NO GIT STATUS!")
    print()
    print("Os seguintes arquivos privados serao commitados:")
    print("-"*70)
    for problem in problems:
        print(problem)
    print()
    print("SOLUCAO:")
    print("  1. Adicione esses padroes ao .gitignore")
    print("  2. Execute: git rm --cached <arquivo>")
    print("  3. Execute este script novamente")
    print()
    sys.exit(1)
else:
    print("[OK] Nenhum arquivo privado detectado no git status")

print()
print("[2/3] Verificando git status --ignored...")

# Verificar ignored
try:
    result = subprocess.run(
        ["git", "status", "--ignored", "--short"],
        capture_output=True,
        text=True,
        check=True
    )
    ignored_output = result.stdout
except Exception as e:
    print(f"AVISO: Nao foi possivel verificar ignored - {e}")
    ignored_output = ""

# Contar quantos privados estão ignorados
ignored_count = 0
for line in ignored_output.split('\n'):
    if line.startswith('!!'):
        filename = line[3:].strip()
        for pattern in private_patterns:
            if pattern.upper() in filename.upper():
                ignored_count += 1
                break

if ignored_count > 0:
    print(f"[OK] {ignored_count} arquivos privados estao ignorados (correto)")
else:
    print("[!] Nenhum arquivo privado detectado em ignored")
    print("  (Isso pode ser OK se nao houver arquivos privados ainda)")

print()
print("[3/3] Verificando padrões no .gitignore...")

gitignore_path = root_dir / ".gitignore"
if gitignore_path.exists():
    gitignore_content = gitignore_path.read_text(encoding='utf-8')
    
    found_patterns = 0
    for pattern in private_patterns:
        if pattern in gitignore_content:
            found_patterns += 1
    
    print(f"[OK] {found_patterns}/{len(private_patterns)} padrões privados no .gitignore")
    
    if found_patterns < len(private_patterns) // 2:
        print("[!] AVISO: Poucos padrões privados no .gitignore")
        print("  Revise se todos os padrões necessários foram adicionados")
else:
    print("[X] ERRO: .gitignore não encontrado!")
    sys.exit(1)

# Resultado final
print()
print("="*70)
print(" RESULTADO")
print("="*70)
print()

if problems:
    print("[X] FALHOU - Arquivos privados serao commitados!")
    print()
    print("NAO FACA PUSH ate resolver os problemas acima.")
    sys.exit(1)
else:
    print("[OK] PASSOU - Nenhum arquivo privado sera commitado!")
    print()
    print("Seguro para:")
    print("  - git add .")
    print("  - git commit -m '...'")
    print("  - git push")
    print()
    print("Arquivos publicos que serao compartilhados:")
    print("  [OK] Codigos dos encontros (E1, E2, E3)")
    print("  [OK] DADOS_SINARM/")
    print("  [OK] utils/")
    print("  [OK] _DOCUMENTACAO/")
    print("  [OK] _SETUP/")
    print("  [OK] README.md, QUICK_START.md, etc.")
    print()
    print("Arquivos privados mantidos localmente:")
    print(f"  [OK] {ignored_count} arquivos ignorados")
    print("  [OK] _INTERNO/")
    print("  [OK] Scripts de teste")
    print("  [OK] Roteiros e gabaritos")
    print()
    sys.exit(0)
