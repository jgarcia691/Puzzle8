from collections import deque

MOVIMIENTOS = {
    'arriba': (-1, 0),
    'abajo': (1, 0),
    'izquierda': (0, -1),
    'derecha': (0, 1)
}

def encontrar_cero(matriz):
    for i in range(3):
        for j in range(3):
            if matriz[i][j] == 0:
                return i, j

def mover(matriz, direccion):
    x, y = encontrar_cero(matriz)
    dx, dy = MOVIMIENTOS[direccion]
    nx, ny = x + dx, y + dy
    if 0 <= nx < 3 and 0 <= ny < 3:
        nueva = [fila[:] for fila in matriz]
        nueva[x][y], nueva[nx][ny] = nueva[nx][ny], nueva[x][y]
        return nueva
    return None

def iguales(m1, m2):
    return all(m1[i][j] == m2[i][j] for i in range(3) for j in range(3))

def a_tupla(matriz):
    return tuple(tuple(fila) for fila in matriz)

def bfs(inicial, meta):
    cola = deque()
    cola.append((inicial, [inicial]))
    visitados = set()
    nodos_expandidos = 0

    while cola:
        actual, camino = cola.popleft()
        nodos_expandidos += 1

        if iguales(actual, meta):
            return camino, nodos_expandidos

        visitados.add(a_tupla(actual))

        for direccion in MOVIMIENTOS:
            siguiente = mover(actual, direccion)
            if siguiente and a_tupla(siguiente) not in visitados:
                nuevo_camino = camino + [siguiente]
                cola.append((siguiente, nuevo_camino))

    return None, nodos_expandidos
