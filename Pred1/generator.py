import matplotlib.pyplot as plt

I = [2]
c, a, m = 1, 7, 517
x, y = [], []

for i in range(1, 20001):
    I.append((a*I[-1]+c)%m)
    if i%2 == 0:
        x.append(I[i])
    else:
        y.append(I[i])
        
fig = plt.figure(figsize=(6,4), dpi=90)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.70])
plt.rcParams.update({'font.size': 10})           #type: ignore
axes.scatter(x, y, c='orange', edgecolor='red')
axes.grid(lw=0.2, linestyle=':')
plt.show()
