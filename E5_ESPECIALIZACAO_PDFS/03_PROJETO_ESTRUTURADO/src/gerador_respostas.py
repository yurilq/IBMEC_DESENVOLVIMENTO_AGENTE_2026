"""
GERADOR_RESPOSTAS.PY - Integração de LLM com Pipeline de Busca

Combina busca semântica + reranking com geração de respostas usando LLM.

Uso:
    from src.gerador_respostas import gerar_resposta_com_llm
    
    resposta = gerar_resposta_com_llm(
        pergunta="Qual é a arma mais comum em ocorrências?",
        documentos_recuperados=[...],
        llm=llm
    )
"""

from typing import List, Dict, Any, Optional
from src.config_llm import criar_llm


def formatar_contexto(documentos: List[Dict[str, Any]]) -> str:
    """
    Formata documentos recuperados em contexto para o LLM
    
    Args:
        documentos: Lista de documentos com 'arquivo' e 'conteudo'
        
    Returns:
        String formatada com contexto
        
    Example:
        >>> docs = [{'arquivo': 'doc1.txt', 'conteudo': 'Texto...'}]
        >>> contexto = formatar_contexto(docs)
    """
    if not documentos:
        return "Nenhum documento relevante encontrado."
    
    contexto = "DOCUMENTOS RELEVANTES:\n"
    contexto += "=" * 70 + "\n\n"
    
    for i, doc in enumerate(documentos, 1):
        arquivo = doc.get('arquivo', 'desconhecido')
        conteudo = doc.get('conteudo', '')
        
        contexto += f"[Documento {i}] {arquivo}\n"
        contexto += "─" * 70 + "\n"
        contexto += conteudo[:500]  # Limitar a 500 caracteres
        if len(conteudo) > 500:
            contexto += "\n... (truncado)"
        contexto += "\n\n"
    
    return contexto


def criar_prompt_rag(
    pergunta: str,
    documentos: List[Dict[str, Any]],
    instrucoes_adicionais: str = ""
) -> str:
    """
    Cria prompt RAG para o LLM
    
    Args:
        pergunta: Pergunta do usuário
        documentos: Documentos recuperados
        instrucoes_adicionais: Instruções extras para o LLM
        
    Returns:
        Prompt formatado
        
    Example:
        >>> prompt = criar_prompt_rag(
        ...     pergunta="O que é calibre?",
        ...     documentos=[...]
        ... )
    """
    
    contexto = formatar_contexto(documentos)
    
    prompt = f"""Você é um assistente especializado em análise de dados de ocorrências PCDF.

{contexto}

PERGUNTA DO USUÁRIO:
{pergunta}

{instrucoes_adicionais}

INSTRUÇÕES:
1. Responda baseado APENAS nos documentos acima
2. Se a resposta não estiver nos documentos, diga claramente
3. Cite a fonte (arquivo) quando usar informações
4. Seja conciso e objetivo
5. Use português claro e profissional

RESPOSTA:"""
    
    return prompt


def gerar_resposta_com_llm(
    pergunta: str,
    documentos_recuperados: List[Dict[str, Any]],
    llm: Optional[Any] = None,
    instrucoes_adicionais: str = "",
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Gera resposta usando LLM com contexto de documentos recuperados
    
    Args:
        pergunta: Pergunta do usuário
        documentos_recuperados: Documentos do pipeline de busca
        llm: Instância de LLM (cria nova se None)
        instrucoes_adicionais: Instruções extras para o LLM
        verbose: Mostrar logs detalhados
        
    Returns:
        Dict com 'resposta', 'documentos_usados', 'modelo'
        
    Example:
        >>> resultado = gerar_resposta_com_llm(
        ...     pergunta="Qual é a arma mais comum?",
        ...     documentos_recuperados=[...]
        ... )
        >>> print(resultado['resposta'])
    """
    
    # Criar LLM se não fornecido
    if llm is None:
        if verbose:
            print("[INFO] Criando instância de LLM...")
        llm = criar_llm()
    
    # Criar prompt
    if verbose:
        print("[INFO] Criando prompt RAG...")
    prompt = criar_prompt_rag(pergunta, documentos_recuperados, instrucoes_adicionais)
    
    if verbose:
        print(f"[INFO] Prompt criado ({len(prompt)} caracteres)")
        print(f"[INFO] Documentos: {len(documentos_recuperados)}")
    
    # Gerar resposta
    if verbose:
        print("[INFO] Invocando LLM...")
    
    try:
        resposta = llm.invoke(prompt)
        
        if verbose:
            print(f"[INFO] Resposta gerada ({len(resposta)} caracteres)")
        
        return {
            "resposta": resposta,
            "documentos_usados": len(documentos_recuperados),
            "modelo": getattr(llm, 'model_name', 'desconhecido'),
            "pergunta": pergunta,
            "sucesso": True
        }
        
    except Exception as e:
        if verbose:
            print(f"[ERRO] Erro ao invocar LLM: {e}")
        
        return {
            "resposta": None,
            "erro": str(e),
            "documentos_usados": len(documentos_recuperados),
            "modelo": getattr(llm, 'model_name', 'desconhecido'),
            "pergunta": pergunta,
            "sucesso": False
        }


def gerar_resposta_simples(
    pergunta: str,
    llm: Optional[Any] = None,
    verbose: bool = False
) -> str:
    """
    Gera resposta simples sem contexto de documentos
    
    Args:
        pergunta: Pergunta do usuário
        llm: Instância de LLM (cria nova se None)
        verbose: Mostrar logs detalhados
        
    Returns:
        Resposta do LLM
        
    Example:
        >>> resposta = gerar_resposta_simples("Qual é a capital do Brasil?")
        >>> print(resposta)
    """
    
    if llm is None:
        if verbose:
            print("[INFO] Criando instância de LLM...")
        llm = criar_llm()
    
    if verbose:
        print(f"[INFO] Pergunta: {pergunta}")
        print("[INFO] Invocando LLM...")
    
    try:
        resposta = llm.invoke(pergunta)
        
        if verbose:
            print(f"[INFO] Resposta gerada ({len(resposta)} caracteres)")
        
        return resposta
        
    except Exception as e:
        if verbose:
            print(f"[ERRO] {e}")
        raise


def comparar_respostas(
    pergunta: str,
    documentos: List[Dict[str, Any]],
    llm_ollama: Optional[Any] = None,
    llm_openrouter: Optional[Any] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Compara respostas de dois LLMs diferentes
    
    Args:
        pergunta: Pergunta do usuário
        documentos: Documentos recuperados
        llm_ollama: Instância Ollama (cria se None)
        llm_openrouter: Instância OpenRouter (cria se None)
        verbose: Mostrar logs detalhados
        
    Returns:
        Dict com respostas de ambos os modelos
        
    Example:
        >>> resultado = comparar_respostas(
        ...     pergunta="O que é calibre?",
        ...     documentos=[...]
        ... )
        >>> print(resultado['ollama'])
        >>> print(resultado['openrouter'])
    """
    
    resultado = {
        "pergunta": pergunta,
        "ollama": None,
        "openrouter": None
    }
    
    # Testar Ollama
    if llm_ollama is not None:
        if verbose:
            print("\n[TESTE] Testando Ollama...")
        try:
            resp = gerar_resposta_com_llm(
                pergunta, documentos, llm_ollama, verbose=verbose
            )
            resultado["ollama"] = resp
        except Exception as e:
            resultado["ollama"] = {"erro": str(e)}
    
    # Testar OpenRouter
    if llm_openrouter is not None:
        if verbose:
            print("\n[TESTE] Testando OpenRouter...")
        try:
            resp = gerar_resposta_com_llm(
                pergunta, documentos, llm_openrouter, verbose=verbose
            )
            resultado["openrouter"] = resp
        except Exception as e:
            resultado["openrouter"] = {"erro": str(e)}
    
    return resultado


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    from src.config_llm import validar_configuracao
    
    print("="*70)
    print("TESTE: GERADOR DE RESPOSTAS COM LLM")
    print("="*70)
    
    try:
        # Validar configuração
        validar_configuracao()
        
        # Criar LLM
        print("\n[INFO] Criando LLM...")
        llm = criar_llm()
        
        # Teste 1: Resposta simples
        print("\n" + "="*70)
        print("TESTE 1: Resposta Simples")
        print("="*70)
        
        pergunta = "Qual é a capital do Brasil?"
        print(f"\nPergunta: {pergunta}")
        resposta = gerar_resposta_simples(pergunta, llm, verbose=True)
        print(f"\nResposta:\n{resposta}")
        
        # Teste 2: Resposta com contexto
        print("\n" + "="*70)
        print("TESTE 2: Resposta com Contexto")
        print("="*70)
        
        documentos = [
            {
                "arquivo": "documento1.txt",
                "conteudo": "Calibre é a medida do diâmetro interno do cano de uma arma de fogo."
            },
            {
                "arquivo": "documento2.txt",
                "conteudo": "Os calibres mais comuns são .38, .40 e 9mm."
            }
        ]
        
        pergunta = "O que é calibre e quais são os mais comuns?"
        print(f"\nPergunta: {pergunta}")
        resultado = gerar_resposta_com_llm(
            pergunta, documentos, llm, verbose=True
        )
        print(f"\nResposta:\n{resultado['resposta']}")
        print(f"\nDocumentos usados: {resultado['documentos_usados']}")
        
        print("\n[OK] Testes concluídos com sucesso!")
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
