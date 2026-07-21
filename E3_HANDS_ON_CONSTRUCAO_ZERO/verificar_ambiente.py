# verificar_ambiente.py
# Script de verificação do ambiente E3
# Execute ANTES de começar a aula

import sys
import os

print("="*60)
print("🔍 VERIFICAÇÃO DE AMBIENTE - E3")
print("="*60)

erros = []
avisos = []
ok = []

# 1. Verificar Python
print("\n[1/6] Verificando Python...")
versao = sys.version_info
if versao.major >= 3 and versao.minor >= 9:
    ok.append(f"✅ Python {versao.major}.{versao.minor}.{versao.micro}")
else:
    erros.append(f"❌ Python {versao.major}.{versao.minor} (requer 3.9+)")

# 2. Verificar pandas
print("[2/6] Verificando pandas...")
try:
    import pandas as pd
    ok.append(f"✅ pandas {pd.__version__}")
except ImportError:
    erros.append("❌ pandas não instalado (pip install pandas)")

# 3. Verificar LangChain
print("[3/6] Verificando LangChain...")
try:
    from langchain_core.tools import tool
    ok.append("✅ langchain_core instalado")
except ImportError:
    erros.append("❌ langchain_core não instalado (pip install langchain-core)")

try:
    from langchain_ollama import OllamaLLM
    ok.append("✅ langchain_ollama instalado")
except ImportError:
    erros.append("❌ langchain_ollama não instalado (pip install langchain-ollama)")

# 4. Verificar Ollama
print("[4/6] Verificando Ollama...")
try:
    import subprocess
    result = subprocess.run(['ollama', 'list'], 
                          capture_output=True, 
                          text=True, 
                          timeout=5)
    if result.returncode == 0:
        ok.append("✅ Ollama instalado e acessível")
        # Verificar modelos
        if 'llama3' in result.stdout or 'llama3.2' in result.stdout:
            ok.append("✅ Modelo LLM disponível")
        else:
            avisos.append("⚠️  Nenhum modelo Ollama instalado (ollama pull llama3.2:1b)")
    else:
        erros.append("❌ Ollama não está rodando (execute: ollama serve)")
except FileNotFoundError:
    erros.append("❌ Ollama não instalado (https://ollama.ai/download)")
except subprocess.TimeoutExpired:
    erros.append("❌ Ollama não responde (verifique se está rodando)")

# 5. Verificar CSV
print("[5/6] Verificando CSV...")
csv_path = "DADOS_SINARM/OCORRENCIAS_2026.csv"
if os.path.exists(csv_path):
    size = os.path.getsize(csv_path) / (1024 * 1024)  # MB
    ok.append(f"✅ CSV encontrado ({size:.1f} MB)")
else:
    erros.append(f"❌ CSV não encontrado em {csv_path}")
    avisos.append("   Certifique-se de estar na pasta de trabalho correta")
    avisos.append("   Leia: ESTRUTURA_PASTAS_E3.md")

# 6. Verificar estrutura de pastas
print("[6/6] Verificando estrutura...")
if os.path.exists("DADOS_SINARM"):
    ok.append("✅ Pasta DADOS_SINARM existe")
else:
    erros.append("❌ Pasta DADOS_SINARM não existe (mkdir DADOS_SINARM)")

# Resumo
print("\n" + "="*60)
print("📊 RESUMO DA VERIFICAÇÃO")
print("="*60)

if ok:
    print("\n✅ OK:")
    for item in ok:
        print(f"   {item}")

if avisos:
    print("\n⚠️  AVISOS:")
    for item in avisos:
        print(f"   {item}")

if erros:
    print("\n❌ ERROS:")
    for item in erros:
        print(f"   {item}")

print("\n" + "="*60)

if erros:
    print("❌ AMBIENTE NÃO ESTÁ PRONTO")
    print("="*60)
    print("\n🔧 AÇÕES NECESSÁRIAS:")
    print("\n1. Instalar dependências:")
    print("   pip install pandas langchain-core langchain-ollama")
    print("\n2. Instalar e iniciar Ollama:")
    print("   https://ollama.ai/download")
    print("   ollama serve")
    print("\n3. Baixar modelo:")
    print("   ollama pull llama3.2:1b")
    print("\n4. Verificar estrutura de pastas:")
    print("   Leia: ESTRUTURA_PASTAS_E3.md")
    sys.exit(1)
elif avisos:
    print("⚠️  AMBIENTE PARCIALMENTE PRONTO")
    print("="*60)
    print("\nResolva os avisos antes de começar a aula.")
    sys.exit(0)
else:
    print("✅ AMBIENTE 100% PRONTO PARA AULA!")
    print("="*60)
    print("\nVocê pode começar seguindo os guias em 01_GUIAS_ALUNO/")
    sys.exit(0)
