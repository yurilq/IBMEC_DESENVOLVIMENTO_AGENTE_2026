# 🎯 COMO FAZER AS PERGUNTAS - ATIVIDADE 1A

## 📋 VOCÊ TEM 3 OPÇÕES

---

## ✅ **OPÇÃO 1: SCRIPT AUTOMÁTICO (MAIS FÁCIL)**

### Passo a Passo:

```bash
# 1. Navegue para a pasta
cd conceitos/01_fewshot

# 2. Execute o script de teste automático
python TESTE_AUTOMATICO_1A.py
```

### O que acontece:

```
╔═══════════════════════════════════════════════════════════════╗
║  TESTE AUTOMÁTICO - ATIVIDADE 1A                             ║
╚═══════════════════════════════════════════════════════════════╝

🔧 Inicializando agente v1.8...
✅ Agente v1.8 carregado!

================================================================================
QUERY 1/5
================================================================================

📝 Pergunta: Quantas ocorrências de furto de armas Taurus aconteceram no DF?

[Agente executa automaticamente]

🤖 Resposta do Agente:
--------------------------------------------------------------------------------
Consultei SINARM/OCORRENCIAS com filtros marca=Taurus, tipo=Furto, uf=DF.
Resultado: 487 ocorrências de furto de armas Taurus no DF.
--------------------------------------------------------------------------------

⏱️  Tempo: 2.8s

📊 AVALIAÇÃO (preencha manualmente):
   Dataset correto? (S/N): S
   Campos corretos? (S/N): S
   Qualidade (1-5): 5

Pressione ENTER para próxima query...
```

### ✅ Vantagens:
- ✅ **Automático** - Roda todas as 5 queries
- ✅ **Rápido** - Não precisa copiar/colar
- ✅ **Relatório final** - Gera tabela e métricas automaticamente

### ⚠️ Único requisito:
- Ter agente v1.8 na pasta: `E1_ANATOMIA_DO_AGENTE/solucao_final/E1_agente_react_v3.py`

---

## ✅ **OPÇÃO 2: AGENTE INTERATIVO (MODO MANUAL)**

### Passo a Passo:

#### 1. Abra DOIS terminais lado a lado

**Terminal 1 (Esquerda):**
```bash
cd conceitos/01_fewshot
python ATIVIDADE_1A_baseline.py
```

Resultado:
```
================================================================================
QUERIES DE TESTE
================================================================================

1. Quantas ocorrências de furto de armas Taurus aconteceram no DF?
   📊 Dataset: ocorrencias
   🔍 Campos: marca:Taurus, tipo:Furto, uf:DF
```

#### 2. No Terminal 2 (Direita), rode o agente:

**Se o agente v1.8 for interativo:**
```bash
cd E1_ANATOMIA_DO_AGENTE/solucao_final
python E1_agente_react_v3.py
```

Deve aparecer:
```
🔍 Agente ReAct SINARM v1.8
Digite sua pergunta:
>>> _
```

#### 3. Copie a Query 1 do Terminal 1

```
Quantas ocorrências de furto de armas Taurus aconteceram no DF?
```

#### 4. Cole no Terminal 2 e pressione ENTER

```
>>> Quantas ocorrências de furto de armas Taurus aconteceram no DF?

[Agente processa]

🤖 Resposta:
Consultei SINARM/OCORRENCIAS...
Resultado: 487 ocorrências.
```

#### 5. Cronometre o tempo e avalie

```
⏱️  Tempo: 2.8s (cronometre manualmente)

Avalie:
- Dataset OK? → Sim, usou buscar_ocorrencias ✅
- Campos OK? → Sim, filtrou marca, tipo, uf ✅
- Qualidade? → 5/5 (precisa e completa) ✅
```

#### 6. Volte ao Terminal 1 e preencha a tabela

```
1    Quantas ocorrências...    [X]    [X]    [5/5]    [2.8]
```

#### 7. Repita para as 5 queries

---

## ✅ **OPÇÃO 3: IMPORTAR E CHAMAR PROGRAMATICAMENTE**

### Se você quer testar em Python diretamente:

```python
# No terminal Python ou Jupyter
import sys
sys.path.append("../E1_ANATOMIA_DO_AGENTE/solucao_final")

from E1_agente_react_v3 import AgenteInvestigador

# Inicializar agente
agente = AgenteInvestigador(verbose=True)

# Fazer pergunta
resposta = agente.executar("Quantas ocorrências de furto de armas Taurus aconteceram no DF?")

print(resposta)
```

---

## 🚨 **TROUBLESHOOTING**

### ❌ "Não encontrei o agente v1.8"

**Solução A:** Procure o arquivo
```bash
# Encontre onde está o agente v1.8
dir /s E1_agente_react_v3.py
```

**Solução B:** Copie temporariamente para E2
```bash
cd E2_QUALIDADE_E_MEMORIA
copy ..\E1_ANATOMIA_DO_AGENTE\solucao_final\E1_agente_react_v3.py .\agente_v1.8.py
```

**Solução C:** Use solução final (temporário)
```bash
# Se não tiver v1.8, use da solução final
python ../../solucao_final/agente_v2.0_fewshot.py
# (Mas anote que usou v2.0, não v1.8!)
```

---

### ❌ "O agente não é interativo"

Se o agente v1.8 não aceita perguntas interativas, use:

```bash
# Execute o script de teste automático
python TESTE_AUTOMATICO_1A.py
```

Este script **importa o agente** e **chama o método executar()** para cada query.

---

### ❌ "ModuleNotFoundError: No module named 'langchain'"

```bash
# Instale dependências
pip install langchain langchain-ollama
```

---

### ❌ "Ollama não está rodando"

```bash
# Inicie o Ollama
ollama serve

# Em outro terminal, teste
ollama run llama3.2
```

---

## 📊 **RESULTADO ESPERADO**

Ao final, você deve ter:

```
================================================================================
TABELA DE RESULTADOS - BASELINE ZERO-SHOT (v1.8)
================================================================================
ID   Query                                              Dataset OK   Campos OK    Qualidade    Tempo (s) 
--------------------------------------------------------------------------------
1    Quantas ocorrências de furto de armas Taurus ac    [X]          [X]          [5  /5]      [2.8]    
2    Quais marcas de arma têm mais portes válidos at    [X]          [ ]          [3  /5]      [3.1]    
3    Quantos registros de pistola calibre 9mm existe    [X]          [X]          [5  /5]      [2.3]    
4    Qual a taxa de aprovação de requerimentos de po    [ ]          [ ]          [2  /5]      [4.2]    
5    Quais municípios do DF tiveram mais recuperaçõe    [X]          [ ]          [3  /5]      [3.5]    
--------------------------------------------------------------------------------

MÉTRICAS CALCULADAS:
  Accuracy:    60% (3/5 queries corretas)
  Tempo médio: 3.18s
  Taxa erro:   40% (2/5 queries erraram)
```

**Anote esses resultados! Você vai comparar com v2.0 na ATIVIDADE 1D.**

---

## 🎯 **RECOMENDAÇÃO**

Para a **aula prática**, use:

👍 **OPÇÃO 1 (Script Automático)** - Mais rápido, sem erros de digitação

Se quiser aprender o processo manual:

👍 **OPÇÃO 2 (Modo Interativo)** - Mais pedagógico, você vê cada passo

---

## ❓ **AINDA COM DÚVIDAS?**

Pergunte ao professor ou monitor:
- "O agente v1.8 deve estar onde?"
- "Como sei se o dataset está correto?"
- "O que significa 'campos corretos'?"

**BOA PRÁTICA! 🚀**
