// sem_c.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "ran1.c" // generator slucajnih brojeva

#define PI 3.14159265358979323846
#define T0 10.0 // temperatura sustava prije quencha
#define T_quench 0.5 // quench temperatura
#define J 1.0 // integral izmjene

#define Nk 5 // broj koraka po cestici
#define Nb_skip 4000 // broj blokova za ekvilibraciju
#define Nb0 2500 // broj blokova prije quencha
#define Nb 2500 // broj blokova nakon quencha
#define Nsim 100 // broj uzastopnih simulacija
#define acceptance 0.4 // udio prihvacanja 40%

const int L = 32; // sirina sustava
const int N = L * L; // broj cestica u sustavu

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
            double delta1 = theta[i][j] - theta[pbc(i+1, L)][j];
            double delta2 = theta[i][j] - theta[i][pbc(j+1, L)];
            energy += -J * (cos(delta1) + cos(delta2));
        }
    }
    return energy;
}

// alokacija i oslobadanje 2D matrica
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
    FILE *f_mean_vortices_all_sim = fopen("mean_vortices_all_sim_32x32.dat", "w"); // srednji broj vrtloga za svaku simulaciju
    
    fprintf(f_mean_vortices_all_sim, "# is - <vortices> - <antivortices> - N_vortices - N_antivortices\n");

    long idum = -1208; // seed za ran1

    for (int is = 1; is <= Nsim; is++) { // petlja po simulacijama
        FILE *f_energy = fopen("energy_32x32.dat", "w"); // energija u sustavu prije i poslije quencha
        FILE *f_theta_map = fopen("theta_map_32x32.dat", "w"); // mapa spinova (kuteva u xy-ravnini)
        FILE *f_vortices_all_per_sim = fopen("vortices_all_per_sim_32x32.dat", "w"); // pozicije vrtloga i antivrtloga prije i poslije quencha

        fprintf(f_energy, "# ib - <E>b - <E> - sigma_E - T\n");
        fprintf(f_vortices_all_per_sim, "# i - j - type - ib\n");

        double dmax = 1.0; // maksimalna vrijednost kuta theta
        double **Theta = alloc_matrix(L+2, L+2); // 2D matrica spinova (kuteva u xy-ravnini)
        for (int i = 0; i <= L+1; i++)
            for (int j = 0; j <= L+1; j++)
                Theta[i][j] = 2 * PI * ran1(&idum);

        double T = T0, beta = 1.0 / T;

        // stvaranje w[j] liste kao u b) zadatku
        double max_dE = 20.0;
        int w_size = (int)(max_dE * 1000) + 1;
        double *w = (double *)malloc(w_size * sizeof(double));
        for (int j = 0; j < w_size; j++)
            w[j] = exp(-beta * (j / 1000.0));

        double sum_E = 0.0, sum_E2 = 0.0;
        int Nb_eff = 0;
        double sum_vortex = 0.0, sum_antivortex = 0.0;
        int accept = 0, every_step = 0;

        double E0 = E(Theta, L); // pocetna energija sustava

        // Metropolisov algoritam
        for (int ib = 1; ib <= Nb_skip + Nb0 + Nb_skip + Nb; ib++) {
            if (ib == Nb_skip + Nb0 + 1) { // uvjet za quench
                T = T_quench;
                beta = 1.0 / T;
                for (int j = 0; j < w_size; j++)
                    w[j] = exp(-beta * (j / 1000.0));
            }

            for (int ik = 0; ik < Nk * N; ik++) {
                int i = 1 + (int)(ran1(&idum) * L);
                int j = 1 + (int)(ran1(&idum) * L);
                double old_theta = Theta[i][j];
                double dtheta = (ran1(&idum) - 0.5) * 2 * dmax;
                double new_theta = fmod(old_theta + dtheta + 2*PI, 2*PI);

                int ni[4] = {pbc(i+1,L), pbc(i-1,L), i, i}; // prvi susjedi
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
            double accept_rate = (double)accept / (double)every_step;
            if (ib % 5 == 0) {
                if (accept_rate > acceptance)
                    dmax *= 1.05;
                else if (accept_rate < acceptance)
                    dmax *= 0.95;
            }
            
            // racunanje srednje vrijednosti energije i standardne devijacije 
            if ((Nb_skip < ib && ib <= Nb_skip + Nb0) || (ib > Nb_skip + Nb0 + Nb_skip)) {
                double E_block = E(Theta, L) / N;
                Nb_eff++;
                sum_E += E_block;
                sum_E2 += E_block * E_block;
                double E_mean = sum_E / Nb_eff;
                double sigma_E = sqrt((sum_E2 / Nb_eff - E_mean * E_mean) / Nb_eff);
                fprintf(f_energy, "%6d %14.8f %14.8f %14.8f %4.1f\n", ib, E_block, E_mean, sigma_E, T);
            
                // odredivanje vrtloga i antivrtloga
                int vortices = 0, antivortices = 0;
                for (int i = 1; i < L; i++) {
                    for (int j = 1; j < L; j++) {
                        double angles[5] = {Theta[i][j], Theta[i+1][j], Theta[i+1][j+1], Theta[i][j+1], Theta[i][j]}; // prvi susjedi spina (i,j)
                        double winding = 0.0;
                        for (int k = 0; k < 4; k++) {
                            double diff = angles[k+1] - angles[k];
                            winding += atan2(sin(diff), cos(diff));
                        }
                        if (fabs(winding - 2*PI) < 0.5) { // pronalazak vrtloga
                            vortices++;
                            fprintf(f_vortices_all_per_sim, "%3d %3d +1 %4d\n", i, j, ib);
                        } else if (fabs(winding + 2*PI) < 0.5) { // pronalazak antivrtloga
                            antivortices++;
                            fprintf(f_vortices_all_per_sim, "%3d %3d -1 %4d\n", i, j, ib);
                        }
                    }
                }
                sum_vortex += vortices;
                sum_antivortex += antivortices;

                // zapis mape spinova (kuteva u xy-ravnini)
                if (vortices != 0 || antivortices != 0) {
                    fprintf(f_theta_map, "# ib %6d\n", ib);
                    for (int i = 1; i <= L; i++) {
                        for (int j = 1; j <= L; j++)
                            fprintf(f_theta_map, "%.6f ", Theta[i][j]);
                        fprintf(f_theta_map, "\n");
                    }
                }
            }
        }

        double mean_vortex = sum_vortex / Nb_eff;
        double mean_antivortex = sum_antivortex / Nb_eff;
        fprintf(f_mean_vortices_all_sim, "%4d %.5f %.5f %.0f %.0f\n", is, mean_vortex, mean_antivortex, sum_vortex, sum_antivortex);

        free(w);
        free_matrix(Theta, L+2);

        fclose(f_energy);
        fclose(f_theta_map);
        fclose(f_vortices_all_per_sim);
    }

    fclose(f_mean_vortices_all_sim);

    return 0;

    }

