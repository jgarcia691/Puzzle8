import random

def contar_inversiones(matriz):
    plano = sum(matriz, [])
    plano = [x for x in plano if x != 0]
    inversiones = 0
    for i in range(len(plano)):
        for j in range(i + 1, len(plano)):
            if plano[i] > plano[j]:
                inversiones += 1
    return inversiones


# Genera un estado inicial aleatorio que sea resoluble
def generar_estado_inicial(meta):
    # Obtener paridad del estado meta
    inv_meta = contar_inversiones(meta) % 2

    while True:
        numeros = list(range(9))
        random.shuffle(numeros)
        matriz = [numeros[i:i+3] for i in range(0, 9, 3)]
        inv_ini = contar_inversiones(matriz) % 2

        if inv_ini == inv_meta:
            return matriz
