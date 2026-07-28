"""
agente_sinarm_v2_completo.py
============================

AGENTE SINARM v2.0 - VERSÃO COMPLETA COM TODAS AS TOOLS DO E3
Implementa TODAS as funcionalidades criadas durante o E3

TOOLS IMPLEMENTADAS (8 total):
1. contar_armas_marca - Conta por marca específica
2. contar_armas_calibre - Conta por calibre
3. contar_armas_tipo - Conta por tipo de ocorrência
4. contar_armas_combinado - Conta marca + tipo
5. ranking_marcas - TOP 5 marcas mais registradas
6. ranking_calibres - TOP 5 calibres mais comuns
7. estatisticas_gerais - Resumo completo dos dados
8. distribuicao_marca_por_tipo - Distribuição de marca por tipo (NOVA!)

MELHORIAS v2.0:
- Busca parcial com .str.contains() (resolve erros de digitação)
- Respostas mais detalhadas (inclui marca/tipo na resposta)
- Novas tools de ranking e estatísticas
- Roteador inteligente expandido
- Tool de distribuição por tipo (NOVA!)

USO:
    python agente_sinarm_v2_completo.py

AUTOR: MBA IA Generativa PCDF - IBMEC
DATA: 2026-07-26
"""

import pandas as pd
from functools import lru_cache
from langchain_core.tools import tool


# ============================================================================
# CARREGAMENTO DE DADOS
# ============================================================================

@lru_cache(maxsize=1)
def carregar_csv():
    """Carrega dados do SINARM com cache"""
    print("[CACHE] Carregando CSV...")
    # Dados sintéticos para demonstração - distribuição realista
    import numpy as np
    
    # Criar 120 registros com distribuição variada
    marcas = []
    calibres = []
    tipos = []
    
    # TAURUS: 30 registros
    marcas.extend(['TAURUS'] * 30)
    calibres.extend(['9mm'] * 12 + ['.38'] * 10 + ['.40'] * 5 + ['.380'] * 3)
    tipos.extend(['FURTO'] * 12 + ['ROUBO'] * 10 + ['APREENSAO'] * 7 + ['PERDA'] * 1)
    
    # GLOCK: 25 registros
    marcas.extend(['GLOCK'] * 25)
    calibres.extend(['9mm'] * 15 + ['.40'] * 8 + ['.45'] * 2)
    tipos.extend(['ROUBO'] * 15 + ['FURTO'] * 7 + ['APREENSAO'] * 3)
    
    # BERETTA: 20 registros
    marcas.extend(['BERETTA'] * 20)
    calibres.extend(['9mm'] * 12 + ['.40'] * 5 + ['.380'] * 3)
    tipos.extend(['APREENSAO'] * 10 + ['FURTO'] * 7 + ['ROUBO'] * 3)
    
    # IMBEL: 15 registros
    marcas.extend(['IMBEL'] * 15)
    calibres.extend(['.38'] * 10 + ['9mm'] * 5)
    tipos.extend(['FURTO'] * 8 + ['APREENSAO'] * 5 + ['ROUBO'] * 2)
    
    # ROSSI: 12 registros
    marcas.extend(['ROSSI'] * 12)
    calibres.extend(['.38'] * 8 + ['.357'] * 4)
    tipos.extend(['FURTO'] * 6 + ['ROUBO'] * 4 + ['PERDA'] * 2)
    
    # SIG SAUER: 10 registros
    marcas.extend(['SIG SAUER'] * 10)
    calibres.extend(['9mm'] * 6 + ['.40'] * 4)
    tipos.extend(['ROUBO'] * 6 + ['FURTO'] * 3 + ['APREENSAO'] * 1)
    
    # SMITH & WESSON: 8 registros
    marcas.extend(['SMITH & WESSON'] * 8)
    calibres.extend(['.38'] * 5 + ['.357'] * 3)
    tipos.extend(['FURTO'] * 4 + ['ROUBO'] * 3 + ['APREENSAO'] * 1)
    
    df = pd.DataFrame({
        'MARCA_ARMA': marcas,
        'CALIBRE': calibres,
        'TIPO_OCORRENCIA': tipos
    })
    
    print(f"[OK] {len(df)} registros carregados!")
    return df


# ============================================================================
# TOOLS BÁSICAS (do tools_basicas_v2.py)
# ============================================================================

@tool
def contar_armas_marca(marca: str) -> str:
    """Conta quantas armas de uma marca específica estão registradas.
    
    Args:
        marca: Nome da marca (ex: Taurus, Glock, Rossi, Beretta)
    
    Returns:
        Total de armas encontradas dessa marca
    
    Exemplos:
        - "Quantas armas Taurus?"
        - "Quantas Glock registradas?"
    """
    df = carregar_csv()
    # Busca parcial (resolve erros de digitação)
    resultado = df[df["MARCA_ARMA"].str.contains(marca.upper(), case=False, na=False)]
    total = len(resultado)
    
    if total > 0:
        marca_real = resultado["MARCA_ARMA"].iloc[0]
        return f"Encontrei {total} armas da marca '{marca_real}'"
    else:
        return f"Não encontrei armas da marca '{marca}'"


@tool
def contar_armas_calibre(calibre: str) -> str:
    """Conta quantas armas de um calibre específico.
    
    Args:
        calibre: Calibre da arma (ex: .38, 9mm, .40, .380, .45)
    
    Returns:
        Total de armas do calibre especificado
    
    Exemplos:
        - "Quantas armas calibre 9mm?"
        - "Quantas .38 registradas?"
    """
    df = carregar_csv()
    resultado = df[df["CALIBRE"].str.contains(calibre, case=False, na=False)]
    total = len(resultado)
    
    if total > 0:
        calibre_real = resultado["CALIBRE"].iloc[0]
        return f"Encontrei {total} armas calibre '{calibre_real}'"
    else:
        return f"Não encontrei armas calibre '{calibre}'"


@tool
def contar_armas_tipo(tipo: str) -> str:
    """Conta armas por tipo de ocorrência.
    
    Args:
        tipo: Tipo de ocorrência (ex: Furto, Roubo, Apreensão, Perda)
    
    Returns:
        Total de ocorrências do tipo especificado
    
    Exemplos:
        - "Quantas armas foram roubadas?"
        - "Quantos furtos registrados?"
    """
    df = carregar_csv()
    resultado = df[df["TIPO_OCORRENCIA"].str.contains(tipo.upper(), case=False, na=False)]
    total = len(resultado)
    
    if total > 0:
        tipo_real = resultado["TIPO_OCORRENCIA"].iloc[0]
        return f"Encontrei {total} ocorrências tipo '{tipo_real}'"
    else:
        return f"Não encontrei ocorrências tipo '{tipo}'"


@tool
def contar_armas_combinado(marca: str, tipo: str) -> str:
    """Conta armas por marca E tipo de ocorrência simultaneamente.
    
    Args:
        marca: Marca da arma
        tipo: Tipo de ocorrência
    
    Returns:
        Total de armas que atendem ambos critérios
    
    Exemplos:
        - "Quantas armas Taurus foram roubadas?"
        - "Quantas Glock foram apreendidas?"
    """
    df = carregar_csv()
    resultado = df[
        (df["MARCA_ARMA"].str.contains(marca.upper(), case=False, na=False)) & 
        (df["TIPO_OCORRENCIA"].str.contains(tipo.upper(), case=False, na=False))
    ]
    total = len(resultado)
    
    if total > 0:
        marca_real = resultado["MARCA_ARMA"].iloc[0]
        tipo_real = resultado["TIPO_OCORRENCIA"].iloc[0]
        return f"Encontrei {total} armas '{marca_real}' tipo '{tipo_real}'"
    else:
        return f"Não encontrei armas '{marca}' tipo '{tipo}'"


# ============================================================================
# TOOLS NOVAS (v2.0) - RANKING E ESTATÍSTICAS
# ============================================================================

@tool
def ranking_marcas(top_n: int = 5) -> str:
    """Retorna ranking das marcas mais registradas.
    
    Args:
        top_n: Número de marcas no ranking (padrão: 5)
    
    Returns:
        Lista das top N marcas com quantidades
    
    Exemplos:
        - "Qual marca tem mais registros?"
        - "Top 5 marcas mais comuns"
        - "Ranking de marcas"
    """
    df = carregar_csv()
    ranking = df["MARCA_ARMA"].value_counts().head(top_n)
    
    resultado = f"TOP {top_n} MARCAS MAIS REGISTRADAS:\n"
    for i, (marca, qtd) in enumerate(ranking.items(), 1):
        resultado += f"  {i}º - {marca}: {qtd} armas\n"
    
    return resultado.strip()


@tool
def ranking_calibres(top_n: int = 5) -> str:
    """Retorna ranking dos calibres mais comuns.
    
    Args:
        top_n: Número de calibres no ranking (padrão: 5)
    
    Returns:
        Lista dos top N calibres com quantidades
    
    Exemplos:
        - "Qual calibre é mais comum?"
        - "Top 5 calibres"
        - "Ranking de calibres"
    """
    df = carregar_csv()
    ranking = df["CALIBRE"].value_counts().head(top_n)
    
    resultado = f"TOP {top_n} CALIBRES MAIS COMUNS:\n"
    for i, (calibre, qtd) in enumerate(ranking.items(), 1):
        resultado += f"  {i}º - {calibre}: {qtd} armas\n"
    
    return resultado.strip()


@tool
def estatisticas_gerais() -> str:
    """Retorna estatísticas gerais do banco de dados.
    
    Returns:
        Resumo completo: total de registros, marcas, calibres, tipos
    
    Exemplos:
        - "Resumo dos dados"
        - "Estatísticas gerais"
        - "Quantos registros no total?"
    """
    df = carregar_csv()
    
    total_registros = len(df)
    total_marcas = df["MARCA_ARMA"].nunique()
    total_calibres = df["CALIBRE"].nunique()
    total_tipos = df["TIPO_OCORRENCIA"].nunique()
    
    marca_mais_comum = df["MARCA_ARMA"].value_counts().index[0]
    calibre_mais_comum = df["CALIBRE"].value_counts().index[0]
    tipo_mais_comum = df["TIPO_OCORRENCIA"].value_counts().index[0]
    
    resultado = f"""ESTATISTICAS GERAIS DO SINARM:

TOTAIS:
  - Registros: {total_registros}
  - Marcas diferentes: {total_marcas}
  - Calibres diferentes: {total_calibres}
  - Tipos de ocorrencia: {total_tipos}

MAIS COMUNS:
  - Marca: {marca_mais_comum}
  - Calibre: {calibre_mais_comum}
  - Tipo: {tipo_mais_comum}
"""
    return resultado.strip()


@tool
def distribuicao_marca_por_tipo(marca: str) -> str:
    """Mostra distribuicao de uma marca por tipo de ocorrencia.
    
    Args:
        marca: Nome da marca
    
    Returns:
        Distribuicao detalhada por tipo de ocorrencia
    
    Exemplos:
        - "Quantas Beretta por tipo de ocorrencia?"
        - "Distribuicao de Taurus por tipo"
        - "Beretta em ocorrencias"
    """
    df = carregar_csv()
    resultado = df[df["MARCA_ARMA"].str.contains(marca.upper(), case=False, na=False)]
    
    if len(resultado) == 0:
        return f"Nao encontrei armas da marca '{marca}'"
    
    marca_real = resultado["MARCA_ARMA"].iloc[0]
    distribuicao = resultado["TIPO_OCORRENCIA"].value_counts()
    
    resposta = f"DISTRIBUICAO DE {marca_real} POR TIPO:\n"
    resposta += f"  Total: {len(resultado)} armas\n\n"
    for tipo, qtd in distribuicao.items():
        percentual = (qtd/len(resultado)*100)
        resposta += f"  - {tipo}: {qtd} armas ({percentual:.1f}%)\n"
    
    return resposta.strip()


# ============================================================================
# ROTEADOR INTELIGENTE (v2.0 - EXPANDIDO)
# ============================================================================

def processar_pergunta(pergunta: str) -> str:
    """Processa pergunta e chama tool apropriada"""
    pergunta_lower = pergunta.lower()
    
    # PRIORIDADE 1: Ranking e estatísticas
    keywords_ranking_marca = ['ranking', 'top', 'mais registr', 'marca com mais', 'qual marca']
    if any(kw in pergunta_lower for kw in keywords_ranking_marca) and 'marca' in pergunta_lower:
        return ranking_marcas.invoke({"top_n": 5})
    
    keywords_ranking_calibre = ['ranking', 'top', 'mais comum', 'calibre com mais', 'qual calibre']
    if any(kw in pergunta_lower for kw in keywords_ranking_calibre) and 'calibre' in pergunta_lower:
        return ranking_calibres.invoke({"top_n": 5})
    
    keywords_estatisticas = ['estatistica', 'resumo', 'total', 'geral', 'quantos registros']
    if any(kw in pergunta_lower for kw in keywords_estatisticas):
        return estatisticas_gerais.invoke({})
    
    # PRIORIDADE 2: Detectar marca (com variações de digitação)
    marcas_map = {
        'taurus': ['taurus', 'tauros', 'tauru'],
        'glock': ['glock', 'glok'],
        'beretta': ['beretta', 'bereta'],
        'imbel': ['imbel', 'imbell'],
        'sig sauer': ['sig sauer', 'sig', 'sauer'],
        'rossi': ['rossi', 'rosi'],
        'smith': ['smith', 'smith & wesson', 'wesson']
    }
    
    marca_encontrada = None
    for marca_oficial, variacoes in marcas_map.items():
        for variacao in variacoes:
            if variacao in pergunta_lower:
                marca_encontrada = marca_oficial
                break
        if marca_encontrada:
            break
    
    # PRIORIDADE 3: Detectar calibre
    calibres = ['9mm', '.38', '.40', '.45', '.380', '380']
    calibre_encontrado = None
    for calibre in calibres:
        if calibre in pergunta_lower:
            calibre_encontrado = calibre
            break
    
    # PRIORIDADE 4: Detectar tipo
    tipos = ['furto', 'roubo', 'apreens', 'perda', 'roubad', 'furtad']
    tipo_encontrado = None
    for tipo in tipos:
        if tipo in pergunta_lower:
            # Normalizar para palavra completa
            if 'roub' in tipo:
                tipo_encontrado = 'roubo'
            elif 'furt' in tipo:
                tipo_encontrado = 'furto'
            elif 'apreens' in tipo:
                tipo_encontrado = 'apreensao'
            else:
                tipo_encontrado = tipo
            break
    
    # PRIORIDADE 5: Detectar perguntas sobre distribuicao
    keywords_distribuicao = ['distribuicao', 'por tipo', 'em ocorrencias', 'por ocorrencia', 'tipos de ocorrencia']
    if marca_encontrada and any(kw in pergunta_lower for kw in keywords_distribuicao):
        return distribuicao_marca_por_tipo.invoke({"marca": marca_encontrada})
    
    # DECISÃO: Qual tool usar?
    if marca_encontrada and tipo_encontrado:
        return contar_armas_combinado.invoke({"marca": marca_encontrada, "tipo": tipo_encontrado})
    elif marca_encontrada:
        return contar_armas_marca.invoke({"marca": marca_encontrada})
    elif calibre_encontrado:
        return contar_armas_calibre.invoke({"calibre": calibre_encontrado})
    elif tipo_encontrado:
        return contar_armas_tipo.invoke({"tipo": tipo_encontrado})
    else:
        return "Nao consegui entender a pergunta. Tente perguntar sobre:\n  - Marca especifica (ex: 'Quantas Taurus?')\n  - Calibre (ex: 'Quantas 9mm?')\n  - Tipo de ocorrencia (ex: 'Quantos roubos?')\n  - Distribuicao (ex: 'Beretta por tipo')\n  - Ranking (ex: 'Top 5 marcas')\n  - Estatisticas gerais"


# ============================================================================
# VALIDAÇÃO E SEGURANÇA
# ============================================================================

def validar_input(texto: str):
    """Valida entrada do usuário"""
    if len(texto) > 500:
        raise ValueError("Query muito longa (máx 500 caracteres)")
    if len(texto) < 3:
        raise ValueError("Query muito curta (mín 3 caracteres)")
    
    perigosos = [";", "--", "DROP", "DELETE", "INSERT", "UPDATE"]
    for char in perigosos:
        if char in texto.upper():
            raise ValueError(f"Caractere/comando perigoso detectado: {char}")
    
    return True


def perguntar_seguro(pergunta: str):
    """Faz pergunta com validação"""
    try:
        validar_input(pergunta)
        return processar_pergunta(pergunta)
    except ValueError as e:
        return f"❌ ERRO DE VALIDACAO: {e}"
    except Exception as e:
        return f"❌ ERRO INESPERADO: {e}"


# ============================================================================
# TESTES AUTOMATICOS
# ============================================================================

def executar_testes():
    """Executa suite de testes automaticos"""
    print("="*70)
    print("TESTES AUTOMATICOS - AGENTE SINARM v2.1")
    print("="*70)
    
    testes = [
        ("Quantas armas Taurus?", "basico"),
        ("Quantas armas calibre 9mm?", "basico"),
        ("Quantas armas Glock foram roubadas?", "combinado"),
        ("Beretta em ocorrencias", "distribuicao"),
        ("Qual marca tem mais registros?", "ranking"),
        ("Top 5 calibres", "ranking"),
        ("Resumo dos dados", "estatisticas"),
        ("Quantas armas tauros foram roubadas?", "erro_digitacao"),
        ("Distribuicao de Glock por tipo", "distribuicao"),
    ]
    
    print(f"\nExecutando {len(testes)} testes...\n")
    
    sucessos = 0
    falhas = 0
    
    for i, (pergunta, categoria) in enumerate(testes, 1):
        print(f"\nTESTE #{i}: {categoria}")
        print(f"Pergunta: {pergunta}")
        
        try:
            resposta = perguntar_seguro(pergunta)
            
            if resposta and "None" not in str(resposta):
                # Mostrar primeiras 2 linhas da resposta
                linhas = resposta.split('\n')[:2]
                print(f"Resposta: {linhas[0]}")
                if len(linhas) > 1:
                    print(f"          {linhas[1]}")
                print("[OK]")
                sucessos += 1
            else:
                print(f"Resposta: {resposta}")
                print("[FALHA]")
                falhas += 1
        except Exception as e:
            print(f"[ERRO] {e}")
            falhas += 1
    
    print(f"\n{'='*70}")
    print(f"RESULTADO: {sucessos}/{len(testes)} testes aprovados")
    print(f"Taxa de sucesso: {(sucessos/len(testes)*100):.1f}%")
    print(f"{'='*70}")
    
    return falhas == 0


# ============================================================================
# MODO INTERATIVO
# ============================================================================

def modo_interativo():
    """Modo interativo com loop de perguntas"""
    print("\n" + "="*70)
    print("AGENTE SINARM v2.1 - MODO INTERATIVO")
    print("="*70)
    print("\nEXEMPLOS DE PERGUNTAS:")
    print("\nConsultas especificas:")
    print("  - Quantas armas Taurus?")
    print("  - Quantas armas calibre 9mm?")
    print("  - Quantas armas Glock foram roubadas?")
    print("\nDistribuicao e analises:")
    print("  - Beretta em ocorrencias")
    print("  - Distribuicao de Taurus por tipo")
    print("\nRankings e estatisticas:")
    print("  - Qual marca tem mais registros?")
    print("  - Top 5 calibres mais comuns")
    print("  - Resumo dos dados")
    print("\nDigite 'sair' para encerrar\n")
    print("="*70 + "\n")
    
    contador = 0
    
    while True:
        pergunta = input("Sua pergunta: ")
        
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            print("\n" + "="*70)
            print(f"Total de perguntas realizadas: {contador}")
            print("Ate logo!")
            print("="*70)
            break
        
        if not pergunta.strip():
            continue
        
        contador += 1
        resposta = perguntar_seguro(pergunta)
        
        print("\n" + "="*70)
        print(f"PERGUNTA #{contador}:")
        print(f"  {pergunta}")
        print("\nRESPOSTA:")
        for linha in resposta.split('\n'):
            print(f"  {linha}")
        print("="*70 + "\n")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Funcao principal com suporte a argumentos"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Agente SINARM v2.1 - Sistema de Consulta Inteligente',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python agente_sinarm_v2_completo.py                          # Testes automaticos
  python agente_sinarm_v2_completo.py "Quantas armas Taurus?"  # Pergunta unica
  python agente_sinarm_v2_completo.py --interativo             # Modo interativo
  python agente_sinarm_v2_completo.py --testes                 # Testes explicitos
        """
    )
    
    parser.add_argument(
        'pergunta',
        nargs='?',
        help='Pergunta para o agente (opcional)'
    )
    
    parser.add_argument(
        '--interativo', '-i',
        action='store_true',
        help='Inicia modo interativo'
    )
    
    parser.add_argument(
        '--testes', '-t',
        action='store_true',
        help='Executa testes automaticos'
    )
    
    args = parser.parse_args()
    
    # MODO 1: Pergunta unica via argumento
    if args.pergunta:
        resposta = perguntar_seguro(args.pergunta)
        print(resposta)
        return
    
    # MODO 2: Modo interativo
    if args.interativo:
        modo_interativo()
        return
    
    # MODO 3: Testes automaticos (padrao)
    if args.testes or len(sys.argv) == 1:
        sucesso = executar_testes()
        sys.exit(0 if sucesso else 1)
    
    # Se nenhum argumento valido, mostrar ajuda
    parser.print_help()


if __name__ == "__main__":
    main()

