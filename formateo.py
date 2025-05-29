import random

# Función para contar el número de inversiones en una matriz 3x3
def contar_inversiones(matriz):
    # Convierte la matriz 3x3 en una lista plana
    plano = sum(matriz, [])
    
    # Elimina el valor 0 (representa el espacio vacío en el Puzzle 8)
    plano = [x for x in plano if x != 0]
    
    inversiones = 0
    # Cuenta el número de pares (i, j) tal que i < j y plano[i] > plano[j]
    for i in range(len(plano)):
        for j in range(i + 1, len(plano)):
            if plano[i] > plano[j]:
                inversiones += 1
    return inversiones

# Función para generar un estado inicial aleatorio del Puzzle 8 que sea resoluble
def generar_estado_inicial(meta):
    # Calcula la paridad (par o impar) del número de inversiones del estado meta
    inv_meta = contar_inversiones(meta) % 2

    while True:
        # Genera una permutación aleatoria de los números del 0 al 8
        numeros = list(range(9))
        random.shuffle(numeros)
        
        # Convierte la lista en una matriz 3x3
        matriz = [numeros[i:i+3] for i in range(0, 9, 3)]
        
        # Calcula la paridad del número de inversiones del estado generado
        inv_ini = contar_inversiones(matriz) % 2

        # Si la paridad del estado generado coincide con la del estado meta,
        # entonces el estado generado es resoluble y se retorna
        if inv_ini == inv_meta:
            return matriz

def generar_estado_aleatorio():
    numeros = list(range(9))
    random.shuffle(numeros)
    return [numeros[i:i+3] for i in range(0, 9, 3)]

def es_resoluble(matriz, meta):
    inversiones_matriz = contar_inversiones(matriz) % 2
    inversiones_meta = contar_inversiones(meta) % 2
    return inversiones_matriz == inversiones_meta

