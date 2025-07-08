import numpy as np
import matplotlib.pyplot as plt
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fr = np.loadtxt('energy.dat', comments='#', usecols=1)
fstdev = open('st_dev.dat', 'w') #file za graf

N = len(fr)
Nkmax = 150

for Nk in range(1, Nkmax+1):
    Nb = N//Nk #koriste se samo cijeli blokovi
    if Nb <= 2: #ne analiziraju se blokovi s 2 ili manje podataka (losa statistika)
        continue
    Sfb, Sf2b = 0.0, 0.0 #suma srednjih vrijednosti po bloku
    for b in range(Nb):
        block = fr[b*Nk : (b+1)*Nk]  #uzima vrijednosti samo iz 2. stupca "r_H300.txt"
        Sfk = np.sum(block)
        Sfb += Sfk/Nk
        Sf2b += (Sfk*Sfk)/(Nk*Nk)
    Smb = Sfb/Nb #srednja vrijednost
    var = ((Sf2b/Nb)-Smb**2)/(Nb-1) #varijanca
    fstdev.write(f"{Nk:<3d} {Smb:>13.9f} {np.sqrt(var):>12.9f}\n")
        
fstdev.close()

fo = np.loadtxt('st_dev.dat')
dev, ib = [], []

for i in range(len(fo)):
    ib.append(fo[i, 0])
    dev.append(fo[i, 2])

print(r'<\sigma> = {}'.format(np.mean(dev)))

plt.plot(ib, dev)
plt.show()


# 1.6991112781954888e-05