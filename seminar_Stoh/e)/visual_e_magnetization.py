import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

fM128 = np.loadtxt('magnetization_128x128.dat', comments='#')

ib, Mb, Mc = [], [], []
for i in range(len(fM128)):
    ib.append(fM128[i, 0])
    Mb.append(fM128[i, 2])
    Mc.append(fM128[i, 3])
    
# prikaz energije samo za T=0.9
ib = ib[3204:4005]
Mb = Mb[3204:4005]
Mc = Mc[3204:4005]

fig = plt.figure(figsize=(12,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 13}) #type: ignore
ax.plot(ib, Mb, color='orange', lw=1.1, linestyle='--', zorder=0, label=r'$\langle M \rangle_{b}$')
ax.plot(ib, Mc, color='red', lw=1.5, zorder=2, label=r'$\langle M \rangle$')
ax.set_xlim(41900, 50100)
ax.set_ylim(-0.025, 0.375)
ax.set_xlabel('block')
ax.set_ylabel('$M$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(500))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.05))
ax.grid(lw=0.2, linestyle=':')
ax.legend(loc='upper right')
plt.show()