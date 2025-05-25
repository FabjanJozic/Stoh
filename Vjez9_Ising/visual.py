import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

'''f4 = np.loadtxt('f_TCxEM_4x4.dat', comments='#', usecols=(0,1,2))
f8 = np.loadtxt('f_TCxEM_8x8.dat', comments='#', usecols=(0,1,2))
f16 = np.loadtxt('f_TCxEM_16x16.dat', comments='#', usecols=(0,1,2))

kT, x4, x8, x16, C4, C8, C16 = [], [], [], [], [], [], []

for i in range(len(f4)):
    kT.append(f4[i, 0])
    C4.append(f4[i, 1])
    x4.append(f4[i, 2])
    C8.append(f8[i, 1])
    x8.append(f8[i, 2])
    C16.append(f16[i, 1])
    x16.append(f16[i, 2])
    
fig = plt.figure(figsize=(7,6), dpi=110)
ax = fig.add_axes([0.15, 0.15, 0.80, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.scatter(kT, C4, color='red', s=10, label='L=4')
ax.scatter(kT, C8, color='purple', s=10, label='L=8')
ax.scatter(kT, C16, color='blue', s=10, label='L=16')
ax.plot(kT, C4, color='red', lw=0.5, linestyle='--')
ax.plot(kT, C8, color='purple', lw=0.5, linestyle='--')
ax.plot(kT, C16, color='blue', lw=0.5, linestyle='--')
ax.set_xlim(0.8, 4.2)
ax.set_ylim(0.0, 1.5)
ax.set_xlabel('T / K')
ax.set_ylabel('C$_{V}$ / k$_{B}$')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.2))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.grid(lw=0.2, linestyle=':')
ax.legend(loc='upper right')
ax.set_title('2D Isingov model spinova: toplinski kapacitet po čestici')
plt.show()

fig = plt.figure(figsize=(7,6), dpi=110)
ax = fig.add_axes([0.15, 0.15, 0.80, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.scatter(kT, x4, color='red', s=10, label='L=4')
ax.scatter(kT, x8, color='purple', s=10, label='L=8')
ax.scatter(kT, x16, color='blue', s=10, label='L=16')
ax.plot(kT, x4, color='red', lw=0.5, linestyle='--')
ax.plot(kT, x8, color='purple', lw=0.5, linestyle='--')
ax.plot(kT, x16, color='blue', lw=0.5, linestyle='--')
ax.set_xlim(0.8, 4.2)
ax.set_ylim(0.0, 44.0)
ax.set_xlabel('T / K')
ax.set_ylabel('$\u03C7$')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.2))
ax.yaxis.set_major_locator(tick.MultipleLocator(2.0))
ax.grid(lw=0.2, linestyle=':')
ax.legend(loc='upper right')
ax.set_title('2D Isingov model spinova: magnetska susceptibilnost po čestici')
plt.show()'''


fEM4 = np.loadtxt('f_TCxEM_4x4.dat', comments='#', usecols=(0,3,4))
fEM8 = np.loadtxt('f_TCxEM_8x8.dat', comments='#', usecols=(0,3,4))
fEM16 = np.loadtxt('f_TCxEM_16x16.dat', comments='#', usecols=(0,3,4))

kT, E4, E8, E16, M4, M8, M16 = [], [], [], [], [], [], []

for i in range(len(fEM4)):
    kT.append(fEM4[i, 0])
    E4.append(fEM4[i, 1])
    M4.append(fEM4[i, 2])
    E8.append(fEM8[i, 1])
    M8.append(fEM8[i, 2])
    E16.append(fEM16[i, 1])
    M16.append(fEM16[i, 2])
    
fig = plt.figure(figsize=(7,6), dpi=110)
ax = fig.add_axes([0.15, 0.15, 0.80, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.scatter(kT, E4, color='red', s=10, label='L=4')
ax.scatter(kT, E8, color='purple', s=10, label='L=8')
ax.scatter(kT, E16, color='blue', s=10, label='L=16')
ax.plot(kT, E4, color='red', lw=0.5, linestyle='--')
ax.plot(kT, E8, color='purple', lw=0.5, linestyle='--')
ax.plot(kT, E16, color='blue', lw=0.5, linestyle='--')
ax.set_xlim(0.8, 4.2)
ax.set_ylim(-2.1, -0.5)
ax.set_xlabel('T / K')
ax.set_ylabel(r'$\dfrac{<E>}{N}$')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.2))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.grid(lw=0.2, linestyle=':')
ax.legend(loc='upper left')
ax.set_title('2D Isingov model spinova: srednja energija po čestici')
plt.show()

fig = plt.figure(figsize=(7,6), dpi=110)
ax = fig.add_axes([0.15, 0.15, 0.80, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.scatter(kT, M4, color='red', s=10, label='L=4')
ax.scatter(kT, M8, color='purple', s=10, label='L=8')
ax.scatter(kT, M16, color='blue', s=10, label='L=16')
ax.plot(kT, M4, color='red', lw=0.5, linestyle='--')
ax.plot(kT, M8, color='purple', lw=0.5, linestyle='--')
ax.plot(kT, M16, color='blue', lw=0.5, linestyle='--')
ax.set_xlim(0.8, 4.2)
ax.set_ylim(-0.4, 1.1)
ax.set_xlabel('T / K')
ax.set_ylabel(r'$\dfrac{<M>}{N}$')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.2))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.grid(lw=0.2, linestyle=':')
ax.legend(loc='upper right')
ax.set_title('2D Isingov model spinova: srednja magnetizacija po čestici')
plt.show()