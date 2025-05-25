import numpy as np

L = 16 #dimenzija resetke L*L
kT0 = 1.0 #podetna temperatura
dkT = 0.2
NkT = 15 #broj temperaturnih koraka (4.0-1.0)/0.2

Jv = 1.0 #integral izmjene
mH = 0.0 #magnetsko polje

Nb_skip = 200
Nk = 1000
Nb = 1000

write_spins_map = 0 #0=N, 1=Y

def E(s): #energija sustava
    sum_E = 0.0
    for i in range(1, L+1):
        for j in range(1, L+1):
            right = 1 if i == L else i+1
            up = 1 if j == L else j+1
            sum_E -= Jv*s[i, j]*(s[i, up]+s[right, j])+mH*s[i, j]
    return sum_E

def M(s): #magnetizacija sustava
    sum_M = 0.0
    for i in range(1, L+1):
        for j in range(1, L+1):
            sum_M += s[i, j]
    return sum_M

S = np.ones((L+2, L+2), dtype=int) #pocetna konfiguracija S[i,j]=1

fMag = open('f_M_{}x{}.dat'.format(L, L), 'w') #magnetizacija
fEne = open('f_E_{}x{}.dat'.format(L, L), 'w') #energija
fSmap = open('f_S_map_{}x{}.dat'.format(L, L), 'w') #mapa spinova
fTCxEM = open('f_TCxEM_{}x{}.dat'.format(L, L), 'w') #temperatura, toplinski kapacitet, susceptibilnost, energija, magnetizacija

fMag.write("#b - Mb - M - sigM\n")
fEne.write("#b - Eb - E - sigE\n")
fTCxEM.write("#T - C - x - E - M\n")

for it in range(NkT+1):
    kT = kT0+it*dkT #temperatura sustava
    sum_bE, sum_bM, sum_bE2, sum_bM2 = 0.0, 0.0, 0.0, 0.0
    reject = 0.0
    E0 = E(S) #pocetna energija
    M0 = M(S) #pocetna magnetizacija
    for ib in range(1, Nb_skip+Nb+1):
        sum_kE, sum_kM, sum_kE2, sum_kM2 = 0.0, 0.0, 0.0, 0.0
        for ik in range(1, Nk+1):
            ei = int(1.0+np.random.rand()*L)
            ej = int(1.0+np.random.rand()*L)
            S[ei, ej] *= -1
            S[ei-1, ej] = S[L, ej] if ei == 1 else S[ei-1, ej] #periodicni rubni uvjeti
            S[ei+1, ej] = S[1, ej] if ei == L else S[ei+1, ej]
            S[ei, ej-1] = S[ei, L] if ej == 1 else S[ei, ej-1]
            S[ei, ej+1] = S[ei, 1] if ej == L else S[ei, ej+1]
            dE = -2.0*Jv*S[ei, ej]*(S[ei+1, ej]+S[ei-1, ej]+S[ei, ej+1]+S[ei, ej-1])-2.0*S[ei, ej]*mH
            dM = 2.0*S[ei, ej]
            if (dE > 0.0) and (np.exp(-dE/kT) <= np.random.rand()):
                S[ei, ej] = S[ei, ej]*(-1) #odbacivanje promjene spina
                reject += 1.0
                dE = 0.0
                dM = 0.0
            E0 += dE
            M0 += dM
            if ib > Nb_skip: #sakupljanje i uprosjecivanje energije i magnetizacije
                sum_kE += E0
                sum_kE2 += E0**2
                sum_kM += M0
                sum_kM2 += M0**2
        if ib > Nb_skip:
            sum_bE += sum_kE/Nk
            sum_bE2 += sum_kE2/Nk
            sum_bM += sum_kM/Nk
            sum_bM2 += sum_kM2/Nk
            if write_spins_map == 1: #zapisivanje mapa spinova
                for i in range(1, L+1):
                    for j in range(1, L+1):
                        fSmap.write(f"{i:>3d} {j:>3d} {S[i, j]:>3d}\n")
                fSmap.write("\n\n")
            Nb_eff = ib-Nb_skip
            mean_E = sum_bE/Nb_eff
            mean_E2 = sum_bE2/Nb_eff
            sigmaE = np.sqrt((mean_E2-mean_E**2)/Nb_eff)
            fEne.write(f"{ib:>5d} {sum_kE/Nk:>15.7f} {mean_E:>15.7f} {sigmaE:>15.7f}\n")
            mean_M = sum_bM/Nb_eff
            mean_M2 = sum_bM2/Nb_eff
            sigmaM = np.sqrt((mean_M2-mean_M**2)/Nb_eff)
            fMag.write(f"{ib:>5d} {sum_kM/Nk:>15.7f} {mean_M:>15.7f} {sigmaM:>15.7f}\n")
    fEne.write("\n\n")
    fMag.write("\n\n")
    C = (mean_E2-mean_E**2)/(kT**2) #toplinski kapacitet
    sus = (mean_M2-mean_M**2)/kT #susceptibilnost
    fTCxEM.write(f"{kT:>4.1f} {C/(L**2):>15.9f} {sus/(L**2):>15.9f} {mean_E/(L**2):>15.7f} {mean_M/(L**2):>15.7f}\n")
    reject /= Nk*(Nb+Nb_skip)
    print("-------------------------------------------\n")
    print("<E> = {}\n".format(mean_E))
    print("T = {} K\n".format(kT))
    print("acceptance = {} %\n".format((1.0-reject)*100))
    print("-------------------------------------------\n")
    
fMag.close()
fEne.close()
fSmap.close()
fTCxEM.close()
            