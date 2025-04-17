import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

delta = 2.5
burn = 5000 #broj pocetnih odbacenih koraka
N = 100000 #
Nw = 300 #setaci
xrange = 1.0

def p(x): #distribucijska funkcija
    return np.exp(-0.5*x**2)
def f(x): #funkcija koja se integrira
    return x**2

'''with open('exp2_Metropolis.txt', 'w') as wr:
    accept = 0 #udio prihvacenih slucajeva
    x0 = [-xrange+2*xrange*np.random.rand() for _ in range(Nw)]
    for j in range(1, N+burn+1):
        Ival = []
        for i in range(Nw):
            xn = x0[i]+delta*(2*np.random.rand()-1)
            w = p(xn)/p(x0[i])
            if w >= 1.0 or np.random.rand() <= w:
                x0[i] = xn
                accept += 1
            if j > burn:
                Ival.append(f(x0[i]))
        if j > burn and (j-burn) % 100 == 0:
            I = np.mean(Ival)
            wr.write(f"%7d %7.5f\n" % (j, I))
    accept /= Nw*(N+burn)
    wr.close()
    
print(accept)'''

with open('exp2_Metropolis.txt', 'r') as re:
    R = re.readlines()
    Nv, Iv, I0 = [], [], []
    for u in range(len(R)):
        nval, ival = R[u].strip().split()
        Nv.append(float(nval))
        Iv.append(float(ival))
        I0.append(1.0) #egzaktna vrijednost integrala
    re.close()
        
fig = plt.figure(figsize=(11,4), dpi=110)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
axes.plot(Nv, Iv, color='red', lw=1.0, label='numerical value')
axes.plot(Nv, I0, color='black', linestyle='--', lw=1.5, label='exact value')
axes.grid(lw=0.3, linestyle=':')
axes.set_xlim(burn, N+burn)
#axes.set_ylim(0.0, 10000.0)
axes.xaxis.set_major_locator(tick.MultipleLocator(10000))
axes.yaxis.set_major_locator(tick.MultipleLocator(0.1))
axes.legend(loc='upper right')
plt.show()  