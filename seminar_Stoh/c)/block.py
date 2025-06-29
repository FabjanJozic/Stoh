import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fE32_50 = np.loadtxt('energy_32x32_Nbskip50.dat', comments='#', usecols=1)
    fE64 = np.loadtxt('energy_64x64.dat', comments='#', usecols=1)

fstdev32 = open('blocking_stdev_32x32_Nbskip50.dat', 'w')
fstdev64 = open('blocking_stdev_64x64.dat', 'w')

fstdev32.write('# ib - <E>b - stdev\n')
fstdev64.write('# ib - <E>b - stdev\n')

Nbmax = 1000

E32 = fE32_50[2050:]
E64 = fE64[2050:]
N = len(E32)

for Nk in range(1, Nbmax+1):
    Nb = N//Nk
    if Nb <= 2:
        continue
    Sfb, Sf2b = 0.0, 0.0
    for b in range(Nb):
        block = E64[b*Nk : (b+1)*Nk]
        Sfk = np.sum(block)
        Sfb += Sfk/Nk
        Sf2b += (Sfk*Sfk)/(Nk*Nk)
    Smb = Sfb/Nb
    var = ((Sf2b/Nb)-Smb**2)/(Nb-1)
    fstdev32.write(f"{Nk:<5d} {Smb:>13.9f} {np.sqrt(var):>12.9f}\n")
    
fstdev32.close()
fstdev64.close()

fo = np.loadtxt('blocking_stdev_64x64.dat')
bl , dev = [], []

for i in range(len(fo)):
    bl.append(fo[i, 0])
    dev.append(1000*fo[i, 2])

mdev = f"{np.mean(dev)/1000:<7.5f}"

fig = plt.figure(figsize=(8,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 14}) #type: ignore
ax.plot(bl, dev, color='blue', lw=1.7)
ax.set_xlim(0, Nbmax)
ax.set_ylim(0.0, 1.5)
ax.set_xlabel('block')
ax.set_ylabel('$10^{3} \u03C3_{E}$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(50))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.grid(lw=0.2, linestyle=':')
ax.text(20, 1.35, s=r'$\langle\sigma\rangle_{}$={} a.u.'.format('E', mdev))
plt.show()