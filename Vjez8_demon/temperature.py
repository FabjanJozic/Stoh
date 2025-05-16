import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from scipy import stats as S

input = np.loadtxt('P_ED.dat')
ED, pED, ln_pED = [], [], []

for i in range(len(input)):
    if input[i, 1] != 0.000000:
        ED.append(input[i, 0])
        pED.append(input[i, 1])
        ln_pED.append(np.log(input[i, 1]))

a, b, r, p, std_err = S.linregress(ED, ln_pED)
kT = -1/a #temperatura demona
# kT = 0.46

'''y = [a*e+b for e in ED]

fig = plt.figure(figsize=(8,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.scatter(ED, ln_pED, color='cyan', s=1, label='ln(P$_{ED}$)')
ax.plot(ED, y, color='blue', lw=1.0, label=f"{a:<5.2f}*ED+{b:<5.2f}")
ax.set_xlim(0.0, 4.0)
#ax.set_ylim(0.3, 0.8)
ax.set_xlabel('ED')
ax.set_ylabel('ln(P$_{ED}$)')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.5))
ax.yaxis.set_major_locator(tick.MultipleLocator(1.0))
#ax.grid(lw=0.2, linestyle=':')
ax.set_title('Idealni plin: N=80, E=20')
legend = ax.legend(loc='upper right')
legend.get_texts()[0].set_color('cyan')
legend.get_texts()[1].set_color('blue')
plt.show()'''

fig = plt.figure(figsize=(7,6), dpi=110)
ax = fig.add_axes([0.15, 0.15, 0.80, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.plot(ED, pED, color='red', lw=1.2)
ax.set_xlim(0.0, 4.0)
ax.set_ylim(0.0, 2.16)
ax.set_xlabel('ED')
ax.set_ylabel('P$_{ED}$')
ax.xaxis.set_major_locator(tick.MultipleLocator(0.5))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.24))
#ax.grid(lw=0.2, linestyle=':')
ax.set_title('Idealni plin: N=80, E=20')
plt.show()