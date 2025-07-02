import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fE32 = np.loadtxt('energy_32x32.dat', comments='#', usecols=2)

fstdev32 = open('blocking_stdev_32x32.dat', 'w')

fstdev32.write('# ib - <E>b - stdev\n')

Nbmax = 200

E32 = fE32[3204:4005]
N = len(E32)

for Nk in range(1, Nbmax+1):
    Nb = N//Nk
    if Nb <= 2:
        continue
    Sfb, Sf2b = 0.0, 0.0
    for b in range(Nb):
        block = E32[b*Nk : (b+1)*Nk]
        Sfk = np.sum(block)
        Sfb += Sfk/Nk
        Sf2b += (Sfk*Sfk)/(Nk*Nk)
    Smb = Sfb/Nb
    var = ((Sf2b/Nb)-Smb**2)/(Nb-1)
    fstdev32.write(f"{Nk:<5d} {Smb:>13.9f} {np.sqrt(var):>12.9f}\n")
    
fstdev32.close()

fo = np.loadtxt('blocking_stdev_32x32.dat')
bl , dev = [], []

for i in range(len(fo)):
    bl.append(fo[i, 0])
    dev.append(1000*fo[i, 2])

mdev = f"{np.mean(dev)/Nbmax:<7.5f}"

fig = plt.figure(figsize=(8,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 14}) #type: ignore
ax.plot(bl, dev, color='blue', lw=1.7)
ax.set_xlim(0, Nbmax)
ax.set_ylim(0.18, 1.62)
ax.set_xlabel('block')
ax.set_ylabel('$10^{3} \u03C3_{E}$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(20))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.2))
ax.grid(lw=0.2, linestyle=':')
ax.text(5, 1.4, s=r'$\langle\sigma\rangle_{}$={} a.u.'.format('E', mdev)+'\n$T = 0.9$ K, $L = 32$')
plt.show()