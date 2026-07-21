# TEMPLATE_HORA_2.py
# Código de referência para Parte 2: Primeira Tool (SEM decorator)
# Use se ficar travado na Parte 2
#
# ⚠️ ATUALIZADO PARA LANGCHAIN 1.3+
# Usa agente MANUAL (sem initialize_agent que foi removido)

from langchain_ollama import OllamaLLM
from langchain.agents import Tool
import pandas as pd

# ============================================================
# FUNÇÃO PYTHON SIMPLES
# ============================================================

def contar_armas_marca(marca: str):
    """Conta quantas armas de uma marca específica"""
    
    print(f"🔍 Buscando armas da marca: {marca}")
    
    # Carregar CSV
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", 
                     sep=";", 
                     encoding="latin1")
    
    # Filtrar por marca (usa .str.contains para busca parcial mais robusta)
    df["MARCA_ARMA"] = df["MARCA_ARMA"].str.strip()
    resultado = df[df["MARCA_ARMA"].str.contains(marca, case=False, na=False)]
    
    # Contar
    total = len(resultado)
    
    return f"Encontrei {total} armas da marca {marca}"


# ============================================================
# TESTAR FUNÇÃO ISOLADA
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("TESTANDO FUNÇÃO")
    print("="*60)
    
    resultado = contar_armas_marca("Taurus")
    print(f"✅ {resultado}")
    
    resultado = contar_armas_marca("Glock")
    print(f"✅ {resultado}")
    
    print("="*60)
    
    # ============================================================
    # AGENTE MANUAL (LangChain 1.3+)
    # ============================================================
    
    print("\n" + "="*60)
    print("CRIANDO AGENTE MANUAL")
    print("="*60)
    
    # LLM
    llm = OllamaLLM(model="llama3", temperature=0)
    
    # Agente manual simples
    def agente_manual(pergunta: str):
        """Agente manual que seleciona e executa a tool"""
        print(f"\n[PERGUNTA] {pergunta}")
        print("-"*60)
        
        pergunta_lower = pergunta.lower()
        
        # Detectar marca
        marcas = ["taurus", "glock", "rossi", "beretta"]
        for marca in marcas:
            if marca in pergunta_lower:
                print(f"[AÇÃO] Detectei marca: {marca}")
                print(f"[TOOL] Chamando contar_armas_marca('{marca.capitalize()}')")
                return contar_armas_marca(marca.capitalize())
        
        return "Não consegui identificar a marca da arma na pergunta."
    
    # Testar
    print("\n" + "="*60)
    print("TESTANDO AGENTE")
    print("="*60 + "\n")
    
    pergunta = "Quantas armas Taurus existem?"
    print(f"❓ PERGUNTA: {pergunta}\n")
    
    resposta = agente_manual(pergunta)
    
    print(f"\n✅ RESPOSTA FINAL: {resposta}\n")
    print("="*60)
