#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define NRANSI
#include "ran1.c"
#include "gasdev.c"
             //  1D (an)harmonic oscillator

#define np 1                               /* number of objects */
#define nwmax 400
#define seed 68111
#define PI 3.14159265
double alf,alf1,alf2,bp;
main()
{
   long idum=(-2);
   int i, j, ei,ej, ngr,ko,k,brkor=100,ib,brblok=300,iw,ip,nw;
   int jpop,nsons,js,nwend,nuk;
   int icrit, icrmin,icrmax;
   double ampi, redu, xsons,nsaux;
   double olden, eav,eav2,endev,del=1.,w,rsons;
   double xu,tau,d,var,et;
   double eavb,eav2b, x[nwmax][np+1], xn[nwmax][np+1],x1,y1,del0;
   double y[nwmax][np+1];
   double dE,E[nwmax],accept,En[nwmax],psi2[nwmax],psi2n[nwmax];
   double fx[np+1],eold[nwmax],elocal[nwmax];
   double energy(double x[nwmax][np+1], int iw, double bp);                /* energy of system */
   double psi(double x[nwmax][np+1], int iw);         /* trial wave function*/

   FILE *output4, *output5;		      /* */
   FILE *output6, *output7, *output8;

   output7=fopen("konfigVMCho1_5.dat","r");
   output4 =fopen("edmcHO_05.dat","w");
   output6=fopen("eblokdmcHO_05.dat","w");

   alf=1.5;
   alf1=0.5-2.*alf*alf;
   bp=0.;
   printf("alf1\t%f\n",alf1);
   printf("a,bp=\t%f\t%f\n",alf,bp);


   eav=0.;
   eav2=0.;
   ngr=30;   //number of blocks to be discarded
   accept=0;
//   del0=0.4;
   nw=10;   //initial number of walkers
   tau=0.05;   //time-step
   d=0.5;       //parameters for the diffusion
   var=sqrt(2.*d*tau);   //parameters for the diffusion
   et=0.5;           //reference energy
   ko=ib-ngr;
   icrit=200;         //desired mean number of walkers
   icrmin = icrit - 20;
   icrmax = icrit + 20;
   redu = 0.5 * float ( icrmin + icrmax ) / float ( icrmax );
   ampi = 0.5 * float ( icrmin + icrmax ) / float ( icrmin );
   printf("tau,d,var\t%f\t%f\t%f\n",tau,d,var);
   printf("icrmin,icrmax\t%d\t%d\n",icrmin,icrmax);
   printf("icrmin,icrmax\t%f\t%f\n",redu,ampi);
   system("pause");
//
   fscanf(output7,"%d",&nw);  //reading the initial configuration
   printf("initial configuration\n");
   for (iw=0; iw<nw; iw++)
   {
   for (i=1; i<=np; i++){
     fscanf(output7,"%lf",&xu);
     printf("%lf\n",xu);
     x[iw][i]=xu;
    }
   psi2[iw]=psi(x,iw);   //initial probability
   eold[iw]=energy(x,iw,bp);  //initial walker energy
//   printf("initial\t\t probability\t\t %d\t%f\t%f\n",iw,psi2[iw],eold[iw]);
   }         /* initial configuration */
   fclose(output7);

   for(ib=1; ib<=brblok; ib++)  /*loop over blocks*/
   {
   eavb=0.;
   eav2b=0.;
   nuk=0;
   for (i=1; i<=brkor; i++)                     /* loop over steps  */
   {
    jpop=0;                                //counter for new walkers
        for(iw=0; iw<nw; iw++){               /*loop over walkers*/
          for(ip=1;ip<=np;ip++){              /*loop over particles*/
        fx[ip]=-4.*alf*x[iw][ip];
        xn[iw][ip]=x[iw][ip]+d*tau*fx[ip]+var*gasdev(&idum);      /* moving the walkers*/
      }

      E[iw]=energy(x,iw,bp);
      rsons =  exp ( tau * (et - 0.5 * (E[iw]+eold[iw])));   //branching
      nsons = int ( rsons + ran1(&idum) );
      if ( nsons>0 ){
   // modifing the number of suns to keep the population in balance
        if (nw>icrmax) {
           xsons = nsons * redu;
           nsaux = xsons + ran1 (&idum);
           nsons = int(nsaux);
           }
        if (nw<icrmin) {
           xsons = nsons * ampi;
           nsaux = xsons + ran1 (&idum);
           nsons = int(nsaux);
           }
//
        for (js = 1;js<=nsons;js++)   //making nsons copies
        {
         elocal[jpop]=E[iw];
         for(ip=1;ip<=np;ip++){
          y[jpop][ip]=xn[iw][ip];
         }
         jpop = jpop + 1;
      }  //end of loop over sons
      } //end of if  (nsons > 0)
      eavb+=E[iw]*nsons;
      eav2b+=E[iw]*nsons*E[iw]*nsons;
      } //end of loop over walkers
/*      system("pause");  */
      nw=jpop;         //new number of walkers
      nuk+=jpop;
 //     printf("%f\t%d\t%d\n",eavb,nw,nuk);
      for(iw=0;iw<nw;iw++){    //preparing the configuration for the next step
          eold[iw]=elocal[iw];
          for(ip=1;ip<=np;ip++){
          x[iw][ip]=y[iw][ip];
          }
          }    //end of preparing the configuration for the next step
      }  // end of loop over steps
      if(ib>ngr){     //accumulating the energy for bloks larger than ngr
      eav+=eavb/nuk;
      eav2+=eav2b/nuk;
//
      endev=sqrt(eav2/ko-eav*eav/ko/ko)/sqrt(ko);
      fprintf(output4, "%d\t%f\t%f\n",ib,eav/(ib-ngr),endev);
      fprintf(output6, "%d\t%f\t%d\n",ib,eavb/nuk,jpop);
      fflush(output6);
      } // endif (ib>ngr)
   } // end of loop over blocks
   fclose(output4);
   fclose(output6);
   printf("a,bp=\t%f\t%f\n",alf,bp);
   output8=fopen("konfigDMC.dat","w");
   /*---------writing the last configuration -------*/
for (iw=0; iw<nw; iw++)
   {
   for (i=1; i<=np; i++){
    fprintf(output8, "%f\n",x[iw][i]);
      fflush(output8 );
   }
}
   system("pause");
}
/*----------------------end of main program---------------------------*/

/* function returns energy of the system */
double energy (double x[nwmax][np+1],int iw, double bp)
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

/* function returns wave function of the system */
double psi (double x[nwmax][np+1],int iw)
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
