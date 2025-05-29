from collections import deque

# Diccionario con los posibles movimientos del espacio vacío (0),
# representados como desplazamientos (fila, columna).
MOVIMIENTOS = {
    'arriba': (-1, 0),
    'abajo': (1, 0),
    'izquierda': (0, -1),
    'derecha': (0, 1)
}

def encontrar_cero(matriz):
    """
    Encuentra la posición del valor 0 (espacio vacío) en una matriz 3x3.
    """
    for i in range(3):
        for j in range(3):
            if matriz[i][j] == 0:
                return i, j

def mover(matriz, direccion):
    """
    Intenta mover el espacio vacío en la dirección especificada.
        matriz (list[list[int]]): Estado actual del puzzle.
        direccion (str): Dirección de movimiento ('arriba', 'abajo', 'izquierda', 'derecha').

    """
    x, y = encontrar_cero(matriz)
    dx, dy = MOVIMIENTOS[direccion]
    nx, ny = x + dx, y + dy

    # Validar que la nueva posición esté dentro del tablero
    if 0 <= nx < 3 and 0 <= ny < 3:
        nueva = [fila[:] for fila in matriz]  # Copia profunda
        nueva[x][y], nueva[nx][ny] = nueva[nx][ny], nueva[x][y]  # Intercambiar valores
        return nueva
    return None

def iguales(m1, m2):
    """
    Compara dos matrices 3x3 para verificar si son iguales.
        m1 (list[list[int]]): Primera matriz.
        m2 (list[list[int]]): Segunda matriz.
    """
    return all(m1[i][j] == m2[i][j] for i in range(3) for j in range(3))

def a_tupla(matriz):
    """
    Convierte una matriz en una tupla de tuplas, para que sea hashable y usable en sets.
    """
    return tuple(tuple(fila) for fila in matriz)

def bfs(inicial, meta):
    """
    Implementa el algoritmo de búsqueda en anchura (BFS) para resolver el Puzzle 8.
    """
    cola = deque()
    cola.append((inicial, [inicial]))  # Cada elemento es (estado_actual, camino_hasta_ahí)
    visitados = set()
    nodos_expandidos = 0

    while cola:
        actual, camino = cola.popleft()
        nodos_expandidos += 1

        if iguales(actual, meta):
            return camino, nodos_expandidos  # Solución encontrada

        visitados.add(a_tupla(actual))

        # Generar movimientos válidos desde el estado actual
        for direccion in MOVIMIENTOS:
            siguiente = mover(actual, direccion)
            if siguiente and a_tupla(siguiente) not in visitados:
                nuevo_camino = camino + [siguiente]
                cola.append((siguiente, nuevo_camino))

    return None, nodos_expandidos  # No se encontró una solución
