# experimento_args_kwargs.py
# Demonstração prática de *args e **kwargs

print("="*60)
print("EXPERIMENTO: *args e **kwargs")
print("="*60)

def funcao_completa(obrigatorio, *args, padrao="valor padrao", **kwargs):
    """Demonstra todos os tipos de argumentos"""
    
    print("\n1. Argumento obrigatorio:")
    print(f"   obrigatorio = {obrigatorio}")
    
    print("\n2. *args (tupla):")
    print(f"   args = {args}")
    print(f"   Tipo: {type(args)}")
    if args:
        for i, valor in enumerate(args):
            print(f"   args[{i}] = {valor}")
    
    print("\n3. Argumento com padrao:")
    print(f"   padrao = {padrao}")
    
    print("\n4. **kwargs (dict):")
    print(f"   kwargs = {kwargs}")
    print(f"   Tipo: {type(kwargs)}")
    if kwargs:
        for chave, valor in kwargs.items():
            print(f"   kwargs['{chave}'] = {valor}")

# TESTE 1: So obrigatorio
print("\n" + "-"*60)
print("TESTE 1: So obrigatorio")
print("-"*60)
funcao_completa("primeiro")

# TESTE 2: Obrigatorio + args
print("\n" + "-"*60)
print("TESTE 2: Obrigatorio + *args")
print("-"*60)
funcao_completa("primeiro", "segundo", "terceiro")

# TESTE 3: Obrigatorio + padrao
print("\n" + "-"*60)
print("TESTE 3: Obrigatorio + padrao modificado")
print("-"*60)
funcao_completa("primeiro", padrao="novo valor")

# TESTE 4: Obrigatorio + args + kwargs
print("\n" + "-"*60)
print("TESTE 4: Obrigatorio + *args + **kwargs")
print("-"*60)
funcao_completa(
    "primeiro",
    "segundo", "terceiro",
    nome="Joao",
    idade=30,
    cidade="Rio"
)

# TESTE 5: TUDO JUNTO!
print("\n" + "-"*60)
print("TESTE 5: TUDO junto!")
print("-"*60)
funcao_completa(
    "obrigatorio",
    "arg1", "arg2", "arg3",
    padrao="customizado",
    chave1="valor1",
    chave2="valor2",
    chave3="valor3"
)

print("\n" + "="*60)
print("EXPERIMENTO CONCLUIDO!")
print("="*60)

print("\n\nRESUMO:")
print("-"*60)
print("*args   = tupla com argumentos posicionais")
print("**kwargs = dict com argumentos nomeados (chave=valor)")
print("\nUso comum: decorators que funcionam com qualquer funcao!")
print("-"*60)
