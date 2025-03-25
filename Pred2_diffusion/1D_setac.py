import numpy as np
import matplotlib.pyplot as plt

t, n = 100, 1000 #vrijeme i broj setaca
time = np.zeros(t)
Xave, X2ave = np.zeros(t), np.zeros(t) #<x> i <x^2>

for j in range(n):
    x = 0
    for i in range(1, t):
        time[i] = i
        r = np.random.rand() #pseudonasumicni broj
        if r < 0.5:
            x += 1
        else:
            x -= 1
        Xave[i] += x/n
        X2ave[i] += x**2/n
        
fig = plt.figure(figsize=(6,4), dpi=90)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.70])
plt.rcParams.update({'font.size': 12}) #type: ignore
axes.scatter(time, Xave, c='orange', edgecolor='red', s=2)
axes.scatter(time, X2ave, c='blue', edgecolor='purple', s=2)
axes.legend(['$<x>$', '$<x^{2}>$'])
axes.set_xlabel('vremenski korak')
axes.set_ylabel('$<x>$ i $<x^{2}>$ vrijednosti')
axes.grid(lw=0.2, linestyle=':')
plt.show()
        
        


