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
print(f"Se guardó la imagen en: {out_png}")

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

print(f"Distancia media al servicio más cercano: {mean_dist:.3f}")
print(f"Distancia mediana al servicio más cercano: {median_dist:.3f}")
print(f"Porcentaje del área con distancia > {umbral}: {pct_bad:.2f}%")


bad_mask = (min_dists > umbral)
if bad_mask.any():
    bad_pts = grid_points[bad_mask]
    ax.scatter(bad_pts[:,0], bad_pts[:,1], s=2, c='orange', alpha=0.3, label=f'Área > {umbral}')
    ax.legend()

# re-guardar figura con overlay de zonas mal servidas
out_png2 = os.path.join(plot_path, "voronoi_city_coverage.png")
plt.savefig(out_png2, dpi=300, bbox_inches='tight')
print(f"Se guardó la imagen con zonas de mala cobertura en: {out_png2}")

# mostrar en pantalla
plt.show()
