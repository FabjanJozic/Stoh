import numpy as np

NbSkip = 50 #broj preskocenih blokova
Nb = 200 #ukupni broj blokova
Nk = 100 #broj koraka
Nw = 100 #broj setaca
Nacc = 100 #broj koraka za provjeru prihvacanja

def Psi(r, z): #valna funkcija
    return z*np.exp(-r/2.)

ib, ik = 1, 0  #indeksi blokova i koraka
x = np.zeros((4, Nw+1)) #koordinate setaca
xp = np.zeros(4) #koordinate probnog setaca
dX = np.array([0, 1.5, 1.5, 1.5]) #maksimalne vrijednosti koraka
f = np.zeros(Nw+1) #vrijednost funkcije f (radijalna udaljenost)
P = np.zeros(Nw+1) #vjerojatnost nalazenja na polozaju X

ff = open("r.dat", "w") #datoteka za spremanje srednje vrijednosti
frNw = open("rNw.dat", "w") #datoteka za spremanje polozaja setaca
for iw in range(1, Nw+1):
    rp2 = 0.0
    for k in range(1, 4):
        x[k][iw] = 14.0*(np.random.rand()-0.5)
        rp2 += x[k][iw]*x[k][iw]
    frNw.write("%7d  %13.8e  %13.8e  %13.8e\n" % ((ib-1)*Nk+ik, x[1][iw], x[2][iw], x[3][iw]))
    rp = np.sqrt(rp2)
    tmp = Psi(rp, x[3][iw])
    P[iw] = tmp*tmp #Psi^2
    f[iw] = rp
frNw.write("\n\n")

acc = 0.0 #broj prihvacenih setaca
Sbf = 0.0 #suma srednjih vrijednosti po blokovima
Sbf2 = 0.0

for ib in range(1-NbSkip, Nb+1):
    '''Indeksacija pocinje od negativne vrijednosti da mozemo odbaciti sve vrijednosti do NbSkip.'''
    Skf = 0.0 #suma srednjih vrijednosti po koracima
    if ib == 1:
        acc = 0.0
    for ik in range(1, Nk+1): #indeks koraka
        Swf = 0.0 #suma vrijednosti f po svim setacima
        for iw in range(1, Nw+1):
            rp2 = 0.0
            for k in range(1, 4):
                dx = 2.0*(np.random.rand()-0.5)*dX[k]
                xp[k] = x[k][iw]+dx
                rp2 += xp[k]*xp[k]
            rp = np.sqrt(rp2) #r (radijalna udaljenost) probnog polozaja
            tmp = Psi(rp, xp[3])
            Pp = tmp*tmp #vjerojatnost za probni polozaj
            T = Pp/P[iw] #vjerojatnost prijelaza
            if T >= 1 or np.random.rand() <= T:
                for k in range(1, 4):
                    x[k][iw] = xp[k]
                acc += 1
                P[iw] = Pp
                f[iw] = rp
            Swf += f[iw]
        if ((ib-1+NbSkip)*Nk+ik)%Nacc == 0 and ib < 1:
            accP = acc/(Nacc*Nw)
            # 1) PRILAGODITE MAX KOORDINATNE POMAKE (ADJUST MAX COORDINATE CHANGES)
            
            
            if ib%10: #nakon stabilizacije sustava
                print("ib = %d, accP = %3.1lf\n" % (ib, accP*100.0))
            acc = 0.0
        if ib > 0:
            Skf += Swf/Nw
    if ib > 0:
        Sbf += Skf/Nk
        Sbf2 += Skf*Skf/(Nk*Nk)
        accP = acc/(ib*Nw*Nk) #udio prihvacenih koraka
        # 2) PRILAGODITE MAX KOORDINATNE POMAKE (ADJUST MAX COORDINATE CHANGES)
        
        
        if ib%(Nb/10) == 0:
            print("ib = %d, accP = %3.1lf\n" % (ib, accP*100.0))
        # 3) POHRANITE SVE POLOZAJE U frNw (STORE ALL POSITIONS IN frNw)
        
        
        frNw.write("\n\n")
        ff.write("%7d  %13.8e  %13.8e\n" % (ib, Skf/Nk, Sbf/ib))
# 4) IZRACUNAJTE PROSJEK, DEVIJACIJU I PRIHVACENOST: ave_f, sig_f, accP
# 4) (CALCULATE AVERAGE, DEVIATION, ACCEPTANCE: ave_f, sig_f, accP)



'''print("\n accP = %4.1lf\n" % (accP * 100.0))
print("\n max dx = %6.4lf, %6.4lf, %6.4lf\n" % (dX[1], dX[2], dX[3]))
print("\n <r> = %8.5lf +- %8.5lf \n" % (ave_f, sig_f))'''

