"""
Módulo de Carregamento de Dados

Responsável por carregar:
- CSV com dados SINARM
- Documentos .txt conceituais
- PDFs da PCDF

Usa cache para evitar recarregar dados múltiplas vezes.
"""

import os
import pandas as pd
from functools import lru_cache
from PyPDF2 import PdfReader
from typing import List, Dict, Optional

# Obter diretório base do projeto (3 níveis acima de loader.py)
# loader.py → src/ → 03_PROJETO_ESTRUTURADO/ → E5_ESPECIALIZACAO_PDFS/ → CODIGOS_AULA/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS_DIR = os.path.join(os.path.dirname(BASE_DIR), "DADOS_SINARM")


@lru_cache(maxsize=1)
def carregar_csv(
    caminho: Optional[str] = None,
    encoding: str = "latin-1",
    sep: str = ";"
) -> pd.DataFrame:
    """
    Carrega dados SINARM do CSV.
    
    Cache garante que carrega apenas UMA VEZ.
    
    Args:
        caminho: Caminho do arquivo CSV
        encoding: Encoding do arquivo
        sep: Separador de colunas
    
    Returns:
        DataFrame com dados carregados
    
    Raises:
        FileNotFoundError: Se arquivo não encontrado
        Exception: Se não conseguir ler com nenhuma configuração
    
    Example:
        >>> df = carregar_csv()
        >>> print(f"{len(df)} registros carregados")
    """
    # Tentar diferentes caminhos
    if caminho is None:
        caminhos_possiveis = [
            os.path.join(DADOS_DIR, "OCORRENCIAS_2026.csv"),  # Diretamente em DADOS_SINARM
            os.path.join(DADOS_DIR, "OCORRENCIAS", "OCORRENCIAS_2026.csv"),  # Em subpasta
            os.path.join(BASE_DIR, "01_DADOS", "DADOS_SINARM", "OCORRENCIAS", "OCORRENCIAS_2026.csv"),  # Caminho antigo
            os.path.join(BASE_DIR, "..", "E4_RAG_FAISS", "01_DADOS", "DADOS_SINARM", "OCORRENCIAS", "OCORRENCIAS_2026.csv"),  # E4
        ]
    else:
        caminhos_possiveis = [caminho]
    
    caminho_encontrado = None
    for c in caminhos_possiveis:
        if os.path.exists(c):
            caminho_encontrado = c
            break
    
    if not caminho_encontrado:
        raise FileNotFoundError(
            f"Arquivo não encontrado em nenhum dos caminhos: {caminhos_possiveis}"
        )
    
    # Tentar diferentes configurações
    configs = [
        {'encoding': 'latin-1', 'sep': ';'},  # ⭐ ESTE É O CORRETO!
        {'encoding': 'utf-8', 'sep': ';'},
        {'encoding': 'iso-8859-1', 'sep': ';'},
    ]
    
    for config in configs:
        try:
            df = pd.read_csv(caminho_encontrado, **config)
            
            # Validar se carregou corretamente (deve ter múltiplas colunas)
            if len(df.columns) > 1:
                print(f"[CACHE] Carregando CSV com encoding={config['encoding']}, sep='{config['sep']}'")
                print(f"[OK] {len(df)} registros, {len(df.columns)} colunas carregadas!")
                print(f"[COLUNAS] {list(df.columns)[:5]}...")
                return df
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    
    raise Exception(f"Não foi possível ler o arquivo com nenhuma configuração testada")


@lru_cache(maxsize=1)
def carregar_documentos_txt(
    caminho_docs: Optional[str] = None
) -> List[Dict[str, str]]:
    """
    Carrega documentos conceituais do E4 (.txt).
    
    Args:
        caminho_docs: Caminho da pasta com documentos
    
    Returns:
        list: [{\"arquivo\": str, \"conteudo\": str}]
    
    Example:
        >>> docs = carregar_documentos_txt()
        >>> print(f"{len(docs)} documentos carregados")
    """
    if caminho_docs is None:
        caminhos_possiveis = [
            os.path.join(DADOS_DIR, "documentos_conceituais"),  # NOVO: Dados em CODIGOS_AULA
            os.path.join(BASE_DIR, "01_DADOS", "documentos_conceituais"),  # Caminho antigo
            os.path.join(BASE_DIR, "..", "E4_RAG_FAISS", "01_DADOS", "documentos_conceituais"),  # E4
        ]
    else:
        caminhos_possiveis = [caminho_docs]
    
    caminho_docs_encontrado = None
    for c in caminhos_possiveis:
        if os.path.exists(c):
            caminho_docs_encontrado = c
            break
    
    if not caminho_docs_encontrado:
        print(f"⚠️ Pasta de documentos não encontrada")
        return []
    
    documentos = []
    for arquivo in os.listdir(caminho_docs_encontrado):
        if arquivo.endswith('.txt'):
            caminho_completo = os.path.join(caminho_docs_encontrado, arquivo)
            try:
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    documentos.append({
                        "arquivo": arquivo,
                        "conteudo": f.read()
                    })
            except Exception as e:
                print(f"⚠️ Erro ao ler {arquivo}: {e}")
    
    return documentos


@lru_cache(maxsize=1)
def carregar_pdfs(
    caminho_pdfs: Optional[str] = None
) -> List[Dict[str, any]]:
    """
    Carrega e processa PDFs da PCDF.
    
    Args:
        caminho_pdfs: Caminho da pasta com PDFs
    
    Returns:
        list: [{
            \"arquivo\": str,
            \"caminho\": str,
            \"conteudo\": str,
            \"num_paginas\": int
        }]
    
    Example:
        >>> pdfs = carregar_pdfs()
        >>> print(f"{len(pdfs)} PDFs carregados")
    """
    if caminho_pdfs is None:
        caminhos_possiveis = [
            os.path.join(DADOS_DIR, "pdfs_pcdf"),  # NOVO: Dados em CODIGOS_AULA
            os.path.join(BASE_DIR, "01_DADOS", "pdfs_pcdf"),  # Caminho antigo
            os.path.join(BASE_DIR, "..", "E5_ESPECIALIZACAO_PDFS", "01_DADOS", "pdfs_pcdf"),  # E5
        ]
    else:
        caminhos_possiveis = [caminho_pdfs]
    
    caminho_pdfs_encontrado = None
    for c in caminhos_possiveis:
        if os.path.exists(c):
            caminho_pdfs_encontrado = c
            break
    
    if not caminho_pdfs_encontrado:
        print(f"⚠️ Pasta de PDFs não encontrada")
        print(f"💡 Crie a pasta: ../01_DADOS/pdfs_pcdf/")
        print(f"💡 Adicione PDFs de leis, manuais, portarias")
        return []
    
    pdfs = []
    total_erros = 0
    
    print("[CACHE] Carregando PDFs...")
    
    for root, dirs, files in os.walk(caminho_pdfs_encontrado):
        for file in files:
            if file.endswith('.pdf'):
                caminho = os.path.join(root, file)
                try:
                    reader = PdfReader(caminho)
                    texto = ""
                    for page in reader.pages:
                        texto += page.extract_text()
                    
                    # Validar se extraiu texto
                    if len(texto.strip()) < 100:
                        print(f"⚠️ {file}: Texto muito curto ({len(texto)} chars), possível erro")
                        total_erros += 1
                        continue
                    
                    pdfs.append({
                        'arquivo': file,
                        'caminho': caminho,
                        'conteudo': texto,
                        'num_paginas': len(reader.pages)
                    })
                    
                    print(f"✅ {file}: {len(reader.pages)} páginas, {len(texto)} caracteres")
                    
                except Exception as e:
                    print(f"❌ {file}: Erro ao ler - {e}")
                    total_erros += 1
    
    print(f"\n[OK] {len(pdfs)} PDFs carregados com sucesso!")
    if total_erros > 0:
        print(f"[AVISO] {total_erros} PDFs com erro")
    
    return pdfs


def limpar_cache():
    """
    Limpa o cache de carregamento de dados.
    
    Útil para recarregar dados após atualizações.
    """
    carregar_csv.cache_clear()
    carregar_documentos_txt.cache_clear()
    carregar_pdfs.cache_clear()
    print("✅ Cache limpo!")
