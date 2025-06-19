// sem_b.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define PI 3.14159265358979323846
#define MAX_L 230
#define MAX_W 20001

#include "ran1.c"  // Generator slucajnih brojeva

// Alokacija i oslobadjanje 2D matrice
double** alloc_matrix(int n, int m) {
    double** mat = (double**) malloc(n * sizeof(double*));
    for (int i = 0; i < n; i++)
        mat[i] = (double*) malloc(m * sizeof(double));
    return mat;
}

void free_matrix(double** mat, int n) {
    for (int i = 0; i < n; i++)
        free(mat[i]);
    free(mat);
}

int pbc(int x, int L) {
    return (x == 0) ? L : (x == L + 1 ? 1 : x);
}

double E(double** theta, int L, double J) {
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

double M_angle(double** theta, int L) {
    double mx = 0.0, my = 0.0;
    for (int i = 1; i <= L; i++) {
        for (int j = 1; j <= L; j++) {
            mx += cos(theta[i][j]);
            my += sin(theta[i][j]);
        }
    }
    return atan2(my, mx);
}

double theta2(double** theta, double phi, int L) {
    double sum = 0.0;
    for (int i = 1; i <= L; i++) {
        for (int j = 1; j <= L; j++) {
            double delta = theta[i][j] - phi;
            double wrapped = atan2(sin(delta), cos(delta));
            sum += wrapped * wrapped;
        }
    }
    return sum / (L * L);
}

int main() {
    double kT = 0.1, beta = 1.0 / kT, J = 1.0;
    int Nk = 4, Nb_skip = 1500, Nb = 10000;
    double acceptance = 0.4;
    double dmax_init = 1.0;
    int Ls[] = {4, 8, 16, 32, 48, 64, 80, 96, 128, 160, 192, 224};
    int num_L = sizeof(Ls) / sizeof(Ls[0]);

    long idum = -1208; // Seed za ran1

    FILE* fTheta2 = fopen("f_theta2_vs_L.dat", "w");
    fprintf(fTheta2, "# L  N  <theta^2>  ln(N)\n");

    for (int idx = 0; idx < num_L; idx++) {
        int L = Ls[idx];
        int N = L * L;
        double dmax = dmax_init;

        double** Theta = alloc_matrix(L+2, L+2);
        for (int i = 0; i <= L+1; i++)
            for (int j = 0; j <= L+1; j++)
                Theta[i][j] = ran1(&idum) * 2 * PI;

        double max_dE = 20.0;
        int w_size = (int)(max_dE * 1000) + 1;
        double* w = (double*) malloc(w_size * sizeof(double));
        for (int j = 0; j < w_size; j++)
            w[j] = exp(-beta * (j / 1000.0));

        double E0 = E(Theta, L, J);
        double accept = 0.0, sum_theta2 = 0.0;

        for (int ib = 1; ib <= Nb_skip + Nb; ib++) {
            for (int ik = 0; ik < Nk * N; ik++) {
                int i = 1 + (int)(ran1(&idum) * L);
                int j = 1 + (int)(ran1(&idum) * L);
                double old_theta = Theta[i][j];
                double dtheta = (ran1(&idum) - 0.5) * 2 * dmax;
                double new_theta = fmod(old_theta + dtheta + 2*PI, 2 * PI);

                double dE = 0.0;
                int ni[4] = {pbc(i+1,L), pbc(i-1,L), i, i};
                int nj[4] = {j, j, pbc(j+1,L), pbc(j-1,L)};

                for (int n = 0; n < 4; n++) {
                    double old_diff = old_theta - Theta[ni[n]][nj[n]];
                    double new_diff = new_theta - Theta[ni[n]][nj[n]];
                    dE -= J * (cos(new_diff) - cos(old_diff));
                }

                if (dE <= 0.0 || ((int)(1000*dE) < w_size && ran1(&idum) < w[(int)(1000*dE)])) {
                    Theta[i][j] = new_theta;
                    E0 += dE;
                    accept += 1.0;
                }
            }

            if (ib > Nb_skip) {
                double phiM = M_angle(Theta, L);
                sum_theta2 += theta2(Theta, phiM, L);
            }

            if (ib % 100 == 0) {
                double accept_ib = accept / (Nk * N * ib);
                if (accept_ib > acceptance) dmax *= 1.05;
                else if (accept_ib < acceptance) dmax *= 0.95;
            }
        }

        double mean_theta2 = sum_theta2 / Nb;
        double lnN = log((double) N);
        fprintf(fTheta2, "%4d %6d %15.9f %12.7f\n", L, N, mean_theta2, lnN);

        free(w);
        free_matrix(Theta, L+2);
    }

    fclose(fTheta2);
    return 0;
}
