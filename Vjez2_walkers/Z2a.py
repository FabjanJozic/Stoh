import numpy as np
import matplotlib.pyplot as plt

Nw = 5000 #broj setaca
Nk = 5000 #broj koraka
walkers = np.zeros((Nw, 2))
'''
with open('rNw.txt', 'w') as wr:
    sen = ""
    for w in range(Nw): #pocetne pozicije
        walkers[w, 0], walkers[w, 1] = 40.0+20.0*np.random.rand(), 15.0+10.0*np.random.rand()
        sen += f"%12.6f %12.6f" %(walkers[w, 0], walkers[w, 1]) 
    sen += "\n"
    wr.write(sen) #zapisivanje pocetnih pozicija
    for k in range(Nk-1):
        lin = ""
        for w in range(Nw):
            dx, dy = -0.5+np.random.rand(), -1.5+3.0*np.random.rand()
            walkers[w, 0] += dx
            walkers[w, 1] += dy
            if walkers[w, 0] < 0.0 or walkers[w, 0] > 100.0: #elasticni sudar s rubom domene
                walkers[w, 0] -= 2*dx
            if walkers[w, 1] < 0.0 or walkers[w, 1] > 100.0:
                walkers[w, 1] -= 2*dy
            lin += f"%12.6f %12.6f" %(walkers[w, 0], walkers[w, 1])
        lin += "\n"
        wr.write(lin) #zapisivanje koraka
    wr.close()
'''
with open('rNw.txt', 'r') as re:
    W = [10, 1001, 4329] #redni broj setaca koji se plota
    R = re.readlines()
    X1, Y1, X2, Y2, X3, Y3 = [], [], [], [], [], []
    for l in range(len(R)):
        val = R[l].strip().split()
        for i in range(len(val)):
            if i == int(W[0]-1):
                X1.append(float(val[i]))
                Y1.append(float(val[i+1]))
            elif i == int(W[1]-1):
                X2.append(float(val[i]))
                Y2.append(float(val[i+1]))
            elif i == int(W[2]-1):
                X3.append(float(val[i]))
                Y3.append(float(val[i+1]))
                           
fig = plt.figure(figsize=(6,6), dpi=110)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
plt.axis('equal')
axes.plot(X1, Y1, color='red', lw=0.7, label='walker {}'.format(W[0]))
axes.plot(X2, Y2, color='blue', lw=0.7, label='walker {}'.format(W[1]))
axes.plot(X3, Y3, color='lime', lw=0.7, label='walker {}'.format(W[2]))
axes.legend()
axes.set_xlim(0.0, 100.0)
axes.set_ylim(0.0, 100.0)
plt.show()