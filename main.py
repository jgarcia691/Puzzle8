import pygame
import sys
from b_informada import a_star
from formateo import generar_estado_inicial
from b_estrecha import bfs
import time

# Matriz de estado (puedes cambiarla luego con un generador aleatorio válido)
estado_meta = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

# Configuración básica
TAM_CASILLA = 80
MARGEN = 10
ANCHO = 800  # como mínimo (3 celdas de 100px + separación)
ALTO = 600

pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Puzzle 8 - BFS vs A*")
fuente = pygame.font.SysFont(None, 40)


def dibujar_matriz(ventana, matriz, offset_x, offset_y, fuente):
    for i in range(3):
        for j in range(3):
            valor = matriz[i][j]
            color = (255, 255, 255) if valor != 0 else (50, 50, 50)

            rect_x = offset_x + j * (TAM_CASILLA + MARGEN)
            rect_y = offset_y + i * (TAM_CASILLA + MARGEN)

            pygame.draw.rect(
                ventana,
                color,
                (rect_x, rect_y, TAM_CASILLA, TAM_CASILLA)
            )
            pygame.draw.rect(ventana, (0, 0, 0), (rect_x, rect_y, TAM_CASILLA, TAM_CASILLA), 2)

            if valor != 0:
                texto = fuente.render(str(valor), True, (0, 0, 0))
                ventana.blit(texto, (rect_x + 25, rect_y + 20))



def dibujar_botones(ventana, fuente):
    # Botones de ejecución
    boton_bfs = pygame.Rect(50, 330, 140, 40)
    boton_astar = pygame.Rect(400, 330, 140, 40)

    # Botones de reinicio
    reset_bfs = pygame.Rect(50, 380, 140, 35)

    # Dibujar botones
    pygame.draw.rect(ventana, (0, 128, 0), boton_bfs)
    pygame.draw.rect(ventana, (0, 0, 128), boton_astar)

    pygame.draw.rect(ventana, (180, 0, 0), reset_bfs)

    # Dibujar texto
    ventana.blit(fuente.render("BFS", True, (255, 255, 255)), boton_bfs.move(10, 5))
    ventana.blit(fuente.render("A*", True, (255, 255, 255)), boton_astar.move(10, 5))
    ventana.blit(fuente.render("Reset", True, (255, 255, 255)), reset_bfs.move(15, 2))

    return boton_bfs, boton_astar, reset_bfs


# ---------- MAIN LOOP ----------
def main():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Puzzle 8 - BFS vs A*")
    fuente = pygame.font.SysFont(None, 36)

    corriendo = True
    estado_inicial = generar_estado_inicial(estado_meta)
    print("Estado Inicial: ",estado_inicial)
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


    while corriendo:
        ventana.fill((200, 200, 200))

        
        

        # -------- DIBUJO MATRIZ BFS (izquierda) --------
        if mostrar_bfs and indice_bfs < len(solucion_bfs):
            estado = solucion_bfs[indice_bfs]
            print("Estado actual BFS:", solucion_bfs[indice_bfs])
            dibujar_matriz(ventana, estado, 50, 30, fuente)
            estado_final_bfs = estado  # Guarda último mostrado
        elif estado_final_bfs:
            dibujar_matriz(ventana, estado_final_bfs, 50, 30, fuente)
        else:
            dibujar_matriz(ventana, estado_inicial, 50, 30, fuente)

        # -------- DIBUJO MATRIZ A* (derecha) --------
        if mostrar_astar and indice_astar < len(solucion_astar):
            estado = solucion_astar[indice_astar]
            print("Estado actual A*:", solucion_astar[indice_astar])
            dibujar_matriz(ventana, estado, 400, 30, fuente)
            estado_final_astar = estado
        elif estado_final_astar:
            dibujar_matriz(ventana, estado_final_astar, 400, 30, fuente)
        else:
            dibujar_matriz(ventana, estado_inicial, 400, 30, fuente)

            

        # Dibujar botones
        boton_bfs, boton_astar, reset_bfs = dibujar_botones(ventana, fuente)

        if tiempo_bfs is not None:
            txt = fuente.render(f"BFS: {tiempo_bfs:.3f}s", True, (0, 0, 0))
            ventana.blit(txt, (50, 500))

        if tiempo_astar is not None:
            txt = fuente.render(f"A*: {tiempo_astar:.3f}s", True, (0, 0, 0))
            ventana.blit(txt, (400, 500))


        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_bfs.collidepoint(evento.pos):
                    print("Ejecutar BFS...")
                    tiempo_inicio = time.time()
                    solucion_bfs, nodos_bfs = bfs(estado_inicial, estado_meta)
                    tiempo_bfs = time.time() - tiempo_inicio

                    if solucion_bfs:
                        print(f"BFS encontró solución en {len(solucion_bfs)} movimientos. Nodos: {nodos_bfs}, Tiempo: {tiempo_bfs:.4f}s")
                        indice_bfs = 0
                        mostrar_bfs = True
                    else:
                        print("No se encontró solución con BFS.")

                elif boton_astar.collidepoint(evento.pos):
                    print("Ejecutar A*...")
                    tiempo_inicio = time.time()
                    solucion_astar, nodos_astar = a_star(estado_inicial, estado_meta)
                    tiempo_astar = time.time() - tiempo_inicio

                    if solucion_astar:
                        print(f"A* encontró solución en {len(solucion_astar)} movimientos. Nodos: {nodos_astar}, Tiempo: {tiempo_astar:.4f}s")
                        indice_astar = 0
                        mostrar_astar = True
                    else:
                        print("No se encontró solución con A*.")
                
                elif reset_bfs.collidepoint(evento.pos):
                    estado_inicial = generar_estado_inicial(estado_meta)
                    print("Nuevo estado inicial:", estado_inicial)

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

        
            pygame.display.flip()

        # --- ANIMAR BFS paso a paso ---
        if mostrar_bfs:
            print(f"{len(solucion_bfs)} movimientos")
            if indice_bfs < len(solucion_bfs) - 1:
                indice_bfs += 1
                pygame.time.delay(800)  # <- PAUSA entre pasos
            else:
                mostrar_bfs = False

        # --- ANIMAR A* paso a paso ---
        if mostrar_astar:
            if indice_astar < len(solucion_astar) - 1:
                indice_astar += 1
                pygame.time.delay(800)
            else:
                mostrar_astar = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
