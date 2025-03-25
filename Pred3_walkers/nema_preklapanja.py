import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

Nw = 3 #broj setaca
Nk = 100 #broj koraka

walkers = np.zeros((Nw, 2), dtype=int) #prva lista
moves = [(1, 0), (-1, 0), (0, 1), (0, -1)] #moguci koraci
full_positions = [set([(0, 0)]) for n in range(Nw)] #lista za biljezenje pojedinacnih koraka
visited_positions = set((0, 0)) #lista za biljezenje globalnih koraka

def R(x, y): #udaljenost od ishodista
    return np.sqrt(x**2 + y**2)

with open('SAW3.txt', 'w') as wr:
    for w in range(Nw):
        wr.write(f"{0:8d}{0:8d}{0:12.4f}") #pocetne pozicije
    wr.write("\n")
    for k in range(Nk):
        lin = ""
        for w in range(Nw):
            np.random.shuffle(moves)  #randomiziranje koraka
            je_nije = False
            for dx, dy in moves:
                new_x, new_y = walkers[w, 0]+dx, walkers[w, 1]+dy
                if (new_x, new_y) not in visited_positions and (new_x, new_y) not in full_positions[w]:  #provjeri je li moguc pomak
                    walkers[w, 0], walkers[w, 1] = new_x, new_y
                    visited_positions.add((new_x, new_y))
                    full_positions[w].add((new_x, new_y))
                    moved = True
                    break
            if not je_nije:  #pamti se zadnja pozicija setaca koji zapne
                new_x, new_y = walkers[w, 0], walkers[w, 1]
            r = R(new_x, new_y)
            lin += f"{new_x:8d}{new_y:8d}{r:12.4f}"
        lin += "\n"
        wr.write(lin)

with open('SAW3.txt', 'r') as re:
    R = re.readlines()
    X1, Y1, X2, Y2, X3, Y3 = [], [], [], [], [], []
    for l in range(len(R)):
        val = R[l].strip().split()
        for i in range(len(val)):
            if i == 0:
                X1.append(float(val[i]))
                Y1.append(float(val[i+1]))
            elif i == 3:
                X2.append(float(val[i]))
                Y2.append(float(val[i+1]))
            elif i == 6:
                X3.append(float(val[i]))
                Y3.append(float(val[i+1]))
                           
fig = plt.figure(figsize=(6,6), dpi=110)
axes = fig.add_axes([0.15, 0.15, 0.75, 0.70])
plt.rcParams.update({'font.size': 10}) #type: ignore
plt.axis('equal')
axes.scatter(0.0, 0.0, color='black', s=15, label='start')
axes.plot(X1, Y1, color='red', lw=1.0, label='walker 1')
axes.plot(X2, Y2, color='blue', lw=1.0, label='walker 2')
axes.plot(X3, Y3, color='lime', lw=1.0, label='walker 3')
axes.grid(lw=0.3, linestyle=':')
axes.xaxis.set_major_locator(tick.MultipleLocator(1))
axes.yaxis.set_major_locator(tick.MultipleLocator(1))
axes.set_xticklabels([])
axes.set_yticklabels([])
axes.legend()
plt.show()