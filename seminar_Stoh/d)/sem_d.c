// sem_d.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "ran1.c"

#define PI 3.14159265358979323846
#define J 1.0 // integral izmjene
#define Nk 4 // broj koraka po cestici
#define Nb_skip 2000 // broj blokova za ekvilibraciju
#define Nb 8000 // broj blokova za evoluciju sustava na temperaturi T
#define acceptance 0.4 // udio prihvacanja 40%

const int L = 64; // sirina sustava
const int N = L * L; // broj cestica u sustavu
const double Tmin = 0.5;
const double Tmax = 1.5;
const double dT = 0.1;

// periodicni rubni uvjeti
int pbc(int x, int L) {
    if (x == 0) return L;
    else if (x == L + 1) return 1;
    else return x;
}

// energija sustava spinova
double E(double **theta, int L) {
    double energy = 0.0;
    for (int i = 1; i <= L; i++) {
        for (int j = 1; j <= L; j++) {
            double delta1 = theta[i][j] - theta[pbc(i+1,L)][j];
            double delta2 = theta[i][j] - theta[i][pbc(j+1,L)];
            energy += -J * (cos(delta1) + cos(delta2));
        }
    }
    return energy;
}

// alokacija i oslobadanje 2D matrice
double **alloc_matrix(int n, int m) {
    double **mat = (double **)malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++)
        mat[i] = (double *)malloc(m * sizeof(double));
    return mat;
}

void free_matrix(double **mat, int n) {
    for (int i = 0; i < n; i++)
        free(mat[i]);
    free(mat);
}

int main() {
    long idum = -2024; // seed za ran1
    double **Theta = alloc_matrix(L+2, L+2); // 2D matrica spinova (kuteva u xy-ravnini)

    for (int i = 0; i <= L+1; i++)
        for (int j = 0; j <= L+1; j++)
            Theta[i][j] = 0.0; // pocetni uvjeti za T=0.5

    FILE *fout = fopen("temp_ene_Cv_vor_antivor_64x64.dat", "w");
    FILE *f_energy = fopen("energy_64x64.dat", "w");

    fprintf(fout, "# T - <E> - Cv - N_vor - N_antivor - N_vor/N - N_antivor/N\n");
    fprintf(f_energy, "# ib - T - <E>b - <E> - sigma_E\n");

    int ib_G = 1; // globalni indeks bloka

    for (double T = Tmin; T <= Tmax + 1e-6; T += dT) { // petlja po temperaturama
        double beta = 1.0 / T;

        // stvaranje w[j] liste kao u b) zadatku
        double max_dE = 20.0;
        int w_size = (int)(max_dE * 1000) + 1;
        double *w = (double *)malloc(w_size * sizeof(double));
        for (int j = 0; j < w_size; j++)
            w[j] = exp(-beta * (j / 1000.0));

        double dmax = 1.0; // maksimalna vrijednost kuta theta
        int accept = 0, every_step = 0;

        double E0 = E(Theta, L); // pocetna energija sustava

        double sum_E = 0.0, sum_E2 = 0.0;
        int sum_vortex = 0, sum_antivortex = 0;
        int Nb_eff = 0;

        // Metropolisov algoritam
        for (int ib = 1; ib <= Nb_skip + Nb; ib++, ib_G++) {
            for (int ik = 0; ik < Nk * N; ik++) {
                int i = 1 + (int)(ran1(&idum) * L);
                int j = 1 + (int)(ran1(&idum) * L);
                double old_theta = Theta[i][j];
                double dtheta = (ran1(&idum) - 0.5) * 2 * dmax;
                double new_theta = fmod(old_theta + dtheta + 2*PI, 2*PI);

                int ni[4] = {pbc(i+1,L), pbc(i-1,L), i, i};
                int nj[4] = {j, j, pbc(j+1,L), pbc(j-1,L)};
                double dE = 0.0;
                for (int n = 0; n < 4; n++) {
                    double old_diff = old_theta - Theta[ni[n]][nj[n]];
                    double new_diff = new_theta - Theta[ni[n]][nj[n]];
                    dE -= J * (cos(new_diff) - cos(old_diff));
                }

                every_step++;
                if (dE <= 0.0 || ((int)(1000*dE) < w_size && ran1(&idum) < w[(int)(1000*dE)])) {
                    Theta[i][j] = new_theta;
                    accept++;
                    E0 += dE;
                }
            }

            // adaptiranje dmax s obzirom na udio prihvacenih koraka
            if (ib % 5 == 0) {
                double acc_ratio = (double)accept / every_step;
                if (acc_ratio > acceptance) dmax *= 1.05;
                else if (acc_ratio < acceptance) dmax *= 0.95;
            }
        
        if (ib >= Nb_skip) {
            Nb_eff = ib - Nb_skip + 1;
            double E_block = E(Theta, L) / N;
            sum_E += E_block;
            sum_E2 += E_block * E_block;
            double E_mean = sum_E / Nb_eff;
            double sigma_E = sqrt((sum_E2 / Nb_eff - E_mean * E_mean) / Nb_eff);
            if (ib % 10 == 0) { // za minimiziranje broja podataka
                fprintf(f_energy, "%7d %4.2f %11.8f %11.8f %11.8f\n", ib_G, T, E_block, E_mean, sigma_E);
            }

            // detektiranje i racunanje broja vrtloga i antivrtloga kao u c) zadatku
            for (int i = 1; i < L; i++) {
                for (int j = 1; j < L; j++) {
                    double a0 = Theta[i][j];
                    double a1 = Theta[i][j+1];
                    double a2 = Theta[i+1][j+1];
                    double a3 = Theta[i+1][j];

                    double winding = 0.0;
                    winding += atan2(sin(a1 - a0), cos(a1 - a0));
                    winding += atan2(sin(a2 - a1), cos(a2 - a1));
                    winding += atan2(sin(a3 - a2), cos(a3 - a2));
                    winding += atan2(sin(a0 - a3), cos(a0 - a3));

                    if (fabs(winding - 2*PI) < 0.1)
                        sum_vortex++;
                    else if (fabs(winding + 2*PI) < 0.1)
                        sum_antivortex++;
                }
            }
        }
        }

        double mean_E = sum_E / Nb_eff;
        double Cv = (sum_E2 / Nb_eff - mean_E * mean_E) * N / (T * T); // racunanje specificnog toplinskog kapaciteta
        double Nvortex = (double)sum_vortex / N;
        double Nantivortex = (double)sum_antivortex / N;

        fprintf(fout, "%4.2f %12.8f %12.8f %8d %8d %12.6f %12.6f\n", T, mean_E, Cv, sum_vortex, sum_antivortex, Nvortex, Nantivortex);
        fprintf(f_energy, "\n");

        free(w);
    }

    free_matrix(Theta, L+2);
    fclose(fout);
    fclose(f_energy);
    return 0;
}
