#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "ran1.c"

#define Na 224 //broj atoma
#define my2 8
#define Nb 600 //broj blokova
#define Nk 250 //broj koraka po bloku
#define Nw 10 //broj setaca
#define Nb_skip 150 //broj prvotno preskocenih koraka
#define Nbins 500 //broj binova za podrucje analize radijalne distribucijske funkcije
#define PI 3.14159265358979323846

double rho = 0.92; //pocetna gustoca u sustavu
double kT = 0.02; //temperatura sustava
double dmax = 0.1; //maksimalni pomak
double Lx, Ly, Lxp, Lyp, Lminp2;
double X[Nw+1][Na+2][2], Xp[Nw+1][Na+2][2], E[Nw+1], gr[Nbins+1];

double energy(double x[Nw+1][Na+2][2], int iw) { //funkcija energije sustava
    double sum = 0.0;
    for (int i = 1; i < Na; i++) {
        double rxi = x[iw][i][0];
        double ryi = x[iw][i][1];
        for (int j = i+1; j <= Na; j++) {
            double rxij = rxi - x[iw][j][0];
            double ryij = ryi - x[iw][j][1];
            if (rxij > Lxp) rxij -= Lx;
            if (rxij < -Lxp) rxij += Lx;
            if (ryij > Lyp) ryij -= Ly;
            if (ryij < -Lyp) ryij += Ly;
            double rij2 = rxij*rxij + ryij*ryij;
            if (rij2 <= Lminp2) {
                double r2 = 1.0 / rij2;
                double r6 = r2*r2*r2;
                double r12 = r6*r6;
                sum += r12 - r6; //Lennard-Jones tip potencijala
            }
        }
    }
    return 4.0 * sum;
}

int main() {
    long seed = -12345;  //seed za ran1()

    FILE *f_xy = fopen("xy.dat", "r");
    if (!f_xy) {
        printf("Error: Cannot open 'xy.dat'\n");
        return 1;
    }
    FILE *fE = fopen("E.dat", "w"); //ib, <Ek>, <Eb>, sigmaE
    FILE *fRDF = fopen("RDF.dat", "w"); //r, g(r)

    int mx = (int)(my2 * sqrt(3.0) + 0.5);
    if (Na != 2 * mx * my2) {
        printf("\nNisu uskladene postavke. Ugasi program.\n");
        return 1;
    }

    double S = Na / rho;
    double o = mx / (my2 * sqrt(3.0));
    Lx = sqrt(S * o);
    Ly = sqrt(S / o);
    double Lmin = fmin(Lx, Ly);
    double Lminp = Lmin / 2.0;
    Lxp = Lx / 2.0; //pola sirine podrucja
    Lyp = Ly / 2.0; //pola visine podrucja
    Lminp2 = Lminp * Lminp;
    double dr = Lminp / Nbins; //sirina podrucja za radijalnu distribucijsku funkciju

    printf("\n%d cestica u podrucju (%.6f x %.6f), L_min/2 = %.6f\n", Na, Lx, Ly, Lminp);

    for (int i = 1; i <= Na; i++) { //pocetni polozaji
        double rxi, ryi;
        fscanf(f_xy, "%lf %lf", &rxi, &ryi);
        for (int iw = 1; iw <= Nw; iw++) {
            X[iw][i][0] = rxi;
            X[iw][i][1] = ryi;
        }
    }
    fclose(f_xy);

    for (int iw = 1; iw <= Nw; iw++) { //pocetna energija sustava
        E[iw] = energy(X, iw);
    }

    printf("Pocetna energija: %.6f\n", E[1]);

    double sum_Eb = 0.0, sum_Eb2 = 0.0, reject_tot = 0.0;

    for (int ib = 1; ib <= Nb + Nb_skip; ib++) { //Metropolosov algoritam
        double reject = 0.0, sum_Ek = 0.0, sum_Ek2 = 0.0;

        for (int ik = 0; ik < Nk; ik++) {
            for (int iw = 1; iw <= Nw; iw++) {
                for (int i = 1; i <= Na; i++) {
                    Xp[iw][i][0] = fmod(X[iw][i][0] + dmax * (ran1(&seed) - 0.5) + Lx, Lx);
                    Xp[iw][i][1] = fmod(X[iw][i][1] + dmax * (ran1(&seed) - 0.5) + Ly, Ly);
                }
                double dE = energy(Xp, iw) - E[iw];
                if (dE > 0.0 && exp(-dE / kT) <= ran1(&seed)) {
                    reject += 1.0;
                    reject_tot += 1.0;
                    dE = 0.0;
                } else {
                    for (int i = 1; i <= Na; i++) {
                        X[iw][i][0] = Xp[iw][i][0];
                        X[iw][i][1] = Xp[iw][i][1];
                    }
                }
                E[iw] += dE;
                if (ib > Nb_skip) {
                    sum_Ek += E[iw] / Nw;
                    sum_Ek2 += E[iw]*E[iw] / Nw;
                    for (int i = 1; i < Na; i++) {
                        double rxi = X[iw][i][0];
                        double ryi = X[iw][i][1];
                        for (int j = i+1; j <= Na; j++) {
                            double rxij = rxi - X[iw][j][0];
                            double ryij = ryi - X[iw][j][1];
                            if (rxij > Lxp) rxij -= Lx; //aproksimacija minimalne slike
                            if (rxij < -Lxp) rxij += Lx;
                            if (ryij > Lyp) ryij -= Ly;
                            if (ryij < -Lyp) ryij += Ly;
                            double rij = sqrt(rxij*rxij + ryij*ryij); //udaljenost medu parom cestica (i,j)
                            if (rij < Lminp) {
                                int iring = (int)(rij / dr); //prsten kojem pripada cestica
                                if (iring < Nbins) gr[iring] += 2.0; //punjenje radijalne distribucijske funkcije za parove (i,j)
                            }
                        }
                    }
                }
            }
        }

        double accept_ib = 1.0 - reject / (Nk * Nw);
        if (accept_ib > 0.5) dmax *= 1.05; //optimizacijske korekcije
        else if (accept_ib < 0.5) dmax *= 0.95;

        if (ib > Nb_skip) {
            int Nb_eff = ib - Nb_skip;
            sum_Eb += sum_Ek / Nk;
            sum_Eb2 += sum_Ek2 / Nk;
            double sigmaE = 0.0;
            if (Nb_eff > 1)
                sigmaE = sqrt(sum_Eb2 / Nb_eff - (sum_Eb * sum_Eb) / (Nb_eff * Nb_eff)) / sqrt(Nb_eff - 1);
            fprintf(fE, "%6d %13.6f %13.6f %13.6f\n", ib, sum_Ek / Nk, sum_Eb / Nb_eff, sigmaE);
        }
    }

    fclose(fE);

    double accept = 1.0 - reject_tot / ((Nb + Nb_skip) * Nk * Nw);

    for (int ir = 1; ir <= Nbins; ir++) {
        double r_lower = ir * dr;
        double r_upper = (ir + 1) * dr;
        double shell = PI * (r_upper*r_upper - r_lower*r_lower);
        if (shell > 0.0) {
            gr[ir] /= shell * rho * Na * Nw * Nk * Nb; //normalizacija radijalne distribucijske funkcije
            fprintf(fRDF, "%11.6f %11.6f\n", r_lower + dr / 2.0, gr[ir]);
        }
    }

    fclose(fRDF);

    double E_out = 4.0 * PI * Na * (0.2 / pow(Lminp, 10.0) - 0.5 / pow(Lminp, 4.0));
    printf("\nPostotak prihvacenih pomaka: %.2f %%\n", accept * 100.0);
    printf("Energija unutar L_min/2: %.6f\n", sum_Eb / Nb);
    printf("Energija izvan L_min/2: %.6f\n", E_out);

    return 0;
}
