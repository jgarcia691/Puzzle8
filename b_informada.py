import heapq

# Diccionario con las direcciones posibles del movimiento del espacio vacío (0)
# Cada dirección representa un cambio de fila y columna
MOVIMIENTOS = {
    'arriba': (-1, 0),
    'abajo': (1, 0),
    'izquierda': (0, -1),
    'derecha': (0, 1)
}

# Función de heurística: calcula la distancia de Manhattan entre cada pieza
# y su posición objetivo en la matriz meta
def heuristica(matriz, objetivo):
    distancia = 0
    for i in range(3):
        for j in range(3):
            valor = matriz[i][j]
            if valor != 0:
                # Buscar la posición del valor actual en la matriz objetivo
                for x in range(3):
                    for y in range(3):
                        if objetivo[x][y] == valor:
                            # Sumar la distancia Manhattan entre la posición actual y la deseada
                            distancia += abs(i - x) + abs(j - y)
                            break
    return distancia

# Encuentra la posición del número 0 (espacio vacío) en la matriz
def encontrar_cero(matriz):
    for i in range(3):
        for j in range(3):
            if matriz[i][j] == 0:
                return i, j

# Intenta mover el espacio vacío en la dirección especificada
# Si el movimiento es válido, retorna la nueva matriz resultante
def mover(matriz, direccion):
    x, y = encontrar_cero(matriz)
    dx, dy = MOVIMIENTOS[direccion]
    nx, ny = x + dx, y + dy
    if 0 <= nx < 3 and 0 <= ny < 3:
        # Crear una copia de la matriz para no modificar la original
        nueva = [fila[:] for fila in matriz]
        # Intercambiar el valor del cero con la celda de destino
        nueva[x][y], nueva[nx][ny] = nueva[nx][ny], nueva[x][y]
        return nueva
    return None  # Movimiento inválido

# Compara si dos matrices son iguales (misma configuración de piezas)
def iguales(m1, m2):
    return all(m1[i][j] == m2[i][j] for i in range(3) for j in range(3))

# Convierte una matriz en una tupla de tuplas para que pueda almacenarse en un set
def a_tupla(matriz):
    return tuple(tuple(fila) for fila in matriz)

# Implementación del algoritmo A* para resolver el Puzzle 8
def a_star(inicial, meta):
    abiertos = []  # Cola de prioridad (heap) con nodos por explorar
    # Cada elemento en la cola: (f, g, estado_actual, camino_recorrido)
    heapq.heappush(abiertos, (heuristica(inicial, meta), 0, inicial, [inicial]))
    
    visitados = set()  # Conjunto de estados ya visitados
    nodos_expandidos = 0  # Contador de nodos expandidos (estadística)

    while abiertos:
        f, costo, actual, camino = heapq.heappop(abiertos)
        nodos_expandidos += 1

        if iguales(actual, meta):
            return camino, nodos_expandidos  # Se encontró la solución

        visitados.add(a_tupla(actual))

        # Intentar todos los movimientos posibles desde el estado actual
        for direccion in MOVIMIENTOS:
            siguiente = mover(actual, direccion)
            if siguiente and a_tupla(siguiente) not in visitados:
                nuevo_camino = camino + [siguiente]
                g = costo + 1  # Costo acumulado del camino
                h = heuristica(siguiente, meta)  # Estimación restante
                heapq.heappush(abiertos, (g + h, g, siguiente, nuevo_camino))

    return None, nodos_expandidos  # No se encontró solución
