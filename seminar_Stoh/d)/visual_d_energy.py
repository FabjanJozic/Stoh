import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

fE32 = np.loadtxt('energy_32x32.dat', comments='#')

ib, Eb, Ec = [], [], []
for i in range(len(fE32)):
    ib.append(fE32[i, 0])
    Eb.append(fE32[i, 2])
    Ec.append(fE32[i, 3])
    
# prikaz energije samo za T=0.9
ib = ib[3204:4005]
Eb = Eb[3204:4005]
Ec = Ec[3204:4005]

fig = plt.figure(figsize=(12,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 13}) #type: ignore
ax.plot(ib, Eb, color='orange', lw=1.1, linestyle='--', zorder=0, label=r'$\langle E \rangle_{b}$')
ax.plot(ib, Ec, color='red', lw=1.5, zorder=2, label=r'$\langle E \rangle$')
ax.set_xlim(41900, 50100)
ax.set_ylim(-1.53, -1.29)
ax.set_xlabel('block')
ax.set_ylabel('$E$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(500))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.025))
ax.grid(lw=0.2, linestyle=':')
ax.legend(loc='upper right')
plt.show()