import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
import matplotlib.ticker as tick

dx = 2.0
P, rho = np.zeros((200, int(200.0/dx)+1)), np.zeros((200, int(200.0/dx)+1))
xpos = np.arange(-100.0, 100.0+dx, dx)

k = [5, 10, 15, 50] #trenutci u vremenu
X1, Y1, X2, Y2, X3, Y3, X4, Y4 = [], [], [], [], [], [], [], []

with open('probability.txt', 'r') as re1:
    R1 = re1.readlines()
    for i in range(len(R1)):
        val1 = R1[i].strip().split()
        for j in range(len(val1)):
            P[i, j] = float(val1[j])
    re1.close()
    
with open('diffusion.txt', 'r') as re2:
    R2 = re2.readlines()
    for i in range(len(R2)):
        val2 = R2[i].strip().split()
        for j in range(len(val2)):
            rho[i, j] = float(val2[j])
    re2.close()

text = 'walkers:   N=64000, x$_{i}$(t=0)=0.0\n\t\t$\u0394$x\u2208[-3,3] cm, $\u0394$t=1 s\ndiffusion: D=1.5 cm$^{2}$s$^{-1}$, $\u03C1$(x,t=0)=$\u03B4$(x) cm$^{-1}$\n\t\t$\u0394$x=2.0 cm, $\u0394$t=0.1 s'

fig = plt.figure(figsize=(10,7), dpi=120)
metadata = dict(title="Distributions")
plt.rcParams.update({'font.size': 15}) #type:ignore
writer = PillowWriter(fps=10, metadata=metadata) #type: ignore
with writer.saving(fig, "Walkers_Diffusion.gif", 120):
    for j in range(200):
        plt.clf()
        plt.plot(xpos, P[j, :], lw=1.0, color='cyan', label='P$_{walkers}$(x,t)')
        plt.plot(xpos, rho[j, :], lw=1.0, color='navy', label='P$_{diffusion}$(x,t)')
        plt.xlabel('$x$ / cm')
        plt.ylabel('P(x,t) / cm$^{-1}$')
        plt.legend(loc='upper right')
        plt.xlim(-100.0, 100.0)
        plt.ylim(0.0, 0.05)
        plt.text(50.0, 0.039, s='t={}s'.format(j), fontsize='medium')
        plt.text(-95.0, 0.039, s=text, fontsize='medium')
        plt.grid(lw=0.3, linestyle=':')
        writer.grab_frame()   