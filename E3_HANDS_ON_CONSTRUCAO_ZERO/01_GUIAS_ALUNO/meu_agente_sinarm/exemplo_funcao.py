
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