# 🎨 PARTE 3: ENTENDENDO @DECORATOR

**Horário:** 15:15-16:00 (45 minutos)  
**Objetivo:** Entender decorators profundamente  
**Nível:** Intermediário → Avançado  
**⭐ PARTE MAIS IMPORTANTE DA AULA**

---

## ⚠️ IMPORTANTE: O QUE FAZER NESTA PARTE

### **📂 ARQUIVOS - Atenção!**

**NÃO MODIFIQUE os arquivos da PARTE 2:**
- ❌ `tools_basicas.py` (deixe como está)
- ❌ `agente_v0_1.py` (deixe como está)

**CRIE ARQUIVOS NOVOS para aprender:**
- ✅ `exemplo_funcao.py` (criar agora)
- ✅ `decorator_exemplo.py` (criar agora)
- ✅ `exemplo_tool_decorator.py` (já existe - apenas executar)

### **🎯 Objetivo desta Parte**

**FOCO 100% EM:**
- ✅ Entender O QUE é um decorator Python
- ✅ Entender COMO decorators funcionam
- ✅ Ver exemplo de @tool em ação
- ✅ **PREPARAR-SE** para PARTE 4

**NÃO é para:**
- ❌ Modificar código da PARTE 2
- ❌ Criar agente completo agora
- ❌ Mexer em `tools_basicas.py` ainda

### **📅 Quando Modificar os Arquivos?**

**Na PARTE 4 (próxima - 16:00):**
- Aí sim vamos modificar `tools_basicas.py`
- Aí sim vamos adicionar @tool nas funções
- Aí sim vamos criar agente com 4 tools

**Agora (PARTE 3):** Foco é **APRENDER** o conceito! 🧠

---

## 🎯 O QUE VOCÊ VAI APRENDER

1. ✅ O que é uma função Python normal
2. ✅ Problema: código repetido
3. ✅ Solução: Decorator
4. ✅ Como decorator funciona (anatomia)
5. ✅ Ver @tool em ação (exemplo prático)
6. ✅ Entender vantagens do @tool

**Tempo estimado:** 45 minutos (siga o ritmo do professor)

---

## 📋 PASSO A PASSO

### 📌 CHECKPOINT INICIAL

**Antes de começar, confirme:**
- [ ] Arquivos da PARTE 2 estão funcionando
- [ ] Você está em uma pasta/diretório de trabalho
- [ ] Vai criar ARQUIVOS NOVOS (não modificar os antigos)

**Pronto? Vamos começar! 🚀**

---

### PASSO 1: Função Normal (5 min)

**🆕 CRIAR ARQUIVO NOVO:** `exemplo_funcao.py`

```python
# exemplo_funcao.py
# Arquivo NOVO - aprendendo funções Python básicas

def somar(a, b):
    """Soma dois números"""
    return a + b

def multiplicar(a, b):
    """Multiplica dois números"""
    return a * b

# Testar
print("2 + 3 =", somar(2, 3))
print("2 x 3 =", multiplicar(2, 3))
```

**Execute:** `python exemplo_funcao.py`

**Saída esperada:**
```
2 + 3 = 5
2 x 3 = 6
```

**✅ Checkpoint:** Funciona? Ótimo! Próximo passo →

---

### PASSO 2: Problema - Código Repetido (10 min)

**Cenário:** Agora quero adicionar LOG em TODAS as funções.

**❌ Solução ruim - Repetir código:**

```python
# exemplo_funcao.py (VERSÃO 2 - COM LOG - NÃO CRIAR AINDA!)
# Apenas OBSERVE o problema:

def somar(a, b):
    """Soma dois números"""
    print(f"Chamando somar({a}, {b})...")  # ← REPETIR
    resultado = a + b
    print(f"Resultado: {resultado}")        # ← REPETIR
    return resultado

def multiplicar(a, b):
    """Multiplica dois números"""
    print(f"Chamando multiplicar({a}, {b})...")  # ← REPETIR
    resultado = a * b
    print(f"Resultado: {resultado}")              # ← REPETIR
    return resultado

def dividir(a, b):
    """Divide dois números"""
    print(f"Chamando dividir({a}, {b})...")  # ← REPETIR
    resultado = a / b
    print(f"Resultado: {resultado}")          # ← REPETIR
    return resultado

# Testar
somar(2, 3)
multiplicar(2, 3)
dividir(6, 2)
```

**😫 PROBLEMA IDENTIFICADO:**
- Repetimos 2 linhas de log em CADA função!
- Se tivermos 50 funções → 100 linhas repetidas!
- Se quiser mudar o formato do log → mudar em 50 lugares!

**💡 Pergunta:** Como resolver isso? **Decorator!**

---

### PASSO 3: Solução - Decorator (15 min)

**🆕 CRIAR ARQUIVO NOVO:** `decorator_exemplo.py`

```python
# decorator_exemplo.py
# Arquivo NOVO - aprendendo decorators

# PASSO 1: Criar DECORATOR
def mostrar_log(funcao):
    """Decorator que adiciona log automaticamente"""
    
    def funcao_embrulhada(a, b):
        # ANTES: Log antes de chamar função
        print(f"Chamando {funcao.__name__}({a}, {b})...")
        
        # CHAMAR função original
        resultado = funcao(a, b)
        
        # DEPOIS: Log após chamar função
        print(f"Resultado: {resultado}")
        
        return resultado
    
    return funcao_embrulhada

# PASSO 2: Usar decorator com @
@mostrar_log
def somar(a, b):
    return a + b

@mostrar_log
def multiplicar(a, b):
    return a * b

@mostrar_log
def dividir(a, b):
    return a / b

# PASSO 3: Testar
print("="*40)
somar(2, 3)
print("="*40)
multiplicar(4, 5)
print("="*40)
dividir(10, 2)
print("="*40)
```

**Execute:** `python decorator_exemplo.py`

**Saída:**
```
========================================
Chamando somar(2, 3)...
Resultado: 5
========================================
Chamando multiplicar(4, 5)...
Resultado: 20
========================================
Chamando dividir(10, 2)...
Resultado: 5.0
========================================
```

**MAGIA!** ✨ Log adicionado automaticamente!

---

## 🧠 ENTENDENDO DECORATORS

### Analogia: Papel de Presente

```
DECORATOR = PAPEL DE PRESENTE

┌─────────────────────────────┐
│    PAPEL DE PRESENTE        │  ← Decorator (adiciona funcionalidade)
│  ┌───────────────────────┐  │
│  │   PRESENTE            │  │  ← Função original
│  │   (função somar)      │  │
│  └───────────────────────┘  │
└─────────────────────────────┘

Decorator "embrulha" função SEM mudar o presente dentro!
```

---

### O Que Acontece com @

```python
@mostrar_log
def somar(a, b):
    return a + b

# É EXATAMENTE o mesmo que:

def somar(a, b):
    return a + b

somar = mostrar_log(somar)
```

**@ é atalho!** Mais legível e pythônico.

---

### Anatomia do Decorator

```python
def meu_decorator(funcao_original):     # 1. Recebe função
    
    def wrapper(*args, **kwargs):       # 2. Define wrapper
        # ANTES
        print("Antes...")
        
        # EXECUTAR ORIGINAL
        resultado = funcao_original(*args, **kwargs)
        
        # DEPOIS
        print("Depois...")
        
        return resultado
    
    return wrapper                      # 3. Retorna wrapper
```

**3 Partes:**
1. Recebe função original
2. Cria wrapper (embrulho)
3. Retorna wrapper

---

## ✅ CHECKPOINT 3A

- [ ] Entendeu que decorator "embrulha" função
- [ ] Viu que @ é atalho
- [ ] Decorator NÃO muda função original
- [ ] Decorator adiciona funcionalidade ANTES/DEPOIS

**Teste seu entendimento:** Explique para o colega ao lado!

---

### PASSO 4: Ver @tool em Ação (10 min)

**⚠️ ATENÇÃO: Apenas OBSERVAR! Não modificar arquivos ainda!**

Agora que você entende decorators, vamos ver um decorator **real** do LangChain: `@tool`

---

#### **4.1. Executar Exemplo Prático**

**📁 EXECUTE (arquivo já existe):**

```bash
python exemplo_tool_decorator.py
```

**O que você verá:**

```
1. INSPEÇÃO: O que @tool criou?
   Nome da tool: contar_armas_marca
   Description: Conta quantas armas...
   Tipo: <class 'StructuredTool'>

2. TESTE: Invocar a tool
   Resultado: Encontrei X armas da marca Taurus

3. COMPARAÇÃO: Tool vs Função Normal
   Função normal tem .name? False
   Tool tem .name? True
   ...
```

**💡 Conclusão:** @tool TRANSFORMA função Python em StructuredTool!

---

#### **4.2. Entender o Conceito Visualmente**

**Como @tool funciona (conceito):**

```python
# Você escreve:
@tool
def minha_funcao(parametro: str) -> str:
    """Descrição do que faz"""
    return f"Resultado: {parametro}"

# @tool faz automaticamente:
# 1. Lê nome da função → "minha_funcao"
# 2. Lê docstring → "Descrição do que faz"  
# 3. Lê type hints → parametro: str, return: str
# 4. Cria StructuredTool com tudo isso!
```

**Resultado:** Função vira Tool automaticamente!

---

#### **4.3. Comparação Simples**

| Sem Decorator | Com @tool |
|---------------|-----------|
| Função Python normal | StructuredTool |
| Tem: `__name__`, `__doc__` | Tem: `.name`, `.description`, `.invoke` |
| Não é tool | É tool pronta para usar! |

---

#### **4.4. Por Que Isso É Útil?**

**SEM @tool (manual):**
```python
def contar_armas(marca):
    """Conta armas"""
    return resultado

# Criar tool manualmente
tool = Tool(name="contar_armas", func=contar_armas, description="Conta armas")
```

**COM @tool (automático):**
```python
@tool
def contar_armas(marca: str) -> str:
    """Conta armas"""  # ← description automática!
    return resultado

# Já é tool! Não precisa criar Tool()
```

**Vantagem:** Menos código, menos repetição! ✅

---

---

## ✅ CHECKPOINT 3B

**Você deve ter entendido:**
- [ ] O que é um decorator Python
- [ ] Como decorator "embrulha" uma função
- [ ] Que @tool é um decorator do LangChain
- [ ] Que @tool transforma função em StructuredTool
- [ ] Vantagem: menos código, automático

**Você NÃO precisa:**
- ❌ Ter modificado `tools_basicas.py`
- ❌ Ter criado agente completo
- ❌ Dominar toda API do LangChain

**Foco desta parte:** Conceito de decorator! 🎯

**Teste:** Consegue explicar o que é decorator para um colega? 

---

## 📊 RESUMO VISUAL: Decorator em Ação

### **O Poder do Decorator**

```
FUNÇÃO NORMAL (Python básico)
↓
def somar(a, b):
    return a + b
↓
Tem: __name__, __doc__, __call__
Não tem: log, validação, transformação


FUNÇÃO COM DECORATOR
↓
@mostrar_log
def somar(a, b):
    return a + b
↓
Tem: __name__, __doc__, __call__
MAIS: log automático antes/depois!


FUNÇÃO COM @tool
↓
@tool
def contar_armas(marca: str) -> str:
    """Conta armas"""
    return resultado
↓
Virou: StructuredTool
Tem: .name, .description, .invoke
Pronta para usar em agente!
```

---

### **Comparação: Manual vs Decorator**

| Aspecto | Sem Decorator | Com Decorator |
|---------|---------------|---------------|
| **Código** | Repetitivo | DRY (Don't Repeat Yourself) |
| **Manutenção** | Difícil (mudar em N lugares) | Fácil (mudar 1 lugar) |
| **Legibilidade** | Poluído | Limpo |
| **Erros** | Fácil esquecer algo | Impossível (automático) |
| **Exemplo** | 15 linhas | 8 linhas |

**Conclusão:** Decorator é SEMPRE melhor! ✅

---

## 🎓 EXERCÍCIO OPCIONAL

**Desafio:** Crie um decorator `medir_tempo` que mostra quanto tempo uma função levou:

```python
# exercicio_decorator.py
import time

def medir_tempo(funcao):
    """Decorator que mede tempo de execução"""
    
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcao(*args, **kwargs)
        fim = time.time()
        tempo = fim - inicio
        print(f"Funcao {funcao.__name__} levou {tempo:.2f}s")
        return resultado
    
    return wrapper

# Testar
@medir_tempo
def processar_dados():
    time.sleep(1)  # Simula processamento
    return "Concluído"

resultado = processar_dados()
print(resultado)
```

**Execute:**
```bash
python exercicio_decorator.py
```

**Output esperado:**
```
Funcao processar_dados levou 1.00s
Concluído
```

**💡 Nota:** Pode usar MÚLTIPLOS decorators empilhados!

```python
@medir_tempo
@mostrar_log
def minha_funcao():
    pass
```

---

## 📚 CONCEITOS APRENDIDOS

✅ **Decorator**: Função que modifica outra função  
✅ **@**: Sintaxe para aplicar decorator  
✅ **Wrapper**: Função embrulho que chama original  
✅ **@tool**: Decorator LangChain que cria Tool automaticamente  
✅ **DRY**: Don't Repeat Yourself (decorators evitam repetição)

---

## 🎯 RESUMO: O QUE VOCÊ FEZ NESTA PARTE

### **Arquivos CRIADOS:**
- ✅ `exemplo_funcao.py` - funções Python básicas
- ✅ `decorator_exemplo.py` - criou decorator customizado
- ✅ Executou `exemplo_tool_decorator.py` - viu @tool em ação

### **Arquivos NÃO MODIFICADOS:**
- ⏸️ `tools_basicas.py` - **deixou como estava**
- ⏸️ `agente_v0_1.py` - **deixou como estava**

### **O que você APRENDEU:**
- ✅ Conceito de decorator
- ✅ Como decorator funciona (wrapper pattern)
- ✅ Como @tool simplifica código
- ✅ Vantagens do decorator (DRY, menos repetição)

### **O que você VAI FAZER na PARTE 4:**
- ⏭️ **Modificar** `tools_basicas.py` (adicionar @tool)
- ⏭️ **Adicionar** 3 novas tools com @tool
- ⏭️ **Criar** `agente_v1_0.py` com 4 tools
- ⏭️ **Usar** @lru_cache (outro decorator)

---

## 🚀 PRÓXIMOS PASSOS

### **Preparado para PARTE 4?**

**Checklist:**
- [ ] Entendi o que é decorator
- [ ] Vi @tool em ação
- [ ] Sei que vou modificar `tools_basicas.py` na PARTE 4
- [ ] Estou pronto para adicionar mais 3 tools

**✅ Tudo certo?** Vamos para PARTE 4!

**📄 Arquivo:** [PARTE_4_QUATRO_TOOLS.md](PARTE_4_QUATRO_TOOLS.md)

---

## ⚠️ LEMBRE-SE

### **PARTE 3 (você está aqui):**
```
Foco: APRENDER decorator
Arquivos: NOVOS (exemplo_*.py)
Modificações: NENHUMA em tools_basicas.py
```

### **PARTE 4 (próxima):**
```
Foco: APLICAR @tool
Arquivos: MODIFICAR tools_basicas.py
Adicionar: 3 novas tools com @tool
```

**Progressão pedagógica:** Aprender → Aplicar ✅

---

**Parte:** 3/5  
**Tempo:** 45 minutos  
**Status:** ✅ PRONTO PARA USO  
**⭐ Parte mais importante! Revise se necessário!**
