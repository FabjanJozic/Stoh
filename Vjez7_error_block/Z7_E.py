import numpy as np

'''
U ovom kodu racuna se standardna devijacija energetskih vrijednosti iz E.txt.
'''

#fEdev = np.loadtxt('E_dev.dat', comments='#', usecols=(0,1))
fE = np.loadtxt('E.txt', comments='#')
fstdev = open('st_dev_E.dat', 'w') #file za graf

N = len(fE)
for Nk in range(1, 201):
    Nb = N//Nk #broj blokova
    Sbf = 0.0
    Sbf2 = 0.0
    idx = 0
    while idx < N:
        Sfk = 0.0
        nepun = False
        if idx+Nk <= N: #za puni blok
            for _ in range(Nk):
                Sfk += fE[idx][1]
                idx += 1
            n = Nk
        else: #za nepotpuni blok
            nepun = True
            preostali = N-idx #preostali neukljuceni retci
            for __ in range(preostali):
                Sfk += fE[idx][1]
                idx += 1
            n = preostali
        Sbf += Sfk/n #akumulirano dijelim sa brojem linija u bloku i dodaje srednjem po blokovima
        Sbf2 += (Sfk*Sfk)/(n*n)
        Nb += 1
    if Nb > 1: #standardna devijacija usrednjena po bloku
        st_dev = ((Sbf2/Nb)-(Sbf/Nb)**2)/(Nb-1)
        fstdev.write(f"{Nk:>5d} {np.sqrt(st_dev):>10.6f}\n")
    else:
        fstdev.write(f"{Nk:>5d} {0.0:>10.6f}\n")

fstdev.close()