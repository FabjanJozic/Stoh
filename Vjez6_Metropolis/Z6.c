#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "ran1.c" 

#define NbSkip 50
#define Nb 100
#define Nk 300
#define Nw 5000
#define Nacc 300

double Psi(double r);

int main()
{
    long idum = -2024;
    int ib, ik, iw, k;
    double acc = 0.0, accP;
    double x[4][Nw];
    double xp[4], dx, rp, r2, Swf, Skf, Sbf = 0.0, Sbf2 = 0.0;
    double dX[4] = {0.0, 5.0, 5.0, 5.0}; // indexing from 1
    double P[Nw], f[Nw], Pp, T, tmp, scale;
    double dDX = 0.05;

    FILE *ff = fopen("r_H300.dat", "w");
    FILE *frNw = fopen("rNw_H300.dat", "w");

    fprintf(ff, "# Block   <r> (block average)   <r> (cumulative average)\n");
    fprintf(frNw, "# Step        x               y              z\n");

    // Initial walker positions
    for (iw = 0; iw < Nw; iw++)
    {
        r2 = 0.0;
        for (k = 1; k <= 3; k++)
        {
            x[k][iw] = 34.0*(ran1(&idum)-0.5); // between -17 and 17
            r2 += x[k][iw] * x[k][iw];
        }
        rp = sqrt(r2);
        tmp = Psi(rp);
        P[iw] = tmp * tmp;
        f[iw] = rp;
        fprintf(frNw, "%7d %13.6f %13.6f %13.6f\n", 0, x[1][iw], x[2][iw], x[3][iw]);
    }
    fprintf(frNw, "\n");
    for (ib = 1 - NbSkip; ib <= Nb; ib++)
    {
        Skf = 0.0;
        if (ib == 1)
            acc = 0.0;
        for (ik = 1; ik <= Nk; ik++)
        {
            Swf = 0.0;
            for (iw = 0; iw < Nw; iw++)
            {
                r2 = 0.0;
                for (k = 1; k <= 3; k++)
                {
                    dx = (2.0*ran1(&idum)-1.0)*dX[k];
                    xp[k] = x[k][iw] + dx;
                    r2 += xp[k] * xp[k];
                }
                rp = sqrt(r2);
                tmp = Psi(rp);
                Pp = tmp*tmp;
                T = Pp / P[iw];
                if (T >= 1.0 || ran1(&idum) <= T)
                {
                    for (k = 1; k <= 3; k++)
                        x[k][iw] = xp[k];
                    P[iw] = Pp;
                    f[iw] = rp;
                    acc += 1.0;
                }
                Swf += f[iw];
            }

            if (((ib-1+NbSkip)*Nk+ik) % Nacc == 0 && ib < 1)
            {
                accP = acc/(Nacc*Nw);
                scale = (accP > 0.5) ? (1.0+dDX) : (1.0-dDX);
                for (k = 1; k <= 3; k++)
                    dX[k] *= scale;
                if (ib % 10)
                    printf("ib = %d, accP = %3.1f\n", ib, accP * 100.0);
                acc = 0.0;
            }
            if (ib > 0)
                Skf += Swf / Nw;
        }
        if (ib > 0)
        {
            Sbf += Skf/Nk;
            Sbf2 += (Skf/Nk)*(Skf/Nk);
            accP = acc/(ib*Nw*Nk);
            scale = (accP > 0.5) ? (1.0+dDX) : (1.0-dDX);
            for (k = 1; k <= 3; k++)
                dX[k] *= scale;
            if (ib % (Nb / 10) == 0)
                printf("ib = %d, accP = %3.1f\n", ib, accP * 100.0);
            for (iw = 0; iw < Nw; iw++)
            {
                fprintf(frNw, "%7d %13.6f %13.6f %13.6f\n", (ib-1)*Nk+ik, x[1][iw], x[2][iw], x[3][iw]);
            }
            fprintf(frNw, "\n");
            fprintf(ff, "%7d %16.7f %16.7f\n", ib, Skf/Nk, Sbf/ib);
        }
    }

    double ave_f = Sbf/Nb;
    double sig_f = sqrt((Sbf2/Nb)-ave_f*ave_f);

    printf("\n accP = %4.1lf\n", accP * 100.0);
    printf("\n max dx = %6.4lf, %6.4lf, %6.4lf\n", dX[1], dX[2], dX[3]);
    printf("\n <r> = %8.5lf +- %8.5lf \n", ave_f, sig_f);

    fclose(ff);
    fclose(frNw);
    return 0;
}

double Psi(double r)
{
    return (27.0-18.0*r+2.0*r*r)*exp(-r/3.0); // |300> state
}
