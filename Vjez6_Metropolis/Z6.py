import numpy as np

NbSkip = 50 #broj preskocenih blokova
Nb = 100 #broj blokova
Nk = 300 #broj koraka
Nw = 5000 #broj setaca
Nacc = 300 #broj koraka za provjeru prihvacanja

def Psi(r): #valna funkcija |3,0,0> stanja
    return (27-18*r+2*r**2)*np.exp(-r/3.0)

x = np.random.uniform(-17.0, 17.0, (3, Nw)) #pocetni polozaji setaca
dX = np.array([5.0, 5.0, 5.0]) #pocetni maksimalni koraci setaca
f = np.zeros(Nw) #funkcija za radijalnu udaljenost <r>
P = np.zeros(Nw) #|Ψ|²
dDX = 0.05 #faktor promjene maksimalnih koraka setaca

#izracun pocetnih vrijdnosti r i |Ψ|²
r2 = np.sum(x**2, axis=0)
r = np.sqrt(r2)
P = Psi(r)**2
f = r.copy()

ff = open("r_H300.dat", "w") #file za <r>
frNw = open("rNw_H300.dat", "w") #file za polozaje setaca

ff.write("# Block   <r> (block average)   <r> (cumulative average)\n")
frNw.write("# Step        x               y              z\n")

for iw in range(Nw): #spremanje pocetnih vrijednosti
    frNw.write(f"{0:<7d} {x[0, iw]:>12.6f} {x[1, iw]:>12.6f} {x[2, iw]:>12.6f}\n")
frNw.write("\n")

acc = 0 #broj prihvacenih setaca
Sbf = 0.0 #suma srednjih vrijednosti po blokovima
Sbf2 = 0.0

for ib in range(1-NbSkip, Nb+1): #Metropolisova petlja
    Skf = 0.0 #suma srednjih vrijednosti po setacima
    if ib == 1:
        acc = 0
    for ik in range(1, Nk+1):
        Swf = 0.0 #suma funkcije f po setacima
        for iw in range(Nw):
            dx = (2*np.random.rand(3)-1)*dX
            xp = x[:, iw]+dx
            rp = np.linalg.norm(xp) #radijalna udaljenost probnog polozaja
            tmp = Psi(rp)
            Pp = tmp * tmp
            T = Pp/P[iw] #vjerojatnost za prihvacanje pomaka
            if T >= 1 or np.random.rand() <= T:
                x[:, iw] = xp
                P[iw] = Pp
                f[iw] = rp
                acc += 1
            Swf += f[iw]
        #podesavanje velicine koraka na pocetku simulacije
        if ((ib-1+NbSkip)*Nk+ik) % Nacc == 0 and ib < 1:
            accP = acc/(Nacc*Nw)
            scale = (1+dDX) if accP > 0.5 else (1-dDX)
            dX *= scale
            if ib % 10:
                print(f"ib = {ib}, accP = {accP*100.0:3.1f}")
            acc = 0
        if ib > 0:
            Skf += Swf/Nw
    #dio simulacije koji se prihvaca
    if ib > 0:
        Sbf += Skf/Nk
        Sbf2 += (Skf/Nk)**2
        accP = acc/(ib*Nw*Nk) #udio prihvacenih koraka
        scale = (1+dDX) if accP > 0.5 else (1-dDX)
        dX *= scale
        if ib % (Nb//10) == 0:
            print(f"ib = {ib}, accP = {accP*100.0:3.1f}")
        for iw in range(Nw): #biljezenje polozaja setaca
            frNw.write(f"{(ib-1)*Nk+ik:<7d} {x[0, iw]:>12.6f} {x[1, iw]:>12.6f} {x[2, iw]:>12.6f}\n")
        frNw.write("\n")
        ff.write(f"{ib:<7d} {Skf/Nk:>16.7f} {Sbf/ib:>16.7f}\n") #spremanje <r> za dani blok

ave_f = Sbf/Nb #prosjek prihvacenih koraka
sig_f = np.sqrt((Sbf2/Nb)-ave_f**2) #devijacija za <r>

print("\n accP = %4.1lf\n" % (accP*100.0))
print("\n max dx = %6.4lf, %6.4lf, %6.4lf\n" % tuple(dX))
print("\n <r> = %8.5lf +- %8.5lf \n" % (ave_f, sig_f))
