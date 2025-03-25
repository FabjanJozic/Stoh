import numpy as np
import matplotlib.pyplot as plt

dx, dt = 0.1, 0.005
D = 1e-2
xL, xR = -3.0, 3.0 #lijevi i desni rub domene
xLC, xRC = 0.0, 0.0 #rubni uvjeti
alpha = D*dt/(dx**2)

N, T = int((xR-xL)/dx), 200

dif1, dif2 = np.zeros(N+1), np.zeros(N+1)
x = np.arange(xL, xR+dx, dx)
for i in range(len(dif1)):
    if i > len(dif1)/2-1 and i < len(dif1)/2+1:
        dif1[i] = 1.0
    else:
        dif1[i] = 0.0

for t in range(T):
    for p in range(1, N):
        dif2[p] = alpha*(dif1[p+1]+dif1[p-1])+(1-2*alpha)*dif1[p]
        dif2[0], dif2[-1] = xLC, xRC
    dif1 = np.copy(dif2)

fig = plt.figure(figsize=(6,4), dpi=90)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.70])
plt.rcParams.update({'font.size': 12}) #type: ignore
axes.plot(x, dif2, c='green', lw=1.0)
#axes.legend(['$<x>$', '$<x^{2}>$'])
axes.set_xlabel('x')
axes.set_ylabel('rho(x,t)')
axes.grid(lw=0.2, linestyle=':')
plt.show()