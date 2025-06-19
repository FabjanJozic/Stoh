import numpy as np

L = 16 #sirina resetke spinova (LxL)
kT0 = 0.5 #pocetna temperatura
dkT = 0.1
NkT = 10 #broj temperaturnih koraka
J = 1.0 #integral interakcije

Nb_skip = 1500 #broj preskocenih blokova za ekvilibraciju
Nb = 10000 #broj blokova
Nk = 1 #broj Monte Carlo koraka po cestici
target_accept = 0.4 #udio prihvacanja 40%

seed = 1208 #seed za Monte Carlo
rng = np.random.default_rng(seed)

fEne = open(f"f_E_{L}x{L}.dat", "w")
fMag = open(f"f_M_{L}x{L}.dat", "w")
fTCxEM = open(f"f_TCxEM_{L}x{L}.dat", "w")

fEne.write("# b - Eb - E - sigE\n")
fMag.write("# b - Mb - M - sigM\n")
fTCxEM.write("# T - C - chi - E - M\n")

Theta = 2 * np.pi * rng.random((L+2, L+2)) #matrica kuteva theta [0, 2π)

def E(theta): #funkcija energije sustava
    energy = 0.0
    for i in range(1, L+1):
        for j in range(1, L+1):
            right = theta[i+1, j] if i < L else theta[1, j] #rubni uvjeti
            up = theta[i, j+1] if j < L else theta[i, 1]
            delta1 = theta[i, j]-right
            delta2 = theta[i, j]-up
            energy += -J * (np.cos(delta1) + np.cos(delta2))
    return energy

def M(theta): #funkcija magnetizacije sustava
    mx = np.sum(np.cos(theta[1:L+1, 1:L+1]))
    my = np.sum(np.sin(theta[1:L+1, 1:L+1]))
    return np.sqrt(mx**2 + my**2)

for it in range(NkT + 1): #petlja po temperaturama
    kT = kT0+it*dkT #trenutna temperatura sustava
    beta = 1.0/kT
    dmax = 1.0 #delta theta
    E0 = E(Theta)
    M0 = M(Theta)
    
    max_dE = 20.0
    w_size = int(max_dE*1000)+1
    w = np.exp(-beta * np.linspace(0.0, max_dE, w_size))
    '''
    Kut theta je kontinuirana varijabla pa je i Boltzmannov faktor promjene energije sustava kontinuirana
    varijabla. Kreira se lista w, gdje je w[j] element ekvivalentan Boltzmannovom faktoru za promjenu
    energije sustava spinova, a j je cijeli broj jednak 1000*dE. Ovo daje rezoluciju energije od 0.001.
    Vrijednost max_dE predstavlja gornju granicu energije za sustav spinova |S(x,y)|=1 gdje se razmatra
    interakcija prvih susjeda, koja ne bi smjera premasiti E=16J, J=1.
    '''

    sum_bE = sum_bE2 = sum_bM = sum_bM2 = 0.0
    accept = 0.0

    for ib in range(1, Nb_skip+Nb+1): #glavna petlja Metropolisovog algoritma
        for ik in range(Nk*L*L):
            i = rng.integers(1, L+1)
            j = rng.integers(1, L+1)

            Theta_old = Theta[i, j]
            dTheta = (rng.random()-0.5)*2*dmax
            Theta_new = (Theta_old+dTheta) % (2*np.pi)

            neighbors = [(i+1 if i < L else 1, j),
                         (i-1 if i > 1 else L, j),
                         (i, j+1 if j < L else 1),
                         (i, j-1 if j > 1 else L)] #rubni uvjeti

            dE = 0.0
            for x, y in neighbors:
                dE -= J*(np.cos(Theta_new-Theta[x, y])-np.cos(Theta_old-Theta[x, y]))
            dE *= -J

            if dE <= 0.0:
                Theta[i, j] = Theta_new
                E0 += dE
            else:
                j_idx = int(1000*dE) #inteksi j liste w[j]
                if j_idx < w_size and rng.random() < w[j_idx]: #prihvacanja promjene energije sustava
                    Theta[i, j] = Theta_new
                    E0 += dE
                    accept += 1.0

        if ib > Nb_skip:
            M0 = M(Theta)
            sum_bE += E0
            sum_bE2 += E0**2
            sum_bM += M0
            sum_bM2 += M0**2

            Nb_eff = ib-Nb_skip
            mean_E = sum_bE/Nb_eff
            mean_E2 = sum_bE2/Nb_eff
            sigmaE = np.sqrt((mean_E2-mean_E**2)/Nb_eff)

            mean_M = sum_bM/Nb_eff
            mean_M2 = sum_bM2/Nb_eff
            sigmaM = np.sqrt((mean_M2-mean_M**2)/Nb_eff)

            fEne.write(f"{ib:>5d} {E0:>15.7f} {mean_E:>15.7f} {sigmaE:>15.7f}\n")
            fMag.write(f"{ib:>5d} {M0:>15.7f} {mean_M:>15.7f} {sigmaM:>15.7f}\n")

        if ib % 100 == 0:
            accept_ib = accept/(Nk*L*L*ib)
            if accept_ib > target_accept: #prilagodavanje maksimale vrijednosti kuta theta
                dmax *= 1.05
            elif accept_ib < target_accept:
                dmax *= 0.95

    mean_E = sum_bE/Nb
    mean_E2 = sum_bE2/Nb
    mean_M = sum_bM/Nb
    mean_M2 = sum_bM2/Nb

    C = (mean_E2-mean_E**2)/(kT**2*L**2) #toplinski kapacitet po cestici
    sus = (mean_M2-mean_M**2)/(kT*L**2) #magnetska susceptibilnost po cestici

    fTCxEM.write(f"{kT:>4.2f} {C:>15.9f} {sus:>15.9f} {mean_E/(L**2):>15.7f} {mean_M/(L**2):>15.7f}\n")

fEne.close()
fMag.close()
fTCxEM.close()
