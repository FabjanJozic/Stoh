import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import re

# ucitavanje mape spinova po temperaturi
theta_file = 'theta_map_32x32.dat'
with open(theta_file, 'r') as f:
    raw_lines = f.readlines()

theta_configs = []
theta_temperatures = []
current_config = []
current_T = None

for line in raw_lines:
    if line.startswith('#'):
        if current_config and current_T is not None:
            try:
                theta_array = np.array(current_config, dtype=float)
                theta_configs.append(theta_array)
                theta_temperatures.append(float(current_T))
            except ValueError:
                print(f"Skipped malformed configuration at T = {current_T}")
            current_config = []
        match = re.search(r'T\s*=\s*([\d.]+)', line)
        if match:
            current_T = match.group(1)
        else:
            current_T = None
    elif line.strip():  # skip empty lines
        row = [float(val) for val in line.strip().split()]
        current_config.append(row)

# za zadnju konfiguraciju ako daje error
if current_config and current_T is not None:
    try:
        theta_array = np.array(current_config, dtype=float)
        theta_configs.append(theta_array)
        theta_temperatures.append(float(current_T))
    except ValueError:
        print(f"Skipped malformed configuration at T = {current_T}")

# ucitavanje informacija o vrtlozima i antivrtlozima
vortex_data = np.genfromtxt('vortex_coords_32x32.dat', comments='#',
                            dtype=[('T', 'f4'), ('x', 'i4'), ('y', 'i4'),('charge', 'i4')], delimiter=None)

# podesavanje mreze
grid_size = 32
X, Y = np.meshgrid(np.arange(grid_size), np.arange(grid_size))

# stvaranje GIFa
fig, ax = plt.subplots(figsize=(6, 6))
metadata = dict(title="Theta Field with Vortices", artist="Matplotlib")
writer = PillowWriter(fps=2, metadata=metadata)

with writer.saving(fig, "spin_map_32x32.gif", dpi=120):
    for i, theta in enumerate(theta_configs):
        T = theta_temperatures[i]
        ax.clear()
        U = np.cos(theta)
        V = np.sin(theta)
        ax.quiver(X, Y, U, V, pivot='middle', scale=30, color='black')

        # filtriraj vrtloge za trenutan T
        T_rounded = round(T, 2)
        mask = np.isclose(vortex_data['T'], T_rounded, atol=1e-3)
        vortices_T = vortex_data[mask]
        has_vortex = len(vortices_T) > 0

        for vortex in vortices_T:
            x, y = vortex['x'] - 1, vortex['y'] - 1
            charge = vortex['charge']
            symbol = '\u21BA' if charge == 1 else '\u21BB'
            color = 'red' if charge == 1 else 'blue'
            ax.text(x, y, symbol, color=color, fontsize=18, ha='center', va='center', zorder=5)

        ax.set_title(f'Kosterlitz-Thouless 2D spin system, $L={grid_size}, T = {T:.2f}$')
        ax.set_xlim(-1, grid_size)
        ax.set_ylim(-1, grid_size)
        ax.set_aspect('equal')
        ax.axis('off')
        writer.grab_frame()
