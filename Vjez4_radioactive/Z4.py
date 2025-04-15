import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

Sb133, Te133, I133 = 10000, 0, 0 #pocetni broj atoma
t_Sb133, t_Te133 = 2.5, 12.5 #vrijeme poluraspada Sb133 i Te133 u minutama

L_Sb, L_Te = np.log(2)/t_Sb133, np.log(2)/t_Te133
atoms = np.zeros(3, dtype=int) #lista s brojem atomskih jedinki
atoms[0] = Sb133
dt = 1.0
t0, tN = 0.0, 60.0 #pocetno i konacno vrijeme
p1, p2 = L_Sb*dt, L_Te*dt #vjerojatnosti prijelaza

#kod za numericno racunanje
with open('num_decay_dt1.txt', 'w') as wr:
    wr.write(f"%6d %6d %6d %8.1f\n" %(atoms[0], atoms[1], atoms[2], t0))
    while t0 < tN:
        N1, N2, N3 = atoms[0], atoms[1], atoms[2]
        decayed_1_to_2 = np.sum(np.random.rand(N1) < p1) #ukupni broj raspada svih preostalih Sb u Te
        decayed_2_to_3 = np.sum(np.random.rand(N2) < p2) #ukupni broj raspada svih preostalih Te u I
        N1 -= decayed_1_to_2
        N2 += decayed_1_to_2 - decayed_2_to_3
        N3 += decayed_2_to_3
        atoms[0], atoms[1], atoms[2] = N1, N2, N3
        t0 += dt
        wr.write(f"%6d %6d %6d %8.1f\n" %(atoms[0], atoms[1], atoms[2], t0))
    wr.close()
        
#kod za analiticko
'''with open('ana_decay_dt1.txt', 'w') as wr:
    wr.write(f"%8.1f %8.1f %8.1f %8.1f\n" %(Sb133, Te133, I133, t0))
    Sb, Te, I, t = np.zeros(int(tN/dt)+1), np.zeros(int(tN/dt)+1), np.zeros(int(tN/dt)+1), np.zeros(int(tN/dt)+1)
    Sb[0] = Sb133
    for j in range(1, int(tN/dt)+1):
        Sb[j] = Sb[0]*np.exp(-L_Sb*j*dt)
        Te[j] = Sb[0]*L_Sb/(L_Te-L_Sb)*(np.exp(-L_Sb*j*dt)-np.exp(-L_Te*j*dt))
        I[j] = Sb[0]-(Sb[j]+Te[j])
        t[j] = j*dt
        wr.write(f"%8.1f %8.1f %8.1f %8.1f\n" %(Sb[j], Te[j], I[j], t[j]))
    wr.close()'''
    
with open('ana_decay_dt1.txt', 'r') as re1:
    R1 = re1.readlines()
    aSb, aTe, aI, T = [], [], [], []
    for i in range(len(R1)):
        val1, val2, val3, val4 = R1[i].strip().split()
        aSb.append(float(val1))
        aTe.append(float(val2))
        aI.append(float(val3))
        T.append(float(val4))
    re1.close()

with open('num_decay_dt1.txt', 'r') as re2:
    R2 = re2.readlines()
    nSb, nTe, nI = [], [], []
    for i in range(len(R2)):
        val1, val2, val3, val4 = R2[i].strip().split()
        nSb.append(float(val1))
        nTe.append(float(val2))
        nI.append(float(val3))
    re2.close()
       
fig = plt.figure(figsize=(10,5), dpi=120)
axes = fig.add_axes([0.15, 0.15, 0.80, 0.80])
plt.rcParams.update({'font.size': 10}) #type: ignore
axes.plot(T, aSb, lw=2.0, linestyle=':', color='blue', label='$^{133}$Sb - analytical')
axes.scatter(T, nSb, s=8, edgecolor='black', color='blue', label='$^{133}$Sb - numerical')
axes.plot(T, aTe, lw=2.0, linestyle=':', color='lime', label='$^{133}$Te - analytical')
axes.scatter(T, nTe, s=8, edgecolor='black', color='lime', label='$^{133}$Te - numerical')
axes.plot(T, aI, lw=2.0, linestyle=':', color='purple', label='$^{133}$I - analytical')
axes.scatter(T, nI, s=5, edgecolor='black', color='purple', label='$^{133}$I - numerical')
axes.set_xlim(0.0, 60.0)
axes.set_ylim(0.0, 10000.0)
axes.set_xlabel('time / min')
axes.set_ylabel('number of atomic nuclei')
axes.xaxis.set_major_locator(tick.MultipleLocator(5))
axes.yaxis.set_major_locator(tick.MultipleLocator(1000))
axes.grid(lw=0.2, linestyle=':')
axes.set_title("$^{133}$Sb - $^{133}$Te - $^{133}$I chain radioactive decay, $\u0394$t=1.0 min")
axes.legend()
plt.show()

'''with open('num_decay_dt02.txt', 'r') as re1:
    R1 = re1.readlines()
    Sb1, T1 = [], []
    for i in range(len(R1)):
        val1, val2, val3, val4 = R1[i].strip().split()
        Sb1.append(float(val1))
        T1.append(float(val4))
    re1.close()

with open('num_decay_dt05.txt', 'r') as re2:
    R2 = re2.readlines()
    Sb2, T2 = [], []
    for i in range(len(R2)):
        val1, val2, val3, val4 = R2[i].strip().split()
        Sb2.append(float(val1))
        T2.append(float(val4))
    re2.close()

with open('num_decay_dt1.txt', 'r') as re3:
    R3 = re3.readlines()
    Sb3, T3 = [], []
    for i in range(len(R3)):
        val1, val2, val3, val4 = R3[i].strip().split()
        Sb3.append(float(val1))
        T3.append(float(val4))
    re3.close()

with open('num_decay_dt5.txt', 'r') as re4:
    R4 = re4.readlines()
    Sb4, T4 = [], []
    for i in range(len(R4)):
        val1, val2, val3, val4 = R4[i].strip().split()
        Sb4.append(float(val1))
        T4.append(float(val4))
    re4.close()

fig = plt.figure(figsize=(10,5), dpi=120)
axes = fig.add_axes([0.15, 0.15, 0.80, 0.80])
plt.rcParams.update({'font.size': 10}) #type: ignore
axes.plot(T1, Sb1, lw=1.3, color='black', label='$\u0394$t=0.2 min')
axes.plot(T2, Sb2, lw=1.3, color='darkred', label='$\u0394$t=0.5 min')
axes.plot(T3, Sb3, lw=1.3, color='red', label='$\u0394$t=1.0 min')
axes.plot(T4, Sb4, lw=1.3, color='orange', label='$\u0394$t=5.0 min')
axes.set_xlim(0.0, 10.0)
axes.set_ylim(0.0, 10000.0)
axes.set_xlabel('time / min')
axes.set_ylabel('number of $^{133}$Sb atomic nuclei')
axes.xaxis.set_major_locator(tick.MultipleLocator(1))
axes.yaxis.set_major_locator(tick.MultipleLocator(1000))
axes.grid(lw=0.2, linestyle=':')
axes.set_title("Numerical $^{133}$Sb decay rate")
axes.legend()
plt.show()'''