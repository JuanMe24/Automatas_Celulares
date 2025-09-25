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
