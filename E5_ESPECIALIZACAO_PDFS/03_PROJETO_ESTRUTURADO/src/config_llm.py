"""
CONFIG_LLM.PY - Configuração Flexível de LLM para E5
Suporta Ollama (local) e OpenRouter (API)

Uso:
    from src.config_llm import criar_llm, validar_configuracao
    
    # Validar antes de usar
    validar_configuracao()
    
    # Criar LLM
    llm = criar_llm()
    
    # Usar
    resposta = llm.invoke("Sua pergunta aqui")
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================================================
# CARREGAR VARIÁVEIS DE AMBIENTE
# ============================================================================

# Procurar .env no diretório do projeto
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    # Se não encontrar, procurar no diretório raiz
    load_dotenv()

# ============================================================================
# CONFIGURAÇÃO DE LLM
# ============================================================================

# Tipo de LLM a usar: 'ollama' ou 'openrouter'
LLM_TYPE = os.getenv("LLM_TYPE", "ollama").lower()

# ─────────────────────────────────────────────────────────────────────────
# Configuração Ollama (Local)
# ─────────────────────────────────────────────────────────────────────────

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# Modelos recomendados para Ollama:
# - llama2 (7B) - Rápido, bom para português
# - llama2:13b - Melhor qualidade, mais lento
# - mistral (7B) - Muito rápido
# - neural-chat (7B) - Otimizado para chat
# - openchat (7B) - Bom custo-benefício

# ─────────────────────────────────────────────────────────────────────────
# Configuração OpenRouter (API)
# ─────────────────────────────────────────────────────────────────────────

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct")

# Modelos recomendados para OpenRouter:
# - meta-llama/llama-3-8b-instruct - Bom custo-benefício
# - meta-llama/llama-3-70b-instruct - Melhor qualidade
# - mistralai/mistral-7b-instruct - Muito rápido
# - openai/gpt-3.5-turbo - Melhor qualidade (mais caro)
# - openai/gpt-4 - Melhor qualidade (muito caro)

# ─────────────────────────────────────────────────────────────────────────
# Parâmetros Gerais
# ─────────────────────────────────────────────────────────────────────────

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
NUM_CTX = int(os.getenv("NUM_CTX", "4096"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))


# ============================================================================
# FUNÇÕES
# ============================================================================

def criar_llm():
    """
    Cria instância de LLM baseado na configuração do .env
    
    Returns:
        LLM configurado (Ollama ou OpenRouter)
        
    Raises:
        ValueError: Se configuração inválida ou LLM não disponível
        
    Example:
        >>> llm = criar_llm()
        >>> resposta = llm.invoke("Olá, como você está?")
        >>> print(resposta)
    """
    
    if LLM_TYPE == "ollama":
        print(f"[CONFIG] Usando Ollama Local")
        print(f"  - Modelo: {OLLAMA_MODEL}")
        print(f"  - URL: {OLLAMA_BASE_URL}")
        print(f"  - Timeout: {OLLAMA_TIMEOUT}s")
        print(f"  - Temperatura: {TEMPERATURE}")
        print(f"  - Contexto: {NUM_CTX} tokens")
        
        try:
            from langchain_ollama import OllamaLLM
        except ImportError:
            raise ImportError(
                "langchain-ollama não está instalado. "
                "Execute: pip install langchain-ollama"
            )
        
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
                "Configure no arquivo .env ou variável de ambiente"
            )
        
        print(f"[CONFIG] Usando OpenRouter API")
        print(f"  - Modelo: {OPENROUTER_MODEL}")
        print(f"  - Temperatura: {TEMPERATURE}")
        print(f"  - Max tokens: {MAX_TOKENS}")
        
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise ImportError(
                "langchain-openai não está instalado. "
                "Execute: pip install langchain-openai"
            )
        
        return ChatOpenAI(
            model=OPENROUTER_MODEL,
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            default_headers={
                "HTTP-Referer": "https://github.com/ibmec-agentes-ia/e5-especializacao-pdfs",
                "X-Title": "E5 Especialização em PDFs - IBMEC"
            }
        )
    
    else:
        raise ValueError(
            f"LLM_TYPE inválido: {LLM_TYPE}. "
            f"Use 'ollama' ou 'openrouter'"
        )


def validar_configuracao() -> bool:
    """
    Valida configuração antes de usar
    
    Returns:
        True se configuração válida
        
    Raises:
        ValueError: Se configuração inválida
        
    Example:
        >>> validar_configuracao()
        [OK] Configuração válida!
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
        try:
            import requests
            response = requests.get(
                f"{OLLAMA_BASE_URL}/api/tags",
                timeout=5
            )
            
            if response.status_code == 200:
                print("  - Status: [OK] Ollama respondendo")
                
                # Verificar se modelo está disponível
                try:
                    data = response.json()
                    modelos = [m.get('name', '').split(':')[0] for m in data.get('models', [])]
                    
                    if OLLAMA_MODEL in modelos or any(OLLAMA_MODEL in m for m in modelos):
                        print(f"  - Modelo: [OK] {OLLAMA_MODEL} disponível")
                    else:
                        print(f"  - Modelo: [AVISO] {OLLAMA_MODEL} não encontrado")
                        print(f"    Modelos disponíveis: {', '.join(modelos) if modelos else 'nenhum'}")
                except:
                    pass
                
            else:
                print(f"  - Status: [AVISO] Ollama retornou código {response.status_code}")
                
        except Exception as e:
            print(f"  - Status: [ERRO] Ollama não está respondendo")
            print(f"    Erro: {e}")
            raise ValueError(
                "Ollama não está rodando! "
                "Inicie com: ollama serve"
            )
    
    elif LLM_TYPE == "openrouter":
        print(f"  - Modelo: {OPENROUTER_MODEL}")
        
        if OPENROUTER_API_KEY:
            print(f"  - API Key: ***{OPENROUTER_API_KEY[-4:]}")
        else:
            print(f"  - API Key: [NÃO CONFIGURADA]")
            raise ValueError(
                "OPENROUTER_API_KEY não configurada no .env!"
            )
    
    else:
        raise ValueError(f"LLM_TYPE inválido: {LLM_TYPE}")
    
    print(f"\nParâmetros:")
    print(f"  - Temperatura: {TEMPERATURE}")
    print(f"  - Contexto: {NUM_CTX} tokens")
    if LLM_TYPE == "openrouter":
        print(f"  - Max tokens: {MAX_TOKENS}")
    
    print("\n[OK] Configuração válida!")
    print("="*70)
    
    return True


def listar_modelos_ollama() -> list:
    """
    Lista modelos disponíveis no Ollama
    
    Returns:
        Lista de nomes de modelos
        
    Example:
        >>> modelos = listar_modelos_ollama()
        >>> print(modelos)
        ['llama2', 'mistral', 'neural-chat']
    """
    try:
        import requests
        response = requests.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            modelos = [m.get('name', '') for m in data.get('models', [])]
            return modelos
        else:
            return []
            
    except Exception as e:
        print(f"Erro ao listar modelos: {e}")
        return []


def testar_llm(pergunta: str = "Say 'Hello' in one word") -> str:
    """
    Testa LLM com pergunta simples
    
    Args:
        pergunta: Pergunta para testar
        
    Returns:
        Resposta do LLM
        
    Example:
        >>> resposta = testar_llm("Qual é a capital do Brasil?")
        >>> print(resposta)
    """
    try:
        llm = criar_llm()
        print(f"\n[TESTE] Pergunta: {pergunta}")
        resposta = llm.invoke(pergunta)
        print(f"[RESPOSTA] {resposta}")
        return resposta
    except Exception as e:
        print(f"[ERRO] {e}")
        raise


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    import sys
    
    try:
        # Validar configuração
        validar_configuracao()
        
        # Listar modelos Ollama (se aplicável)
        if LLM_TYPE == "ollama":
            print("\n[INFO] Modelos disponíveis no Ollama:")
            modelos = listar_modelos_ollama()
            for modelo in modelos:
                print(f"  - {modelo}")
        
        # Testar LLM
        print("\n[TESTE] Testando LLM...")
        testar_llm()
        
        print("\n[OK] LLM funcionando corretamente!")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
