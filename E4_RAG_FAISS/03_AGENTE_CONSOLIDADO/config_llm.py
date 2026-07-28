"""
CONFIG_LLM.PY - Configuração Flexível de LLM
Suporta Ollama (local) e OpenRouter (API)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# ============================================================================
# CONFIGURAÇÃO DE LLM
# ============================================================================

LLM_TYPE = os.getenv("LLM_TYPE", "ollama").lower()

# Configuração Ollama
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# Configuração OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct")

# Parâmetros gerais
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))
NUM_CTX = int(os.getenv("NUM_CTX", "4096"))


def criar_llm():
    """
    Cria instância de LLM baseado na configuração do .env
    
    Returns:
        LLM configurado (Ollama ou OpenRouter)
    """
    
    if LLM_TYPE == "ollama":
        print(f"[CONFIG] Usando Ollama Local: {OLLAMA_MODEL}")
        print(f"[CONFIG] URL: {OLLAMA_BASE_URL}")
        print(f"[CONFIG] Timeout: {OLLAMA_TIMEOUT}s")
        
        from langchain_ollama import OllamaLLM
        
        return OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=TEMPERATURE,
            num_ctx=NUM_CTX,
            timeout=OLLAMA_TIMEOUT,
            request_timeout=OLLAMA_TIMEOUT
        )
    
    elif LLM_TYPE == "openrouter":
        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY não configurada! "
                "Configure no arquivo .env"
            )
        
        print(f"[CONFIG] Usando OpenRouter API: {OPENROUTER_MODEL}")
        print(f"[CONFIG] Temperatura: {TEMPERATURE}")
        
        from langchain_openai import ChatOpenAI
        
        return ChatOpenAI(
            model=OPENROUTER_MODEL,
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=TEMPERATURE,
            max_tokens=NUM_CTX,
            default_headers={
                "HTTP-Referer": "https://github.com/ibmec-agentes-ia/e4-rag-faiss",
                "X-Title": "E4 RAG FAISS - IBMEC"
            }
        )
    
    else:
        raise ValueError(
            f"LLM_TYPE inválido: {LLM_TYPE}. "
            f"Use 'ollama' ou 'openrouter'"
        )


def validar_configuracao():
    """
    Valida configuração antes de usar
    
    Raises:
        ValueError: Se configuração inválida
    """
    
    print("="*70)
    print("VALIDANDO CONFIGURAÇÃO DE LLM")
    print("="*70)
    
    print(f"\nTipo de LLM: {LLM_TYPE}")
    
    if LLM_TYPE == "ollama":
        print(f"  - Modelo: {OLLAMA_MODEL}")
        print(f"  - URL: {OLLAMA_BASE_URL}")
        print(f"  - Timeout: {OLLAMA_TIMEOUT}s")
        
        # Verificar se Ollama está rodando
        import requests
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                print("  - Status: [OK] Ollama respondendo")
            else:
                print(f"  - Status: [AVISO] Ollama retornou código {response.status_code}")
        except Exception as e:
            print(f"  - Status: [ERRO] Ollama não está respondendo: {e}")
            raise ValueError(
                "Ollama não está rodando! Inicie com: ollama serve"
            )
    
    elif LLM_TYPE == "openrouter":
        print(f"  - Modelo: {OPENROUTER_MODEL}")
        print(f"  - API Key: {'***' + OPENROUTER_API_KEY[-4:] if OPENROUTER_API_KEY else '[NÃO CONFIGURADA]'}")
        
        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY não configurada no .env!"
            )
    
    else:
        raise ValueError(f"LLM_TYPE inválido: {LLM_TYPE}")
    
    print(f"\nTemperatura: {TEMPERATURE}")
    print(f"Contexto: {NUM_CTX} tokens")
    
    print("\n[OK] Configuração válida!")
    print("="*70)


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Validar configuração
    try:
        validar_configuracao()
    except Exception as e:
        print(f"\n[ERRO] {e}")
        exit(1)
    
    # Criar LLM
    try:
        llm = criar_llm()
        
        # Testar
        print("\n[TESTE] Fazendo pergunta simples...")
        resposta = llm.invoke("Say 'Hello' in one word")
        print(f"[RESPOSTA] {resposta}")
        
        print("\n[OK] LLM funcionando corretamente!")
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        exit(1)
