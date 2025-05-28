import heapq

# Dirección de movimientos: (fila, columna)
MOVIMIENTOS = {
    'arriba': (-1, 0),
    'abajo': (1, 0),
    'izquierda': (0, -1),
    'derecha': (0, 1)
}

# Heurística: distancia Manhattan
def heuristica(matriz, objetivo):
    distancia = 0
    for i in range(3):
        for j in range(3):
            valor = matriz[i][j]
            if valor != 0:
                for x in range(3):
                    for y in range(3):
                        if objetivo[x][y] == valor:
                            distancia += abs(i - x) + abs(j - y)
                            break
    return distancia

# Obtener posición del 0 (espacio vacío)
def encontrar_cero(matriz):
    for i in range(3):
        for j in range(3):
            if matriz[i][j] == 0:
                return i, j

# Genera un nuevo estado moviendo el cero
def mover(matriz, direccion):
    x, y = encontrar_cero(matriz)
    dx, dy = MOVIMIENTOS[direccion]
    nx, ny = x + dx, y + dy
    if 0 <= nx < 3 and 0 <= ny < 3:
        nueva = [fila[:] for fila in matriz]
        nueva[x][y], nueva[nx][ny] = nueva[nx][ny], nueva[x][y]
        return nueva
    return None

# Comparar estados (listas de listas)
def iguales(m1, m2):
    return all(m1[i][j] == m2[i][j] for i in range(3) for j in range(3))

# Convertir matriz en tupla hashable
def a_tupla(matriz):
    return tuple(tuple(fila) for fila in matriz)

# Algoritmo A*
def a_star(inicial, meta):
    abiertos = []
    heapq.heappush(abiertos, (heuristica(inicial, meta), 0, inicial, [inicial]))
    visitados = set()
    nodos_expandidos = 0

    while abiertos:
        f, costo, actual, camino = heapq.heappop(abiertos)
        nodos_expandidos += 1

        if iguales(actual, meta):
            return camino, nodos_expandidos

        visitados.add(a_tupla(actual))

        for direccion in MOVIMIENTOS:
            siguiente = mover(actual, direccion)
            if siguiente and a_tupla(siguiente) not in visitados:
                nuevo_camino = camino + [siguiente]
                g = costo + 1
                h = heuristica(siguiente, meta)
                heapq.heappush(abiertos, (g + h, g, siguiente, nuevo_camino))

    return None, nodos_expandidos  # No se encontró solución
