import numpy as np
import matplotlib.pyplot as plt

N = 500
#m = 1
Ed = 0.0 #energija demona
E = [25 for __ in range(N)] #energija sustava idealnog plina
v = [np.sqrt(2*E[e]/N) for e in range(N)] #pocetne brzine
dv = v[0]*4

burn = 5000 #broj odbacenih koraka
Nk = 20000 #broj koraka

accept = 0
energy, demon, step = [], [], []
for i in range(1, burn+Nk+1):
    brz = [] #lista za v^2
    for j in range(N):
        v_prob = v[j]+dv*(np.random.rand()-0.5)
        dE = 0.5*N*v_prob**2-E[j]
        if (dE < 0.0) or (dE > 0.0 and dE < Ed):
            E[j] += dE
            Ed -= dE
            v[j] = v_prob
            accept += 1
        if i == Nk+burn: #gleda se raspodjela brzina samo u konacnom trenutku
            brz.append(v[j]**2)
    if (i > burn) and (i%500 == 0):
        energy.append(np.mean(E))
        demon.append(Ed)
        step.append(i)
accept /= (Nk+burn)*N

print(accept)

plt.plot(step, demon, lw=1.5)
#plt.xlabel('$v^{2}$ / (m/s)$^{2}$')
plt.show()