#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "ran1.c"

#define Nk 500 // broj koraka
#define Nw 500 // broj setaca
#define Nb 400 // broj blokova za akomulaciju bitnih velicina
#define Nb_skip 100 // broj blokova za ekvilibraciju

#define h_ 1.0 // reducirana Planckova konstanta
#define m 1.0 // masa cestice
#define K 0.5 // konstanta potencijalne energije V(x)=Kx
#define PI 3.14159265358979323846

// valna funkcija
double Psi(double x, double a) {
    if (x >= 0.0)
        return x * exp(-a * x * x);
    else
        return 0.0;
}

int main() {
    // varijacijski parametar
    double alpha[20];
    for (int i = 0; i < 20; i++) alpha[i] = 0.05 * (i + 1);

    FILE *falpha = fopen("E_alpha.dat", "w");
    fprintf(falpha, "# alpha - <E> - sigma_E - dx_max - acceptance\n");

    long seed = -208;

    for (int ia = 0; ia < 20; ia++) {
        double X[Nw] = {0}; // polozaji setaca
        double Xp[Nw] = {0}; // probni polozaji setaca
        double E[Nw] = {0}; // energija setaca
        double P[Nw] = {0}; // vjerojatnost
        double dx_max = 1.0; // maksimalni pomak setaca

        double accept = 0.0;

        // pocetne vrijednosti
        for (int iw = 0; iw < Nw; iw++) {
            X[iw] = 10.0 * ran1(&seed);
            P[iw] = Psi(X[iw], alpha[ia]) * Psi(X[iw], alpha[ia]);
            E[iw] = -(h_ * h_) / m * alpha[ia] * (2 * alpha[ia] * X[iw] * X[iw] - 3) + K * X[iw];
        }

        double sum_E = 0.0, sum_E2 = 0.0;
        for (int ib = 1; ib <= Nb + Nb_skip; ib++) {
            double sum_Ek = 0.0;
            int Nb_eff = ib - Nb_skip;
            for (int ik = 0; ik < Nk; ik++) {
                double sum_Ew = 0.0;
                for (int iw = 0; iw < Nw; iw++) {
                    double dx = 2.0 * (ran1(&seed) - 0.5) * dx_max;
                    Xp[iw] = X[iw] + dx;

                    // prihvacanje samo vrijednosti >= 0.0 radi ogranicenja valne funkcije
                    if (Xp[iw] >= 0.0) {
                        double Pp = Psi(Xp[iw], alpha[ia]) * Psi(Xp[iw], alpha[ia]);
                        double T = Pp / P[iw];
                        if (T >= 1.0 || ran1(&seed) < T) {
                            accept += 1.0;
                            X[iw] = Xp[iw];
                            P[iw] = Pp;
                            E[iw] = -(h_ * h_) / m * alpha[ia] * (2 * alpha[ia] * X[iw] * X[iw] - 3) + K * X[iw];
                        }
                    }
                    sum_Ew += E[iw];
                }
                if (Nb_eff > 0) sum_Ek += sum_Ew / Nw;
            }

            // prilagodba dx_max s obzirom na udio prihvacenih pomaka u energiji
            double accept_ib = accept / (ib * Nw * Nk);
            if (accept_ib < 0.5)
                dx_max *= 0.95;
            else if (accept_ib > 0.5)
                dx_max *= 1.5;

            if (Nb_eff > 0) {
                sum_E += sum_Ek / Nk;
                sum_E2 += (sum_Ek * sum_Ek) / (Nk * Nk);
            }
        }

        int Nb_eff_final = Nb;
        double mean_E = sum_E / Nb_eff_final;
        double sigma_E = sqrt((sum_E2 / Nb_eff_final - mean_E * mean_E) / (Nb_eff_final - 1));
        double acceptance = accept / (Nw * Nk * (Nb + Nb_skip));

        fprintf(falpha, "%6.3f %12.8f %12.8f %10.6f %7.3f\n", alpha[ia], mean_E, sigma_E, dx_max, acceptance*100.0);
    }

    double alpha_A = pow((sqrt(2.0 / PI) * K * m / (3.0 * h_)), 2.0 / 3.0); // analiticka vrijednost varijacijskog parametra
    fprintf(falpha, "\n# alpha(K=%.1f,m=%.1f) = %.5f\n", K, m, alpha_A);

    fclose(falpha);
    return 0;
}
