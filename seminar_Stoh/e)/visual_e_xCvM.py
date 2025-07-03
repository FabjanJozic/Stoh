import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

fx128 = np.loadtxt('T_x_Cv_M_128x128.dat', comments='#')
fx192 = np.loadtxt('T_x_Cv_M_192x192.dat', comments='#')
fx256 = np.loadtxt('T_x_Cv_M_256x256.dat', comments='#')

T = []
x_scal128, x_vec128, x_scal192, x_vec192, x_scal256, x_vec256 = [], [], [], [], [], []
Cv128, Cv192, Cv256, M128, M192, M256 = [], [], [], [], [], []

for i in range(len(fx128)):
    T.append(fx128[i, 0])
    x_scal128.append(fx128[i, 1])
    x_vec128.append(fx128[i, 2])
    Cv128.append(fx128[i, 3])
    M128.append(fx128[i, 4])
    x_scal192.append(fx192[i, 1])
    x_vec192.append(fx192[i, 2])
    Cv192.append(fx192[i, 3])
    M192.append(fx192[i, 4])
    x_scal256.append(fx256[i, 1])
    x_vec256.append(fx256[i, 2])
    Cv256.append(fx256[i, 3])
    M256.append(fx256[i, 4])
    
# magnetska susceptibilnost
'''fig = plt.figure(figsize=(10,6), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(T, x_scal128, color='cyan', lw=0.8, linestyle='--', zorder=0)
ax.plot(T, x_scal192, color='blue', lw=0.8, linestyle='--', zorder=1)
ax.plot(T, x_scal256, color='navy', lw=0.8, linestyle='--', zorder=2)
ax.plot(T, x_vec128, color='coral', lw=0.8, linestyle='--', zorder=3)
ax.plot(T, x_vec192, color='red', lw=0.8, linestyle='--', zorder=4)
ax.plot(T, x_vec256, color='firebrick', lw=0.8, linestyle='--', zorder=5)
ax.scatter(T, x_scal128, color='cyan', s=25, marker='D', label='scalar, $L = 128$', zorder=6)
ax.scatter(T, x_scal192, color='blue', s=25, marker='D', label='scalar, $L = 192$', zorder=7)
ax.scatter(T, x_scal256, color='navy', s=25, marker='D', label='scalar, $L = 256$', zorder=8)
ax.scatter(T, x_vec128, color='coral', s=25, marker='s', label='vector, $L = 128$', zorder=9)
ax.scatter(T, x_vec192, color='red', s=25, marker='s', label='vector, $L = 192$', zorder=10)
ax.scatter(T, x_vec256, color='firebrick', s=25, marker='s', label='vector, $L = 256$', zorder=11)
ax.set_xlim(0.995, 1.205)
ax.set_ylim(-25, 825)
ax.set_xlabel('$T$ / K')
ax.set_ylabel('$\u03C7$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.01))
ax.yaxis.set_major_locator(tick.MultipleLocator(50))
ax.legend(loc='best')
ax.grid(lw=0.2, linestyle=':')
plt.show()'''

# specificni toplinski kapacitet
'''fig = plt.figure(figsize=(10,6), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(T, Cv128, color='mediumaquamarine', lw=0.8, linestyle='--', zorder=0)
ax.plot(T, Cv192, color='limegreen', lw=0.8, linestyle='--', zorder=1)
ax.plot(T, Cv256, color='darkgreen', lw=0.8, linestyle='--', zorder=2)
ax.scatter(T, Cv128, color='mediumaquamarine', s=25, marker='s', label='$L = 128$', zorder=4)
ax.scatter(T, Cv192, color='limegreen', s=25, marker='D', label='$L = 192$', zorder=5)
ax.scatter(T, Cv256, color='darkgreen', s=25, marker='h', label='$L = 256$', zorder=6)
ax.set_xlim(0.995, 1.205)
ax.set_ylim(1.05, 2.65)
ax.set_xlabel('$T$ / K')
ax.set_ylabel('$C_{V}$ / k$_{B}$')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.01))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.legend(loc='best')
ax.grid(lw=0.2, linestyle=':')
plt.show()'''

# srednja magnetizacija
'''fig = plt.figure(figsize=(10,6), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(T, M128, color='cyan', lw=0.8, linestyle='--', zorder=0)
ax.plot(T, M192, color='blue', lw=0.8, linestyle='--', zorder=1)
ax.plot(T, M256, color='navy', lw=0.8, linestyle='--', zorder=2)
ax.scatter(T, M128, color='cyan', s=25, marker='s', label='$L = 128$', zorder=4)
ax.scatter(T, M192, color='blue', s=25, marker='D', label='$L = 192$', zorder=5)
ax.scatter(T, M256, color='navy', s=25, marker='h', label='$L = 256$', zorder=6)
ax.set_xlim(0.995, 1.205)
ax.set_ylim(0.01, 0.31)
ax.set_xlabel('$T$ / K')
ax.set_ylabel(r'$\langle M \rangle$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.01))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.02))
ax.legend(loc='best')
ax.grid(lw=0.2, linestyle=':')
plt.show()'''