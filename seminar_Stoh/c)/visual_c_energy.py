import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

fE32_50 = np.loadtxt('energy_32x32_Nbskip50.dat', comments='#')
fE32_150 = np.loadtxt('energy_32x32_Nbskip150.dat', comments='#')
fE64 = np.loadtxt('energy_64x64.dat', comments='#')

ib = []
Eb32_50, Ec32_50, Eb32_150, Ec32_150, Eb64, Ec64 = [], [], [], [], [], []

for i in range(len(fE32_50)):
    if i >= 2050:
        ib.append(fE32_50[i, 0])
        Eb32_50.append(fE32_50[i, 1])
        Ec32_50.append(fE32_50[i, 2])
        Eb32_150.append(fE32_150[i, 1])
        Ec32_150.append(fE32_150[i, 2])
        Eb64.append(fE64[i, 1])
        Ec64.append(fE64[i, 2])

# sustava 32*32 spina za Nb_skip=50 sve
'''fig = plt.figure(figsize=(12,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 13}) #type: ignore
ax.plot(ib, Eb32_50, color='lime', lw=1.1, linestyle='--', zorder=0, label=r'$\langle E \rangle_{b}$')
ax.plot(ib, Ec32_50, color='green', lw=1.1, zorder=2, label=r'$\langle E \rangle$')
ax.set_xlim(950, 11100)
ax.set_ylim(-1.81, 0.01)
ax.set_xlabel('block')
ax.set_ylabel('$E$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(500))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.2))
ax.grid(lw=0.2, linestyle=':')
ax.legend(loc='upper right')
plt.show()'''

# sustava 32*32 spina za Nb_skip=50
'''fig = plt.figure(figsize=(12,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 13}) #type: ignore
ax.plot(ib, Eb32_50, color='lime', lw=1.1, linestyle='--', zorder=0, label=r'$\langle E \rangle_{b}$')
ax.plot(ib, Ec32_50, color='green', lw=1.1, zorder=2, label=r'$\langle E \rangle$')
ax.set_xlim(3000, 11100)
ax.set_ylim(-1.78, -1.65)
ax.set_xlabel('block')
ax.set_ylabel('$E$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(500))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.01))
ax.grid(lw=0.2, linestyle=':')
ax.legend(loc='upper right')
plt.show()'''

# sustava 64*64 spina
'''fig = plt.figure(figsize=(12,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 13}) #type: ignore
ax.plot(ib, Eb64, color='cyan', lw=1.1, linestyle='--', zorder=0, label=r'$\langle E \rangle_{b}$')
ax.plot(ib, Ec64, color='blue', lw=1.1, zorder=2, label=r'$\langle E \rangle$')
ax.set_xlim(3000, 11100)
ax.set_ylim(-1.76, -1.68)
ax.set_xlabel('block')
ax.set_ylabel('$E$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(500))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.01))
ax.grid(lw=0.2, linestyle=':')
ax.legend(loc='upper right')
plt.show()'''

# usporedba sustava 32*32 spina za Nb_skip=50 i Nb_skip=150
'''fig = plt.figure(figsize=(12,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(ib, Ec32_50, color='green', lw=1.3, zorder=2, label='$Nb^{+} = 50$')
ax.plot(ib, Ec32_150, color='red', lw=1.3, zorder=3, label='$Nb^{+} = 150$')
ax.set_xlim(3000, 11200)
ax.set_ylim(-1.73, -1.675)
ax.set_xlabel('block')
ax.set_ylabel(r'$\langle E \rangle$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(500))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.005))
ax.grid(lw=0.2, linestyle=':')
ax.legend(loc='upper right')
plt.show()'''




