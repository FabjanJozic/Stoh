import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import matplotlib.ticker as tick

'''rf = np.loadtxt('rNw_H300.dat', comments='#')

Nw = 10000  #broj setaca
steps = len(rf)//Nw

fig = plt.figure(figsize=(7, 7), dpi=120)
metadata = dict(title="Hydrogen Atom Walkers", artist="Me")
writer = PillowWriter(fps=10, metadata=metadata)

with writer.saving(fig, "H_300.gif", dpi=120):
    for i in range(1, steps):
        plt.clf()
        plt.rcParams.update({'font.size': 15}) #type: ignore
        ax = fig.add_subplot(111, projection='3d')
        ax.view_init(elev=6, azim=145)
        walkers = rf[i*Nw:(i+1)*Nw]
        x = walkers[:, 1]
        y = walkers[:, 2]
        z = walkers[:, 3]
        ax.set_aspect('equal')
        ax.scatter(x, y, z, c='blue', s=1)
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        ax.set_zlim(-20, 20)
        ax.set_xlabel('x / a$_{0}$')
        ax.set_ylabel('y / a$_{0}$')
        ax.set_zlabel('z / a$_{0}$')
        ax.invert_yaxis()
        ax.invert_xaxis()
        ax.text(x=-20, y=-22, z=30, s=f"$\u03A8_{'H'}$(r)=|3,0,0>")
        ax.text(x=-20, y=-22, z=26, s="N$_{W}$=10000")
        ax.text(x=-22, y=25, z=26, s="t={} $\u0394$t".format(int(walkers[0,0])))
        plt.tight_layout()
        writer.grab_frame()'''
        
rfr = np.loadtxt('r_H300.dat', comments='#')
block, r, rb = [], [], []
for _ in range(len(rfr)):
    val1, val2, val3 = rfr[_]
    block.append(val1)
    r.append(val3)
    rb.append(val2)

fig = plt.figure(figsize=(11,4), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(block, rb, color='lime', lw=1.0, label='<r>$_{b}$')
ax.plot(block, r, color='blue', lw=1.0, label='<r>')
ax.set_xlim(0, 200)
ax.set_ylim(13.46, 13.55)
ax.set_xlabel('t / 500 $\u0394$t')
ax.set_ylabel('<r> / a$_{0}$')
ax.xaxis.set_major_locator(tick.MultipleLocator(20))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.01))
ax.text(x=3, y=13.54, s=f"N$_{'W'}$=10000, N$_{'b'}^{'-'}$=50, N$_{'b'}$=200, N$_{'k'}$=500")
ax.legend(loc='upper right')
plt.show()

