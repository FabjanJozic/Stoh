import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as tick

N_max, k = 1e7, 5
x = []

#ovaj blok koda stvara datoteku s vrijednostima
'''with open('dev_val.txt', 'w') as wr:
    for i in range(1, int(N_max)+1):
        x.append(np.random.rand()) #generira random vrijednosti u rasponu [0,1]
        if i%10000 == 0: #korak za 10000 u N
            Ck = 0.0
            for j in range(1, i+1-k):
                Ck += x[j-1]*x[j-1+k]/i #sumacija za C(k)
            dev = abs(Ck-0.25)*np.sqrt(i) #racunanje devijacije
            lin = f"{i}\t{dev}\n"
            wr.write(lin)
    wr.close()'''

#ovaj blok koda cita vrijednosti iz datoteke    
with open('dev_val.txt', 'r') as re:
    R = re.readlines()
    X, Y = [], [] #N i dev liste
    for k in range(len(R)):
        val1, val2 = R[k].strip().split()
        X.append(float(val1))
        Y.append(float(val2))
    re.close()
    
fig = plt.figure(figsize=(10,5), dpi=120)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
axes.scatter(X, Y, color='red', s=1.0)
axes.set_xlim(0.0, N_max)
axes.set_ylim(0.0, 0.6)
axes.set_xlabel('N')
axes.set_ylabel('$|C(5)-0.25|\sqrt{N}$')
axes.xaxis.set_major_locator(tick.MultipleLocator(1e6))
axes.yaxis.set_major_locator(tick.MultipleLocator(0.1))
axes.set_title('C(5) korelacije za numpy.random generator')
axes.grid(lw=0.2, linestyle=':')
plt.show()