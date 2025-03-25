import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from matplotlib import cm

Dx, Dy = 2.0, 2.0

Nw = 200000 #broj setaca
Nk = 5000 #broj koraka
walkers = np.zeros((Nw, 2))

#kod za odredivanje distribucijske funkcije
N_time = 500 #konacni trenutak u vremenu
with open('2D_walkers_distribution.txt', 'w') as wr:
    for w in range(Nw): #pocetne pozicije setaca
        walkers[w, 0], walkers[w, 1] = 40.0+20.0*np.random.rand(), 15.0+10.0*np.random.rand()
    k = 0
    while k <= N_time:
        prob = np.zeros((int(100/Dx), int(100/Dy))) #mreza za vjerojatnosti pronalaska setaca
        lin = ""
        for w in range(Nw):
            dx, dy = -0.5+np.random.rand(), -1.5+3.0*np.random.rand() #random pomaci setaca
            walkers[w, 0] += dx
            walkers[w, 1] += dy
            if walkers[w, 0] < 0.0 or walkers[w, 0] > 100.0: #elasticni sudar s rubom domene
                walkers[w, 0] -= 2*dx
            if walkers[w, 1] < 0.0 or walkers[w, 1] > 100.0:
                walkers[w, 1] -= 2*dy
            i, j = int(walkers[w, 0]/Dx), int(walkers[w, 1]/Dy)
            prob[i, j] += 1.0
        if k == N_time:
            for x in range(int(100/Dx)):
                for y in range(int(100/Dy)):
                    P_ij = prob[x, y]/Nw #normalizacija
                    Xc, Yc = (x+0.5)*Dx, (y+0.5)*Dy
                    rho = P_ij/(Dx*Dy) #vrijednost distribucijske funkcije
                    lin += f"%5d %4d %4d %12.8f\n" %(k, Xc, Yc, rho)
            wr.write(lin)
        k += 1
    wr.close()

with open('2D_walkers_distribution.txt', 'r') as re:
    Xpos, Ypos, dis = [], [], []
    R = re.readlines()
    N = len(R)
    for o in range(len(R)):
        valN, valX, valY, valg = R[o].strip().split()
        Xpos.append(float(valX))
        Ypos.append(float(valY))
        dis.append(float(valg)*1000)
    re.close()


X = np.reshape(Xpos, (50, 50))
Y = np.reshape(Ypos, (50, 50))
Z = np.reshape(dis, (50, 50))

fig = plt.figure(figsize=(7,5), dpi=120)
axes = plt.axes(projection ='3d')
plt.rcParams.update({'font.size': 12}) #type: ignore
surface = axes.plot_surface(X, Y, Z, cmap=cm.Reds, linewidth=0, antialiased=False)
axes.set_xlim(0.0, 100.0)
axes.set_ylim(0.0, 100.0)
axes.xaxis.set_major_locator(tick.MultipleLocator(20))
axes.yaxis.set_major_locator(tick.MultipleLocator(20))
axes.zaxis.set_major_locator(tick.MultipleLocator(0.5))
fig.colorbar(surface, shrink=0.5, aspect=5)
#axes.grid(lw=0.2, linestyle=':')
axes.set_xlabel('x / mm')
axes.set_ylabel('y / mm')
axes.legend(['$10^{3}$ P$_{2D}$(x, y, t=$500\cdot\u0394$t, N=$2\cdot10^{5}$) / mm$^{-2}$'])
plt.show()

#kod za racunanje entropije
#uputa: Nw <= 50000   
'''with open('2D_walkers_entropy.txt', 'w') as wr:
    for w in range(Nw): #pocetne pozicije setaca
        walkers[w, 0], walkers[w, 1] = 40.0+20.0*np.random.rand(), 15.0+10.0*np.random.rand()
    for k in range(Nk+1):
        prob = np.zeros((int(100/Dx), int(100/Dy))) #mreza za vjerojatnosti pronalaska setaca
        S = 0.0 #entropija
        lin = ""
        for w in range(Nw):
            dx, dy = -0.5+np.random.rand(), -1.5+3.0*np.random.rand() #random pomaci setaca
            walkers[w, 0] += dx
            walkers[w, 1] += dy
            if walkers[w, 0] < 0.0 or walkers[w, 0] > 100.0: #elasticni sudar s rubom domene
                walkers[w, 0] -= 2*dx
            if walkers[w, 1] < 0.0 or walkers[w, 1] > 100.0:
                walkers[w, 1] -= 2*dy
            i, j = int(walkers[w, 0]/Dx), int(walkers[w, 1]/Dy)
            prob[i, j] += 1.0
        if k%10 == 0.0:
            for x in range(int(100/Dx)):
                for y in range(int(100/Dy)):
                    P_ij = prob[x, y]/Nw #normalizacija
                    if P_ij != 0.0:
                        S -= P_ij*np.log(P_ij) #racunanje entropije
            lin += f"%6d %10.6f\n" %(k, S)
            wr.write(lin)
    wr.close()
    
with open('2D_walkers_entropy.txt', 'r') as re:
    N, ent = [], []
    R = re.readlines()
    for q in range(len(R)):
        valN, valS = R[q].strip().split()
        N.append(float(valN))
        ent.append(float(valS))
    re.close()
    
fig = plt.figure(figsize=(7,5), dpi=110)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.70])
plt.rcParams.update({'font.size': 12}) #type: ignore
axes.plot(N, ent, color='red', lw=1.2)
axes.set_title('Entropija sustava za {} šetača'.format(Nw))
axes.set_xlim(0.0, 5000.0)
axes.set_ylim(4.0, 8.0)
axes.xaxis.set_major_locator(tick.MultipleLocator(500))
axes.yaxis.set_major_locator(tick.MultipleLocator(0.5))
axes.grid(lw=0.2, linestyle=':')
axes.set_xlabel('broj koraka / vrijeme')
axes.set_ylabel('S / k$_{B}$')
plt.show()'''