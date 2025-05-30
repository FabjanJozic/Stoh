import numpy as np

'''
Kod za stvaranje trokutaste atomske resetke. 'Na' atoma smjesta se u 'jNa' tocaka
Raspodjela u 'my2*2' redaka i 'mx' stupaca unutar podrucja definiranim za 'Lx' i
'Ly', cime je postignuta gustoca 'jNa/(Lx*Ly)'. Prvi susjedi udaljeni su za 'a'.
'''


my2 = 10 #broj parova redaka u y smjeru \ ukupno/2
rho = 0.08 #pocetna gustoca sustava
Nw = 1 #broj setaca

dmx = my2*np.sqrt(3.0)+0.5
mx = int(dmx) #broj mjesta u x smjeru

Na = 2*mx*my2 #broj atoma

p = Na/rho 
o = mx/(my2*np.sqrt(3.0))
Lx = np.sqrt(p*o) #sirina podrucja
Ly = np.sqrt(p/o) #visina podrucja
a = Lx/mx #udaljenost medu atomima u x smjeru

fxy = open('xy.dat', 'w') #za zapisivanje koordinata

x01 = 0.25*a
y01 = 0.25*a*np.sqrt(3.0)
x02 = x01+0.5*a
y02 = y01+0.5*a*np.sqrt(3.0)

for iw in range(1, Nw+1):
    jNa = 0 #broj tocaka
    for nx in range(mx):
        for ny in range(my2):
            x1 = x01+nx*a
            y1 = y01+ny*a*np.sqrt(3.0)
            x2 = x02+nx*a
            y2 = y02+ny*a*np.sqrt(3.0)
            fxy.write(f"{x1:.7f}\t{y1:.7f}\n")
            fxy.write(f"{x2:.7f}\t{y2:.7f}\n")
            jNa += 2
    fxy.write('\n')
    print(f'\nBroj atoma u resetci: {jNa:d}\n')
            
fxy.close()

#kod za vizualizaciju resetke
'''import matplotlib.pyplot as plt

er = np.loadtxt('xy.dat')
x, y = [], []
for j in range(len(er)):
    x.append(er[j, 0])
    y.append(er[j, 1])
    
plt.scatter(x, y)
plt.show()'''