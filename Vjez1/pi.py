from numpy import random as r
import numpy as np
import matplotlib.pyplot as plt

#kod za procjenu broja pi
N_max = 3e5
pi, dev, N = [], [], []
N_k = 0

for i in range(int(N_max)):
    x, y = r.rand(), r.rand()
    if x**2+y**2 <= 1.0:
        N_k += 1
    pi.append(4*N_k/(i+1))
    dev.append(abs(pi[i]-np.pi)*np.sqrt(N_max))
    N.append(i)
    
fig = plt.figure(figsize=(6,4), dpi=100)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.70])
plt.rcParams.update({'font.size': 10})           #type: ignore
axes.plot(N, dev, lw=1.0, color='red')
axes.grid(lw=0.2, linestyle=':')
plt.show()