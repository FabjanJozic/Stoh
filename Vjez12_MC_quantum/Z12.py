import numpy as np

seed = 208 #za random number generator

Nk = 200
Nw = 100
Nb = 100
Nb_skip = 40
alpha = 1.3 #parmetar probne valne funkcije

h_ = 1.0 #reducirana Planckova konstanta
m = 1.0 #masa cestice
K = 1.0 #konstanta potencijalne energije

def Psi(x): #valna funkcija
    if x >= 0.0:
        val = x*np.exp(-alpha*x*x)
    else:
        val = 0.0
    return val

X = np.zeros(Nw+1) #polozaji setaca
Xp = np.zeros(Nw+1) #probni polozaji setaca
E = np.zeros(Nw+1) #lokalna energija
P = np.zeros(Nw+1) #vjerojatnost nalazenja setaca na polozaju x
dk = [1.5, 1.5, 1.5] #maksimalna duljina koraka

fout = open('E.dat', 'w') #Nb_eff, N_acc, sum_Ek/Nk

accept = 0.0

for iw in range(Nw+1):
    X[iw] = 14*np.random.default_rng(seed)
    P[iw] = Psi(X[iw])*Psi(X[iw])