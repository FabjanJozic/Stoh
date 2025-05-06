import random
import math

max = 32  # broj spinova u 1 smjeru
kt = 2.0  # temperatura
Jv = 1.0  # energija izmjene

def ran1(idum):
    return random.random()

def energy(s):
    sum = 0.0
    for i in range(1, max + 1):
        for j in range(1, max + 1):
            desno = 1 if i == max else i + 1
            gore = 1 if j == max else j + 1
            sum += s[i][j] * (s[i][gore] + s[desno][j])
    return -Jv * sum

def magnet(s):
    sum = 0.0
    for i in range(1, max + 1):
        for j in range(1, max + 1):
            sum += s[i][j]
    return sum

output3 = open("magnet_2d_2p.dat", "w")
output4 = open("energy_2d_2p.dat", "w")
output5 = open("magnetKan22d_2p.dat", "w")
output6 = open("energy_block_2p.dat", "w")
output7 = open("magnet_block_2p.dat", "w")

magn = 0.0  # magnetizacija
eav = 0.0   # energija
eav2 = 0.0   # kvadrat energije
magn2 = 0.0  # kvadrat magnetizacije
nsteps = 1000
nblocks = 5000
ngr = 1500  # broj koraka koji se odbacuje
accept = 0.0

s = [[1 for _ in range(max + 2)] for _ in range(max + 2)]
E = energy(s)   # pocetna energija
print("initial\t\t energy\t\t", E)
magk = magnet(s)  # pocetna magnetizacija
print("initial\t\t magnetisation \t\t", magk)

for ib in range(1, nblocks + 1):
    eavb = 0.0    # energija u bloku
    eav2b = 0.0   # kvadrat energije u bloku
    magnb = 0.0    # magnetizacija u bloku
    magn2b = 0.0   # kvadrat magnetizacije u bloku
    for _ in range(1, nsteps + 1):  # petlja po koracima
        ei = int(1.0 + ran1(-1) * max)  # slucajan odabir elementa od 1 do max
        ej = int(1.0 + ran1(-1) * max)
        s[ei][ej] *= -1  # preokret spina
        s[ei-1][ej]=s[max][ej] if ei == 1 else  s[ei-1][ej] # periodicni rubni uvjeti
        s[ei+1][ej]=s[1][ej] if ei == max else s[ei+1][ej]
        s[ei][ej-1]=s[ei][max] if ej == 1 else s[ei][ej-1]
        s[ei][ej+1]=s[ei][1] if ej == max else s[ei][ej+1]
        dm = 2.0 * s[ei][ej]  # razlika magnetizacije
        dE = -2.0 * Jv * s[ei][ej] * (s[ei+1][ej] + s[ei - 1][ej] + s[ei][ej+1] + s[ei][ej - 1])  # razlika energije
        if dE > 0 and math.exp(-dE / kt) <= random.random():
            s[ei][ej] = -s[ei][ej]  # Metropolis - odbacivanje promjene
            dm = 0.0
            accept += 1.0 / nsteps / nblocks
            dE = 0.0
        E += dE  # osvjezivanje energije
        magk += dm  # osvjezivanje magnetizacije
        if ib > ngr:
            magnb += magk
            magn2b += magk * magk
            eavb += E
            eav2b += E * E
    if ib > ngr:  # skupljanje prosječnih vrijednosti
        eav += eavb / nsteps
        eav2 += eav2b / nsteps
        magn += magnb / nsteps
        magn2 += magn2b / nsteps
        output1 = open("spin-up2d_2p.dat", "w")  # spinovi gore i dolje u dva dokumenta
        output2 = open("spin-down2d_2p.dat", "w")
        for j in range(1, max + 1):  # spremanje "mape"spinova
            for k in range(1, max + 1):
                if s[j][k] == 1:
                    output1.write(f"{j}  {k}\n")
                if s[j][k] == -1:
                    output2.write(f"{j}  {k}\n")
        output1.close()
        output2.close()
        ko = ib - ngr
        endev = math.sqrt(eav2 / ko - eav * eav / ko / ko) / math.sqrt(ko)
        magdev = math.sqrt(magn2 / ko - magn * magn / ko / ko) / math.sqrt(ko)
        output3.write(f"{ib}\t{magn / (ib - ngr)}\t{magdev}\n")
        output4.write(f"{ib}\t{eav / (ib - ngr)}\t{endev}\n")
        output5.write(f"{ib}\t{magn2 / (ib - ngr)}\n")
        output7.write(f"{ib}\t{magnb / nsteps}\n")
        output6.write(f"{ib}\t{eavb / nsteps}\n")

c = (eav2 / ko - (eav / ko) ** 2) / kt ** 2
sus = (magn2 / ko - (magn / ko) ** 2) / kt
print("susceptibilnost po spinu \t", sus / max)
print("toplinski kapacitet po spinu \t", c / max)
print("udio prihvacanja \t", 1.0 - accept)

output3.close()
output4.close()
output5.close()
output6.close()
output7.close()

print("podaci spremljeni u spin-up2d.dat, spin-down2d.dat")

