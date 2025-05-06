import numpy as np
import matplotlib.pyplot as plt

max = 32 #broj spinova u jednom smjeru
kT = 2.0 #temperatura
Jv = 1.0 #integral izmjene
mH = 0.0 #magnetsko polje

def energy(s): #energija jednog spina
    sum = 0.0
    for i in range(1, max+1):
        for j in range(1, max+1):
            h = 1 if i == max else i+1 #polozaj horizontalnog spina
            v = 1 if j == max else j+1 #polozaj vertikalnog spina
            sum += Jv*s[i, j]*(s[i, v]+s[h, j])+s[i, j]*mH
    return -sum

def magnet(s): #ukupna magnetizacija sustava
    sum = 0.0
    for i in range(1, max+1):
        for j in range(1, max+1):
            sum += s[i, j]
    return sum

Mav, Mav2 = 0.0, 0.0 #prosjecna vrijednost magnetizacije
Eav, Eav2 = 0.0,0.0 #prosjecna vrijednost energije

Nk = 1000 #broj koraka
Nb = 5000 #broj blokova
burn = 1500 #broj odbacenih koraka
Naccept = 0.0

output3 = open('Magnetisation.dat', 'w') #kumulativna vrijednost magnetizacije
output4 = open('Magnetisation_b.dat', 'w') #magnetizacija po blokovima
output5 = open('Energy.dat', 'w') #kumulativna vrijednost energije sustava
output6 = open('Energy_b.dat', 'w') #energija po blokovima

S = np.ones((max+2, max+2), dtype=int) #pocetni sustav spinova
E0 = energy(S)
M0 = magnet(S)

for ib in range(1, Nb+burn+1):
    Eavb, Eavb2 = 0.0, 0.0
    Mavb, Mavb2 = 0.0, 0.0
    for _ in range(1, Nk+1):
        ei = int(1.0+np.random.rand()*max)
        ej = int(1.0+np.random.rand()*max)
        S[ei, ej] *= -1 #preokret spina
        S[ei-1, ej] = S[max, ej] if ei == 1 else S[ei-1, ej] # periodicni rubni uvjeti
        S[ei+1, ej] = S[1, ej] if ei == max else S[ei+1, ej]
        S[ei, ej-1] = S[ei, max] if ej == 1 else S[ei, ej-1]
        S[ei, ej+1] = S[ei, 1] if ej == max else S[ei, ej+1]
        dM = 2*S[ei, ej] #promjena magnetizacije
        dE = -2*Jv*S[ei, ej]*(S[ei+1, ej]+S[ei-1, ej]+S[ei, ej+1]+S[ei, ej-1])-2*S[ei, ej]*mH #promjena energije
        if dE > 0.0 and np.exp(-dE/kT) <= np.random.rand(): #odbacivanje promjene po Metropolisu
            S[ei, ej] = -S[ei, ej]
            dM = 0.0
            Naccept += 1.0
            dE = 0.0
        E0 += dE #osvjezenje energije
        M0 += dM #osvjezenje magnetizacije
        if ib > burn:
            Mavb += M0
            Mavb2 += M0*M0
            Eavb += E0
            Eavb2 += E0*E0
    if ib > burn: #zapisivanje podataka
        Eav += Eavb/Nk
        Eav2 += Eavb2/Nk
        Mav += Mavb/Nk
        Mav2 += Mavb2/Nk
        output1 = open('SpinUp.dat', 'w') #koordinate za spin-up
        output2 = open('SpinDown.dat', 'w') #koordinate za spin-down
        for j in range(1, max+1):
            for k in range(1, max+1):
                if S[j, k] == 1:
                    output1.write(f"{j:<3d} {k:<3d}\n")
                if S[j, k] == -1:
                    output2.write(f"{j:<3d} {k:<3d}\n")
        output1.close()
        output2.close()
        ko = ib-burn
        Edev = np.sqrt(Eav2/ko-(Eav/ko)**2)/np.sqrt(ko)
        Mdev = np.sqrt(Mav2/ko-(Mav/ko)**2)/np.sqrt(ko)
        output3.write(f"{ib:>6d} {M0/ko:>12.7f} {np.sqrt(Mdev):>12.7f}\n")
        output4.write(f"{ib:>6d} {Mav/ko:>12.7f}\n")
        output5.write(f"{ib:>6d} {E0/ko:>12.7f} {np.sqrt(Edev):>12.7f}\n")
        output6.write(f"{ib:>6d} {Eav/ko:>12.7f}\n")
output3.close()
output4.close()
output5.close()
output6.close()

accept = 1.0-Naccept/(Nk*(Nb+burn))

C = (Eav2/ko-(Eav/ko)**2)/kT**2 #toplinski kapacitet
sus = (Mav2/ko-(Mav/ko)**2)/kT #magnetska susceptibilnost
print("susceptibilnost po spinu \t", sus/max)
print("toplinski kapacitet po spinu \t", C/max)
print("udio prihvacanja \t", accept)
        