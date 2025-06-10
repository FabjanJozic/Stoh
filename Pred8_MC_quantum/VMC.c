#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define NRANSI
#include "ran1.c"
             //  1D harmonic oscillator

#define np 1                               /* number of objects */
#define nw 10                          /*number of walkers */
#define seed 68111
#define PI 3.14159265		      /* seed for srand48 */
double alf,alf1,alf2,bp;
main()
{
   long idum=(-2);
   int i, j, ei,ej, ngr,ko,k,brkor=500,ib,brblok=100,iw,ip;
   double olden, eav,eav2,endev,del=2.,w;
   double eavb,eav2b, x[nw][np+1], xn[nw][np+1],x1,y1,del0;
   double dE,E[nw],accept,En[nw],psi2[nw],psi2n[nw];
   double energy(double x[nw][np+1], int iw, double bp);                /* energy of system */
   double psi(double x[nw][np+1], int iw);         /* trial wave function*/

   FILE *output4, *output5;
   FILE *output6, *output7;

   output4 =fopen("eaHO_0_6.dat","w");
   output6=fopen("eblockaHO_0_6.dat","w");

   alf=0.6;          /* variational parameter */
   alf1=0.5-2.*alf*alf;
   bp=0.125; /*constant for the anharmonic potential*/
   printf("alf,bp=\t%f\t%f\n",alf,bp);
   printf("alf1\t%f\n",alf1);


   eav=0.0;
   eav2=0.;
   ngr=10;   /*number of blocks to be rejected */
   accept=0;
   del0=1.;   /*initial distribution of walkers */
   for (iw=0; iw<nw; iw++)
   {
   for (i=1; i<=np; i++){
     x[iw][i]= del0*(2.*ran1(&idum)-1.);   //x-koord
/*     y[iw][i]= del0*(2.*ran1(&idum)-1.);   //y-koord  */
/*     z[iw][i]= del0*(2.*ran1(&idum)-1.);  //z-koord     */
    printf("%f\n",x[iw][i]);
    }
   psi2[iw]=psi(x,iw);   //initial probability
   printf("initial \t\t probability\t\t %d\t%f\n",iw,psi2[iw]);
   }         /* initial configuration */

   for(ib=1; ib<=brblok; ib++)  /*loop over blocks*/
   {
   eavb=0.;
   eav2b=0.;
   for (i=1; i<=brkor; i++)                     /* loop over steps  */
   {
        for(iw=0; iw<nw; iw++){               /*loop over walkers*/
          for(ip=1;ip<=np;ip++){              /*loop over particles*/
         xn[iw][ip]=x[iw][ip]+del*(2.*ran1(&idum)-1.);               /* suggesting the walker move*/
      }
      psi2n[iw]=psi(xn,iw); //new wave function**2
      w=psi2n[iw]/psi2[iw];
      if ( (w<1.) && (w < ran1(&idum)) )
      {
         accept=accept+1./brkor/brblok/nw;   //counts rejected steps
      }
      else{
          for(ip=1; ip<=np;ip++){    //in case of acceptance the configuration and w.f. squared are updated
           x[iw][ip]=xn[iw][ip];
           psi2[iw]=psi2n[iw];
           }
           }
      if(ib>ngr)
      {
      E[iw]=energy(x,iw,bp);   //accumulate averages
      eavb+=E[iw];
      eav2b+=E[iw]*E[iw];
      }
      } //end of loop over walkers
      }  // end of loop over steps
      if(ib>ngr){
      eav+=eavb/brkor/nw;
      eav2+=eav2b/brkor/nw;
//
      ko=ib-ngr;
      endev=sqrt(eav2/ko-eav*eav/ko/ko)/sqrt(ko);
      fprintf(output4, "%d\t%f\t%f\n",ib,eav/(ib-ngr),endev);
      fprintf(output6, "%d\t%f\n",ib,eavb/brkor/nw);
      fflush(output6);
      } // end if (ib>ngr)
   } // end of loop over blocks
   printf("acceptance ratio \t%f\n",1.-accept);
   fclose(output4);
   fclose(output6);
   printf("a,bp=\t%f\t%f\n",alf,bp);
   printf("energy, st. dev=\t%f\t%f\n",eav/(brblok-ngr),endev);
   output7=fopen("konfigVMCaho0_6.dat","w");
/*---------write the last configuration -------*/
fprintf(output7,"%d\n",nw);
for (iw=0; iw<nw; iw++)
   {
   for (i=1; i<=np; i++){
    fprintf(output7, "%f\n",x[iw][i]);
      fflush(output7 );
   }
}
   system("pause");
}
/*----------------------end of main program---------------------------*/

/* function returns energy of the system */
double energy (double x[nw][np+1],int iw, double bp)
{
   int i;
   double sum,rxi,ryi,rzi,r2;
   sum = 0.;
   for(i=1; i<=(np); i++){
        rxi=x[iw][i];
      r2=rxi*rxi;
      sum+=alf1*r2+alf+bp*r2*r2;
   }
   return (sum);
}

/* function returns squared trial wave function of the system */
double psi (double x[nw][np+1],int iw)
{
   int i;
   double sum,rxi,ryi,rzi,r2,expo;
   sum = 1.;
   for(i=1; i<=(np); i++){
        rxi=x[iw][i];
      r2=rxi*rxi;
      expo=-2.*alf*r2;
      sum*=exp(expo);
   }
   return (sum);
}
