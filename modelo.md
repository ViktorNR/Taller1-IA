# Modelamiento Previo al Código: Mundo del Wumpus Simplificado

Antes de programar, se debe estructurar el problema como un **problema de búsqueda en grafos**. Esto implica definir los elementos esenciales: estados, acciones, transiciones y objetivo.

---

## 1. Representación del mundo

* **Entorno**: una grilla 4×4.
* **Celdas**: pueden ser libres (`.`), pozos (`P`), inicio (`A`) u objetivo (`G`).
* **Restricción**: no se puede atravesar una celda con pozo.

Ejemplo de grilla:

```
. P . G
. . P .
. . . .
A . . .
```

---

## 2. Estados

* Un **estado** se define por la posición del agente en la grilla: `(fila, columna)`.
* **Estado inicial**: coordenada donde está `A`.
* **Estado meta**: coordenada donde está `G`.

---

## 3. Acciones

* Conjunto de acciones posibles: mover **Norte, Sur, Este u Oeste**.
* Restricciones:

  * El movimiento no debe salir de la grilla.
  * El movimiento no debe llevar a un pozo (`P`).

---

## 4. Transición

* Función de transición: `(r, c) + (dr, dc) -> (r+dr, c+dc)`.
* Válida si `(r+dr, c+dc)` está dentro de la grilla y no es pozo.

---

## 5. Costo de las acciones

* Cada movimiento tiene un costo uniforme de **1 paso**.
* El costo total de un camino es la suma de los pasos.

---

## 6. Objetivo

* Alcanzar la celda que contiene el `G` (oro).

---

## 7. Estrategias de búsqueda a aplicar

* **BFS**: asegura encontrar la solución óptima (mínimos pasos).
* **DFS**: puede encontrar soluciones pero no garantiza optimalidad.
* **A**\*: utiliza heurística Manhattan para encontrar el camino óptimo de forma más eficiente que BFS.

---

## 8. Heurística (para A\*)

* Se utiliza la **distancia Manhattan** entre el estado actual `(r, c)` y el objetivo `(r_goal, c_goal)`:

  ```
  h = |r - r_goal| + |c - c_goal|
  ```
* Propiedades: es **admisible** y **consistente** en este dominio.

---

✅ Este modelamiento conceptual es la base previa antes de escribir código: permite tener claro **qué se busca, cómo se representa y cuáles son las reglas del entorno**.





# Modelamiento del Problema: Mundo del Wumpus Simplificado

## Representación del Estado

* El **estado** se modela como una tupla `(r, c)` que indica la posición actual del agente en la grilla.
* Estado inicial: coordenada de `A` (Agente).
* Estado meta: coordenada de `G` (Oro).

## Espacio de Estados

* Todos los pares `(r, c)` que cumplen:

  * `0 <= r < ROWS`, `0 <= c < COLS` (dentro de los límites).
  * La celda `(r, c)` **no contiene un pozo** (`P`).

## Operadores (Acciones)

* Conjunto de movimientos posibles: **4 direcciones** (Norte, Sur, Este, Oeste).
* Acción válida si la celda destino está dentro de la grilla y es transitable (no es pozo).

## Función de Transición

* Dado un estado `(r, c)` y una acción `(dr, dc)`, el nuevo estado es `(r+dr, c+dc)` si es válido.

## Costo de Camino

* Cada acción tiene un costo uniforme de `1`.
* El costo total de un camino es la cantidad de pasos realizados.

## Función Objetivo

* El problema se resuelve cuando el agente alcanza la celda `G` (oro).

## Heurística (para A\*)

* Distancia Manhattan entre el estado actual `(r, c)` y la meta `(r_goal, c_goal)`:

  ```
  h((r, c)) = |r - r_goal| + |c - c_goal|
  ```
* Es **admisible** porque nunca sobreestima el costo real.
* Es **consistente** porque cumple la desigualdad triangular en movimientos de costo uniforme.

## Estructuras de Datos Usadas

* **BFS**: Cola FIFO (`collections.deque`).
* **DFS**: Pila LIFO (lista en Python con `.append()` y `.pop()`).
* **A**\*: Cola de prioridad (min-heap con `heapq`).

## Reconstrucción de Solución

* Se usa un diccionario `parent` que guarda para cada nodo el nodo del cual provino.
* La solución se reconstruye recorriendo `parent` desde la meta hasta el inicio.

---

✅ Con este modelamiento se puede aplicar cualquier estrategia de búsqueda (BFS, DFS, A\*) sobre la misma base.



