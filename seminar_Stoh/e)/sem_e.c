// sem_e.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "ran1.c"

#define PI 3.14159265358979323846
#define J 1.0 // integral izmjene
#define Nk 4 // broj koraka po cestici
#define Nb_skip 2000 // broj koraka za ekvilibraciju
#define Nb 8000 // broj koraka za evoluciju sustava na temperaturi T
#define acceptance 0.4 // udio prihvacanja 40%

const int L = 256; // sirina sustava
const int N = L * L; // broj cestica u sustavu
const double Tmin = 1.0;
const double Tmax = 1.2;
const double dT = 0.01;

// periodicni rubni uvjeti
int pbc(int x, int L) {
    return (x == 0) ? L : (x == L + 1 ? 1 : x);
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
    long idum = -1208; // seed za ra1
    FILE *fsus = fopen("T_x_Cv_M_256x256.dat", "w");
    FILE *fmagnetization = fopen("magnetization_256x256.dat", "w");

    fprintf(fsus, "# T - x_scal - x_vec - Cv - <M>\n");
    fprintf(fmagnetization, "# ib - T - <M>b - <M> - sigma_M\n");

    double **Theta = alloc_matrix(L+2, L+2); // 2D matrica spinova (kuteva u xy-ravnini)

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

        for (int i = 0; i <= L+1; i++)
            for (int j = 0; j <= L+1; j++)
                Theta[i][j] = 2 * PI * ran1(&idum);

        double E0 = E(Theta, L); // pocetna energija sustava

        double sum_Mx = 0.0, sum_Mx2 = 0.0;
        double sum_My = 0.0, sum_My2 = 0.0;
        double sum_M = 0.0, sum_M2 = 0.0;
        double sum_E = 0.0, sum_E2 = 0.0;
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

                /*
                Magnetizacija cijelog sustava racuna se uvazavajuci vektorske komponente spina S(x,y) kao M^2=Mx^2+My^2, gdje
                je Mx=cos(S) i My=sin(S). Mozemo magnetsku susceptibilnost racunati tako da u obzir uzimamo samo normu vektora
                magnetizacije M (chi_scal), no mozemo ju racunati tako sto uvazavamo vektorske komponente magnetizacije Mx i
                My (chi_vec). Racuna se i toplinski kapacitet Cv kako bi se uocilo oko koje temperature dolazi do pojave faznog
                prijelaza. 
                */
                double Mx = 0.0, My = 0.0;
                for (int i = 1; i <= L; i++) {
                    for (int j = 1; j <= L; j++) {
                        Mx += cos(Theta[i][j]);
                        My += sin(Theta[i][j]);
                    }
                }

                Mx /= N;
                My /= N;

                sum_Mx += Mx;
                sum_Mx2 += Mx * Mx;
                sum_My += My;
                sum_My2 += My * My;
                double M_block = sqrt(Mx * Mx + My * My);
                sum_M += M_block;
                sum_M2 += M_block * M_block;
                double M_mean = sum_M / Nb_eff;
                double sigma_M = sqrt((sum_M2 / Nb_eff - M_mean * M_mean) / Nb_eff);
                if (ib % 10 == 0) { // za minimiziranje broja podataka
                    fprintf(fmagnetization, "%7d %4.2f %11.8f %11.8f %11.8f\n", ib_G, T, M_block, M_mean, sigma_M);
                }
            }
        }

        double mean_M = sum_M / Nb_eff;
        double mean_M2 = sum_M2 / Nb_eff;
        double mean_Mx = sum_Mx / Nb_eff;
        double mean_My = sum_My / Nb_eff;
        double mean_Mx2 = sum_Mx2 / Nb_eff;
        double mean_My2 = sum_My2 / Nb_eff;
        double mean_E = sum_E / Nb_eff;

        // racunanje magnetske susceptibilnosti
        double chi_vec = (mean_Mx2 - mean_Mx * mean_Mx + mean_My2 - mean_My * mean_My) * N / T;
        double chi_scal = (mean_M2 - mean_M * mean_M) * N / T;

        // racunanje specificnog toplinskog kapaciteta
        double Cv = (sum_E2 / Nb_eff - mean_E * mean_E) * N / (T * T);

        fprintf(fsus, "%6.3f %13.6f %13.6f %12.6f %11.8f\n", T, chi_scal, chi_vec, Cv, mean_M);
        fprintf(fmagnetization, "\n");

        free(w);
    }

    free_matrix(Theta, L+2);
    fclose(fsus);
    fclose(fmagnetization);
    return 0;
}
