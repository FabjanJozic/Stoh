import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

fE = np.loadtxt('E.dat')
fRDF = np.loadtxt('RDF.dat')

ib, Ek, Eb = [], [], []
r, gr = [], []

for i in range(len(fE)):
    ib.append(fE[i, 0])
    Ek.append(fE[i, 1])
    Eb.append(fE[i, 2])
    
for j in range(len(fRDF)):
    r.append(fRDF[j, 0])
    gr.append(fRDF[j, 1])
    
#kod za plot energije
'''fig = plt.figure(figsize=(10,4), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.plot(ib, Ek, color='lime', lw=1.0, label='<E$_{b}$>')
ax.plot(ib, Eb, color='blue', lw=1.0, label='<E$_{u}$>')
ax.set_xlim(150, 601+150)
ax.set_ylim(-751.6, -751.0)
ax.set_xlabel('block')
ax.set_ylabel('<E> / $\u03B5$')
ax.xaxis.set_major_locator(tick.MultipleLocator(50))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.text(x=160, y=-751.05, s=f"N$_{'W'}$=10, N$_{'b'}^{'+'}$=150, N$_{'b'}$=600, N$_{'k'}$=250")
ax.set_title('Energija sustava krutine')
ax.legend(loc='upper right')
plt.show()'''

#kod za plot radijalne distribucijske funkcije
fig = plt.figure(figsize=(9,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.plot(r, gr, color='red', lw=1.0)
ax.set_xlim(0.0, 8.0)
ax.set_ylim(-0.5, 22.5)
ax.set_xlabel('r / $\u03C3$')
ax.set_ylabel('g(r)')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.5))
ax.yaxis.set_major_locator(tick.MultipleLocator(2.0))
ax.text(x=5.7, y=20.9, s=f"N$_{'a'}$=224, \u03C1=0.92, T=0.02 $\u03B5/k_{'B'}$")
ax.grid(lw=0.2, linestyle=':')
ax.set_title('Radijalna distribucijska funkcija sustava krutine')
plt.show()