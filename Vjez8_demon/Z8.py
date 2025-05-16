import numpy as np

ES = 20.0 #energija sustava
N = 80 #broj cestica
ED = 0.0 #energija demona
dvMax = 0.9 #maksimalna promjena brzine v
burn = 1000 #odbaceni koraci
Nk = 10000 #ukupni broj koraka
Nw = 50 #broj setaca

v = np.zeros((N, Nw))
v[0, :] = np.sqrt(2*ES/N) #pocetne brzine

def E(vel):
    '''Energija cestice u 1D idealnom plinu.'''
    return 0.5*(vel**2)

accept = 0
output1 = open('ES.dat', 'w') #korak, energija sustava po koraku, ukupna energija sustava
output2 = open('ED.dat', 'w') #korak, energija demona po koraku, ukupna energija demona

dES, dED = 0.0, 0.0

for k in range(1, Nk+1):
    ESk, EDk = 0.0, 0.0 #energije po koraku
    for j in range(Nw):
        ip = int(np.random.rand()*N) #indeks cestice
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
    if k >= burn and k%10 == 0:
        ko = k-burn+1
        output1.write(f"{k:>6d} {ESk/Nw+ES:>15.11f} {dES+ES:>15.11f}\n")
        output2.write(f"{k:>6d} {EDk/Nw+ED:>15.11f} {dED+ED:>15.11f}\n")

output1.close()
output2.close()
print("\nacceptance rate = {} %\n".format(accept/(Nk*Nw)*100))

output3 = open('table.txt', 'w') #tablica za E=20 i N=80
input1 = np.loadtxt('ES.dat', usecols=2)
input2 = np.loadtxt('ED.dat', usecols=2)

mES = np.mean(input1) #srednja vrijednost ukupne energije sustava
mED = np.mean(input2) #srednja vrijednost ukupne energije demona
print(mES, mED)

output3.write(f"{'N':14s} {N:<8d}\n")
output3.write(f"{'E':14s} {ES+ED:<8.0f}\n")
output3.write(f"{'<ED>':14s} {mED:<8.1f}\n")
output3.write(f"{'<ES>':14s} {mES:<8.1f}\n")
output3.write(f"{'<ES>/N':14s} {mES/N:<8.5f}\n")
output3.write(f"{'<ES>/(N*<ED>)':14s} {mES/(N*mED):<8.3f}\n")
output3.write(f"{'0.5N*<ED>':14s} {0.5*N*mED:<8.0f}\n")
output3.close()