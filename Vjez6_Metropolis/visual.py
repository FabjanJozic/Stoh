import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

rf = np.loadtxt('rNw_H210.dat', comments='#')

Nw = 2000  #broj setaca
steps = len(rf)//Nw

fig = plt.figure(figsize=(7, 7), dpi=120)
metadata = dict(title="Hydrogen Atom Walkers", artist="Me")
writer = PillowWriter(fps=5, metadata=metadata)

with writer.saving(fig, "H_210.gif", dpi=120):
    for i in range(1, steps):
        if i%10 == 0:
            plt.clf()
            plt.rcParams.update({'font.size': 15}) #type: ignore
            ax = fig.add_subplot(111, projection='3d')
            ax.view_init(elev=6, azim=145)
            walkers = rf[i*Nw:(i+1)*Nw]
            x = walkers[:, 1]
            y = walkers[:, 2]
            z = walkers[:, 3]
            ax.set_aspect('equal')
            ax.scatter(x, y, z, c='blue', s=2)
            ax.set_xlim(-8, 8)
            ax.set_ylim(-8, 8)
            ax.set_zlim(-15, 15)
            ax.set_xlabel('x / a$_{0}$')
            ax.set_ylabel('y / a$_{0}$')
            ax.set_zlabel('z / a$_{0}$')
            ax.invert_yaxis()
            ax.invert_xaxis()
            ax.text(x=-8, y=-9, z=20, s=f"$\u03A8_{'H'}$(r,t)=|2,1,0>")
            ax.text(x=-8, y=-9, z=17, s="N$_{W}$=2000, N$_{b}$=200, N$_{k}$=150")
            ax.text(x=-9, y=10, z=17, s="t={} $\u0394$t".format(int(walkers[0,0])))
            plt.tight_layout()
            writer.grab_frame()
