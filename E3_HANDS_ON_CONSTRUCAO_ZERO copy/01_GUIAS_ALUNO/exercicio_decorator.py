# exercicio_decorator.py
# Exercício: Decorator que mede tempo de execução

import time

print("="*60)
print("EXERCÍCIO: DECORATOR MEDIR_TEMPO")
print("="*60)

# 1. CRIAR O DECORATOR
def medir_tempo(funcao):
    """Decorator que mede quanto tempo uma função leva para executar"""
    
    def wrapper(*args, **kwargs):
        # Marcar tempo ANTES
        inicio = time.time()
        
        # Executar função original
        resultado = funcao(*args, **kwargs)
        
        # Marcar tempo DEPOIS
        fim = time.time()
        
        # Calcular diferença
        tempo_decorrido = fim - inicio
        
        # Mostrar resultado
        print(f"[TEMPO] {funcao.__name__} levou {tempo_decorrido:.4f} segundos")
        
        return resultado
    
    return wrapper


# 2. TESTAR COM FUNÇÕES SIMPLES

print("\n" + "-"*60)
print("TESTE 1: Função rápida (sem delay)")
print("-"*60)

@medir_tempo
def funcao_rapida():
    """Função que executa instantaneamente"""
    return 2 + 2

resultado = funcao_rapida()
print(f"Resultado: {resultado}")


print("\n" + "-"*60)
print("TESTE 2: Função com delay de 0.5s")
print("-"*60)

@medir_tempo
def funcao_lenta():
    """Função que demora 0.5 segundos"""
    time.sleep(0.5)
    return "Concluído"

resultado = funcao_lenta()
print(f"Resultado: {resultado}")


print("\n" + "-"*60)
print("TESTE 3: Função com argumentos")
print("-"*60)

@medir_tempo
def processar_dados(quantidade, delay=0.1):
    """Processa dados com delay configurável"""
    for i in range(quantidade):
        time.sleep(delay)
    return f"Processados {quantidade} itens"

resultado = processar_dados(3, delay=0.2)
print(f"Resultado: {resultado}")


print("\n" + "-"*60)
print("TESTE 4: Função que faz cálculo pesado")
print("-"*60)

@medir_tempo
def calcular_soma_grande(n):
    """Calcula soma de 1 até n"""
    total = 0
    for i in range(n):
        total += i
    return total

resultado = calcular_soma_grande(1000000)
print(f"Resultado: {resultado}")


# 3. MÚLTIPLOS DECORATORS EMPILHADOS

print("\n" + "-"*60)
print("TESTE 5: MÚLTIPLOS DECORATORS (empilhados)")
print("-"*60)

def mostrar_log(funcao):
    """Decorator que mostra log de execução"""
    def wrapper(*args, **kwargs):
        print(f"[LOG] Chamando {funcao.__name__}...")
        resultado = funcao(*args, **kwargs)
        print(f"[LOG] {funcao.__name__} retornou: {resultado}")
        return resultado
    return wrapper

@medir_tempo        # ← Aplicado por último (mais externo)
@mostrar_log        # ← Aplicado primeiro (mais interno)
def funcao_com_dois_decorators(x, y):
    """Função com dois decorators empilhados"""
    time.sleep(0.3)
    return x + y

resultado = funcao_com_dois_decorators(5, 10)
print(f"Resultado final: {resultado}")


# 4. APLICAÇÃO PRÁTICA: MEDIR PERFORMANCE

print("\n" + "="*60)
print("APLICAÇÃO PRÁTICA: COMPARAR PERFORMANCE")
print("="*60)

@medir_tempo
def buscar_linear(lista, alvo):
    """Busca linear (O(n))"""
    for item in lista:
        if item == alvo:
            return True
    return False

@medir_tempo
def buscar_set(conjunto, alvo):
    """Busca em set (O(1))"""
    return alvo in conjunto

# Criar dados de teste
numeros_lista = list(range(100000))
numeros_set = set(range(100000))
alvo = 99999  # Último elemento

print("\nBuscar 99999 em lista de 100.000 elementos:")
resultado1 = buscar_linear(numeros_lista, alvo)
print(f"Encontrado: {resultado1}")

print("\nBuscar 99999 em set de 100.000 elementos:")
resultado2 = buscar_set(numeros_set, alvo)
print(f"Encontrado: {resultado2}")

print("\nCONCLUSÃO: Set é MUITO mais rápido!")


# 5. VERSÃO MELHORADA: COM FORMATAÇÃO

print("\n" + "="*60)
print("VERSÃO MELHORADA: FORMATAÇÃO BONITA")
print("="*60)

def medir_tempo_v2(funcao):
    """Versão melhorada com formatação"""
    
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = funcao(*args, **kwargs)
        fim = time.time()
        
        tempo = fim - inicio
        
        # Formatação inteligente
        if tempo < 0.001:
            tempo_str = f"{tempo*1000000:.2f} microsegundos"
        elif tempo < 1:
            tempo_str = f"{tempo*1000:.2f} milissegundos"
        else:
            tempo_str = f"{tempo:.2f} segundos"
        
        print(f"[TEMPO] {funcao.__name__}: {tempo_str}")
        
        return resultado
    
    return wrapper

@medir_tempo_v2
def operacao_rapida():
    return sum(range(100))

@medir_tempo_v2
def operacao_media():
    time.sleep(0.05)
    return "ok"

@medir_tempo_v2
def operacao_lenta():
    time.sleep(1.5)
    return "ok"

print("\nTeste com formatação automática:")
operacao_rapida()
operacao_media()
operacao_lenta()


# RESUMO FINAL

print("\n" + "="*60)
print("RESUMO DO EXERCICIO")
print("="*60)

print("""
VOCE APRENDEU:

1. Criar decorator customizado (medir_tempo)
2. Usar *args e **kwargs para aceitar qualquer funcao
3. Empilhar multiplos decorators (@medir_tempo + @mostrar_log)
4. Aplicacao pratica: medir performance de codigo
5. Melhorar decorator com formatacao inteligente

SINTAXE:

@medir_tempo
def minha_funcao():
    pass

E EQUIVALENTE A:

def minha_funcao():
    pass
minha_funcao = medir_tempo(minha_funcao)

ORDEM DOS DECORATORS (empilhados):

@decorator_externo    <- Aplicado por ultimo
@decorator_interno    <- Aplicado primeiro
def funcao():
    pass

USO REAL:
- Performance profiling
- Debug e logging
- Caching de resultados
- Validacao de entrada
- Rate limiting
- Authentication

PARABENS! Voce domina decorators!
""")

print("="*60)
print("EXERCICIO CONCLUIDO!")
print("="*60)
