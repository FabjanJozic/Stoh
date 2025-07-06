import numpy as np
import matplotlib.pyplot as plt

rad = np.arange(0.0, 7.0, 0.001)

m, h_ = 1.0, 1.0
k = 2.0 # V(x)=kx

alpha = (np.sqrt(2/np.pi)*(k*m)/(3*h_))**(2/3) # varijacijski parametar
A = (128*(alpha**3)/np.pi)**(1/4) #normalizacijska konstanta

def Psi(x):
    return A*x*np.exp(-alpha*x*x)

psi2 = [Psi(rad[i])**2 for i in range(len(rad))]
psi = [Psi(rad[i]) for i in range(len(rad))]
Vx = [k*rad[i] for i in range(len(rad))]

fig = plt.figure(figsize=(7,6), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(rad, psi2, color='red', lw=1.0, label='$|\u03A8(x)|^{2}$')
ax.plot(rad, psi, color='blue', lw=1.0, label='$\u03A8(x)$')
ax.plot(rad, Vx, color='black', lw=2.0, label='$V(x) = kx$, k={}'.format(k))
ax.fill_between(rad, psi2, color='orange', alpha=0.8)
ax.fill_between(rad, psi, color='cyan', alpha=0.4)
ax.set_xlim(0.0, 3.0)
ax.set_ylim(0.0, 3.0)
ax.set_xlabel('x')
ax.legend(loc='best')
plt.show()

I = 0.0
for k in range(len(rad)):
    I += psi2[k]*0.001

print(I)