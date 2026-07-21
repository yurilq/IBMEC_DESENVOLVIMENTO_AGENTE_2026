# 🔍 EXPLICAÇÃO: *args e **kwargs em Python

**Pergunta:** O que é `**kwargs`? E `*args`?

---

## 🎯 RESPOSTA RÁPIDA

```python
*args   = argumentos POSICIONAIS variáveis (tupla)
**kwargs = argumentos NOMEADOS variáveis (dicionário)
```

**"kwargs"** = **k**eyword **arg**ument**s** (argumentos com palavra-chave)

---

## 📚 ENTENDENDO PASSO A PASSO

### **1. Função Normal (Argumentos Fixos)**

```python
def somar(a, b):
    return a + b

somar(2, 3)  # OK - 2 argumentos
somar(2, 3, 4)  # ERRO! Função espera apenas 2
```

**Problema:** Número de argumentos FIXO!

---

### **2. Com *args (Argumentos Posicionais Variáveis)**

```python
def somar_todos(*args):
    """args = tupla com todos argumentos posicionais"""
    print(f"args = {args}")
    print(f"Tipo: {type(args)}")
    
    total = 0
    for numero in args:
        total += numero
    return total

# Testar
print(somar_todos(1))           # args = (1,)
print(somar_todos(1, 2))        # args = (1, 2)
print(somar_todos(1, 2, 3, 4))  # args = (1, 2, 3, 4)
```

**Resultado:**
```
args = (1,)
1
args = (1, 2)
3
args = (1, 2, 3, 4)
10
```

**O que aconteceu:**
- `*args` captura TODOS os argumentos posicionais
- Vira uma TUPLA
- Você pode ter 1, 2, 10, 100 argumentos!

---

### **3. Com **kwargs (Argumentos Nomeados Variáveis)**

```python
def mostrar_info(**kwargs):
    """kwargs = dicionário com argumentos nomeados"""
    print(f"kwargs = {kwargs}")
    print(f"Tipo: {type(kwargs)}")
    
    for chave, valor in kwargs.items():
        print(f"  {chave} = {valor}")

# Testar
mostrar_info(nome="João")
print()
mostrar_info(nome="Maria", idade=25)
print()
mostrar_info(cidade="Rio", país="Brasil", população=6000000)
```

**Resultado:**
```
kwargs = {'nome': 'João'}
Tipo: <class 'dict'>
  nome = João

kwargs = {'nome': 'Maria', 'idade': 25}
Tipo: <class 'dict'>
  nome = Maria
  idade = 25

kwargs = {'cidade': 'Rio', 'país': 'Brasil', 'população': 6000000}
Tipo: <class 'dict'>
  cidade = Rio
  país = Brasil
  população = 6000000
```

**O que aconteceu:**
- `**kwargs` captura TODOS os argumentos nomeados (chave=valor)
- Vira um DICIONÁRIO
- Chaves = nomes dos parâmetros
- Valores = valores passados

---

## 🔬 ANATOMIA DOS ASTERISCOS

### **Um asterisco (*)**

```python
*args
│ │
│ └─ nome (pode ser qualquer nome, mas "args" é convenção)
└─ captura argumentos posicionais em TUPLA
```

### **Dois asteriscos (**)**

```python
**kwargs
 │ │
 │ └─ nome (pode ser qualquer nome, mas "kwargs" é convenção)
 └─ captura argumentos nomeados em DICIONÁRIO
```

---

## 📖 CONVENÇÃO DE NOMES

### **Por que "args" e "kwargs"?**

**Convenção da comunidade Python:**
- `*args` = **arg**ument**s** (argumentos)
- `**kwargs` = **k**eyword **arg**uments (argumentos com palavra-chave)

**Você PODE usar outros nomes:**

```python
def funcao(*numeros, **opcoes):  # ← Funciona!
    pass

def funcao(*valores, **configs):  # ← Funciona!
    pass
```

**MAS:** Todo mundo usa `args` e `kwargs`! Use também! 🎯

---

## 🎨 USANDO JUNTOS

### **Ordem dos Parâmetros (IMPORTANTE!)**

```python
def funcao_completa(arg_normal, *args, **kwargs):
    """
    1. Argumentos normais (fixos)
    2. *args (posicionais variáveis)
    3. **kwargs (nomeados variáveis)
    """
    print(f"Normal: {arg_normal}")
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

# Usar
funcao_completa(
    "primeiro",           # arg_normal
    "segundo", "terceiro", # args (tupla)
    nome="João",          # kwargs (dict)
    idade=30              # kwargs (dict)
)
```

**Output:**
```
Normal: primeiro
Args: ('segundo', 'terceiro')
Kwargs: {'nome': 'João', 'idade': 30}
```

---

## 💡 CASOS DE USO REAIS

### **1. Decorators (onde você viu!)**

```python
def meu_decorator(funcao):
    def wrapper(*args, **kwargs):  # ← Aceita QUALQUER argumento!
        print("Antes...")
        resultado = funcao(*args, **kwargs)  # ← Passa tudo adiante
        print("Depois...")
        return resultado
    return wrapper

@meu_decorator
def somar(a, b):
    return a + b

@meu_decorator
def saudar(nome, saudacao="Olá"):
    return f"{saudacao}, {nome}!"

# Funciona com AMBAS!
print(somar(2, 3))           # wrapper recebe: args=(2,3), kwargs={}
print(saudar("Maria", saudacao="Oi"))  # wrapper recebe: args=("Maria",), kwargs={"saudacao":"Oi"}
```

**Por quê?**
- Decorator não sabe quantos argumentos a função tem
- `*args, **kwargs` aceita QUALQUER combinação!

---

### **2. Wrapper de Funções**

```python
def criar_pessoa(nome, idade, **dados_extras):
    """
    nome, idade = obrigatórios
    dados_extras = opcionais (quantos quiser!)
    """
    pessoa = {
        "nome": nome,
        "idade": idade
    }
    
    # Adicionar dados extras
    pessoa.update(dados_extras)
    
    return pessoa

# Usar
p1 = criar_pessoa("João", 30)
print(p1)  # {'nome': 'João', 'idade': 30}

p2 = criar_pessoa("Maria", 25, cidade="Rio", profissão="Dev")
print(p2)  # {'nome': 'Maria', 'idade': 25, 'cidade': 'Rio', 'profissão': 'Dev'}
```

---

### **3. Passar Argumentos Adiante**

```python
def log_e_executa(funcao, *args, **kwargs):
    """Loga e depois executa função com argumentos recebidos"""
    print(f"Chamando {funcao.__name__}")
    print(f"  Args: {args}")
    print(f"  Kwargs: {kwargs}")
    
    resultado = funcao(*args, **kwargs)  # ← PASSA ADIANTE!
    
    print(f"  Resultado: {resultado}")
    return resultado

def calcular_area(largura, altura, unidade="m²"):
    return f"{largura * altura} {unidade}"

# Usar
log_e_executa(calcular_area, 5, 10)
log_e_executa(calcular_area, 5, 10, unidade="cm²")
```

**Output:**
```
Chamando calcular_area
  Args: (5, 10)
  Kwargs: {}
  Resultado: 50 m²

Chamando calcular_area
  Args: (5, 10)
  Kwargs: {'unidade': 'cm²'}
  Resultado: 50 cm²
```

---

## 🧪 EXPERIMENTO PRÁTICO

Crie arquivo: `experimento_args_kwargs.py`

```python
# experimento_args_kwargs.py

print("="*60)
print("EXPERIMENTO: *args e **kwargs")
print("="*60)

def funcao_completa(obrigatorio, *args, padrao="valor padrão", **kwargs):
    """Demonstra todos os tipos de argumentos"""
    
    print("\n1. Argumento obrigatório:")
    print(f"   obrigatorio = {obrigatorio}")
    
    print("\n2. *args (tupla):")
    print(f"   args = {args}")
    print(f"   Tipo: {type(args)}")
    if args:
        for i, valor in enumerate(args):
            print(f"   args[{i}] = {valor}")
    
    print("\n3. Argumento com padrão:")
    print(f"   padrao = {padrao}")
    
    print("\n4. **kwargs (dict):")
    print(f"   kwargs = {kwargs}")
    print(f"   Tipo: {type(kwargs)}")
    if kwargs:
        for chave, valor in kwargs.items():
            print(f"   kwargs['{chave}'] = {valor}")

# TESTE 1: Só obrigatório
print("\n" + "─"*60)
print("TESTE 1: Só obrigatório")
print("─"*60)
funcao_completa("primeiro")

# TESTE 2: Obrigatório + args
print("\n" + "─"*60)
print("TESTE 2: Obrigatório + *args")
print("─"*60)
funcao_completa("primeiro", "segundo", "terceiro")

# TESTE 3: Obrigatório + padrao
print("\n" + "─"*60)
print("TESTE 3: Obrigatório + padrão modificado")
print("─"*60)
funcao_completa("primeiro", padrao="novo valor")

# TESTE 4: Obrigatório + args + kwargs
print("\n" + "─"*60)
print("TESTE 4: Obrigatório + *args + **kwargs")
print("─"*60)
funcao_completa(
    "primeiro",
    "segundo", "terceiro",
    nome="João",
    idade=30,
    cidade="Rio"
)

# TESTE 5: TUDO JUNTO!
print("\n" + "─"*60)
print("TESTE 5: TUDO junto!")
print("─"*60)
funcao_completa(
    "obrigatório",
    "arg1", "arg2", "arg3",
    padrao="customizado",
    chave1="valor1",
    chave2="valor2",
    chave3="valor3"
)

print("\n" + "="*60)
print("EXPERIMENTO CONCLUÍDO!")
print("="*60)
```

**Execute:**
```bash
python experimento_args_kwargs.py
```

---

## 📊 TABELA RESUMO

| Sintaxe | Nome | Tipo Resultante | Captura | Exemplo |
|---------|------|-----------------|---------|---------|
| `arg` | Argumento normal | - | 1 valor fixo | `func(10)` |
| `*args` | Args | `tuple` | N valores posicionais | `func(1, 2, 3)` |
| `**kwargs` | Kwargs | `dict` | N valores nomeados | `func(a=1, b=2)` |

---

## ⚠️ ERROS COMUNS

### **Erro 1: Ordem errada**

```python
# ERRADO!
def funcao(**kwargs, *args):  # ❌ SyntaxError
    pass

# CERTO!
def funcao(*args, **kwargs):  # ✅
    pass
```

**Ordem obrigatória:** `*args` ANTES de `**kwargs`

---

### **Erro 2: Esquecer asteriscos ao passar**

```python
def funcao(*args, **kwargs):
    outra_funcao(*args, **kwargs)  # ← PRECISA dos asteriscos!
```

**Por quê?**
- `args` é tupla
- `*args` DESEMPACOTA a tupla
- `kwargs` é dict
- `**kwargs` DESEMPACOTA o dict

```python
numeros = (1, 2, 3)
print(*numeros)  # Imprime: 1 2 3 (desempacotado)
print(numeros)   # Imprime: (1, 2, 3) (tupla inteira)
```

---

### **Erro 3: Confundir nome**

```python
# NÃO é mágico! Pode ser qualquer nome:
def funcao(*valores, **opcoes):  # ✅ Funciona!
    pass

# MAS use args/kwargs por convenção!
def funcao(*args, **kwargs):  # ✅ Melhor!
    pass
```

---

## 🎯 RESUMO FINAL

### **O que é *args?**
```python
*args = captura argumentos POSICIONAIS em TUPLA
Exemplo: func(1, 2, 3) → args = (1, 2, 3)
```

### **O que é **kwargs?**
```python
**kwargs = captura argumentos NOMEADOS em DICIONÁRIO
Exemplo: func(a=1, b=2) → kwargs = {'a': 1, 'b': 2}
```

### **Por que usar?**
1. ✅ Flexibilidade (aceita quantos argumentos quiser)
2. ✅ Decorators (não sabe argumentos da função)
3. ✅ Wrappers (passar argumentos adiante)
4. ✅ APIs extensíveis (adicionar opções depois)

### **Onde você viu?**
```python
def wrapper(*args, **kwargs):  # ← AQUI no decorator!
    resultado = funcao(*args, **kwargs)
    return resultado
```

**Motivo:** Decorator precisa funcionar com QUALQUER função!

---

## 🔗 PARA SABER MAIS

**Documentação oficial Python:**
- https://docs.python.org/3/tutorial/controlflow.html#arbitrary-argument-lists

**PEP 3102 (Keyword-Only Arguments):**
- https://www.python.org/dev/peps/pep-3102/

---

**Arquivo:** EXPLICACAO_ARGS_KWARGS.md  
**Localização:** 04_MATERIAL_APOIO/  
**Para:** Entender `*args` e `**kwargs` completamente  
**Status:** ✅ Explicação completa com exemplos

**Agora você domina args e kwargs! 🎯**
