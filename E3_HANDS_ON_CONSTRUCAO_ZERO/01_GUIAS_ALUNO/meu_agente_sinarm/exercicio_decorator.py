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
    time.sleep(2)  # Simula processamento
    return "Concluído"

resultado = processar_dados()
print(resultado)