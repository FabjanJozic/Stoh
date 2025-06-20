import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import numpy as np

f_data = np.loadtxt("f_theta2_vs_L.dat", comments='#')

theta2, lnN, sigma = [], [], []

for il in range(len(f_data)):
    theta2.append(f_data[il, 2])
    lnN.append(f_data[il, 4])
    sigma.append(100*f_data[il, 3])

fig = plt.figure(figsize=(9,4), dpi=120)
axes = fig.add_axes([0.10, 0.15, 0.85, 0.80])
plt.rcParams.update({'font.size': 13}) #type: ignore
axes.errorbar(lnN, theta2, yerr=sigma, fmt='o', capsize=3, label=r'$\langle\theta^{2}\rangle$ $\pm$ $10^{2}\sigma$', ecolor='red',
              elinewidth=0.4, mfc='black', mec='black', ms=4, mew=2, color='purple', linestyle='--', lw=0.6)
axes.set_xlim(2.4, 12.1)
axes.set_ylim(-0.4, 3.1)
axes.set_xlabel('ln($N$)')
axes.set_ylabel(r'$\langle\theta^{2}\rangle$ / rad$^{2}$')
axes.xaxis.set_major_locator(tick.MultipleLocator(0.5))
axes.yaxis.set_major_locator(tick.MultipleLocator(0.3))
axes.text(2.6, 2.1, '$N = L^{2}$\n$\u03B8$'+r' = $\angle(M, S(x,y))$')
axes.legend(loc='best')
axes.grid(lw=0.2, linestyle=':')
plt.show()
