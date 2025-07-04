import numpy as np

rho = 0.08 #pocetna gustoca sustava
my2 = 3 #broj parova redaka u y smjeru
Na = 30 #broj atoma

Nb = 200
Nk = 100
Nw = 10
Nb_skip = 100
kT = 0.1 #temperatura sustava
dmax = 0.1 #maksmimalni pomak

Nbins = 500 #broj binova za histogram radijalne distribucijske funkcije

Lx, Ly = 0.0, 0.0 #sirina i visina podrucja
Lxp, Lyp = 0.0, 0.0 #polovica sirine i visine podrucja

def energy(x, iw): #energija sustava
    global Lx, Ly, Lxp, Lyp, Lminp2
    sum = 0.0
    for i in range(1, Na):
        rxi = x[iw, i, 0] #pomocna x koordinata cestice
        ryi = x[iw, i, 1] #pomocna y koordinata cestice
        for j in range(i+1, Na+1):
            rxij = rxi-x[iw, j, 0]
            ryij = ryi-x[iw, j, 1] 
            if rxij > Lxp:
                rxij -= Lx
            if rxij < -Lxp:
                rxij += Lx
            if ryij > Lyp:
                ryij -= Ly
            if ryij < -Lyp:
                ryij += Ly
            rij2 = rxij**2+ryij**2
            if rij2 <= Lminp2:
                r2 = 1/rij2
                r6 = r2**3
                r12 = r6**2
                sum += r12-r6 #Lennard-Jones tip potencijala
    return 4*sum

X = np.zeros((Nw+1, Na+2, 2))
Xp = np.zeros((Nw+1, Na+2, 2)) #probni polozaj atoma
E = np.zeros(Nw+1) #energija
gr = np.zeros(Nbins+1) #radijalna distribucijska funkcija

dmx = my2*np.sqrt(3.0)+0.5
mx = int(dmx)
if Na != 2*mx*my2:
    print('\nNisu uskladene postavke s onima u kodu za generiranje resetke xy_trinagle.py. Ugasi program.\n')

S = Na/rho
o = mx/(my2*np.sqrt(3.0))
Lx = np.sqrt(S*o)
Ly = np.sqrt(S/o)
Lmin = min(Lx, Ly)
Lminp = Lmin/2.0
Lminp2 = Lminp**2
dr = Lminp/Nbins #sirina podrucja

print(f"{Na:d} cestica u podrucju ({Lx:.6f} x {Ly:.6f}), L_min/2 = {Lminp:.6f}.")

with open('xy.dat', 'r') as f_xy: #pocetni polozaji
    for i in range(1, Na+1):
        rxi, ryi = map(float, f_xy.readline().split())
        for iw in range(1, Nw+1):
            X[iw, i, 0] = rxi
            X[iw, i, 1] = ryi

for iw in range(1, Nw+1): # pocetne energije
    E[iw] = energy(X, iw)

print(f"Pocetna energija: {E[1]:.6f}")

sum_Eb, sum_Eb2 = 0.0, 0.0
reject_tot = 0.0

fE = open('E.dat', 'w') #ib, E_k, E_b, sigmaE
fRDF = open('RDF.dat', 'w') #r, g(r)

for ib in range(1, Nb+Nb_skip+1): #Metropolisov algoritam
    reject = 0.0
    sum_Ek, sum_Ek2 = 0.0, 0.0
    for ik in range(1, Nk+1):
        for iw in range(1, Nw+1):
            for i in range(1, Na+1):
                Xp[iw, i, 0] = X[iw, i, 0]+dmax*(np.random.rand()-0.5)
                Xp[iw, i, 1] = X[iw, i, 1]+dmax*(np.random.rand()-0.5)
                Xp[iw, i, 0] %= Lx
                Xp[iw, i, 1] %= Ly
            dE = energy(Xp, iw)-E[iw]
            if dE > 0.0 and np.exp(-dE/kT) <= np.random.rand():
                reject += 1.0
                reject_tot += 1.0
                dE = 0.0
            else:
                for i in range(1, Na+1):
                    X[iw, i, 0] = Xp[iw, i, 0]
                    X[iw, i, 1] = Xp[iw, i, 1]
            E[iw] += dE
            if ib > Nb_skip:
                sum_Ek += E[iw]/Nw
                sum_Ek2 += E[iw]**2/Nw
                for i in range(1, Na):
                    rxi = X[iw, i, 0]
                    ryi = X[iw, i, 1]
                    for j in range(i+1, Na+1):
                        rxij = rxi-X[iw, j, 0]
                        ryij = ryi-X[iw, j, 1]
                        if rxij > Lxp: #aproksimacija minimalne slike
                            rxij -= Lx
                        if rxij < -Lxp:
                            rxij += Lx
                        if ryij > Lyp:
                            ryij -= Ly
                        if ryij < -Lyp:
                            ryij += Ly
                        rij = np.sqrt(rxij**2+ryij**2) #udaljenost para cestica (i,j)
                        if rij < Lminp:
                            iring = int(rij/dr) #prsten kojem pripada cestica
                            if iring < Nbins:
                                gr[iring] += 2 #punjenje radijalne distribucijske funkcije g(r) za parove (i,j)
    reject /= Nk*Nw
    accept_ib = 1-reject/ib
    if accept_ib > 0.5: #optimizacijske korekcije
        dmax *= 1.05
    elif accept_ib < 0.5:
        dmax*= 0.95
    if ib > Nb_skip:
        Nb_eff = ib-Nb_skip
        sum_Eb += sum_Ek/Nk
        sum_Eb2 += sum_Ek2/Nk
        sigmaE = 0.0
        if Nb_eff > 1:
            sigmaE = np.sqrt(sum_Eb2/Nb_eff-(sum_Eb**2)/(Nb_eff**2))/np.sqrt(Nb_eff-1)
        fE.write(f"{ib:>5d} {sum_Ek/Nk:>11.6f} {sum_Eb/Nb_eff:>11.6f} {sigmaE:>11.6f}\n")

fE.close()
accept = 1.0-reject_tot/((Nb+Nb_skip)*Nk*Nw)

for ir in range(1, Nbins+1):
    r_lower = ir*dr
    r_upper = (ir+1)*dr
    shell = np.pi*(r_upper**2-r_lower**2)
    if shell > 0.0:
        gr[ir] /= shell*rho*Na*Nw*Nk*Nb  #normalizacija
        fRDF.write(f"{r_lower+dr/2:>11.6f} {gr[ir]:>11.6f}\n")
fRDF.close()
    
E_out = 4.0*np.pi*Na*(0.2/(Lminp**10)-0.5/(Lminp**4))
print('\nPostotak prihvacenih pomaka: {:.2f} %'.format(accept*100))
print('Energija unutar L_min/2: {:.6f}'.format(sum_Eb/Nb_eff))
print('Energija izvan L_min/2: {:.6f}\n'.format(E_out))