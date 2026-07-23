"""
VERIFICACAO DE AMBIENTE - E4 RAG + FAISS
Verifica se todas as versoes estao corretas e compativeis
"""

import sys
import subprocess
from pathlib import Path

print("="*70)
print("VERIFICACAO DE AMBIENTE - E4 RAG + FAISS")
print("="*70)
print()

# Versoes esperadas
VERSOES_ESPERADAS = {
    'python': '3.11',  # minimo
    'numpy': '2.4.2',
    'pandas': '2.2.2',
    'torch': '2.13.0',
    'sentence-transformers': '3.1.1',
    'faiss-cpu': '1.14.3',
    'langchain': '1.3.13',
    'langchain-community': '0.4.2',
    'langchain-ollama': '1.3.0',
    'ollama': '0.32.1',
}

resultados = []
erros = []
avisos = []

# ===== VERIFICACAO 1: Python =====
print("[1/10] Verificando Python...")

python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
python_full = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

if float(python_version) >= float(VERSOES_ESPERADAS['python']):
    print(f"   [OK] Python {python_full}")
    resultados.append(("Python", True, python_full))
else:
    print(f"   [ERRO] Python {python_full} (requer {VERSOES_ESPERADAS['python']}+)")
    erros.append(f"Python versao {python_full} < {VERSOES_ESPERADAS['python']}")
    resultados.append(("Python", False, python_full))

# ===== VERIFICACAO 2-8: Bibliotecas Python =====

bibliotecas = [
    ('numpy', 'numpy'),
    ('pandas', 'pandas'),
    ('torch', 'torch'),
    ('sentence-transformers', 'sentence_transformers'),
    ('faiss-cpu', 'faiss'),
    ('langchain', 'langchain'),
    ('langchain-community', 'langchain_community'),
    ('langchain-ollama', 'langchain_ollama'),
]

for i, (nome_pip, nome_import) in enumerate(bibliotecas, 2):
    print(f"[{i}/10] Verificando {nome_pip}...")
    
    try:
        # Tentar importar
        modulo = __import__(nome_import)
        
        # Pegar versao
        if hasattr(modulo, '__version__'):
            versao_atual = modulo.__version__
        elif hasattr(modulo, 'VERSION'):
            versao_atual = modulo.VERSION
        else:
            versao_atual = "unknown"
        
        # Comparar versao
        versao_esperada = VERSOES_ESPERADAS.get(nome_pip, "any")
        
        if versao_esperada == "any" or versao_atual == versao_esperada:
            print(f"   [OK] {nome_pip} {versao_atual}")
            resultados.append((nome_pip, True, versao_atual))
        else:
            print(f"   [AVISO] {nome_pip} {versao_atual} (esperado: {versao_esperada})")
            avisos.append(f"{nome_pip} versao {versao_atual} != {versao_esperada}")
            resultados.append((nome_pip, True, versao_atual))
    
    except ImportError:
        print(f"   [ERRO] {nome_pip} NAO instalado")
        erros.append(f"{nome_pip} nao instalado")
        resultados.append((nome_pip, False, "N/A"))

# ===== VERIFICACAO 9: Ollama =====
print("[9/10] Verificando Ollama...")

try:
    result = subprocess.run(['ollama', '--version'], 
                          capture_output=True, 
                          text=True, 
                          timeout=5)
    
    if result.returncode == 0:
        output = result.stdout.strip()
        # Extrair versao (formato: "ollama version is X.Y.Z")
        if 'version is' in output:
            versao_ollama = output.split('version is')[1].strip()
        else:
            versao_ollama = output
        
        versao_esperada = VERSOES_ESPERADAS['ollama']
        
        if versao_ollama == versao_esperada:
            print(f"   [OK] Ollama {versao_ollama}")
            resultados.append(("Ollama", True, versao_ollama))
        else:
            print(f"   [AVISO] Ollama {versao_ollama} (esperado: {versao_esperada})")
            avisos.append(f"Ollama versao {versao_ollama} != {versao_esperada}")
            resultados.append(("Ollama", True, versao_ollama))
    else:
        print(f"   [ERRO] Ollama instalado mas nao responde")
        erros.append("Ollama nao responde")
        resultados.append(("Ollama", False, "N/A"))

except FileNotFoundError:
    print(f"   [ERRO] Ollama NAO instalado")
    erros.append("Ollama nao instalado")
    resultados.append(("Ollama", False, "N/A"))
except subprocess.TimeoutExpired:
    print(f"   [ERRO] Ollama timeout")
    erros.append("Ollama timeout")
    resultados.append(("Ollama", False, "N/A"))

# ===== VERIFICACAO 10: Modelo llama3 =====
print("[10/10] Verificando modelo llama3...")

try:
    result = subprocess.run(['ollama', 'list'], 
                          capture_output=True, 
                          text=True, 
                          timeout=10)
    
    if result.returncode == 0:
        output = result.stdout
        
        if 'llama3' in output.lower():
            # Extrair tamanho (aproximado)
            lines = output.split('\n')
            for line in lines:
                if 'llama3' in line.lower():
                    parts = line.split()
                    if len(parts) >= 3:
                        tamanho = parts[2]
                        print(f"   [OK] Modelo llama3 ({tamanho})")
                        resultados.append(("llama3", True, tamanho))
                        break
            else:
                print(f"   [OK] Modelo llama3 (instalado)")
                resultados.append(("llama3", True, "instalado"))
        else:
            print(f"   [ERRO] Modelo llama3 NAO encontrado")
            erros.append("Modelo llama3 nao baixado")
            resultados.append(("llama3", False, "N/A"))
    else:
        print(f"   [ERRO] Nao foi possivel listar modelos")
        erros.append("Ollama list falhou")
        resultados.append(("llama3", False, "N/A"))

except FileNotFoundError:
    print(f"   [ERRO] Ollama nao instalado (pular modelo)")
    resultados.append(("llama3", False, "N/A"))
except subprocess.TimeoutExpired:
    print(f"   [ERRO] Ollama timeout ao listar modelos")
    erros.append("Ollama list timeout")
    resultados.append(("llama3", False, "N/A"))

# ===== RESUMO =====
print()
print("="*70)
print("RESUMO DA VERIFICACAO:")
print("="*70)

total = len(resultados)
ok = sum(1 for _, status, _ in resultados if status)
falhas = total - ok

print(f"\nVerificacoes: {ok}/{total} passaram")
print()

for nome, status, versao in resultados:
    icone = "[OK]" if status else "[X]"
    print(f"{icone} {nome:25} {versao}")

print()

# ===== ERROS E AVISOS =====

if erros:
    print("="*70)
    print("ERROS ENCONTRADOS:")
    print("="*70)
    for i, erro in enumerate(erros, 1):
        print(f"{i}. {erro}")
    print()
    
    print("COMO CORRIGIR:")
    print()
    
    # Sugestoes especificas
    if any("nao instalado" in e for e in erros):
        print("Instalar bibliotecas faltando:")
        print("  pip install -r requirements.txt")
        print()
    
    if "Ollama nao instalado" in erros:
        print("Instalar Ollama:")
        print("  Baixar: https://ollama.ai/download")
        print()
    
    if "Modelo llama3 nao baixado" in erros:
        print("Baixar modelo llama3:")
        print("  ollama pull llama3")
        print()

if avisos:
    print("="*70)
    print("AVISOS (versoes diferentes):")
    print("="*70)
    for i, aviso in enumerate(avisos, 1):
        print(f"{i}. {aviso}")
    print()
    print("Versoes diferentes podem causar problemas.")
    print("Recomendado atualizar para versoes padrao:")
    print("  pip install -r requirements.txt --upgrade")
    print()

# ===== RESULTADO FINAL =====

if falhas == 0 and not erros:
    print("="*70)
    print("AMBIENTE COMPLETO E COMPATIVEL!")
    print("="*70)
    print()
    print("Tudo configurado corretamente!")
    print("Pronto para executar o pipeline RAG.")
    print()
    sys.exit(0)
elif not erros and avisos:
    print("="*70)
    print("AMBIENTE OK (com avisos)")
    print("="*70)
    print()
    print("Ambiente funcional, mas versoes diferentes.")
    print("Pode haver problemas de compatibilidade.")
    print("Recomendado atualizar versoes.")
    print()
    sys.exit(0)
else:
    print("="*70)
    print("AMBIENTE INCOMPLETO")
    print("="*70)
    print()
    print(f"{falhas} verificacao(oes) falharam")
    print()
    print("CORRIJA OS ERROS ACIMA antes de executar os scripts.")
    print("Consulte: AMBIENTE_PADRONIZADO.md")
    print()
    sys.exit(1)
