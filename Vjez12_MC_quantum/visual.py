import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

# ovisnost energije o varijacijskom parametru
'''falpha = np.loadtxt('E_alpha.dat', comments='#')

alpha, mE, sigma_E = [], [], []
for i in range(len(falpha)):
    alpha.append(falpha[i, 0])
    mE.append(falpha[i, 1])
    sigma_E.append(1000*falpha[i,2])

fig = plt.figure(figsize=(10,6), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.errorbar(alpha, mE, yerr=sigma_E, fmt='o-', capsize=4, label=r'$\langle E\rangle \pm 10^{3}\sigma_{E}$',
            ecolor='green', elinewidth=0.4, mfc='lime', mec='green', ms=5, mew=1)
ax.set_xlim(0.04, 1.01)
ax.set_ylim(1.05, 2.35)
ax.set_xlabel('$\u03B1$ / $\AA^{-2}$')
ax.set_ylabel('$E$ / eV')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.05))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.grid(lw=0.2, linestyle=':')
ax.set_title('Graf ovisnosti energije osnovnog stanja o varijacijskom parametru $\u03B1$')
ax.legend(loc='upper right')
plt.show()'''

# ravnotezno uzorkovanje
fE = np.loadtxt('energy.dat', comments='#')

ib, Eb, Ec = [], [], []
for i in range(len(fE)):
    ib.append(fE[i, 0])
    Eb.append(fE[i, 1])
    Ec.append(fE[i,2])
    
fig = plt.figure(figsize=(12,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(ib, Eb, lw=1.0, color='lime', label=r'$\langle E_{b}\rangle$', zorder=0)
ax.plot(ib, Ec, lw=1.5, color='darkgreen', label=r'$\langle E\rangle$', zorder=1)
ax.set_xlim(0, 401)
ax.set_ylim(1.1711, 1.1743)
ax.set_xlabel('block')
ax.set_ylabel('$E$ / eV')
ax.xaxis.set_major_locator(tick.MultipleLocator(40))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.0003))
ax.grid(lw=0.2, linestyle=':')
ax.set_title('Evolucija energije osnovnog stanja za $\u03B1$=0.25')
ax.legend(loc='upper right')
ax.text(10, 1.1740, f'$E=({np.mean(Ec):.4f} \pm {1.6991112781954888e-05:.4e})$ eV')
plt.show()