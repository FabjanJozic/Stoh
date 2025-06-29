import numpy as np

# Parametri
L = 32
T0 = 10.0
T_quench = 0.5
J = 1.0
N = L * L

Nk = 10
Nb_skip = 150
Nb0 = 150
Nb = 300
Nsim = 10

acceptance = 0.4
dmax = 1.0
seed = 1208

# Periodični rubni uvjeti
def pbc(i, L):
    return 1 if i > L else (L if i < 1 else i)

def E(theta, L):
    energy = 0.0
    for i in range(1, L+1):
        for j in range(1, L+1):
            right = theta[pbc(i+1, L)][j]
            up = theta[i][pbc(j+1, L)]
            delta1 = theta[i][j] - right
            delta2 = theta[i][j] - up
            energy += -J * (np.cos(delta1) + np.cos(delta2))
    return energy

def count_vortices_with_positions(Theta, L):
    vortices = []
    antivortices = []
    for i in range(1, L):
        for j in range(1, L):
            angles = [
                Theta[i, j],
                Theta[i+1, j],
                Theta[i+1, j+1],
                Theta[i, j+1]
            ]
            dtheta = np.angle(np.exp(1j * np.diff(angles + [angles[0]])))
            winding = np.sum(dtheta)
            if np.isclose(winding, 2*np.pi, atol=0.5):
                vortices.append((i, j))
            elif np.isclose(winding, -2*np.pi, atol=0.5):
                antivortices.append((i, j))
    return vortices, antivortices

# Priprema datoteka
f_energy_log = open("energy_{L}x{L}.dat", "w")
f_mean_vortices = open("mean_vortices.dat", "w")
f_mean_vortex_stats = open("vortex_statistics_mean.dat", "w")
f_theta_map_series = open("theta_map_{L}x{L}.dat", "w")
f_vortices_all = open("vortices_all.dat", "w")

f_energy_log.write("# is - ib - Eb - E - sigma_E T\n")
f_mean_vortices.write("# is - mean_vortices - mean_antivortices\n")
f_vortices_all.write("# i - j - type - step\n")

rng = np.random.default_rng(seed)
total_vortex_sum = 0
total_antivortex_sum = 0

for sim in range(1, Nsim + 1):
    Theta = 2 * np.pi * rng.random((L + 2, L + 2))
    T = T0
    beta = 1.0 / T
    max_dE = 20.0
    w_size = int(max_dE * 1000) + 1
    w = np.exp(-beta * np.linspace(0.0, max_dE, w_size))

    E0 = E(Theta, L)
    accept = 0.0
    sum_E = 0.0
    sum_E2 = 0.0
    measure_counter = 0
    vortex_sum = 0
    antivortex_sum = 0

    for ib in range(1, Nb_skip + Nb0 + Nb_skip + Nb + 1):
        if ib == Nb_skip + Nb0 + 1:
            T = T_quench
            beta = 1.0 / T
            w = np.exp(-beta * np.linspace(0.0, max_dE, w_size))

        for ik in range(Nk * N):
            i = rng.integers(1, L+1)
            j = rng.integers(1, L+1)

            Theta_old = Theta[i, j]
            dTheta = (rng.random() - 0.5) * 2 * dmax
            Theta_new = (Theta_old + dTheta) % (2*np.pi)

            neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
            dE = 0.0
            for x, y in neighbors:
                x, y = pbc(x, L), pbc(y, L)
                dE -= J * (np.cos(Theta_new - Theta[x, y]) - np.cos(Theta_old - Theta[x, y]))

            if dE <= 0.0 or (int(1000*dE) < w_size and rng.random() < w[int(1000*dE)]):
                Theta[i, j] = Theta_new
                E0 += dE
                accept += 1

        if ib % 100 == 0:
            accept_ib = accept / (Nk * N * ib)
            if accept_ib > acceptance:
                dmax *= 1.05
            elif accept_ib < acceptance:
                dmax *= 0.95

        if Nb_skip < ib <= Nb_skip + Nb0 or ib > Nb_skip + Nb0 + Nb_skip:
            E_block = E(Theta, L) / N
            measure_counter += 1
            sum_E += E_block
            sum_E2 += E_block ** 2
            E_mean = sum_E / measure_counter
            sigma_E = np.sqrt((sum_E2 / measure_counter - E_mean ** 2) / measure_counter)
            f_energy_log.write(f"{sim} {ib} {E_block:.8f} {E_mean:.8f} {sigma_E:.8f} {T:.1f}\n")

            vortices, antivortices = count_vortices_with_positions(Theta, L)
            vortex_sum += len(vortices)
            antivortex_sum += len(antivortices)

        if ib == Nb_skip + Nb0 + Nb_skip + Nb:
            for (i, j) in vortices:
                f_vortices_all.write(f"{i} {j} +1 {sim}\n")
            for (i, j) in antivortices:
                f_vortices_all.write(f"{i} {j} -1 {sim}\n")

            f_theta_map_series.write(f"# sim {sim}\n")
            np.savetxt(f_theta_map_series, Theta[1:L+1, 1:L+1], fmt="%.6f")
            f_theta_map_series.write("\n")

    mean_vortex = vortex_sum / measure_counter
    mean_antivortex = antivortex_sum / measure_counter
    f_mean_vortices.write(f"{sim} {mean_vortex:.4f} {mean_antivortex:.4f}\n")
    total_vortex_sum += mean_vortex
    total_antivortex_sum += mean_antivortex


f_theta_map_series.close()
f_vortices_all.close()
f_energy_log.close()
f_mean_vortices.close()
