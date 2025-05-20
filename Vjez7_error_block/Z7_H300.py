import numpy as np
import warnings
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

'''
U ovom kodu racuna se standardna devijacija srednje udaljenosti iz "rNw_H300.dat".
'''

#Nw = 10000  #broj setaca
Nkmax = 200

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fr = np.loadtxt('r_H300.dat', comments='#', usecols=2)
fstdev = open('st_dev_H300.dat', 'w') #file za graf

N = len(fr)

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

fo = np.loadtxt('st_dev_H300.dat')
bl, mr, dev = [], [], []

for i in range(len(fo)):
    bl.append(fo[i, 0])
    mr.append(fo[i, 1])
    dev.append(1000*fo[i, 2])
    
'''fig = plt.figure(figsize=(12,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.errorbar(bl, mr, yerr=dev, fmt='o-', capsize=2, label='data', ecolor='green', elinewidth=0.3,
            mfc='lime', mec='green', ms=5, mew=1)
ax.set_xlim(0, 67)
ax.set_ylim(13.1, 13.9)
ax.set_xlabel('b')
ax.set_ylabel('<r> / a$_{0}$')
ax.xaxis.set_major_locator(tick.MultipleLocator(6))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.1))
ax.grid(lw=0.2, linestyle=':')
ax.set_title('Vrijednosti srednje radijalne udaljenosti <r> elektrona u\n|3,0,0> stanju $^{1}$H atoma dobivene dodatnim blokiranjem')
ax.legend(loc='upper right')
plt.show()'''

mdev = f"{np.mean(dev)/1000:<5.5f}"

fig = plt.figure(figsize=(8,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.plot(bl, dev, color='green', lw=1.7)
ax.set_xlim(0, 67)
ax.set_ylim(0.04, 0.36)
ax.set_xlabel('b')
ax.set_ylabel('$10^{3} \u03C3_{r}$ / $\u212B$')
ax.xaxis.set_major_locator(tick.MultipleLocator(6))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.04))
ax.grid(lw=0.2, linestyle=':')
ax.set_title('Standardna devijacija $\u03C3_{r}$ radijalne udaljenosti <r> elektrona u\n|3,0,0> stanju $^{1}$H atoma')
#ax.legend(loc='upper right')
ax.text(4, 0.32, s='$\u03C3_{}$={} $\u212B$'.format('r', mdev))
plt.show()