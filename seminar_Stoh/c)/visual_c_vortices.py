import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fv32_50 = np.loadtxt('mean_vortices_all_sim_32x32_Nbskip50.dat', comments='#', usecols=[0, 3, 4])
    fv32_150 = np.loadtxt('mean_vortices_all_sim_32x32_Nbskip150.dat', comments='#', usecols=[0, 3, 4])
    fv64 = np.loadtxt('mean_vortices_all_sim_64x64.dat', comments='#', usecols=[0, 3, 4])

isim = []
vor32_50, vor32_150, vor64, avor32_50, avor32_150, avor64 = [], [], [], [], [], []

for i in range(len(fv32_50)):
    isim.append(fv32_50[i, 0])
    vor32_50.append(fv32_50[i, 1])
    avor32_50.append(fv32_50[i, 2])
    vor32_150.append(fv32_150[i, 1])
    avor32_150.append(fv32_150[i, 2])
    vor64.append(fv64[i, 1])
    avor64.append(fv64[i, 2])


# sustav 32*32 spina za Nb_skip=50 i Nb_skip=150
fig = plt.figure(figsize=(12,6), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(isim, vor32_50, color='red', lw=0.2, linestyle='--', zorder=0)
ax.plot(isim, avor32_50, color='blue', lw=0.2, linestyle='--', zorder=1)
ax.plot(isim, vor64, color='brown', lw=0.2, linestyle='--', zorder=2)
ax.plot(isim, avor64, color='purple', lw=0.2, linestyle='--', zorder=3)
ax.scatter(isim, vor32_50, color='red', s=40, marker='d', label='vortex, $L = 32$', zorder=4)
ax.scatter(isim, avor32_50, color='blue', s=20, marker='s', label='antivortex, $L = 32$', zorder=5)
ax.scatter(isim, vor64, color='brown', s=40, marker='d', label='vortex, $L = 64$', zorder=6)
ax.scatter(isim, vor64, color='purple', s=20, marker='s', label='antivortex, $L = 64$', zorder=7)
ax.set_xlim(0, 101)
ax.set_ylim(-200, 10200)
ax.set_xlabel('simulation')
ax.set_ylabel('number of vortices')
ax.xaxis.set_major_locator(tick.MultipleLocator(5))
ax.yaxis.set_major_locator(tick.MultipleLocator(1000))
ax.legend(loc='best')
plt.show()