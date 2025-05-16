import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

ES = 20.0 #energija sustava
N = 80 #broj cestica
ED = 0.0 #energija demona
dvMax = 1.4 #maksimalna promjena brzine v
burn = 1000 #odbaceni koraci
Nk = 10000 #ukupni broj koraka
Nw = 50 #broj setaca


#kod za racunanje energije sustava i demona
v = np.zeros((N, Nw))
v[:, :] = np.sqrt(2*ES/N) #pocetne brzine

def E(vel):
    # Energija cestice u 1D idealnom plinu.
    return 0.5*(vel**2)

accept = 0
output1 = open('ES.dat', 'w') #korak, energija sustava po koraku, ukupna energija sustava
output2 = open('ED.dat', 'w') #korak, energija demona po koraku, ukupna energija demona
output3 = open('P_ED.dat', 'w') #energija demona, razdioba

ctES, ctED = 0.0, 0.0 #kumulativna ukupna energija sustava i demona
count = 0
demon_E = np.zeros(Nw) #energija demona za svakog setaca

ED_max = 4.0 #maksimalna vrijednost energije demona
NED = 500 #broj intervala za energiju demona
dED = ED_max/NED
pED = np.zeros(NED+1) #funkcija razdiobe

for k in range(1, Nk+1):
    ESk, EDk = 0.0, 0.0 #energije po koraku
    for j in range(Nw):
        ip = np.random.randint(N) #indeks cestice
        dv = (2*np.random.rand()-1.0)*dvMax
        vTmp = v[ip, j]+dv
        dE = E(vTmp)-E(v[ip, j])
        if dE < 0.0 or demon_E[j] >= dE: #demon algoritam
            v[ip, j] = vTmp
            demon_E[j] -= dE
            accept += 1
        ESk += np.sum(E(v[:, j]))
        EDk += demon_E[j]
        id = int(demon_E[j]/dED) #indeks energije demona
        if id <= NED:
            pED[id] += 1
    if k >= burn and k%10 == 0: #racunanje srednjih vrijednosti i zapisivanje
        mESk = ESk/Nw
        mEDk = EDk/Nw
        ctES += mESk
        ctED += mEDk
        count += 1
        output1.write(f"{k:>6d} {mESk:>15.11f} {ctES/count:>15.11f}\n")
        output2.write(f"{k:>6d} {mEDk:>15.11f} {ctED/count:>15.11f}\n")

for i in range(NED+1): #racunanje razdiobe energije demona
    pED[i] /= dED*Nw*Nk
    output3.write(f"{i*dED:>8.5f} {pED[i]:>10.7f}\n")

output1.close()
output2.close()
output3.close()
print("\nacceptance rate = {} %\n".format(accept/(Nk*Nw)*100))


#kod za pisanje tablice
'''output4 = open('table.txt', 'w') #tablica za E=20 i N=80
input1 = np.loadtxt('ES.dat', usecols=2)
input2 = np.loadtxt('ED.dat', usecols=2)

mES = np.mean(input1) #srednja vrijednost ukupne energije sustava
mED = np.mean(input2) #srednja vrijednost ukupne energije demona
print(mES, mED)

output4.write(f"{'N':14s} {N:>8d}\n")
output4.write(f"{'E':14s} {ES+ED:>8.0f}\n")
output4.write(f"{'<ED>':14s} {mED:>8.1f}\n")
output4.write(f"{'<ES>':14s} {mES:>8.1f}\n")
output4.write(f"{'<ES>/N':14s} {mES/N:>8.5f}\n")
output4.write(f"{'<ES>/(N*<ED>)':14s} {mES/(N*mED):>8.3f}\n")
output4.write(f"{'0.5N*<ED>':14s} {0.5*N*mED:>8.0f}\n")
output4.close()'''


#kod za plotanje srednjih vrijednosti
'''input1 = np.loadtxt('ES.dat')
input2 = np.loadtxt('ED.dat')
step, mES_step, mED_step, mES_cu, mED_cu = [], [], [], [], []

for l in range(len(input1)):
    step.append(input1[l, 0])
    mES_step.append(input1[l, 1])
    mES_cu.append(input1[l, 2])
    mED_step.append(input2[l, 1])
    mED_cu.append(input2[l, 2])

fig = plt.figure(figsize=(8,5), dpi=110)
ax = fig.add_axes([0.10, 0.15, 0.85, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
ax.plot(step, mED_step, color='lime', lw=0.9, label='Srednja energija tijekom jednog koraka')
ax.plot(step, mED_cu, color='red', lw=1.0, label='Ukupna srednja energija nakon $is$ koraka')
ax.set_xlim(burn, Nk)
ax.set_ylim(0.3, 0.8)
ax.set_xlabel('$is$ / korak')
ax.set_ylabel('E$_{demon}$')
ax.xaxis.set_major_locator(tick.MultipleLocator(1000))
ax.yaxis.set_major_locator(tick.MultipleLocator(0.05))
#ax.grid(lw=0.2, linestyle=':')
ax.set_title('Idealni plin: N={}, E={}'.format(N, ES))
legend = ax.legend(loc='upper right')
legend.get_texts()[0].set_color('lime')
legend.get_texts()[1].set_color('red')
plt.show()'''