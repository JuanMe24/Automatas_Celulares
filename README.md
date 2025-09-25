# :house_with_garden: Automatas Celulares
Juan David Meza Criollo  
Andres Avilán  

## 1. Reglas básicas de comportamiento

En la vida cotidiana, así como en los **autómatas celulares (AC)**, existen **reglas locales** que guían el comportamiento de cada individuo en función de su contexto inmediato o “vecindad”. Estas reglas no son impuestas por un control central, sino que emergen de la interacción con los demás y con el entorno, generando patrones de conducta colectivos.  

### En la casa
Algunas de las reglas cotidianas son:  
- Tender la cama antes de salir.  
- Servir la comida a los perros a las 8 a.m.  
- Cenar junto a mi hermano en las noches.  
- No hacer mucho ruido en las noches entre semana.  
- Recoger la losa sucia del cuarto.  

**Paralelismo con AC:** cada regla depende de un **estado inicial** (por ejemplo: “antes de salir” → tender la cama) o de la **influencia de un vecino** (cenar junto a mi hermano). En términos de vecindad, estas conductas se activan de acuerdo con la situación del entorno inmediato, igual que una celda que cambia de estado dependiendo de sus vecinas.

---

### En la universidad
Algunas reglas sociales y académicas son:  
- Prestar atención en clase.  
- No hacer plagio.  
- Taparse al estornudar.  

**Paralelismo con AC:** estas normas funcionan como **condiciones de transición**:  
- Si el profesor explica (vecino activo), el estudiante atiende.  
- Si un compañero estornuda, la reacción esperada es cubrirse.  
Así como en los AC, el comportamiento individual se ajusta en relación con la **vecindad académica y social**.

---

### En el transporte público
Las reglas más comunes son:  
- Hacer la fila mientras se espera el bus.  
- Respetar el turno al abordar.  

**Paralelismo con AC:** aquí se observa claramente la lógica de **vecindad secuencial**: una persona avanza solo cuando la persona de adelante avanza, igual que una celda cambia su estado en función de lo que ocurre en su vecina inmediata.

---

### Síntesis
Al igual que en los autómatas celulares, las conductas en casa, en la universidad o en el transporte público se rigen por **reglas simples y locales** que, al combinarse, generan un **orden social colectivo**.

## 🚗 2. Modelo de difusión o robot de dos ruedas

En lugar de un modelo de difusión, se plantea un **robot móvil de dos ruedas** que se desplaza en un entorno y debe **evitar obstáculos**. Para modelar su comportamiento podemos usar el marco de los **autómatas celulares (AC)**.

### Estados del robot
- `0` → Avanzar recto.  
- `1` → Girar a la izquierda.  
- `2` → Girar a la derecha.  
- `3` → Detenerse.  

### Vecindad
El robot percibe su entorno inmediato mediante sensores de proximidad. En el modelo, los obstáculos cercanos equivalen a los **vecinos activos** en un AC, que determinan el cambio de estado.

- **Sensor izquierdo** → detecta obstáculos a la izquierda.  
- **Sensor derecho** → detecta obstáculos a la derecha.  
- **Sensor frontal** → detecta obstáculos de frente.  

### Reglas de transición (analogía con AC)
1. Si **sensor frontal detecta obstáculo** → cambiar a estado `3` (detenerse) y luego decidir giro.  
2. Si **sensor izquierdo detecta obstáculo** → pasar a estado `2` (girar a la derecha).  
3. Si **sensor derecho detecta obstáculo** → pasar a estado `1` (girar a la izquierda).  
4. Si **ningún sensor detecta obstáculo** → permanecer en estado `0` (avanzar recto).  

### Paralelismo con los autómatas celulares
- En un AC, cada celda actualiza su estado en función de la vecindad (ej. Moore o Von Neumann).  
- En el robot, el "estado" es la acción que ejecuta, y la "vecindad" son los sensores que leen el entorno inmediato.  
- Así como en un AC los patrones globales emergen de reglas locales, en el robot el **comportamiento global de navegación** emerge de reglas simples de evasión.  

### Ejemplo de secuencia
1. El robot inicia en estado `0` (avanzando).  
2. Encuentra un obstáculo de frente → pasa a estado `3` (detenerse).  
3. Evalúa los sensores laterales: si el derecho está libre, pasa a estado `2` (giro derecha).  
4. Una vez libre, regresa al estado `0` (avanzar).  

De esta forma, con reglas **locales y simples**, el robot logra un comportamiento **emergente de navegación autónoma**, análogo a la dinámica de los autómatas celulares.

## 3. Simulación de un robot y coliciones. 

Primero se planteo el esquematico: 

<p align="center">
  <img src="img_taller2/esqrob.png" alt="Vista del robot" />
</p>

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# -----------------------------
# 1. Parámetros del entorno
# -----------------------------
arena_size = 10
num_obstacles = 4
step_size = 0.2  # cuanto avanza por paso

# Obstáculos aleatorios
np.random.seed(40)  
obstacles = np.random.uniform(1, 10, size=(num_obstacles, 2))

# -----------------------------
# 2. Robot inicial
# -----------------------------
robot_pos = np.array([5.0, 2.0])  # posición inicial
directions = {
    "up": np.array([0, 1]),
    "down": np.array([0, -1]),
    "left": np.array([-1, 0]),
    "right": np.array([1, 0]),
}
robot_dir = "up"  # dirección inicial

# -----------------------------
# 3. Función para detección de colisión
# -----------------------------
def detect_collision(pos, direction, obstacles, threshold=0.6):
    """Detecta si en la próxima posición hay un obstáculo o un borde"""
    next_pos = pos + directions[direction] * step_size
    
    # 1) Revisar obstáculos
    for obs in obstacles:
        if np.linalg.norm(next_pos - obs) < threshold:
            return True
    
    # 2) Revisar bordes de la cuadrícula
    if (next_pos[0] - threshold < 0 or next_pos[0] + threshold > arena_size or
        next_pos[1] - threshold < 0 or next_pos[1] + threshold > arena_size):
        return True
    
    return False

# -----------------------------
# 4. Reglas de comportamiento
# -----------------------------
def update_robot(pos, direction, obstacles):
    if detect_collision(pos, direction, obstacles):
        # Si hay choque, giramos a otra dirección
        if direction == "up":
            direction = "right"
        elif direction == "right":
            direction = "down"
        elif direction == "down":
            direction = "left"
        else:
            direction = "up"
    # Avanzar en la dirección actual
    pos = pos + directions[direction] * step_size
    return pos, direction

# -----------------------------
# 5. Animación con matplotlib
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, arena_size)
ax.set_ylim(0, arena_size)
ax.set_aspect('equal')

# Dibujar obstáculos
obstacle_patches = [plt.Rectangle((x-0.3, y-0.3), 0.6, 0.6, color="green") for x, y in obstacles]
for patch in obstacle_patches:
    ax.add_patch(patch)

# Dibujar robot
robot_patch = plt.Circle(robot_pos, 0.3, color="skyblue", ec="blue")
ax.add_patch(robot_patch)

def animate(frame):
    global robot_pos, robot_dir
    robot_pos, robot_dir = update_robot(robot_pos, robot_dir, obstacles)
    robot_patch.center = robot_pos
    return robot_patch,

ani = animation.FuncAnimation(fig, animate, frames=200, interval=200, blit=True)
plt.show()

```
Se puede ver el funcionamiento en el siguiente gif:  
<p align="center">
  <img src="img_taller2/taller2_robsim.gif" alt="Simulación del robot" width="700" />
</p>

## 4. Diagrama de Voronoi para servicios urbanos

### Objetivo
Tomar un plano simplificado de una ciudad pequeña y ubicar puntos que representen **droguerías**, **centros de salud** y **colegios**. Construir el **diagrama de Voronoi** para visualizar la zona de influencia de cada servicio y analizar posibles deficiencias de cobertura.

### Procedimiento
1. Representar el área de la ciudad como un plano 2D (por ejemplo, coordenadas X e Y en [0, 10]).  
2. Ubicar las instalaciones (puntos) con coordenadas (pueden ser reales o generadas aleatoriamente con semilla para reproducibilidad).  
3. Construir el diagrama de Voronoi para todos los puntos de servicio (o por tipo si se quiere comparar).  
4. Analizar las regiones:
   - Regiones muy extensas indican **posible falta de cobertura**.
   - Agrupaciones densas indican **posible saturación** de servicios en una zona.
5. Calcular métricas simples (opcional): distancia media al servicio más cercano, porcentaje del área por encima de un umbral de distancia (zonas mal servidas).

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import os

# -----------------------------
# Parámetros
# -----------------------------
np.random.seed(42)         
area_size = 10.0            # tamaño del plano [0, area_size] x [0, area_size]
n_drog = 3
n_salud = 2
n_coleg = 3
plot_path = "../plots"
os.makedirs(plot_path, exist_ok=True)

# -----------------------------
# Generar/definir puntos
# -----------------------------
# aquí usamos puntos aleatorios reproducibles; puedes fijar coordenadas manuales
drog = np.random.uniform(1, area_size-1, size=(n_drog, 2))
salud = np.random.uniform(1, area_size-1, size=(n_salud, 2))
coleg = np.random.uniform(1, area_size-1, size=(n_coleg, 2))

# unir todos los puntos 
points = np.vstack([drog, salud, coleg])
types = (["drog"] * n_drog) + (["salud"] * n_salud) + (["coleg"] * n_coleg)

# -----------------------------
# Construir Voronoi
# -----------------------------
vor = Voronoi(points)

# -----------------------------
# Plot base
# -----------------------------
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, area_size)
ax.set_ylim(0, area_size)
ax.set_aspect('equal')
ax.set_title("Diagrama de Voronoi - Servicios urbanos (simulado)")

# dibujar diagrama (líneas)
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='gray', line_width=1, line_alpha=0.7, point_size=0)

# colorear puntos por tipo
colors = {'drog': 'tab:green', 'salud': 'tab:red', 'coleg': 'tab:blue'}
markers = {'drog': 's', 'salud': 'D', 'coleg': '^'}
for t in set(types):
    mask = [i for i, tt in enumerate(types) if tt == t]
    pts = points[mask]
    ax.scatter(pts[:,0], pts[:,1], c=colors[t], marker=markers[t], s=120, label=t.capitalize())

ax.legend()

# agregar etiquetas con coordenadas (opcional)
for i, p in enumerate(points):
    ax.text(p[0]+0.12, p[1]+0.12, f"{i}", fontsize=9)

# guardar figura
out_png = os.path.join(plot_path, "voronoi_city.png")
plt.savefig(out_png, dpi=300, bbox_inches='tight')
print(f"Se guardo la imagen en: {out_png}")

# -----------------------------
# Análisis simple de cobertura
# -----------------------------
# muestreo en una rejilla fina para estimar distancia al servicio más cercano
grid_n = 200
xs = np.linspace(0, area_size, grid_n)
ys = np.linspace(0, area_size, grid_n)
xx, yy = np.meshgrid(xs, ys)
grid_points = np.column_stack([xx.ravel(), yy.ravel()])

# distancia a punto de servicio más cercano (euclidiana)
dists = np.linalg.norm(grid_points[:, None, :] - points[None, :, :], axis=2)  # (ngrid, npoints)
min_dists = dists.min(axis=1)

# métricas
mean_dist = min_dists.mean()
median_dist = np.median(min_dists)

# calcular % de área con distancia > umbral
umbral = 1.5
pct_bad = 100.0 * np.mean(min_dists > umbral)

print(f"Distancia media al servicio mas cercano: {mean_dist:.3f}")
print(f"Distancia mediana al servicio mas cercano: {median_dist:.3f}")
print(f"Porcentaje del area con distancia > {umbral}: {pct_bad:.2f}%")


bad_mask = (min_dists > umbral)
if bad_mask.any():
    bad_pts = grid_points[bad_mask]
    ax.scatter(bad_pts[:,0], bad_pts[:,1], s=2, c='orange', alpha=0.3, label=f'Área > {umbral}')
    ax.legend()

out_png2 = os.path.join(plot_path, "voronoi_city_coverage.png")
plt.savefig(out_png2, dpi=300, bbox_inches='tight')
print(f"Se guardo la imagen con zonas de mala cobertura en: {out_png2}")

# mostrar en pantalla
plt.show()
```
Se guardo la imagen en: ../plots\voronoi_city.png  
Distancia media al servicio mas cercano: 1.785  
Distancia mediana al servicio mas cercano: 1.728  
Porcentaje del area con distancia > 1.5: 59.03% 

<p align="center">
  <img src="img_taller2/voronoi_city_coverage.png" alt="Voronoi" width="600" />
</p>

### Interpretación / Análisis
- **Cobertura insuficiente**: zonas cuya distancia al servicio más cercano supera un umbral razonable (p. ej. 1.5 unidades en el plano normalizado).  
- **Saturación**: barrios con varias regiones de Voronoi pequeñas superpuestas entre tipos (posible duplicación de servicios).  
- **Recomendación práctica**: proponer la ubicación de un nuevo servicio en las regiones más lejanas (centroides de las celdas más grandes o puntos con máxima distancia al servicio).



