import numpy as np
import sys

sys.getdefaultencoding()

'''
Ovaj kod je optimiziran koristenjem numpy paketa. Vektorizacija
unutar numpya je brza od obicnih petlji za 2 reda veličine.
'''

n1 = 5000000
n2 = 400000
A = np.exp(1)/(np.exp(1)-1) #normalizacijska konstanta za p(x)=Ae^(-x)

# distribucija p(x)=1
r1 = np.random.random(n1)
x1 = r1
Fn1 = np.exp(-x1**2)
mean_Fn1 = np.mean(Fn1) #vrijednost funkcije F za n1
var1 = np.var(Fn1, ddof=0)

# distribucija p(x)=Ae^(-x)
r2 = np.random.random(n2)
x2 = -np.log(1-r2/A) #inverzna transformacija
Fn2 = np.exp(-x2**2)/(A*np.exp(-x2))
mean_Fn2 = np.mean(Fn2) #vrijednost funkcije F za n2
var2 = np.var(Fn2, ddof=0)

varn1, varn2 = var1/np.sqrt(n1), var2/np.sqrt(n2)

T1, T2, T3, T4 = 'n (uzoraka)', 'Fn', '\u03C3', '\u03C3/sqrt(n)'
with open('Z5_MC.txt', 'w', encoding='utf-8') as wr:
    wr.write(f"{T1:<12} {n1:10d} {n2:10d}\n")
    wr.write(f"{T2:<12} {mean_Fn1:10.7f} {mean_Fn2:10.7f}\n")
    wr.write(f"{T3:<12} {var1:10.7f} {var2:10.7f}\n")
    wr.write(f"{T4:<12} {varn1:10.7f} {varn2:10.7f}")
    wr.close()
