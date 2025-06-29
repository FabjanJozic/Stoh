import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

fE32_50 = np.loadtxt('energy_32x32_Nbskip50.dat', comments='#')
fE32_150 = np.loadtxt('energy_32x32_Nbskip150.dat', comments='#')
fE64 = np.loadtxt('energy_64x64.dat', comments='#')

