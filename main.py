# --- Mundo del Wumpus simplificado: modelamiento base ---
from collections import deque
import seaborn as sns
import matplotlib.pyplot as plt
import heapq
import copy
import random

def generar_mapa(n=20, prob_pozo=0.1, seed=None):

    if seed is not None:
        random.seed(seed)

    # Inicializar grilla vacía
    grid = [["." for _ in range(n)] for _ in range(n)]

    # Definir posiciones fijas
    start = (n-1, 0)   # esquina inferior izquierda
    goal = (0, n-1)    # esquina superior derecha
    grid[start[0]][start[1]] = "A"
    grid[goal[0]][goal[1]] = "G"

    # Llenar con pozos aleatorios
    for r in range(n):
        for c in range(n):
            if (r, c) not in [start, goal]:  # evitar A y G
                if random.random() < prob_pozo:
                    grid[r][c] = "P"

    return grid

# Ejemplo de uso
mapa = generar_mapa(20, prob_pozo=0.15, seed=42)

# Mostrar primeras filas
for fila in mapa[:5]:
    print(fila)




# Grilla 4x4 de ejemplo (el docente puede cambiarla en clase)
GRIDS = [[
    [".","P",".","G"],
    [".",".","P","."],
    [".",".",".","."],
    ["A",".",".","."]
    ],
    generar_mapa(n=10, prob_pozo=0.1),
    generar_mapa(n=15, prob_pozo=0.1),
    generar_mapa(n=20, prob_pozo=0.1)]

RUN = len(GRIDS)

for grid in GRIDS:

    ROWS, COLS = len(grid), len(grid[0])

    # Estado inicial (A) y objetivo (G)
    def find(symbol):
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == symbol:
                    return (r, c)
        return None
    INI = find("A")
    GOAL = find("G")

    # Movimientos validos: 4 direcciones (N, S, E, O)
    DIRS4 = [(1,0),(-1,0),(0,1),(0,-1)]

    def in_bounds(r, c):
        return 0 <= r < ROWS and 0 <= c < COLS

    def passable(r, c):
        # No se puede pasar por pozos
        return grid[r][c] != "P"


    def neighbors(r, c):
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc) and passable(nr, nc):
                yield (nr, nc)

    def reconstruct(parent, goal):
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parent.get(cur)
        return path[::-1]


    # --- Puntos de integracin (implementar en otro archivo o debajo):
    def bfs(start=INI, goal=GOAL):
        frontier = deque([start])
        parent = {start: None}
        expanded = []  # keep track of expansions

        while frontier:
            current = frontier.popleft()
            expanded.append(current)

            if current == goal:
                return reconstruct(parent, goal), expanded

            for nxt in neighbors(*current):
                if nxt not in parent:
                    parent[nxt] = current
                    frontier.append(nxt)
        return None, expanded


    def dfs(start=INI, goal=GOAL):
        stack = [start]
        parent = {start: None}
        expanded = []

        while stack:
            current = stack.pop()
            expanded.append(current)

            if current == goal:
                return reconstruct(parent, goal), expanded

            for nxt in reversed(list(neighbors(*current))):
                if nxt not in parent:
                    parent[nxt] = current
                    stack.append(nxt)
        return None, expanded

    def manhattan(a, b):
        (r1, c1), (r2, c2) = a, b
        return abs(r1 - r2) + abs(c1 - c2)


    def astar(start=INI, goal=GOAL, heuristic=manhattan):
        frontier = []
        heapq.heappush(frontier, (0, start))
        parent = {start: None}
        g_score = {start: 0}
        expanded = []

        while frontier:
            _, current = heapq.heappop(frontier)
            expanded.append(current)

            if current == goal:
                return reconstruct(parent, goal), expanded

            for nxt in neighbors(*current):
                tentative_g = g_score[current] + 1
                if nxt not in g_score or tentative_g < g_score[nxt]:
                    g_score[nxt] = tentative_g
                    f_score = tentative_g + heuristic(nxt, goal)
                    heapq.heappush(frontier, (f_score, nxt))
                    parent[nxt] = current
        return None, expanded


    def plot_path(path, expanded=None, title="Camino encontrado"):
        # Crear una matriz numérica para el mapa
        # 0 = libre, 1 = pozo, 2 = agente, 3 = oro, 4 = camino, 5 = expandidos
        mapa = []
        for r in range(ROWS):
            fila = []
            for c in range(COLS):
                if grid[r][c] == ".":
                    fila.append(0)
                elif grid[r][c] == "P":
                    fila.append(1)
                elif grid[r][c] == "A":
                    fila.append(2)
                elif grid[r][c] == "G":
                    fila.append(3)
            mapa.append(fila)

        # Marcar nodos expandidos si se proporcionan
        if expanded:
            for r, c in expanded:
                if mapa[r][c] == 0:  # Solo marcar si es espacio libre
                    mapa[r][c] = 5

        # Marcar el camino encontrado
        if path:
            for i, (r, c) in enumerate(path):
                if mapa[r][c] not in (2, 3):  # Solo marcar si es espacio libre
                    mapa[r][c] = 4

        # Definir colores para cada tipo de celda
        cmap = sns.color_palette([
            "#e0e0e0",  # 0: libre
            "#c62828",  # 1: pozo
            "#1565c0",  # 2: agente
            "#ffd600",  # 3: oro
            "#2e7d32",  # 4: camino
            "#80cbc4"  # 5: expandidos
        ])

        # Crear anotaciones para el grid
        annotations = []
        for r in range(ROWS):
            row_annotations = []
            for c in range(COLS):
                if grid[r][c] != ".":
                    row_annotations.append(grid[r][c])
                elif mapa[r][c] == 4:
                    row_annotations.append("•")  # Camino
                elif mapa[r][c] == 5:
                    row_annotations.append("×")  # Expandido
                else:
                    row_annotations.append("")
            annotations.append(row_annotations)

        # Graficar el mapa
        plt.figure(figsize=(8, 8))
        ax = sns.heatmap(mapa, annot=annotations, fmt="", cmap=cmap, cbar=False,
                         linewidths=1, linecolor="black", square=True)

        # Dibujar flechas para mostrar el movimiento en el camino
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                r1, c1 = path[i]
                r2, c2 = path[i + 1]

                # Calcular dirección de la flecha
                dr = r2 - r1
                dc = c2 - c1

                # Posición central de la flecha
                x = c1 + 0.5
                y = r1 + 0.5

                # Dibujar flecha
                plt.arrow(x, y, dc * 0.6, dr * 0.6,
                         head_width=0.15, head_length=0.15,
                         fc='red', ec='red', alpha=0.8)

        plt.title(title, fontsize=14, pad=20)
        plt.xticks([])
        plt.yticks([])

        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor="#e0e0e0", edgecolor="black", label="Libre"),
            plt.Rectangle((0, 0), 1, 1, facecolor="#c62828", edgecolor="black", label="Pozo"),
            plt.Rectangle((0, 0), 1, 1, facecolor="#1565c0", edgecolor="black", label="Agente"),
            plt.Rectangle((0, 0), 1, 1, facecolor="#ffd600", edgecolor="black", label="Oro"),
            plt.Rectangle((0, 0), 1, 1, facecolor="#2e7d32", edgecolor="black", label="Camino"),
            plt.Rectangle((0, 0), 1, 1, facecolor="#80cbc4", edgecolor="black", label="Expandido"),
        ]

        plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        plt.show()



    def show_path(path, grid):
        g = copy.deepcopy(grid)
        if path is None:
            return g  # No hay camino
        for (r, c) in path:
            if g[r][c] not in ("A", "G"):  # No reemplazar inicio/goal
                g[r][c] = "*"
        return g

    def print_grid(g):
        for row in g:
            print(" ".join(row))
        print()




    path_bfs, exp_bfs = bfs()
    path_dfs, exp_dfs = dfs()
    path_astar, exp_astar = astar()

    print("\nBFS path:")
    print_grid(show_path(path_bfs, grid))
    print("BFS expanded:", exp_bfs)
    print("Costo: ",len(path_bfs)-1 if path_bfs else 0)
    print("Nodos expandidos: ", len(exp_bfs))
    if path_bfs:
        plot_path(path_bfs, exp_bfs, "Camino BFS")

    print("\nDFS path:")
    print_grid(show_path(path_dfs, grid))
    print("DFS expanded:", exp_dfs)
    print("Costo: ",len(path_dfs)-1 if path_dfs else 0)
    print("Nodos expandidos: ", len(exp_dfs))
    if path_dfs:
        plot_path(path_dfs, exp_dfs, "Camino DFS")

    print("\nA* path:")
    print_grid(show_path(path_astar, grid))
    print("A* expanded:", exp_astar)
    print("Costo: ",len(path_astar)-1 if path_astar else 0)
    print("Nodos expandidos: ", len(exp_astar))
    if path_astar:
        plot_path(path_astar, exp_astar, "Camino Astar")




