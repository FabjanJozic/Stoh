import numpy as np
import warnings

'''
U ovom kodu racuna se standardna devijacija srednje udaljenosti iz "rNw_H300.dat".
'''

Nw = 10000  #broj setaca
Nkmax = 200
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    frNw = np.loadtxt('rNw_H300.dat', comments='#', max_rows=Nw*200, usecols=(1,2,3))
fstdev = open('st_dev_H300.dat', 'w') #file za graf

N = len(frNw)

for Nk in range(1, Nkmax+1):
    Nb = N//Nk #koriste se samo cijeli blokovi
    if Nb <= 2: #ne analiziraju se blokovi s 2 ili manje podataka (losa statistika)
        continue
    Sfb, Sf2b = 0.0, 0.0 #suma srednjih vrijednosti po bloku
    for b in range(Nb):
        block = frNw[b*Nk : (b+1)*Nk]
        r = np.linalg.norm(block, axis=1) #radijalna udaljenost
        r_mean = np.mean(r)
        Sfb += r_mean
        Sf2b += r_mean**2
    Smb = Sfb/Nb #srednja vrijednost
    var = ((Sf2b/Nb)-Smb**2)/(Nb-1) #varijanca
    fstdev.write(f"{Nk:<3d} {Smb:>13.9f} {np.sqrt(var):>12.9f}\n")
        
fstdev.close()