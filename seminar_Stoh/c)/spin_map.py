import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import re

# ucitavanje mape spinova
theta_file = 'theta_map_32x32_Nbskip50.dat'
with open(theta_file, 'r') as f:
    raw_lines = f.readlines()

# parsiranje konfiguracija i pravih ib indeksa
theta_configs = []
theta_indices = []
current_config = []
current_ib = None

for line in raw_lines:
    if line.startswith('#'):
        if current_config and current_ib is not None:
            theta_configs.append(np.array(current_config))
            theta_indices.append(current_ib)
            current_config = []
        match = re.search(r'\b(\d+)\b', line) # uzimanje ib vrijednosti
        if match:
            current_ib = int(match.group(1))
        else:
            current_ib = None  
    else:
        current_config.append([float(val) for val in line.strip().split()])
if current_config and current_ib is not None:
    theta_configs.append(np.array(current_config))
    theta_indices.append(current_ib)

# ucitavanje informacija o vrtlozima i antivrtlozima
vortex_data = np.genfromtxt('vortices_all_per_sim_32x32_Nbskip50.dat', comments='#',
    dtype=[('x', 'i4'), ('y', 'i4'), ('charge', 'i4'), ('ib', 'i4')], delimiter=None)

# podesavanje mreze
grid_size = 32
X, Y = np.meshgrid(np.arange(grid_size), np.arange(grid_size))

# stvaranje GIFa
fig, ax = plt.subplots(figsize=(6, 6))
metadata = dict(title="Theta Field with Vortices", artist="Matplotlib")
writer = PillowWriter(fps=10, metadata=metadata)

repeat_if_vortex = 2  # produzenje framea kada ima vrtloga

with writer.saving(fig, "spin_map_32x32.gif", dpi=120):
    for i, theta in enumerate(theta_configs):
        ib = theta_indices[i]
        ax.clear()
        U = np.cos(theta)
        V = np.sin(theta)
        ax.quiver(X, Y, U, V, pivot='middle', scale=30, color='black')

        # filtriraj vrtloge za stvarni ib
        ib_vortices = vortex_data[vortex_data['ib'] == ib]
        has_vortex = len(ib_vortices) > 0

        for vortex in ib_vortices:
            x, y = vortex['x'] - 1, vortex['y'] - 1
            charge = vortex['charge']
            symbol = '\u21BA' if charge == 1 else '\u21BB'
            color = 'red' if charge == 1 else 'blue'
            ax.text(x, y, symbol, color=color, fontsize=18, ha='center', va='center', zorder=5)

        ax.set_title(f'Kosterlitz-Thouless 2D spin system, $L = 32$, $ib = {ib}$')
        ax.set_xlim(-1, grid_size)
        ax.set_ylim(-1, grid_size)
        ax.set_aspect('equal')
        ax.axis('off')

        repeat = repeat_if_vortex if has_vortex else 1
        for _ in range(repeat):
            writer.grab_frame()
