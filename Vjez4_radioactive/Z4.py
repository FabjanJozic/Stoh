import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

Sb133, Te133, I133 = 10000, 0, 0 #pocetni broj atoma
t_Sb133, t_Te133 = 2.5, 12.5 #vrijeme poluraspada Sb133 i Te133 u minutama

L_Sb, L_Te = np.log(2)/t_Sb133, np.log(2)/t_Te133
atoms = np.zeros(3, dtype=int) #lista s brojem atomskih jedinki
atoms[0] = Sb133
dt = 5.0
t0, tN = 0.0, 600.0 #pocetno i konacno vrijeme
p1, p2 = L_Sb*dt, L_Te*dt #vjerojatnosti prijelaza

with open('radiactive_decay.txt', 'w') as wr:
    wr.write(f"%6d %6d %6d %6.1f\n" %(atoms[0], atoms[1], atoms[2], t0))
    while t0 <= tN:
        n1, n2 = 1, 1
        N1, N2, N3 = atoms[0], atoms[1], atoms[2]
        if n1 <= N1:
            r1 = np.random.rand()
            if r1 <= p1:
                N1 -= 1
                N2 += 1
            else:
                n1 += 1
        if n2 <= N2:
            r2 = np.random.rand()
            if r2 <= p2:
                N2 -= 1
                N3 += 1
            else:
                n2 += 1
        else:
            atoms[0], atoms[1], atoms[2] = N1, N2, N3
        t0 += dt
        wr.write(f"%6d %6d %6d %6.1f\n" %(atoms[0], atoms[1], atoms[2], t0))
    wr.close()
        
        
    
