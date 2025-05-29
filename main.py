import pygame
import sys
from b_informada import a_star         # Importa el algoritmo A* desde el módulo correspondiente
from formateo import generar_estado_inicial, generar_estado_aleatorio, es_resoluble # Función que genera un estado inicial resoluble
from b_estrecha import bfs             # Importa el algoritmo BFS desde el módulo correspondiente
import time

# Estado objetivo del rompecabezas (Puzzle 8)
estado_meta = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

# Configuración visual básica para el juego
TAM_CASILLA = 80
MARGEN = 10
ANCHO = 800
ALTO = 600

# Inicialización de Pygame y ventana principal
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Puzzle 8 - BFS vs A*")
fuente = pygame.font.SysFont(None, 40)

# Dibuja una matriz de 3x3 en la ventana en la posición (offset_x, offset_y)
def dibujar_matriz(ventana, matriz, offset_x, offset_y, fuente):
    for i in range(3):
        for j in range(3):
            valor = matriz[i][j]
            color = (255, 255, 255) if valor != 0 else (50, 50, 50)  # Color negro para el espacio vacío

            rect_x = offset_x + j * (TAM_CASILLA + MARGEN)
            rect_y = offset_y + i * (TAM_CASILLA + MARGEN)

            pygame.draw.rect(ventana, color, (rect_x, rect_y, TAM_CASILLA, TAM_CASILLA))
            pygame.draw.rect(ventana, (0, 0, 0), (rect_x, rect_y, TAM_CASILLA, TAM_CASILLA), 2)

            if valor != 0:
                texto = fuente.render(str(valor), True, (0, 0, 0))
                ventana.blit(texto, (rect_x + 25, rect_y + 20))

# Dibuja los botones en la interfaz (BFS, A*, Reset)
def dibujar_botones(ventana, fuente):
    boton_bfs = pygame.Rect(50, 330, 140, 40)
    boton_astar = pygame.Rect(400, 330, 140, 40)
    reset_bfs = pygame.Rect(50, 380, 140, 35)
    reset_caos = pygame.Rect(400, 380, 140, 35)

    pygame.draw.rect(ventana, (0, 128, 0), boton_bfs)
    pygame.draw.rect(ventana, (0, 0, 128), boton_astar)
    pygame.draw.rect(ventana, (180, 0, 0), reset_bfs)
    pygame.draw.rect(ventana, (128, 0, 128), reset_caos)

    ventana.blit(fuente.render("BFS", True, (255, 255, 255)), boton_bfs.move(10, 5))
    ventana.blit(fuente.render("A*", True, (255, 255, 255)), boton_astar.move(10, 5))
    ventana.blit(fuente.render("Reset", True, (255, 255, 255)), reset_bfs.move(15, 2))
    ventana.blit(fuente.render("Modo Caos", True, (255, 255, 255)), reset_caos.move(5, 2))

    return boton_bfs, boton_astar, reset_bfs, reset_caos 

# Bucle principal del juego
def main():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Puzzle 8 - BFS vs A*")
    fuente = pygame.font.SysFont(None, 36)

    corriendo = True
    estado_inicial = generar_estado_inicial(estado_meta)
    print("Estado Inicial: ", estado_inicial)

    # Variables de estado
    solucion_bfs = []
    solucion_astar = []
    tiempo_bfs = None
    tiempo_astar = None
    indice_bfs = 0
    indice_astar = 0
    mostrar_bfs = False
    mostrar_astar = False
    estado_final_bfs = None
    estado_final_astar = None

    # Bucle del juego
    while corriendo:
        ventana.fill((200, 200, 200))

        # Mostrar animación BFS
        if mostrar_bfs and indice_bfs < len(solucion_bfs):
            estado = solucion_bfs[indice_bfs]
            dibujar_matriz(ventana, estado, 50, 30, fuente)
            estado_final_bfs = estado
        elif estado_final_bfs:
            dibujar_matriz(ventana, estado_final_bfs, 50, 30, fuente)
        else:
            dibujar_matriz(ventana, estado_inicial, 50, 30, fuente)

        # Mostrar animación A*
        if mostrar_astar and indice_astar < len(solucion_astar):
            estado = solucion_astar[indice_astar]
            dibujar_matriz(ventana, estado, 400, 30, fuente)
            estado_final_astar = estado
        elif estado_final_astar:
            dibujar_matriz(ventana, estado_final_astar, 400, 30, fuente)
        else:
            dibujar_matriz(ventana, estado_inicial, 400, 30, fuente)

        # Dibujar botones
        boton_bfs, boton_astar, reset_bfs, reset_caos = dibujar_botones(ventana, fuente)

        # Mostrar tiempos si existen
        if tiempo_bfs is not None:
            txt = fuente.render(f"BFS: {tiempo_bfs:.3f}s", True, (0, 0, 0))
            ventana.blit(txt, (50, 450))

            txt = fuente.render(f"Nodos: {nodos_bfs}", True, (0, 0, 0))
            ventana.blit(txt, (50, 490))

            txt = fuente.render(f"Moves: {len(solucion_bfs) - 1}", True, (0, 0, 0))
            ventana.blit(txt, (50, 540))


        if tiempo_astar is not None:
            txt = fuente.render(f"A*: {tiempo_astar:.3f}s", True, (0, 0, 0))
            ventana.blit(txt, (400, 450))

            txt = fuente.render(f"Nodos: {nodos_astar}", True, (0, 0, 0))
            ventana.blit(txt, (400, 490))

            txt = fuente.render(f"Moves: {len(solucion_astar) - 1}", True, (0, 0, 0))
            ventana.blit(txt, (400, 540))


        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_bfs.collidepoint(evento.pos):
                        if not es_resoluble(estado_inicial, estado_meta):
                            print("¡Advertencia! Estado inicial NO resoluble. BFS no se ejecutará.")
                        else:
                            # Ejecutar búsqueda BFS
                            tiempo_inicio = time.time()
                            solucion_bfs, nodos_bfs = bfs(estado_inicial, estado_meta)
                            tiempo_bfs = time.time() - tiempo_inicio
                            if solucion_bfs:
                                print(f"BFS encontró solución en {len(solucion_bfs)-1} movimientos. Nodos: {nodos_bfs}, Tiempo: {tiempo_bfs:.4f}s")
                                indice_bfs = 0
                                mostrar_bfs = True

                elif boton_astar.collidepoint(evento.pos):
                    if not es_resoluble(estado_inicial, estado_meta):
                        print("¡Advertencia! Estado inicial NO resoluble. BFS no se ejecutará.")
                    else:
                    # Ejecutar búsqueda A*
                        tiempo_inicio = time.time()
                        solucion_astar, nodos_astar = a_star(estado_inicial, estado_meta)
                        tiempo_astar = time.time() - tiempo_inicio
                        if solucion_astar:
                            print(f"A* encontró solución en {len(solucion_astar)-1} movimientos. Nodos: {nodos_astar}, Tiempo: {tiempo_astar:.4f}s")
                            indice_astar = 0
                            mostrar_astar = True

                elif reset_bfs.collidepoint(evento.pos):
                    # Reiniciar estado y limpiar resultados
                    estado_inicial = generar_estado_inicial(estado_meta)
                    solucion_bfs = []
                    solucion_astar = []
                    tiempo_bfs = None
                    tiempo_astar = None
                    indice_bfs = 0
                    indice_astar = 0
                    mostrar_bfs = False
                    mostrar_astar = False
                    estado_final_bfs = None
                    estado_final_astar = None
                
                elif reset_caos.collidepoint(evento.pos):
                    estado_inicial = generar_estado_aleatorio()
                    print("Estado aleatorio (sin verificar resolubilidad):", estado_inicial)

                    solucion_bfs = []
                    solucion_astar = []
                    tiempo_bfs = None
                    tiempo_astar = None
                    indice_bfs = 0
                    indice_astar = 0
                    mostrar_bfs = False
                    mostrar_astar = False
                    estado_final_bfs = None
                    estado_final_astar = None


        # Animar solución paso a paso
        if mostrar_bfs and indice_bfs < len(solucion_bfs) - 1:
            indice_bfs += 1
            pygame.time.delay(800)
        else:
            mostrar_bfs = False

        if mostrar_astar and indice_astar < len(solucion_astar) - 1:
            indice_astar += 1
            pygame.time.delay(800)
        else:
            mostrar_astar = False

    pygame.quit()
    sys.exit()

# Ejecutar si se corre directamente
if __name__ == "__main__":
    main()
