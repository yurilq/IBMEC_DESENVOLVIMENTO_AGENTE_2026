# tools_basicas.py
# VERSÃO INICIAL - SEM TRATAMENTO DE DADOS
# Esta versão VAI FALHAR propositalmente para ensinar tratamento de dados!

import pandas as pd

def contar_armas_marca(marca: str):
    """Conta quantas armas de uma marca específica"""
    
    # PASSO 1: Carregar CSV
    print(f"Buscando armas da marca: {marca}")
    df = pd.read_csv("DADOS_SINARM/OCORRENCIAS_2026.csv", 
                     sep=";", 
                     encoding="latin1")
    
    # PASSO 2: Filtrar por marca
    # ⚠️ ATENÇÃO: Esta comparação vai falhar!
    # Por quê? Descubra na aula! 🔍
    resultado = df[df["MARCA_ARMA"] == marca.upper()]
    
    # PASSO 3: Contar linhas
    total = len(resultado)
    
    # PASSO 4: Retornar texto
    return f"Encontrei {total} armas da marca {marca}"

# Fim da função

# Teste da função
if __name__ == "__main__":
    print("="*60)
    print("TESTANDO FUNÇÃO")
    print("="*60)
    
    # Teste 1: Taurus
    resultado = contar_armas_marca("Taurus")
    print(f"[RESULTADO] {resultado}")
    
    # ⚠️ ESPERADO: Vai retornar 0 armas!
    # Por quê? Vamos investigar juntos!
    
    # Teste 2: Glock
    resultado = contar_armas_marca("Glock")
    print(f"[RESULTADO] {resultado}")
    
    print("="*60)
    print("\nPROBLEMA: Por que retorna 0?")
    print("SOLUÇÃO: Veja TRATAMENTO_DE_DADOS_E3.md")
