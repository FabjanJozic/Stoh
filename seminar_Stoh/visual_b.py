import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import numpy as np

f_data = np.loadtxt("f_theta2_vs_L.dat", comments='#')

theta2, lnN = [], []

for il in range(len(f_data)):
    theta2.append(f_data[il, 2])
    lnN.append(f_data[il, 3])


