# Análisis Final de Estrategias de Búsqueda

## 1. Resultados obtenidos

### **BFS (Breadth-First Search)**

* Siempre encuentra el **camino óptimo** (menor número de pasos).
* Expande muchos nodos porque explora en anchura.
* En grillas grandes, el costo computacional y el número de nodos expandidos crece rápidamente.

### **DFS (Depth-First Search)**

* Encuentra un camino, pero **no garantiza optimalidad**.
* Tiende a recorrer largas ramas inútiles antes de encontrar el oro.
* Su ventaja es el **bajo uso de memoria** (solo necesita almacenar la rama actual).

### **A**\*

* Encuentra el **camino óptimo**, igual que BFS.
* Expande significativamente **menos nodos** porque guía la búsqueda usando la heurística Manhattan.
* Es el más **eficiente** en este dominio (grilla con movimientos uniformes).

---

## 2. Comparación de métricas

| Algoritmo | Camino (pasos) | Nodos expandidos | Optimalidad | Eficiencia |
| --------- | -------------- | ---------------- | ----------- | ---------- |
| **BFS**   | Óptimo         | Alto             | ✔️ Sí       | Baja       |
| **DFS**   | No óptimo      | Variable         | ❌ No        | Media      |
| **A**\*   | Óptimo         | Bajo             | ✔️ Sí       | Alta       |

---

## 3. Conclusiones

* **BFS** asegura siempre la solución óptima, pero a un costo elevado de expansión.
* **DFS** puede ser útil en entornos pequeños o cuando se busca solo "alguna solución", pero no es recomendable si se necesita optimalidad.
* **A**\* combina lo mejor de ambos mundos: logra la solución óptima como BFS, pero con mucha mayor eficiencia al reducir la exploración innecesaria.

➡️ En este problema del Mundo del Wumpus simplificado, **A**\* es la estrategia más recomendable porque garantiza el camino más corto con la menor cantidad de nodos expandidos.
