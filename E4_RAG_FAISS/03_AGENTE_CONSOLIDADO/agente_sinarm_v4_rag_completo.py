"""
agente_sinarm_v4_rag_completo.py
=================================

AGENTE SINARM v4.0 - RAG + 8 TOOLS E3
Implementa RAG (Retrieval-Augmented Generation) + todas as tools do E3

PROGRESSO E3  E4:
- E3: 8 tools para dados estruturados (CSV)
- E4: 8 tools E3 + RAG para perguntas conceituais

TOOLS IMPLEMENTADAS (9 total):
1-8. Tools E3 (dados estruturados)
9. buscar_conhecimento - RAG para perguntas conceituais

MODOS DE EXECUO:
1. Sem argumentos: Executa testes automticos
   python agente_sinarm_v4_rag_completo.py

2. Com pergunta: Responde pergunta especfica
   python agente_sinarm_v4_rag_completo.py "Quantas armas Taurus?"

3. Modo interativo: Loop de perguntas
   python agente_sinarm_v4_rag_completo.py --interativo

AUTOR: MBA IA Generativa PCDF - IBMEC
DATA: 2026-07-26
VERSO: 4.0
"""

import pandas as pd
import os
import sys
from functools import lru_cache
from langchain_core.tools import tool
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ============================================================================
# CONFIGURAES
# ============================================================================

# Caminhos relativos ao script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(SCRIPT_DIR, "..", "01_DADOS")
CSV_PATH = os.path.join(DADOS_DIR, "DADOS_SINARM", "OCORRENCIAS", "OCORRENCIAS_2026.csv")
DOCS_PATH = os.path.join(DADOS_DIR, "documentos_conceituais")


# ============================================================================
# CARREGAMENTO DE DADOS ESTRUTURADOS (CSV)
# ============================================================================

@lru_cache(maxsize=1)
def carregar_csv():
    """
    Carrega dados SINARM do CSV.
    Cache garante que carrega apenas UMA VEZ.
    """
    print("[CACHE] Carregando CSV...")
    
    # Tentar diferentes caminhos
    caminhos_possiveis = [
        CSV_PATH,
        os.path.join(DADOS_DIR, "DADOS_SINARM", "OCORRENCIAS_2026.csv"),
        "../01_DADOS/DADOS_SINARM/OCORRENCIAS/OCORRENCIAS_2026.csv",
    ]
    
    caminho = None
    for c in caminhos_possiveis:
        if os.path.exists(c):
            caminho = c
            break
    
    if not caminho:
        raise FileNotFoundError(f"CSV no encontrado em: {caminhos_possiveis}")
    
    # Tentar diferentes configuraes (encoding + separador)
    configs = [
        {'encoding': 'utf-8', 'sep': ','},
        {'encoding': 'utf-8', 'sep': ';'},
        {'encoding': 'latin-1', 'sep': ','},
        {'encoding': 'latin-1', 'sep': ';'},  # Padro CSV brasileiro
        {'encoding': 'iso-8859-1', 'sep': ';'},
        {'encoding': 'cp1252', 'sep': ';'},
    ]
    
    for config in configs:
        try:
            df = pd.read_csv(caminho, **config)
            
            # Validar se carregou corretamente (deve ter mltiplas colunas)
            if len(df.columns) > 1:
                print(f"[OK] {len(df)} registros, {len(df.columns)} colunas carregadas!")
                return df
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    
    raise Exception(f"No foi possvel ler o CSV com nenhuma configurao testada")


# ============================================================================
# CARREGAMENTO DE DOCUMENTOS CONCEITUAIS (RAG)
# ============================================================================

@lru_cache(maxsize=1)
def carregar_documentos_conceituais():
    """
    Carrega documentos .txt para RAG.
    Cache garante que carrega apenas UMA VEZ.
    """
    print("[CACHE] Carregando documentos conceituais...")
    
    if not os.path.exists(DOCS_PATH):
        print(f"[AVISO] Pasta de documentos no encontrada: {DOCS_PATH}")
        return []
    
    documentos = []
    for arquivo in os.listdir(DOCS_PATH):
        if arquivo.endswith('.txt'):
            caminho = os.path.join(DOCS_PATH, arquivo)
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    documentos.append({
                        'arquivo': arquivo,
                        'conteudo': conteudo
                    })
            except Exception as e:
                print(f"[ERRO] No foi possvel ler {arquivo}: {e}")
    
    print(f"[OK] {len(documentos)} documentos carregados!")
    return documentos


# ============================================================================
# SISTEMA RAG (TF-IDF)
# ============================================================================

class SistemaRAG:
    """Sistema de busca semntica usando TF-IDF"""
    
    def __init__(self):
        self.documentos = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self.inicializado = False
    
    def inicializar(self):
        """Inicializa o sistema RAG"""
        if self.inicializado:
            return
        
        print("[RAG] Inicializando sistema RAG...")
        
        # Carregar documentos
        docs = carregar_documentos_conceituais()
        if not docs:
            print("[RAG] Nenhum documento encontrado. RAG desabilitado.")
            return
        
        self.documentos = docs
        textos = [doc['conteudo'] for doc in docs]
        
        # Criar ndice TF-IDF
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words=None  # Manter stop words para portugus
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(textos)
        
        self.inicializado = True
        print(f"[RAG] Sistema inicializado com {len(docs)} documentos!")
    
    def buscar(self, pergunta, k=3, max_chars=500):
        """
        Busca documentos relevantes para a pergunta.
        
        Args:
            pergunta: Pergunta do usurio
            k: Nmero de documentos a retornar
            max_chars: Mximo de caracteres por documento
        
        Returns:
            Lista de trechos relevantes
        """
        if not self.inicializado:
            self.inicializar()
        
        if not self.inicializado:
            return []
        
        # Gerar embedding da pergunta
        query_vec = self.vectorizer.transform([pergunta])
        
        # Calcular similaridades
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        
        # Top-K documentos
        top_k_indices = similarities.argsort()[-k:][::-1]
        
        # Retornar trechos
        resultados = []
        for i in top_k_indices:
            if similarities[i] > 0.01:  # Threshold mnimo
                doc = self.documentos[i]
                trecho = doc['conteudo'][:max_chars]
                resultados.append({
                    'arquivo': doc['arquivo'],
                    'similaridade': float(similarities[i]),
                    'trecho': trecho
                })
        
        return resultados


# Instncia global do sistema RAG
sistema_rag = SistemaRAG()


# ============================================================================
# TOOLS E3 (8 TOOLS DE DADOS ESTRUTURADOS)
# ============================================================================

@tool
def contar_armas_marca(marca: str) -> str:
    """
    Conta quantas armas de uma marca especfica existem no banco.
    
    Args:
        marca: Nome da marca (ex: TAURUS, GLOCK, BERETTA)
    
    Returns:
        String com o resultado da contagem
    """
    df = carregar_csv()
    
    # Busca parcial (aceita variaes)
    resultado = df[df['MARCA_ARMA'].str.contains(marca, case=False, na=False)]
    total = len(resultado)
    
    if total == 0:
        return f"No encontrei armas da marca '{marca}'"
    
    marca_real = resultado['MARCA_ARMA'].iloc[0]
    return f"Encontrei {total} armas da marca '{marca_real}'"


@tool
def contar_armas_calibre(calibre: str) -> str:
    """
    Conta quantas armas de um calibre especfico existem.
    
    Args:
        calibre: Calibre da arma (ex: 9mm, .38, .40)
    """
    df = carregar_csv()
    resultado = df[df['CALIBRE_ARMA'].str.contains(calibre, case=False, na=False)]
    total = len(resultado)
    
    if total == 0:
        return f"No encontrei armas calibre '{calibre}'"
    
    return f"Encontrei {total} armas calibre '{calibre}'"


@tool
def contar_armas_tipo(tipo: str) -> str:
    """
    Conta ocorrncias por tipo (FURTO, ROUBO, APREENSAO).
    
    Args:
        tipo: Tipo de ocorrncia
    """
    df = carregar_csv()
    resultado = df[df['TIPO_OCORRENCIA'].str.contains(tipo, case=False, na=False)]
    total = len(resultado)
    
    if total == 0:
        return f"No encontrei ocorrncias tipo '{tipo}'"
    
    return f"Encontrei {total} ocorrncias tipo '{tipo}'"


@tool
def contar_armas_combinado(marca: str, tipo: str) -> str:
    """
    Conta armas filtrando por marca E tipo de ocorrncia.
    
    Args:
        marca: Nome da marca
        tipo: Tipo de ocorrncia
    """
    df = carregar_csv()
    
    # Filtro combinado
    resultado = df[
        df['MARCA_ARMA'].str.contains(marca, case=False, na=False) &
        df['TIPO_OCORRENCIA'].str.contains(tipo, case=False, na=False)
    ]
    total = len(resultado)
    
    if total == 0:
        return f"No encontrei armas '{marca}' com tipo '{tipo}'"
    
    marca_real = resultado['MARCA_ARMA'].iloc[0]
    return f"Encontrei {total} armas '{marca_real}' do tipo '{tipo}'"


@tool
def ranking_marcas(top: int = 5) -> str:
    """
    Retorna ranking das marcas mais registradas.
    
    Args:
        top: Nmero de marcas no ranking (padro: 5)
    """
    df = carregar_csv()
    ranking = df['MARCA_ARMA'].value_counts().head(top)
    
    resultado = f" TOP {top} Marcas:\n"
    for i, (marca, qtd) in enumerate(ranking.items(), 1):
        resultado += f"{i}. {marca}: {qtd} armas\n"
    
    return resultado


@tool
def ranking_calibres(top: int = 5) -> str:
    """
    Retorna ranking dos calibres mais comuns.
    
    Args:
        top: Nmero de calibres no ranking (padro: 5)
    """
    df = carregar_csv()
    ranking = df['CALIBRE_ARMA'].value_counts().head(top)
    
    resultado = f" TOP {top} Calibres:\n"
    for i, (calibre, qtd) in enumerate(ranking.items(), 1):
        resultado += f"{i}. {calibre}: {qtd} armas\n"
    
    return resultado


@tool
def estatisticas_gerais() -> str:
    """
    Retorna estatsticas gerais do banco de dados.
    """
    df = carregar_csv()
    
    total_armas = len(df)
    total_marcas = df['MARCA_ARMA'].nunique()
    total_calibres = df['CALIBRE_ARMA'].nunique()
    
    marca_mais_comum = df['MARCA_ARMA'].value_counts().index[0]
    calibre_mais_comum = df['CALIBRE_ARMA'].value_counts().index[0]
    
    resultado = f"""
 ESTATSTICAS GERAIS SINARM

Total de Armas: {total_armas}
Total de Marcas: {total_marcas}
Total de Calibres: {total_calibres}

Marca Mais Comum: {marca_mais_comum}
Calibre Mais Comum: {calibre_mais_comum}
"""
    return resultado


@tool
def distribuicao_marca_por_tipo(marca: str) -> str:
    """
    Mostra distribuio de uma marca por tipo de ocorrncia.
    
    Args:
        marca: Nome da marca
    """
    df = carregar_csv()
    
    # Filtrar marca
    resultado_marca = df[df['MARCA_ARMA'].str.contains(marca, case=False, na=False)]
    
    if len(resultado_marca) == 0:
        return f"No encontrei armas da marca '{marca}'"
    
    marca_real = resultado_marca['MARCA_ARMA'].iloc[0]
    
    # Distribuio por tipo
    distribuicao = resultado_marca['TIPO_OCORRENCIA'].value_counts()
    
    resultado = f" Distribuio '{marca_real}' por tipo:\n"
    for tipo, qtd in distribuicao.items():
        percentual = (qtd / len(resultado_marca)) * 100
        resultado += f"  {tipo}: {qtd} ({percentual:.1f}%)\n"
    
    return resultado


# ============================================================================
# TOOL RAG (NOVA NO E4)
# ============================================================================

@tool
def buscar_conhecimento(pergunta: str) -> str:
    """
    Busca informaes conceituais sobre armas, calibres, marcas, etc.
    Use para perguntas como: "O que  calibre?", "O que  SINARM?", etc.
    
    Args:
        pergunta: Pergunta conceitual do usurio
    
    Returns:
        Resposta baseada nos documentos
    """
    # Inicializar RAG se necessrio
    if not sistema_rag.inicializado:
        sistema_rag.inicializar()
    
    if not sistema_rag.inicializado:
        return "Sistema RAG no disponvel. Documentos conceituais no encontrados."
    
    # Buscar documentos relevantes
    resultados = sistema_rag.buscar(pergunta, k=3, max_chars=800)
    
    if not resultados:
        return "No encontrei informaes relevantes sobre essa pergunta."
    
    # Montar resposta
    resposta = " Informaes encontradas:\n\n"
    
    for i, res in enumerate(resultados, 1):
        resposta += f"[{i}] {res['arquivo']} (relevncia: {res['similaridade']:.2f})\n"
        resposta += f"{res['trecho']}\n"
        if i < len(resultados):
            resposta += "\n---\n\n"
    
    return resposta


# ============================================================================
# ROTEADOR INTELIGENTE
# ============================================================================

def rotear_pergunta(pergunta: str):
    """
    Decide qual tool usar baseado na pergunta.
    
    Returns:
        (tool_function, args) ou None
    """
    pergunta_lower = pergunta.lower()
    
    # Perguntas conceituais (RAG) - verificar PRIMEIRO
    if any(palavra in pergunta_lower for palavra in ['o que ', 'o que so', 'explique', 'defina', 'diferena', 'como funciona']):
        return buscar_conhecimento, {'pergunta': pergunta}
    
    # Palavras-chave para dados estruturados (tools E3)
    if any(palavra in pergunta_lower for palavra in ['quantas', 'quantos', 'contar', 'nmero', 'existem']):
        # Perguntas de contagem - verificar marca PRIMEIRO
        for marca in ['taurus', 'glock', 'beretta', 'imbel', 'rossi', 'sig']:
            if marca in pergunta_lower:
                return contar_armas_marca, {'marca': marca.upper()}
        
        # Depois verificar calibre
        for calibre in ['9mm', '.38', '.40', '.45', '.380', '.357']:
            if calibre in pergunta_lower:
                return contar_armas_calibre, {'calibre': calibre}
        
        # Por último, tipo de ocorrência
        for tipo in ['furto', 'roubo', 'apreensao', 'perda']:
            if tipo in pergunta_lower:
                return contar_armas_tipo, {'tipo': tipo.upper()}
    
    # Ranking
    if 'ranking' in pergunta_lower or 'top' in pergunta_lower:
        if 'marca' in pergunta_lower:
            return ranking_marcas, {}
        if 'calibre' in pergunta_lower:
            return ranking_calibres, {}
    
    # Estatsticas
    if 'estatistica' in pergunta_lower or 'resumo' in pergunta_lower or 'geral' in pergunta_lower:
        return estatisticas_gerais, {}
    
    # Distribuio
    if 'distribuicao' in pergunta_lower or 'distribuio' in pergunta_lower:
        for marca in ['taurus', 'glock', 'beretta', 'imbel', 'rossi', 'sig']:
            if marca in pergunta_lower:
                return distribuicao_marca_por_tipo, {'marca': marca.upper()}
    
    # Padro: tentar RAG
    return buscar_conhecimento, {'pergunta': pergunta}


def processar_pergunta(pergunta: str) -> str:
    """
    Processa uma pergunta e retorna a resposta.
    """
    print(f"\n Pergunta: {pergunta}")
    
    # Rotear pergunta
    resultado = rotear_pergunta(pergunta)
    
    if resultado is None:
        return "No consegui entender sua pergunta. Tente reformular."
    
    tool_func, args = resultado
    
    # Executar tool
    try:
        print(f" Usando: {tool_func.name}")
        resposta = tool_func.invoke(args)
        return resposta
    except Exception as e:
        return f"Erro ao processar pergunta: {e}"


# ============================================================================
# TESTES AUTOMTICOS
# ============================================================================

def executar_testes():
    """Executa bateria de testes automticos"""
    print("="*60)
    print(" EXECUTANDO TESTES AUTOMTICOS")
    print("="*60)
    
    # Testes de dados estruturados (Tools E3)
    testes_e3 = [
        "Quantas armas Taurus existem?",
        "Quantas armas calibre 9mm?",
        "Quantos roubos foram registrados?",
        "Ranking de marcas",
        "Ranking de calibres",
        "Estatsticas gerais",
        "Distribuio Taurus por tipo",
    ]
    
    # Testes de RAG (Tool E4)
    testes_e4 = [
        "O que  calibre?",
        "O que  SINARM?",
        "Qual a diferena entre pistola e revlver?",
    ]
    
    print("\n TESTES E3 (Dados Estruturados)")
    print("-"*60)
    for pergunta in testes_e3:
        resposta = processar_pergunta(pergunta)
        print(f" {resposta}\n")
    
    print("\n TESTES E4 (RAG)")
    print("-"*60)
    for pergunta in testes_e4:
        resposta = processar_pergunta(pergunta)
        print(f" {resposta[:200]}...\n")  # Primeiros 200 chars
    
    print("="*60)
    print(" TESTES CONCLUDOS!")
    print("="*60)


# ============================================================================
# MODO INTERATIVO
# ============================================================================

def modo_interativo():
    """Modo interativo de perguntas"""
    print("="*60)
    print(" MODO INTERATIVO")
    print("="*60)
    print("Digite suas perguntas (ou 'sair' para encerrar)")
    print("-"*60)
    
    while True:
        try:
            pergunta = input("\n Voc: ").strip()
            
            if not pergunta:
                continue
            
            if pergunta.lower() in ['sair', 'exit', 'quit']:
                print(" At logo!")
                break
            
            resposta = processar_pergunta(pergunta)
            print(f"\n Agente: {resposta}")
            
        except KeyboardInterrupt:
            print("\n\n At logo!")
            break
        except Exception as e:
            print(f"\n Erro: {e}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Funo principal"""
    print("="*60)
    print(" AGENTE SINARM v4.0 - RAG + 8 TOOLS E3")
    print("="*60)
    
    # Verificar argumentos
    if len(sys.argv) == 1:
        # Sem argumentos: testes automticos
        executar_testes()
    
    elif sys.argv[1] == '--interativo':
        # Modo interativo
        modo_interativo()
    
    else:
        # Pergunta nica
        pergunta = ' '.join(sys.argv[1:])
        resposta = processar_pergunta(pergunta)
        print(f"\n Resposta: {resposta}")


if __name__ == "__main__":
    main()
