import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import numpy as np

f_data = np.loadtxt("f_theta2_vs_L.dat", comments='#')

theta2, lnN = [], []

for il in range(len(f_data)):
    theta2.append(f_data[il, 2])
    lnN.append(f_data[il, 3])

fig = plt.figure(figsize=(9,4), dpi=120)
axes = fig.add_axes([0.10, 0.15, 0.85, 0.80])
plt.rcParams.update({'font.size': 10}) #type: ignore
axes.plot(lnN, theta2, lw=0.9, linestyle='--', color='purple', zorder=0)
axes.scatter(lnN, theta2, color='black', marker='d', s=40, zorder=1)
axes.set_xlim(2.5, 12.0)
axes.set_ylim(-0.1, 2.8)
axes.set_xlabel('ln($N$)')
axes.set_ylabel('<$\u03B8^{2}$> / rad$^{2}$')
axes.xaxis.set_major_locator(tick.MultipleLocator(0.5))
axes.yaxis.set_major_locator(tick.MultipleLocator(0.3))
axes.text(2.8, 2.4, '$N = L^{2}$\n$\u03B8$'+r' = $\angle(M, S(x,y))$')
plt.show()
