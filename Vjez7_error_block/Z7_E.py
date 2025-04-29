import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

'''
U ovom kodu racuna se standardna devijacija energetskih vrijednosti
iz datoteka E_dev.dat i E.txt.
'''

fEdev = np.loadtxt('E_dev.dat', comments='#', usecols=(0,1))
fE = np.loadtxt('E.txt', comments='#')
fstdev = open('st_dev_E.dat', 'w') #file za graf