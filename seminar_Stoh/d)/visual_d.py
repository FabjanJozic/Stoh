import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

fL8 = np.loadtxt('temp_ene_Cv_vor_antivor_8x8.dat', comments='#')
fL16 = np.loadtxt('temp_ene_Cv_vor_antivor_16x16.dat', comments='#')
fL32 = np.loadtxt('temp_ene_Cv_vor_antivor_32x32.dat', comments='#')
fL64 = np.loadtxt('temp_ene_Cv_vor_antivor_64x64.dat', comments='#')

T = []
E8, E16, E32, E64 = [], [], [], []
Cv8, Cv16, Cv32, Cv64 = [], [], [], []
mvor8, mvor16, mvor32, mvor64 = [] ,[], [], []

for i in range(len(fL8)):
    T.append(fL8[i, 0])
    E8.append(fL8[i, 1])
    E16.append(fL16[i, 1])
    E32.append(fL32[i, 1])
    E64.append(fL64[i, 1])
    Cv8.append(fL8[i, 2])
    Cv16.append(fL16[i, 2])
    Cv32.append(fL32[i, 2])
    Cv64.append(fL64[i, 2])
    mvor8.append(fL8[i, 5])
    mvor16.append(fL16[i, 5])
    mvor32.append(fL32[i, 5])
    mvor64.append(fL64[i ,5])
    
# ovisnost <E> o T
'''fig = plt.figure(figsize=(10,6), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(T, E8, color='blue', lw=0.8, linestyle='--', zorder=0)
ax.plot(T, E16, color='cyan', lw=0.8, linestyle='--', zorder=1)
ax.plot(T, E32, color='lime', lw=0.8, linestyle='--', zorder=2)
ax.plot(T, E64, color='green', lw=0.8, linestyle='--', zorder=3)
ax.scatter(T, E8, color='blue', s=25, marker='s', label='$L = 8$', zorder=4)
ax.scatter(T, E16, color='cyan', s=25, marker='D', label='$L = 16$', zorder=5)
ax.scatter(T, E32, color='lime', s=25, marker='h', label='$L = 32$', zorder=6)
ax.scatter(T, E64, color='green', s=25, marker='o', label='$L = 64$', zorder=7)
ax.set_xlim(0.45, 1.55)
ax.set_ylim(-1.75, -0.75)
ax.set_xlabel('$T$ / K')
ax.set_ylabel(r'$\langle E \rangle$ / a.u.')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.legend(loc='best')
ax.grid(lw=0.2, linestyle=':')
plt.show()'''

# ovisnost Cv o T
'''fig = plt.figure(figsize=(10,6), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(T, Cv8, color='blue', lw=0.8, linestyle='--', zorder=0)
ax.plot(T, Cv16, color='cyan', lw=0.8, linestyle='--', zorder=1)
ax.plot(T, Cv32, color='lime', lw=0.8, linestyle='--', zorder=2)
ax.plot(T, Cv64, color='green', lw=0.8, linestyle='--', zorder=3)
ax.scatter(T, Cv8, color='blue', s=25, marker='s', label='$L = 8$', zorder=4)
ax.scatter(T, Cv16, color='cyan', s=25, marker='D', label='$L = 16$', zorder=5)
ax.scatter(T, Cv32, color='lime', s=25, marker='h', label='$L = 32$', zorder=6)
ax.scatter(T, Cv64, color='green', s=25, marker='o', label='$L = 64$', zorder=7)
ax.set_xlim(0.45, 1.55)
ax.set_ylim(0.45, 1.55)
ax.set_xlabel('$T$ / K')
ax.set_ylabel('$C_{V}$ / k$_{B}$')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.legend(loc='best')
ax.grid(lw=0.2, linestyle=':')
plt.show()'''

#ovisnost N_vor i N_antivor o T
'''fig = plt.figure(figsize=(8,6), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(T, mvor8, color='blue', lw=0.8, linestyle='--', zorder=0)
ax.plot(T, mvor16, color='cyan', lw=0.8, linestyle='--', zorder=1)
ax.plot(T, mvor32, color='lime', lw=0.8, linestyle='--', zorder=2)
ax.plot(T, mvor64, color='green', lw=0.8, linestyle='--', zorder=3)
ax.scatter(T, mvor8, color='blue', s=25, marker='s', label='$L = 8$', zorder=4)
ax.scatter(T, mvor16, color='cyan', s=25, marker='D', label='$L = 16$', zorder=5)
ax.scatter(T, mvor32, color='lime', s=25, marker='h', label='$L = 32$', zorder=6)
ax.scatter(T, mvor64, color='green', s=25, marker='o', label='$L = 64$', zorder=7)
ax.set_xlim(0.45, 1.55)
ax.set_ylim(-50, 650)
ax.set_xlabel('$T$ / K')
ax.set_ylabel('number of vortices')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.yaxis.set_major_locator(tick.MultipleLocator(100))
ax.legend(loc='best')
ax.grid(lw=0.2, linestyle=':')
plt.show()'''

#ovisnost ln(N_vor) o T
ln8 = [np.log(n) for n in mvor8]
ln16 = [np.log(n) for n in mvor16]
ln32 = [np.log(n) for n in mvor32]
ln64 = [np.log(n) for n in mvor64]

T = T[:7]
ln8 = ln8[:7]
ln16 = ln16[:7]
ln32 = ln32[:7]
ln64 = ln64[:7]

fig = plt.figure(figsize=(8,6), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(T, ln8, color='blue', lw=0.8, linestyle='--', zorder=0)
ax.plot(T, ln16, color='cyan', lw=0.8, linestyle='--', zorder=1)
ax.plot(T, ln32, color='lime', lw=0.8, linestyle='--', zorder=2)
ax.plot(T, ln64, color='green', lw=0.8, linestyle='--', zorder=3)
ax.scatter(T, ln8, color='blue', s=25, marker='s', label='$L = 8$', zorder=4)
ax.scatter(T, ln16, color='cyan', s=25, marker='D', label='$L = 16$', zorder=5)
ax.scatter(T, ln32, color='lime', s=25, marker='h', label='$L = 32$', zorder=6)
ax.scatter(T, ln64, color='green', s=25, marker='o', label='$L = 64$', zorder=7)
ax.set_xlim(0.45, 1.15)
ax.set_ylim(-3.6, 5.6)
ax.set_xlabel('$T$ / K')
ax.set_ylabel('ln($N_{vortex}$)')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.yaxis.set_major_locator(tick.MultipleLocator(1))
ax.legend(loc='best')
ax.grid(lw=0.2, linestyle=':')
plt.show()