# CORREÇÃO: Agente que compara múltiplas marcas

## 🔴 PROBLEMA IDENTIFICADO

### Código Atual (linhas 96-101):
```python
# Detectar marca
marcas = ["taurus", "glock", "rossi", "beretta", "smith"]
marca_encontrada = None
for marca in marcas:
    if marca in pergunta_lower:
        marca_encontrada = marca.capitalize()
        break  # ← PROBLEMA! Para na primeira marca encontrada
```

**Pergunta:** "Há mais Taurus ou Glock?"

**O que acontece:**
1. Detecta "taurus" → `marca_encontrada = "Taurus"`
2. Faz `break` → **PARA AQUI**
3. Nunca detecta "glock"
4. Chama tool apenas para Taurus
5. Resposta incorreta ❌

---

## ✅ SOLUÇÃO: Detectar TODAS as marcas

### Versão Corrigida:

```python
def agente_v3_fewshot_cot_comparacao(pergunta_usuario):
    """
    Agente v3.0 que DETECTA MÚLTIPLAS MARCAS
    e faz COMPARAÇÕES
    """
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*60)
    
    pergunta_lower = pergunta_usuario.lower()
    
    # ✅ SOLUÇÃO: Detectar TODAS as marcas (não só a primeira)
    marcas_disponiveis = ["taurus", "glock", "rossi", "beretta", "smith"]
    marcas_encontradas = []
    
    for marca in marcas_disponiveis:
        if marca in pergunta_lower:
            marcas_encontradas.append(marca.capitalize())
    
    print(f"[DETECÇÃO] Marcas encontradas: {marcas_encontradas}")
    
    # Detectar palavras de comparação
    palavras_comparacao = ["mais", "menos", "maior", "menor", "comparar", "diferenca", "ou"]
    eh_comparacao = any(palavra in pergunta_lower for palavra in palavras_comparacao)
    
    # ===== CASO 1: COMPARAÇÃO (múltiplas marcas) =====
    if len(marcas_encontradas) >= 2 and eh_comparacao:
        print(f"[TIPO] COMPARAÇÃO entre {len(marcas_encontradas)} marcas")
        print("[CHAIN-OF-THOUGHT]")
        print(f"PASSO 1: Pergunta de COMPARAÇÃO detectada")
        print(f"PASSO 2: Executar tool para cada marca")
        
        resultados = {}
        
        for marca in marcas_encontradas:
            print(f"PASSO 2.{len(resultados)+1}: Buscando dados de {marca}...")
            resultado = contar_armas_marca.func(marca)
            
            # Extrair número
            import re
            numeros = re.findall(r'\d+', resultado)
            total = int(numeros[0]) if numeros else 0
            
            resultados[marca] = total
            print(f"         {marca}: {total:,} armas")
        
        print(f"\nPASSO 3: Comparando resultados...")
        
        # Encontrar maior e menor
        marca_maior = max(resultados, key=resultados.get)
        marca_menor = min(resultados, key=resultados.get)
        diferenca = resultados[marca_maior] - resultados[marca_menor]
        
        print(f"         Maior: {marca_maior} ({resultados[marca_maior]:,} armas)")
        print(f"         Menor: {marca_menor} ({resultados[marca_menor]:,} armas)")
        print(f"         Diferença: {diferenca:,} armas")
        
        print(f"\nPASSO 4: Formular resposta final...")
        
        # Formatar resposta
        resposta = f"Segundo o SINARM 2026:\n\n"
        
        for marca, total in resultados.items():
            resposta += f"- {marca.upper()}: {total:,} armas\n"
        
        resposta += f"\nConclusão: Há {diferenca:,} armas {marca_maior.upper()} a mais que {marca_menor.upper()}.\n"
        resposta += f"Portanto, {marca_maior.upper()} tem mais armas registradas.\n\n"
        resposta += f"Fonte: SINARM 2026, OCORRENCIAS_2026.csv"
        
        return resposta
    
    # ===== CASO 2: MARCA ÚNICA =====
    elif len(marcas_encontradas) == 1:
        print(f"[TIPO] CONSULTA SIMPLES (1 marca)")
        marca = marcas_encontradas[0]
        
        print("[CHAIN-OF-THOUGHT]")
        print(f"PASSO 1: Pergunta sobre DADOS")
        print(f"PASSO 2: Tool = contar_armas_marca")
        print(f"PASSO 3: Buscando dados de {marca}...")
        
        resultado = contar_armas_marca.func(marca)
        
        print(f"PASSO 4: Dados obtidos = {resultado}")
        print(f"PASSO 5: Formatando resposta...")
        
        # Extrair número
        import re
        numeros = re.findall(r'\d+', resultado)
        total = numeros[0] if numeros else "?"
        
        resposta = f"Segundo o SINARM 2026, existem {total} armas da marca {marca.upper()}.\n"
        resposta += f"Fonte: SINARM 2026, OCORRENCIAS_2026.csv"
        
        return resposta
    
    # ===== CASO 3: NENHUMA MARCA =====
    else:
        print(f"[TIPO] SEM MARCAS DETECTADAS")
        return "Não consegui identificar marcas de armas na pergunta. Por favor, especifique a marca (ex: Taurus, Glock, Rossi)."
```

---

## 📝 CÓDIGO COMPLETO CORRIGIDO

Arquivo: `agente_v3_1_comparacao.py`

```python
# agente_v3_1_comparacao.py
# Agente v3.1 COM suporte a COMPARAÇÃO de múltiplas marcas

from langchain_ollama import OllamaLLM
from tools_basicas_v2 import (
    contar_armas_marca,
    contar_armas_calibre,
    contar_armas_tipo,
    contar_armas_combinado
)
import re

print("="*60)
print("AGENTE v3.1 - Comparação de Múltiplas Marcas")
print("="*60)

def agente_v3_1_comparacao(pergunta_usuario):
    """
    Agente v3.1 que suporta:
    - Consultas simples: "Quantas armas Taurus?"
    - Comparações: "Há mais Taurus ou Glock?"
    - Múltiplas marcas: "Compare Taurus, Glock e Rossi"
    """
    
    print(f"\n[PERGUNTA] {pergunta_usuario}")
    print("-"*60)
    
    pergunta_lower = pergunta_usuario.lower()
    
    # ===== DETECTAR TODAS AS MARCAS (não só a primeira) =====
    marcas_disponiveis = ["taurus", "glock", "rossi", "beretta", "smith"]
    marcas_encontradas = []
    
    for marca in marcas_disponiveis:
        if marca in pergunta_lower:
            marcas_encontradas.append(marca.capitalize())
    
    print(f"[DETECÇÃO] Marcas: {marcas_encontradas if marcas_encontradas else 'Nenhuma'}")
    
    # Detectar palavras de comparação
    palavras_comparacao = [
        "mais", "menos", "maior", "menor", 
        "comparar", "compare", "diferenca", "diferença",
        "ou", "vs", "versus"
    ]
    eh_comparacao = any(palavra in pergunta_lower for palavra in palavras_comparacao)
    
    # ===== CASO 1: COMPARAÇÃO (2+ marcas) =====
    if len(marcas_encontradas) >= 2 and eh_comparacao:
        print(f"[TIPO] COMPARAÇÃO")
        print("\n[CHAIN-OF-THOUGHT]")
        print(f"PASSO 1: Detectei {len(marcas_encontradas)} marcas para comparar")
        print(f"PASSO 2: Executar tool {len(marcas_encontradas)}x")
        
        resultados = {}
        
        for i, marca in enumerate(marcas_encontradas, 1):
            print(f"\nPASSO 2.{i}: Consultando {marca}...")
            resultado = contar_armas_marca.func(marca)
            
            # Extrair número
            numeros = re.findall(r'\d+', resultado)
            total = int(numeros[0]) if numeros else 0
            
            resultados[marca] = total
            print(f"         → {marca}: {total:,} armas")
        
        print(f"\nPASSO 3: Comparando resultados...")
        
        # Ordenar por quantidade (maior para menor)
        marcas_ordenadas = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
        
        marca_maior = marcas_ordenadas[0][0]
        total_maior = marcas_ordenadas[0][1]
        marca_menor = marcas_ordenadas[-1][0]
        total_menor = marcas_ordenadas[-1][1]
        diferenca = total_maior - total_menor
        
        print(f"         Ranking:")
        for i, (marca, total) in enumerate(marcas_ordenadas, 1):
            print(f"         {i}º {marca}: {total:,} armas")
        
        print(f"\nPASSO 4: Formular resposta final...")
        
        # ===== RESPOSTA FORMATADA =====
        resposta = "Segundo o SINARM 2026:\n\n"
        
        # Mostrar todas as marcas
        for i, (marca, total) in enumerate(marcas_ordenadas, 1):
            resposta += f"{i}º {marca.upper()}: {total:,} armas\n"
        
        resposta += f"\n" + "="*50 + "\n"
        resposta += f"Conclusão:\n"
        resposta += f"- {marca_maior.upper()} tem MAIS armas ({total_maior:,})\n"
        resposta += f"- {marca_menor.upper()} tem MENOS armas ({total_menor:,})\n"
        resposta += f"- Diferença: {diferenca:,} armas\n"
        resposta += f"\n→ Resposta: {marca_maior.upper()} tem {diferenca:,} armas a mais.\n"
        resposta += f"\nFonte: SINARM 2026, OCORRENCIAS_2026.csv"
        
        return resposta
    
    # ===== CASO 2: CONSULTA SIMPLES (1 marca) =====
    elif len(marcas_encontradas) == 1:
        print(f"[TIPO] CONSULTA SIMPLES")
        marca = marcas_encontradas[0]
        
        print("\n[CHAIN-OF-THOUGHT]")
        print(f"PASSO 1: Pergunta sobre 1 marca ({marca})")
        print(f"PASSO 2: Tool = contar_armas_marca")
        print(f"PASSO 3: Executando...")
        
        resultado = contar_armas_marca.func(marca)
        
        print(f"PASSO 4: Resultado obtido")
        
        # Extrair número
        numeros = re.findall(r'\d+', resultado)
        total = int(numeros[0]) if numeros else 0
        
        resposta = f"Segundo o SINARM 2026:\n"
        resposta += f"- {marca.upper()}: {total:,} armas\n"
        resposta += f"\nFonte: SINARM 2026, OCORRENCIAS_2026.csv"
        
        return resposta
    
    # ===== CASO 3: SEM MARCAS =====
    else:
        print(f"[TIPO] SEM MARCAS")
        print("\n[ERRO] Nenhuma marca detectada na pergunta")
        
        return "Não consegui identificar marcas de armas na pergunta.\n" \
               "Marcas disponíveis: Taurus, Glock, Rossi, Beretta, Smith & Wesson\n" \
               "Exemplo: 'Quantas armas Taurus?' ou 'Compare Taurus e Glock'"


# ===== TESTES =====
if __name__ == "__main__":
    print("\n[TESTES] Executando testes...")
    print("="*60)
    
    testes = [
        # Teste 1: Consulta simples
        "Quantas armas Taurus existem?",
        
        # Teste 2: Comparação (2 marcas)
        "Ha mais Taurus ou Glock?",
        
        # Teste 3: Comparação (3 marcas)
        "Compare Taurus, Glock e Rossi",
        
        # Teste 4: Sem marca
        "Quantas armas?"
    ]
    
    for i, pergunta in enumerate(testes, 1):
        print(f"\n{'='*60}")
        print(f"TESTE {i}/{len(testes)}")
        print("="*60)
        
        resposta = agente_v3_1_comparacao(pergunta)
        
        print(f"\n[RESPOSTA FINAL]")
        print(resposta)
        print()
        
        if i < len(testes):
            input("[Pressione ENTER para próximo teste]")
    
    print("="*60)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("="*60)
```

---

## 🎯 DIFERENÇAS PRINCIPAIS

| Aspecto | Versão Antiga (v3.0) | Versão Nova (v3.1) |
|---------|---------------------|-------------------|
| Detecta marcas | Apenas 1ª encontrada | TODAS as marcas |
| Comparação | ❌ Não suporta | ✅ Suporta |
| "Taurus ou Glock?" | ❌ Só responde Taurus | ✅ Compara ambas |
| Múltiplas marcas | ❌ Não | ✅ Sim (3+) |
| Ranking | ❌ Não | ✅ Ordena por quantidade |

---

## 📊 EXEMPLO DE SAÍDA

### Pergunta: "Há mais Taurus ou Glock?"

**Antes (v3.0):**
```
[DETECÇÃO] Marca: Taurus
[RESULTADO] 17.760 armas Taurus
[PROBLEMA] Não buscou Glock!
```

**Depois (v3.1):**
```
[DETECÇÃO] Marcas: ['Taurus', 'Glock']
[TIPO] COMPARAÇÃO

PASSO 2.1: Consultando Taurus...
         → Taurus: 17,760 armas

PASSO 2.2: Consultando Glock...
         → Glock: 8,543 armas

PASSO 3: Comparando...
         Ranking:
         1º Taurus: 17,760 armas
         2º Glock: 8,543 armas

Conclusão: TAURUS tem 9,217 armas a mais.
```

---

## 🎓 PARA OS ALUNOS

**Explicação pedagógica:**

1. **Problema:** `break` para na primeira marca
2. **Solução:** Remover `break`, usar lista
3. **Detecção:** `marcas_encontradas = []` (lista vazia)
4. **Comparação:** Se `len(marcas_encontradas) >= 2` → comparar
5. **Execução:** Loop para chamar tool N vezes
6. **Ranking:** `sorted()` para ordenar resultados

---

**Arquivo criado:** `CORRECAO_COMPARACAO_MARCAS.md`  
**Código corrigido:** Acima (copie para `agente_v3_1_comparacao.py`)
