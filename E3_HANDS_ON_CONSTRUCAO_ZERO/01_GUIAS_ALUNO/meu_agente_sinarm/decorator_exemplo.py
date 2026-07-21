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
        print(f"Resultado desta função é : {resultado}")
        
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