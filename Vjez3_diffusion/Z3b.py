import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

dx = 0.5
D = 1.5 #D=1.495273208054622 iz Z3a
dt = 0.05 #izracunato preko dx^2 => 2Ddt

Nx = int(200.0/dx)
Nt = int(200.0/dt)
left, right = 0.0, 0.0 #rubni uvjeti
alpha = D*dt/(dx**2)

dif1, dif2 = np.zeros(Nx+1), np.zeros(Nx+1)

def distribution(s): #funkcija raspodjele cestica za t=0
    if s > -0.8*dx and s < 0.8*dx:
        return 1.0/dx
    else:
        return 0.0

'''with open('diffusion.txt', 'w') as wr:
    lin0 = ""
    for p in range(len(dif1)): #pocetno stanje sustava
        dif1[p] = distribution(-100.0+p*dx)
        if (dif1[p] == 0.0 and dif1[p-1] == 1.0/dx): #za ocuvanje mase
            U = dif1[p-1]
            dif1[u-1] = U/2
        elif (dif1[p] == 1.0/dx and dif1[p-1] == 0.0):
            U = dif1[p]
            dif1[p] = U/2
        lin0 += f"%9.7f " %(distribution(-100.0+p*dx))
    lin0 += "\n"
    wr.write(lin0)
    for t in range(1, Nt): #koraci u vremenu
        lin = ""
        for x in range(1, Nx): #koraci po koordinatama
            dif2[x] = alpha*(dif1[x+1]+dif1[x-1])+(1-2*alpha)*dif1[x]
        dif2[0], dif2[-1] = left, right
        dif1 = np.copy(dif2)
        if t%int(1/dt) == 0:
            for xx in range(len(dif2)):
                lin += f"%9.7f " %(dif2[xx])
            lin += "\n"
            wr.write(lin)
    wr.close()'''
    
with open('diffusion.txt', 'r') as re:
    R = re.readlines()
    Dif = np.zeros((200, Nx+1))
    for i in range(len(R)):
        row = R[i].strip().split()
        for j in range(len(row)):
            Dif[i, j] = float(row[j])
            
xpos = np.arange(-100.0, 100.0+dx, dx)

fig = plt.figure(figsize=(10,7), dpi=120)
metadata = dict(title="Diffusion")
plt.rcParams.update({'font.size': 15}) #type:ignore
writer = PillowWriter(fps=15, metadata=metadata) #type: ignore
with writer.saving(fig, "diffusion.gif", 120):
    for j in range(200):
        plt.clf()
        plt.plot(xpos, Dif[j, :], lw=2.5, color='blue', label='$\u03C1$(x,t)')
        plt.xlabel('$x$ / cm')
        plt.ylabel('$\u03C1$(x,t) / cm$^{-1}$')
        plt.legend(loc='upper right')
        plt.xlim(-100.0, 100.0)
        plt.ylim(0.0, 0.2)
        plt.text(65.0, 0.17, s='t={}s'.format(j), fontsize='medium')
        plt.grid(lw=0.3, linestyle=':')
        writer.grab_frame()
    