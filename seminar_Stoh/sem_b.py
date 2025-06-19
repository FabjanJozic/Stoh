import numpy as np

'''
Kod za rjesavanje b) seminarskog zadatka. Racunanje vrijenosti ⟨θ^2⟩, gdje je θ kut spina cestice u xy-ravnini,
te ln(N), gdje je N=L^2. Proucavanje ovisnosti ⟨θ^2⟩ o ln(N). Simulacija se održava na udjelu prihvacanja 40%.
'''

kT = 0.1 #fiksna temperatura za zadatak b)
beta = 1.0/kT
J = 1.0 #integral interakcije
Nk = 4 #broj Monte Carlo koraka po cestici
Nb_skip = 1500 #broj preskocenih blokova za ekvilibraciju
Nb = 10000 #broj blokova za mjerenje
acceptance = 0.4 #udio prihvacanja 40%

seed = 1208 #seed za nasumicni broj
rng = np.random.default_rng(seed)

Ls = [4, 8, 16, 32, 48, 64, 80, 96, 128] #razlicite velicine resetki
fTheta2 = open("f_theta2_vs_L.dat", "w")
fTheta2.write("# L  N  <theta^2>  ln(N)\n")

def E(theta, L): #funkcija energije sustava
        energy = 0.0
        for i in range(1, L+1):
            for j in range(1, L+1):
                right = theta[i+1, j] if i < L else theta[1, j] #rubni uvjeti
                up = theta[i, j+1] if j < L else theta[i, 1]
                delta1 = theta[i, j]-right
                delta2 = theta[i, j]-up
                energy += -J*(np.cos(delta1)+np.cos(delta2))
        return energy

def M(theta, L): #funkcija magnetizacije sustava
    mx = np.sum(np.cos(theta[1:L+1, 1:L+1]))
    my = np.sum(np.sin(theta[1:L+1, 1:L+1]))
    return np.sqrt(mx**2 + my**2)

def M_angle(theta, L): #kut magnetizacije u xy-ravnini
    mx = np.sum(np.cos(theta[1:L+1, 1:L+1]))
    my = np.sum(np.sin(theta[1:L+1, 1:L+1]))
    return np.arctan2(my, mx)

def theta2(theta, phi, L): #⟨θ^2⟩
    delta = theta[1:L+1, 1:L+1]-phi
    delta_wrapp = np.angle(np.exp(1j*delta))  #dobivanje kuta u intervalu [-π, π]
    return np.mean(delta_wrapp**2)

for iL in Ls: #petlja po velicinama resetke
    Theta = 2*np.pi*rng.random((iL+2, iL+2)) #matrica kuteva theta [0, 2π)

    dmax = 1.0
    max_dE = 20.0
    w_size = int(max_dE*1000)+1
    w = np.exp(-beta*np.linspace(0.0, max_dE, w_size))
    '''
    Kut theta je kontinuirana varijabla pa je i Boltzmannov faktor promjene energije sustava kontinuirana
    varijabla. Kreira se lista w, gdje je w[j] element ekvivalentan Boltzmannovom faktoru za promjenu
    energije sustava spinova, a j je cijeli broj jednak 1000*dE. Ovo daje rezoluciju energije od 0.001.
    Vrijednost max_dE predstavlja gornju granicu energije za sustav spinova |S(x,y)|=1 gdje se razmatra
    interakcija prvih susjeda, koja ne bi smjera premasiti E=16J, J=1.
    '''
    N = iL**2 #broj cestica u sustavu

    E0 = E(Theta, iL)
    accept = 0.0
    sum_theta2 = 0.0

    for ib in range(1, Nb_skip+Nb+1): #glavna petlja Metropolisovog algoritma
        for ik in range(Nk*N):
            i = rng.integers(1, iL+1)
            j = rng.integers(1, iL+1)

            Theta_old = Theta[i, j]
            dTheta = (rng.random()-0.5)*2*dmax
            Theta_new = (Theta_old+dTheta) % (2*np.pi)

            neighbors = [(i+1 if i < iL else 1, j),
                         (i-1 if i > 1 else iL, j),
                         (i, j+1 if j < iL else 1),
                         (i, j-1 if j > 1 else iL)] #rubni uvjeti

            dE = 0.0
            for x, y in neighbors:
                dE -= J*(np.cos(Theta_new-Theta[x, y])-np.cos(Theta_old-Theta[x, y]))

            if dE <= 0.0:
                Theta[i, j] = Theta_new
                E0 += dE
                accept += 1.0
            else:
                j_idx = int(1000*dE) #indeks j liste w[j]
                if j_idx < w_size and rng.random() < w[j_idx]:
                    Theta[i, j] = Theta_new
                    E0 += dE
                    accept += 1.0

        if ib > Nb_skip:
            phiM = M_angle(Theta, iL) #kut magnetizacije
            sum_theta2 += theta2(Theta, phiM, iL)

        if ib % 100 == 0:
            accept_ib = accept/(Nk*N*ib)
            if accept_ib > acceptance:
                dmax *= 1.05
            elif accept_ib < acceptance:
                dmax *= 0.95

    mean_theta2 = sum_theta2/Nb
    lnN = np.log(N)
    fTheta2.write(f"{iL:>4d} {N:>6d} {mean_theta2:>15.9f} {lnN:>12.7f}\n")

fTheta2.close()
