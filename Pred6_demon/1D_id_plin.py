import numpy as np

N, nw = 40, 10 #broj cestica i setaca
Ed, Es = 0.0, 0.0 #energija demona i sustava*
E = 40 #energija sustava idealnog plina
v = np.zeros((N+1, nw+1))
v[0, :] = np.sqrt(2*E/N) #pocetne brzine
dv = 1.6

burn = 3000 #broj odbacenih koraka
Nk = 5000 #broj koraka
Es_s, Es_s2 = 0.0, 0.0
Ed_s, Ed_s2 = 0.0, 0.0

accept = 0
outputS = open('sustav_1Dplin.dat', 'w')
outputD = open('demon_1Dplin.dat', 'w')

for i in range(1, burn+Nk+1):
    Eak_D, Eak_S = 0.0, 0.0 #akumulirane vrijednosti energije
    for j in range(1, nw+1):
        iw = round(np.random.rand()*N)
        v_prob = v[iw, j]+dv*(np.random.rand()-0.5)
        dE = 0.5*(v_prob**2-v[iw, j]**2)
        if (dE < 0.0) or (dE > 0.0 and dE < Ed):
            v[iw, j] = v_prob
            Es += dE
            Ed -= dE
            accept += 1
        if i > burn:
            Eak_S += Es
            Eak_D += Ed
    Es_s += Eak_S/(nw*N)
    Es_s2 += Eak_S**2/(nw*N)**2
    Ed_s += Eak_D/(nw*N)
    Ed_s2 += Eak_D**2/(nw*N)**2
    if i > burn and i%10 == 0:
        ko = i-burn
        dels = Es_s2/ko-(Es_s/ko)**2
        sigmaS = np.sqrt(dels/ko)
        deld = Ed_s2/ko-(Ed_s/ko)**2
        sigmaD = np.sqrt(deld/ko)
        outputS.write(f"{i:>6d} {-np.sqrt(abs(Es_s/ko)):>14.8f} {np.sqrt(sigmaS):>14.8e}\n")
        outputD.write(f"{i:>6d} {np.sqrt(Ed_s/ko):>14.8f} {np.sqrt(sigmaD):>14.8e}\n")
accept /= (Nk+burn)*nw

print(accept)

outputS.close()
outputD.close()