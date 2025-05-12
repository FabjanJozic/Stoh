import numpy as np

ES = 20.0 #energija sustava
N = 80 #broj cestica
ED = 0.0 #energija demona
dvMax = 0.4 #maksimalna promjena brzine v
burn = 1000 #odbaceni koraci
Nk = 10000 #ukupni broj koraka
Nw = 40 #broj setaca

v = np.zeros((N, Nw))
v[0, :] = np.sqrt(2*ES/N) #pocetne brzine

def E(vel):
    '''Energija cestice u 1D idealnom plinu.'''
    return 0.5*(vel**2)

accept = 0
output1 = open('ES.dat', 'w') #korak, energija sustava, ukupna energija sustava
output2 = open('ED.dat', 'w') #korak, energija demona, ukupna energija demona
output3 = open('table.txt', 'w') #tablica za ES=20 i N=80

dES, dED = 0.0, 0.0
mES, mED = 0.0, 0.0

for k in range(1, Nk+1):
    ESk, EDk = 0.0, 0.0 #energije po koraku
    for j in range(Nw):
        ip = int(np.random.rand()*N)
        if ip == N:
            ip = N-1
        dv = (2*np.random.rand()-1.0)*dvMax
        vTmp = v[ip, j]+dv
        dE = E(vTmp)-E(v[ip, j])
        if dED >= dE: #demon algoritam
            v[ip, j] = vTmp
            dED -= dE
            dES += dE
            accept += 1
        if k >= burn:
            ESk += dES
            EDk += dED
    mES += ESk/Nw
    mED += EDk/Nw
    if k >= burn and k%10 == 0:
        ko = k-burn+1
        output1.write(f"{k:>6d} {mES/ko+ES:>15.11f} {dES+ES:>15.11f}\n")
        output2.write(f"{k:>6d} {mED/ko+ED:>15.11f} {dED+ED:>15.11f}\n")

output1.close()
output2.close()

fES = ES+dES #konacna energija po cestici
fED = ED+dED

accept /= Nk*Nw
print(accept*100, fES, fED, fES+fED)

output3.write(f"{'N':14s} {N:>8d}\n")
output3.write(f"{'E':14s} {ES+ED:>8.0f}\n")
output3.write(f"{'<ED>':14s} {fED:>8.1f}\n")
output3.write(f"{'<ES>':14s} {fES:>8.1f}\n")
output3.write(f"{'<ES>/N':14s} {fES/N:>8.5f}\n")
output3.write(f"{'<ES>/(N*<ED>)':14s} {fES/(N*fED):>8.3f}\n")
output3.write(f"{'0.5N*<ED>':14s} {0.5*N*fED:>8.0f}\n")
output3.close()