import numpy as np
import matplotlib.pyplot as plt

Nw = 3 #broj setaca
Nk = 5000 #broj koraka
walkers = np.zeros((Nw, 2))
'''
with open('r3w.txt', 'w') as wr:
    for w in range(Nw):
        walkers[w, 0], walkers[w, 1] = 40.0+20.0*np.random.rand(), 15.0+10.0*np.random.rand()
        for k in range(1, Nk+1):
            dx, dy = -0.5+np.random.rand(), -1.5+3.0*np.random.rand()
            walkers[w, 0] += dx
            walkers[w, 1] += dy
            if walkers[w, 0] < 0.0 or walkers[w, 0] > 100.0: #elasticni sudar s rubom domene
                walkers[w, 0] -= 2*dx
            if walkers[w, 1] < 0.0 or walkers[w, 1] > 100.0:
                walkers[w, 1] -= 2*dy
            lin = f"{walkers[w, 0]}\t{walkers[w, 1]}\n"
            wr.write(lin)
        wr.write("\n")
    wr.close()
'''
with open('r3w.txt', 'r') as re:
    R = re.readlines()
    X1, Y1, X2, Y2, X3, Y3 = [], [], [], [], [], []
    for o in range(len(R)):
        if o < Nk:
            valx, valy = R[o].strip().split()
            X1.append(float(valx))
            Y1.append(float(valy))
        elif o >= Nk+1 and o <= 2*Nk:
            valx, valy = R[o].strip().split()
            X2.append(float(valx))
            Y2.append(float(valy))
        elif o > 2*Nk+1 and o <= 3*Nk+1:
            valx, valy = R[o].strip().split()
            X3.append(float(valx))
            Y3.append(float(valy))
            
fig = plt.figure(figsize=(6,6), dpi=120)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
plt.axis('equal')
axes.plot(X1, Y1, color='red', lw=0.7, label='walker 1')
axes.plot(X2, Y2, color='blue', lw=0.7, label='walker 2')
axes.plot(X3, Y3, color='lime', lw=0.7, label='walker 3')
axes.legend()
axes.set_xlim(0.0, 100.0)
axes.set_ylim(0.0, 100.0)
plt.show()