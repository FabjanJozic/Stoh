import numpy as np
import warnings
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

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

fo = np.loadtxt('st_dev_H300.dat')
bl, mr, dev = [], [], []

for i in range(Nkmax):
    bl.append(fo[i, 0])
    mr.append(fo[i, 1])
    dev.append(fo[i, 2])
    
fig = plt.figure(figsize=(12,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.errorbar(bl, mr, yerr=dev, fmt='o-', capsize=2, label='data', ecolor='green', elinewidth=0.3,
            mfc='lime', mec='green', ms=5, mew=1)
ax.set_xlim(0, 201)
ax.set_ylim(13.51, 13.52)
ax.set_xlabel('b / $10^{4}$')
ax.set_ylabel('<r> / a$_{0}$')
ax.xaxis.set_major_locator(tick.MultipleLocator(20))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.001))
ax.grid(lw=0.2, linestyle=':')
ax.set_title('Vrijednosti srednje radijalne udaljenosti <r> elektrona u\n|3,0,0> stanju $^{1}$H atoma dobivene dodatnim blokiranjem')
ax.legend(loc='upper right')
plt.show()