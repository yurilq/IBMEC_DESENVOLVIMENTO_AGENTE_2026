# SOLUÇÃO: Instalação Completa de Dependências E5
# Execute esta célula ANTES dos imports

import sys
import subprocess

print("🔧 INSTALANDO DEPENDÊNCIAS E5...")
print(f"📍 Python: {sys.version}")
print(f"📍 Executável: {sys.executable}\n")

# Lista de pacotes necessários
pacotes = [
    'sentence-transformers',
    'faiss-cpu',
    'PyPDF2',
    'transformers',
    'torch',
]

print("="*60)
print("INSTALANDO PACOTES...")
print("="*60)

for pacote in pacotes:
    print(f"\n📦 Instalando {pacote}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", pacote])
        print(f"✅ {pacote} instalado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao instalar {pacote}: {e}")

print("\n" + "="*60)
print("VERIFICANDO INSTALAÇÕES...")
print("="*60)

# Verificar instalações
pacotes_verificar = {
    'sentence_transformers': 'sentence-transformers',
    'faiss': 'faiss-cpu',
    'PyPDF2': 'PyPDF2',
    'transformers': 'transformers',
    'torch': 'torch',
}

for modulo, nome_pacote in pacotes_verificar.items():
    try:
        __import__(modulo)
        print(f"✅ {nome_pacote}: OK")
    except ImportError:
        print(f"❌ {nome_pacote}: FALHOU")

print("\n" + "="*60)
print("🎉 INSTALAÇÃO CONCLUÍDA!")
print("="*60)
print("\n💡 Agora execute a célula de imports novamente.")
