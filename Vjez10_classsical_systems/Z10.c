#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "ran1.c"

#define Na 340
#define my2 10
#define rho 0.6
#define Nb 1000
#define Nk 200
#define Nw 10
#define NbSkip 200
#define kT 0.1
#define d0 0.1
#define Nbins 500
#define PI 3.141592653589793

double Lx, Ly, Lxp, Lyp, Lminp2;

// Lennard-Jones energy
double energy(double x[Nw+1][Na+2][2], int iw) {
    double sum = 0.0;
    for (int i = 1; i < Na; i++) {
        double rxi = x[iw][i][0];
        double ryi = x[iw][i][1];
        for (int j = i+1; j <= Na; j++) {
            double rxij = rxi-x[iw][j][0];
            double ryij = ryi-x[iw][j][1];
            if (rxij > Lxp) rxij -= Lx;
            if (rxij < -Lxp) rxij += Lx;
            if (ryij > Lyp) ryij -= Ly;
            if (ryij < -Lyp) ryij += Ly;
            double rij2 = rxij*rxij+ryij*ryij;
            if (rij2 <= Lminp2 && rij2 > 1e-12) {
                double r2 = 1.0/rij2;
                double r6 = r2*r2*r2;
                double r12 = r6*r6;
                sum += r12-r6;
            }
        }
    }
    return 4.0*sum;
}

int main() {
    double X[Nw+1][Na+2][2] = {{{0}}};
    double Xp[Nw+1][Na+2][2] = {{{0}}};
    double E[Nw+1] = {0};
    double gr[Nbins+1] = {0};
    double dmax = d0, dE;

    long idum = -1;

    int mx = (int)(my2*sqrt(3.0)+0.5);
    if (Na != 2*mx*my2) {
        printf("\nNisu uskladene postavke s kodom za generiranje resetke.\n");
        system("PAUSE");
        return 0;
    }

    double S = (double)Na/rho;
    double o = (double)mx/(my2*sqrt(3.0));
    Lx = sqrt(S*o);
    Ly = sqrt(S/o);
    Lxp = Lx/2.0;
    Lyp = Ly/2.0;
    double Lmin = (Lx < Ly) ? Lx : Ly;
    double Lminp = Lmin/2.0;
    Lminp2 = Lminp*Lminp;
    double dr = Lminp/Nbins;

    FILE *fxy = fopen("xy.dat", "r");
    for (int i = 1; i <= Na; i++) {
        double rxi, ryi;
        fscanf(fxy, "%lf %lf", &rxi, &ryi);
        for (int iw = 1; iw <= Nw; iw++) {
            X[iw][i][0] = rxi;
            X[iw][i][1] = ryi;
        }
    }
    fclose(fxy);

    for (int iw = 1; iw <= Nw; iw++)
        E[iw] = energy(X, iw);
    
    printf("%d cestica u podrucju (%lf x %lf), Lmin/2 = %f.\n", Na, Lx, Ly, Lminp);
    double E_start = 0.0;
    for (int iw = 1; iw <= Nw; iw++)
        E_start += E[iw];
    E_start /= Nw;
    printf("Pocetna srednja energija: %f\n", E_start);

    double sum_Eb = 0.0, sum_Eb2 = 0.0;
    double reject_tot = 0.0;

    FILE *fE = fopen("E.dat", "w");
    FILE *fRDF = fopen("RDF.dat", "w");

    for (int ib = 1; ib <= Nb + NbSkip; ib++) {
        double reject = 0.0;
        double sum_Ek = 0.0, sum_Ek2 = 0.0;

        for (int ik = 1; ik <= Nk; ik++) {
            for (int iw = 1; iw <= Nw; iw++) {
                for (int i = 1; i <= Na; i++) {
                    Xp[iw][i][0] = fmod(X[iw][i][0]+dmax*(2.0*ran1(&idum)-1.0)+Lx, Lx);
                    Xp[iw][i][1] = fmod(X[iw][i][1]+dmax*(2.0*ran1(&idum)-1.0)+Ly, Ly);
                }
                dE = energy(Xp, iw)-E[iw];
                if (dE <= 0.0 || exp(-dE / kT) > ran1(&idum)) {
                    for (int i = 1; i <= Na; i++) {
                        X[iw][i][0] = Xp[iw][i][0];
                        X[iw][i][1] = Xp[iw][i][1];
                    }
                } else {
                    reject += 1.0;
                    reject_tot += 1.0;
                    dE = 0.0;
                }
                E[iw] += dE;

                if (ib > NbSkip) {
                    sum_Ek += E[iw]/Nw;
                    sum_Ek2 += E[iw]*E[iw]/Nw;

                    for (int i = 1; i < Na; i++) {
                        double rxi = X[iw][i][0];
                        double ryi = X[iw][i][1];
                        for (int j = i+1; j <= Na; j++) {
                            double rxij = rxi-X[iw][j][0];
                            double ryij = ryi-X[iw][j][1];
                            if (rxij > Lxp) rxij -= Lx;
                            if (rxij < -Lxp) rxij += Lx;
                            if (ryij > Lyp) ryij -= Ly;
                            if (ryij < -Lyp) ryij += Ly;
                            double rij = sqrt(rxij*rxij+ryij*ryij);
                            if (rij < Lminp) {
                                int iring = (int)(rij/dr);
                                if (iring < Nbins)
                                    gr[iring] += 2.0;
                            }
                        }
                    }
                }
            }
        }

        reject /= (Nk*Nw);
        double accept_ib = 1.0-reject;
        if (accept_ib > 0.5) dmax *= 1.05;
        else if (accept_ib < 0.5) dmax *= 0.95;

        if (ib > NbSkip) {
            int Nb_eff = ib-NbSkip;
            sum_Eb += sum_Ek/Nk;
            sum_Eb2 += sum_Ek2/Nk;
            double sigmaE = (Nb_eff > 1) ? sqrt(sum_Eb2/Nb_eff-(sum_Eb*sum_Eb)/(Nb_eff*Nb_eff))/sqrt(Nb_eff-1) : 0.0;
            fprintf(fE, "%5d %11.6f %11.6f %11.6f\n", ib, sum_Ek/Nk, sum_Eb/Nb_eff, sigmaE);
        }
    }
    double n_samples = Nb * Nk * Nw;
    for (int ir = 1; ir <= Nbins; ir++) {
        double r_lower = ir*dr;
        double r_upper = (ir+1)*dr;
        double shell = PI*(r_upper*r_upper-r_lower*r_lower);
        if (shell > 0.0) {
            gr[ir] /= (n_samples*shell*rho*Na);
            fprintf(fRDF, "%11.6f %11.6f\n", r_lower+dr/2.0, gr[ir]);
        }
    }

    fclose(fE);
    fclose(fRDF);

    double E_out = 4.0*PI*Na*(1.0/pow(Lminp, 12.0)-1.0/pow(Lminp, 6.0));
    printf("\nPostotak prihvacenih pomaka: %.2f %%\n", 100.0*(1.0-reject_tot/((Nb+NbSkip)*Nk*Nw)));
    int Nb_eff = Nb;
    if (Nb_eff > 0) printf("Energija unutar L_min/2: %.6f\n", sum_Eb / Nb_eff);
    else printf("Energija unutar L_min/2: N/A (no data accumulated)\n");
    printf("Energija izvan L_min/2: %.6f\n\n", E_out);

    return 0;
}
