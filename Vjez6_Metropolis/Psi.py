import numpy as np
import matplotlib.pyplot as plt

rad = np.arange(0.0, 30.0, 0.01)

def Psi(r): #valna funkcija |3,0,0> stanja H atoma
    return 1.0/(81.0*np.sqrt(3.0*np.pi))*(27.0-18.0*r+2.0*r**2)*np.exp(-r/3.0)

psi2 = [(Psi(rad[i])**2)*4*np.pi*rad[i]**2 for i in range(len(rad))]

fig = plt.figure(figsize=(11,4), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.75])
plt.rcParams.update({'font.size': 12}) #type: ignore
ax.plot(rad, psi2, color='blue', lw=1.0, label='|3,0,0>')
ax.fill_between(rad, psi2, color='skyblue', alpha=0.8)
ax.set_xlim(0, 30)
ax.set_ylim(0.0, 0.12)
ax.set_xlabel('r / a$_{0}$')
ax.set_ylabel('$|\u03A8|^{2}$')
ax.legend(loc='upper right')
plt.show()