import numpy as np
import sys

sys.getdefaultencoding()

'''
Ovaj kod je optimiziran koristenjem numpy paketa. Vektorizacija
unutar numpya je brza od obicnih petlji za 2 reda velicine.
'''

n1 = 5000000
n2 = 400000
A = np.exp(1)/(np.exp(1)-1) #normalizacijska konstanta za p(x)=Ae^(-x)

# distribucija p(x)=1
r1 = np.random.random(n1)
x1 = r1
Fn1 = np.exp(-x1**2)
mean_Fn1 = np.mean(Fn1) #vrijednost funkcije F za n1
var1 = 0.0
for u in range(n1):
    var1 += (Fn1[u]-mean_Fn1)**2
var1f = np.sqrt(var1/(n1-1))

# distribucija p(x)=Ae^(-x)
r2 = np.random.random(n2)
x2 = -np.log(1-r2/A) #inverzna transformacija
Fn2 = np.exp(-x2**2)/(A*np.exp(-x2))
mean_Fn2 = np.mean(Fn2) #vrijednost funkcije F za n2
var2 = 0.0
for v in range(n2):
    var2 += (Fn2[v]-mean_Fn2)**2
var2f = np.sqrt(var2/(n2-1))

varn1, varn2 = var1f/np.sqrt(n1), var2f/np.sqrt(n2)

T1, T2, T3, T4 = 'n (uzoraka)', 'Fn', '\u03C3', '\u03C3/sqrt(n)'
with open('Z5_MC.txt', 'w', encoding='utf-8') as wr:
    wr.write(f"{T1:<12} {n1:10d} {n2:10d}\n")
    wr.write(f"{T2:<12} {mean_Fn1:10.5f} {mean_Fn2:10.5f}\n")
    wr.write(f"{T3:<12} {var1f:10.4f} {var2f:10.4f}\n")
    wr.write(f"{T4:<12} {varn1:10.5f} {varn2:10.5f}")
    wr.close()
