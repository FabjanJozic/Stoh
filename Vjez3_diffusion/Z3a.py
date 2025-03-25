import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from scipy import stats as S

Nw = 64000
Nt = 200
Dx = 0.1
walkers = np.zeros(Nw)
prob = np.zeros((int(200.0/Dx), Nt))

r_MS, time = [0.0], [0]

t = 1
while t <= Nt:
    r = 0.0
    for w in range(Nw):
        dx = -3.0+6*np.random.rand()
        walkers[w] += dx
        if walkers[w] < -100.0 or walkers[w] > 100.0:
            walkers[w] -= 2*dx
        i = int(walkers[w]/Dx)
        prob[i, t-1] += 1
        r += walkers[w]**2
    r_MS.append(r/Nw)
    time.append(t)
    t += 1
    
for x in range(int(6.0/Dx)):
    for y in range(Nt):
        prob[x, y] /= Nw

const, b, r, p, std_err = S.linregress(time, r_MS)
D = const/2
#D = 1.495273208054622

'''X = np.arange(0.0, Nt+0.5, 0.5)
Y = [const*p for p in X]
        
fig = plt.figure(figsize=(12,6), dpi=120)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.75])
plt.rcParams.update({'font.size': 10}) #type: ignore
axes.plot(X, Y, lw=1.0, color='blue', label='<r$^{2}$(t)>=2Dt - fit')
axes.scatter(time, r_MS, facecolor='none', edgecolor='darkred', s=8.0, label='MC data')
axes.set_xlim(0.0, Nt)
axes.set_ylim(0.0, 600.0)
axes.set_xlabel('t / s')
axes.set_ylabel('<r$^{2}$(t)> / cm$^{2}$')
axes.xaxis.set_major_locator(tick.MultipleLocator(20))
axes.yaxis.set_major_locator(tick.MultipleLocator(50))
axes.grid(lw=0.2, linestyle=':')
axes.legend()
plt.show()'''
        